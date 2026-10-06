# Consulta completa de Zettel (v1) · diseño para afinar

Fecha: 06-10-2026. **Estado: borrador de diseño; nada implementado.** Este
documento es la superficie de trabajo: se afina aquí antes de escribir código y
antes de llamar a un modelo.

**Para qué.** Construir el **primer recorrido completo** de Zettel sobre el
corpus: recibir una pregunta y entregar una respuesta respaldada, un conflicto o
una explicación precisa de lo que no se puede establecer, con el recorrido
registrado.

**Qué se considera terminado.** Una ejecución acotada de ese recorrido, sobre un
dominio y unas preguntas fijadas antes, evaluada contra lo que se dejó escrito:
si la respuesta es fiel y está justificada, y si lo que no se puede establecer se
dice con precisión.

**Base.** [orquestador-plan.md](orquestador-plan.md) §3 (estaciones) y §11 (F0,
F1); el contrato de [mesa-dominio-plan.md](mesa-dominio-plan.md) §9 y su cierre;
la extracción cerrada del paso 2 ([paso2/informe_paso2.md](paso2/informe_paso2.md)).
**Se mantienen congelados el paso 1 (v9) y el paso 2** (candidato provisional:
no se reabre ni se adopta). Sin Jev y sin búsqueda externa.

---

## 1. Reparto de papeles

En esta versión, **el código es el ORQUESTADOR y el LLM es el AGENTE ENCARGADO**.
Es la separación «control/contenido» del plan, con los nombres cambiados: el
código conduce, admite, ejecuta, verifica, calcula y registra; el agente
interpreta, selecciona y propone.

| | Código (orquestador) | Agente encargado (LLM) |
|---|---|---|
| Prepara | configuración, dominio, documentos admitidos, anclas | — |
| Entrega | inventario y lectura de unidades por la tool | — |
| Hace | ejecuta las acciones de la tool, calcula fechas y aritmética, verifica, registra | — |
| Decide | qué material está admitido; cuándo se cierra | qué unidades leer; qué datos son campo; qué sostiene una respuesta |
| **Memoria** | lleva el estado y arma el prompt de cada llamada | **ninguna**: es stateless, solo sabe lo que va en el prompt |
| Propone | — | encabezado, tablas, brechas, respuesta, derivado |
| Juzga | no juzga contenido | no ejecuta acciones ni calcula por su cuenta |

**D1 (decidida).** **Código = ORQUESTADOR, LLM = AGENTE ENCARGADO.** El agente es
**stateless**: cada llamada es una interacción nueva y solo sabe lo que va en el
prompt; el orquestador es quien lleva la memoria y compone cada prompt (§6). La
coherencia de esta etiqueta con los documentos vivos está en §16.

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
| `unidades.jsonl` | log de líneas | una fila por unidad: `id`, documento, dominio, `subtema`, `oraciones`, `texto` numerado, **`referencias`** y **`dudas`** (JSON) |
| `inscripciones.jsonl` | log de líneas | una fila por **lo que el documento establece**: `tipo` (determinación · relación · acción · capa · marca · duda), columnas comunes (`id`, `unidad`, `condiciones`, `respaldo`, `inferido`, `dentro_de`) y `cuerpo` JSON por tipo |
| `traza.jsonl` | log append-only | el recorrido de cada consulta; **no es corpus** |
| `corpus.jsonl` | log append-only | los datos derivados, en la forma de [pieza1/esquema2.md](pieza1/esquema2.md) §5 |

La tabla **`datos`** que ve el agente es una **vista** sobre `inscripciones`
(`tipo = "determinación"`). Así se conservan tus dos tablas —unidades y datos—
sin siete tablas, y sin perder capas, relaciones, casos ni dudas: `leer_unidad`
devuelve la unidad con sus inscripciones agrupadas por tipo.

**Identificadores.** `documento` (`doc5`) · `unidad` (`doc5:U1`) · `caso`
(`doc5:U1:C1`) · `dato` (`doc5:U1:D1`) · `oración` (`doc5:S2`) · derivado
(`DD1`, global). Los ids locales de cada ficha **nunca** se comparan entre
unidades; dos menciones son el mismo caso solo por declaración del documento o
criterio explícito. Sin fusión.

