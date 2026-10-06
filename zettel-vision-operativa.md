# Zettel: cómo lo soñamos (visión operativa)

Fecha: 2026-10-04 (revisada el mismo día con Frat, y con las tensiones
discutidas con DeepSeek en `mvp/tensiones-vision-operativa-2026-10-04.md`).
Origen: discusión de Frat y Cowork. Este documento recuerda, con un ejemplo
completo, cómo debería funcionar Zettel de punta a punta. Es visión, no
especificación: el marco filosófico es lo único fijo (`marco filosófico/`,
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

**Notación.** El ensayo escribe la operación como A₀(Q) —D,R→ A₁(Q) (l. 283).
Zettel usa **A(Q | K, D; R)**: los subíndices se leen como elementos y no
como conjuntos, y la implementación necesita mostrar de dónde viene cada
cosa. Es la misma operación con otra escritura (registrada en
`definiciones-del-marco.md`, parte C).

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
  y sostén. No es monótono: pueden aparecer distinciones nuevas.
- **Brecha:** lo que falta para pasar de A(Q | K) a una respuesta.

**La tabla de A(Q).** A(Q) se representa, para que el efecto no sea un
autorreporte del modelo. Reglas probadas en la mesa 1 (`mvp/mesa1/`):

| posicion | si | estado | ruta |
|---|---|---|---|
| una posición, escrita en la escala que fija el aspecto | supuesto no establecido del que depende la fila | admisible o inadmisible | ids de lo que establece el estado |

- **Fila `resto`:** el dominio se escribe como regla, y una fila `resto`
  cubre lo no listado. Para el diff, una posición listada en una tabla
  tenía en la anterior el estado de `resto`.
- **`si`:** solo supuestos no establecidos («horario de verano», «la bodega
  está en el hemisferio norte»). Lo establecido va en `ruta`.
- **`estado`:** solo admisible o inadmisible. Verdadero, falso o
  indeterminado son predicados de la determinación, no de la posición
  (ensayo, l. 223). Una posición admisible sin ruta es «admisible, sin
  sostén», no un tercer estado.
- **`ruta`:** en una fila admisible es su sostén; en una inadmisible, su
  razón de exclusión. Todo saber del mundo que fija una posición está en la
  ruta como dependencia.
- **Excluir y sostener.** Solo una determinación incompatible, bajo las
  mismas condiciones constitutivas, vuelve inadmisible una posición (ensayo,
  l. 229). Una regla genérica («suele») solo añade sostén.
- **Por tabla:** `conflicto: [ids]` cuando dos fuentes chocan; `campo`: los
  datos considerados pertinentes (los mudos son el campo menos las rutas).
- **Ids:** D = dato del corpus; K = mundo (dato o regla); R = regla de la
  consulta.
- **Quién la escribe:** el orquestador propone las filas; el código llena
  lo que es cómputo (fechas, husos, aritmética).
- **El efecto informativo** es la diferencia entre la tabla de antes y la de
  después, calculada por el código, en cuatro clases: cambian de estado (en
  los dos sentidos); ganan o pierden sostén (fila admisible que cambia de
  ruta o entra en un conflicto); cambia la razón de exclusión (fila
  inadmisible que cambia de ruta); aparecen distinciones (filas nuevas o
  cambios en `si`). Si no hay cambios, no hubo efecto y el sistema lo dice.
- **Tres desenlaces** cuando la pregunta no se cierra: **no establecido**
  (nada mueve la tabla: «el documento no lo establece»); **no cerrable**
  (falta un dato que ni el corpus ni el mundo disponible dan; puede haber
  información parcial, como ramas con `si`); en los dos, el usuario es la
  fuente de último recurso.

**Los datos (D).** Los datos que se consideran: los del documento o los
derivados. Todos tienen el mismo estatus de dato.

**Fecha de radicación.** La fecha en que un dato entra a Zettel. La lleva
todo dato: el de un documento, la del día en que el documento se incorpora;
el derivado, la del día en que se guarda. Si el documento trae una fecha
propia, esa fecha es un **dato**, no la radicación (bitemporalidad: tiempo
de transacción y tiempo de validez).

**El mundo (K).** Entra como marco del caso y del aspecto: completa,
enmarca y trae escalas y reglas de inferencia.

- **Qué mundos hay:** el del **orquestador** (el único mundo LLM que cuenta
  como tal), el del **código** (aritmética, calendarios, zonas horarias) y
  el de las **fuentes consultadas** (APIs, web, Wikidata). Los demás LLM y
  Jev son **herramientas**: lo que devuelven entra como resultado de una
  herramienta, con su procedencia.
- **K es una procedencia, no otra clase de cosa.** Lo que llega de K es un
  dato, con procedencia «mundo». Si sostiene una respuesta, se registra como
  **dependencia** del dato derivado, con su valor.
- **Qué mundo entra:** el que R señale y esté disponible. Si R no dice
  nada, el orquestador usa los mundos suficientes y necesarios para
  enmarcar bien la pregunta.
- **K en operación (04-10).** K no se configura. Lo disponible es
  **inventario** del sistema (herramientas instaladas y sus claves), no una
  regla; el código lo conoce. La configuración de una consulta solo lleva R.
  El código cruza R con el inventario y le ofrece al orquestador solo lo que
  cumple ambas cosas. K es el mundo que **efectivamente entró**: lo que quedó
  en las rutas, con su procedencia.
- **Cuándo un mundo consultado es necesario:** si cierra algo que faltaba,
  si valida un dato o parte de él, o si abre una distinción pertinente.
- **Mundo como competencia y mundo como premisa.** Leer y calcular exigen
  mundo como **competencia**, que siempre está. Las restricciones regulan
  el mundo como **premisa**: un dato que entra a la respuesta.

**Las reglas de la consulta (R).** Las reglas con las que se manipula,
orquesta y funciona el corpus. Las fija el usuario, el documento o el
sistema. **Homónimo:** en el ensayo, R son las reglas presentes en sentido
amplio, incluidas las de inferencia; en Zettel, R son solo las de la
consulta, y las de inferencia viven en K. Entre ellas:

- **Fuentes admitidas como premisa:** «solo el documento» (ninguna premisa
  externa); «sin fuentes externas, con el mundo del orquestador»; libre (por
  defecto). En el modo «solo el documento», R dice también si Jev puede
  usarse.
- **Autorización de agentes:** por defecto, libertad para el orquestador.
- **Tope de costo o tiempo:** uno por defecto.
- **Anclas:** la hora del sistema, para «hoy» o «mañana» cuando nada más lo
  resuelve.

**El prompt del orquestador (04-10).** Lo arma el código con la entrada del
usuario y un archivo de configuración (en la MVP, solo el archivo): rol y
tarea; pregunta, corpus (fichas con ids) y R; herramientas ofrecidas (qué
hace cada una, cuándo usarla, cómo pedirla); salida y formato; reglas de la
tabla. El orquestador **pide** herramientas (*function calling*); el código
las ejecuta y anota procedencia y fecha de consulta, para que la ruta
registre lo que de verdad se consultó.

Estas reglas son de Zettel en marcha. En nuestro taller de desarrollo
siguen rigiendo las de `otros documentos/agentes-delegados.md` (copia en el repo
del original que vive en `~/Claude-memoria/memoria/`).

**El usuario.** Tiene su propio mundo, que decide si hubo efecto para él.
Es fuente de **último recurso**: si el orquestador no alcanza a dar el
marco, le pregunta.

**Sostén y juicio.** Dos cosas distintas que no se mezclan:

- **Sostén:** la ruta o rutas que sostienen una determinación (ensayo,
  A.7); su robustez depende de cuán independientes son (N(δ) = ⋂Cᵢ).
- **Juicio (de Jev):** el juicio que se le somete y su grado, con la banda
  y el modelo. Es el registro de un juicio concreto, no una propiedad del
  dato, y nunca se llama sostén. La banda sirve como **política de
  entrega**: elige el tono.

**Dependencias y promoción.** Cada dato derivado guarda sus dependencias:
identidad, valor, procedencia y fecha de consulta. Una dependencia se
**promueve** a dato del corpus solo si otra pregunta la reutiliza. Por clase
de premisa:

| clase | ejemplo | qué hacer |
|---|---|---|
| caduca de inmediato | estado de un vuelo hoy | no promover |
| estable | husos, calendarios | no guardar; citar la versión (p. ej., de tzdata) |
| volátil pero reutilizable | duración programada de una ruta | guardar con su fecha de consulta |

**Información y dato.**

- **Efecto informativo** (lo que recibe el usuario): la diferencia entre
  tablas, con su ruta. Ocurrió o no.
- **Contenido informativo** (lo que guarda el sistema): la determinación que
  queda sostenida. Es verdadera o falsa; registrada, es un **dato
  derivado**.

## El ejemplo completo

### 1. El documento

Una agencia de viajes envía un boletín. El usuario lo incorpora a Zettel el
2-10-2026 (fecha de radicación):

> Boletín del 24 de septiembre de 2026. El vuelo AV-569 despega a las 8:15 de
> El Dorado el lunes. Lleva 280 pasajeros.

### 2. Extracción de datos (al incorporar el documento)

- **Código:** numera las oraciones: [1], [2] y [3].
- **DeepSeek** (herramienta): unidades temáticas (`unidades_v5`) y ficha
  (`ficha_v1`).
- **Código:** verifica que cada respaldo sea literal.

```
D0 · boletín · fecha de emisión · 24-9-2026
     respaldo: [1] «Boletín del 24 de septiembre de 2026» · radicación: 2-10-2026
D1 · AV-569 · hora de despegue · 8:15 · condiciones: desde El Dorado, «el lunes»
     respaldo: [2] «despega a las 8:15 de El Dorado el lunes» · radicación: 2-10-2026
D2 · AV-569 · pasajeros · 280
     respaldo: [3] «Lleva 280 pasajeros» · radicación: 2-10-2026
```

### 3. La consulta

«¿A qué hora local llega el AV-569 a París?». R no dice nada: el
orquestador tiene libertad.

### 4. El orquestador

1. **Estructura la pregunta.** Caso de estudio: el vuelo AV-569. Aspecto:
   hora local de llegada. Condición: París. Dominio: x:yy, de 0:00 a 23:59.
2. **Escribe la tabla inicial.** Una fila: «resto · — · admisible · —».
   Es A(Q | K).
3. **Lee R** y **busca el campo:** D0, D1 y D2.
4. **Mide la brecha:** faltan la fecha de «el lunes», la duración, los husos
   y una validación del horario.
5. **Trae el mundo necesario (K).**
   - K3, mundo del orquestador: «el lunes» en un texto fechado es el
     próximo lunes desde su fecha. Con D0 (jueves 24-9), da el 28-9-2026.
   - K2, mundo del código (tzdata): Bogotá UTC−5; París UTC+2 el 28-9.
   - K1, una herramienta consulta la API de la aerolínea: el AV-569 del
     28-9 sale a las 8:15 (valida D1) y dura 10 h 35 min (valor
     ilustrativo), consultada el 4-10-2026.
6. **El código calcula:** 13:15 UTC + 10 h 35 min = 23:50 UTC = 1:50 en
   París. Y llena la tabla final:

| posicion | si | estado | ruta |
|---|---|---|---|
| 1:50 | duración normal | admisible | D0, D1, K1, K2, K3 |
| 0:50 | — | inadmisible | D0, K3, K2 (el 28-9 rige el horario de verano) |
| resto | — | inadmisible | D1, K1, K2 |

   `campo`: D0, D1, D2.
   El efecto (diferencia de tablas): de todo el dominio admisible a una
   sola posición. D2 no aparece en ninguna fila: quedó **mudo**.
7. **Lleva la respuesta a Jev:** juicio «el AV-569 llega a París hacia la
   1:50, hora local», con el expediente (los valores de la ruta, no solo sus
   ids). Supuesto: grado 0,88, banda «muy
   seguramente cierto».

El orquestador puede lanzar varias instancias de un LLM con funciones
distintas; no les pide «dime lo que sabes». Verifica de forma selectiva: lo
que sostiene la respuesta, o cuando la banda es baja, o cuando hay
conflicto. Cada tarea la orienta la brecha, no una búsqueda a ciegas.

### 5. Lo que recibe el usuario: información

Se entrega una respuesta solo si:

1. La tabla final difiere de la inicial (hubo efecto; lo calcula el código).
2. Se respetó R.
3. Los conflictos entre D y K se muestran: una contradicción es en sí
   información para el usuario.
4. La banda de Jev alcanza para formar juicio (política de entrega): por
   encima de 0,85 se afirma; entre 0,65 y 0,85, con cautela; por debajo de
   0,65 no se forma juicio y se explica qué falta.

> El AV-569 llega a París hacia la 1:50, hora local, en condiciones normales.
>
> Ruta: la salida es del boletín (oración 2), confirmada por la aerolínea.
> «El lunes» es el 28-9-2026, resuelto con la fecha del boletín (oración 1).
> La duración es de la aerolínea, consultada el 4-10-2026. La conversión de
> husos la hizo el código.

### 6. Lo que recibe el sistema: un dato derivado (parte de la MVP)

```
D3 · AV-569 · hora local de llegada · 1:50 · condiciones: París, 28-9-2026, duración normal
radicación: 4-10-2026 · inferido: sí
pregunta: Q («¿A qué hora local llega el AV-569 a París?»)
dependencias: D0 (boletín, fecha de emisión 24-9-2026, radicado 2-10)
              D1 (boletín, despegue 8:15, radicado 2-10)
              K1 (API de la aerolínea, duración 10 h 35, consultada 4-10)
              K2 (tzdata, versión usada por el código)
              K3 (mundo del orquestador: regla del lunes)
              R vigente (libre)
rutas: 1
juicio: noul · grado 0,88 · banda «muy seguramente cierto» · modelo jev-1.13.0
```

K1 es volátil pero reutilizable: queda como dependencia con su valor, y se
promueve a dato del corpus si otra pregunta la reutiliza.

**Mantenimiento de la verdad.** Si la aerolínea cambia la duración a
11 h 10, hay que volver a consultar para enterarse; lo que el registro gana
es que la comparación es mecánica (10 h 35 frente a 11 h 10) y dice qué se
cae: D3 pierde sostén y se revisa. Detectar el cambio sin consultar exigiría
suscribirse a la fuente (fuera de la MVP).

### Variantes

- **R = «solo el documento».** K1 no puede entrar como premisa. La tabla no
  cambia: no hay efecto, y la respuesta es «el documento no establece la
  hora de llegada; solo la de salida».
- **Boletín sin fecha propia.** Falta D0 y «el lunes» no se resuelve (la
  radicación no sirve). La tabla final muestra la distinción: 1:50 admisible
  con `si` «horario de verano», 0:50 admisible con `si` «horario de
  invierno». Es un desenlace no cerrable, con información parcial. Como último recurso, el orquestador pregunta: «¿de qué lunes se
  trata?».

