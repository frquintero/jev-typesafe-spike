#!/usr/bin/env python3
"""`paso2_seco_v1.py` con MiMo-V2.6-Flash por OpenCode Go, sin tocar el repo.

Todo se declara acá, en memoria: el alias `mimo`, la clave por host (`OPENCODE_API_KEY`) y la
cabecera `x-opencode-session` que pide Go (un id estable por corrida). El `User-Agent` es el del
repo (`spike-jev/1.0`), que ya es propio.

El esfuerzo `sin` no manda `reasoning_effort` (no se sabe si Go lo acepta para MiMo); cualquier
otro valor sí lo manda, para probarlo aparte.

    bash -ic 'python3 temp/datos-test/paso2_seco_v1_mimo.py <doc> mimo <sin|low|high> <rN>'
"""
import pathlib
import runpy
import sys
import uuid

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
import proveedores  # noqa: E402
from proveedores import claves, openai_compatible  # noqa: E402

claves.CLAVE_POR_HOST["opencode.ai"] = "OPENCODE_API_KEY"
SESION = str(uuid.uuid4())
_cabeceras = claves.cabeceras


def _con_sesion(proveedor, url, conv_id=None):
    h = _cabeceras(proveedor, url, conv_id)
    if url.split("/")[2] == "opencode.ai":
        h["x-opencode-session"] = conv_id or SESION
    return h


openai_compatible.cabeceras = _con_sesion

proveedores.ALIAS.setdefault("mimo", {
    "proveedor": "openai_compatible", "id": "mimo-v2.6-flash",
    "url": "https://opencode.ai/zen/go/v1/chat/completions", "esfuerzo": None})

_resolver = proveedores.resolver


def _resolver_sin(alias, esfuerzo=None):
    config = _resolver(alias, None if esfuerzo == "sin" else esfuerzo)
    if esfuerzo == "sin":
        config["esfuerzo"] = None  # no se manda reasoning_effort
    return config


proveedores.resolver = _resolver_sin
runpy.run_path(str(AQUI / "paso2_seco_v1.py"), run_name="__main__")
