# Consulta completa de Zettel (v1) · diseño

Diseño de la consulta: qué entra, cómo se resuelve, qué se registra y cómo se juzga. Este
documento describe **lo que hay**; donde algo está abierto, lo dice con esa palabra. **El estado y
lo que sigue viven en `mvp/memoria de trabajo y pendientes.md`**, y los resultados de cada ronda,
en el registro de esa ronda.

**Para qué.** El **primer recorrido completo** de Zettel sobre el corpus: recibir
una pregunta y entregar una respuesta con lo que el corpus establece —o decir con
precisión que no está—, con el recorrido registrado.

**Qué se considera terminado.** Una ejecución acotada del recorrido, sobre un dominio y con las
baterías de preguntas fijadas antes, juzgada contra lo que se dejó escrito: si la respuesta es
fiel, si se sostiene en lo que el documento establece, y si lo que no se puede establecer se dice
con precisión.

**Base.** [orquestador-plan.md](../historico/orquestador-plan.md) §3 (estaciones); la extracción
del paso 2 (el informe de esa ronda, archivado en `mvp/temp/`). **Los tres prompts de trabajo viven
en
`mvp/prompts/`:** `prompt_UT.md` (paso 1, unidades temáticas), `prompt_DATOS.md` (paso 2,
los datos por unidad —una unidad por turno: devuelve `caso` y `datos`
(`aspecto · valor · unidad_valor`)—) y `prompt_ORQ.md` (el agente de la consulta,
§8). El paso 1 de la ronda cerrada (v9) y el candidato
`prompt_ficha_contexto.md` quedan congelados: no se reabren ni se adoptan. Sin Jev y
sin búsqueda externa.

---

## 1. Reparto de papeles

**El código es el ORQUESTADOR y el LLM es el AGENTE ENCARGADO** (D1). El agente es
**stateless**: cada llamada es una interacción nueva y solo sabe lo que va en el
prompt; el orquestador lleva la memoria y compone cada llamada (§6).

| | Orquestador (el código) | Agente encargado (el LLM) |
|---|---|---|
| Prepara | configuración y rutas; el dominio y sus documentos; las anclas; la lista de casos; el prompt de cada llamada | — |
| Sirve | los datos del caso que el agente pide (la única herramienta) | — |
| Hace | ejecuta la herramienta, lleva los mensajes, registra la corrida y la respuesta | — |
| Piensa | **nada**: no interpreta la pregunta, no elige casos, no juzga la entrega | qué casos pedir; qué responder; cuándo parar |
| **Memoria** | los mensajes de la consulta | **ninguna** |
| Propone | — | la respuesta, en el JSON de `RESPUESTA_JSON` |
| Juzga | **no juzga** | no ejecuta ni calcula |

El juicio no se pierde: vive en la **evaluación** (§12), fuera del ORQ. Es la
separación «control/contenido» del plan: el orquestador no comprueba la entrega ni
la cobertura, solo orquesta.

---

## 2. La extracción y el corpus

**El paso 1** (las unidades temáticas): el procedimiento completo —qué entra, de dónde viene, cómo
se procesa, qué se entrega y cómo se entrega— está en [guía_UT.md](guía_UT.md).

**El paso 2** (los datos por unidad) corre **por la API y en tanda**: **una llamada por documento**
con todas las unidades que falten, y la respuesta se reparte por la **posición en la lista
enviada**. La vía es `mvp/prompts/prompt_DATOS.md`:

```bash
python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--rehacer]
```

Escribe en la base —la corrida y los datos—, **todo o nada**: la tanda manda **todas** las unidades
del documento, y si alguna no se puede armar, o si la llamada falla, no se escribe ningún dato. **La medición que lo decidió está en
`mvp/memoria de trabajo y pendientes.md`.** El procedimiento completo —qué entra, de dónde viene,
cómo se procesa, qué se entrega y cómo se entrega— está en [guía_DATOS.md](guía_DATOS.md).

**Radicar es fijar.** Un documento radicado no cambia: si su texto cambia, eso es
**otro documento**, con su radicación y su fila propias. El `sello` (sha256 de lo
radicado) es el guardián: si el archivo ya no coincide, la carga de los datos se detiene y
reporta. Una **mudanza** de archivo es otra cosa —el documento es el mismo y el
sello no cambia— y se resuelve con una actualización de la base, autorizada.

**El conflicto entre fuentes, sin ejercitar.** Ejercitarlo pide un hecho disputado entre dos
documentos del mismo dominio. **Abierto.**

**La declaración del esquema** —con qué partición, qué prompt, con qué hash y con qué modelo se
extrajo— **está en la base**: la fila de `corridas` guarda el prompt y su hash, el modelo y el
esfuerzo de lo que está en la base, y los tokens (D23).

---

## 3. La base: el centro de datos

