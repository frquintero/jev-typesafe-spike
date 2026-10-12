# El almacén de documentos (diseño)

**Estado:** diseño. El acto (`volcar.py`) y la base (`almacen.db`) **no están construidos todavía**:
esto fija qué van a ser. Lo que hoy existe es `mvp/documentos/*.md` + una fila en `documentos` con
la ruta y el sello, y el texto viviendo en el archivo.

## 1. Por qué

1. **El archivo no puede ser el original.** El corpus se reseteó dos veces y se llevó los documentos
   con él: el archivo de Zettel tiene que ser un lugar, no un proyecto que se vacía.
2. **Radicar no debería ser copiar un archivo.** Un acto sobre la base no depende de dónde estaba el
   `.md`, ni de que nadie lo mueva, ni de que el sistema de archivos se acuerde de su fecha.
3. **Falta la procedencia.** Hoy se guarda la ruta y el sello. No se guarda de qué archivo salió, ni
   con qué nombre, ni cuándo se lo modificó por última vez.

## 2. Qué guarda

**El texto volcado, en markdown.** El volcado es un acto: toma una fuente en cualquier forma, le
**marca los encabezados** con la jerarquía que decide el modelo (prompt `prompt_volcado`), y guarda
ese markdown. **Ese markdown es el original para Zettel**: todo lo de después —las oraciones, los
tramos, los datos— se cuenta sobre él.

```sql
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre con que se radica ('sol')
  coleccion          TEXT NOT NULL,      -- la etiqueta que hoy se llama `dominio`
  texto              TEXT NOT NULL,      -- el markdown volcado: el original
  sello              TEXT NOT NULL,      -- sha256 del texto: es su identidad
  nombre_fuente      TEXT,               -- el nombre del archivo del que se volcó
  ruta_fuente        TEXT,               -- dónde estaba, en el sistema de archivos
  fecha_modificacion TEXT,               -- el mtime que el sistema registra, tomado al volcar
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base
  UNIQUE (sello)                          -- el mismo texto no entra dos veces
);

CREATE TABLE volcados (                  -- el intento de volcado: la cédula del acto
  id             TEXT PRIMARY KEY,       -- el intento, no el documento
  documento_id   TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- **nulo si falló**
  modelo         TEXT NOT NULL,
  esfuerzo       TEXT,
  prompt         TEXT NOT NULL,          -- el nombre del prompt
  hash_prompt    TEXT NOT NULL,
  tokens_entrada INTEGER, tokens_salida INTEGER, tokens_pensando INTEGER, cache_hit INTEGER,
  segundos       REAL,
  estado         TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo         TEXT,
  fecha          TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL)
);
```

**Por qué `volcados` tiene id propio y `documento_id` admite nulo:** un volcado **fallido no deja
documento** —es justo el que más interesa—, así que su fila tiene que poder existir sola. Es el único
lugar donde la cédula del acto no cuelga de lo que produjo.

**No hay versión del volcado.** El markdown **no tiene versiones**: es el documento. Si un volcado
produce otro markdown, es **otro documento**, con otro nombre. Y lo que identifica cómo se hizo ya
está: el `prompt` y su `hash` en la cédula, y **el armador es el commit de git** — el código está
versionado, y con más verdad que una etiqueta que alguien se acuerde de subir.

**No se guarda el índice.** Los encabezados, sus tramos, las secciones y la jerarquía **se derivan
del markdown** (las líneas que empiezan con `#`, y su nivel). Guardarlo sería guardar dos veces lo
mismo; y lo que el volcado tiene que dejar es el texto, no la respuesta del modelo.

**Tres tiempos, y no se mezclan:** la fecha propia del documento (si el texto la declara) es un
**dato**; el `fecha_modificacion` de la fuente es **procedencia** (lo que el sistema registró); la
`fecha_radicacion` es el **tiempo de transacción** y la pone la base.

## 3. El acto: `volcar.py`

```
python3 mvp/código/volcar.py <fuente> [--id NOMBRE] [--coleccion E] [--rehacer]
```

1. **Lee la fuente** y su procedencia (nombre, ruta, mtime). Si la fuente ya es markdown, no importa:
   el volcado la normaliza (ver §5).
2. **Pide el índice** con `prompt_volcado` (los encabezados, con su `padre`).
3. **Verifica y arma el markdown** (ver §4). Nada del texto se reescribe: solo se le insertan las
   marcas `#` en las líneas de encabezado.
4. **Escribe, en una sola transacción**: la fila del almacén, la corrida del volcado, y **el espejo
   en el corpus** (§6).
