# Mesa de dominio: de los documentos a una respuesta

Fecha: 5-10-2026. Estado: **diseño completo; mesa ejecutada en comprobación
guiada y registro cerrado** (`mesa-dominio-resultado.md`).
Trabajo dentro del MVP existente. Este paquete es una propuesta de prueba y
de contrato; no adopta cambios en los documentos vivos ni ejecuta modelos.

## 1. Para qué hacemos esta mesa

**Decisión que debe permitir tomar:** si podemos llevar a código un contrato
de consulta donde el usuario elige un dominio documental, el orquestador
selecciona unidades pertinentes dentro de él y usa sus datos con contexto para
proponer el cambio en A(Q), sin necesitar una identidad global de casos
resuelta al incorporar los documentos.

**Conjetura:** ese recorrido puede describirse sin contradicciones en los seis
casos de este paquete. El recorte documental evita mezclar dominios; la
reidentificación que una pregunta necesita se establece con evidencia, y la
referencia insuficiente queda abierta.

La mesa examina si el contrato es coherente y suficientemente concreto para
implementar una primera versión. Una ejecución manual favorable no mide la
precisión de un LLM ni demuestra que el diseño escale a cualquier corpus.

**Producto del cierre:** un registro de seis consultas, una lectura de sus
resultados y una disposición sobre el contrato de §9. Incluso si hay fallos,
debe quedar escrito qué obligación falla, qué cambio concreto exige y qué
trabajo sigue. El producto no es otro documento de preguntas abiertas.

## 2. Qué aprendemos de las mesas anteriores

Fuentes locales: `mesa1/resultado.md`, `mesa1b/resultado.md` y
`pieza1/registro.md`.

La mesa 1 dejó seis reglas abiertas y una ampliación del diff. La mesa 1b
mezcló diferencias de formato con revisión, conflicto y condiciones
temporales. La pieza 1 convirtió parte de ese trabajo en código y en un
registro derivado. Por tanto, las mesas sí dejaron resultados; el recorrido
fue creciendo mientras se evaluaba.

Esta mesa tiene una sola decisión de contrato. Se evalúan obligaciones
semánticas fijadas antes de ejecutar. Las diferencias de redacción, orden de
ids o presentación se aceptan cuando conservan el mismo significado. La
sesión termina con una disposición y un siguiente trabajo identificable.

## 3. Paquete listo para ejecutar

| Archivo | Para qué sirve |
|---|---|
| [Plan](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/mvp/temp/mesa-dominio-plan.md) | Objetivo, consultas, instrucciones, evaluación, cierre y contrato candidato. |
| [Materiales](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/mvp/temp/mesa-dominio-materiales.md) | Dos dominios, cuatro documentos sintéticos, cinco unidades y ocho datos preparados a mano. |
| [Referencia](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/mvp/temp/mesa-dominio-referencia.md) | Evidencia y resultados esperados, fijados antes de ejecutar. Se abre al evaluar. |
| [Registro](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/mvp/temp/mesa-dominio-resultado.md) | Registro para llenar; comienza expresamente pendiente. |

Todo el material es sintético. Las unidades y los datos están dados: en esta
mesa se prueba su uso ante una pregunta. El desempeño del extractor se medirá
en otra etapa.

**Vocabulario fijo para esta sesión:**

- **Dominio documental:** documentos que el usuario eligió consultar. Se
  registra como `dominio_consulta`.
- **Dominio de respuestas:** posiciones posibles bajo el aspecto de Q. Se
  describe al anotar A(Q). No determina qué documentos están disponibles.
- **Campo:** material de las unidades seleccionadas para Q, con sus datos,
  contexto y respaldos. No es el conjunto de respuestas.
- **Ruta:** lo utilizado para sostener o excluir una posición. Un dato puede
  estar en el campo y quedar mudo.

Se sigue la distinción de `definiciones-del-marco.md`, A.8 y parte C, y la
tabla de `zettel-vision-operativa.md`. La selección por unidades es el puente
operativo candidato que examinamos aquí.

## 4. Reglas y seis consultas

R es común: las premisas documentales admitidas son las de los documentos del
dominio elegido. Se admite aritmética entera sobre sus valores, dejando
registrada la operación. No se admiten nuevas premisas del saber del lector,
de otro dominio ni de fuentes externas. Jev no participa.

