#!/usr/bin/env python3
"""`paso2_seco_v1.py` mandando el prompt en UN solo mensaje de usuario (system y user unidos).

Prueba si el razonamiento de GLM en `low` depende de la forma del envío: las corridas de doc10
(un solo mensaje) razonaron; las del café (system + user) no. Solo en memoria.

    python3 temp/datos-test/paso2_seco_v1_un_mensaje.py <doc> <alias> <esfuerzo> <rN>
"""
import pathlib
import runpy
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
import mensajes  # noqa: E402

_partir = mensajes.partir


def partir_en_uno(*args, **kwargs):
    sistema, usuario = _partir(*args, **kwargs)
    return [{"role": "user", "content": sistema["content"] + "\n\n" + usuario["content"]}]


mensajes.partir = partir_en_uno
runpy.run_path(str(AQUI / "paso2_seco_v1.py"), run_name="__main__")