5. **Idempotente**: si el id ya está con el **mismo sello**, no hace nada. Si el id ya está con otro
   texto, **se detiene**: eso es otro documento, y va con otro nombre.

**Este acto es la radicación.** `radicar.py` se funde en él: la fecha de radicado, el sello y el
espejo son los mismos; lo que cambia es que el texto entra a la base y el archivo pasa a ser
**procedencia**.

## 4. Qué verifica, antes de escribir

| chequeo | qué protege |
|---|---|
| cada título está en el texto, **literal** y en orden | el modelo no reformula |
| `n` = 1..k y `padre` = 0 o un número anterior | la única regla mecánica del prompt |
| **los subárboles son contiguos** | que la jerarquía sea representable como niveles de markdown: un bosque cruzado el markdown no lo puede escribir |
| **quitar las marcas devuelve la fuente, byte a byte** | el volcado no inventa ni pierde nada |
| **idempotencia**: re-armar un markdown ya marcado no lo cambia | volcar dos veces no lo toca |
| índice **vacío** | un documento sin encabezados es un documento válido: el markdown sale igual a la fuente |

Si algo de eso falla, la corrida queda `fallida` con su motivo **y no se escribe nada**.

## 5. Las marcas: qué se toca del texto y qué no

- Se inserta `#` (una por nivel de profundidad) **al principio de la línea** del encabezado.
- Si la línea ya traía un marcador markdown, **se descarta y se pone el canónico** — por eso el
  volcado es idempotente y un markdown vuelto a volcar sale igual.
- **Nada más se toca**: ni los saltos, ni los espacios, ni los números que el texto ya traía
  (`# 1. Aviones más eficientes` — la marca es del código, el `1.` es del documento).
- No se normaliza el texto (no se borran los `1.`, `1.1`): eso sería *reescribir*, y rompería el
  chequeo de ida y vuelta. Si alguna vez se quiere un markdown «limpio», es **otra normalización**,
  declarada y con su versión.

## 6. El vínculo con el corpus

**Entre archivos no hay claves foráneas.** Así que:

- El **almacén es el dueño** del texto, del sello y de la procedencia.
- El **corpus conserva una fila fina** de `documentos` —`id`, `coleccion` (hoy `dominio`), `sello` y
  `fecha_radicacion`, más la ruta de la fuente **por ahora**— para que sus propias claves foráneas
  sigan existiendo y para que el ORQ resuelva un dominio y el reloj del radicado funcione sin abrir
  dos bases. Es un **espejo**, y el sello es lo que lo ata: si los dos no coinciden, hay algo
  roto. La ruta sale del espejo cuando los actos lean el texto de acá.
- Los dos escritos van en **una sola transacción** (`ATTACH`), y por eso **ninguna de las dos bases
  usa WAL**: con WAL la escritura entre archivos deja de ser atómica.

Los actos de después leen el texto del **almacén**: `paso1` y `paso2` dejan de leer
`mvp/documentos/<doc>.md`, y `exigir_sello` pasa a leer el markdown guardado.

## 7. Lo que se decidió (y por qué)

| decisión | por qué |
|---|---|
| **el id es el nombre** que se da al volcar, y **el sello es la identidad** | un id derivado del contenido haría ilegibles las referencias que ya usamos en todas partes (`sol:U1`); y el `UNIQUE (sello)` ya impide que el mismo texto entre dos veces |
| **el corpus conserva una fila fina** | sus claves foráneas necesitan un `documentos` vivo, y el ORQ necesita resolver dominios |
| **`coleccion` es una etiqueta por documento** | una tabla de colecciones con pertenencia es para cuando un documento tenga que estar en varias; hoy no lo necesita |
| **el índice no se guarda** | se deriva del markdown: guardarlo sería guardar dos veces lo mismo |
| **el volcado no normaliza el texto** | el markdown es la fuente + las marcas, y eso es lo que hace verificable el acto |
| **no hay versión del volcado** | el markdown es el documento y no tiene versiones; y el armador es el commit de git, que ya está |
| **el volcado no tiene `--rehacer`** | un documento radicado no se mueve: re-volcar con otra cosa es radicar otro documento |

## 8. Lo abierto

- **La numeración derivada** (`1`, `1.1`, `2`…) no siempre coincide con la que el documento trae
  (si hay una introducción o unos anexos sin número). No se guarda, y en el informe del acto se
  muestra **como lo que es: una etiqueta del código**, no una corrección del documento.

Lo demás quedó fijado en la tabla de §7 — incluido lo que había quedado abierto: la versión del
volcado y el `--rehacer`.
