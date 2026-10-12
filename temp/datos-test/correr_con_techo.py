#!/usr/bin/env python3
"""Corre `correr.py` con otro techo de tokens para un alias, solo en memoria.

No toca el registro de proveedores del repo: cambia `ALIAS[alias]["max_tokens"]` en esta ejecución
y llama a `correr.main`. El techo usado queda en el crudo (`peticion.max_tokens`).

    python3 temp/datos-test/correr_con_techo.py <alias> <max_tokens> <argumentos de correr.py…>
"""
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
sys.path.insert(0, str(AQUI))

import proveedores  # noqa: E402

# Sonnet no está en el registro del repo: se declara acá, en memoria, con el transporte de Haiku.
proveedores.ALIAS.setdefault("sonnet", dict(proveedores.ALIAS["haiku"], id="claude-sonnet-5-5"))

alias, techo = sys.argv[1], int(sys.argv[2])
proveedores.ALIAS[alias]["max_tokens"] = techo

import correr  # noqa: E402

correr.main(sys.argv[3:])