Estas reglas están escritas en lenguaje de mesa. No añaden un nuevo alias a
los modos de configuración existentes.

| Consulta | Dominio elegido | Pregunta | Qué discrimina |
|---|---|---|---|
| T1 | MONTAÑA | Según el parte del refugio, ¿cuántas plazas habilitadas para pernoctar había la noche del 27-9-2026? | Resolver «el refugio» dentro del dominio y distinguir plazas de sillas. |
| T2 | RIBERA | Según el parte del refugio, ¿cuántas plazas habilitadas para pernoctar había la noche del 27-9-2026? | La misma pregunta, en otro dominio, debe usar otra fuente y otro caso. |
| T3 | MONTAÑA | ¿Cuántas plazas habilitadas para pernoctar tenía Peña Clara la noche del 27-9-2026, considerando el parte y el control? | Reidentificar con evidencia explícita y mostrar un conflicto entre documentos. |
| T4 | MONTAÑA | Según el parte, ¿cuántas plazas del refugio estaban sin reservar la noche del 27-9-2026? | Calcular con dos datos del mismo contexto y proponer un derivado trazable. |
| T5 | MONTAÑA | ¿El refugio mencionado en la nota M3 es Peña Clara? | Mantener abierta una identidad que el material no establece. |
| T6 | MONTAÑA | ¿En qué año se inauguró el refugio Peña Clara? | Declarar la falta de respuesta, aunque otro dominio sí tenga un año de inauguración. |

En T1, T2 y T4, «según el parte» fija la procedencia de lo preguntado. T3 pide
considerar ambos documentos. Una fecha de radicación posterior no establece
por sí sola que una fuente corrija a otra.

## 5. Cómo se ejecuta: una pasada y una revisión

Duración orientativa: una sesión de unos 45 minutos. El cierre lo fija el
procedimiento, no acertar antes de que venza un reloj.

1. **Preparar.** Una persona hace el recorrido y otra puede evaluarlo. Anotar
   quién participa y la fecha en `mesa-dominio-resultado.md`. Si la misma
   persona hace ambos papeles o ya vio la referencia, registrar
   «comprobación guiada»; no presentarla como lectura independiente.
2. **Congelar.** Usar estos documentos, unidades, datos, preguntas y R tal
   como están. Abrir materiales y plan. Reservar la referencia para el
   cotejo. Durante la pasada no se cambian las entradas para mejorar una
   respuesta.
3. **Recorrer T1–T6, una vez cada una.** Para cada consulta, llenar los
   apartados del registro: alcance; unidades elegidas; datos del campo;
   identificación y comparabilidad; posiciones y rutas; cambio en A(Q);
   respuesta y brecha; derivado cuando corresponda. Escribir las evidencias
   que permiten pasar de un apartado al siguiente.
4. **Distinguir dos decisiones.** Primero, la pertenencia documental delimita
   qué se puede consultar. Después, la pertinencia decide qué unidades se
   consideran. Al seleccionar una unidad se conserva su texto completo y
   los datos preparados, aunque algunos queden mudos.
5. **Cotejar una vez.** Abrir la referencia. Aplicar §6 por consulta, citando
   el resultado observado y el respaldo que decide la evaluación. Una
   respuesta ambigua del ejecutante puede aclararse una vez usando las
   mismas entradas; se conserva la respuesta inicial y la aclaración.
   Una propuesta de cambiar el material o la regla se registra como tal,
   sin convertirla en una nueva corrida dentro de la sesión.
6. **Cerrar.** Llenar la disposición de §7 y el siguiente trabajo de §8. Una
   pregunta no resuelta se registra como brecha concreta; no autoriza a
   escoger una respuesta ni a seguir agregando casos.

Para anotar A(Q) basta expresar las posiciones que ganan sostén, las
alternativas que quedan abiertas y el conflicto, con sus rutas. Se pueden
usar las filas del esquema existente. El cotejo de esta mesa compara esa
proyección semántica; no exige dos JSON idénticos ni reabre la representación
de `resto` o el comparador de las mesas anteriores.

## 6. Cómo se leen los resultados

