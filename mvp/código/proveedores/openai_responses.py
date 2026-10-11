"""El proveedor de la familia **`responses`** (Responses API de OpenAI), por OpenCode Go.

Es el transporte que faltaba: la familia `responses` —**GPT 6 Luna**, y por ahí también los
`grok` de xAI y `muse-spark` cuando haya créditos— devuelve otra forma que `openai_compatible` no
parsea: `output[].content[].text` y `usage.input_tokens`, no `choices[0].message`. Acá se traduce a
la forma interna de siempre, y el resto del MVP no se entera.

El contrato está **medido en el scratch** (`temp/datos-test/paso2_seco_v1_luna.py`, cuatro corridas
sobre `preparacion_cafe` el 10-10): `[SISTEMA]` va como `instructions` —invariante, y es lo que
cachea Go: la segunda llamada reusó 1.839 de 1.842 tokens de entrada—, `[TAREA]` como `input`, y el
esfuerzo como `reasoning.effort`. Sin streaming: un POST y la respuesta entera.

**Los cuatro esfuerzos son `none`, `low`, `medium`, `high` y, además, `xhigh` y `max`; el defecto
del modelo es `medium`** (no `low`). El alias fija el suyo y la llamada puede pisarlo.

Lo que este transporte **no** hace, a propósito y en voz alta:

- **`tools`**: la familia `responses` las quiere en otra forma y no se ha probado; si llegan, se
  detiene con un motivo en vez de mandar un cuerpo que no se sabe leer. El ORQ no usa esta vía.
- **Más de un mensaje `user`, o roles que no sean `system`/`user`**: la familia tiene su forma para
  el historial y acá no se inventa. UT y DATOS mandan un solo `user`.

`finish_reason` **se sintetiza**: `completed` → `stop` (es lo que exigen los corredores) y,
si `status` no es `completed`, el motivo del corte tal como lo traiga `incomplete_details` —así el
acto lo registra en su motivo, que es justo lo que hace falta para diagnosticar.
"""

import json
import time
import urllib.error
import urllib.request
import uuid

from .claves import ErrorDeLlamada, cabeceras, exigir

TIMEOUT = 900  # segundos: una sola espera, como el resto del MVP


def traducir(datos, segundos):
    """La respuesta de `responses` en la forma interna (la de OpenAI que consume el MVP)."""
    contenido = "".join(
        parte.get("text") or ""
        for item in datos.get("output") or []
        if item.get("type") == "message"
        for parte in item.get("content") or []
        if parte.get("type") == "output_text")
    razonamiento = "\n".join(
        json.dumps(item, ensure_ascii=False)
        for item in datos.get("output") or []
        if item.get("type") == "reasoning")

    if datos.get("status") == "completed":
        terminó = "stop"
    else:
        terminó = ((datos.get("incomplete_details") or {}).get("reason")
                   or datos.get("status") or "sin estado")

    uso = datos.get("usage") or {}
    entrada = uso.get("input_tokens")
    cacheados = (uso.get("input_tokens_details") or {}).get("cached_tokens")
    return {
        "id": datos.get("id"), "object": "chat.completion", "model": datos.get("model"),
        "choices": [{"index": 0, "finish_reason": terminó,
                     "message": {"role": "assistant", "content": contenido,
                                 "reasoning_content": razonamiento or None}}],
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


def _partes(mensajes, herramientas):
    """El `instructions` (lo invariante) y el `input` (el material)."""
    if herramientas:
        raise ErrorDeLlamada("este transporte todavía no manda `tools`: la familia `responses` las "
                             "quiere en otra forma y no se ha probado (mvp/proveedores.md §6)")
    sistema = [m.get("content") or "" for m in mensajes if m.get("role") == "system"]
    usuario = [m.get("content") or "" for m in mensajes if m.get("role") == "user"]
    otras = [m.get("role") for m in mensajes if m.get("role") not in ("system", "user")]
    if otras:
        raise ErrorDeLlamada(f"este transporte solo sabe de `system` y `user`; llegaron {otras}")
    if len(usuario) != 1:
        raise ErrorDeLlamada(f"este transporte espera un solo mensaje `user`; llegaron {len(usuario)}")
    return "\n\n".join(sistema), usuario[0]


def llamar(cfg, mensajes, herramientas, conv_id=None):
    """Devuelve (cuerpo enviado, respuesta en la forma de siempre)."""
    url = cfg["url"]
    exigir(url)
    instrucciones, entrada = _partes(mensajes, herramientas)

    cuerpo = {"model": cfg["id"], "input": entrada}
    if instrucciones:
        cuerpo["instructions"] = instrucciones
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
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta_http:
            datos = json.loads(respuesta_http.read())
    except urllib.error.HTTPError as error:
        raise ErrorDeLlamada(f"la API contestó {error.code} ({cfg['id']}): "
                             f"{error.read().decode('utf-8', 'replace')[:800]}")

    return cuerpo, traducir(datos, round(time.time() - t0, 1))
