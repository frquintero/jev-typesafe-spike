#!/usr/bin/env python3
"""`paso2_seco_v1.py` con GLM y `thinking: {"type": "enabled"}` explícito, solo en memoria.

Z.ai lo documenta como el valor por defecto, pero las corridas del café en `low` volvieron con 0
tokens de razonamiento; acá se manda explícito. No toca el registro de proveedores.

    python3 temp/datos-test/paso2_seco_v1_glm_thinking.py <doc> glm <esfuerzo> <rN>
"""
import pathlib
import runpy
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
import proveedores  # noqa: E402

proveedores.ALIAS["glm"]["extra"] = {"thinking": {"type": "enabled"}}
runpy.run_path(str(AQUI / "paso2_seco_v1.py"), run_name="__main__")
