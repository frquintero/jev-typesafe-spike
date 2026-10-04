# Tensiones de la visión operativa — estado de la discusión

**Fecha:** 2026-10-04. **Origen:** conversación Frat–DeepSeek sobre
`zettel-vision-operativa.md`. **Para:** Opus, que lo lea y aporte su opinión.
**Estado:** borrador de trabajo, **no** documento vivo. Ningún documento vivo
se ha tocado.

**Cómo leerlo.** Cada tensión trae: lo que dice hoy la visión, el problema, lo
**acordado** y lo que queda **propuesto sin decidir**. Lo acordado son cuatro
cosas: el sentido de `D`, la formulación de la cadena de datos, la separación
de `sostén` y `juicio`, y el criterio de vocabulario con sus filas. El resto
es propuesta mía, sin veredicto.

---

## Tensión 1 — A(Q) no tiene representación

**Lo que dice la visión.** El paso 4, «Mide la brecha», y la condición de
entrega 1, «A(Q | K, D; R) se movió respecto del dominio» (:150-152, :181-183).

**El problema.** No existe ninguna estructura que diga qué respuestas eran
admisibles, cuáles dejaron de serlo y por qué regla. Lo único que hay es el
texto de la pregunta, los datos y la explicación que el orquestador escribe al
final. Consecuencias: (a) no se puede comprobar («hubo efecto» es una frase
del modelo); (b) no se puede auditar después, porque la «ruta» que recibe el
usuario es prosa; (c) no se puede medir cuánto cambió; (d) la cuenta se rehace
en tokens en cada pregunta, porque no está escrita en ninguna parte.

**Propuesta (sin decidir): una tabla mínima.** Tres columnas y tres estados
por respuesta:

| posición | estado | por qué |
|---|---|---|
| 1:50 | admisible, con sostén | 8:15 Bogotá = 13:15 UTC (código) + 10 h 35 (API) − husos |
| 0:50 | admisible, sin sostén | solo si el vuelo cae en horario de invierno |
| cualquier otra hora | inadmisible | fuera del dominio, o contradice un dato |

Los tres estados son los que el marco ya usa para cada determinación
(verdadera, falsa, indeterminada), un nivel más arriba: **admisible,
inadmisible, indecidible**. Comparar la tabla de antes con la de después **es**
el efecto informativo, y la comparación la puede hacer el código.

**Qué se gana.** La condición 1 pasa a ser una resta de tablas; si son
iguales, no hubo efecto y el sistema lo dice. La ruta sale de la columna «por
qué» en lugar de redactarse. Los conflictos D↔K y las distinciones nuevas se
ven como filas. El modelo rellena celdas en vez de razonar todo de nuevo, y el
código puede rellenar las que son cómputo (fechas, husos, aritmética).

**Qué no hace falta.** No hay que enumerar dominios sin fin: basta la regla
(«las horas 0:00–23:59», «sí/no», «los tres niveles»). El juicio difícil
—decidir qué falta, qué mundo traer— sigue siendo del orquestador.

**Decidir:** ¿A(Q) se representa, o se acepta por escrito que las condiciones
de entrega son auto-reporte del orquestador? Si se representa, ¿quién la
escribe y quién la comprueba?

---

## Tensión 2 — D y las premisas de K

**Acordado: qué es D.** En `A(Q | K, D; R)`, **D son los datos que se
consideran: los del documento y los derivados** (:35-37; el ejemplo usa D0, D1
y D2, que salen del boletín). Frat leyó la «D» como «derivados» al principio;
conviene que la línea lo blinde: «D: los datos que se consideran, del documento
o derivados».

**Acordado: la cadena.** `dato + datos intermedios = dato nuevo`. En el
ejemplo:

```
D1  (boletín, or. 2)       AV-569 · hora de despegue · 8:15          radicado 2-10
K1  (API, consultada 4-10)  AV-569 del 28-9 · duración · 10 h 35     ← dato intermedio
    + regla del lunes (mundo del orquestador)
    + husos IANA (mundo del código)
D3  (derivado, 4-10)        AV-569 · llegada local a París · 1:50    radicado 4-10
```

La duración **generalizada** de la ruta («Bogotá–París, ~10 h 35 en
condiciones normales») es otro dato intermedio, más valioso y de caducidad más
lenta que la del vuelo del 28-9.

