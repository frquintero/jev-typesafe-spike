#!/usr/bin/env python3
"""El almacén de documentos: **el original de Zettel**, en su propia base.

`mvp/código/almacen.db` guarda **el texto volcado** (el markdown), su **sello**, su **procedencia**
(el nombre, la ruta y el mtime de la fuente) y su **radicación**; más la cédula de cada volcado, la
**plantilla** con la que se volcó y su **contador**. El diseño —qué guarda y por qué— está en
`mvp/almacen-diseno.md`.

Tres cosas que hay que tener presentes:

1. **El texto es el original.** Lo que estaba en el sistema de archivos pasa a ser **procedencia**:
   el archivo de origen puede repetirse, y es **traza**, no identidad. **El markdown no tiene
   versiones**, y acá no hay `--rehacer`: un documento radicado no se mueve.
2. **La identidad es el volcado y su fecha.** El **sello** (sha256 del markdown) es el **guardián**
   de que el texto guardado no se tocó, no la identidad: dos volcados del mismo texto —otra fecha,
   y por eso otro documento— **entran los dos**, cada uno con su nombre.
3. **El corpus guarda un espejo** (`documentos`: id, dominio, sello y —por ahora— la ruta y la fecha
   de radicación) para que sus claves foráneas sigan existiendo. **Entre archivos no hay claves
   foráneas**, así que el espejo se escribe **en la misma transacción**, con `ATTACH`; y por eso
   **ninguna de las dos bases usa WAL**.

La cédula del volcado y la plantilla viven **acá**, en la base del acto: si el corpus se resetea,
el almacén se sigue explicando solo.
"""

import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import esquema  # noqa: E402
from base import DB as CORPUS, hash_texto  # noqa: E402

DB = AQUI / "almacen.db"
ESQUEMA_VERSION = 1

ESQUEMA = """
CREATE TABLE IF NOT EXISTS documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre con que se radica ('sol')
  coleccion          TEXT NOT NULL,      -- la etiqueta que en el corpus se llama `dominio`
  texto              TEXT NOT NULL,      -- el markdown volcado: el original
  sello              TEXT NOT NULL,      -- sha256 del texto: guardián de que no se tocó
  nombre_fuente      TEXT,               -- el nombre del archivo del que se volcó (procedencia)
  ruta_fuente        TEXT,               -- dónde estaba, en el sistema de archivos (procedencia)
  fecha_modificacion TEXT,               -- el mtime que el sistema registra, tomado al volcar
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime'))  -- la pone la base
);

CREATE TABLE IF NOT EXISTS volcados (    -- el intento de volcado: la cédula del acto
  id             TEXT PRIMARY KEY,       -- el token del acto: A000123
  documento_id   TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- nulo si falló
  modelo         TEXT NOT NULL,
  esfuerzo       TEXT,
  prompt_id      TEXT NOT NULL,          -- la plantilla que corrió ('volcado')
  prompt_version INTEGER NOT NULL,
  hash_prompt    TEXT NOT NULL,
  reloj_radicado TEXT,                   -- los relojes, tal como entraron al prompt
  reloj_sistema  TEXT,
  sello_fuente   TEXT,                   -- sha256 de la fuente: identificada, no conservada
  tokens_entrada INTEGER,
  tokens_salida  INTEGER,                -- incluye el pensamiento
  tokens_pensando INTEGER,               -- detalle de lo anterior
  cache_hit      INTEGER,
  segundos       REAL,
  estado         TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo         TEXT,
  iniciado       TEXT,
  terminado      TEXT,
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL)
);

CREATE TABLE IF NOT EXISTS prompts (     -- las plantillas del volcado, con su versión
  id       TEXT NOT NULL,                -- 'volcado'
  version  INTEGER NOT NULL,
  texto    TEXT NOT NULL,
  sello    TEXT NOT NULL,                -- sha256 del texto: guardián
  fecha    TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  PRIMARY KEY (id, version)
);

CREATE TABLE IF NOT EXISTS contador (    -- el token de esta base
  id     INTEGER PRIMARY KEY CHECK (id = 1),
  ultimo INTEGER NOT NULL DEFAULT 0
);
"""

CAMPOS_VOLCADO = ("modelo", "esfuerzo", "prompt_id", "prompt_version", "hash_prompt",
                  "reloj_radicado", "reloj_sistema", "sello_fuente", "tokens_entrada",
                  "tokens_salida", "tokens_pensando", "cache_hit", "segundos")


def conectar():
    """Abre el almacén (lo crea, o lo rehace si está vacío y el esquema cambió)."""
    return esquema.abrir(DB, ESQUEMA, ESQUEMA_VERSION)


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
    - El **mismo texto bajo otro id** es **otro documento** (la fecha del volcado los distingue):
      entra. La procedencia puede repetirse: es traza, no identidad.
    """
    sello = hash_texto(texto)
    ya = documento(db, identificador)
    if ya is not None:
        if ya["sello"] == sello:
            return {"estado": "ya_estaba", "documento": identificador, "sello": sello}
        raise SystemExit(f"'{identificador}' ya está radicado con otro texto (sello "
                         f"{ya['sello'][:12]}…): eso es otro documento. Radicá con otro nombre.")

    # `ATTACH` no se puede hacer **dentro** de una transacción: se adjunta antes, y desde ahí las dos
    # escrituras —el almacén y el espejo del corpus— van en la misma transacción.
    db.execute("ATTACH DATABASE ? AS corpus", (str(CORPUS),))
    db.execute("BEGIN")
    db.execute("INSERT INTO documentos (id, coleccion, texto, sello, nombre_fuente, ruta_fuente, "
               "fecha_modificacion) VALUES (?,?,?,?,?,?,?)",
               (identificador, coleccion, texto, sello, procedencia.get("nombre"),
                procedencia.get("ruta"), procedencia.get("fecha_modificacion")))
    _insertar_volcado(db, volcado, identificador)
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
    _insertar_volcado(db, volcado, documento_id, estado="fallido", motivo=motivo)
    db.commit()
    return volcado["id"]


def _insertar_volcado(db, volcado, documento_id, estado=None, motivo=None):
    """La fila de la cédula: el token, sus campos y cómo terminó."""
    columnas = ("id", "documento_id") + CAMPOS_VOLCADO + ("estado", "motivo", "iniciado",
                                                          "terminado")
    valores = (volcado["id"], documento_id,
               *[volcado.get(campo) for campo in CAMPOS_VOLCADO],
               estado or volcado.get("estado", "exitoso"),
               motivo if motivo is not None else volcado.get("motivo"),
               volcado.get("iniciado"), volcado.get("terminado"))
    db.execute(f"INSERT INTO volcados ({', '.join(columnas)}) "
               f"VALUES ({', '.join('?' * len(columnas))})", valores)
