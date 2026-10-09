#!/usr/bin/env python3
"""Resuelve el dominio a sus documentos: pertenencia de la tabla, sin juicio.

No lee la pregunta. El dominio es una **entrada** —lo elige el usuario— y acá solo se busca qué
documentos llevan esa etiqueta. Si el dominio no tiene documentos, se detiene: no se sigue.
"""


def resolver_dominio(db, dominio):
    """Devuelve las filas de `documentos` con ese dominio."""
    filas = db.execute(
        "SELECT id, dominio, fecha_radicacion, ubicacion_upstream, "
        "sello FROM documentos WHERE dominio = ? ORDER BY id", (dominio,)
    ).fetchall()
    if not filas:
        raise SystemExit(f"el dominio '{dominio}' no tiene documentos en la base")
    return [dict(fila) for fila in filas]
