"""El proveedor de la familia **`responses`** (Responses API de OpenAI), por OpenCode Go.

La familia —**GPT 6 Luna**, y por ahí también los `grok` de xAI y `muse-spark` cuando haya
créditos— devuelve otra forma que `openai_compatible` no parsea: `output[].content[].text` y
`usage.input_tokens`, no `choices[0].message`. Acá se traduce a la forma interna de siempre, y el
resto del MVP no se entera.

El contrato está **medido**: primero en el scratch (`temp/datos-test/paso2_seco_v1_luna.py`, cuatro
corridas el 10-10), y después con herramientas (`temp/orq_luna/adaptador_luna.py`, la consulta 1
del Sol el 10-10: dos turnos, una llamada, `function_call` → `function_call_output`).

**Dos formas de entrada, y no es capricho:**

- **Sin herramientas y con un solo `user`** —el caso de UT y DATOS— va el camino ya medido: el
  `system` como `instructions` y el material como `input` de texto pelado. Es exactamente el
  cuerpo con el que corrieron las extracciones que están en la base.
- **Con herramientas o con historial** —el caso del ORQ— va el historial en items (`message`,
  `function_call`, `function_call_output`) y la oferta de `tools` **plana**, que es como la quiere
  esta familia.

**Los items de razonamiento se devuelven.** Con herramientas, el turno siguiente tiene que llevar
el item de razonamiento que precedió a la llamada. Como el bucle del ORQ solo transporta
`content` y `reasoning_content`, los items crudos viajan codificados en `reasoning_content` y se
reconstruyen al armar el turno siguiente.

`finish_reason` **se sintetiza**: con llamadas, `tool_calls`; si no, `completed` → `stop`, y
cualquier otro estado, el motivo del corte tal como lo traiga `incomplete_details` —así el acto lo
registra en su motivo.
"""

import json
import time
import urllib.request
import uuid

from .claves import cabeceras, exigir, pedir_json

TIMEOUT = 900  # segundos: una sola espera, como el resto del MVP


def traducir(datos, segundos):
    """La respuesta de `responses` en la forma interna (la de OpenAI que consume el MVP)."""
    salida = datos.get("output") or []
    contenido = "".join(
        parte.get("text") or ""
        for item in salida if item.get("type") == "message"
        for parte in item.get("content") or []
        if parte.get("type") == "output_text")
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

    mensaje = {"role": "assistant", "content": contenido or None, "reasoning_content": None}
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
        "usage": {
            "prompt_tokens": entrada,
            "completion_tokens": uso.get("output_tokens"),
            "thinking_tokens": (uso.get("output_tokens_details") or {}).get("reasoning_tokens"),
            "prompt_cache_hit_tokens": cacheados,
            "prompt_cache_miss_tokens": (entrada - cacheados
                                         if entrada is not None and cacheados is not None else None),
        },
        "_segundos": segundos,
        "_respuesta": datos,  # el cuerpo tal como llegó, para diagnosticar
    }


def _herramientas(herramientas):
    """La oferta en la forma de `responses`: la función va **plana**, no bajo `function`."""
    return [{"type": "function",
             "name": herramienta["function"]["name"],
             "description": herramienta["function"].get("description", ""),
             "parameters": herramienta["function"]["parameters"]}
            for herramienta in herramientas or []]


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


def _camino_simple(mensajes, herramientas):
    """El camino ya medido (UT y DATOS): sin herramientas, un solo `user`, el texto pelado."""
    if herramientas:
        return None
    sistema = [m.get("content") or "" for m in mensajes if m.get("role") == "system"]
    usuarios = [m.get("content") or "" for m in mensajes if m.get("role") == "user"]
    otros = [m.get("role") for m in mensajes if m.get("role") not in ("system", "user")]
    if otros or len(usuarios) != 1:
        return None
    return "\n\n".join(sistema), usuarios[0]


def llamar(cfg, mensajes, herramientas, conv_id=None):
    """Devuelve (cuerpo enviado, respuesta en la forma de siempre)."""
    url = cfg["url"]
    exigir(url)
    sistema = "\n\n".join(m.get("content") or "" for m in mensajes if m.get("role") == "system")

    simple = _camino_simple(mensajes, herramientas)
    if simple is not None:
        cuerpo = {"model": cfg["id"], "input": simple[1]}
        if simple[0]:
            cuerpo["instructions"] = simple[0]
    else:
        cuerpo = {"model": cfg["id"], "input": _items(mensajes),
                  "tools": _herramientas(herramientas), "tool_choice": "auto"}
        if sistema:
            cuerpo["instructions"] = sistema
    if cfg.get("max_output_tokens"):
        cuerpo["max_output_tokens"] = cfg["max_output_tokens"]
    cuerpo.update(cfg.get("extra") or {})
    if cfg.get("esfuerzo"):
        cuerpo["reasoning"] = {"effort": cfg["esfuerzo"]}

    # Go pide su propia sesión por conversación; sin `conv_id`, una por llamada.
    cabeceras_http = cabeceras("openai_responses", url, conv_id)
    cabeceras_http["x-opencode-session"] = conv_id or str(uuid.uuid4())

    peticion = urllib.request.Request(
        url, data=json.dumps(cuerpo, ensure_ascii=False).encode(),
        headers=cabeceras_http, method="POST")
    t0 = time.time()
    datos = pedir_json(peticion, cfg, TIMEOUT)

    return cuerpo, traducir(datos, round(time.time() - t0, 1))
