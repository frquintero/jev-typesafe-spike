# Consulta completa de Zettel (v1) · diseño para afinar

Fecha: 06-10-2026. **Estado: borrador de diseño; nada implementado.** Este
documento es la superficie de trabajo: se afina aquí antes de escribir código y
antes de llamar a un modelo. **Revisión tras la primera ronda de discusión**
(D1 cerrada; corpus reconfigurado, §3).

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
| Propone | — | encabezado, tablas, brechas, respuesta, derivado |
| Juzga | no juzga contenido | no ejecuta acciones ni calcula por su cuenta |

**D1 cerrada (Frat, 06-10).** Queda como está dicho: **código = ORQUESTADOR,
LLM = AGENTE ENCARGADO**. La coherencia con los documentos vivos se hace en el
mismo tramo en que se escriba el código; las ediciones exactas están en §15. El
encargo que originó este documento mezclaba los dos sentidos («pasa una a una al
orquestador (LLM)»); queda resuelto por D1.

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
mismo refugio y la misma noche), cuyos datos son a mano. **Decisión abierta D2.**

---

## 3. El corpus consultable: una configuración mínima

El encargo admitía «dos tablas»; tras revisarlo, la recomendación es **elegir por
forma de acceso** en vez de meter todo en un mismo molde. La discusión clásica en
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

### 4.1. Archivo de preguntas (es el usuario)

`mvp/consulta/preguntas.md` (o `.json`): 5 preguntas fijadas antes de correr,
con su texto y su expectativa escrita (qué establece el documento, qué la
sostiene, qué no autoriza, qué cambio en A(Q) se espera). Las cinco, en §10.

### 4.2. Archivo de R

`mvp/consulta/R.md`. Contenido propuesto:

```
fuentes admitidas: solo el documento
  - premisas admitidas: los datos de los documentos del dominio elegido
  - K admitida: solo el mundo del código (calendario, aritmética), con su versión
  - no admitidas: internet; otras tools o agentes; el saber del agente; el usuario
operaciones admitidas: aritmética y fechas por la biblioteca del código,
  cada una registrada (id, función, entradas, resultado)
entrega:
  - solo si la tabla final difiere de la inicial (hubo efecto)
  - los conflictos se muestran; no se elige
  - «no establecido» y «no cerrable» se entregan explícitos, con la brecha
guardias: máximo de turnos por pregunta; tope de llamadas; corte por ciclo
```

**K se deduce de R.** Precisión: R fija **qué clases de premisa pueden entrar**;
con esta R, la única K admitida es el **mundo del código**, que se registra con
su versión. Estrictamente, K es lo que efectivamente entró y queda en las rutas;
lo que se deduce de R es qué K puede entrar. El **dominio** es entrada aparte de
R (no es un modo de R). Las **anclas** (fecha del sistema) no son premisa con
esta R: si se inyectan, se declaran y no abren puerta al mundo.

---

## 5. El recorrido

| # | Subpaso | Quién | Qué pasa | Termina cuando |
|---|---|---|---|---|
| 1 | Incorporar las extracciones | código | carga documento, dominio, unidades, fichas, referencias y respaldos; asigna ids; registra el esquema | un dato resuelve a su oración y dos unidades no comparten ids |
| 2 | Abrir la consulta | código | recibe pregunta, dominio y R; fija documentos admitidos; anclas; abre el expediente | la corrida anota dominio, R y documentos admitidos |
| 3 | Encuadrar y consultar | código + agente | el agente interpreta la pregunta, ve el inventario del dominio y pide leer unidades; el código entrega la lectura completa | las unidades leídas quedan registradas como **examinadas** |
| 4 | Proponer la respuesta | agente | con los datos leídos, propone encabezado, tabla inicial y final, campo, conflicto, brechas, respuesta y derivado; pide los cálculos al código | la propuesta llega en el formato de entrega |
| 5 | Comprobar y entregar | código | verifica forma, alcance por dominio, admisión por R, encabezado y cálculos; calcula el efecto; entrega y registra | hay respuesta con respaldo o falta explícita, con el recorrido |

**Estaciones del plan que se usan:** E0, E1, E2, E5, E6. **No** E3 (Jev) ni E4
(mundo).

---

## 6. Protocolo de comunicación (la tool)

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

## 7. El prompt del agente (secciones)

1. **Rol y tarea.** Qué se le pide: interpretar la pregunta, leer, proponer.
2. **Qué recibe.** Pregunta, dominio, documentos admitidos, R, anclas, y la vía
   de la tool.
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

## 8. Salidas

- **`mvp/consulta/salida.md`** (el usuario lee esto): por pregunta, la respuesta
  en lenguaje natural con su ruta en palabras (documento y oración), el desenlace
  y, cuando no se puede establecer, qué falta. Anexo por pregunta con la tabla de
  A(Q) (inicial y final) y el campo.
