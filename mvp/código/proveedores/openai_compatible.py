"""El proveedor **OpenAI-compatible**: DeepSeek, GLM (z.ai) y Grok (x.ai).

Hablan el mismo cuerpo y la misma respuesta que el resto del MVP ya consume —`messages`, `tools`
anidadas, y de vuelta `choices[0].message` con `content`, `reasoning_content` y `tool_calls`—, así
que acá no hay traducción: solo la URL, el id, la clave y el `extra` de cada host.

Sin streaming: un POST y la respuesta entera. El razonamiento se pide con `reasoning_effort`, que
se pone **después** del `extra` para que el esfuerzo de la llamada siempre gane.
"""

import json
import time
import urllib.error
import urllib.request

from .claves import ErrorDeLlamada, cabeceras, exigir

TIMEOUT = 900  # segundos: una sola espera, sin el «600 s entre bytes» del streaming


def llamar(cfg, mensajes, herramientas, conv_id=None):
    """Devuelve (cuerpo enviado, respuesta). La respuesta ya viene en la forma de OpenAI."""
    url = cfg["url"]
    exigir(url)
    cuerpo = {"model": cfg["id"], "messages": mensajes}
    if herramientas:
        cuerpo["tools"] = herramientas
    cuerpo.update(cfg.get("extra") or {})
    if cfg.get("esfuerzo"):
        cuerpo["reasoning_effort"] = cfg["esfuerzo"]

    peticion = urllib.request.Request(
        url, data=json.dumps(cuerpo, ensure_ascii=False).encode(),
        headers=cabeceras("openai_compatible", url, conv_id), method="POST")
    t0 = time.time()
    try:
        with urllib.request.urlopen(peticion, timeout=TIMEOUT) as respuesta_http:
            datos = json.loads(respuesta_http.read())
    except urllib.error.HTTPError as error:
        raise ErrorDeLlamada(f"la API contestó {error.code} ({cfg['id']}): "
                             f"{error.read().decode('utf-8', 'replace')[:800]}")

    respuesta = dict(datos)
    respuesta["_segundos"] = round(time.time() - t0, 1)
    uso = respuesta.get("usage") or {}
    # Los tokens de pensamiento vienen con otro nombre en estos hosts: se normalizan para que la
    # columna sea la misma que la de Anthropic.
    detalles = uso.get("completion_tokens_details") or {}
    if uso.get("thinking_tokens") is None and detalles.get("reasoning_tokens") is not None:
        uso["thinking_tokens"] = detalles["reasoning_tokens"]
        respuesta["usage"] = uso
    return cuerpo, respuesta
