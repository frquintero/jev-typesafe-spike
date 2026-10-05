# Registro de la mesa de dominio

**Estado: EJECUTADA — comprobación guiada. Registro cerrado.**
Diseño, materiales y referencia preparados el 5-10-2026. Recorrido T1–T6 en una
pasada y un solo cotejo, según `mesa-dominio-plan.md` §5. Entradas congeladas:
no se modificó el plan, ni los materiales, ni la referencia.

## Datos de la sesión

- Fecha de ejecución: 5-10-2026, 15:31 (−05).
- Persona que recorre: Claude (agente, DeepSeek Harness), sesión local.
- Persona que evalúa: la misma.
- Modalidad: **comprobación guiada**, no lectura independiente. La referencia se
  había leído en esta misma sesión antes de la pasada; por eso ningún «cumple»
  de este registro se presenta como observación independiente. Una lectura
  limpia exigiría repetir T1–T6 con alguien que no haya visto la referencia
  (plan §5.1); no es condición para avanzar (véase la revisión posterior).
- Entradas utilizadas: las del paquete, sin desviación.
- Cálculo: en papel; sin herramienta, sin modelo y sin llamada a API. Jev no
  participa.
- R aplicada en las seis: solo premisas documentales de los documentos del
  dominio elegido; aritmética entera con la operación registrada; sin saber del
  lector, sin otro dominio y sin fuentes externas.

## Recorridos observados

### T1 · MONTAÑA, según el parte

- **Alcance documental utilizado:** `dominio_consulta = MONTAÑA`; documentos
  admitidos M1, M2 y M3.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** caso de estudio
  M1:C1 (refugio Peña Clara); aspecto «plazas habilitadas para pernoctar»;
  condiciones: noche del 27-9-2026 y «según el parte»; dominio de respuestas:
  número entero de plazas, con la regla «lo que el parte registra». Dentro de
  MONTAÑA, «el parte» resuelve a M1 (M1:S1, «Parte del refugio Peña Clara»),
  frente a M2 («Control de plazas») y M3 («Nota»).
- **Unidades examinadas y unidades seleccionadas, con motivo:** inventario de
  MONTAÑA examinado = M1:U1, M1:U2, M2:U1, M3:U1. Seleccionada **M1:U1**
  (M1:S1–S4): es la unidad del parte y su núcleo es el refugio preguntado.
  Excluidas: M1:U2 (senda del Robledal, ajena al aspecto), M2:U1 (el control no
  es el parte), M3:U1 (nota de un refugio sin identificación establecida).
- **Datos del campo, procedencia, radicación y respaldos:** campo = M1:D1 (42
  plazas; M1:S1–S2; documento M1; radicación 2-10-2026), M1:D2 (30 reservadas;
  M1:S1–S3), M1:D3 (60 sillas; M1:S1, M1:S4). Entran con la unidad. Mudas para
  esta pregunta: M1:D2 y M1:D3.
- **Identificación y evidencia o brecha:** no hay reidentificación que hacer:
  M1:S1 nombra Peña Clara y fija la noche. El caso es M1:C1, local a M1.
- **Posiciones antes/después, rutas, datos mudos y cambio en A(Q):** antes,
  ningún número sostenido. Después, **42 admisible con ruta M1:D1**; las demás
  cantidades no ganan sostén y no se marcan inadmisibles, porque el parte no
  contiene una determinación incompatible con 42 y solo una determinación
  incompatible bajo las mismas condiciones constitutivas excluye (mesa 1,
  decisión 3; ensayo l. 229). Efecto: **gana sostén**.
  - *Aclaración registrada (plan §5.5).* Lectura inicial: «según el parte» acota
    las unidades seleccionadas, así que M2:D1 (47) no entra en el campo ni es
    posición de esta pregunta. Lectura alterna: la restricción fija qué fuente
    **sostiene** la respuesta, no qué unidades pueden **examinarse**; bajo ella
    M2:U1 se examina y M2:D1 queda fuera del campo. La respuesta observada no
    cambia. Las dos lecturas se conservan (E5); la cláusula «examinado ≠ campo ≠
    ruta» de la revisión posterior las cubre.
- **Respuesta observada y brecha:** «Según el parte de Peña Clara (M1), la noche
  del 27-9-2026 había 42 plazas habilitadas para pernoctar». Cerrada respecto de
  lo que dice el parte; sin brecha.

