#!/usr/bin/env python3
"""Corre `correr.py` mandando el prompt como lo manda el acto real: dos mensajes (system y user).

`correr.py` arma el prompt entero y lo manda como un solo mensaje de usuario; acá, en memoria, se
parte con `mensajes.partir` por las marcas [SISTEMA] y [TAREA] antes de llamar. No toca el repo.

    python3 temp/ut-haiku/correr_dos_mensajes.py <argumentos de correr.py…>
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
sys.path.insert(0, str(AQUI))

import correr  # noqa: E402
from mensajes import partir  # noqa: E402

_llamar = correr.llamar


def llamar_partido(modelo, prompt=None, **resto):
    return _llamar(modelo, mensajes=partir(prompt), **resto)


correr.llamar = llamar_partido
correr.main(sys.argv[1:])