**El corpus es un derivado regenerable.** `documentos`, `unidades` e
`inscripciones` se **generan** con un cargador idempotente a partir de los
documentos, la partición de v9 y las fichas del paso 2 (con el hash del esquema);
si cambia el cargador, se regeneran. Lo único append-only es `traza.jsonl` y
`corpus.jsonl`. Esto evita migraciones, copias de seguridad y versionado de la
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
| **Dependencias y promoción** | el derivado guarda su bloque `derivacion` con valores y procedencia; la promoción queda diferida hasta que otra pregunta lo reutilice |
| **No fusión de casos** | ids calificados; la correspondencia se acredita con la declaración documental y se registra, no se persiste |
| **Revisión que conserva** | el almacén se regenera; la traza y los derivados son append-only y no se sobrescriben |

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

Son tres cosas distintas, y no se mezclan: **las preguntas** (el usuario), **R**
(lo que el agente lee y el orquestador hace valer) y **las expectativas** (nuestras,
para evaluar).

### 4.1. Archivo de preguntas (es el usuario)

`mvp/consulta/preguntas.md`: **solo el texto de las cinco preguntas, limpias** —sin
condiciones, sin expectativas, sin pistas—. Es lo único que aporta el usuario,
junto con el dominio elegido. Las cinco están en §11.

### 4.2. Documento R

`mvp/consulta/R.md`: un documento con dos partes que dicen lo mismo. La primera,
un bloque que el código lee para **hacer valer** R; la segunda, la prosa que **lee
el agente**, porque el orquestador se la pasa en el prompt. Si se separan, manda
el bloque y se corrige la prosa.

```json
{ "fuentes_admitidas": "solo el documento",
  "k_admitida": ["mundo/codigo"],
  "herramientas": ["listar_unidades", "leer_unidad", "calcular", "entregar"],
  "calcular": ["sumar", "restar", "dias_entre", "dia_siguiente", "parsear_fecha"],
  "prohibido": ["internet", "otros_agentes", "mundo_del_agente", "usuario"],
  "limites": { "turnos_por_pregunta": 6, "llamadas_totales": 20 } }
```

Prosa para el agente (las condiciones de la consulta): sin internet; sin otras
herramientas ni agentes; el saber del agente no es premisa; no hay interacción
con el usuario; la aritmética y las fechas las hace el código; solo se entrega si
hubo efecto; los conflictos se muestran y no se eligen; «no establecido» y «no
cerrable» se entregan explícitos, con la brecha.

**R la hace valer el orquestador.** El agente la recibe en el prompt, y además el
código la aplica: si pide una herramienta, una función o una fuente que R no
admite, el orquestador **no la ejecuta y se lo comunica por el protocolo** (§7),
citando la regla que la excluye, para que el agente busque otra vía. Cada
denegación queda en la traza; si insiste, corta la guardia de ciclo.

**K se deduce de R.** Precisión: R fija **qué clases de premisa pueden entrar**;
con esta R, la única K admitida es el **mundo del código**, que se registra con su
versión. Estrictamente, K es lo que efectivamente entró y queda en las rutas; lo
que se deduce de R es qué K puede entrar. El **dominio** es entrada aparte de R
(no es un modo de R). Las **anclas** (fecha del sistema) no son premisa con esta
R: si se inyectan, se declaran y no abren puerta al mundo.

### 4.3. Expectativas preinscritas (nuestras, no del agente)

Antes de correr escribimos en `mvp/consulta/evaluacion.md`, por pregunta, **qué
establece el documento, qué lo sostiene, qué no autoriza y qué cambio en A(Q) se
espera** (§12). **No se le pasa al agente**: si las viera, dejaría de medir su
inferencia.

---

## 5. El recorrido

| # | Subpaso | Quién | Qué pasa | Termina cuando |
|---|---|---|---|---|
| 1 | Incorporar las extracciones | código | carga documento, dominio, unidades, fichas, referencias y respaldos; asigna ids; registra el esquema | un dato resuelve a su oración y dos unidades no comparten ids |
| 2 | Abrir la consulta | código | recibe pregunta, dominio y R; fija documentos admitidos; anclas; abre el expediente y **arma el prompt de cada interacción** | la corrida anota dominio, R y documentos admitidos |
| 3 | Encuadrar y consultar | código + agente | el orquestador le da el inventario del dominio y el estado; el agente pide leer unidades; el código entrega la lectura completa | las unidades leídas quedan registradas como **examinadas** |
| 4 | Proponer la respuesta | agente | con los datos leídos, propone encabezado, tabla inicial y final, campo, conflicto, brechas, respuesta y derivado; pide los cálculos al código | la propuesta llega en el formato de entrega |
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