Se evalúa cada consulta por estas cinco obligaciones. Una obligación puede
quedar «cumple», «falla» o «no evaluable», con una evidencia escrita.

| Obligación | Pregunta de evaluación | Fallo que importa |
|---|---|---|
| O1 · Alcance | ¿Campo, rutas y respuesta usan únicamente documentos admitidos del dominio elegido? | Entra un documento de otro dominio, incluso como premisa sin cita. |
| O2 · Selección y contexto | ¿Se recuperan las unidades necesarias, conservando condiciones, citas y contexto? | Se pierde el total o la fecha; se confunden sillas y plazas; se trae una unidad ajena a la pregunta. |
| O3 · Identificación | ¿La identidad y la comparabilidad se sostienen con evidencia, o quedan abiertas cuando falta? | Fusionar por nombre o dominio; tratar T5 como identidad o diferencia establecida. |
| O4 · Respuesta y efecto | ¿La posición, el conflicto o la brecha corresponden a los datos y R? ¿Se distingue campo de ruta? | Elegir una fuente en T3 sin regla; inventar un año en T6; usar datos mudos como sostén. |
| O5 · Registro | ¿Cada resultado mantiene su procedencia y T4 conserva sus entradas y operación? | Una cifra sin ruta; un derivado sin fecha de referencia o sin dependencias recuperables. |

La referencia declara unidades necesarias y, donde procede, contexto
opcional. No se penaliza una variante allí admitida. Una diferencia de forma
que conserva las cinco obligaciones se anota como «equivalente» y no abre una
decisión nueva.

Si una obligación no puede evaluarse porque el propio paquete está ambiguo,
anotar el pasaje exacto y las dos lecturas posibles. Eso es una limitación de
la mesa, no un error atribuible al ejecutante.

**Lectura conjunta:** T1–T2 examinan el aislamiento; T3, identidad y conflicto;
T4, selección, cálculo y derivación; T5–T6, referencia insuficiente y ausencia
de respuesta. Se informa el resultado de los seis casos. Un porcentaje global
no compensa una fuga de dominio o una identidad inventada.

## 7. Regla de cierre y decisión utilizable

Tras la revisión se elige una de estas disposiciones:

| Disposición | Cuándo corresponde | Qué queda al cerrar |
|---|---|---|
| **Contrato coherente para estos casos** | Los seis recorridos cumplen las obligaciones aplicables, sin aspectos no evaluables. | Contrato de §9 listo como base de una implementación candidata; seis casos de desarrollo para probarla. |
| **Recorrido con fallos identificados** | Hay fallos evaluables en selección, identidad, respuesta o registro. | Lista finita de fallos y ubicación de la corrección: código, lectura del orquestador o contrato. Un error del ejecutante no demuestra por sí solo que el contrato sea incoherente. |
| **Decisión insuficientemente fundada** | Falta una consulta, el material admite lecturas incompatibles relevantes o no se puede decidir una obligación. | Límite concreto y dato o decisión necesarios para resolverlo. Se indica qué parte del contrato queda lista y cuál queda pendiente. |

El registro se cierra también en las dos últimas disposiciones. No se
rebautizan fallos como diferencias de formato ni se adopta el contrato por
defecto. La decisión final de adopción corresponde a Frat; el ejecutante
deja el resultado y la propuesta revisables.

**Esta mesa no demuestra que nunca hará falta un índice.** Un resultado
favorable muestra que estos recorridos no necesitan una fusión global previa.
La necesidad futura de una estructura de búsqueda se examinará con un problema
de recuperación observado.

## 8. Para qué se usan los resultados y qué sigue

Cada hallazgo debe producir una acción con destino, sin volver a afinar esta
mesa por rutina:

| Hallazgo | Trabajo que sigue |
|---|---|
| Recorrido coherente | Llevar §9 al plan candidato del orquestador y construir la parte mecánica: pertenencia, consulta ligada a dominio, lectura protegida y procedencia. Después ejecutar un orquestador mínimo sobre ese contrato. |
| Fuga de dominio o lectura de un id fuera del alcance | Corregir el límite de las herramientas en código y comprobarlo en la implementación. |
| Unidad omitida, contexto perdido o ruta que no sostiene | Corregir la obligación de lectura y probarla al implementar E1. Estas entradas quedan como desarrollo; medir generalización requiere una reserva independiente. |
| Identidad inventada o conflicto resuelto sin respaldo | Explicitar en E1 qué evidencia permite reidentificar y qué queda abierto; conservar las referencias documentales. |
| Derivado sin dependencias | Ampliar el registro candidato y comprobar guardado/lectura con la pieza 1. |
| Ambigüedad del contrato o del propio paquete | Escribir una única modificación concreta, su motivo y qué caso afecta. Frat decide esa modificación; el registro conserva el desacuerdo o la parte pendiente. |

