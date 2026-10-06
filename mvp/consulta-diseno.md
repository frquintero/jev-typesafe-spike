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
| Propone | — | encabezado, tablas, brechas, respuesta, derivado |
| Juzga | no juzga contenido | no ejecuta acciones ni calcula por su cuenta |

**Decisión abierta D1 (vocabulario).** El plan y los documentos vivos llaman
«orquestador» al LLM ([orquestador-plan.md](orquestador-plan.md) §2,
[zettel-vision-operativa.md](../zettel-vision-operativa.md),
[definiciones-del-marco.md](../definiciones-del-marco.md) parte B); este diseño
llama orquestador al código. En el encargo que originó este documento conviven
las dos cosas («el código toma el archivo de preguntas y pasa una a una al
orquestador (LLM)» y «el código es el ORQUESTADOR y el LLM es el AGENTE
ENCARGADO»). Opciones: (i) adoptar estos nombres y actualizar los tres
documentos vivos; (ii) dejar «orquestador» al LLM y llamar «conductor» al
código; (iii) registrar el homónimo en la parte C de las definiciones.
**Recomendación: (i)**, con el cambio de nombres hecho en el mismo tramo en que
se escriba el código, para que no haya dos sentidos vivos.

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

## 3. El corpus consultable: dos tablas

| Tabla | Columnas |
|---|---|
| **unidades** | `id` (`doc5:U1`), `documento`, `dominio`, `subtema`, `oraciones`, `texto` numerado, `radicacion`, `esquema`, `referencias` (JSON), `dudas` (JSON), `ficha` (JSON con capas, relaciones, acciones, marcas, casos) |
| **datos** | `id` (`doc5:U1:D1`), `unidad`, `caso`, `aspecto`, `valor`, `unidad_valor`, `condiciones` (JSON), `respaldo` (JSON), `inferido`, `dentro_de` (capa), `cambio` |

**Identificadores.** `documento` (`doc5`) · `unidad` (`doc5:U1`) · `caso`
(`doc5:U1:C1`) · `dato` (`doc5:U1:D1`) · `oración` (`doc5:S2`) · derivado
(`DD1`, global). Los ids locales de cada ficha **nunca** se comparan entre
unidades; dos menciones son el mismo caso solo por declaración del documento o
criterio explícito. Sin fusión.

**Formato en disco.** JSON/JSONL por documento (diffeable, reproducible), no
SQLite; el código lo carga en memoria. Capas, relaciones, casos y dudas viajan
en la columna `ficha`/columnas JSON y se exponen solo en `leer_unidad`: no hacen
falta como tablas propias para estas preguntas, pero sin ellas no se puede
responder «según», «atribuyó» ni conservar una duda.

**Módulo.** El cargador/registro vive en `mvp/consulta/` (nombre por confirmar);
es el subpaso 1 y no llama a ningún modelo.

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

## 13. Decisiones abiertas

| # | Decisión | Recomendación |
|---|---|---|
| **D1** | Nombres: código = orquestador y LLM = agente | adoptarlos y actualizar los tres documentos vivos en el mismo tramo |
| **D2** | Corpus: solo `doc5`, o `doc5` + la mesa de dominio para tener conflicto | solo `doc5` en la primera pasada; el conflicto, después |
| **D3** | Protocolo: bucle con lectura en lote, o todo inyectado en una llamada | bucle con lectura en lote (la selección queda visible) |
| **D4** | P2 con derivado (1929) o sin él («dos años») | con derivado: estrena `guardar`/`mantener` |
| **D5** | R: `solo el documento`, mundo del código registrado, anclas fuera como premisa | sí |
| **D6** | Nombre y sitio de los archivos (`mvp/consulta/`) | confirmarlo antes de crear código |

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
