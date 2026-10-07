# Consulta completa de Zettel (v1) · diseño para afinar

Fecha: 06-10-2026. **Estado: borrador de diseño; nada implementado.** Este
documento es la superficie de trabajo: se afina aquí antes de escribir código y
antes de llamar a un modelo. **Lo que sigue (07-10): revisar el prompt del
AGENTE ENCARGADO** (§8–§9), con la extracción ya fijada.

**Para qué.** Construir el **primer recorrido completo** de Zettel sobre el
corpus: recibir una pregunta y entregar una respuesta respaldada, un conflicto o
una explicación precisa de lo que no se puede establecer, con el recorrido
registrado.

**Qué se considera terminado.** Una ejecución acotada de ese recorrido, sobre un
dominio y unas preguntas fijadas antes, evaluada contra lo que se dejó escrito:
si la respuesta es fiel y está justificada, y si lo que no se puede establecer se
dice con precisión.

**Base.** [orquestador-plan.md](../historico/orquestador-plan.md) §3 (estaciones) y §11 (F0,
F1); el contrato de [mesa-dominio-plan.md](mesa-dominio-plan.md) §9 y su cierre;
la extracción cerrada del paso 2 ([paso2/informe_paso2.md](paso2/informe_paso2.md)).
**Prompts de trabajo (07-10):** paso 1, `mvp/pruebas/prompt_v10.md`; paso 2,
`mvp/pruebas/prompt_datos_v1.md` —una unidad por turno: devuelve `caso`, `datos`
(`aspecto · valor · unidad_valor`) y `dudas`—. El paso 1 de la ronda cerrada (v9) y el
candidato `prompt_ficha_contexto.md` quedan **congelados**: no se reabren ni se adoptan.
Sin Jev y sin búsqueda externa.

---

## 1. Reparto de papeles

En esta versión, **el código es el ORQUESTADOR y el LLM es el AGENTE ENCARGADO**.
Es la separación «control/contenido» del plan: **el orquestador no piensa** —
resuelve, aplica, ejecuta, comprueba, calcula y registra, todo determinista— y
**el agente es el que piensa** —interpreta, selecciona y propone—.

| | Orquestador (el código) | Agente encargado (el LLM) |
|---|---|---|
| Prepara | configuración, dominio, documentos admitidos, anclas | — |
| Entrega | inventario y lectura de unidades por la tool | — |
| Hace | ejecuta las acciones, calcula fechas y aritmética, comprueba, registra | — |
| Piensa | **nada**: aplica la pertenencia por dominio, R y las guardias | qué unidades leer; qué datos son campo; qué sostiene una respuesta |
| **Memoria** | lleva el estado y arma el prompt de cada llamada | **ninguna**: es stateless, solo sabe lo que va en el prompt |
| Propone | — | encabezado, tablas, brechas y respuesta |
| Juzga | no juzga contenido | no ejecuta acciones ni calcula por su cuenta |

**D1 (decidida).** **Código = ORQUESTADOR, LLM = AGENTE ENCARGADO.** El agente es
**stateless**: cada llamada es una interacción nueva y solo sabe lo que va en el
prompt; el orquestador es quien lleva la memoria y compone cada prompt (§6). La
coherencia de esta etiqueta con los documentos vivos está en §17.

---

## 2. Corpus: un documento

Trabajamos con las extracciones existentes. El documento elegido es **`doc5`
(los tranvías)**, el que más rindió en la ronda del paso 2, entrada (b):

| Documento | Unidades | Recuperación estricta (b) | Fidelidad (b) | Referencias | Dudas |
|---|---|---|---|---|---|
| **`doc5`** | 5 | **17/17 = 100 %** | **37/37 = 100 %** | 8 | 3 |
| `doc4` | 6 | DeepSeek 22/24; Muse 23/24 | DeepSeek 74/76 (fusión en U5); Muse 37/37 | 11 | 5 |

Material medido de `doc5` (entrada b, `deepseek-flash`): 5 unidades, **14
determinaciones**, 3 capas, 11 acciones, 9 relaciones, 10 marcas, 3 dudas, 8
referencias, 31 casos.

- Documento: `mvp/pruebas/doc5.md`
- Partición congelada de v9: `mvp/pruebas/salida_prueba9-v9-doc5.md`
- Fichas por unidad (crudos del paso 2): `mvp/paso2/cache/comp-doc5-b-u{1..5}-deepseek-r1.json`
  (la ficha es el campo `parsed`; hoy no tiene archivo propio: el cargador lo estabiliza)
- Las unidades: `U1 [1–3]`, `U2 [4–7]`, `U3 [8–11]`, `U4 [12,13,17]`, `U5 [14–16]`.

**Declaración del esquema.** Cada documento registra con qué se extrajo:
partición (v9), prompt candidato con su hash, modelo y fecha de radicación. El
candidato es **provisional**: el corpus no lo presenta como extracción adoptada.

**Conflictos.** Con un solo documento no hay conflicto entre fuentes. Si se
quiere ejercitar ese desenlace en esta simulación, hace falta un segundo corpus
(la mesa de dominio: `M1` 42 plazas frente a `M2` 47, con `M2:S1` acreditando el
mismo refugio y la misma noche), cuyos datos son a mano. **D2.**

---

## 3. El corpus consultable: una configuración mínima

