"""La base del corpus: el registro (SQLite), en un solo lugar.

`mvp/código/corpus.db` **es el centro**: no hay archivos intermedios que leer para seguir. Todo lo
que los actos producen —y lo que la consulta responde— queda acá, encadenado, para poder hacer la
**traza completa**: de una respuesta al dato, a la unidad, a la oración del documento, y a la
corrida que lo produjo.

**El corpus**

- `documentos`: un documento **radicado** por fila —su nombre, su dominio, la fecha y la hora (que
  pone la base), la procedencia de la fuente y su **sello** (sha256 del texto: guardián de que no
  cambió)—. Es un **espejo** del almacén, que es el dueño del texto (`mvp/almacen-diseno.md`), y acá
  viven las claves foráneas. Un documento radicado no se mueve.
- `unidades`: la salida de UT —el nombre de cada unidad y su orden—. Cada unidad cuelga de **su**
  corrida de UT: dos particiones del mismo documento **conviven**, y la vigente se deriva.
- `unidad_oraciones`: los tramos de cada unidad —la oración **literal** tal como la devolvió el
  modelo, con su `desde` y su `hasta` sobre el texto del documento radicado—. La literal es la
  **evidencia** de lo que el modelo devolvió; el **tramo** es la referencia, y el sello del
  documento es el guardián: cortar el texto por el tramo tiene que devolver la literal, palabra por
  palabra. **No hay números de oración** (un número depende de la regla con la que se cortó).
- `datos`: la salida de DATOS —caso, aspecto, valor y unidad del valor—, colgando de **su** corrida.

**El expediente**

- `corridas`: **una fila por acto** (volcado, UT, DATOS, ORQ), con su **token** (`C000123`): modelo,
  esfuerzo, **plantilla y versión**, los **relojes que se inyectaron**, los tokens, segundos,
  `iniciado` y `terminado`, y `estado` (`exitoso` / `fallido`) con su `motivo`. Se escribe una sola
  vez, **al cerrar el acto**: **una corrida no se toca** y cada intento es su fila, así que rehacer
  no pisa el intento anterior y las rondas se pueden comparar.
- `prompts`: las **plantillas** con su versión. La registra el acto que las usa; editar una
  plantilla es una versión nueva, nunca un `UPDATE`.
- `contador`: de acá sale el token de esta base.
- `consultas` + `consulta_casos`: la pregunta y su respuesta, con los casos que el agente leyó.

Los contratos que la base **impone** (además de las claves foráneas): `paso` y `estado` solo toman
sus valores; UT y DATOS son de un documento y el ORQ de un dominio; una corrida fallida dice su
motivo; y no hay dos unidades con el mismo número **en una misma corrida**.

Ningún acto borra ni vacía nada por su cuenta: lo que entra, queda. Rehacer es **correr otra vez**,
y lo que estaba sigue ahí.
"""

import hashlib
import pathlib

import ajustes
import esquema

AQUI = pathlib.Path(__file__).resolve().parent
DB = AQUI / "corpus.db"
ESQUEMA_VERSION = 3

