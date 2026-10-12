#!/usr/bin/env python3
"""El almacén de documentos: **el original de Zettel**, en su propia base.

`mvp/código/almacen.db` guarda **el texto volcado** (el markdown), su **sello**, su **procedencia**
(el nombre, la ruta y el mtime de la fuente) y su **radicación**; más la cédula de cada volcado. El
diseño —qué guarda y por qué— está en `mvp/almacen-diseno.md`.

Tres cosas que hay que tener presentes:

1. **El texto es el original.** Lo que estaba en el sistema de archivos pasa a ser **procedencia**.
   Y un volcado distinto es **otro documento**, con otro nombre: acá no hay `--rehacer`, porque un
   documento radicado no se mueve. **El markdown no tiene versiones.**
2. **El sello es la identidad**: sha256 del markdown. El `UNIQUE (sello)` impide que el mismo texto
   entre dos veces.
3. **El corpus guarda un espejo** (`documentos`: id, dominio, sello y —por ahora— la ruta y la fecha
   de radicación) para que sus claves foráneas sigan existiendo. **Entre archivos no hay claves
   foráneas**, así que el espejo se escribe **en la misma transacción**, con `ATTACH`; y por eso
   **ninguna de las dos bases usa WAL**.
"""

import pathlib
import sqlite3
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from base import DB as CORPUS, hash_texto  # noqa: E402

DB = AQUI / "almacen.db"

ESQUEMA = """
CREATE TABLE IF NOT EXISTS documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre con que se radica ('sol')
  coleccion          TEXT NOT NULL,      -- la etiqueta que en el corpus se llama `dominio`
  texto              TEXT NOT NULL,      -- el markdown volcado: el original
  sello              TEXT NOT NULL,      -- sha256 del texto: es su identidad
  nombre_fuente      TEXT,               -- el nombre del archivo del que se volcó
  ruta_fuente        TEXT,               -- dónde estaba, en el sistema de archivos
  fecha_modificacion TEXT,               -- el mtime que el sistema registra, tomado al volcar
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base
  UNIQUE (sello)                          -- el mismo texto no entra dos veces
);

CREATE TABLE IF NOT EXISTS volcados (    -- el intento de volcado: la cédula del acto
  id             TEXT PRIMARY KEY,       -- el intento, no el documento
  documento_id   TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- nulo si falló
  modelo         TEXT NOT NULL,
  esfuerzo       TEXT,
  prompt         TEXT NOT NULL,          -- el nombre del prompt
  hash_prompt    TEXT NOT NULL,
  tokens_entrada INTEGER,
  tokens_salida  INTEGER,                -- incluye el pensamiento
  tokens_pensando INTEGER,               -- detalle de lo anterior
  cache_hit      INTEGER,
  segundos       REAL,
  estado         TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo         TEXT,
  fecha          TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL)
);
"""

CAMPOS_VOLCADO = ("modelo", "esfuerzo", "prompt", "hash_prompt", "tokens_entrada", "tokens_salida",
                  "tokens_pensando", "cache_hit", "segundos")


def conectar():
    """Abre el almacén (lo crea si no está), con las tablas y las claves foráneas encendidas."""
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(ESQUEMA)
    return db


def documento(db, identificador):
    """La fila del documento, o `None`."""
    return db.execute("SELECT * FROM documentos WHERE id = ?", (identificador,)).fetchone()


def exigir_documento(db, identificador):
    """La fila del documento, o se detiene: sin documento radicado no hay nada que hacer."""
    fila = documento(db, identificador)
    if fila is None:
        raise SystemExit(f"'{identificador}' no está radicado en el almacén ({DB.name})")
    return fila


def documentos_de(db, coleccion):
    """Los documentos de una colección, en orden."""
    return db.execute("SELECT * FROM documentos WHERE coleccion = ? ORDER BY id",
                      (coleccion,)).fetchall()


def texto_de(db, identificador):
    """**El texto volcado** —el original—, con su sello comprobado.

    El sello se comprueba contra el texto guardado: es el chequeo de que la base no se tocó.
    """
    fila = exigir_documento(db, identificador)
    if hash_texto(fila["texto"]) != fila["sello"]:
        raise SystemExit(f"el texto de '{identificador}' no coincide con su sello: el almacén se "
                         f"tocó, o la fila se escribió mal")
    return fila["texto"]


def escribir(db, identificador, coleccion, texto, procedencia, volcado):
    """Escribe el documento, su cédula y su espejo en el corpus, **en una sola transacción**.

    - Si el id ya está con el **mismo sello**, no hace nada (idempotente).
    - Si el id ya está con **otro texto**, se detiene: eso es otro documento, y va con otro nombre.
    - Si el **texto ya está** con otro id, se detiene: el mismo documento no entra dos veces.
    """
    sello = hash_texto(texto)
    ya = documento(db, identificador)
    if ya is not None:
        if ya["sello"] == sello:
            return {"estado": "ya_estaba", "documento": identificador, "sello": sello}
        raise SystemExit(f"'{identificador}' ya está radicado con otro texto (sello "
                         f"{ya['sello'][:12]}…): eso es otro documento. Radicá con otro nombre.")
    mismo = db.execute("SELECT id FROM documentos WHERE sello = ?", (sello,)).fetchone()
    if mismo is not None:
        raise SystemExit(f"ese mismo texto ya está radicado como '{mismo['id']}': el mismo "
                         f"documento no entra dos veces.")

    # `ATTACH` no se puede hacer **dentro** de una transacción: se adjunta antes, y desde ahí las dos
    # escrituras —el almacén y el espejo del corpus— van en la misma transacción.
    db.execute("ATTACH DATABASE ? AS corpus", (str(CORPUS),))
    db.execute("BEGIN")
    db.execute("INSERT INTO documentos (id, coleccion, texto, sello, nombre_fuente, ruta_fuente, "
               "fecha_modificacion) VALUES (?,?,?,?,?,?,?)",
               (identificador, coleccion, texto, sello, procedencia.get("nombre"),
                procedencia.get("ruta"), procedencia.get("fecha_modificacion")))
    db.execute("INSERT INTO volcados (id, documento_id, " + ", ".join(CAMPOS_VOLCADO) + ", "
               "estado, motivo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (volcado["id"], identificador, *[volcado.get(campo) for campo in CAMPOS_VOLCADO],
                volcado.get("estado", "exitoso"), volcado.get("motivo")))
    db.execute("INSERT INTO corpus.documentos (id, dominio, ubicacion_upstream, sello) "
               "VALUES (?,?,?,?)",
               (identificador, coleccion, procedencia.get("ruta") or "", sello))
    db.commit()
    db.execute("DETACH DATABASE corpus")
    return {"estado": "escrito", "documento": identificador, "sello": sello}


def registrar_fallo(db, volcado, motivo, documento_id=None):
    """Deja la cédula de un volcado que **no** produjo documento (o que falló al escribirlo).

    Es el único caso en que una cédula existe sola: es la única traza que queda del intento.
    """
    db.execute("INSERT INTO volcados (id, documento_id, " + ", ".join(CAMPOS_VOLCADO) + ", "
               "estado, motivo) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
               (volcado["id"], documento_id, *[volcado.get(campo) for campo in CAMPOS_VOLCADO],
                "fallido", motivo))
    db.commit()
    return volcado["id"]
