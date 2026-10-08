"""La base del corpus: el registro (SQLite), en un solo lugar.

`mvp/código/corpus.db` **es el registro**: no es una vista derivada y no se regenera. Dos tablas:

- `documentos`: un documento **radicado** por fila —su nombre, su dominio, la fecha y la hora de la
  radicación (las pone la base), dónde vive, su sello y, si está publicado, su commit—. Un
  documento radicado no se mueve: si su texto cambia, eso es otro documento.
- `datos`: las filas de datos de cada unidad de un documento radicado. Se cargan **después**, en un
  acto aparte, y recargarlas no toca la fila del documento.

Ningún acto de acá borra ni vacía nada: lo que entra, queda.
"""

import pathlib
import sqlite3

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent.parent
DB = AQUI / "corpus.db"
DOCUMENTOS = RAIZ / "mvp" / "documentos"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre del documento radicado
  dominio            TEXT NOT NULL,      -- el alcance al que pertenece
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base, al radicar
  ubicacion_local    TEXT NOT NULL,      -- dónde vive en esta máquina
  ubicacion_upstream TEXT NOT NULL,      -- dónde vive en el repo
  commit_publicacion TEXT,               -- el commit que lo publica, si ya está publicado
  sello              TEXT NOT NULL       -- sha256 del texto radicado
);
CREATE TABLE IF NOT EXISTS datos (
  id           TEXT PRIMARY KEY,
  unidad_id    TEXT NOT NULL,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT
);
CREATE INDEX IF NOT EXISTS idx_datos_unidad ON datos(unidad_id);
"""


def conectar():
    """Abre la base (la crea si no está) y se asegura de que las tablas existan."""
    db = sqlite3.connect(DB)
    db.executescript(ESQUEMA)
    return db


def prefijo_de(identificador):
    """El prefijo de las unidades de ese documento ('doc8' → 'doc8:U')."""
    return f"{identificador}:U"


def datos_de(db, identificador):
    """Cuántas filas de datos tiene cargadas ese documento."""
    prefijo = prefijo_de(identificador)
    return db.execute("SELECT COUNT(*) FROM datos WHERE substr(unidad_id, 1, ?) = ?",
                      (len(prefijo), prefijo)).fetchone()[0]


def borrar_datos(db, identificador):
    """Saca solo las filas de datos del documento. No toca su fila: el documento no se mueve."""
    prefijo = prefijo_de(identificador)
    db.execute("DELETE FROM datos WHERE substr(unidad_id, 1, ?) = ?", (len(prefijo), prefijo))
