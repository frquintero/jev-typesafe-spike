# Zettel: cómo lo soñamos (visión operativa)

Fecha: 2026-10-04 (revisada el mismo día con Frat). Origen: discusión de
Frat y Cowork. Este documento recuerda, con un ejemplo completo, cómo
debería funcionar Zettel de punta a punta. Es visión, no especificación: el
marco filosófico es lo único fijo (`marco filosófico/`,
`definiciones-del-marco.md`); todo lo demás se valida al andar. Al final se
separa lo probado de lo por probar.

## La idea en una frase

Lo que Zettel entrega es **información**: el cambio en el conjunto de
respuestas admisibles a una pregunta, cuando se consideran los datos del
corpus y del **mundo** conforme a unas reglas. El inventario de datos es
útil como inventario; lo útil de verdad sale de **pregunta + datos + mundo**.
Por eso la pregunta es el punto de partida, y un orquestador trae el mundo
que la pregunta necesita.

## Notación y vocabulario

**La pregunta.**

- **Q:** la pregunta. Se estructura en caso de estudio, aspecto, condiciones
  y **dominio** (las posiciones admisibles bajo el aspecto, en una escala;
  ensayo l. 133). El aspecto queda fijado; la respuesta será una posición
  del dominio.
- **A(Q | K):** las completaciones que **estarían** admisibles antes de
  declarar datos. Nunca hay un estado sin nada: es un límite construido para
  comparar.
- **A(Q | K, D; R):** las completaciones admisibles después de considerar D
  conforme a R, con el mundo K. Estructura: orden, equivalencia, distinción
  y sostén. No es monótono: pueden aparecer distinciones nuevas, así que no
  siempre está contenido en A(Q | K).

**Los datos (D).** Los datos del corpus que eligió el usuario (fichas
extraídas de sus documentos) y los datos derivados que Zettel ha ido
guardando. Todos tienen el mismo estatus de dato.

**Fecha de radicación.** La fecha en que un dato entra a Zettel. La lleva
todo dato: el de un documento, la del día en que el documento se incorpora;
el derivado, la del día en que se guarda. No tiene ambigüedad. Si el
documento trae una fecha propia («Boletín del 24 de septiembre»), esa fecha
es un **dato** del documento, no la radicación. Es la distinción
bitemporal: tiempo de transacción (radicación) y tiempo de validez (lo que
el dato dice del mundo).

**El mundo (K).** Entra como marco del caso y del aspecto: completa,
enmarca y trae escalas y reglas de inferencia.

- **Qué mundos hay:** el mundo del **orquestador** (el único mundo LLM que
  cuenta como tal), el del **código** (aritmética, calendarios, zonas
  horarias) y el de las **fuentes consultadas** (APIs, web, Wikidata). Los
  demás LLM y Jev son **herramientas**: lo que devuelven entra como
  resultado de una herramienta, con su procedencia, no como «su mundo».
- **Qué mundo entra:** el que R señale y esté disponible. Si R no dice
  nada, el orquestador usa los mundos que considere suficientes y
  necesarios para enmarcar bien la pregunta.
- **Cuándo un mundo consultado es necesario:** si cierra algo que faltaba,
  si valida un dato o parte de él, o si abre una distinción pertinente (el
  horario de verano no cierra ni valida: revela que la respuesta depende de
  la fecha).
- **Mundo como competencia y mundo como premisa.** Leer «despega» exige
  competencia del idioma; sumar horas exige aritmética. Ese mundo como
  **competencia** siempre está. Lo que las restricciones regulan es el
  mundo como **premisa**: un dato que entra a la respuesta.
- Todo lo que entra de K como premisa lleva su procedencia: quién lo
  sostiene, por qué herramienta llegó y cuándo se consultó.

**Las reglas de la consulta (R).** Las reglas con las que se manipula,
orquesta y funciona el corpus. Las fija el usuario, el documento o el
sistema. Entre ellas:

- **Fuentes admitidas como premisa:**
  - «solo el documento»: ninguna premisa externa;
  - «sin fuentes externas, con el mundo del orquestador»: premisas del
    orquestador, sin consultas;
  - libre (por defecto).
  En el modo «solo el documento», R dice también si Jev puede usarse.
- **Autorización de agentes:** por defecto, si R no dice nada, el
  orquestador tiene libertad para usar su mundo y sus herramientas.