### T2 · RIBERA, misma pregunta

- **Alcance documental utilizado:** `dominio_consulta = RIBERA`; documento
  admitido B1, y solo B1.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** caso B1:C1 (refugio
  Puerto Azul); mismo aspecto y noche que T1; «según el parte» resuelve a B1
  (B1:S1, «Parte del refugio Puerto Azul»).
- **Unidades examinadas y unidades seleccionadas, con motivo:** inventario de
  RIBERA = B1:U1. Seleccionada **B1:U1** (B1:S1–S3).
- **Datos del campo, procedencia, radicación y respaldos:** campo = B1:D1 (88
  plazas; B1:S1–S2; documento B1; radicación 3-10-2026) y B1:D2 (año de
  inauguración 1998; B1:S1, B1:S3). Mudo para esta pregunta: B1:D2.
- **Identificación y evidencia o brecha:** B1:S1 identifica Puerto Azul en la
  bahía del Astillero y fija la noche. No hay reidentificación que hacer.
- **Posiciones antes/después, rutas, datos mudos y cambio en A(Q):** antes,
  ningún número sostenido. Después, **88 admisible con ruta B1:D1**. Efecto:
  **gana sostén**. Frontera de dominio: «el refugio» de M1 no entra; de haber
  entrado, sería fuga de dominio (O1).
- **Respuesta observada y brecha:** «Según el parte de Puerto Azul (B1), la
  noche del 27-9-2026 había 88 plazas habilitadas para pernoctar». Cerrada; sin
  brecha. La misma Q con el mismo texto cambia de respuesta porque cambia el
  `dominio_consulta`.

### T3 · MONTAÑA, parte y control

- **Alcance documental utilizado:** `dominio_consulta = MONTAÑA`; documentos
  admitidos M1, M2 y M3.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** caso Peña Clara
  (M1:C1); aspecto «plazas habilitadas para pernoctar»; condiciones: noche del
  27-9-2026 y considerar el parte y el control.
- **Unidades examinadas y unidades seleccionadas, con motivo:** examinadas
  M1:U1, M1:U2, M2:U1, M3:U1. Seleccionadas **M1:U1 y M2:U1**: Q nombra el parte
  y el control. Excluidas M1:U2 (senda) y M3:U1 (nota de identidad no
  establecida, que no aporta al recuento).
- **Datos del campo, procedencia, radicación y respaldos:** campo = M1:D1 (42),
  M1:D2 (30), M1:D3 (60 sillas), y M2:D1 (47 plazas; M2:S1–S2; documento M2;
  radicación 4-10-2026). Mudas para el recuento: M1:D2 y M1:D3.
- **Reidentificación y comparabilidad, evidencia o brecha:** M2:S1 declara «el
  mismo refugio y la misma noche que el parte M1»; con M1:S1 (Peña Clara,
  27-9-2026) queda acreditado que los dos recuentos son del mismo caso, aspecto
  y condiciones. Se conservan los ids locales M1:C1 y M2:C1: no se fusionan ni
  se construye un registro de identidad. No hay regla de prioridad registrada:
  la radicación posterior (4-10 frente a 2-10) no concede prioridad **por sí
  sola**, y eso no depende de la declaración de M2:S3, que solo confirma que no
  hay corrección ni sustitución.
- **Posiciones antes/después, rutas, conflicto y cambio en A(Q):** antes,
  ninguna posición sostenida. Después, **42 con ruta [M1:D1]** y **47 con ruta
  [M2:D1]**, ambas admisibles, con `conflicto: [M1:D1, M2:D1]`; no se dispone
  cifra única. Efecto: **ganan sostén y entra un conflicto**.
- **Respuesta observada y brecha:** «El parte registra 42 plazas y el control
  47, para el mismo refugio y la misma noche, según declara M2:S1. El control
  dice que no sustituye el parte: los documentos dejan el recuento en
  conflicto». Desenlace: **en conflicto**. Brecha: una regla registrada de
  prioridad, si se quisiera una cifra única; el paquete no la trae.

### T4 · MONTAÑA, cálculo y derivado