ESQUEMA = """
CREATE TABLE IF NOT EXISTS documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre del documento radicado
  dominio            TEXT NOT NULL,      -- el alcance al que pertenece
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base, al radicar
  ubicacion_upstream TEXT NOT NULL,      -- dónde vive en el repo
  sello              TEXT NOT NULL       -- sha256 del texto radicado: guardián de que no cambió
);
CREATE TABLE IF NOT EXISTS preguntas (   -- las preguntas radicadas: la única entrada de la consulta
  id               INTEGER PRIMARY KEY,  -- el número de la pregunta (1, 2, 3…)
  dominio          TEXT NOT NULL,        -- el alcance: la unidad semántica donde vive
  texto            TEXT NOT NULL,
  fuente           TEXT NOT NULL,        -- 'tecleada', o la ruta del archivo del que se leyó
  fecha_radicacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);
CREATE TABLE IF NOT EXISTS corridas (
  id              TEXT PRIMARY KEY,      -- el token del acto: C000123
  paso            TEXT NOT NULL CHECK (paso IN ('UT', 'DATOS', 'ORQ')),
  documento_id    TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- UT y DATOS
  dominio         TEXT,                  -- ORQ: el alcance de la consulta
  pregunta_id     INTEGER REFERENCES preguntas(id),  -- ORQ: la pregunta radicada
  pregunta_texto  TEXT,                  -- ORQ: el texto tal como se leyó
  prompt_id       TEXT,                  -- la plantilla que corrió (en `prompts`)
  prompt_version  INTEGER,
  hash_prompt     TEXT,                  -- sha256 de su texto: guardián
  hash_r          TEXT,                  -- ORQ: sha256 de R.json
  modelo          TEXT NOT NULL,         -- el id del modelo
  esfuerzo        TEXT,
  reloj_radicado  TEXT,                  -- los relojes, tal como entraron al prompt
  reloj_sistema   TEXT,
  corrida_origen  TEXT REFERENCES corridas(id),  -- DATOS: la corrida de UT que usó
  tokens_entrada  INTEGER,
  tokens_salida   INTEGER,               -- incluye el pensamiento: no se suma aparte
  tokens_pensando INTEGER,               -- detalle de lo anterior
  cache_hit       INTEGER,
  segundos        REAL,
  turnos          INTEGER,
  llamadas        INTEGER,
  estado          TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo          TEXT,                  -- si falló: sin JSON · cortada por… · error de la API
  iniciado        TEXT,                  -- cuándo empezó el acto
  terminado       TEXT,                  -- cuándo cerró
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL),                    -- un fallo dice por qué
  CHECK ((paso = 'ORQ' AND dominio IS NOT NULL AND documento_id IS NULL)
      OR (paso <> 'ORQ' AND documento_id IS NOT NULL))                 -- el alcance de cada paso
);
CREATE TABLE IF NOT EXISTS unidades (
  id           TEXT PRIMARY KEY,         -- <token_UT>:U<n>
  documento_id TEXT NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,
  subtema      TEXT NOT NULL,            -- el nombre del caso
  corrida_id   TEXT NOT NULL REFERENCES corridas(id),
  UNIQUE (corrida_id, n)                 -- una partición por corrida; las anteriores conviven
);
CREATE TABLE IF NOT EXISTS unidad_oraciones (   -- las oraciones de la unidad, con su tramo
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,         -- el orden dentro de la unidad
  desde        INTEGER NOT NULL,         -- offsets en caracteres sobre el texto del documento
  hasta        INTEGER NOT NULL,
  texto        TEXT NOT NULL,            -- la oración literal, tal como la devolvió el modelo
  PRIMARY KEY (unidad_id, n)
);
CREATE TABLE IF NOT EXISTS datos (
  id           TEXT PRIMARY KEY,         -- <token_DATOS>:U<n>:D<j>
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT,
  corrida_id   TEXT NOT NULL REFERENCES corridas(id)
);
CREATE INDEX IF NOT EXISTS idx_datos_unidad ON datos(unidad_id);
CREATE TABLE IF NOT EXISTS prompts (     -- las plantillas, con su versión
  id       TEXT NOT NULL,                -- 'volcado' · 'UT' · 'DATOS' · 'ORQ'
  version  INTEGER NOT NULL,
  texto    TEXT NOT NULL,
  sello    TEXT NOT NULL,                -- sha256 del texto: guardián
  fecha    TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  PRIMARY KEY (id, version)
);
CREATE INDEX IF NOT EXISTS idx_prompts_sello ON prompts(sello);
CREATE TABLE IF NOT EXISTS contador (    -- el token de esta base
  id     INTEGER PRIMARY KEY CHECK (id = 1),
  ultimo INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS ajustes (     -- el modelo y el esfuerzo de cada acto (la política)
  paso     TEXT PRIMARY KEY,             -- 'volcado' · 'UT' · 'DATOS' · 'ORQ'
  modelo   TEXT NOT NULL,                -- un alias del registro de proveedores
  esfuerzo TEXT                          -- el escalón, o null para el del alias
);
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
  unidad_id   TEXT NOT NULL,             -- el id de la unidad: <token_UT>:U<n>
  PRIMARY KEY (consulta_id, unidad_id)
);
CREATE TABLE IF NOT EXISTS consulta_llamadas (   -- la operación: qué herramienta pidió, en qué turno
  consulta_id TEXT NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
  turno       INTEGER NOT NULL,          -- la vuelta del bucle (1..max_turnos)
  orden       INTEGER NOT NULL,          -- la posición de la llamada dentro del turno (1..n)
  herramienta TEXT NOT NULL,
  argumentos  TEXT,                      -- tal como los mandó el modelo (puede no ser JSON válido)
  ok          INTEGER NOT NULL,          -- 1 la ejecutó · 0 volvió error por el canal `tool`
  error       TEXT,                      -- qué devolvió el canal `tool` cuando no fue ok
  PRIMARY KEY (consulta_id, turno, orden)
);
"""

