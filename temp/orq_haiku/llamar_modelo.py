#!/usr/bin/env python3
"""COPIA TEMPORAL del ORQ para probar Haiku 5.5. NO es el del repo.

El único cambio de fondo es el **transporte**. En vez de `call_model` (formato OpenAI), habla la
API de Mensajes de Anthropic y devuelve **la forma que espera el bucle** —`choices[0].message` con
`content`, `reasoning_content`, `tool_calls` y `finish_reason`—, así el resto del ORQ corre igual
y sin tocar una línea.

Traducciones:

- el `system` sale de `messages` y va al parámetro `system`;
- las herramientas: `function.parameters` → `input_schema`;
- `role: "tool"` → bloque `tool_result` dentro de un mensaje de usuario; los resultados
  consecutivos se juntan en un solo mensaje, como pide la API;
- el turno del asistente → bloques `tool_use`, y **se guarda el turno crudo** que devolvió la API
  (con sus bloques de pensamiento) para reenviarlo tal cual cuando el bucle lo pida de vuelta;
- el razonamiento: `thinking` adaptativo con `display: summarized` → `reasoning_content`.

La clave se lee de `ANTHROPIC_API_KEY` y **nunca se imprime ni se guarda**: el cuerpo que se
devuelve para el crudo no lleva cabeceras.
"""

import json
import os
import pathlib
import time
import urllib.error
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/orq_haiku → la raíz del repo
URL = "https://api.anthropic.com/v1/messages"
VERSION_API = "2023-06-01"

# Turnos del asistente tal como los devolvió la API, por los ids de sus llamadas: el bucle rearma
# el mensaje, así que acá se reconoce por los ids y se reenvía el original.
_CRUDOS = {}


def _clave():
    clave = os.environ.get("ANTHROPIC_API_KEY")
    if not clave:
        raise SystemExit("falta ANTHROPIC_API_KEY en el entorno (correr con bash -ic)")
    return clave


def _firma(mensaje):
    return tuple(llamada["id"] for llamada in mensaje.get("tool_calls") or [])


def _herramientas(tools):
    salida = []
    for t in tools or []:
        f = t.get("function", {})
        salida.append({"name": f["name"],
                       "description": f.get("description", ""),
                       "input_schema": f.get("parameters") or {"type": "object"}})
    return salida


def _solo_resultados(mensaje):
    return all(b.get("type") == "tool_result" for b in mensaje.get("content") or [])


def _mensajes(mensajes):
    """Devuelve (system, mensajes en formato Anthropic)."""
    system = None
    salida = []
    for m in mensajes:
        rol = m.get("role")
        if rol == "system":
            system = m.get("content") or ""
        elif rol == "user":
            salida.append({"role": "user",
                           "content": [{"type": "text", "text": m.get("content") or ""}]})
        elif rol == "assistant":
            bloques = _CRUDOS.get(_firma(m))
            if bloques is None:  # sin crudo reconocible: se rearma con lo que hay
                bloques = []
                if m.get("content"):
                    bloques.append({"type": "text", "text": m["content"]})
                for llamada in m.get("tool_calls") or []:
                    bloques.append({"type": "tool_use", "id": llamada["id"],
                                    "name": llamada["function"]["name"],
                                    "input": json.loads(llamada["function"]["arguments"] or "{}")})
            salida.append({"role": "assistant", "content": bloques})
        elif rol == "tool":
            bloque = {"type": "tool_result", "tool_use_id": m.get("tool_call_id"),
                      "content": m.get("content") or ""}
            if salida and salida[-1]["role"] == "user" and _solo_resultados(salida[-1]):
                salida[-1]["content"].append(bloque)
            else:
                salida.append({"role": "user", "content": [bloque]})
    return system, salida


def _respuesta(d):
    """Traduce la respuesta de Anthropic a la forma que consume el bucle."""
    bloques = d.get("content") or []
    textos = [b.get("text") or "" for b in bloques if b.get("type") == "text"]
    pensamientos = [b.get("thinking") or "" for b in bloques if b.get("type") == "thinking"]
    llamadas = [{"id": b["id"], "type": "function",
                 "function": {"name": b["name"],
                              "arguments": json.dumps(b.get("input") or {}, ensure_ascii=False)}}
                for b in bloques if b.get("type") == "tool_use"]
    if llamadas:
        _CRUDOS[tuple(c["id"] for c in llamadas)] = bloques
    uso = d.get("usage") or {}
    prompt = uso.get("input_tokens")
    completion = uso.get("output_tokens")
    return {
        "model": d.get("model"),
        "choices": [{
            "index": 0,
            "finish_reason": "tool_calls" if d.get("stop_reason") == "tool_use" else "stop",
            "message": {"role": "assistant",
                        "content": "".join(textos) or None,
                        "reasoning_content": "".join(pensamientos) or None,
                        "tool_calls": llamadas or None},
        }],
        "usage": {"prompt_tokens": prompt, "completion_tokens": completion,
                  "total_tokens": (prompt or 0) + (completion or 0),
                  "prompt_cache_hit_tokens": uso.get("cache_read_input_tokens"),
                  "prompt_cache_miss_tokens": prompt,
                  "thinking_tokens": (uso.get("output_tokens_details") or {}).get("thinking_tokens"),
                  "anthropic": uso},
        "stop_reason": d.get("stop_reason"),
        "_stream_chunks_crudos": None,
        "_anthropic_crudo": d,
    }


def llamar_modelo(config, mensajes, herramientas):
    """Devuelve (cuerpo enviado, respuesta ensamblada). Misma firma que el del repo."""
    modelo = config["modelo"]
    system, msgs = _mensajes(mensajes)
    cuerpo = {"model": modelo["alias"],
              "max_tokens": modelo.get("max_tokens", 16384),
              "output_config": {"effort": modelo.get("effort", "high")},
              "thinking": {"type": "adaptive", "display": "summarized"},
              "messages": msgs}
    if system:
        cuerpo["system"] = system
    if herramientas:
        cuerpo["tools"] = _herramientas(herramientas)

    peticion = urllib.request.Request(
        URL, data=json.dumps(cuerpo, ensure_ascii=False).encode(),
        headers={"x-api-key": _clave(), "anthropic-version": VERSION_API,
                 "content-type": "application/json"},
        method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(peticion, timeout=1800) as r:
            d = json.loads(r.read())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"la API contestó {e.code}: "
                         f"{e.read().decode('utf-8', 'replace')[:800]}")
    segundos = round(time.time() - t0, 1)
    respuesta = _respuesta(d)
    respuesta["_segundos"] = segundos
    uso = respuesta["usage"]
    print(f"    [haiku {modelo.get('effort')}] {segundos} s · {uso['prompt_tokens']} in / "
          f"{uso['completion_tokens']} out ({uso['thinking_tokens']} pensando) · "
          f"{respuesta['stop_reason']}")
    return cuerpo, respuesta