## 7. Protocolo de comunicación (la tool)

`call_model` **no soporta `tools` ni multi-turno**: manda un solo mensaje `user`
([run_niveles.py:110](../niveles/run_niveles.py#L110)). El protocolo es
**textual y simulado por el código**: en cada turno el agente responde con **un
único objeto JSON con una acción**; el código la ejecuta, acumula el resultado y
vuelve a llamar con el historial serializado en ese mensaje.

```json
{"accion": "listar_unidades"}
{"accion": "leer_unidad", "ids": ["doc5:U1", "doc5:U2"]}
{"accion": "calcular", "funcion": "sumar", "args": [1927, 2]}
{"accion": "entregar", "propuesta": { … esquema 2 … }}
```

Reglas:

- **Lista blanca**; cualquier otra acción devuelve error y consume turno.
- **R se hace valer aquí.** Si la acción pide algo que R no admite —una función
  fuera de la lista, una fuente externa, otro agente—, el orquestador **no la
  ejecuta** y contesta con la regla que la excluye, para que el agente busque otra
  vía:
  ```json
  {"ok": false, "error": "R no admite fuentes externas", "regla_r": "fuentes_admitidas"}
  ```
  La denegación queda en la traza; insistir corta por ciclo.
- **`calcular` no es `eval`**: tabla fija de funciones (`sumar`, `restar`,
  `dia_siguiente`, `dias_entre`, `parsear_fecha`, …). El código no ejecuta nada
  que el agente escriba.
- **El dominio lo inyecta el código**: no hay acción para ampliarlo; todo id
  fuera de los documentos admitidos se rechaza.
- **Guardias:** máximo de turnos por pregunta, corte por ciclo (misma acción y
  argumentos dos veces), tope total de llamadas; al agotarse, desenlace
  «agotada».
- **`entregar`** trae la propuesta en el esquema de `pieza1`; si no verifica, se
  permite **una** vuelta de reparación.

---

## 8. El prompt del agente (secciones)

1. **Rol y tarea.** Qué se le pide: interpretar la pregunta, leer, proponer.
2. **Qué recibe, en cada llamada.** Los bloques de §6 —instrucciones, R,
   pregunta y dominio, inventario, estado y cola—. Nada más: **lo que no va en el
   prompt, el agente no lo sabe.**
3. **Protocolo.** Las cuatro acciones, con ejemplos; una acción por turno.
4. **R y K.** Solo el documento; el cálculo lo hace el código; su propio saber no
   es premisa.
5. **SELECCIÓN** (hoy sin escribir en ninguna parte). Propuesta:
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
   `conflicto`, `desenlace`, `respuesta`, `brechas`, `dato_derivado` si lo hay).
   Restricción de `pieza1`: `dependencias` es exactamente lo que aparece en las
   rutas, y `campo` solo datos.
8. **Prohibiciones.** No inventar identidades ni valores; no elegir en un
   conflicto; no calcular por su cuenta; no salir del dominio.

---

## 9. Salidas

- **`mvp/consulta/salida.md`** (el usuario lee esto): por pregunta, la respuesta
  en lenguaje natural con su ruta en palabras (documento y oración), el desenlace
  y, cuando no se puede establecer, qué falta. Anexo por pregunta con la tabla de
  A(Q) (inicial y final) y el campo.
- **`mvp/consulta/traza.jsonl`**: expediente del recorrido (dominio, documentos
  admitidos, unidades examinadas, acciones de la tool, campo, ruta, efecto,
  desenlace, llamadas y consumo).
- **`corpus.jsonl`** (el de `pieza1.guardar`): el dato derivado, si lo hay.

---

## 10. Guardias y presupuesto (se fijan antes de llamar)

- **Modelo:** `deepseek-flash` (alias `deepseek`), el del paso 2; esfuerzo `low`
  (que DeepSeek trata como `high`).
- **Llamadas:** inventario 1 + lectura en lote 1 + cálculo ≤2 + entrega 1 +
  reparación 1 ⇒ **≤6 por pregunta**; **tope 20** para las cinco, con parada y
  desenlace «agotada».
- **Estimación:** 3–12 k tokens de entrada por llamada (el historial crece) y
  3–12 k de salida (≈91 % razonamiento, medido); total aproximado **40–90 k de
  entrada y 50–120 k de salida**. El importe se calcula con la tarifa publicada
  de DeepSeek el día de la corrida y se registra; **no se estima a ojo**.
- El prompt se muestra antes de correr.

---

## 11. Las cinco preguntas (texto limpio, es el archivo del usuario)

`mvp/consulta/preguntas.md` contiene **solo esto**:

1. ¿En qué año empezó a rodar el primer tranvía de la ciudad y qué compañía lo operaba?
2. ¿En qué año se restableció el servicio del tranvía tras el incendio de 1927?
3. ¿Cuántos kilómetros de vías llegó a tener la red, y según qué?
4. ¿Cuánto costó la compra de la red en 1948?
5. ¿Quién encontró el plano de 1911, la historiadora o la archivista?

Ni condiciones ni expectativas: las condiciones van en el documento R (§4.2) y las
expectativas son nuestras, para evaluar (§12). El agente ve la pregunta tal cual.

---

## 12. Cómo se evalúa

**Expectativas preinscritas** (`mvp/consulta/evaluacion.md`, escritas antes de
correr; **no se le pasan al agente**):

| # | Desenlace esperado | Qué debe sostenerlo | Qué no autoriza |
|---|---|---|---|
| P1 | cerrada | 1893 y la compañía inglesa con capital privado, con respaldo `[1]`–`[2]` | el nombre de la compañía (no está) ni que fuera la única operadora |
| P2 | cerrada con **derivado** | 1927 y «dos años» de `U2`; el cálculo (1929) lo hace el código y el derivado se guarda | fechas que el documento no da |
| P3 | cerrada con **capa** | veintiocho kilómetros, con la atribución «según los planos» en la ruta | afirmarlo como voz del documento; la longitud actual |
| P4 | **no establecido** | campo vacío; **inventario examinado** de las cinco unidades | inventar un precio o traerlo de fuera |
| P5 | **no cerrable** | las dos lecturas abiertas de `U5` («Ella» = historiadora o archivista) | elegir una; declarar que son distintas |

Criterios:

- **Contra lo escrito antes**, no contra lo que salga: respuesta, sostén, límites y
  cambio en A(Q).
- **No cuenta** acertar por casualidad ni citar texto que no sostiene.
- Las cerradas se juzgan por su ruta y su fidelidad; las no cerradas, por la
  precisión de lo que no se puede establecer y por el inventario examinado.
- **No interviene Jev**: el juicio es nuestro y se registra.
- Comprobaciones mecánicas aparte: 0 errores del verificador de forma, alcance por
  dominio, admisión por R, efecto calculado.

---

## 13. Riesgos y límites

- La calidad de la extracción acota la respuesta (es el hallazgo del paso 2, no
  un defecto del puente).
- La partición de `U4`/`U5` corta `[12,13,17]` y `[14,15,16]`: la identidad
  «la historiadora que revisó» vs «Elvira Sanmiguel» cruza unidades y **no está
  declarada**; por eso P5 va por la duda explícita y no por esa identidad.
- El **texto de la respuesta no se verifica**: el código valida rutas y forma;
  que diga solo lo que la tabla establece lo juzgamos nosotros.
- **El prompt es el único canal.** Si el orquestador omite un dato o no le avisa
  de lo que ya hizo, el agente no lo puede saber: repetirá lecturas o propondrá
  sobre material que no vio. La memoria es responsabilidad del código.
- **La compactación puede perder señal.** Si se resume de más, se cae un matiz que
  solo se nota después; por eso lo descargado se conserva recuperable y se empieza
  por máxima retención ([guía de contexto](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)).
- El historial crece por turno: de ahí el tope y el corte por ciclo.
- Un solo documento ⇒ sin conflicto (ver D2).

---

## 14. Decisiones

| # | Decisión | Estado |
|---|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO | **decidida**; coherencia de los documentos vivos, §16 |
| **D2** | Corpus: solo `doc5`, o `doc5` + la mesa de dominio para tener conflicto | por definir — recomendación: solo `doc5` |
| **D3** | Protocolo: bucle con lectura en lote, o todo inyectado en una llamada | por definir — recomendación: bucle con lectura en lote |
| **D4** | P2 con derivado (1929) o sin él («dos años») | por definir — recomendación: con derivado |
| **D5** | R: `solo el documento`, mundo del código registrado, anclas fuera como premisa | por definir — recomendación: sí |
| **D6** | Nombre y sitio de los archivos (`mvp/consulta/`) | por definir — confirmar antes de crear código |
| **D7** | Almacén: tres artefactos JSON/JSONL con `datos` como vista | recomendación: la configuración mínima (§3); normalizar solo ante un cuello de botella medido |
| **D8** | Derivados: en `corpus.jsonl` (forma de pieza 1) o dentro de `inscripciones` | por definir — recomendación: `corpus.jsonl`, sin tocar `guardar`/`mantener` |
| **D9** | Idioma de los `tipo` (`determinación` o `determination`) | por definir — recomendación: español |
| **D10** | Documento R: bloque JSON para el código + prosa para el agente | recomendación: sí (§4.2) |
| **D11** | Compactación: cuántas acciones enteras se conservan y qué se resume | por definir — recomendación: las últimas 5, el resto por referencia + resumen |

---

## 15. Qué se reutiliza

- `mvp/pieza1/pieza1.py`: `verificar`, `comparar`, `guardar`, `mantener` (y hay
  que ampliarlo con el **efecto** y con la **admisión por dominio**, que hoy no
  tiene).
- `unidades/ficha_doc.py`: `verificar` y `fragmentos` para el respaldo literal.
- `unidades/extraer_unidades.py`: `numerar_oraciones`.
- `niveles/run_niveles.py`: `call_model` y `extract_json`.
- `mvp/paso2/comparacion.py`: la re-verificación offline de crudos.
- Las extracciones cerradas del paso 2 (fichas por unidad con referencias,
  respaldos y dudas).

---

## 16. Coherencia de vocabulario (D1)

Se hacen en el mismo tramo en que se escriba el código, no antes. Son
sustituciones de etiqueta, no de concepto: el papel se parte igual que en §1.

**[zettel-vision-operativa.md](../zettel-vision-operativa.md)** (documento vivo):

1. En «Notación y vocabulario», añadir dos entradas:
   **Orquestador (en la implementación)** = el código que conduce las estaciones,
   admite el material, ejecuta las herramientas, verifica, calcula y registra;
   **Agente encargado** = el LLM que interpreta la pregunta, selecciona y propone.
2. «un orquestador trae el mundo que la pregunta necesita» → «un agente,
   conducido por el código, trae el mundo que la pregunta necesita».
3. «El orquestador propone las filas; el código llena lo que es cómputo» →
   «El agente propone las filas; el código llena lo que es cómputo».
4. «El prompt del orquestador (04-10)» → «El prompt del agente encargado».
5. «El orquestador puede lanzar varias instancias de un LLM con funciones
   distintas» → «El código puede lanzar varias instancias del agente».
6. El paso 4 del ejemplo, titulado «El orquestador» → «El agente encargado
   (conducido por el código)».

**[definiciones-del-marco.md](../definiciones-del-marco.md)**, parte B (documento vivo):

7. La fila **Orquestador** pasa a **Orquestador (código)**: componente que
   conduce, ejecuta, comprueba y registra; no juzga contenido.
8. Añadir la fila **Agente encargado (LLM)**: interpreta la pregunta, selecciona
   unidades y datos y propone; es contenido, no control.
9. Ajustar «Relación con el marco» y «Origen» de las dos filas con la fecha.

**[orquestador-plan.md](orquestador-plan.md)** (plan candidato):

10. §1.2: «El orquestador propone; el código dispone» → «El agente propone; el
    orquestador (código) dispone».
11. §2: la fila «Código (plano de control)» pasa a **Orquestador (código)**; la
    fila «Orquestador» pasa a **Agente encargado**.
12. §3: en las estaciones, E1, E4 y E5 dicen «orquestador» → «agente».
13. §7: «El prompt del orquestador» → «El prompt del agente encargado».
14. Repasar las menciones sueltas de §10, §12 y §13.

El archivo sigue llamándose `orquestador-plan.md`: es el plan del que conduce.

---

## 17. Fuentes consultadas

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
