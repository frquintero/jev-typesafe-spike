#!/usr/bin/env python3
"""Corre `correr.py` con DeepSeek sin razonamiento, solo en memoria.

No toca el registro del repo: cambia el `extra` del alias `deepseek` a `thinking: disabled` y quita
`reasoning_effort` del cuerpo (el modo apagado no lo usa). Lo enviado queda en el crudo
(`peticion`). El segundo argumento de `correr.py` («esfuerzo») solo da nombre al archivo.

    python3 temp/datos-test/correr_sin_razonar.py <argumentos de correr.py…>
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
sys.path.insert(0, str(AQUI))

import proveedores  # noqa: E402
from proveedores import openai_compatible  # noqa: E402

proveedores.ALIAS["deepseek"]["extra"] = {"thinking": {"type": "disabled"}}
_original = openai_compatible.llamar


def _sin_esfuerzo(cfg, *args, **kwargs):
    return _original(dict(cfg, esfuerzo=None), *args, **kwargs)


openai_compatible.llamar = _sin_esfuerzo

import correr  # noqa: E402

correr.main(sys.argv[1:])
