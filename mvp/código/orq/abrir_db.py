#!/usr/bin/env python3
"""Abre la base del corpus, en solo lectura.

Solo lectura a propósito: el orquestador **consulta** el corpus; no lo escribe. Lo que produce su
corrida —la fila de `corridas` y la respuesta— lo escribe al final `orq/registrar_consulta.py`, y
lo escriben, en actos separados y a mano, `mvp/código/radicar.py`, `paso1_unidades.py` y
`paso2_datos.py`.
"""

import sqlite3


def abrir_db(ruta):
    """Devuelve la conexión a la base (solo lectura). Si no está, se detiene y reporta."""
    if not ruta.exists():
        raise SystemExit(f"no está la base '{ruta}': la crea mvp/código/radicar.py")
    db = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db
