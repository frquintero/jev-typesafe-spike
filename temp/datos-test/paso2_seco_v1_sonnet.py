#!/usr/bin/env python3
"""`paso2_seco_v1.py` con Sonnet 5.5 y el transporte del repo tal cual (pensamiento adaptativo).

Sonnet no está en el registro del repo: se declara acá, en memoria, con el transporte de Haiku.

    python3 temp/datos-test/paso2_seco_v1_sonnet.py <doc> sonnet <esfuerzo> <rN>
"""
import pathlib
import runpy
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
import proveedores  # noqa: E402

proveedores.ALIAS.setdefault("sonnet", dict(proveedores.ALIAS["haiku"], id="claude-sonnet-5-5",
                                             max_tokens=32000))
runpy.run_path(str(AQUI / "paso2_seco_v1.py"), run_name="__main__")