`mvp/código/corpus.db` (SQLite) **es el centro**: no hay archivos intermedios, y todo lo que los
pasos producen queda ahí, encadenado, para poder hacer la traza completa. Lo escriben **actos
manuales y separados**: `radicar.py` pone la fila del documento —su nombre, su dominio, dónde vive
y **la fecha y la hora, que pone la base** al radicar—; `paso1_unidades.py` (UT) escribe su corrida
y las unidades; `paso2_datos.py` (DATOS) escribe su corrida y los datos; y
`orq/registrar_consulta.py` escribe la corrida del ORQ y la respuesta. **Nunca se toca la fila del
documento**: un documento radicado no se mueve. En pruebas, `radicar.py --rehacer <doc>` saca su
fila y todo lo que cuelga de ella.

```sql
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,   -- el documento radicado
  dominio            TEXT NOT NULL,      -- GENERAL
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- fecha y hora: las pone la base, al radicar
  ubicacion_upstream TEXT NOT NULL,      -- dónde vive en el repo
  sello              TEXT NOT NULL       -- sha256 de lo radicado: es su identidad
);

CREATE TABLE corridas (                  -- una fila por corrida de UT, DATOS y el ORQ
  id              TEXT PRIMARY KEY,      -- <doc>:UT · <doc>:DATOS · <doc>:q<n>
  paso            TEXT NOT NULL CHECK (paso IN ('UT', 'DATOS', 'ORQ')),
  documento_id    TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- UT y DATOS
  dominio         TEXT,                  -- ORQ: el alcance de la consulta
  bateria         TEXT,                  -- ORQ: el archivo de preguntas
  pregunta_numero INTEGER,
  pregunta_texto  TEXT,
  prompt          TEXT, hash_prompt TEXT, hash_r TEXT,
  modelo          TEXT NOT NULL, esfuerzo TEXT,
  tokens_entrada INTEGER, tokens_salida INTEGER, tokens_pensando INTEGER, cache_hit INTEGER,
  segundos        REAL, turnos INTEGER, llamadas INTEGER,
  estado          TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo          TEXT,                  -- cortada por… · sin JSON · error de la API
  fecha           TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL),                   -- un fallo dice por qué
  CHECK ((paso = 'ORQ' AND dominio IS NOT NULL AND documento_id IS NULL)
      OR (paso <> 'ORQ' AND documento_id IS NOT NULL))                -- el alcance de cada paso
);

CREATE TABLE unidades (                  -- la salida de UT
  id           TEXT PRIMARY KEY,         -- <doc>:U1
  documento_id TEXT NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,
  subtema      TEXT NOT NULL,            -- el nombre del caso
  oraciones    TEXT NOT NULL,            -- los números de oración, "1,4"
  corrida_id   TEXT NOT NULL REFERENCES corridas(id),
  UNIQUE (documento_id, n)
);

CREATE TABLE datos (                     -- la salida de DATOS
  id           TEXT PRIMARY KEY,         -- <doc>:U1:D4
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT,                     -- "horas", "años", …
  corrida_id   TEXT NOT NULL REFERENCES corridas(id)
);

CREATE TABLE consultas (                 -- la respuesta del ORQ
  id             TEXT PRIMARY KEY,       -- <doc>:q<n>
  corrida_id     TEXT NOT NULL REFERENCES corridas(id),
  dominio        TEXT NOT NULL, documentos TEXT NOT NULL,
  pregunta_texto TEXT NOT NULL,
  desenlace      TEXT, respuesta TEXT,
  fecha          TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE consulta_casos (            -- los casos que el agente leyó
  consulta_id TEXT NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
  unidad_id   TEXT NOT NULL,
  PRIMARY KEY (consulta_id, unidad_id)
);
```

Así se lee una fila (ejemplo del formato):

| id | unidad_id | caso | aspecto | valor | unidad_valor |
|---|---|---|---|---|---|
| `<doc>:U1:D1` | `<doc>:U1` | el hecho que trata la unidad | el aspecto del dato | el valor | su unidad |
| `<doc>:U1:D4` | `<doc>:U1` | … | otro aspecto | otro valor | — |

**Qué NO guarda la base, y por qué:**

- **El texto del documento ni las oraciones literales**: viven en el documento radicado, que es la
  **fuente única**; la base guarda los **números** de oración de cada unidad, y el sello es el
  guardián de que el texto no cambió.
- **El crudo de las llamadas**: la petición se rearma —el prompt, el texto numerado desde el
  documento, y las unidades o los datos que ya están en la base—, y lo que el modelo produjo está en
  la base. Se pierde lo que dijo de más: su razonamiento.
- **Los reintentos**: una sola fila por paso y documento; la corrida efectiva reescribe la suya.

