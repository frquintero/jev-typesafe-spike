# Consulta completa de Zettel (v1) · diseño

Fecha: 07-10-2026.

El primer recorrido está construido: base, orquestador, prompt del agente y las
cinco preguntas de `doc4` más las cinco de `doc6` corridas. Este documento describe
**lo que hay**; donde algo está abierto, lo dice con esa palabra.

**Lo que sigue.** (a) Cómo se lee el JSON de salida del agente, que no se lee cuando
viene con prosa o envuelto (§9; 5 de las 13 corridas); (b) las condiciones de la
consulta que el código no puede aplicar y no están escritas en ninguna parte (§4.2);
(c) la evaluación de las respuestas (§12).

**Para qué.** El **primer recorrido completo** de Zettel sobre el corpus: recibir
una pregunta y entregar una respuesta con lo que el corpus establece —o decir con
precisión que no está—, con el recorrido registrado.

**Qué se considera terminado.** Una ejecución acotada de ese recorrido, sobre un
dominio (`GENERAL`) y dos baterías de preguntas fijadas antes, evaluada contra lo que
se dejó escrito: si la respuesta es fiel, si se sostiene en lo que el documento
establece, y si lo que no se puede establecer se dice con precisión. El recorrido está
terminado; **la evaluación, pendiente**.

**Base.** [orquestador-plan.md](../historico/orquestador-plan.md) §3 (estaciones) y
§11 (F0, F1); el contrato de [mesa-dominio-plan.md](mesa-dominio-plan.md) §9 y su
cierre; la extracción del paso 2
([paso2/informe_paso2.md](paso2/informe_paso2.md)). **Prompts de la extracción:**
paso 1, `mvp/pruebas/prompt_v10.md`; paso 2, `mvp/pruebas/prompt_datos_v1.md` —una
unidad por turno: devuelve `caso`, `datos` (`aspecto · valor · unidad_valor`) y
`dudas`—. El paso 1 de la ronda cerrada (v9) y el candidato
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
| Hace | ejecuta la herramienta, lleva los mensajes, registra (crudo, traza, salida) | — |
| Piensa | **nada**: no interpreta la pregunta, no elige casos, no juzga la entrega | qué casos pedir; qué responder; cuándo parar |
| **Memoria** | los mensajes de la consulta | **ninguna** |
| Propone | — | la respuesta, en el JSON de `RESPUESTA_JSON` |
| Juzga | **no juzga** | no ejecuta ni calcula |

El juicio no se pierde: vive en la **evaluación** (§12), fuera del ORQ. Es la
separación «control/contenido» del plan: el orquestador no comprueba la entrega ni
la cobertura, solo orquesta.

---

## 2. El corpus: `doc4` y `doc6` radicados

Los documentos radicados son **`doc4`** (el corte de agua) y **`doc6`** (el puente
peatonal sobre la avenida Los Nogales): los textos de pruebas, copiados tal cual, con
su `sello`.

- **`doc4`**: `mvp/corpus/documentos/doc4.md` (copia de `mvp/pruebas/doc4.md`)
  - paso 1 (v10, Muse): `extraccion/doc4/p1-doc4-v10-muse-r1.out` → 5 unidades;
    `[1–3]`, `[4–6]`, `[7]`, `[8,9,10,13–17]`, `[11,12]`
  - paso 2 (`prompt_datos_v1`, r2): `extraccion/doc4/p2-doc4-u{1..5}-r2.out`
  - lo que dio: **5 casos y 26 datos**. Las dos dudas de `U4` —el referente de «Su
    reclamo» y de «Su decisión»— quedan en el crudo del paso 2: la base no las guarda
    (§3).
