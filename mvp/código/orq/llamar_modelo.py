#!/usr/bin/env python3
"""Hace una llamada al modelo dentro del bucle: mensajes + herramientas.

El transporte es `mvp/código/proveedores/`: el `alias` del config elige el proveedor y devuelve el
mensaje del asistente en la forma de siempre (`content`, `reasoning_content`, `tool_calls`), sin
streaming. La clave la lee solo `proveedores/claves.py`, y nunca se guarda.

La API es stateless: cada llamada reenvía todo el historial. Lo que abarata el reenvío es el caché
de prefijo, y por eso el system y la lista de herramientas no se tocan entre turnos.
"""

import pathlib
import sys

CODIGO = pathlib.Path(__file__).resolve().parents[1]  # mvp/código
sys.path.insert(0, str(CODIGO))
from proveedores import llamar  # noqa: E402


def llamar_modelo(config, mensajes, herramientas):
    """Devuelve (cuerpo enviado, respuesta ensamblada)."""
    modelo = config["modelo"]
    return llamar(modelo["alias"], mensajes=mensajes, herramientas=herramientas,
                  esfuerzo=modelo.get("esfuerzo"))
