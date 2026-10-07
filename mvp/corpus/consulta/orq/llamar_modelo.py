#!/usr/bin/env python3
"""Hace una llamada al modelo dentro del bucle: mensajes + herramientas.

El transporte es `call_model` (`niveles/run_niveles.py`): es el único código que lee la clave, y
ya devuelve el mensaje del asistente con `content`, `reasoning_content`, `tool_calls` y
`finish_reason` ensamblados del stream.

La API es stateless: cada llamada reenvía todo el historial. Lo que abarata el reenvío es el caché
de prefijo, y por eso el system y la lista de herramientas no se tocan entre turnos.
"""

import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[4]  # mvp/corpus/consulta/orq → la raíz del repo
sys.path.insert(0, str(RAIZ / "niveles"))
from run_niveles import call_model  # noqa: E402


def llamar_modelo(config, mensajes, herramientas):
    """Devuelve (cuerpo enviado, respuesta ensamblada)."""
    return call_model(config["modelo"]["version"], config["modelo"]["alias"], None,
                      messages=mensajes, tools=herramientas)