La recomendación es **elegir por forma de acceso** en vez de meter todo en un
mismo molde. La discusión clásica en
torno a SQLite lo dice bien: el problema no es el formato de serialización, sino
**qué forma tienen los datos y qué operaciones se hacen con ellos**; hay tablas
de consulta, flujos que solo se agregan y relaciones que piden cruces, y cada uno
tiene su formato natural ([SQLite: flat files vs SQLite](https://sqlite.org/forum/forumpost/c43b208884?t=h),
[hilo sobre JSON y SQLite](https://github.com/kody-w/rappterbook/discussions/3742)).

### 3.1. La forma: tres artefactos de corpus, dos logs y una vista

| Artefacto | Forma | Qué guarda |
|---|---|---|
| `documentos.json` | objeto JSON | una fila por documento: `id`, ruta, dominio, `radicacion`, fecha propia si el texto la trae, y la **declaración del esquema** (partición, prompt + hash, modelo) |
| `unidades.jsonl` | log de líneas | una fila por unidad: `id`, documento, dominio, **`caso`** (lo que nombra su núcleo), **`contenido`** (el texto de sus oraciones, en un párrafo y sin numeración) y `oraciones` (los números de la partición) |
| `inscripciones.jsonl` | log de líneas | una fila por **lo que la unidad establece**: `tipo` (**dato** · **duda**), con `id`, `unidad` y `cuerpo` (`caso`, `aspecto`, `valor`, `unidad_valor` en el dato; `texto` en la duda). Las otras listas de la ficha —relación, acción, capa, marca— y las columnas `condiciones`, `respaldo`, `inferido` y `dentro_de` quedan **fuera de esta versión** |
| `traza.jsonl` | log append-only | el recorrido de cada consulta; **no es corpus** |
| `corpus.jsonl` | log append-only | los datos derivados, en la forma de [pieza1/esquema2.md](pieza1/esquema2.md) §5 — **no se usa en esta versión** |

La tabla **`datos`** que ve el agente es una **vista** sobre `inscripciones`
(`tipo = "dato"`). Así se conservan tus dos tablas —unidades y datos— sin siete
tablas: `leer_unidad` devuelve la unidad con sus datos y sus dudas.

**De dónde salen (07-10).** `unidades` se genera con la partición del paso 1
(`mvp/pruebas/prompt_v10.md`): el `caso` de cada unidad lo nombra el `subtema` que
devolvió, el `contenido` es el texto de sus oraciones —en un párrafo y sin
numeración— y los ids los pone el código (`doc5:U1`). `inscripciones` se genera con el
paso 2 (`mvp/pruebas/prompt_datos_v1.md`), que corre **una unidad por turno**: devuelve
`caso`, `datos` (`aspecto · valor · unidad_valor`) y `dudas` de esa unidad. La partición
del paso 1 **no garantiza contigüidad** —una unidad puede tener oraciones posteriores a
las de la siguiente (`doc4`: `[8, 9, 10, 13–17]` antes de `[11, 12]`)— y los ids van por
el orden del arreglo: el orden de lectura se resuelve por la primera oración, no por el id.

**Identificadores.** `documento` (`doc5`) · `unidad` (`doc5:U1`) · `dato`
(`doc5:U1:D1`) · `oración` (`doc5:S2`) · derivado (`DD1`, global, diferido en esta
versión). El `caso` de los datos es el de su unidad: no hay ids de caso en esta versión,
y las menciones de dos unidades **nunca** se comparan; dos menciones son el mismo caso
solo por declaración del documento o criterio explícito. Sin fusión.

**El corpus es un derivado regenerable.** `documentos`, `unidades` e
`inscripciones` se **generan** con un cargador idempotente a partir de los
documentos, la partición del paso 1 y los datos del paso 2 (con el hash del esquema);
si cambia el cargador, se regeneran. Lo único append-only es `traza.jsonl`
(`corpus.jsonl` entra cuando haya derivados, y por ahora no los hay). Esto evita migraciones, copias de seguridad y versionado de la
base: **la fuente de verdad son los documentos y los crudos, no el almacén.**

**Módulo.** El cargador/registro vive en `mvp/consulta/` (nombre por confirmar);
es el subpaso 1 y no llama a ningún modelo.

### 3.2. Por qué esta forma y no otra

- **Una fila por inscripción, con su respaldo y su radicación**, es la forma del
  dato en el marco (un valor que queda, recuperable) y también la de las
  *nanopublicaciones*: aserción + procedencia + información de publicación en una
  unidad pequeña y autocontenida ([guía](https://nanopub.net/guidelines/working_draft/),
  [modelo unificado](https://arxiv.org/html/2006.06348v1)). Tomamos **la forma,
  no la pila**: nada de RDF ni SPARQL.
- **Reificación selectiva.** Cuando el respaldo cabe en la fila, va en la fila; se
  crea una entidad aparte («claim») solo si el hecho está en disputa, acotado en
  el tiempo o reemplazado ([Evidence Model](https://cdn.jsdelivr.net/npm/@a5c-ai/atlas@5.0.1-staging.f17326334/graph/schema/evidence-model.md)).
  Traducido: el dato lleva su respaldo; el **conflicto no se almacena**, se
  calcula (dos filas admisibles con las mismas condiciones) y se registra en la
  traza.
- **Bitemporalidad barata.** La lección del log de aserciones bitemporal es
  guardar *cuándo es verdad en el mundo* y *cuándo el sistema lo supo*, con un
  log append-only como fuente de verdad, y **no optimizar hasta que haya un
  cuello de botella medido** ([knk](https://github.com/cs0lar/knk)). Aquí son dos
  columnas, `radicacion` y la fecha propia del documento; ni motor temporal ni
  índices versionados.
- **Sin resolución de entidades.** La resolución de entidades es la parte que
  convierte un grafo en un elefante, y las fusiones hay que hacerlas
  **no destructivas** (nodo canónico + fuentes conservadas, poder deshacer)
  ([Entity Resolution](https://archtin.com/blog/entity-resolution-in-knowledge-graphs),
  [guía de grafos](https://www.dataaihub.co/learn/knowledge-graphs)). Zettel ya
  decidió lo contrario: ids locales y **reidentificación acreditada al consultar**
  (mesa de dominio, cierre). Eso elimina el subsistema entero.
- **Formato por operación:** la consulta puntual pide un objeto JSON; el flujo de
  inscripciones y la traza piden un log de líneas; los cruces relacionales
  pedirían SQL solo si el corpus creciera. Un formato único para todo es una
  falsa economía (mismo hilo de arriba).

### 3.3. Alineación con la visión

| En la visión | Qué lo cumple aquí |
|---|---|
| **Dato** = valor que queda, recuperable | cada fila de `inscripciones` lleva `respaldo` (oración + fragmento literal), `condiciones` y `radicacion` |
| **La unidad temática** da el contexto que el dato suelto pierde | `unidades` (subtema, oraciones, texto) y `leer_unidad` |
| **Información = cambio en A(Q)** | no se almacena: la calcula el código por consulta; el almacén no contiene respuestas ni tablas de A(Q) |
| **K = lo que efectivamente entró**, en las rutas | no es una tabla; cada entrada queda en `traza.jsonl` (aquí, solo el mundo del código con su versión) |
| **Bitemporalidad** | `radicacion` (cuándo entró) frente a la fecha propia del documento (tiempo de validez) |
| **Dependencias y promoción** | el derivado guardaría su bloque `derivacion` con valores y procedencia, y la promoción queda diferida: **en esta versión no hay derivados** |
| **No fusión de casos** | ids calificados; la correspondencia se acredita con la declaración documental y se registra, no se persiste |
| **Revisión que conserva** | el almacén se regenera; la traza (y los derivados, cuando los haya) es append-only y no se sobrescribe |

### 3.4. Lo que **no** se construye (la lista del elefante)

- **Ningún gestor de base de datos** para 5 unidades: JSON/JSONL en memoria.
- **Ni RDF, ni SPARQL, ni ontología, ni razonador.** «Ship minimal schema, expand
  on demand» ([guía de grafos](https://www.dataaihub.co/learn/knowledge-graphs)).
- **Ni resolución de entidades global**, ni `SAME_AS`, ni cola de revisión de
  fusiones.
- **Ni tablas de A(Q), ni respuestas, ni conflictos almacenados.** Se calculan y
  se registran.
- **Ni motor temporal**: dos columnas de fecha.
- **Ni búsqueda vectorial ni embeddings** (el plan ya la difiere).
- **Ni motor de grafos** para 9 relaciones: son filas.

### 3.5. Cuándo cambiaría

Dos disparadores, y ninguno antes de que ocurran: (a) el corpus no entra en
memoria o los cruces se vuelven consultas reales → el mismo esquema lógico en
SQLite, sin cambiar la API de la tool; (b) una pregunta exige caminos de varios
saltos → entonces se discute un grafo. Mientras tanto, cualquier sofisticación es
deuda.

---

## 4. Entradas: el usuario y las reglas

Dos cosas, y no se mezclan: **las preguntas** (el usuario) y **R** (lo que el
agente lee y el orquestador aplica).

### 4.1. Archivo de preguntas (es el usuario)

`mvp/consulta/preguntas.md`: **solo el texto de las cinco preguntas, limpias** —sin
condiciones, sin expectativas, sin pistas—. Es lo único que aporta el usuario,
junto con el dominio elegido. Las cinco están en §12.

### 4.2. Documento R

`mvp/consulta/R.md` es **un documento, no un programa**: se fija antes de empezar
cada prueba y puede cambiar entre pruebas; con cada corrida queda registrado cuál
estuvo vigente. Tiene dos partes que dicen lo mismo: un esbozo que el código lee
para **aplicar R** y la prosa que **lee el agente**, porque el orquestador se la
pasa en el prompt. Si se separan, manda el esbozo y se corrige la prosa.

```json
{ "fuentes_admitidas": ["solo el documento"],
  "herramientas": ["leer_unidad", "calcular", "entregar"],
  "operaciones": ["sumar", "restar", "dias_entre", "dia_siguiente", "parsear_fecha"] }
```

Es un **esbozo**, no un contrato cerrado: lo que importa es que las condiciones
queden escritas y que el código pueda aplicarlas sin interpretarlas. **Los topes
de turnos y de llamadas no son R**: son guardias del orquestador (§11).

Prosa para el agente (las condiciones de la consulta): sin internet; sin otras
herramientas ni agentes; el saber del agente no es premisa; no hay interacción con
el usuario; la aritmética y las fechas las hace el código; solo se entrega si hubo
efecto; los conflictos se muestran y no se eligen; «no establecido» y «no
cerrable» se entregan explícitos, con la brecha.

**R se aplica ofreciendo.** El agente la recibe en el prompt, y el orquestador la
aplica al armar cada llamada: **cruza R con el inventario y solo le ofrece lo que
cumple ambas cosas** (la visión ya lo dice así). Si una herramienta está
restringida, **no se le da**: no hay nada que denegar. Solo en el camino (A) de §7
—donde el agente puede nombrar cualquier acción en su JSON— el orquestador responde
con la regla que la excluye, sin ejecutarla. En los dos casos queda en la traza, y
si insiste, corta la guardia de ciclo.

**K se deduce de R.** Precisión: R fija **qué clases de premisa pueden entrar**;
con esta R, la única K admitida es el **mundo del código**, que se registra con su
versión. Estrictamente, K es lo que efectivamente entró y queda en las rutas; lo
que se deduce de R es qué K puede entrar. El **dominio** es entrada aparte de R
(no es un modo de R). Las **anclas** (fecha del sistema) no son premisa con esta
R: si se inyectan, se declaran y no abren puerta al mundo.

---

## 5. El recorrido

| # | Subpaso | Quién | Qué pasa | Termina cuando |
|---|---|---|---|---|
| 1 | Incorporar las extracciones | código | carga documento, dominio, unidades, fichas, referencias y respaldos; asigna ids; registra el esquema | un dato resuelve a su oración y dos unidades no comparten ids |
| 2 | Abrir la consulta | código | recibe pregunta, dominio y R; **resuelve el dominio a sus documentos** (pertenencia de la tabla, sin juicio); anclas; abre el expediente y **arma el prompt de cada interacción** | la corrida anota dominio, R y documentos admitidos |
| 3 | Encuadrar y consultar | código + agente | el orquestador le da el inventario del dominio y el estado; el agente pide leer unidades; el código entrega la lectura completa | las unidades leídas quedan registradas como **examinadas** |
| 4 | Proponer la respuesta | agente | con los datos leídos **del corpus**, propone encabezado, tabla inicial y final, campo, conflicto, brechas y respuesta | la propuesta llega en el formato de entrega |
| 5 | Comprobar y entregar | código | verifica forma, alcance por dominio, admisión por R, encabezado y cálculos; calcula el efecto; entrega y registra | hay respuesta con respaldo o falta explícita, con el recorrido |

**Estaciones del plan que se usan:** E0, E1, E2, E5, E6. **No** E3 (Jev) ni E4
(mundo).

---

## 6. La memoria es del orquestador (el agente es stateless)

El agente **no recuerda nada entre llamadas**: cada llamada es una interacción
nueva y solo sabe lo que va en el prompt. Lo que no se le ponga, no lo puede
saber. El orquestador lleva el estado y compone cada prompt; la traza es ese
estado.

**El agente es una función pura:** `agente(prompt) -> acción`. El estado va y
vuelve por el orquestador (el patrón «stateless reducer», factor 12 de
[12-Factor Agents](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md)),
y el prompt se arma a mano desde archivos, sin esconderlo en un framework
(factor 2, «own your prompts»).

**Qué lleva cada llamada** (bloques fijos + estado + cola):

| Bloque | Contenido | Cambia entre turnos |
|---|---|---|
| Instrucciones | rol, tarea, protocolo, formato de entrega, prohibiciones | no |
| R | el documento R (§4.2), tal como lo lee el agente | no |
| Pregunta | texto limpio y dominio elegido | no |
| Inventario | unidades del dominio: id, subtema, oraciones | no dentro de la consulta |
| Estado | encabezado propuesto, unidades leídas (ids), campo, brechas, desenlace en curso | sí |
| Cola | las últimas acciones del agente y sus resultados | sí |

Con **herramientas nativas** (§7), esa «cola» es el array `messages` real
(`assistant` con `tool_calls` → `role: "tool"` con `tool_call_id`), y con `tools`
en la petición hay que devolver además el `reasoning_content` intermedio en todos
los turnos siguientes.

**Cómo se mantiene liviano** (context engineering: el menor conjunto de tokens de
alta señal, [Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)):

- **Just in time:** no se manda el corpus; se mandan **ids** y el agente pide lo
  que necesita. El inventario es liviano; la lectura completa llega cuando la pide.
- **Divulgación progresiva:** inventario → unidad elegida → datos de la unidad.
- **Compactación:** los resultados viejos se reemplazan por su referencia (los
  ids) y un resumen; el texto completo **no se borra nunca**: queda en la traza y
  se puede volver a pedir. Las últimas acciones se conservan enteras. La guía de
  compresión coincide: descargar antes de resumir, y lo descargado tiene que
  seguir siendo recuperable ([context compression](https://www.agentpatterns.ai/context-engineering/context-compression-strategies/)).
- **Errores compactos:** una denegación de R o un JSON inválido vuelven como un
  mensaje corto con la regla y la forma esperada (factor 9).
- **El estado manda:** lo que se compactó y hace falta se vuelve a pedir; el
  orquestador no adivina lo que el agente necesita.

**Guardias del bucle:** máximo de turnos por pregunta, corte por ciclo (misma
acción y argumentos dos veces), tope de llamadas; al agotarse, desenlace
«agotada». Cada llamada y cada resultado van a la traza.

---

## 7. Las herramientas: nativas o simuladas

**Lo que hay hoy en el repo.** `call_model`
([run_niveles.py:110](../niveles/run_niveles.py#L110)) manda **un solo mensaje
`user`** —`messages: [{"role": "user", "content": content}]`—, no manda `tools` y,
al ensamblar el stream, **solo concatena `delta.content` y
`delta.reasoning_content`: los `tool_calls` se pierden**. Es además el único sitio
que arma la petición y pone la clave.

**Lo que la API sí soporta** (api-docs.deepseek.com): `tools` con funciones y
`tool_choice` (`none | auto | required | una función`), **conversación multi-turno
real** (`assistant` con `tool_calls` → mensaje `role: "tool"` con `tool_call_id`),
`delta.tool_calls` en streaming y **herramientas en modo razonamiento** (desde
V3.2). Dos trampas: con `tools` en la petición, el `reasoning_content` intermedio
**tiene que volver en todos los turnos siguientes** o la API responde 400
([thinking mode](https://api-docs.deepseek.com/guides/thinking_mode/)); y con
thinking encendido algunos `tool_choice` forzados dan error
([tool calls](https://api-docs.deepseek.com/guides/tool_calls/)). El modo `strict`
—endpoint `beta`— valida los argumentos contra el JSON schema
([function calling](https://api-docs.deepseek.com/guides/function_calling)).

**Entonces hay dos caminos, no una obligación:**

| | (A) Protocolo textual | (B) Herramientas nativas |
|---|---|---|
| Qué cambia | nada: `call_model` tal cual | extender `call_model` de forma **aditiva**: `messages` opcional, `tools` opcional, acumular `tool_calls` en la respuesta |
| Cómo vuelve el agente | un objeto JSON con `accion`, que el código parsea | `tool_calls` estructurados |
| Coste por turno | el historial se re-serializa como texto | el historial es el array `messages` nativo |
| Riesgo | el parseo del JSON; el formato ocupa prompt | tocar la capa compartida; devolver `reasoning_content`; `tool_choice` + thinking |
| Cuándo | respaldo, si no se quiere tocar `call_model` | **elegido (D13)**: es el camino estándar y no inventa protocolo |

**El canal de vuelta es JSON, siempre.** El agente contesta con `tool_calls` o con
el objeto de `entregar`; no hay rama de «responder en texto». Una respuesta que no
sea JSON, o un `entregar` que no verifique, es un **error de formato**: se registra
como error y **no se interpreta** —el orquestador no lee prosa—; se permite **una**
vuelta indicando el formato esperado y, si reincide, se corta con el error
registrado.

**R se aplica al ofrecer.** Con (B), la lista de `tools` de cada llamada es
**R ∩ inventario**: lo restringido **no se da**, así que el agente no puede
pedirlo y la denegación deja de ser un caso normal. Queda como guardia solo en el
camino (A), donde el agente puede nombrar cualquier acción en su JSON:

```json
{"ok": false, "error": "R no admite fuentes externas", "regla_r": "fuentes_admitidas"}
```

La denegación queda en la traza y insistir corta por ciclo.

**Quién arma las herramientas.** Las escribe **el orquestador, en código**, no el
agente: cada una es una función con nombre, descripción y esquema JSON
(`mvp/consulta/herramientas.py`), y el agente solo produce los argumentos. Son la
**única puerta al corpus de §3**: el agente nunca ve el almacén; `leer_unidad` le
devuelve la unidad con sus inscripciones —datos con condiciones y respaldo, capas,
relaciones, referencias y dudas— y su procedencia. La descripción de cada
herramienta es contrato: es lo que el agente lee para decidir.

- **El dominio va cerrado por el código, no por argumento.** `leer_unidad(id)` no
  acepta `dominio`: el orquestador lo cierra sobre los documentos admitidos y
  valida cada id contra ellos. El agente no puede ampliar el alcance cambiando un
  argumento.
- **Por llamada, el orquestador decide qué se ofrece:** (1) qué herramientas van
  en `tools` (= R ∩ inventario), (2) el `tool_choice` y (3) qué entra en el prompt
  (inventario, estado). Todo lo demás es fijo.
- **El inventario va en el prompt, no en una herramienta** (en la MVP): son cinco
  unidades con id, subtema y oraciones; tenerlo delante hace visible la selección
  (§8) y ahorra un turno. Cuando el dominio crezca, entra
  `buscar_unidades(consulta)` con el contrato del plan y el inventario se pide.
- **Tres herramientas y no una con `metodo`:** cada una con su esquema, su
  descripción (qué hace, cuándo usarla, qué devuelve) y su validación; así la
  lista ofrecida es también la aplicación de R.
- **La ejecución es del código:** valida los argumentos contra el esquema (con
  `strict` si hace falta), comprueba la pertenencia al dominio, ejecuta, recorta la
  respuesta a lo necesario y la devuelve como mensaje `role: "tool"`, anotando todo
  en la traza.
- **Manda el inventario del sistema:** se ofrece lo que cumple R **y** existe; si
  el sistema no tiene la herramienta, no se ofrece aunque R la admita.

**Reglas comunes** (valen para A y B): lista blanca de herramientas —las del
diseño—; `calcular` con **tabla fija** de funciones, nunca `eval`; ids validados
contra los documentos admitidos; toda salida del agente en JSON, y `entregar` en el
esquema de `pieza1`; y las guardias de §11.

**Lo que no cambia con ninguna:** la memoria sigue siendo del orquestador (§6) y
el agente sigue siendo stateless; el dominio lo inyecta el código; R se aplica y
se comunica.

---

## 8. El prompt del agente (secciones)

**Pendiente de revisión (07-10):** esta sección y el §9 son lo que sigue; los prompts de
la extracción ya están fijados (§3).

Cómo se reparten estas secciones entre el system y los mensajes, con qué etiquetas
y cómo se ve la petición en la API: §9.

1. **Rol y tarea.** Qué se le pide: interpretar la pregunta, leer, proponer.
2. **Qué recibe, en cada llamada.** Los bloques de §6 —instrucciones, R,
   pregunta y dominio, inventario, estado y cola—. Nada más: **lo que no va en el
   prompt, el agente no lo sabe.**
3. **Herramientas.** Las tres —`leer_unidad`, `calcular`, `entregar`—, con su
   descripción y su esquema de argumentos; con nativas (§7B) van en `tools`, y con
   el protocolo textual (§7A) son tres acciones, una por turno. El inventario ya
   viene en el prompt; `buscar_unidades` entra cuando el dominio crezca.
4. **R y K.** Solo el documento; el cálculo lo hace el código; su propio saber no
   es premisa.
5. **SELECCIÓN** (regla propuesta, todavía no escrita en ninguna parte). Propuesta:
   - ve el inventario (id, subtema, oraciones) y pide leer las unidades que puedan
     tocar el aspecto, la identidad del caso o sus condiciones; mejor sobreleer;
   - **campo** = determinaciones cuyo caso es el de la pregunta (o uno que haga
     falta para identificar, comparar o condicionar), cuyo aspecto es el aspecto
     o una condición pedida, y cuyas condiciones no chocan con las de la pregunta;
   - lo demás queda **mudo** y no es sostén; el código registra examinado ≠ campo.
6. **INFERENCIA** (tampoco escrita). Propuesta:
   - tabla inicial: `resto` admisible;
   - un dato del campo con condiciones compatibles establece su posición con ruta
     al dato, y vuelve inadmisibles las incompatibles; una regla genérica solo
     añade sostén;
   - una capa la afirma el texto como atribución: lo de dentro sostiene con la
     capa en la ruta;
   - identidad: sin declaración del documento, la posición no se atribuye;
   - conflicto: dos posiciones admisibles bajo las mismas condiciones
     constitutivas, con fuentes que chocan; se muestra, no se elige;
   - sin cierre: `no establecido` si nada del campo mueve la tabla; `no cerrable`
     si falta un dato concreto, con la brecha nombrada.
7. **Formato de entrega.** Objeto estricto del esquema 2 (`encabezado`,
   `dependencias`, `tablas_esperadas`, `tabla_inicial`, `tabla_final`, `campo`,
   `conflicto`, `desenlace`, `respuesta`, `brechas`). **Sin `dato_derivado`** en esta
   versión.
   Restricción de `pieza1`: `dependencias` es exactamente lo que aparece en las
   rutas, y `campo` solo datos. **Toda salida es JSON**: `tool_calls` o el objeto
   de entrega; el texto libre no se lee.
8. **Prohibiciones.** No inventar identidades ni valores; no elegir en un
   conflicto; no calcular por su cuenta; no salir del dominio; no responder fuera
   del JSON pedido.

---

## 9. El system prompt y la petición real (boilerplate)

Cómo se arma el system y cómo se ve la petición en la API. El JSON es
**boilerplate verificado** contra la referencia
([Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/)),
no una especificación nuestra.

### 9.1. Qué va en el system y qué en los mensajes

Lo que **no cambia entre turnos** va al system; lo que cambia, a los mensajes.

| En el **system** (fijo durante toda la consulta) | En los **mensajes** |
|---|---|
| ROL · **TAREA** · ALCANCE (dominio, documentos admitidos, inventario) · R · HERRAMIENTAS (cuándo usar cada una) · SELECCIÓN · INFERENCIA · FORMATO · **ANCLAS (día y hora)** · un ejemplo inventado | la **pregunta** (turno `user`) y el bucle `assistant`/`tool` (lecturas, cálculos, estado) |

El **esquema** de las herramientas viaja en el campo `tools` del mismo request: el
agente lo lee como lee el system. En el texto del system van solo las reglas de
uso; el esquema no se repite ahí (gastaría tokens y se desincronizaría).

### 9.2. La estructura del system, en bloques etiquetados

```
ROL          quién es y para qué
TAREA        la tarea: qué tiene que producir, en una frase
ALCANCE      dominio, documentos admitidos, inventario de unidades
R            fuentes admitidas, prohibiciones, reglas de entrega
HERRAMIENTAS qué hace cada una y cuándo usarla (el esquema va en tools)
SELECCIÓN    qué leer y qué cuenta como campo
INFERENCIA   cómo se pasa de los datos a la tabla y al desenlace
FORMATO      el JSON de entrega (esquema del objeto)
ANCLAS       día y hora del sistema
EJEMPLO      uno, inventado (nunca de los documentos de prueba)
```

Reglas de armado, de la investigación de esta ronda:

- **Lo estable primero.** El system va delante y no se toca entre turnos: el caché
  de DeepSeek es por **prefijo desde el token 0** y cambiar el system lo reinicia
  ([Context Caching](https://api-docs.deepseek.com/guides/kv_cache)).
- **Etiquetas, no prosa.** Bloques etiquetados se malinterpretan menos y se
  versionan mejor ([Anthropic](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices),
  [llmbestpractices](https://llmbestpractices.com/ai-agents/system-prompts)).
- **Restricciones verificables.** «No salgas del dominio; si el dato no está,
  entrega *no establecido*» rinde más que «sé cuidadoso»; sin «DEBES» ni
  mayúsculas, que sobreactúan, y sin instrucciones que se contradigan
  ([llmbestpractices](https://llmbestpractices.com/ai-agents/system-prompts)).
- **Sin duplicar el esquema de las herramientas** en el texto
  ([ai-agent-course](https://github.com/kshvakov/ai-agent-course/blob/main/book/02-prompt-engineering/README.md)).
- **El ejemplo, al final y de forma**: enseña exactamente lo que muestra.

### 9.3. Las anclas: día y hora

Van en el bloque `ANCLAS`, con la fecha y la hora del sistema tomadas en el
arranque de la consulta: **congeladas** para toda la consulta (no cambian entre
turnos, no rompen el prefijo del caché) y **registradas en la traza**. Con R
«solo el documento» el ancla **no es premisa**: el propio prompt lo dice, para que
no se use como dato del documento.

### 9.4. La petición, en la API real

```json
{
  "model": "deepseek-flash",
  "messages": [
    {"role": "system", "content": "ROL …\nTAREA …\nALCANCE …\nR …\nHERRAMIENTAS …\nSELECCIÓN …\nINFERENCIA …\nFORMATO …\nANCLAS …\nEJEMPLO …"},
    {"role": "user", "content": "¿Cuánto tardó la ciudad en restablecer el servicio del tranvía tras el incendio de 1927?"}
  ],
  "tools": [
    {"type": "function",
     "function": {
       "name": "leer_unidad",
       "description": "Devuelve una unidad del dominio con su texto, sus datos (con condiciones y respaldo), sus referencias y sus dudas.",
       "parameters": {
         "type": "object",
         "properties": {"id": {"type": "string", "description": "id de la unidad, p. ej. doc5:U2"}},
         "required": ["id"]
       }}}
  ],
  "tool_choice": "auto",
  "thinking": {"type": "enabled"},
  "reasoning_effort": "high",
  "stream": true,
  "stream_options": {"include_usage": true}
}
```

El bucle, con los mensajes que se agregan (formas de la referencia y del
[guide de tool calls](https://api-docs.deepseek.com/guides/tool_calls/)):

```json
{"role": "assistant", "content": null, "reasoning_content": "…",
 "tool_calls": [{"id": "call_…", "type": "function",
                 "function": {"name": "leer_unidad", "arguments": "{\"id\": \"doc5:U2\"}"}}]}

{"role": "tool", "tool_call_id": "call_…", "content": "{…la lectura…}"}
```

Y el cierre, con la herramienta de entrega:

```json
{"role": "assistant", "content": null,
 "tool_calls": [{"id": "call_…", "type": "function",
                 "function": {"name": "entregar", "arguments": "{…el objeto…}"}}]}
```

Datos exactos que hay que respetar (misma fuente):

- **`model`**: `deepseek-flash` o `deepseek-v4-pro`.
- **`messages`** (≥1): roles `system`, `user`, `assistant`, `tool`. El `assistant`
  puede llevar `content`, `reasoning_content` y `tool_calls`; el mensaje `tool`
  lleva `tool_call_id` y `content`.
- **`function.arguments` es un *string*** con JSON: hay que parsearlo y validarlo
  antes de ejecutar (la referencia avisa que el modelo puede inventar parámetros).
- **`tools[]`**: `type: "function"` y `function{name, description, parameters,
  strict}`. El nombre, hasta 128 caracteres de `a-zA-Z0-9_-`; si se omite
  `parameters`, la función no recibe argumentos; `strict` es Beta y valida el JSON
  schema.
- **`tool_choice`**: `none` (por defecto sin `tools`), `auto` (por defecto con
  `tools`), `required` o una función nombrada. **`required` y la nombrada no se
  admiten en modo razonamiento: la API devuelve 400.**
- **`thinking`**: `{"type": "enabled" | "disabled"}`, por defecto `enabled`.
  **`reasoning_effort`**: `none | low | high | max`, por defecto `high`
  (`minimal`→`low`, `medium`/`xhigh`→`high`).
- **`max_tokens`**: 1–393216; por defecto 8K sin razonamiento y 64K con
  razonamiento (128K con `max`).
- **`response_format`**: `{"type": "text" | "json_object"}`; `json_object`
  garantiza JSON válido, pero **hay que pedirlo también en el prompt**.
- **`temperature`** no tiene efecto en modo razonamiento; **`top_p`** solo actúa
  ahí y se recorta a 0.95–1.0. `frequency_penalty` y `presence_penalty` están
  retirados.
- **Lo que leemos de la respuesta**: `finish_reason` (`stop`, `length`,
  `content_filter`, `tool_calls`, `insufficient_system_resource`, `aborted`),
  `message.content` (puede venir `null`), `message.reasoning_content` y
  `message.tool_calls[]`.
- **El consumo**: `usage.prompt_tokens` = `prompt_cache_hit_tokens` +
  `prompt_cache_miss_tokens` (también en `prompt_tokens_details.cached_tokens`), y
  `completion_tokens_details.reasoning_tokens`. Con eso se mide el acierto de
  caché del §11.

---

## 10. Salidas

- **`mvp/consulta/salida.md`** (el usuario lee esto): por pregunta, la respuesta
  en lenguaje natural con su ruta en palabras (documento y oración), el desenlace
  y, cuando no se puede establecer, qué falta. Anexo por pregunta con la tabla de
  A(Q) (inicial y final) y el campo.
- **`mvp/consulta/traza.jsonl`**: expediente del recorrido (dominio, documentos
  admitidos, unidades examinadas, acciones de la tool, campo, ruta, efecto,
  desenlace, llamadas y consumo).
- **Nada de datos derivados en esta versión:** el agente solo mira el corpus, así
  que no se usa `corpus.jsonl` ni el camino de `guardar`/`mantener`. Cuando el
  corpus no alcance para cerrar la pregunta, el desenlace se entrega explícito
  («no establecido» o «no cerrable»), sin inventar el dato que falta.

---

## 11. Guardias y presupuesto (se fijan antes de llamar)

Las guardias **no son R**: R dice qué se puede usar; esto solo corta si el bucle se
enreda.

- **Modelo:** `deepseek-flash` (alias `deepseek`), el del paso 2; esfuerzo `low`
  (que DeepSeek trata como `high`).
- **De a una:** se manda una pregunta y la siguiente se manda cuando el agente
  entrega su JSON con la respuesta (o cuando una guardia corta la corrida).
- **Llamadas:** el inventario va en el prompt, así que lectura en lote 1 +
  cálculo ≤2 (en estas cinco no hace falta) + entrega 1 + reparación 1 ⇒ **≤5 por
  pregunta**; **tope 20** para las cinco, con parada y desenlace «agotada».
- **Ciclo:** misma acción con los mismos argumentos dos veces → se corta.
- **Salida inválida:** respuesta que no sea JSON, o `entregar` que no verifique →
  **error de formato**; se registra y se permite **una** vuelta de reparación con
  la forma esperada; si reincide, se corta. Nunca se interpreta el texto.
- **Estimación:** 3–12 k tokens de entrada por llamada (el historial crece) y
  3–12 k de salida (≈91 % razonamiento, medido); total aproximado **40–90 k de
  entrada y 50–120 k de salida**. El importe se calcula con la tarifa publicada
  de DeepSeek el día de la corrida y se registra; **no se estima a ojo**.
- **El prompt no se muestra antes de correr:** se guarda con la corrida y se
  muestra cuando Frat lo pida.

---

## 12. Las cinco preguntas (texto limpio, es el archivo del usuario)

`mvp/consulta/preguntas.md` contiene **solo esto**:

1. ¿En qué año empezó a rodar el primer tranvía de la ciudad y qué compañía lo operaba?
2. ¿Cuánto tardó la ciudad en restablecer el servicio del tranvía tras el incendio de 1927?
3. ¿Cuántos kilómetros de vías llegó a tener la red, y según qué?
4. ¿Cuánto costó la compra de la red en 1948?
5. ¿Quién encontró el plano de 1911, la historiadora o la archivista?

Ni condiciones ni expectativas: las condiciones van en el documento R (§4.2). El
agente ve la pregunta tal cual. Las cinco se responden con **lo que el corpus
establece**: ninguna exige calcular ni traer nada de fuera, y se mandan de a una
(§11).

---

## 13. Cómo se evalúa

Se juzga **lo que la corrida entrega y su respaldo**, leyendo el documento:

- la respuesta se sostiene en lo que el documento establece, con la ruta a la
  oración (documento, unidad, dato);
- lo que no se puede establecer se dice con precisión: qué falta, por qué y qué
  quedó abierto;
- **no cuenta** acertar por casualidad ni citar texto que no sostiene la respuesta;
- se respetaron las condiciones de R y, si hay conflicto, se muestra sin elegir;
- las unidades **examinadas** quedan registradas, y se distinguen del campo;
- **no interviene Jev**: el juicio es nuestro y se registra.

Comprobaciones mecánicas aparte: 0 errores del verificador de forma, pertenencia
por dominio, admisión por R, efecto calculado.

---

## 14. Riesgos y límites

- La calidad de la extracción acota la respuesta (es el hallazgo del paso 2, no
  un defecto del puente).
- La partición de `U4`/`U5` corta `[12,13,17]` y `[14,15,16]`: la identidad
  «la historiadora que revisó» vs «Elvira Sanmiguel» cruza unidades y **no está
  declarada**: el agente tiene que dejarla abierta.
- El **texto de la respuesta no se verifica**: el código valida rutas y forma;
  que diga solo lo que la tabla establece lo juzgamos nosotros.
- **El prompt es el único canal.** Si el orquestador omite un dato o no le avisa
  de lo que ya hizo, el agente no lo puede saber: repetirá lecturas o propondrá
  sobre material que no vio. La memoria es responsabilidad del código.
- **La compactación puede perder señal.** Si se resume de más, se cae un matiz que
  solo se nota después; por eso lo descargado se conserva recuperable y se empieza
  por máxima retención ([guía de contexto](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- **El historial crece por turno**: de ahí el tope y el corte por ciclo.
- **Con herramientas nativas (§7B), devolver el `reasoning_content`**: si no vuelve
  en todos los turnos con `tools`, la API responde 400; y algunos `tool_choice`
  forzados chocan con el modo razonamiento.
- Un solo documento ⇒ sin conflicto (ver D2).

---

## 15. Decisiones

| # | Decisión | Estado |
|---|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO | **decidida**; coherencia de los documentos vivos, §17 |
| **D2** | Corpus: solo `doc5`, o `doc5` + la mesa de dominio para tener conflicto | por definir — recomendación: solo `doc5` |
| **D3** | Bucle de la consulta: lectura en lote por turnos, o todo inyectado en una llamada | por definir — recomendación: bucle con lectura en lote |
| **D4** | P2 con derivado (1929) o sin él («dos años») | **decidida: sin derivado**; la pregunta se responde con lo que el corpus establece |
| **D5** | R: `solo el documento`, con el mundo del código para fechas y aritmética, y las anclas fuera como premisa | por definir — recomendación: sí |
| **D6** | Nombre y sitio de los archivos (`mvp/consulta/`) | por definir — confirmar antes de crear código |
| **D7** | Almacén: tres artefactos JSON/JSONL con `datos` como vista | recomendación: la configuración mínima (§3); normalizar solo ante un cuello de botella medido |
| **D8** | Derivados en `corpus.jsonl` | **fuera de esta versión:** el agente solo mira el corpus; `guardar` y `mantener` quedan sin uso |
| **D9** | Idioma de los `tipo` (`determinación` o `determination`) | por definir — recomendación: español |
| **D10** | Documento R: esbozo para el código + prosa para el agente; se fija por prueba | recomendación: sí (§4.2); **los topes no van en R** |
| **D11** | Compactación: cuántas acciones enteras se conservan y qué se resume | por definir — recomendación: las últimas 5, el resto por referencia + resumen |
| **D12** | El mundo del LLM: pasa a llamarse «mundo del agente» en los documentos vivos; en el esquema candidato de la pieza 1 sigue rotulado `orquestador` | recomendación: renombrar en los vivos y declarar la divergencia en `pieza1/esquema2.md` hasta adoptarlo |
| **D13** | Herramientas: (A) protocolo textual sobre `call_model` tal cual, o (B) extender `call_model` con `messages` + `tools` nativos | **decidida: (B)**, aditivo. Con (B), R se aplica **no dando** la herramienta: la lista de `tools` de cada llamada es R ∩ inventario, y la denegación por mensaje queda solo como guardia (§7) |
| **D14** | Prompts de la extracción: paso 1 `mvp/pruebas/prompt_v10.md` (agrupa por asunto, sin referencias) y paso 2 `mvp/pruebas/prompt_datos_v1.md` | **decidida (07-10):** son las versiones de trabajo; no se siguen afinando |
| **D15** | Salida del paso 2: `caso`, `datos` (`aspecto · valor · unidad_valor`) y `dudas`, **una unidad por turno** | **decidida (07-10).** Quedan fuera `sostiene`, `inferido`, `respaldo`, `cambio`, `condiciones` y las listas de la ficha (relación, acción, capa, marca). Pendiente: si vuelven el sostén (quién sostiene el dato) y el respaldo (la ruta al fragmento) |
| **D16** | `unidad_valor`: campo propio o la unidad dentro del `valor` | por definir — el campo se usa poco (3 de 26 datos en `doc4`; 2 de 14 en `doc5`) |

---

## 16. Qué se reutiliza

- `mvp/pieza1/pieza1.py`: `verificar` y `comparar` (y hay que ampliarlo con el
  **efecto** y con la **admisión por dominio**, que hoy no tiene). `guardar` y
  `mantener` quedan sin uso mientras no haya datos derivados.
- `unidades/ficha_doc.py`: `verificar` y `fragmentos` para el respaldo literal.
- `unidades/extraer_unidades.py`: `numerar_oraciones`.
- `niveles/run_niveles.py`: `call_model` (a extender de forma aditiva si se elige
  §7B, herramientas nativas) y `extract_json`.
- `mvp/paso2/comparacion.py`: la re-verificación offline de crudos.
- Las extracciones cerradas del paso 2 (fichas por unidad con referencias,
  respaldos y dudas).

---

## 17. Vocabulario (D1)

Los tres documentos vivos usan esta convención:

- **orquestador** = el código: resuelve, aplica, ejecuta, comprueba, calcula y
  registra. No piensa.
- **agente encargado** = el LLM: interpreta, selecciona y propone. Stateless.
- **mundo del agente** = su saber general y sus convenciones de lectura, que
  antes se llamaba «mundo del orquestador».

Dónde vive: [zettel-vision-operativa.md](../zettel-vision-operativa.md) define los
dos nombres en «Notación y vocabulario» y renombra el mundo;
[definiciones-del-marco.md](../definiciones-del-marco.md) parte B tiene las dos
filas y la parte C dice «mundo del agente»; [orquestador-plan.md](../historico/orquestador-plan.md)
renombra el componente en §0–§2, sus estaciones y el prompt. El archivo sigue
llamándose `orquestador-plan.md`: es el plan del que conduce.

**Divergencia declarada:** [pieza1/esquema2.md](pieza1/esquema2.md) sigue
rotulando `mundo: orquestador` en su lista de R, por compatibilidad con la pieza 1
en prueba; se renombra al adoptar el esquema. Por un cambio de etiqueta no se
tocan `pieza1.py` ni sus tablas de referencia.

---

## 18. Fuentes consultadas

- *Nanopublication Guidelines* — aserción + procedencia + info de publicación en
  una unidad pequeña y autocontenida: <https://nanopub.net/guidelines/working_draft/>
- *A Unified Nanopublication Model…* (arXiv 2006.06348) — el mismo modelo en un
  conjunto real: <https://arxiv.org/html/2006.06348v1>
- *Evidence Model* (esquema con evidencias) — reificar solo si el hecho está en
  disputa, acotado o reemplazado: <https://cdn.jsdelivr.net/npm/@a5c-ai/atlas@5.0.1-staging.f17326334/graph/schema/evidence-model.md>
- `cs0lar/knk` — log de aserciones bitemporal, append-only, y optimización atada
  a un cuello de botella medido: <https://github.com/cs0lar/knk>
- *Flat files vs SQLite* (foro de SQLite) — cuándo cada formato falla:
  <https://sqlite.org/forum/forumpost/c43b208884?t=h>
- Hilo «Flat JSON files vs SQLite for agent state» — elegir por forma de acceso,
  no un formato para todo: <https://github.com/kody-w/rappterbook/discussions/3742>
- *Entity Resolution: The Hardest Part of Any Knowledge Graph* — fusiones no
  destructivas y por qué la resolución global es el elefante:
  <https://archtin.com/blog/entity-resolution-in-knowledge-graphs>
- *Knowledge Graphs · Complete Guide* — «over-engineering the ontology» como
  antipatrón; esquema mínimo y crecer a demanda:
  <https://www.dataaihub.co/learn/knowledge-graphs>
- *12-Factor Agents* — factor 2 «own your prompts», factor 3 «own your context
  window», factor 9 «compact errors», factor 12 «stateless reducer»:
  <https://github.com/humanlayer/12-factor-agents> y
  <https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md>
- *Effective context engineering for AI agents* (Anthropic) — el menor conjunto de
  tokens de alta señal; just-in-time, divulgación progresiva, compactación:
  <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
- *Building effective agents* (Anthropic) — el bucle «LLM + herramientas +
  retroalimentación del entorno», con condiciones de parada y buenos contratos de
  herramienta: <https://www.anthropic.com/engineering/building-effective-agents>
- *Context compression strategies* — descargar antes de resumir; lo descargado
  tiene que seguir siendo recuperable; conservar objetivo, estado y siguiente paso:
  <https://www.agentpatterns.ai/context-engineering/context-compression-strategies/>
- *DeepSeek · Tool Calls* — herramientas en modo razonamiento desde V3.2:
  <https://api-docs.deepseek.com/guides/tool_calls/>
- *DeepSeek · Function Calling* — `tools`, `tool_choice` y modo `strict` (beta)
  que valida los argumentos contra el JSON schema:
  <https://api-docs.deepseek.com/guides/function_calling>
- *DeepSeek · Thinking Mode* — con `tools`, el `reasoning_content` intermedio
  tiene que volver en todos los turnos siguientes (si no, 400):
  <https://api-docs.deepseek.com/guides/thinking_mode/>
- *DeepSeek · Chat Completions* — `tools`, `tool_choice` y `finish_reason:
  tool_calls`: <https://api-docs.deepseek.com/api/create-chat-completion/>
