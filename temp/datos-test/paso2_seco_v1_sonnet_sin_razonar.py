#!/usr/bin/env python3
"""`paso2_seco_v1.py` con Sonnet 5.5 y el razonamiento apagado, solo en memoria.

El transporte de Anthropic del repo fija `thinking: adaptive`; acá se reemplaza en la petición
saliente por el tipo que se pida (`disabled` o `between_tools`) y el crudo guarda el que se mandó.
No toca el registro de proveedores ni el transporte del repo.

    python3 temp/datos-test/paso2_seco_v1_sonnet_sin_razonar.py <tipo> <doc> sonnet <esfuerzo> <rN>
"""
import json
import pathlib
import runpy
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
import proveedores  # noqa: E402
from proveedores import anthropic  # noqa: E402

tipo = sys.argv.pop(1)
proveedores.ALIAS.setdefault("sonnet", dict(proveedores.ALIAS["haiku"], id="claude-sonnet-5-5",
                                             max_tokens=32000))

_Request = anthropic.urllib.request.Request


def Request(url, data=None, **kwargs):
    cuerpo = json.loads(data)
    cuerpo["thinking"] = {"type": tipo}
    return _Request(url, data=json.dumps(cuerpo, ensure_ascii=False).encode(), **kwargs)


anthropic.urllib.request.Request = Request
_llamar = anthropic.llamar


def llamar(*args, **kwargs):
    cuerpo, respuesta = _llamar(*args, **kwargs)
    cuerpo["thinking"] = {"type": tipo}  # el crudo guarda lo que de verdad se mandó
    return cuerpo, respuesta


anthropic.llamar = llamar
proveedores._PROVEEDORES["anthropic"] = anthropic
runpy.run_path(str(AQUI / "paso2_seco_v1.py"), run_name="__main__")