- **Alcance documental utilizado:** `dominio_consulta = MONTAÑA`; admitidos M1,
  M2 y M3.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** caso M1:C1 (Peña
  Clara); aspecto «plazas sin reservar»; condiciones: noche del 27-9-2026, sobre
  plazas habilitadas para pernoctar y «según el parte».
- **Unidades examinadas y unidades seleccionadas, con motivo:** examinadas las
  cuatro de MONTAÑA. Seleccionada **M1:U1**. Excluidas M1:U2 (senda), M2:U1 (el
  control no es el parte) y M3:U1 (nota).
- **Datos del campo, procedencia, radicación y respaldos:** campo = M1:D1
  (42; M1:S1–S2; radicación 2-10-2026), M1:D2 (30; M1:S1–S3) y M1:D3 (60
  sillas; M1:S1, M1:S4). Mudo para la operación: M1:D3.
- **Comparabilidad de las entradas y evidencia:** M1:D2 lleva como condición la
  misma noche y el mismo conjunto de plazas que M1:D1, y su respaldo (M1:S3, «De
  esas plazas») remite al total de M1:S2. Las dos entradas comparten caso,
  aspecto-eje y condiciones constitutivas: la resta es admisible. La relación la
  da el documento; que la operación responda la pregunta es juicio con respaldo
  (§9.7).
- **Operación en papel, posiciones antes/después, rutas y datos mudos:** OP1 =
  «42 − 30 = 12», entradas M1:D1 y M1:D2. Después, **12 admisible con ruta
  [M1:D1, M1:D2, OP1]**. M1:D3 queda en el campo y fuera de la operación (su
  aspecto es el número de sillas del comedor). No se emplea 47, que no es el
  parte. Efecto: **gana sostén**. Se conserva la palabra del parte, «sin
  reservar»; llamarlas «desocupadas» exigiría una premisa de equivalencia que el
  paquete no trae.
- **Cambio en A(Q), respuesta observada y brecha:** de ningún número sostenido a
  12 con ruta. «Según el parte, había 12 plazas sin reservar esa noche: 42
  habilitadas menos 30 reservadas». Cerrada respecto del parte y del cálculo; la
  fecha de referencia la fija el parte (27-9-2026).
- **Registro derivado en papel, con condiciones y dependencias:**

| Elemento | Contenido observado |
|---|---|
| Identificador de ensayo | DD-mesa-1; no incorporado al corpus real. |
| Pregunta | T4, con su texto, `dominio_consulta: MONTAÑA` y la R de la mesa. |
| Determinación | M1:C1, refugio Peña Clara · plazas sin reservar · 12 plazas. |
| Condiciones | Noche del 27-9-2026; plazas habilitadas para pernoctar; resultado según el parte M1; «sin reservar» conserva la palabra del parte. |
| Entrada 1 | M1:D1 = 42 plazas; respaldo M1:S1–S2; documento M1; radicación 2-10-2026. |
| Entrada 2 | M1:D2 = 30 plazas; respaldo M1:S1–S3; documento M1; radicación 2-10-2026. |
| Operación | OP1; expresión `42 − 30`; resultado 12; cálculo en papel. |
| Herramienta o versión | Ninguna: no se atribuye a software ni a una versión. |
| Fecha del registro | 5-10-2026. |
| Juicio de Jev | No ejecutado. |
| Estado | Candidato en papel; no radicado en el corpus real. |

  M1:D3 queda en el campo y no en las entradas del cálculo. Conservar el dominio
  documenta el origen; aquí no se decide la pertenencia del derivado ni su
  reutilización en otros dominios.

### T5 · MONTAÑA, identidad de la nota

- **Alcance documental utilizado:** `dominio_consulta = MONTAÑA`; admitidos M1,
  M2 y M3.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** la referencia de
  M3:U1 (M3:C1, refugio sin nombre ni ubicación establecidos); aspecto
  «identidad del refugio»; pregunta de sí/no; posiciones: «es Peña Clara» y «es
  otro refugio».
- **Unidades examinadas y unidades seleccionadas, con motivo:** examinadas
  M1:U1, M1:U2, M2:U1, M3:U1. Seleccionadas **M1:U1 y M3:U1**: la segunda es el
  caso preguntado y la primera el candidato de identidad. **M2:U1** admitida
  como contexto opcional del refugio ya identificado: aporta todos sus datos al
  campo y quedan mudos respecto de la identidad preguntada. M1:U2 fuera.
