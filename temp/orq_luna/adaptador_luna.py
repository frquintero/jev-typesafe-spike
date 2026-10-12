#!/usr/bin/env python3
"""La llamada al agente por la familia `responses` (OpenCode Go), **con herramientas**.

Es la pieza que el transporte del repo todavía **no** tiene: `openai_responses.llamar` se detiene
si le llegan `tools`, porque la familia las quiere en otra forma y no estaba probada. Acá se prueba
el contrato en el scratch, sin tocar el repo.

Traduce en los dos sentidos:

- `mensajes` (la forma interna: `system`, `user`, `assistant` con `tool_calls`, `tool`) →
  `instructions` + `input` (items: `message`, `function_call`, `function_call_output`).
- la respuesta (`output[]`: `reasoning`, `message`, `function_call`) → `choices[0].message` con
  `content` y `tool_calls`, que es lo que consume el bucle del ORQ sin enterarse.

**Los items de razonamiento se devuelven.** Con herramientas, la familia `responses` exige que el
turno siguiente lleve el item de razonamiento que precedió a la llamada. Como el bucle solo
transporta `content` y `reasoning_content`, los items crudos viajan codificados en
`reasoning_content` y se reconstruyen al armar el turno siguiente.
"""

import json
import pathlib
import sys
import time
import urllib.error
import urllib.request
import uuid

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/orq_luna → la raíz del repo
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from proveedores import claves, resolver  # noqa: E402

TIMEOUT = 900


def _herramientas(herramientas):
    """La oferta en la forma de `responses`: la función va **plana**, no bajo `function`."""
    return [{"type": "function",
             "name": h["function"]["name"],
             "description": h["function"].get("description", ""),
             "parameters": h["function"]["parameters"]}
            for h in herramientas or []]


def _items(mensajes):
    """El historial, en items de `responses`."""
    items = []
    for mensaje in mensajes:
        rol = mensaje.get("role")
        if rol in ("system", "developer"):
            continue  # el system va en `instructions`
        if rol == "user":
            items.append({"role": "user",
                          "content": [{"type": "input_text", "text": mensaje.get("content") or ""}]})
        elif rol == "assistant":
            if mensaje.get("reasoning_content"):
                try:
                    items.extend(json.loads(mensaje["reasoning_content"]))
                except (TypeError, ValueError):
                    pass
            for llamada in mensaje.get("tool_calls") or []:
                items.append({"type": "function_call", "call_id": llamada["id"],
                              "name": llamada["function"]["name"],
                              "arguments": llamada["function"]["arguments"] or "{}"})
            if mensaje.get("content"):
                items.append({"role": "assistant",
                              "content": [{"type": "output_text", "text": mensaje["content"]}]})
        elif rol == "tool":
            items.append({"type": "function_call_output", "call_id": mensaje.get("tool_call_id"),
                          "output": mensaje.get("content") or ""})
    return items


def _traducir(datos, segundos):
    """La respuesta de `responses` en la forma interna (la que consume el bucle)."""
    salida = datos.get("output") or []
    contenido = "".join(
        parte.get("text") or ""
        for item in salida if item.get("type") == "message"
        for parte in item.get("content") or [] if parte.get("type") == "output_text")
    llamadas = [{"id": item.get("call_id") or item.get("id"), "type": "function",
                 "function": {"name": item.get("name"),
                              "arguments": item.get("arguments") or "{}"}}
                for item in salida if item.get("type") == "function_call"]
    razonamiento = [item for item in salida if item.get("type") == "reasoning"]

    if llamadas:
        terminó = "tool_calls"
    elif datos.get("status") == "completed":
        terminó = "stop"
    else:
        terminó = ((datos.get("incomplete_details") or {}).get("reason")
                   or datos.get("status") or "sin estado")

    mensaje = {"role": "assistant", "content": contenido or None}
    if llamadas:
        mensaje["tool_calls"] = llamadas
    if razonamiento:
        mensaje["reasoning_content"] = json.dumps(razonamiento, ensure_ascii=False)

    uso = datos.get("usage") or {}
    entrada = uso.get("input_tokens")
    cacheados = (uso.get("input_tokens_details") or {}).get("cached_tokens")
    return {
        "id": datos.get("id"), "object": "chat.completion", "model": datos.get("model"),
        "choices": [{"index": 0, "finish_reason": terminó, "message": mensaje}],
        "usage": {"prompt_tokens": entrada,
                  "completion_tokens": uso.get("output_tokens"),
                  "thinking_tokens": (uso.get("output_tokens_details") or {}).get("reasoning_tokens"),
                  "prompt_cache_hit_tokens": cacheados,
                  "prompt_cache_miss_tokens": (entrada - cacheados
                                               if entrada is not None and cacheados is not None
                                               else None)},
        "_segundos": segundos,
        "_respuesta": datos,
    }


def llamar_modelo(config, mensajes, herramientas):
    """Una llamada del bucle: devuelve (cuerpo enviado, respuesta en la forma interna)."""
    modelo = config["modelo"]
    cfg = resolver(modelo["alias"], modelo.get("esfuerzo"))
    url = cfg["url"]
    claves.exigir(url)

    sistema = "\n\n".join(m.get("content") or "" for m in mensajes if m.get("role") == "system")
    cuerpo = {"model": cfg["id"], "input": _items(mensajes),
              "tools": _herramientas(herramientas), "tool_choice": "auto"}
    if sistema:
        cuerpo["instructions"] = sistema
    if cfg.get("max_output_tokens"):
        cuerpo["max_output_tokens"] = cfg["max_output_tokens"]
    if cfg.get("esfuerzo"):
        cuerpo["reasoning"] = {"effort": cfg["esfuerzo"]}

    cabeceras = claves.cabeceras("openai_responses", url, None)
    cabeceras["x-opencode-session"] = str(uuid.uuid4())
    peticion = urllib.request.Request(
        url, data=json.dumps(cuerpo, ensure_ascii=False).encode(), headers=cabeceras, method="POST")

    t0 = time.time()
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta_http:
            datos = json.loads(respuesta_http.read())
    except urllib.error.HTTPError as error:
        raise SystemExit(f"HTTP {error.code}: {error.read().decode('utf-8', 'replace')[:800]}")

    respuesta = _traducir(datos, round(time.time() - t0, 1))
    uso = respuesta["usage"]
    print(f"    [luna] {respuesta['_segundos']} s · {uso.get('prompt_tokens')} in "
          f"({uso.get('prompt_cache_hit_tokens')} caché) / {uso.get('completion_tokens')} out · "
          f"{respuesta['choices'][0]['finish_reason']}")
    return cuerpo, respuesta
