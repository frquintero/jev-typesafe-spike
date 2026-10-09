"""La base del corpus: el registro (SQLite), en un solo lugar.

`mvp/código/corpus.db` **es el centro**: no hay archivos intermedios que leer para seguir. Todo lo
que los pasos producen —y lo que la consulta responde— queda acá, encadenado, para poder hacer la
**traza completa**: de una respuesta al dato, a la unidad, a la oración del documento, y a la
llamada que lo produjo.

**El corpus**

- `documentos`: un documento **radicado** por fila —su nombre, su dominio, la fecha y la hora (que
  pone la base), dónde vive en el repo y su **sello** (sha256 del texto: es su identidad)—. El texto
  no se guarda: vive en el documento radicado. Un documento radicado no se mueve.
- `unidades`: la salida de UT —el nombre del caso y **los números de oración** que agrupa—. Las
  oraciones literales no se guardan: se leen del documento radicado, y el sello es el guardián.
- `datos`: la salida de DATOS —caso, aspecto, valor y unidad del valor—.

**El expediente**

- `corridas`: **una fila por corrida** de UT, DATOS o el ORQ: modelo, esfuerzo, prompt (y su hash),
  tokens, segundos, y `estado` (`exitoso` / `fallido`) con su `motivo`. Se escribe **al terminar**,
  una sola vez, y **narra la extracción que está en la base**: si un reintento falla, la fila
  efectiva no se toca (salvo que no hubiera ninguna, y ahí el fallo queda para debug).
- `consultas` + `consulta_casos`: la pregunta y su respuesta, con los casos que el agente leyó.

Los contratos que la base **impone** (además de las claves foráneas): `paso` y `estado` solo toman
sus valores; UT y DATOS son de un documento y el ORQ de un dominio; una corrida fallida dice su
motivo; y no hay dos unidades con el mismo número en un documento.

Ningún acto borra ni vacía nada por su cuenta: lo que entra, queda. Los `--rehacer` son actos
explícitos, y los usa la prueba.
"""

