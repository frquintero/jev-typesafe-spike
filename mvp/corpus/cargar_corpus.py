#!/usr/bin/env python3
"""Construye la base del corpus (SQLite) desde los documentos radicados y los crudos de la extracción.

Qué hay en esta carpeta:

    documentos/         los documentos radicados — la única fuente de verdad de su texto
    extraccion/doc4/    los crudos de los que sale la extracción de doc4:
                        las unidades temáticas (paso 1) y los datos por unidad (paso 2)
    corpus.db           la base: documentos · datos

Qué guarda la base: las **referencias** al documento (dominio, fecha de radicación, ubicación local y en el
repo, commit, sello) y **lo que la extracción produjo** (los datos). No guarda el texto del documento ni los
números de oración: el texto vive en el documento radicado, y los números son la vara con la que evaluamos el
paso 1. Cada fila de `datos` lleva su `caso` y su `unidad_id`, para poder leerse sola.

La base es derivada: se puede borrar y reconstruir con

    python3 mvp/corpus/cargar_corpus.py

Si un documento no está donde dice su `ubicacion_local`, el cargador se detiene y reporta: una mudanza es una
actualización de la base, con autorización.
"""

import hashlib
import json
import pathlib
import sqlite3

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent  # la raíz del repo
AQUI = pathlib.Path(__file__).resolve().parent
DB = AQUI / "corpus.db"

# Un registro por documento radicado.
DOCUMENTOS = [
    {
        "id": "doc4",
        "dominio": "GENERAL",  # el único dominio del MVP
        "fecha_radicacion": "2026-10-07",
        "ubicacion_local": "mvp/corpus/documentos/doc4.md",
        "ubicacion_upstream": (
            "https://github.com/frquintero/jev-typesafe-spike/blob/main/"
            "mvp/corpus/documentos/doc4.md"
        ),
        "commit": "7125733",  # el commit que publica el documento
        "unidades": "extraccion/doc4/p1-doc4-v10-muse-r1.out",
        "datos": "extraccion/doc4/p2-doc4-u{n}-r2.out",
    },
    {
        "id": "doc6",
        "dominio": "GENERAL",  # el mismo dominio del MVP
        "fecha_radicacion": "2026-10-07",
        "ubicacion_local": "mvp/corpus/documentos/doc6.md",
        "ubicacion_upstream": (
            "https://github.com/frquintero/jev-typesafe-spike/blob/main/"
            "mvp/corpus/documentos/doc6.md"
        ),
        "commit": None,  # se llena con el commit que publica el documento
        "unidades": "extraccion/doc6/p1-doc6-v10-muse-r1.out",
        "datos": "extraccion/doc6/p2-doc6-u{n}-r1.out",
    },
]

ESQUEMA = """
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,
  dominio            TEXT NOT NULL,
  fecha_radicacion   TEXT NOT NULL,
  ubicacion_local    TEXT NOT NULL,
  ubicacion_upstream TEXT NOT NULL,
  commit_publicacion TEXT,
  sello              TEXT NOT NULL
);
CREATE TABLE datos (
  id           TEXT PRIMARY KEY,
  unidad_id    TEXT NOT NULL,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT
);
CREATE INDEX idx_datos_unidad ON datos(unidad_id);
"""


def cargar_documento(db, doc):
    ruta = RAIZ / doc["ubicacion_local"]
    if not ruta.exists():
        raise SystemExit(
            f"el documento radicado no está en '{doc['ubicacion_local']}': una mudanza se "
            f"actualiza en la base, con autorización — no se sigue a ciegas"
        )
    db.execute(
        "INSERT INTO documentos VALUES (?,?,?,?,?,?,?)",
        (doc["id"], doc["dominio"], doc["fecha_radicacion"], doc["ubicacion_local"],
         doc["ubicacion_upstream"], doc["commit"],
         hashlib.sha256(ruta.read_bytes()).hexdigest()),
    )
    unidades = json.loads((AQUI / doc["unidades"]).read_text(encoding="utf-8"))["subtemas"]
    for n, unidad in enumerate(unidades, 1):
        uid = f"{doc['id']}:U{n}"
        datos = json.loads((AQUI / doc["datos"].format(n=n)).read_text(encoding="utf-8"))
        for j, dato in enumerate(datos.get("datos") or [], 1):
            db.execute("INSERT INTO datos VALUES (?,?,?,?,?,?)",
                       (f"{uid}:D{j}", uid, dato.get("caso") or unidad["subtema"],
                        dato["aspecto"], dato["valor"], dato.get("unidad_valor")))


def main():
    if DB.exists():
        DB.unlink()  # derivada: se reconstruye entera
    db = sqlite3.connect(DB)
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(ESQUEMA)
    for doc in DOCUMENTOS:
        cargar_documento(db, doc)
    db.commit()

    print(f"base: {DB.relative_to(RAIZ)}")
    for tabla in ("documentos", "datos"):
        print(f"  {tabla}: {db.execute(f'SELECT count(*) FROM {tabla}').fetchone()[0]} filas")
    for d in db.execute("SELECT id, dominio, fecha_radicacion, ubicacion_local, sello FROM documentos"):
        print(f"  documento: {d[0]} · {d[1]} · radicado {d[2]} · {d[3]} · sello {d[4][:12]}…")
    print("\nel mapa del dominio (caso · aspectos):")
    for uid, caso, aspectos in db.execute(
        "SELECT unidad_id, caso, group_concat(aspecto, ' · ') FROM datos "
        "GROUP BY unidad_id, caso ORDER BY unidad_id"
    ):
        print(f"  {uid} · {caso}")
        print(f"      {aspectos or '—'}")
    db.close()


if __name__ == "__main__":
    main()
