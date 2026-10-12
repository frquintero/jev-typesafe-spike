#!/usr/bin/env python3
"""Lee una pregunta radicada: **la única entrada de la consulta**.

La pregunta se lee **siempre de la base** (la tabla `preguntas`): su texto, su **dominio** —el
alcance, la unidad semántica donde vive— y su **fuente** (de qué archivo se leyó, o que fue
tecleada). No hay camino alternativo: ningún acto lee preguntas de un archivo.

Si la pregunta no está radicada, se detiene y dice cómo radicarla.
"""


def leer_pregunta(db, identificador):
    """La pregunta radicada, o se detiene: la radicación es el acto que va primero."""
    fila = db.execute("SELECT id, dominio, texto, fuente, fecha_radicacion FROM preguntas "
                      "WHERE id = ?", (identificador,)).fetchone()
    if fila is None:
        raise SystemExit(f"no hay pregunta {identificador} radicada: se radica primero "
                         f"(python3 mvp/código/radicar_pregunta.py <archivo> --dominio E)")
    return dict(fila)