**El problema.** La premisa que entra de K sostiene la respuesta y **no se
registra**: hoy solo queda como frase de la traza (:217: «API de la aerolínea
del 4-10-2026»), sin el valor. Y K no es una categoría aparte del dato: **es la
ruta por la que llegó un dato**; el dato es lo que vino.

**Cuatro consecuencias.** (1) Se paga dos veces, y el valor nuevo puede
cambiar por la puerta de atrás sin que nadie decida revisar. (2) El
mantenimiento de la verdad (:220-222) no puede funcionar: falta el valor
guardado que comparar. (3) La traza deja de ser auditable: el número que
decidía la respuesta no está en el registro. (4) Los conflictos D↔K
(condición 3, :185-187) no se pueden mostrar si una de las partes es prosa.

**Tensión de fondo: no todo lo consultado merece quedarse.**

| clase de premisa | ejemplo | qué hacer |
|---|---|---|
| caduca de inmediato | estado de un vuelo hoy, precio de hoy | reutilizarla es incorrecto: no promoverla |
| estable, es una regla | husos, calendarios, constantes | no es dato: es el mundo del código |
| volátil pero reutilizable | duración programada, cargo de una persona | guardar con su fecha de consulta |

**Propuesta (sin decidir):** la premisa se registra como **dependencia del
dato derivado** —con identidad, valor, procedencia y fecha de consulta— y
**se promueve a dato del corpus solo si otra pregunta la reutiliza**. Así el
corpus no se llena de datos perecederos y nada de lo que decidió una respuesta
se pierde.

**Prueba de mesa (decide si el registro sirve):** si la aerolínea cambia la
duración de 10 h 35 a 11 h 10, ¿basta mirar la dependencia para saber que el
1:50 perdió sostén, o hay que volver a consultar y comparar con la prosa de la
traza?

---

## Tensión 3 — «sostén: 0,88» (acordado)

**Lo que hay.** En el dato derivado: `radicación: 4-10-2026 · inferido: sí ·
sostén: 0,88` (:214). Un campo y un número bajo el nombre **sostén**.

**Tres cosas distintas bajo un mismo nombre.**

| lo que de verdad hay | dónde vive en el marco |
|---|---|
| **la ruta**: qué datos, reglas y herramientas produjeron la determinación | A.7: el error vive en la ruta |
| **la robustez**: cuántas rutas parcialmente independientes la sostienen | A.7: N(δ) = ⋂Cᵢ |
| **el grado del juicio**: cuánto sostiene Jev el juicio final | A.7 y guía §3.1: heurístico, por bandas |

**Cuatro daños.** (1) No sirve para mantener la verdad: si cambia una
dependencia, `0,88` no dice qué se cayó. (2) Confunde robustez con
verosimilitud: dos copias de la misma fuente dan grado alto y robustez **nula**.
(3) Reintroduce el número sin calibrar que el spike retiró el 19-09. (4) El
grado no es reproducible sin el juicio: 0,88 es el grado de un juicio concreto,
con un expediente y un modelo concretos; si Jev cambia de versión, el número
cambia sin que la ruta cambie.

**Acordado: partir el bloque.**

```
AV-569 · hora local de llegada · 1:50 · condiciones: París, 28-9-2026, duración normal
radicación: 4-10-2026 · inferido: sí

dependencias:  D1 (boletín, 8:15, radicado 2-10)
               K1 (API aerolínea, duración 10 h 35, consultada 4-10)
               R1 (regla del lunes) · R2 (husos IANA)
rutas:         1
juicio:        tipo: noul · grado: 0,88 · banda: «muy seguramente cierto» · modelo: jev-1.13.0
```

Regla de nombres: **«sostén» se reserva para la ruta; el grado de Jev va en
`juicio` y nunca se llama sostén.** La banda sigue sirviendo para elegir el
tono al entregar (condición 4): eso es política de entrega, no atributo del
dato guardado.

---

## Tensión 4 — vocabulario operativo (acordado; borrador de filas)

**Criterio acordado para decidir dónde va un término:**

- **no aparece en el ensayo** → parte **B** (`documento`, `foco`);
- **aparece con otro sentido** → parte **C** (`mundo`);
- **aparece con el mismo sentido aplicado** → no necesita fila, basta la regla
  de uso.

**Borrador de filas para la parte B** (no escritas todavía en el documento
vivo):