- **Datos del campo, procedencia, radicación y respaldos:** M1:D1, M1:D2, M1:D3
  (documento M1, radicación 2-10-2026); M3:D1 (presencia de goteras; M3:S1–S2;
  documento M3; radicación 5-10-2026) y, si se toma el contexto, M2:D1
  (documento M2, radicación 4-10-2026).
- **Reidentificación, evidencia o brecha:** M3:S2 deja sin establecer el nombre
  y la ubicación, y no establece que sea distinto de Peña Clara. M2:S1 vincula
  M2 con M1, no con M3. La fecha compartida del 27-9-2026 y la pertenencia a
  MONTAÑA no deciden identidad. Falta una identificación del refugio o una
  correspondencia documentada con M1.
- **Posiciones antes/después, rutas, datos mudos y cambio en A(Q):** antes y
  después, «es Peña Clara» y «es otro refugio» permanecen **abiertas**, sin ruta
  que sostenga ninguna de las dos. No se atribuye cambio de estado a la falta de
  identificación. Efecto: **ninguno**. M3:D1 y los datos del contexto quedan
  mudos para la identidad preguntada.
- **Respuesta observada y brecha:** «La nota M3 no permite establecer si habla
  de Peña Clara. Hace falta una identificación del refugio o una correspondencia
  documentada con M1». Desenlace: **identidad no establecida**, distinto de «no
  establecido» de la posición (aquí nada mueve la tabla) y de «no cerrable» (no
  falta un dato del corpus ni del mundo: falta evidencia de identidad). Brecha:
  esa identificación o esa correspondencia.

### T6 · MONTAÑA, año de inauguración

- **Alcance documental utilizado:** `dominio_consulta = MONTAÑA`; admitidos M1,
  M2 y M3.
- **Caso, aspecto, condiciones y posiciones posibles de Q:** caso M1:C1 (Peña
  Clara, identificada en M1:S1); aspecto «año de inauguración»; sin condiciones
  añadidas; posiciones: años, en la escala de fechas.
- **Inventario examinado y unidades seleccionadas, con motivo:** inventario de
  MONTAÑA examinado completo: M1:U1, M1:U2, M2:U1, M3:U1. **Ninguna unidad
  determina el año.** Contexto admitido: M1:U1 y/o M2:U1, como contexto del
  caso; se acepta campo vacío o con una o ambas. M1:U2 no es pertinente.
- **Datos del campo, procedencia, radicación y respaldos:** vacío, o los datos
  de M1:U1 (y M2:U1) según el contexto elegido; ninguno es del aspecto
  preguntado. Documentos y radicaciones: M1 (2-10-2026), M2 (4-10-2026).
- **Identificación del caso y evidencia:** Peña Clara queda identificada por
  M1:S1. La ausencia se comprueba sobre el inventario completo de MONTAÑA; las
  unidades examinadas para comprobarla no se convierten todas en campo
  pertinente.
- **Posiciones antes/después, rutas, datos mudos y cambio en A(Q):** ningún año
  gana sostén ni se excluye año alguno. Efecto: **ninguno**. B1:D2 (1998) no
  entra: B1 no pertenece al dominio MONTAÑA, es otro documento y otro refugio.
- **Respuesta observada y brecha:** «Los documentos de MONTAÑA no establecen en
  qué año se inauguró Peña Clara». Desenlace: **año no establecido**. Brecha
  concreta: una determinación de inauguración referida a Peña Clara con respaldo
  documental admitido.

## Discriminadores (referencia §3)

1. **T1 y T2 con el mismo texto de Q:** porque el `dominio_consulta` cambia los
   documentos admitidos. MONTAÑA lleva a M1 (42, M1:D1); RIBERA lleva a B1 (88,
   B1:D1). La coincidencia de «el refugio» no autoriza a cruzarlos.
2. **Qué permite comparar 42 y 47 en T3:** M2:S1, que declara el mismo refugio y
   la misma noche que M1, junto con M1:S1. Sin esa declaración serían dos casos
   locales distintos y las cifras no serían comparables.
3. **Por qué la radicación posterior de M2 no resuelve T3:** porque ninguna regla
   registrada concede prioridad por fecha. La declaración de M2:S3 no es la que
   lo impide: sin regla, la radicación posterior no basta por sí sola, la declare
   o no el control. Sin regla de prioridad hay conflicto y se muestra.
