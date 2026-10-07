#!/usr/bin/env python3
"""Lee R: el JSON que aplica el ORQUESTADOR.

R **no lo ve el agente**. El orquestador la aplica al armar la llamada: de `herramientas` sale
qué se ofrece (se cruza con las que existen) y `operaciones` dice qué puede pedir el agente. Las
condiciones que el código no puede hacer cumplir —«los conflictos se muestran»— no van acá: van
en el prompt del agente, como reglas.

Claves de esta versión:

    fuentes_admitidas  qué fuentes valen
    herramientas       qué herramientas se ofrecen
    operaciones        qué operaciones puede pedir el agente (vacío: ninguna)
"""

import json


def leer_r(ruta):
    """Devuelve R, y se detiene si le falta alguna de las tres claves."""
    if not ruta.exists():
        raise SystemExit(f"no está R en '{ruta}'")
    r = json.loads(ruta.read_text(encoding="utf-8"))
    for clave in ("fuentes_admitidas", "herramientas", "operaciones"):
        if clave not in r:
            raise SystemExit(f"R no trae '{clave}': {ruta}")
    return r
