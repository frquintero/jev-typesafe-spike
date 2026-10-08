#!/usr/bin/env python3
"""Abre la base del corpus, en solo lectura.

Solo lectura a propósito: el orquestador **consulta** el registro, no lo escribe. La base la
**inscribe** `mvp/código/cargar_corpus.py`, documento por documento, y lo inscrito no se vuelve a
tocar.
"""

import sqlite3


def abrir_db(ruta):
    """Devuelve la conexión a la base (solo lectura). Si no está, se detiene y reporta."""
    if not ruta.exists():
        raise SystemExit(f"no está la base '{ruta}': la inscribe mvp/código/cargar_corpus.py")
    db = sqlite3.connect(f"file:{ruta}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    return db