- **`mvp/consulta/traza.jsonl`**: expediente del recorrido (dominio, documentos
  admitidos, unidades examinadas, acciones de la tool, campo, ruta, efecto,
  desenlace, llamadas y consumo).
- **`corpus.jsonl`** (el de `pieza1.guardar`): el dato derivado, si lo hay.

---

## 9. Guardias y presupuesto (se fijan antes de llamar)

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

## 10. Las cinco preguntas (fijadas antes de correr)

| # | Pregunta | Desenlace esperado | Qué prueba |
|---|---|---|---|
| P1 | ¿En qué año empezó a rodar el primer tranvía y qué compañía lo operaba? | cerrada | dos datos con respaldo `[1]`–`[2]` |
| P2 | ¿En qué año se restableció el servicio del tranvía tras el incendio de 1927? | cerrada con **derivado** | obliga a la tool de cálculo (1927 + 2 = 1929); estrena `guardar` y `mantener` |
| P3 | ¿Cuántos kilómetros de vías llegó a tener la red, y según qué? | cerrada con **capa** | el dato está atribuido («según los planos»): no autoriza afirmarlo como voz del documento |
| P4 | ¿Cuánto costó la compra de la red en 1948? | **no establecido** | campo vacío y **inventario examinado** de las 5 unidades |
| P5 | ¿Quién encontró el plano de 1911, la historiadora o la archivista? | **no cerrable** | dos lecturas abiertas (dudas de `U5`): conservarlas, no elegir |

Para cada una se deja escrito, antes de correr: qué establece el documento, qué
datos la sostienen (ids esperados), qué no autoriza a afirmar y qué cambio en
A(Q) se espera.

---

## 11. Cómo se evalúa

- **Contra lo escrito antes**, no contra lo que salga: respuesta, sostén,
  límites y cambio en A(Q).
- **No cuenta** acertar por casualidad ni citar texto que no sostiene.
- Se evalúan las cinco: las cerradas por su ruta y su fidelidad; las no cerradas
  por la precisión de lo que no se puede establecer y por el inventario
  examinado.
- **No interviene Jev**: el juicio es nuestro, y se registra en la evaluación.
- Comprobaciones mecánicas aparte: 0 errores del verificador de forma, alcance
  por dominio, admisión por R, efecto calculado.

---

## 12. Riesgos y límites

- La calidad de la extracción acota la respuesta (es el hallazgo del paso 2, no
  un defecto del puente).
- La partición de `U4`/`U5` corta `[12,13,17]` y `[14,15,16]`: la identidad
  «la historiadora que revisó» vs «Elvira Sanmiguel» cruza unidades y **no está
  declarada**; por eso P5 va por la duda explícita y no por esa identidad.
- El **texto de la respuesta no se verifica**: el código valida rutas y forma;
  que diga solo lo que la tabla establece lo juzgamos nosotros.
- El historial crece por turno: de ahí el tope y el corte por ciclo.
- Un solo documento ⇒ sin conflicto (ver D2).

---

## 13. Estado de las decisiones

| # | Decisión | Estado |
|---|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO | **cerrada (Frat, 06-10)**; coherencia pendiente, §15 |
| **D2** | Corpus: solo `doc5`, o `doc5` + la mesa de dominio para tener conflicto | abierta — recomendación: solo `doc5` en la primera pasada |
| **D3** | Protocolo: bucle con lectura en lote, o todo inyectado en una llamada | abierta — recomendación: bucle con lectura en lote |
| **D4** | P2 con derivado (1929) o sin él («dos años») | abierta — recomendación: con derivado |
| **D5** | R: `solo el documento`, mundo del código registrado, anclas fuera como premisa | abierta — recomendación: sí |
| **D6** | Nombre y sitio de los archivos (`mvp/consulta/`) | abierta — confirmar antes de crear código |
| **D7** | Almacén: tres artefactos JSON/JSONL con `datos` como vista, o tablas normalizadas de verdad | **recomendación nueva, §3**: la configuración mínima; normalizar solo si aparece un cuello de botella |
| **D8** | Derivados: en `corpus.jsonl` (forma de pieza 1) o dentro de `inscripciones` | abierta — recomendación: `corpus.jsonl`, para no tocar `guardar`/`mantener` |
| **D9** | Idioma de las inscripciones: `tipo` en español (`determinación`) o en inglés (`determination`) | abierta — recomendación: español, como el resto del repo |

---

## 14. Qué se reutiliza

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

## 15. Coherencia de vocabulario (D1) · ediciones pendientes

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

## 16. Fuentes consultadas (ronda 1)

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