4. **Por qué las 60 sillas están en el campo de T4 y fuera de su operación:**
   pertenecen a M1:U1 y entran con la unidad, pero su aspecto (número de sillas
   del comedor) no es el de la operación, que resta plazas reservadas de plazas
   habilitadas.
5. **Qué permite reidentificar M2 y qué falta para M3:** para M2, la declaración
   literal M2:S1 con M1:S1. Para M3 falta todo: M3:S2 niega nombre y ubicación, y
   ni la fecha compartida ni el dominio acreditan correspondencia.
6. **Por qué 1998 no puede sostener la respuesta de T6:** B1 no está admitido en
   una consulta de MONTAÑA (O1), y su dato es de otro refugio. No hay ruta
   documental admitida hacia un año de inauguración de Peña Clara.

## Cotejo único

Cotejo aplicado una sola vez, con la referencia abierta después de la pasada.
Valores: cumple / falla / no evaluable.

| Caso | O1 alcance | O2 selección/contexto | O3 identificación | O4 respuesta/efecto | O5 registro | Evidencia de la evaluación |
|---|---|---|---|---|---|---|
| T1 | cumple | cumple | cumple | cumple | cumple | M1:U1 con M1:D1 da 42; M1:D2 y M1:D3 mudos; ninguna premisa de M2. La ambigüedad de «según el parte» se registró con sus dos lecturas (E5); la respuesta no cambia. |
| T2 | cumple | cumple | cumple | cumple | cumple | B1:U1 con B1:D1 da 88; no entra ningún dato de MONTAÑA pese a que ambos documentos dicen «el refugio». B1:D2 mudo. |
| T3 | cumple | cumple | cumple | cumple | cumple | M2:S1 acredita la correspondencia con M1:S1; 42 y 47 con sus rutas y `conflicto: [M1:D1, M2:D1]`; no se elige por radicación, porque sin regla de prioridad la fecha no basta. Ids locales conservados. |
| T4 | cumple | cumple | cumple | cumple | cumple | Comparabilidad de M1:D1 y M1:D2 por sus condiciones y por «De esas plazas» (M1:S3); OP1 `42 − 30 = 12` con entradas y respaldos; M1:D3 en el campo y fuera de la operación; no se usa 47 ni «desocupadas». El registro en papel conserva entradas y operación (E6 para el esquema). |
| T5 | cumple | cumple | cumple | cumple | cumple | M3:S2 no aporta identidad; M2:S1 no vincula M3; las dos posiciones quedan abiertas sin ruta y sin cambio de estado. El desenlace «identidad no establecida» no tiene valor propio en el esquema; basta registrar qué queda sin establecer y su brecha (E1). |
| T6 | cumple | cumple | cumple | cumple | cumple | Inventario de MONTAÑA revisado sin año; B1:D2 (1998) fuera por dominio; ningún año gana ni pierde sostén. El esquema no tiene dónde anotar el inventario examinado, distinto del campo (E9). |

**Lectura del cotejo.** Los seis recorridos cumplen las cinco obligaciones
aplicables y ninguno quedó «no evaluable». La lectura conjunta del plan §6 se
sostiene: T1–T2 aislamiento, T3 identidad y conflicto, T4 selección, cálculo y
derivación, T5–T6 referencia insuficiente y ausencia. No se informa porcentaje
global, porque el plan §6 no lo admite como compensación.

**Salvedad que condiciona todo lo anterior.** Es una comprobación guiada: la
referencia se conocía antes de la pasada. Los «cumple» acreditan que el recorrido
puede describirse sin contradecir la referencia, no que un lector independiente
llegue a lo mismo. Y el producto útil no es el cotejo, sino los hallazgos de
abajo: el contrato describe bien los seis casos, pero su representación no tiene
dónde escribir varios de los datos que los casos exigen (véase la reclasificación
posterior).

## Fallos o límites que producen una acción

Ninguno es un fallo del recorrido: los seis cumplen. Son huecos de
representación que la mesa dejó a la vista, cada uno con su corrección concreta y
su destino. Su adopción se reclasifica en el apartado siguiente.

