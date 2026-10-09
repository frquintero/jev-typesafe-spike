"""El proveedor **Anthropic**: Haiku 5.5 (y cualquier Claude de la casa).

Habla la API de Mensajes y **devuelve la forma que el resto del MVP consume** —`choices[0].message`
con `content`, `reasoning_content` y `tool_calls`—, así que el bucle del ORQ y los corredores no
saben que del otro lado hay otro protocolo.

Traducciones de ida:

- el `system` sale de `messages` y va al parámetro `system`;
- las herramientas: `function.parameters` → `input_schema`;
- `role: "tool"` → bloque `tool_result` dentro de un mensaje de **usuario**; los resultados
  consecutivos se juntan en uno solo, como pide la API;
- el turno del asistente → bloques `tool_use`, y se guarda el turno crudo que devolvió la API
  (con sus bloques de pensamiento) para reenviarlo tal cual cuando el bucle lo pida de vuelta.

De vuelta: `content[]` (`thinking` / `text` / `tool_use`) y `stop_reason` → la forma de siempre,
con el `usage` traducido a los nombres que ya usa la traza (`prompt_tokens`, `completion_tokens`,
`prompt_cache_hit_tokens`, `thinking_tokens`).

Sin streaming, y con el razonamiento adaptativo encendido (`display: summarized`, para poder verlo
en el crudo). El esfuerzo va en `output_config.effort`; `budget_tokens` no se usa: en Haiku 5.5 da
400.
"""

import json
import time
import urllib.error
import urllib.request

from .claves import ErrorDeLlamada, cabeceras, exigir

TIMEOUT = 900

# Turnos del asistente tal como los devolvió la API, por los ids de sus llamadas: el bucle rearma
# el mensaje, así que acá se reconoce por los ids y se reenvía el original.
_TURNOS = {}


def _firma(mensaje):
    return tuple(llamada["id"] for llamada in mensaje.get("tool_calls") or [])


def _herramientas(tools):
    salida = []
    for herramienta in tools or []:
        funcion = herramienta.get("function", {})
        salida.append({"name": funcion["name"],
                       "description": funcion.get("description", ""),
                       "input_schema": funcion.get("parameters") or {"type": "object"}})
    return salida


def _solo_resultados(mensaje):
    return all(b.get("type") == "tool_result" for b in mensaje.get("content") or [])


def _mensajes(mensajes):
    """Devuelve (system, mensajes en formato Anthropic)."""
    system = None
    salida = []
    for mensaje in mensajes:
        rol = mensaje.get("role")
        if rol == "system":
            system = mensaje.get("content") or ""
        elif rol == "user":
            salida.append({"role": "user",
                           "content": [{"type": "text", "text": mensaje.get("content") or ""}]})
        elif rol == "assistant":
            bloques = _TURNOS.get(_firma(mensaje))
            if bloques is None:  # sin crudo reconocible: se rearma con lo que hay
                bloques = []
                if mensaje.get("content"):
                    bloques.append({"type": "text", "text": mensaje["content"]})
                for llamada in mensaje.get("tool_calls") or []:
                    bloques.append({"type": "tool_use", "id": llamada["id"],
                                    "name": llamada["function"]["name"],
                                    "input": json.loads(llamada["function"]["arguments"] or "{}")})
            salida.append({"role": "assistant", "content": bloques})
        elif rol == "tool":
            bloque = {"type": "tool_result", "tool_use_id": mensaje.get("tool_call_id"),
                      "content": mensaje.get("content") or ""}
            if salida and salida[-1]["role"] == "user" and _solo_resultados(salida[-1]):
                salida[-1]["content"].append(bloque)
            else:
                salida.append({"role": "user", "content": [bloque]})
    return system, salida


def _respuesta(datos):
    """Traduce la respuesta de Anthropic a la forma que consume el resto del MVP."""
    bloques = datos.get("content") or []
    textos = [b.get("text") or "" for b in bloques if b.get("type") == "text"]
    pensamientos = [b.get("thinking") or "" for b in bloques if b.get("type") == "thinking"]
    llamadas = [{"id": b["id"], "type": "function",
                 "function": {"name": b["name"],
                              "arguments": json.dumps(b.get("input") or {}, ensure_ascii=False)}}
                for b in bloques if b.get("type") == "tool_use"]
    if llamadas:
        _TURNOS[tuple(llamada["id"] for llamada in llamadas)] = bloques
    uso = datos.get("usage") or {}
    prompt = uso.get("input_tokens")
    completion = uso.get("output_tokens")
    return {
        "model": datos.get("model"),
        "choices": [{
            "index": 0,
            "finish_reason": {"tool_use": "tool_calls", "max_tokens": "length"}.get(
                datos.get("stop_reason"), "stop"),
            "message": {"role": "assistant",
                        "content": "".join(textos) or None,
                        "reasoning_content": "".join(pensamientos) or None,
                        "tool_calls": llamadas or None},
        }],
        "usage": {"prompt_tokens": prompt,
                  "completion_tokens": completion,
                  "total_tokens": (prompt or 0) + (completion or 0),
                  "prompt_cache_hit_tokens": uso.get("cache_read_input_tokens"),
                  "prompt_cache_miss_tokens": prompt,
                  "thinking_tokens": (uso.get("output_tokens_details") or {}).get("thinking_tokens"),
                  "anthropic": uso},
        "stop_reason": datos.get("stop_reason"),
    }


def llamar(cfg, mensajes, herramientas, conv_id=None):
    """Devuelve (cuerpo enviado, respuesta en la forma de siempre)."""
    url = cfg["url"]
    exigir(url)
    system, msgs = _mensajes(mensajes)
    cuerpo = {"model": cfg["id"],
              "max_tokens": cfg.get("max_tokens", 16384),  # obligatorio en esta API
              "thinking": {"type": "adaptive", "display": "summarized"},
              "messages": msgs}
    if cfg.get("esfuerzo"):
        cuerpo["output_config"] = {"effort": cfg["esfuerzo"]}
    if system:
        # El system es el prefijo invariante (las reglas del acto): se marca para el caché, que en
        # esta API hay que pedir. El primer pedido lo escribe; los siguientes lo leen.
        cuerpo["system"] = [{"type": "text", "text": system,
                             "cache_control": {"type": "ephemeral"}}]
    if herramientas:
        cuerpo["tools"] = _herramientas(herramientas)

    peticion = urllib.request.Request(
        url, data=json.dumps(cuerpo, ensure_ascii=False).encode(),
        headers=cabeceras("anthropic", url, conv_id), method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta_http:
            datos = json.loads(respuesta_http.read())
    except urllib.error.HTTPError as error:
        raise ErrorDeLlamada(f"la API contestó {error.code} ({cfg['id']}): "
                             f"{error.read().decode('utf-8', 'replace')[:800]}")

    respuesta = _respuesta(datos)
    respuesta["_segundos"] = round(time.time() - t0, 1)
    return cuerpo, respuesta