- **Tope de costo o tiempo:** conviene que R traiga uno por defecto, porque
  la libertad con varias instancias y consultas puede salir cara.
- **Anclas:** la hora del sistema, para resolver «hoy» o «mañana» cuando
  nada más lo resuelve.

Estas reglas son de Zettel en marcha. En nuestro taller de desarrollo
siguen rigiendo las de `Claude-memoria/memoria/agentes-delegados.md`
(autorización previa de Frat, verificación de lo que reportan los agentes).

**El usuario.** Tiene su propio mundo, y ese mundo decide si hubo efecto: lo
que ya sabía no le informa. Es también fuente de **último recurso**: si el
orquestador no alcanza a dar el marco, le pregunta («¿de qué lunes se
trata?»).

**Información y dato.**

- **Efecto informativo** (lo que recibe el usuario): el paso de A(Q | K) a
  A(Q | K, D; R), con su ruta. Ocurrió o no.
- **Contenido informativo** (lo que guarda el sistema): la determinación que
  queda sostenida. Es verdadera o falsa; registrada, es un **dato
  derivado**.

## El ejemplo completo

### 1. El documento

Una agencia de viajes envía un boletín a sus clientes. El usuario lo
incorpora a Zettel el 2-10-2026 (fecha de radicación):

> Boletín del 24 de septiembre de 2026. El vuelo AV-569 despega a las 8:15 de
> El Dorado el lunes. Lleva 280 pasajeros.

### 2. Extracción de datos (al incorporar el documento)

- **Código:** parte el texto en oraciones y las numera: [1], [2] y [3].
- **DeepSeek** (barato, como herramienta): arma las unidades temáticas
  (`unidades_v5`) y reconstruye la ficha (`ficha_v1`), todo lo que el texto
  establece, por caso de estudio.
- **Código:** verifica que cada respaldo sea literal y esté en la oración
  citada.

Se almacena un registro por determinación, con la forma caso · aspecto ·
valor · condiciones · respaldo (la misma de Wikidata: elemento, propiedad,
valor, calificadores, referencias). Cada registro lleva la radicación:

```
D0 · boletín · fecha de emisión · 24-9-2026
     respaldo: [1] «Boletín del 24 de septiembre de 2026» · radicación: 2-10-2026
D1 · AV-569 · hora de despegue · 8:15 · condiciones: desde El Dorado, «el lunes»
     respaldo: [2] «despega a las 8:15 de El Dorado el lunes» · radicación: 2-10-2026
D2 · AV-569 · pasajeros · 280
     respaldo: [3] «Lleva 280 pasajeros» · radicación: 2-10-2026
```

Esto es inventario: datos, todavía no información.

### 3. La consulta

El usuario pregunta: «¿A qué hora local llega el AV-569 a París?». R no dice
nada sobre fuentes ni agentes: el orquestador tiene libertad.

### 4. El orquestador (un modelo inteligente)

1. **Estructura la pregunta.** Caso de estudio: el vuelo AV-569. Aspecto:
   hora local de llegada. Condición: París. Dominio: las posiciones x:yy, de
   0:00 a 23:59.
2. **Lee R.** Fuentes y agentes libres; tope por defecto.
3. **Busca el campo.** Recorre las unidades, encuentra «el vuelo AV-569» y
   trae D0, D1 y D2.
4. **Mide la brecha.** Para pasar del dominio entero a una respuesta faltan:
   la fecha concreta de «el lunes», la duración del vuelo, las zonas
   horarias y una validación del horario.
5. **Trae el mundo necesario (K).**
   - Su propio mundo: «el lunes» en un texto fechado es el próximo lunes
     desde su fecha. Con D0 (24-9-2026, jueves), da el 28-9-2026.
   - El mundo del código: zonas horarias (IANA). Bogotá UTC−5; París UTC+2
     ese día (horario de verano).
   - Una herramienta (una instancia de LLM o un script) consulta la API de
     la aerolínea: el AV-569 del 28-9 sale a las 8:15 (valida D1) y su
     duración programada es 10 h 35 min (valor ilustrativo), «consultada el
     4-10-2026».
6. **Hace calcular al código.** 8:15 en Bogotá = 13:15 UTC; 13:15 + 10 h 35
   min = 23:50 UTC; 23:50 UTC = 1:50 en París.