- **`doc6`**: `mvp/corpus/documentos/doc6.md` (copia de `mvp/pruebas/doc6.md`; el texto
  y su batería de preguntas entraron el 07-10)
  - paso 1 (v10, Muse): `extraccion/doc6/p1-doc6-v10-muse-r1.out` → **14 unidades**
  - paso 2 (`prompt_datos_v1`, r1): `extraccion/doc6/p2-doc6-u{1..14}-r1.out`
  - lo que dio: **14 casos y 33 datos**.

Cada documento radicado trae su batería de preguntas: `doc4` la de `preguntas.md` y
`doc6` la de `preguntas-doc6.md` (§4.1). `doc5` (los tranvías) no está radicado: sus
preguntas, su partición v9 y sus fichas quedan fuera.

**Radicar es fijar.** Un documento radicado no cambia: si su texto cambia, eso es
**otro documento**, con su radicación y su fila propias. El `sello` (sha256 de lo
radicado) es el guardián: si el archivo ya no coincide, el cargador se detiene y
reporta. Una **mudanza** de archivo es otra cosa —el documento es el mismo y el
sello no cambia— y se resuelve con una actualización de la base, autorizada.

**Conflictos.** Con `doc4` y `doc6` hay dos fuentes en el mismo dominio, pero sus
hechos no se contradicen: el conflicto entre fuentes sigue **sin ejercitar**.
Ejercitarlo pide un hecho disputado entre documentos, o la mesa de dominio (`M1` 42
plazas frente a `M2` 47). **Abierto.**

**La declaración del esquema** —con qué partición, qué prompt, con qué hash y con
qué modelo se extrajo— **no está en la base**: el cargador registra el sello del
documento, no el del esquema. **Abierto.**

---

## 3. La base: dos tablas en SQLite

La base es `mvp/corpus/corpus.db` (SQLite, 40 KB), y la construye
`mvp/corpus/cargar_corpus.py` desde los documentos radicados y los crudos de la
extracción.

```sql
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,   -- doc4, doc6
  dominio            TEXT NOT NULL,      -- GENERAL
  fecha_radicacion   TEXT NOT NULL,      -- 2026-10-07
  ubicacion_local    TEXT NOT NULL,      -- …/documentos/doc4.md, …/doc6.md
  ubicacion_upstream TEXT NOT NULL,      -- …/blob/main/…/doc4.md, …/doc6.md
  commit_publicacion TEXT,               -- el commit que publica el documento
  sello              TEXT NOT NULL       -- sha256 de lo radicado
);

CREATE TABLE datos (
  id           TEXT PRIMARY KEY,         -- doc4:U1:D4, doc6:U7:D1
  unidad_id    TEXT NOT NULL,            -- doc4:U1, doc6:U7
  caso         TEXT NOT NULL,            -- el caso de esa unidad
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT                      -- "horas", "años", …
);
```

Contenido: **2 documentos** (`doc4` y `doc6`, ambos `GENERAL`), **59 datos**,
**19 casos** (doc4: 26 datos en 5 casos · doc6: 33 datos en 14 casos).

| id | unidad_id | caso | aspecto | valor | unidad_valor |
|---|---|---|---|---|---|
| doc4:U1:D1 | doc4:U1 | el corte de agua anunciado en el barrio San Jorge… | anunciante del corte | la empresa de acueducto | — |
| doc4:U1:D4 | doc4:U1 | … | duración del corte | catorce | horas |
| doc4:U5:D3 | doc4:U5 | el corte similar al anunciado ocurrido el año pasado… | duración del corte | diecinueve | horas |

**Qué NO guarda la base, y por qué:**

- **El texto del documento**, ni las oraciones, ni sus números: el texto vive en el
  documento radicado, que es la **fuente única**. La numeración de oraciones es la
  vara con la que se evalúa el paso 1 (§12): vive en los crudos de la extracción.
- **La tabla de unidades**: la unidad existe como columna en cada dato —`unidad_id` y
  `caso`—, así que cada fila se lee sola y agrupar por caso es una consulta de una
  línea.