COLUMNAS_CORRIDA = (
    "id", "paso", "documento_id", "dominio", "pregunta_id", "pregunta_texto",
    "prompt_id", "prompt_version", "hash_prompt", "hash_r", "modelo", "esfuerzo",
    "reloj_radicado", "reloj_sistema", "corrida_origen", "tokens_entrada", "tokens_salida",
    "tokens_pensando", "cache_hit", "segundos", "turnos", "llamadas", "estado", "motivo",
    "iniciado", "terminado")


def conectar():
    """Abre la base (la crea, o la rehace si está vacía y el esquema cambió)."""
    db = esquema.abrir(DB, ESQUEMA, ESQUEMA_VERSION)
    ajustes.sembrar(db)
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
                         f"primero (python3 mvp/código/volcar.py <fuente> --id {identificador})")
    return fila


def corrida(db, token):
    """La fila de una corrida, o None."""
    return db.execute("SELECT * FROM corridas WHERE id = ?", (token,)).fetchone()


def corridas_de(db, identificador):
    """Las corridas de un documento, en orden."""
    return db.execute("SELECT * FROM corridas WHERE documento_id = ? ORDER BY id",
                      (identificador,)).fetchall()


def unidades_de(db, corrida_id):
    """Las unidades de una corrida de UT, en orden."""
    return db.execute("SELECT * FROM unidades WHERE corrida_id = ? ORDER BY n",
                      (corrida_id,)).fetchall()


def ut_vigente(db, identificador):
    """El token de la última UT **exitosa** del documento, o None.

    Los tokens son una secuencia de ancho fijo, así que el orden del id es el orden de los actos.
    """
    fila = db.execute(
        "SELECT id FROM corridas WHERE documento_id = ? AND paso = 'UT' AND estado = 'exitoso' "
        "ORDER BY id DESC LIMIT 1", (identificador,)).fetchone()
    return fila["id"] if fila else None


def datos_vigente(db, identificador):
    """El token de la última tanda DATOS exitosa **sobre la UT vigente**, o None.

    Si la UT se rehízo después de la última tanda, no hay datos vigentes: los de la tanda
    anterior son de otra partición.
    """
    ut = ut_vigente(db, identificador)
    if ut is None:
        return None
    fila = db.execute(
        "SELECT id FROM corridas WHERE documento_id = ? AND paso = 'DATOS' "
        "AND estado = 'exitoso' AND corrida_origen = ? ORDER BY id DESC LIMIT 1",
        (identificador, ut)).fetchone()
    return fila["id"] if fila else None


def unidades_vigentes(db, identificador):
    """Las unidades de la UT vigente del documento (vacío si no hay)."""
    ut = ut_vigente(db, identificador)
    return unidades_de(db, ut) if ut else []


def datos_de(db, identificador):
    """Cuántos datos tiene la tanda DATOS vigente del documento."""
    token = datos_vigente(db, identificador)
    if token is None:
        return 0
    return db.execute("SELECT COUNT(*) FROM datos WHERE corrida_id = ?", (token,)).fetchone()[0]


def registrar_corrida(db, **campos):
    """Escribe la fila de un acto. **Una corrida no se toca**: cada intento es su fila."""
    valores = [campos.get(columna) for columna in COLUMNAS_CORRIDA]
    db.execute(f"INSERT INTO corridas ({', '.join(COLUMNAS_CORRIDA)}) "
               f"VALUES ({', '.join('?' * len(COLUMNAS_CORRIDA))})", valores)
