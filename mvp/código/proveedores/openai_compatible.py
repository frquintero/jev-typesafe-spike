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

from .claves import cabeceras, exigir

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
        raise SystemExit(f"la API contestó {error.code} ({cfg['id']}): "
                         f"{error.read().decode('utf-8', 'replace')[:800]}")

    respuesta = dict(datos)
    respuesta["_segundos"] = round(time.time() - t0, 1)
    respuesta["_stream_chunks_crudos"] = None  # sin streaming: no hay frames que guardar
    return cuerpo, respuesta