El cierre identifica el **primer trabajo ejecutable** y su criterio de
terminación. Por ejemplo: «el lector rechaza un id de RIBERA en una consulta
de MONTAÑA y devuelve completa M1:U1». Las seis consultas pasan a ser casos de
desarrollo para ese trabajo; una nueva mesa exige otra pregunta de diseño
explícita que la ejecución no pueda resolver.

## 9. Contrato candidato que esta mesa deja preparado

1. **Entrada.** Texto de Q, `dominio_consulta` elegido por el usuario y R.
   El dominio documental se fija antes de ofrecer herramientas al
   orquestador; se registra la lista de documentos admitidos en esa consulta.
   El dominio de respuestas se declara aparte al estructurar Q.
2. **Incorporación.** Registrar documento, radicación, pertenencia a dominio,
   unidades, casos locales y datos con condiciones y respaldos. La selección
   pertinente para Q ocurre al consultar. No se exige una identidad global
   entre documentos como requisito de radicación.
3. **Disponibilidad.** `buscar_en_corpus` y las herramientas de lectura están
   ligadas al dominio de la consulta. El código aplica la pertenencia y
   rechaza ids fuera del alcance; el modelo no puede ampliar ese alcance
   cambiando un argumento de búsqueda.
4. **Recuperación.** En la primera versión se puede presentar el inventario
   completo de unidades de ese dominio. El orquestador selecciona las
   pertinentes. Cada unidad elegida entrega texto, datos, condiciones,
   respaldo, documento y radicación. La pertenencia es comprobación mecánica;
   la pertinencia es lectura y juicio.
5. **Identidad.** Mantener los ids locales de los documentos. Cuando Q exige
   reidentificar, anotar qué referencias se vinculan, la evidencia y el
   alcance de esa lectura. Si falta evidencia, dejar la referencia abierta.
   La mesa no fija un formato de persistencia de estas decisiones.
6. **Campo y respuesta.** Registrar unidades elegidas y datos considerados;
   cada posición propuesta tiene su ruta. Los datos mudos permanecen
   distinguibles. A(Q) contiene respuestas, no unidades documentales.
7. **Control y juicio.** El código puede comprobar pertenencia, ids,
   literalidad, forma y operaciones. La aplicabilidad de un dato, su
   pertinencia y el sostén de una respuesta siguen siendo juicios. Jev y el
   mundo se incorporarán en sus fases previstas.
8. **Derivación.** El registro candidato conserva Q, dominio de consulta,
   condiciones, valores de las dependencias, procedencia y cálculo. Aquí se
   prepara el registro en papel; no se introduce un dato en el corpus real.
   Conservar el dominio de origen no decide automáticamente la pertenencia
   del derivado ni su reutilización entre dominios.

Si se dispone avanzar, los puntos afectan E0, E1, E2 y §4.1 del plan del
orquestador. La modificación propuesta reemplaza la exigencia de un índice
global previo por una obligación de reidentificación acreditada cuando Q la
necesite. El plan original permanece intacto hasta esa decisión.

## 10. Estado del paquete

Diseño y referencias preparados antes de ejecutar. **La mesa se ejecutó el
5-10-2026 en comprobación guiada y el registro está cerrado**
(`mesa-dominio-resultado.md`): los seis recorridos cumplen las obligaciones
aplicables, sin aspectos no evaluables, y el cierre deja cuatro obligaciones de
trazabilidad y las precisiones de su «Revisión posterior». La comprobación
editorial del paquete no equivale a una ejecución de la mesa ni a un resultado
del orquestador; una lectura independiente de T1–T6 aportaría evidencia sobre la
claridad del contrato.

Revisión y diseño locales; no se utilizó Exa ni se consultaron fuentes web.
