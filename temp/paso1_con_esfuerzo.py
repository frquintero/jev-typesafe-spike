#!/usr/bin/env python3
"""Corre el acto real de UT (`mvp/código/paso1_unidades.py`) con otro esfuerzo para un alias.

El corredor del repo no recibe el esfuerzo (usa el del alias); acá se cambia solo en memoria, sin
tocar el registro de proveedores. Escribe en la base como el acto real, y la corrida guarda el
esfuerzo usado.

    python3 temp/paso1_con_esfuerzo.py <alias> <esfuerzo> <argumentos de paso1_unidades.py…>
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "mvp" / "código"))
import proveedores  # noqa: E402

alias, esfuerzo = sys.argv[1], sys.argv[2]
proveedores.ALIAS[alias]["esfuerzo"] = esfuerzo
import paso1_unidades  # noqa: E402
paso1_unidades.main(sys.argv[3:])
