#!/usr/bin/env python3
"""Lee R: el JSON que aplica el ORQUESTADOR.

R **no lo ve el agente**. El orquestador la aplica al armar la llamada por una sola clave,
`herramientas`: de ahí sale qué se ofrece, cruzado con las que existen. **`fuentes_admitidas` y
`operaciones` se leen y se validan, pero hoy ningún módulo las aplica** (el diseño lo dice en §9).
Las condiciones que el código no puede hacer cumplir —«los conflictos se muestran»— no van acá: van
en el prompt del agente, como reglas.

Claves de esta versión:

    fuentes_admitidas  qué fuentes valen (declarativa: no la aplica nadie)
    herramientas       qué herramientas se ofrecen
    operaciones        qué operaciones puede pedir el agente (vacío: ninguna; declarativa)
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