| Término | Definición en el proyecto | Relación con el marco | Origen |
|---|---|---|---|
| **Orquestador** | El componente que estructura la pregunta, mide la brecha, decide qué mundos trae, hace calcular al código y entrega o no. No es el usuario ni Jev. | Hace las operaciones que A.1–A.2 atribuyen al observador presente; es un componente del sistema, no un sujeto. | Visión operativa, 04-10 |
| **Brecha** | Lo que falta para pasar de A(Q \| K) a una respuesta: posiciones que siguen abiertas por falta de un dato o de una regla. | A.8: el conjunto de completaciones admisibles y su cambio. | Visión operativa, 04-10 |
| **Reglas de la consulta (R)** | Reglas con que se manipula y consulta el corpus: fuentes admitidas como premisa (solo el documento / sin externas con el mundo del orquestador / libre), autorización de agentes, tope de costo o tiempo, anclas. Las fija el usuario, el documento o el sistema. | Las R de la operación A₀(Q) —D,R→ A₁(Q) (A.8). | Visión operativa, 04-10 |
| **Radicación** | Fecha en que un dato entra a Zettel. La lleva todo dato: el del documento, el día en que se incorpora; el derivado, el día en que se guarda. La fecha propia del documento es un **dato**, no la radicación. | A.6, registro; distinción entre tiempo de transacción y tiempo de validez. | Visión operativa, 04-10 |
| **Dato derivado** | Determinación producida al responder una pregunta, registrada con radicación y dependencias; entra al corpus con el mismo estatus que los del documento. **Dato intermedio:** el derivado que sostiene a otro. | A.6 (dato) + A.7 (ruta). El campo `inferido` lo distingue de lo que el texto dice literalmente. | Visión operativa, 04-10 |
| **Dependencias** | Los datos y reglas que sostienen una determinación, con su valor, su procedencia y su fecha de consulta. | A.7: el sostén es la ruta. Permite reutilizar, revisar y auditar. | Propuesta de esta conversación, 04-10 |
| **Promoción** | Ascenso de una dependencia a dato del corpus cuando otra pregunta la reutiliza y su ventana de validez lo permite. | A.6 (dato registrado y recuperable) y A.7 (robustez por rutas independientes). | Propuesta de esta conversación, 04-10 |
| **Juicio (de Jev)** | El juicio que se somete y su grado, con la banda y el modelo; heurístico, nunca llamado sostén. | A.7 y guía §3.1: bandas heurísticas; el sostén es la ruta. | Propuesta de esta conversación, 04-10 |

**Abierto: «alcance».** A diferencia de `documento` y `foco`, **sí aparece en
el ensayo**: 10 veces (l. 47, 51, 57, 59, 129, 131, 263, 265, 309, 311), con el
sentido de «el alcance dentro del cual algo se considera, se compara o se
revisa». Si «alcance de una consulta» se considera **otro sentido**, su sitio
es C; si es el mismo sentido aplicado, se queda como está (la regla ya está en
la fila de `foco`). No se propone nada: se deja a decisión.

---

## Lo que no se toca

El faro y el marco (Q, A(Q), D, R, información y dato, radicación) se dan por
fijos. Esta discusión no propone cambios al ensayo ni a la parte A.

## Decisiones pendientes (para Frat y Cowork)

1. **¿A(Q) se representa?** Mínimo propuesto: dominio + estado por posición
   (admisible / inadmisible / indecidible). Si no, dejar por escrito que la
   condición de entrega 1 es auto-reporte.
2. **¿El esquema del dato derivado guarda `dependencias` y `rutas`, y promueve
   por reutilización?** Es la decisión que habilita el mantenimiento de la
   verdad y la condición de conflicto.
3. **¿`juicio` va separado del `sostén` en el mismo esquema?** Acordado en
   principio; falta el esquema concreto.
4. **¿Se escriben las ocho filas de B?** ¿Y «alcance» va a C, a B, o se queda
   como regla de uso?
5. **¿`mvp/` cuenta como proyecto nuevo** para la regla de los tres sitios
   (lista del README, mapa de AGENTS, «Dónde quedamos» de la memoria)?

## Qué se espera de Opus

Su opinión sobre los cinco puntos, y —si está de acuerdo— la forma de llevarlo
a los documentos vivos: qué filas van a B, si la tabla de A(Q) entra en la
visión operativa o en otro documento, y en qué orden se prueba.