7. **Lleva la respuesta a Jev** (herramienta de juicio). Le presenta el
   expediente (D0, D1 y lo traído de K) y el juicio «el AV-569 llega a París
   hacia la 1:50, hora local». Supuesto: Jev devuelve 0,88 (muy seguramente
   cierto).

El orquestador puede lanzar varias instancias del mismo LLM, cada una con
una función (investigar un concepto, consultar una API, escribir un script,
ejecutarlo). No les pide «dime lo que sabes»: para eso está su propio
mundo. Tampoco verifica todo lo que le reportan, porque el proceso sería
largo y caro; verifica de forma selectiva lo que sostiene la respuesta (el
dato que cierra la brecha), o cuando Jev da una banda baja, o cuando hay
conflicto. Lo propio de Zettel frente a los agentes genéricos (ReAct,
orquestador-obreros) es que cada tarea la orienta la brecha en A(Q), no una
búsqueda a ciegas.

### 5. Lo que recibe el usuario: información

Se entrega una respuesta solo si:

1. A(Q | K, D; R) se movió respecto del dominio: hubo efecto.
2. Se respetó R.
3. Los conflictos entre D y K se muestran. Una contradicción es en sí
   información para el usuario: si la API dijera 8:40 y el boletín 8:15, se
   le dice.
4. La banda de Jev alcanza para formar juicio: por encima de 0,85 se afirma;
   entre 0,65 y 0,85 se dice con cautela («es probable que…»); por debajo de
   0,65 no se forma juicio y se explica qué falta. El grado no se muestra;
   guía el tono.

Aquí se cumplen:

> El AV-569 llega a París hacia la 1:50, hora local, en condiciones normales.
>
> Ruta: la salida es del boletín de la agencia (oración 2), confirmada por la
> aerolínea. «El lunes» es el 28-9-2026, resuelto con la fecha del boletín
> (oración 1). La duración es de la aerolínea, consultada el 4-10-2026. La
> conversión de zonas horarias la hizo el código.

D2 (280 pasajeros) quedó **mudo**: está en el documento, no en el campo de
la pregunta. El efecto fue el paso del dominio entero a una sola posición, y
ocurrió para este usuario.

### 6. Lo que recibe el sistema: un dato nuevo (parte de la MVP)

El dato derivado entra al corpus con el mismo estatus que cualquier otro.
Se guarda si la banda de Jev fue suficiente y R no lo prohíbe, con su
radicación (el día en que se guarda) y su traza:

```
AV-569 · hora local de llegada · 1:50 · condiciones: París, 28-9-2026, duración normal
radicación: 4-10-2026 · inferido: sí · sostén: 0,88
traza: pregunta Q; caso AV-569; aspecto hora local de llegada;
       D: D0, D1; K: mundo del orquestador (regla del lunes), código
       (zonas horarias IANA), API de la aerolínea del 4-10-2026; R vigente
```

Si cambia una dependencia (la aerolínea modifica la duración, el boletín se
corrige), el dato pierde sostén y se revisa: mantenimiento de la verdad
(Doyle, 1979; en el ensayo, atribución relacional, l. 293). La próxima
pregunta puede usarlo; la traza dice de dónde vino. El ecosistema crece
preguntando.

### Variantes

- **R = «solo el documento».** La duración del vuelo no puede entrar como
  premisa. A(Q | K, D; R) se queda en el dominio entero, y la respuesta es:
  «El documento no establece la hora de llegada; solo la de salida». Con el
  mismo documento y la misma pregunta, R decide si hay respuesta.
- **Boletín sin fecha propia.** Falta D0, y «el lunes» no se resuelve: la
  radicación no sirve, porque el boletín pudo entrar semanas después de
  escrito. La respuesta queda con la distinción abierta («hacia la 1:50 si
  es horario de verano; hacia las 0:50 si es invierno»), o, como último
  recurso, el orquestador le pregunta al usuario: «¿de qué lunes se trata?».

## Lo probado y lo por probar

- **Probado en el spike:** la etapa 2 (oraciones numeradas por código,
  unidades con `unidades_v5`, ficha con `ficha_v1`, verificación literal),
  pero solo en textos sintéticos cortos (unas 220 palabras); F6 sigue sin
  evaluar. Ver `memoria de trabajo y pendientes.md`.
- **Lo que separa de la MVP:** las etapas 4 (orquestador, brecha y tareas
  al mundo), 5 (condiciones de entrega) y 6 (guardar el dato derivado con
  su traza). Ninguna se ha probado.