import hashlib
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
  ubicacion_upstream TEXT NOT NULL,      -- dónde vive en el repo
  sello              TEXT NOT NULL       -- sha256 del texto radicado: es su identidad
);
CREATE TABLE IF NOT EXISTS corridas (
  id              TEXT PRIMARY KEY,      -- <doc>:UT · <doc>:DATOS · <doc>:q<n>
  paso            TEXT NOT NULL CHECK (paso IN ('UT', 'DATOS', 'ORQ')),
  documento_id    TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- UT y DATOS
  dominio         TEXT,                  -- ORQ: el alcance de la consulta
  bateria         TEXT,                  -- ORQ: el archivo de preguntas
  pregunta_numero INTEGER,
  pregunta_texto  TEXT,
  prompt          TEXT,                  -- el archivo del prompt que corrió
  hash_prompt     TEXT,                  -- sha256 de su contenido
  hash_r          TEXT,                  -- ORQ: sha256 de R.json
  modelo          TEXT NOT NULL,         -- el id del modelo
  esfuerzo        TEXT,
  tokens_entrada  INTEGER,
  tokens_salida   INTEGER,               -- incluye el pensamiento: no se suma aparte
  tokens_pensando INTEGER,               -- detalle de lo anterior
  cache_hit       INTEGER,
  segundos        REAL,
  turnos          INTEGER,
  llamadas        INTEGER,
  estado          TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo          TEXT,                  -- si falló: sin JSON · cortada por… · error de la API
  fecha           TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL),                    -- un fallo dice por qué
  CHECK ((paso = 'ORQ' AND dominio IS NOT NULL AND documento_id IS NULL)
      OR (paso <> 'ORQ' AND documento_id IS NOT NULL))                 -- el alcance de cada paso
);
CREATE TABLE IF NOT EXISTS unidades (
  id           TEXT PRIMARY KEY,         -- <doc>:U<n>
  documento_id TEXT NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,
  subtema      TEXT NOT NULL,            -- el nombre del caso
  oraciones    TEXT NOT NULL,            -- los números de oración, "4,5,6"
  corrida_id   TEXT NOT NULL REFERENCES corridas(id),
  UNIQUE (documento_id, n)
);
CREATE TABLE IF NOT EXISTS datos (
  id           TEXT PRIMARY KEY,         -- <doc>:U<n>:D<j>
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT,
  corrida_id   TEXT NOT NULL REFERENCES corridas(id)
);
CREATE INDEX IF NOT EXISTS idx_datos_unidad ON datos(unidad_id);
CREATE TABLE IF NOT EXISTS consultas (
  id             TEXT PRIMARY KEY,       -- <doc>:q<n>
  corrida_id     TEXT NOT NULL REFERENCES corridas(id),
  dominio        TEXT NOT NULL,
  documentos     TEXT NOT NULL,          -- los documentos del dominio que se ofrecieron
  pregunta_texto TEXT NOT NULL,
  desenlace      TEXT,                   -- respondida · no está en los datos · preguntó al usuario
  respuesta      TEXT,                   -- la respuesta, tal como vino
  fecha          TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS consulta_casos (
  consulta_id TEXT NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
  unidad_id   TEXT NOT NULL,             -- el id como texto: rehacer la extracción no rompe el expediente
  PRIMARY KEY (consulta_id, unidad_id)
);
"""


def conectar():
    """Abre la base (la crea si no está), con las tablas y las claves foráneas encendidas."""
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    db.executescript(ESQUEMA)
    return db


def hash_de(ruta):
    """El sha256 de un archivo."""
    return hashlib.sha256(ruta.read_bytes()).hexdigest()


def hash_texto(texto):
    """El sha256 de un texto."""
    return hashlib.sha256(texto.encode("utf-8")).hexdigest()


def documento(db, identificador):
    """La fila del documento radicado, o None."""
    return db.execute("SELECT * FROM documentos WHERE id = ?", (identificador,)).fetchone()


def exigir_documento(db, identificador):
    """Devuelve la fila del documento o se detiene: la radicación es el acto que va primero."""
    fila = documento(db, identificador)
    if fila is None:
        raise SystemExit(f"'{identificador}' no está radicado: la radicación es el acto que va "
                         f"primero (python3 mvp/código/radicar.py {identificador})")
    return fila


def ruta_documento(fila):
    """Dónde está el texto radicado, en el repo."""
    return RAIZ / fila["ubicacion_upstream"]


def exigir_sello(fila):
    """Devuelve el texto radicado, o se detiene si el archivo cambió desde la radicación."""
    ruta = ruta_documento(fila)
    if hash_de(ruta) != fila["sello"]:
        raise SystemExit(f"el texto de '{fila['id']}' cambió desde que se radicó: eso es otro "
                         f"documento. Se radica de nuevo con otro nombre (o, en pruebas, --rehacer).")
    return ruta.read_text(encoding="utf-8")


def unidades_de(db, identificador):
    """Las unidades del documento, en orden."""
    return db.execute("SELECT * FROM unidades WHERE documento_id = ? ORDER BY n",
                      (identificador,)).fetchall()


def datos_de(db, identificador):
    """Cuántas filas de datos tiene cargadas ese documento."""
    prefijo = f"{identificador}:U"
    return db.execute("SELECT COUNT(*) FROM datos WHERE substr(unidad_id, 1, ?) = ?",
                      (len(prefijo), prefijo)).fetchone()[0]


def borrar_datos(db, identificador):
    """Saca las filas de datos del documento. No toca su fila: el documento no se mueve."""
    prefijo = f"{identificador}:U"
    db.execute("DELETE FROM datos WHERE substr(unidad_id, 1, ?) = ?", (len(prefijo), prefijo))


def borrar_unidades(db, identificador):
    """Saca las unidades del documento (y sus datos, que cuelgan de ellas)."""
    borrar_datos(db, identificador)
    db.execute("DELETE FROM unidades WHERE documento_id = ?", (identificador,))


def borrar_corridas(db, identificador):
    """Saca las corridas de UT y DATOS de ese documento (el expediente del ORQ no se toca)."""
    db.execute("DELETE FROM corridas WHERE documento_id = ?", (identificador,))


def registrar_corrida(db, conservar_efectiva=False, **campos):
    """Escribe la fila de una corrida **cuando el proceso terminó**.

    Una sola fila por paso y documento (o por pregunta, en el ORQ): si se reintenta, se reescribe.
    Con `conservar_efectiva=True` —el reintento que falló— la fila que ya estaba **no se toca**,
    porque narra la extracción que sigue en la base. Devuelve True si escribió.
    """
    if conservar_efectiva and db.execute("SELECT 1 FROM corridas WHERE id = ?",
                                         (campos.get("id"),)).fetchone():
        return False
    columnas = ["id", "paso", "documento_id", "dominio", "bateria", "pregunta_numero",
                "pregunta_texto", "prompt", "hash_prompt", "hash_r", "modelo", "esfuerzo",
                "tokens_entrada", "tokens_salida", "tokens_pensando", "cache_hit", "segundos",
                "turnos", "llamadas", "estado", "motivo"]
    valores = [campos.get(columna) for columna in columnas]
    db.execute(
        f"INSERT INTO corridas ({', '.join(columnas)}) VALUES ({', '.join('?' * len(columnas))}) "
        f"ON CONFLICT(id) DO UPDATE SET "
        + ", ".join(f"{columna} = excluded.{columna}" for columna in columnas[1:])
        + ", fecha = datetime('now','localtime')",
        valores)
    return True