| # | Hallazgo | Resultado observado y evidencia | Obligación afectada | Corrección concreta | Destino |
|---|---|---|---|---|---|
| E1 | Falta el desenlace de identidad no establecida. | T5: las dos posiciones quedan abiertas, sin ruta y sin cambio de estado; el contrato §9.5 dice «dejar la referencia abierta» pero los desenlaces del esquema son cerrada · en conflicto · no establecido · no cerrable. | O3, O4 | Añadir el estado de la referencia (abierta / acreditada) y, si se prefiere, el desenlace «identidad no establecida», distinto de «no establecido» y de «no cerrable». | Contrato §9.5 + esquema 2 §4 |
| E2 | El alcance documental no tiene campo en la tabla. | T1, T2 y T6 dependen de qué documentos están admitidos, y no hay dónde conste; sin eso O1 no es auditable en el registro. | O1 | Registrar `dominio_consulta` y la lista de documentos admitidos en la cabecera de la tabla y en la salida de la corrida. | Contrato §9.1 + esquema 2 §4 + E0 |
| E3 | «Dominio» es homónimo dentro del propio esquema. | El esquema 2 §4 usa `dominio {escala, regla}` (sentido del ensayo) y el contrato §9 usa «dominio documental» (documentos elegidos). | O1, O4 | Nombrar `dominio_respuestas` (escala y regla) y `dominio_consulta` (documentos admitidos); registrarlo en la parte C de las definiciones. | Contrato + esquema 2 §4 + `definiciones-del-marco.md` C |
| E4 | La R de la mesa no es expresable con los modos vigentes. | Esquema 2 §3 ofrece `solo el documento`, `sin externas…` y `libre`; ninguno expresa «solo documentos del dominio elegido», y la aritmética admitida no tiene dónde registrarse. | O1, O5 | Mantener el dominio como entrada separada de R (contrato §9.1) y registrar la operación con id, expresión, entradas y resultado. | Contrato + configuración de E0 + esquema 2 §3 |
| E5 | La restricción de procedencia que trae Q no tiene lugar propio. | T1, T2 y T4: «según el parte» decide qué se responde; sus dos lecturas posibles se registraron en T1. | O2, O4 | Declarar que esa restricción entra en las condiciones constitutivas del encabezado y acota la selección de unidades; conservar la aclaración registrada. | Contrato §9.1 y §9.6 + E1 |
| E6 | Al derivado le faltan la operación y el dominio. | T4: el registro en papel conserva entradas, expresión y resultado, pero el bloque de derivación del esquema 2 §5 solo tiene pregunta, R, radicación, dependencias, rutas y juicio. | O5 | Añadir `dominio_consulta` y un bloque de operación (id, expresión, entradas, resultado) al registro del derivado; la equivalencia «sin reservar» = «desocupadas» no se admite sin premisa. | Registro candidato (esquema 2 §5) + `pieza1` |
| E7 | La comparabilidad de las entradas de una operación no tiene comprobación ni lugar. | T4: hubo que establecer que M1:D1 y M1:D2 comparten caso, aspecto-eje y condiciones antes de restar. | O3, O5 | Declarar si esa comparabilidad se comprueba en código contra las condiciones registradas o queda como juicio, y dónde se anota. | Contrato §9.7 + E2 / verificador |
| E8 | El derivado calculado en papel no encaja con el requisito de versión. | Esquema 2 §5 y §7 piden `version` del mundo del código; en la mesa no hay herramienta ni versión que declarar. | O5 | Admitir un derivado con operación registrada y sin versión de software, declarando quién calculó y con qué expresión. | Contrato §9.8 + registro del derivado |
| E9 | La ausencia exige registrar el inventario examinado, que no es el campo. | T6: para sostener «los documentos de MONTAÑA no establecen el año» hay que registrar que se revisó el inventario completo; el esquema solo tiene `campo` como datos pertinentes. | O2, O5 | Guardar en el registro de corrida las unidades examinadas, distintas de las del campo; la ausencia se respalda con ese registro. | Contrato (traza) + E1 |

### Revisión posterior del cierre (5-10-2026)

Los nueve hallazgos se conservan tal como se observaron. Tras revisar el cierre
se reclasifican así, para no convertirlos en un bloque de requisitos:

- **Obligaciones de trazabilidad (se adoptan con §9).** E2 (alcance documental y
  documentos admitidos), E3 (los dos sentidos de «dominio»), E6 (operación y
  dominio en el registro del derivado) y E9 (inventario examinado). La cláusula
  **examinado ≠ campo ≠ ruta** cubre E5 y E9 a la vez: restringir qué fuente
  sostiene la respuesta no prohíbe consultar otras unidades.
- **Precisiones ya resueltas, sin cambio de esquema.** E1: el esquema ya admite
  «no establecido»; basta registrar que lo no establecido es la identidad, con su
  brecha. E7: la relación que autoriza la resta la da el documento (M1:S3, «De
  esas plazas»); el código comprueba los valores registrados y ejecuta la
  operación, y que esa operación responda la pregunta es juicio con respaldo
  (§9.7). E4: no hace falta un modo nuevo de R; basta precisar la aplicación de
  `solo el documento` al conjunto de documentos admitidos y registrar la
  operación.
- **Retirado.** E8: el cálculo en papel es una particularidad de la mesa; no
  justifica quitar su `version` a los cálculos ejecutados por software ni añadir
  soporte de cálculo manual a la primera implementación.

La lectura independiente de T1–T6 no es condición para avanzar: aportaría
evidencia sobre la claridad del contrato, no sobre la verdad de los recorridos.

## Cierre

- **Disposición:** *Contrato coherente para estos casos* (plan §7), con dos
  salvedades: es una comprobación guiada, y el contrato es coherente como
  descripción pero su representación necesita las cuatro obligaciones de
  trazabilidad y las precisiones de la revisión posterior antes de servir de base
  de implementación. Ninguna obligación quedó «no evaluable»; un punto del
  paquete admite dos lecturas (E5) y se conservan las dos.
- **Qué parte del contrato queda fundada para estos casos:** entrada con
  `dominio_consulta` elegido y R aparte; incorporación con ids locales y sin
  identidad global previa; unidades como puente de selección, con su texto y sus
  datos completos; campo, ruta y datos mudos distinguibles; reidentificación
  acreditada con la declaración documental cuando Q la necesita; A(Q) con
  respuestas y no unidades; derivación con condiciones, entradas y operación;
  pertenencia por dominio como propiedad del código.
- **Qué parte queda pendiente y por qué:** las cuatro obligaciones de
  trazabilidad y las precisiones de la revisión posterior, y la decisión de Frat
  sobre la cláusula del índice global previo. La lectura independiente no es
  condición: aportaría evidencia sobre la claridad del contrato (véase la
  salvedad del cotejo).
- **Propuesta de adopción o modificación concreta para Frat:** adoptar §9 como
  base del plan candidato del orquestador con las cuatro obligaciones de
  trazabilidad (E2, E3, E6, E9) y las precisiones de E1, E4 y E7; y sustituir la
  exigencia de un índice de casos previo a la consulta
  (`mvp/orquestador-plan.md`, §4.1) por alcance por dominio más
  reidentificación acreditada durante la consulta. No se adopta E8. El plan
  original permanece intacto hasta esa decisión (plan §9).
- **Primer trabajo ejecutable:** la parte mecánica, sin LLM y sin Jev:
  pertenencia por dominio, consulta ligada al dominio, lectura **completa** de la
  unidad seleccionada (texto, datos, condiciones, respaldo, documento y
  radicación) y cabecera con `dominio_consulta`.
- **Criterio de terminación de ese trabajo:** sobre las entradas de esta mesa, y
  con verificación mecánica, (a) una lectura que pida un id de RIBERA en una
  consulta de MONTAÑA se rechaza por «fuera de alcance»; (b) la lectura de M1:U1
  devuelve M1:S1–S4 y M1:D1–M1:D3 completos, sin perder condiciones ni respaldos;
  (c) el registro de la corrida anota `dominio_consulta: MONTAÑA` y la lista de
  documentos admitidos.
- **Parte de las seis consultas que se utilizará al implementarlo:** T1, T2 y T6
  primero (aislamiento, lectura por unidad y ausencia con inventario examinado);
  T3, T4 y T5 después, como casos de desarrollo del resto del contrato. Las seis
  quedan como casos de desarrollo; medir generalización exige una reserva
  independiente (plan §8).
- **Fecha y responsable del cierre:** 5-10-2026, Claude (DeepSeek Harness), en
  comprobación guiada. La decisión de adopción corresponde a Frat.

No se inicia una segunda mesa dentro de este archivo.