**Por qué SQLite.** La forma se elige por **forma de acceso**, y acá lo que manda es
leer un caso entero y filtrar por dominio y por caso: eso pide claves, foráneas y
consultas, no un molde único. SQLite viene en la biblioteca estándar, no tiene
servidor, y el archivo es uno. La discusión clásica dice lo mismo: el problema no es
el formato de serialización sino qué operaciones se hacen
([flat files vs SQLite](https://sqlite.org/forum/forumpost/c43b208884?t=h),
[hilo sobre JSON y SQLite](https://github.com/kody-w/rappterbook/discussions/3742)).
Con 26 filas cualquier cosa funciona; el motor se elige por lo que se hace con los
datos, no por el volumen.

**No es un derivado regenerable.** El registro **es** la fuente: lo que entra, queda, y no se
reproduce corriendo nada de nuevo (cada corrida se paga). Lo único que vive fuera son los
**documentos radicados** —su texto, con el sello como guardián—, que es de donde se leen las
oraciones. Nada es append-only: la corrida efectiva **reescribe su fila**.

**Invariantes que los actos exigen:**

- Un documento radicado tiene **una unidad o más**: un documento sin unidades no es
  un estado válido, es una extracción que falló (§13). Una línea es una unidad
  temática.
- Si el texto del documento no coincide con su **sello**, el acto **se detiene y reporta**: eso es
  otro documento.

**El vacío legítimo** es de nivel unidad: una unidad cuyas oraciones no establezcan
nada, que no aporta ningún dato. La carga puede avisarlo.

---

## 4. Entradas

### 4.1. Archivos de preguntas (es el usuario)

Un archivo por documento, **solo el texto de las preguntas, limpias** —sin condiciones, sin
expectativas, sin pistas—, en `mvp/consulta/preguntas_<doc>.md` (si el documento es `doc8.md`, sus
preguntas van en `preguntas_doc8.md`). Es lo único que aporta el usuario, junto con el dominio
elegido, y se fija **antes** de correr: no cambia entre réplicas. El formato es solo eso —las
preguntas numeradas, limpias—:

```
1. ¿Quién anunció la medida?
2. ¿Cuánto va a durar?
3. ¿A quién se le atribuye la decisión?
```

### 4.2. R

`mvp/código/R.json` es **un JSON que lee el ORQUESTADOR**. El agente **no
lo ve**: R se aplica ofreciendo —qué fuentes se admiten, qué herramientas se
ofrecen, qué operaciones existen—, no se le explica.

```json
{
  "fuentes_admitidas": ["solo el documento"],
  "herramientas": ["obtener_datos_del_caso", "preguntar_al_usuario"],
  "operaciones": []
}
```

| Clave | Qué dice | Quién la aplica |
|---|---|---|
| `fuentes_admitidas` | la única fuente es el documento radicado | el ORQ |
| `herramientas` | qué se le ofrece; lo que no está, no se le da | el ORQ, al armar `tools` |
| `operaciones` | ninguna: sin aritmética ni fechas calculadas | el ORQ, no ofreciendo nada |

Se fija antes de la corrida y queda registrada en la fila de la corrida. **Los topes de turnos y
de llamadas no son R**: son guardias del orquestador (§11).

**Las condiciones que el código no puede aplicar** —«tu saber no es premisa», «los
conflictos se muestran y no se eligen», «lo que no se cierra se entrega explícito,
con la brecha», «no hay interacción con el usuario»— no van en R: son reglas del
agente, y **no están escritas en ninguna parte**. **Abierto:** decidir si vuelven, y
dónde.

### 4.3. Las anclas

El **día y la hora del sistema**, tomados una sola vez al abrir la consulta
(`orq/anclas.py`) y **congelados**: si cambiaran entre turnos, romperían el prefijo
del caché y la consulta razonaría con dos «ahora» distintos. Van en el `system`,
junto con todo lo que se quiere conservar entre turnos, y quedan en la traza. **No
son dato del documento**, y el prompt lo dice.

---

## 5. El recorrido

| # | Paso | Archivo | Qué hace |
|---|---|---|---|
| 1 | Leer la configuración | `orq/leer_config.py` | las rutas de entrada, el dominio, el modelo y las guardias |
| 2 | Leer la pregunta | `orq/leer_pregunta.py` | la pregunta n del archivo, tal cual |
| 3 | Leer R | `orq/leer_r.py` | el JSON del orquestador |
| 4 | Abrir la base | `orq/abrir_db.py` | `corpus.db`, **solo lectura** |
| 5 | Resolver el dominio | `orq/resolver_dominio.py` | la etiqueta `GENERAL` → sus documentos (pertenencia, sin juicio) |
| 6 | Listar los casos | `orq/listar_casos.py` | `unidad_id` y `caso`, sin aspectos ni valores |
| 7 | Armar las herramientas | `orq/armar_herramientas.py` | R ∩ las que existen |
| 8 | Armar los mensajes | `orq/armar_prompt.py` + `prompt_ORQ.md` | el `system` (anclas) y el `user` (casos, tarea, formato) |
| 9 | El bucle | `orq/llamar_modelo.py`, `orq/ejecutar_herramienta.py`, `orq/obtener_datos_del_caso.py`, `orq/bucle.py` | llama, ejecuta lo que el agente pide, apila, y termina con la respuesta |
| 10 | Registrar | `orq/registrar_consulta.py` | la corrida y la respuesta, en la base |

`orq/orquestador.py` es el `main`: los llama en ese orden y nada más. Cada paso vive
en su archivo; `orq/config.json` tiene las rutas de **entrada** (las preguntas, R, la base y el
prompt), el dominio, el modelo y las guardias. Lo que el ORQ produce no se configura: va a la base.

**La petición.** El `system` lleva lo que se conserva entre turnos (las anclas) y el
`user` los casos del dominio, la tarea y el formato. La **pregunta va dentro de la
tarea 1**, en el `user`. En cada turno siguiente el historial crece con el
`assistant` y los mensajes `tool` (§6).

```
turno 1: ['system', 'user']
turno 2: ['system', 'user', 'assistant', 'tool', 'tool', …]
```

**El dominio es una entrada, no una inferencia.** El ORQ no lee la pregunta: no saca
palabras clave ni elige documentos. Recibe el dominio elegido (`GENERAL`), lo
resuelve por pertenencia a la tabla, y le pasa al agente **todos** los casos de ese
dominio. El que une la pregunta con la base es el **agente**.

---

## 6. La memoria es del orquestador (el agente es stateless)

El agente no recuerda nada entre llamadas: cada llamada es una interacción nueva y
solo sabe lo que va en el prompt. El orquestador lleva el estado —el array de
mensajes— y compone cada llamada; la traza es el registro de ese estado. El agente
es una función pura: `agente(prompt + mensajes) -> acción` (patrón *stateless
reducer*, factor 12 de
[12-Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md)).

**Qué se conserva entre turnos.** Lo que no cambia va en el `system`; hoy, las
anclas. Lo que cambia —el historial del bucle— va en los mensajes.

**La API es stateless.** Cada turno **reenvía todo** el historial. En DeepSeek no
hay `previous_response_id` ni estado del lado del servidor: «no reenviar» es no
**recomponer** el prefijo, no una opción del protocolo
([Responses API](https://api-docs.deepseek.com/guides/responses_api)). Lo que
abarata el reenvío es el **caché de prefijo**: coincidencia desde el token 0, por
unidades de prefijo persistidas
([Context Caching](https://api-docs.deepseek.com/guides/kv_cache)). Medido (§11): el
primer turno es todo `miss` y los siguientes pegan `hit` sobre el prefijo fijo; lo
que se paga es **cada resultado nuevo**.

**La mecánica del bucle**, verificada en `test_tool_calling/` con llamadas reales:

- **El orquestador no tiene estado entre turnos.** El mensaje del asistente vuelve
  tal cual —con sus `tool_calls` y su `reasoning_content`, que la API **exige**
  devolver cuando hay `tools`— y el resultado de la herramienta entra como un
  mensaje `role: "tool"` con su `tool_call_id`.
- **El LLM no calcula: pide.** Y no encadena por sí solo: si una respuesta pidiera
  dos pasos, el valor intermedio lo lleva el agente en la conversación, no el
  código. Cada paso cuesta un turno.
- **El código valida la forma, no la intención**: los argumentos de una herramienta
  pueden ser JSON inválido o traer un id inventado; eso vuelve por el canal `tool`
  como error, y el agente puede corregirse.

---

## 7. Las herramientas: dos

```json
{"type": "function",
 "function": {
   "name": "obtener_datos_del_caso",
   "description": "Devuelve todos los datos de un caso del dominio. Se pide por su id.",
   "parameters": {
     "type": "object",
     "properties": {"unidad_id": {"type": "string",
       "description": "El id del caso, tal como figura en la lista de casos."}},
     "required": ["unidad_id"],
     "additionalProperties": false}}}
```

Devuelve el caso completo: `unidad_id`, `caso` y **todos** sus datos, cada uno con
su id (`aspecto`, `valor`, `unidad_valor`). La lectura es por caso entero: el agente
no filtra por aspecto antes de leer.

**No hay herramienta de entrega.** La respuesta es el **mensaje final** del agente, y
el ORQ la lee de ahí (§9).

La segunda herramienta es la pregunta al usuario:

```json
{"type": "function",
 "function": {
   "name": "preguntar_al_usuario",
   "description": "Pregunta al usuario cuando la pregunta admite dos o más respuestas plausibles. Poné la situación y las respuestas posibles.",
   "parameters": {
     "type": "object",
     "properties": {"pregunta": {"type": "string"},
                    "opciones": {"type": "array", "items": {"type": "string"}}},
     "required": ["pregunta", "opciones"],
     "additionalProperties": false}}}
```

El agente la usa cuando la pregunta **admite dos o más respuestas plausibles** (prompt 4, §8).
El ORQ la registra y **el ciclo termina ahí**: no la responde (D26). No ejecuta nada ni toca la
base — la respuesta del usuario sería K de la consulta, no un dato del corpus.

**R se aplica al ofrecer.** La lista de `tools` es R ∩ lo que existe: lo restringido
no se da, así que el agente no puede pedirlo. Y el sistema decide qué puede: si la
herramienta no existe, no se ofrece aunque R la admita.

**El dominio va cerrado por el código, no por argumento.** La herramienta no acepta
`dominio`: el ORQ lo resuelve por pertenencia y valida cada id contra los casos del
dominio. El agente no puede ampliar el alcance cambiando un argumento.

**Qué le queda al código:** solo lo **mecánico** —parsear los argumentos (si no son
JSON, no hay nada que ejecutar) y saber qué herramienta ejecutar—. No comprueba la
entrega, ni la cobertura, ni que un dato citado exista. El ORQ orquesta; no juzga.

---

## 8. El prompt del agente

Vive en `mvp/prompts/prompt_ORQ.md`, **un solo archivo** con dos
partes marcadas: `[SISTEMA]` (lo que se conserva entre turnos) y `[TAREA]` (lo que
depende del dominio y de la pregunta). `armar_prompt.py` lo parte y devuelve los dos
mensajes. Los huecos son `{{CASOS}}`, `{{PREGUNTA}}` y `{{ANCLAS}}`, rellenados con
`str.replace` —nunca `str.format`—.

**Prompt 3 y prompt 4.** El prompt del agente es el que Frat llama **prompt 3** —hoy
`prompt_ORQ.md`—, y de él sale el lector de la entrega (§9). Lo que
sigue es **prompt 4**, la sonda de `preguntar_al_usuario`: sobre prompt 3 cambian la pregunta
—sale de la tarea 1 y va en su línea—, el nombre del bloque (`TAREAS` → `LÓGICA DEL AGENTE
ENCARGADO`), la tarea 4 (la tríada: una respuesta → responder · dos o más → herramienta ·
ninguna → número 2) y el valor `no_esta_en_el_corpus` → `no_esta_en_los_datos`.

```
[SISTEMA]
ANCLAS: {{ANCLAS}} (día y hora del sistema; no es dato del documento)

[TAREA]
CASOS:
{{CASOS}}

Pregunta: {{PREGUNTA}}

LÓGICA DEL AGENTE ENCARGADO:
1. Escoge los id de los casos que con probabilidad mayor al 80% contengan la respuesta a la pregunta.
2. Si no hay casos que cumplan la condición anterior, pasa al punto 5.
3. Utiliza la HERRAMIENTA obtener_datos_del_caso para obtener los datos de los casos seleccionados. Podés pedir varios casos en un mismo turno.
4. Analiza los datos: si hay una respuesta plausible, armá la respuesta; si hay dos o más respuestas plausibles, usá la HERRAMIENTA preguntar_al_usuario; si no hay ninguna, pasa al punto 5.
5. Diligencia el JSON en RESPUESTA_JSON.

RESPUESTA_JSON:
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_los_datos", "respuesta": ""}
```

**Lo que el prompt no lleva, a propósito:** no hay bloques `ROL`, `REGLAS` ni
`ALCANCE`; no lleva R (la aplica el ORQ); no lleva el esquema de las herramientas
(viaja en `tools`); no dice el dominio ni los documentos —los casos son lo que el
agente necesita para elegir—. La reestructuración que se discutió —`ROL` con el nombre del
modelo, `ALCANCE`, y un bloque `ESTRUCTURAS JSON DE SALIDA` con las estructuras numeradas—
**quedó fuera de esta sonda**: es producto, y la sonda prueba una sola cosa.

**El umbral del 80%** es el criterio de selección: el agente mira los nombres de los
casos y pide los que podrían contener la respuesta. Los nombres son resúmenes: hay
aspectos que el nombre del caso no nombra, así que una pregunta puede quedar sin caso
que la contenga aunque el dato exista. **Abierto:** si el criterio debe mirar algo más
que el nombre.

---

## 9. La respuesta

El agente entrega un JSON con dos estados:

```json
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_los_datos", "respuesta": ""}
```

El segundo valor se llama `no_esta_en_los_datos` desde prompt 4; **el lector acepta también el
viejo** (`no_esta_en_el_corpus`), que es el que traían los crudos de la primera ronda, ya archivados
(`orq/leer_entrega.py`, `ESTADOS`).

**El JSON no tiene campo propio**: como no hay herramienta de entrega, vive **dentro**
del mensaje final, junto a lo que el agente escriba alrededor. Prompt 3 lo pide así —la
respuesta corta de la tarea 5 y, en la 6, «diligencia el JSON en `RESPUESTA_JSON`»—, de modo
que el JSON llega de cuatro formas: solo, dentro de una cerca de código, detrás de la
etiqueta `RESPUESTA_JSON:` o al final, después de la prosa. **El ORQ lo ubica**
(`orq/leer_entrega.py`: recorre los tramos `{…}` balanceados y se queda con el que sigue a la
etiqueta, o con el último que traiga un `desenlace` de los dos estados). No es juzgar: es
leer. La forma de lectura está declarada en `config.json` (`entrega.forma`) y el ORQ se
detiene si no la conoce.

Si el mensaje no trae ningún JSON, la salida escribe el mensaje tal cual y dice que no hubo
JSON; si la corrida la cortó una guardia, dice cuál —no que «el agente no contestó».

**El ORQ no juzga la entrega**: la registra tal como vino y la escribe en la salida.
Si el agente no contesta, la salida dice que no contestó.

**Lo que el sobre mínimo no lleva:** ni los datos que sostienen la respuesta (la
ruta), ni un reporte de lo recorrido. La salida muestra la respuesta y qué casos se
leyeron. El sostén —que el usuario vea de dónde salió— **queda para cuando el usuario
lo pida**.

---

## 10. Salidas

Todo lo que produce la consulta queda **en la base**, y nada en archivos:

- **`consultas`**: una fila por pregunta —el dominio, los documentos ofrecidos, la pregunta y su
  texto, el desenlace (`respondida`, `no está en los datos`, `preguntó al usuario`) y la respuesta,
  tal como vino—. Se reescribe si la pregunta se vuelve a correr: vale la efectiva.
- **`consulta_casos`**: los casos que el agente leyó: es lo que permite la **traza**, de la
  respuesta a la unidad y al dato.
- **`corridas`**: la cédula de la corrida —modelo, esfuerzo, el prompt y su hash, R y su hash, los
  tokens, los segundos, los turnos, las llamadas, y el `estado` con su motivo—.

**Cómo se lee una respuesta.** Con una consulta, no con un archivo: el ORQ no escribe `salida.md`,
ni `traza.jsonl`, ni crudos. Quien quiera ver una respuesta la lee de la base —uniendo `consultas`
con las seis tablas—: `consultas` y `consulta_casos` dan la respuesta y los casos leídos,
`unidades` y `datos` el corpus, `documentos` el texto radicado y `corridas` la cédula de cada
llamada.

---

## 11. Guardias y presupuesto

Las guardias **no son R**: R dice qué se puede usar; esto solo corta si el bucle se
enreda.

- **Modelo:** alias `deepseek` = `deepseek-flash`, con razonamiento encendido
  (`thinking: enabled`) y esfuerzo `low` —el de defecto del registro de proveedores, cambiable por
  alias o por llamada—. El transporte es el del MVP (`mvp/código/proveedores/`, **sin
  streaming**): la respuesta llega entera y se entrega en la forma de siempre
  —`choices[0].message` con `content`, `reasoning_content`, `tool_calls` y `finish_reason`—. Los
  alias declarados son `deepseek`, `glm` (GLM 5.3 Flash) y `haiku` (Claude Haiku 5.5), más `grok`
  sin créditos.
- **De a una:** se manda una pregunta; la siguiente, cuando termina la corrida.
- **Guardias implementadas:** `max_turnos: 8` y `max_herramientas: 20`, y **el tope de
  herramientas se respeta de verdad**: el bucle mira el tope antes de ejecutar y corta la
  corrida (antes ejecutaba una herramienta más por turno). La causa del corte queda en la fila de
  la corrida (`corte`: `max_turnos`, `max_herramientas`, `pregunta_al_usuario`, o `null` si el
  agente cerró), y un corte se registra como **fallido**. **No hay corte por ciclo** (misma acción con los mismos
  argumentos dos veces). **Abierto.**
- **El consumo de las corridas** (`prompt_tokens = hit + miss`): el **prefijo fijo se cachea** (el
  `hit` aparece desde el segundo turno) y lo que se paga es lo nuevo —cada resultado de herramienta
  y cada mensaje del asistente—. El precio se calcula con la tarifa publicada el día de la corrida y
  se registra; no se estima a ojo. **La medición** —corrida por corrida, con su consumo turno por
  turno y lo que entregó cada una— quedó como **registro aparte** de la primera ronda:
  `mvp/temp/consulta/medicion-primera-ronda.md`. Los totales de cada corrida están en `corridas`.
- **El prompt no se muestra antes de correr:** se guarda con la corrida y se muestra
  cuando se pide.

---

## 12. Cómo se evalúa

Se juzga **lo que la corrida entrega**, leyendo el documento. El juicio es nuestro,
no del ORQ (§1):

- la respuesta se sostiene en lo que el documento establece;
- lo que no se puede establecer se dice con precisión: qué falta y por qué;
- **no cuenta** acertar por casualidad ni citar texto que no sostiene la respuesta;
- se distingue «no está en los datos extraídos» de «el documento no lo dice»: la
  extracción puede haber dejado algo afuera, y una unidad vacía es un hueco nuestro,
  no del documento;
- las **unidades examinadas** quedan registradas (los casos leídos están en `consulta_casos`), y se
  distinguen del campo;
- **no interviene Jev**: el juicio es nuestro y se registra.

La **vara** para distinguir el hueco del documento del hueco de la extracción son los
números de oración de la partición del paso 1: viven en `unidades` (los números) y en el documento
radicado (las oraciones), y desde ahí se consultan (§3).

---

## 13. Riesgos y límites

- **La extracción acota la respuesta** (hallazgo del paso 2, no defecto del puente).
- **El JSON de salida se ubica** donde prompt 3 lo ponga (§9); un mensaje que no traiga
  ningún JSON —o ninguna respuesta— sigue sin entrega, y la salida lo dice.
- **El prompt es el único canal.** Lo que el ORQ no ponga, el agente no lo sabe: si
  no le pasa un caso, no existe para él.
- **El historial crece por turno** (§11): de ahí el tope de turnos.
- **Devolver el `reasoning_content`**: con `tools` en la petición, si no vuelve en
  todos los turnos, la API responde 400.
- **El conflicto entre fuentes sigue sin ejercitarse** (§2).
- **Una extracción que falla detiene el proceso**: no produce un documento vacío ni
  una unidad vacía; produce una corrida cortada. Un documento **sin** unidades no es
  un estado válido (§3).

---

## 14. Decisiones

| # | Decisión | Estado |
|---|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO | decidida; vocabulario en §16 |
| **D2** | Corpus: solo un documento, o dos para tener conflicto | decidida en parte: el corpus admite varios documentos por dominio; el conflicto entre fuentes sigue sin ejercitarse (§2) |
| **D3** | Bucle con herramienta, o todo inyectado en una llamada | decidida: bucle con herramienta |
| **D4** | Sin datos derivados en esta versión | decidida |
| **D5** | R: `solo el documento`, sin mundo del LLM ni anclas como premisa | decidida: R.json con tres claves |
| **D6** | Nombre y sitio de los archivos | decidida: el código, `R.json` y la base en `mvp/código/` (el orquestador, en `orq/`); los documentos que se radican, en `mvp/documentos/`; las baterías, en `mvp/consulta/preguntas_<doc>.md`; los prompts, en `mvp/prompts/`; y **lo que se produce, en la base**. `mvp/temp/` es archivo: no se corre desde ahí, no se lee, no se escribe (§2–§3) |
| **D7** | Almacén | decidida: SQLite con **seis tablas** —el corpus (`documentos`, `unidades`, `datos`) y el expediente (`corridas`, `consultas`, `consulta_casos`)—, con claves foráneas y contratos (`paso`, `estado`, `motivo` si falló, un `n` por documento) |
| **D8** | Derivados | fuera de esta versión |
| **D9** | Idioma de los `tipo` | obsoleta: no hay tipos |
| **D10** | Documento R: esbozo + prosa para el agente | reemplazada: R es un JSON que lee el ORQ |
| **D11** | Compactación del historial | no implementada: el historial crece y corta el tope de turnos |
| **D12** | «Mundo del agente» en los documentos vivos | sigue como vocabulario; sin efecto en el código |
| **D13** | Herramientas: (A) protocolo textual o (B) nativas | decidida: (B), aditivo sobre el transporte del MVP (`proveedores`) |
| **D14** | Prompts de la extracción | decidida: `prompt_UT` y `prompt_DATOS`, hoy en `mvp/prompts/` |
| **D15** | Salida del paso 2 | decidida: `caso` y `datos`; **el 08-10 se quitó `dudas`** (no lo leía nadie) **y el paso 2 pasó a la tanda** (D27) |
| **D16** | `unidad_valor`: campo propio o dentro del `valor` | abierta — se usa poco, y no se decidió si merece campo propio |
| **D17** | El agente, ¿lee texto del documento o solo los datos extraídos? | decidida: solo los datos |
| **D18** | El ORQ, ¿juzga la entrega? | decidida: no; el juicio vive en la evaluación (§12) |
| **D19** | La entrega, ¿por herramienta o por mensaje final? | decidida: mensaje final |
| **D20** | Cómo se lee el JSON de salida cuando viene con prosa o envuelto | decidida (08-10): el ORQ ubica el JSON del mensaje final donde prompt 3 lo ponga (§9; `orq/leer_entrega.py`) |
| **D21** | Las condiciones que el código no puede aplicar (premisa, conflictos, brecha) | abierta: no están escritas en ninguna parte (§4.2) |
| **D22** | `documento_id` en `datos`, en vez del prefijo del id | abierta |
| **D23** | La declaración del esquema (partición, prompt, hash, modelo) en la base | **decidida (08-10):** la fila de `corridas` guarda el prompt y su hash, el modelo, el esfuerzo y los tokens de lo que está en la base |
| **D24** | El sostén en la respuesta (datos citados, reporte) | diferida: cuando el usuario pida ver la fuente |
| **D25** | Tope y corte por ciclo | en parte: el tope de herramientas se respeta y la causa del corte se registra; **no hay corte por repetición** |
| **D26** | Al usar `preguntar_al_usuario`, ¿se reanuda la corrida? | decidida (08-10): no en este MVP; el ciclo termina y la pregunta queda en la salida y en el crudo (§7) |
| **D27** | ¿El paso 2 va de a una unidad o en tanda? | decidida (08-10): **en tanda**, una llamada por documento; la medición, en `mvp/memoria de trabajo y pendientes.md` (§2, `guía_DATOS.md`) |

---

## 15. Qué se reutiliza

- `mvp/código/proveedores/`: **el transporte del MVP** —el registro de alias, `llamar` con `prompt`
  o `mensajes` y `tools`, y la única lectura de claves (`claves.py`)—, con la forma de OpenAI como
  contrato; y `mvp/código/respuesta.py`, con `extract_json`.
- `mvp/código/base.py`, `radicar.py`, `paso1_unidades.py` y `paso2_datos.py`: la base y sus
  **actos** (§3).
- `mvp/código/orq/`: el orquestador, un archivo por paso (§5).
- `mvp/código/orq/leer_entrega.py`: el lector de la entrega —el JSON de prompt 3,
  donde venga (§9).
- `test_tool_calling/`: las corridas que fijaron la mecánica del bucle y las
  lecciones del tool calling.
- `mvp/código/extraer_unidades.py`: `numerar_oraciones` y `verificar_subtemas` —la copia propia del
  MVP; para la evaluación, no para la base—.
- `mvp/temp/pieza1/pieza1.py`: `verificar` y `comparar` —para la evaluación—; `guardar` y
  `mantener` quedan sin uso mientras no haya derivados.
- `unidades/ficha_doc.py`: `verificar` y `fragmentos`, si el respaldo literal vuelve.

---

## 16. Vocabulario (D1)

- **orquestador** = el código: resuelve, aplica, ejecuta y registra. No piensa y no
  juzga.
- **agente encargado** = el LLM: interpreta, selecciona y propone. Stateless.
- **mundo del agente** = su saber general y sus convenciones de lectura, que antes se
  llamaba «mundo del orquestador».

Dónde vive: [zettel-vision-operativa.md](../zettel-vision-operativa.md) define los
dos nombres en «Notación y vocabulario»;
[definiciones-del-marco.md](../definiciones-del-marco.md) parte B tiene las filas y la
parte C dice «mundo del agente»;
[orquestador-plan.md](../historico/orquestador-plan.md) renombra el componente en
§0–§2, sus estaciones y el prompt.

---

## 17. Fuentes consultadas

**Del marco y del andar**

- *Nanopublication Guidelines* — aserción + procedencia + publicación en una unidad
  pequeña y autocontenida: <https://nanopub.net/guidelines/working_draft/>
- *A Unified Nanopublication Model…* (arXiv 2006.06348):
  <https://arxiv.org/html/2006.06348v1>
- *Evidence Model* — reificar solo si el hecho está en disputa, acotado o
  reemplazado:
  <https://cdn.jsdelivr.net/npm/@a5c-ai/atlas@5.0.1-staging.f17326334/graph/schema/evidence-model.md>
- `cs0lar/knk` — log bitemporal append-only y optimización atada a un cuello de
  botella medido: <https://github.com/cs0lar/knk>
- *Flat files vs SQLite* (foro de SQLite): <https://sqlite.org/forum/forumpost/c43b208884?t=h>
- Hilo «Flat JSON files vs SQLite for agent state» — elegir por forma de acceso:
  <https://github.com/kody-w/rappterbook/discussions/3742>
- *Towards Principled, Practical Document Database Design* (VLDB) — modelar por forma
  de acceso, incrustar lo que se lee junto:
  <https://www.vldb.org/pvldb/vol18/p4804-carey.pdf>
- *Data modeling with Amazon DocumentDB* — patrones de acceso:
  <https://d1.awsstatic.com/product-marketing/Data%20modeling%20with%20Amazon%20DocumentDB.pdf>
- *Entity Resolution: The Hardest Part of Any Knowledge Graph*:
  <https://archtin.com/blog/entity-resolution-in-knowledge-graphs>
- *Knowledge Graphs · Complete Guide* — esquema mínimo y crecer a demanda:
  <https://www.dataaihub.co/learn/knowledge-graphs>

**De la operación del agente**

- *12-Factor Agents* — factores 2, 3, 9 y 12:
  <https://github.com/humanlayer/12-factor-agents> y
  <https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md>
- *Effective context engineering for AI agents* (Anthropic):
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- *Building effective agents* (Anthropic):
  <https://www.anthropic.com/engineering/building-effective-agents>
- *Writing effective tools for agents* (Anthropic) — buscar, no listar; pocas
  herramientas con propósitos distintos:
  <https://www.anthropic.com/engineering/writing-tools-for-agents>
- *Context compression strategies*:
  <https://www.agentpatterns.ai/context-engineering/context-compression-strategies/>
- *Just-in-time retrieval* — un recuperador ruidoso es peor que precargar:
  <https://learn.agentpatterns.ai/context-engineering/just-in-time-retrieval/>
- *Progressive disclosure* (arXiv 2607.17598) — un nivel de divulgación basta:
  <https://arxiv.org/pdf/2607.17598.pdf>

**De la API**

- *DeepSeek · Chat Completions* — `messages`, `tools`, `tool_choice`,
  `finish_reason`, `usage`: <https://api-docs.deepseek.com/api/create-chat-completion/>
- *DeepSeek · Tool Calls* — el flujo de cuatro pasos y el `role: "tool"`:
  <https://api-docs.deepseek.com/guides/tool_calls/>
- *DeepSeek · Thinking Mode* — con `tools`, el `reasoning_content` tiene que volver en
  todos los turnos siguientes (si no, 400):
  <https://api-docs.deepseek.com/guides/thinking_mode/>
- *DeepSeek · Context Caching* — caché por prefijo, unidades de prefijo, y
  `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`:
  <https://api-docs.deepseek.com/guides/kv_cache>
- *DeepSeek · Responses API* — `previous_response_id` y `conversation` **no
  soportados**: la API es stateless:
  <https://api-docs.deepseek.com/guides/responses_api>