- **La tabla de dudas**: las dudas quedan en el crudo del paso 2.
- **`documento_id` en `datos`**: el documento de un dato se conoce por el prefijo de
  su `unidad_id` (`doc4:U1` → `doc4`). Es una convención sobre el texto del id, no un
  dato. **Abierto.**

**Por qué SQLite.** La forma se elige por **forma de acceso**, y acá lo que manda es
leer un caso entero y filtrar por dominio y por caso: eso pide claves, foráneas y
consultas, no un molde único. SQLite viene en la biblioteca estándar, no tiene
servidor, y el archivo es uno. La discusión clásica dice lo mismo: el problema no es
el formato de serialización sino qué operaciones se hacen
([flat files vs SQLite](https://sqlite.org/forum/forumpost/c43b208884?t=h),
[hilo sobre JSON y SQLite](https://github.com/kody-w/rappterbook/discussions/3742)).
Con 26 filas cualquier cosa funciona; el motor se elige por lo que se hace con los
datos, no por el volumen.

**Es un derivado regenerable.** La construcción es idempotente: borrar `corpus.db` y
correr el cargador reproduce lo mismo. La fuente de verdad son **los documentos y
los crudos**, no el almacén. Lo único append-only es `traza.jsonl`. Esto evita
migraciones, copias de seguridad y versionado de la base.

**Invariantes que el cargador puede exigir:**

- Un documento radicado tiene **una unidad o más**: un documento sin unidades no es
  un estado válido, es una extracción que falló (§14). Una línea es una unidad
  temática: `doc4:U3` es una sola oración y produjo 4 datos.
- Si el documento no está donde dice su `ubicacion_local`, el cargador **se detiene
  y reporta**.

**El vacío legítimo** es de nivel unidad: una unidad cuyas oraciones no establezcan
nada, que no aporta ningún dato. El cargador puede avisarlo en la carga.

---

## 4. Entradas

### 4.1. Archivos de preguntas (es el usuario)

Dos archivos, **solo el texto de las preguntas, limpias** —sin condiciones, sin
expectativas, sin pistas—: `mvp/corpus/consulta/preguntas.md` (las cinco de `doc4`) y
`mvp/corpus/consulta/preguntas-doc6.md` (las cinco de `doc6`). Es lo único que aporta
el usuario, junto con el dominio elegido.

`preguntas.md` (`doc4`):

```
1. ¿Qué empresa anunció el corte de agua y en qué barrio?
2. ¿Cuántas horas va a durar el corte de agua anunciado?
3. ¿Cuál es la causa del corte anunciado?
4. ¿La junta de acción comunal logró que el corte no se hiciera en semana de exámenes?
5. ¿A quién pertenecía el reclamo que quedó registrado en el acta?
```

`preguntas-doc6.md` (`doc6`):

```
1. ¿Sobre qué vía se construirá el puente peatonal y cuánto medirá de largo?
2. ¿Cuánto costará el puente y según qué?
3. ¿Por qué los vecinos del barrio La Esperanza pidieron el puente?
4. ¿Cuántas rampas tendrá el puente?
5. ¿De quién era la recomendación que se conocerá en abril?
```

En la batería de `doc4`, la 4 es la que el corpus **no** responde con un valor (la
decisión se conocerá el miércoles) y la 5 es la que el documento deja con el referente
abierto; en la de `doc6`, la 4 pide un número que el texto no da.

### 4.2. R

`mvp/corpus/consulta/R.json` es **un JSON que lee el ORQUESTADOR**. El agente **no
lo ve**: R se aplica ofreciendo —qué fuentes se admiten, qué herramientas se
ofrecen, qué operaciones existen—, no se le explica.

```json
{
  "fuentes_admitidas": ["solo el documento"],
  "herramientas": ["obtener_datos_del_caso"],
  "operaciones": []
}
```

| Clave | Qué dice | Quién la aplica |
|---|---|---|
| `fuentes_admitidas` | la única fuente es el documento radicado | el ORQ |
| `herramientas` | qué se le ofrece; lo que no está, no se le da | el ORQ, al armar `tools` |
| `operaciones` | ninguna: sin aritmética ni fechas calculadas | el ORQ, no ofreciendo nada |

Se fija antes de la corrida y queda registrada en el crudo. **Los topes de turnos y
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
| 1 | Leer la configuración | `orq/leer_config.py` | rutas, dominio, modelo, guardias, etiqueta del crudo |
| 2 | Leer la pregunta | `orq/leer_pregunta.py` | la pregunta n del archivo, tal cual |
| 3 | Leer R | `orq/leer_r.py` | el JSON del orquestador |
| 4 | Abrir la base | `orq/abrir_db.py` | `corpus.db`, **solo lectura** |
| 5 | Resolver el dominio | `orq/resolver_dominio.py` | la etiqueta `GENERAL` → sus documentos (pertenencia, sin juicio) |
| 6 | Listar los casos | `orq/listar_casos.py` | `unidad_id` y `caso`, sin aspectos ni valores |
| 7 | Armar las herramientas | `orq/armar_herramientas.py` | R ∩ las que existen |
| 8 | Armar los mensajes | `orq/armar_prompt.py` + `prompt_agente.md` | el `system` (anclas) y el `user` (casos, tarea, formato) |
| 9 | El bucle | `orq/llamar_modelo.py`, `orq/ejecutar_herramienta.py`, `orq/obtener_datos_del_caso.py`, `orq/bucle.py` | llama, ejecuta lo que el agente pide, apila, y termina con la respuesta |
| 10 | Registrar y entregar | `orq/guardar_crudo.py`, `orq/registrar_traza.py`, `orq/escribir_salida.py` | el crudo, la traza y `salida.md` |

`orq/orquestador.py` es el `main`: los llama en ese orden y nada más. Cada paso vive
en su archivo; `orq/config.json` tiene las rutas, el dominio, el modelo, las
guardias y la etiqueta del crudo (plantilla por pregunta).

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

## 7. La herramienta: una sola

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

Vive en `mvp/corpus/consulta/orq/prompt_agente.md`, **un solo archivo** con dos
partes marcadas: `[SISTEMA]` (lo que se conserva entre turnos) y `[TAREA]` (lo que
depende del dominio y de la pregunta). `armar_prompt.py` lo parte y devuelve los dos
mensajes. Los huecos son `{{CASOS}}`, `{{PREGUNTA}}` y `{{ANCLAS}}`, rellenados con
`str.replace` —nunca `str.format`—.

```
[SISTEMA]
ANCLAS: {{ANCLAS}} (día y hora del sistema; no es dato del documento)

[TAREA]
CASOS:
{{CASOS}}

TAREAS:
1. Escoge los id de los casos que con probabilidad mayor al 80% contengan la respuesta a la
   siguiente pregunta: {{PREGUNTA}}.
2. Si no hay casos que cumplan la condición anterior, pasa al punto 6 de TAREAS.
3. Utiliza la HERRAMIENTA obtener_datos_del_caso para obtener los datos de los casos
   seleccionados. Podés pedir varios casos en un mismo turno.
4. Si con los datos obtenidos no se puede dar respuesta a la pregunta, pasa al punto 6 de TAREAS.
5. Con los datos obtenidos arma una respuesta corta y autocontenida.
6. Diligencia el JSON en RESPUESTA_JSON.

RESPUESTA_JSON:
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_el_corpus", "respuesta": ""}
```

**Lo que el prompt no lleva, a propósito:** no hay bloques `ROL`, `REGLAS` ni
`ALCANCE`; no lleva R (la aplica el ORQ); no lleva el esquema de las herramientas
(viaja en `tools`); no dice el dominio ni los documentos —los casos son lo que el
agente necesita para elegir—.

**El umbral del 80%** es el criterio de selección: el agente mira los nombres de los
casos y pide los que podrían contener la respuesta. Los nombres son resúmenes: hay
aspectos que el nombre del caso no nombra. La pregunta «¿a qué hora empieza el
corte?» no aparece en el nombre de `U1` («… su **duración** de catorce horas y los
usuarios afectados»), y el dato existe (`doc4:U1:D5`, «desde las seis de la mañana»).
**Abierto:** si el criterio debe mirar algo más que el nombre.

---

## 9. La respuesta

El agente entrega un JSON con dos estados:

```json
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_el_corpus", "respuesta": ""}
```

**El JSON no tiene campo propio**: como no hay herramienta de entrega, vive **dentro**
del mensaje final, junto a lo que el agente escriba alrededor. Eso tiene una
consecuencia medida (§13): si el modelo envuelve el JSON en un bloque de código, o escribe prosa
antes, el ORQ no lo lee y registra «respuesta del agente (sin JSON)». Dos formas de
resolverlo, sin decidir:

1. **En el ORQ**: extraer del contenido el primer bloque `{…}` bien formado, en vez
   de exigir que todo el mensaje sea JSON. No es juzgar: es leer.
2. **En el prompt**: que la tarea 5 diga que la respuesta corta va **en el campo
   `respuesta`** y que el mensaje final sea **solo** el JSON.

**El ORQ no juzga la entrega**: la registra tal como vino y la escribe en la salida.
Si el agente no contesta, la salida dice que no contestó.

**Lo que el sobre mínimo no lleva:** ni los datos que sostienen la respuesta (la
ruta), ni un reporte de lo recorrido. La salida muestra la respuesta y qué casos se
leyeron. El sostén —que el usuario vea de dónde salió— **queda para cuando el usuario
lo pida**.

---

## 10. Salidas

- **`mvp/corpus/consulta/salida.md`** (lo que lee el usuario): por pregunta, la
  respuesta tal como vino, y los casos leídos. Se **agrega**, no se reescribe.
- **`mvp/corpus/consulta/traza.jsonl`** (append-only): una línea por corrida con las
  anclas, la pregunta, el dominio y los documentos, los casos, los casos leídos, las
  herramientas ofrecidas, los turnos, las llamadas, el desenlace, si cerró y el
  consumo por turno, más la ruta del crudo.
- **`mvp/corpus/consulta/cache/consulta-<documento>-q{n}-r{k}.json`** (`doc4` y `doc6`):
  el crudo de la corrida —los cuerpos enviados y las respuestas, con los trozos SSE
  verbatim y sin cabeceras—. No se sobrescribe: una réplica nueva lleva un `k` nuevo.

---

## 11. Guardias y presupuesto

Las guardias **no son R**: R dice qué se puede usar; esto solo corta si el bucle se
enreda.

- **Modelo:** alias `v2/deepseek` = `deepseek-flash`, con razonamiento encendido
  (`thinking: enabled`) y `reasoning_effort: low`. El transporte es `stream: true`
  (excepción autorizada: stream es transporte, no cambia la salida), y `call_model`
  ensambla los deltas: `content`, `reasoning_content`, `tool_calls` y
  `finish_reason`.
- **De a una:** se manda una pregunta; la siguiente, cuando termina la corrida.
- **Guardias implementadas:** `max_turnos: 8` y `max_herramientas: 20`. **No hay
  corte por ciclo** (misma acción con los mismos argumentos dos veces): `doc4` q5 y
  `doc6` q2 pidieron dos veces el mismo caso. **Abierto.**
- **El consumo de las corridas** (`prompt_tokens = hit + miss`):

| Corrida | Turnos | Turno 1 | Turnos siguientes |
|---|---|---|---|
| doc4 Q1 r1 | 2 | 1501 = 0 + 1501 | 1887 = 1536 + 351 |
| doc4 Q1 r2 | 2 | 1020 = 0 + 1020 | 2393 = 1280 + 1113 |
| doc4 Q2 r1 | 2 | 1502 = 0 + 1502 | 1886 = 1536 + 350 |
| doc4 Q2 r2 | 2 | 1021 = 0 + 1021 | 1432 = 1024 + 408 |
| doc4 Q3 r1 | 2 | 1016 = 0 + 1016 | 1408 = 1024 + 384 |
| doc4 Q4 r1 | 2 | 1030 = 0 + 1030 | 2155 = 1152 + 1003 |
| doc4 Q5 r1 | 3 | 879 = 0 + 879 | 1604 = 1024 + 580 · 3023 = 2432 + 591 |
| doc4 Q5 r2 | 2 | 879 = 0 + 879 | 1584 = 896 + 688 |
| doc6 Q1 r1 | 2 | 1431 = 0 + 1431 | 2011 = 1664 + 347 |
| doc6 Q2 r1 | 6 | 1421 = 0 + 1421 | 1704 = 1536 + 168 · 2105 = 1920 + 185 · 2445 = 2176 + 269 · 2717 = 2560 + 157 · 3001 = 2816 + 185 |
| doc6 Q3 r1 | 2 | 1426 = 0 + 1426 | 1768 = 1536 + 232 |
| doc6 Q4 r1 | 2 | 1420 = 0 + 1420 | 2221 = 1792 + 429 |
| doc6 Q5 r1 | 2 | 1423 = 0 + 1423 | 1828 = 1536 + 292 |

  Lectura: el **prefijo fijo se cachea** (el `hit` aparece desde el segundo turno) y
  lo que se paga es lo nuevo —cada resultado de herramienta y cada mensaje del
  asistente—. El precio se calcula con la tarifa publicada el día de la corrida y se
  registra; no se estima a ojo.
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
- las **unidades examinadas** quedan registradas (los casos leídos están en la traza
  y en la salida), y se distinguen del campo;
- **no interviene Jev**: el juicio es nuestro y se registra.

La **vara** para distinguir el hueco del documento del hueco de la extracción son los
números de oración de la partición del paso 1: viven en los crudos
(`extraccion/doc4/p1-doc4-v10-muse-r1.out` y
`extraccion/doc6/p1-doc6-v10-muse-r1.out`) y en el material de evaluación, no en la
base (§3).

---

## 13. Medición de las corridas

Trece corridas: ocho con `doc4` (26 datos, 5 casos) —las cinco preguntas y una réplica
de q1, q2 y q5— y cinco con `doc6` (33 datos, 14 casos), una por pregunta.

| Corrida | Casos pedidos | Distintos | Turnos · llamadas | Qué entregó |
|---|---|---|---|---|
| doc4 Q1 `-r1` | `U1` | 1 | 2 · 2 | respondida: la empresa de acueducto, en el barrio San Jorge |
| doc4 Q1 `-r2` | `U1`, `U3`, `U4` | 3 | 2 · 4 | respondida: la empresa de acueducto, en el barrio San Jorge |
| doc4 Q2 `-r1` | `U1` | 1 | 2 · 2 | respondida: catorce horas |
| doc4 Q2 `-r2` | `U1` | 1 | 2 · 2 | respondida: catorce horas (desde las seis de la mañana del jueves) |
| doc4 Q3 `-r1` | `U2` | 1 | 2 · 2 | respondida: la reparación de una tubería matriz en la carrera séptima |
| doc4 Q4 `-r1` | `U4`, `U1` | 2 | 2 · 2 | sin entrega: el JSON vino como texto |
| doc4 Q5 `-r1` | `U4`, `U4` | 1 | 3 · 2 | sin JSON leído: vino envuelto en ```json |
| doc4 Q5 `-r2` | `U4` | 1 | 2 · 1 | sin JSON leído: prosa + ```json |
| doc6 Q1 `-r1` | `U1`, `U3` | 2 | 2 · 2 | respondida: la avenida Los Nogales, sesenta metros |
| doc6 Q2 `-r1` | `U4`, `U13`, `U1`, `U2`, `U4` | 4 | 6 · 5 | sin JSON leído: el JSON vino envuelto en una cerca |
| doc6 Q3 `-r1` | `U5` | 1 | 2 · 1 | respondida: la muerte de un estudiante atropellado en 2023 |
| doc6 Q4 `-r1` | `U7`, `U12` | 2 | 2 · 2 | sin JSON leído: prosa, y el JSON decía `no_esta_en_el_corpus` |
| doc6 Q5 `-r1` | `U12` | 1 | 2 · 1 | respondida: la secretaria de Infraestructura |

Nunca pidió todos los casos —ni los 5 de `doc4` ni los 14 de `doc6`: filtra por el
umbral del 80 % sobre los nombres. La más larga fue `doc6` Q2, que pidió `U4` dos veces
y gastó 6 turnos y 5 llamadas.

**Dos mecanismos de entrega, no comparables en ese detalle.** Las seis primeras corridas
de `doc4` —q1, q2, q3 y sus réplicas— entregaban con la herramienta `entregar`: su crudo
trae `datos` y `reporte`, y su `contenido_final` está vacío. Desde «fuera la herramienta
entregar» (07-10), la entrega es el **mensaje final**, y así corrieron `doc4` q4–q5 y todo
`doc6`. El campo `herramientas` del crudo dice con cuál se hizo cada corrida.

**Lo que la medición deja a la vista:**

1. **El JSON como texto** (doc4 Q4): con la entrega por herramienta, el agente escribió el
   JSON en su mensaje final y no llamó `entregar`, así que la entrega quedó ausente
   (`cerrado: false`, `contenido_final` vacío). Con la entrega por mensaje final (§7), ese
   JSON se lee.
2. **El JSON envuelto** (doc4 Q5, las dos réplicas; doc6 Q2): el agente escribe,
   además del JSON, la prosa que le pide la tarea 5 y la cerca de código; el ORQ exige
   que el contenido empiece con `{`, así que no lo lee (§9). Son las cuatro corridas que
   ya usaban la entrega por mensaje final y quedaron sin leer.
3. **El referente abierto** (doc4 Q5): la corrida entregó `respondida`, con el reclamo
   atribuido a la junta de acción comunal. Los datos leídos de `U4` no incluyen el
   referente del reclamo; la extracción del paso 2 declaró dos dudas sobre los
   referentes («Su reclamo», «Su decisión»).

---

## 14. Riesgos y límites

- **La extracción acota la respuesta** (hallazgo del paso 2, no defecto del puente).
- **El JSON de salida no se lee** si viene con prosa o envuelto (§9).
- **El prompt es el único canal.** Lo que el ORQ no ponga, el agente no lo sabe: si
  no le pasa un caso, no existe para él.
- **El historial crece por turno** (medido, §11): de ahí el tope de turnos.
- **Devolver el `reasoning_content`**: con `tools` en la petición, si no vuelve en
  todos los turnos, la API responde 400.
- **Un solo documento ⇒ sin conflicto** (§2).
- **Una extracción que falla detiene el proceso**: no produce un documento vacío ni
  una unidad vacía; produce una corrida cortada. Un documento **sin** unidades no es
  un estado válido (§3).

---

## 15. Decisiones

| # | Decisión | Estado |
|---|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO | decidida; vocabulario en §17 |
| **D2** | Corpus: solo `doc4`, o `doc4` + otro documento para tener conflicto | decidida en parte: `doc4` y `doc6` radicados; el conflicto entre fuentes sigue sin ejercitarse (§2) |
| **D3** | Bucle con herramienta, o todo inyectado en una llamada | decidida: bucle con herramienta |
| **D4** | Sin datos derivados en esta versión | decidida |
| **D5** | R: `solo el documento`, sin mundo del LLM ni anclas como premisa | decidida: R.json con tres claves |
| **D6** | Nombre y sitio de los archivos | decidida: base y documento en `mvp/corpus/`, consulta y código en `mvp/corpus/consulta/` |
| **D7** | Almacén | decidida: SQLite con dos tablas (`documentos`, `datos`) |
| **D8** | Derivados | fuera de esta versión |
| **D9** | Idioma de los `tipo` | obsoleta: no hay tipos |
| **D10** | Documento R: esbozo + prosa para el agente | reemplazada: R es un JSON que lee el ORQ |
| **D11** | Compactación del historial | no implementada: el historial crece y corta el tope de turnos |
| **D12** | «Mundo del agente» en los documentos vivos | sigue como vocabulario; sin efecto en el código |
| **D13** | Herramientas: (A) protocolo textual o (B) nativas | decidida: (B), aditivo sobre `call_model` |
| **D14** | Prompts de la extracción | decidida: `prompt_v10` y `prompt_datos_v1` |
| **D15** | Salida del paso 2 | decidida: `caso`, `datos`, `dudas`, una unidad por turno |
| **D16** | `unidad_valor`: campo propio o dentro del `valor` | abierta — se usa poco (3 de 26 datos en `doc4`; 4 de 33 en `doc6`) |
| **D17** | El agente, ¿lee texto del documento o solo los datos extraídos? | decidida: solo los datos |
| **D18** | El ORQ, ¿juzga la entrega? | decidida: no; el juicio vive en la evaluación (§12) |
| **D19** | La entrega, ¿por herramienta o por mensaje final? | decidida: mensaje final |
| **D20** | Cómo se lee el JSON de salida cuando viene con prosa o envuelto | abierta: 5 de 13 corridas quedaron sin entrega leída (§9) |
| **D21** | Las condiciones que el código no puede aplicar (premisa, conflictos, brecha) | abierta: no están escritas en ninguna parte (§4.2) |
| **D22** | `documento_id` en `datos`, en vez del prefijo del id | abierta |
| **D23** | La declaración del esquema (partición, prompt, hash, modelo) en la base | abierta |
| **D24** | El sostén en la respuesta (datos citados, reporte) | diferida: cuando el usuario pida ver la fuente |
| **D25** | Tope y corte por ciclo | abierta: hay tope de turnos y de llamadas; no hay corte por repetición |

---

## 16. Qué se reutiliza

- `niveles/run_niveles.py`: `call_model` —con `messages` y `tools` opcionales, y
  acumulando `tool_calls` y `finish_reason`— y `extract_json`.
- `mvp/corpus/cargar_corpus.py`: el cargador de la base (§3).
- `mvp/corpus/consulta/orq/`: el orquestador, un archivo por paso (§5).
- `test_tool_calling/`: las corridas que fijaron la mecánica del bucle y las
  lecciones del tool calling.
- `unidades/extraer_unidades.py`: `numerar_oraciones` —para la evaluación, no para la
  base—.
- `mvp/pieza1/pieza1.py`: `verificar` y `comparar` —para la evaluación—; `guardar` y
  `mantener` quedan sin uso mientras no haya derivados.
- `unidades/ficha_doc.py`: `verificar` y `fragmentos`, si el respaldo literal vuelve.
- Los crudos de la extracción de `doc4` y `doc6` (§2).

---

## 17. Vocabulario (D1)

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

**Divergencia declarada:** [pieza1/esquema2.md](pieza1/esquema2.md) sigue rotulando
`mundo: orquestador` en su lista de R, por compatibilidad con la pieza 1 en prueba;
se renombra al adoptar el esquema. Por un cambio de etiqueta no se tocan `pieza1.py`
ni sus tablas de referencia.

---

## 18. Fuentes consultadas

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
