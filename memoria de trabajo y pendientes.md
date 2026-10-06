# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 06-10-2026. **Fuente única del estado: solo lo que estamos trabajando y lo que
hace falta para trabajarlo.** El detalle de cada ronda vive en el `PLAN.md` de su
proyecto; lo superado, en `historico/`; el vocabulario y los informes sueltos, en
`otros documentos/`; la casa, la actualización de los tres sitios y los reportes, en
`política.md`.

## Dónde quedamos (leer primero)

- **Faro.** El objetivo es un ecosistema de unidades temáticas y datos sobre el que operen
  preguntas y se obtenga información: el cambio en A(Q) al considerar datos conforme a
  reglas. Recuperar no es responder. Detalle en `README.md`, «Visión», y en
  `definiciones-del-marco.md`.
- **Hilo activo: `unidades/`.** Paso 1 (unidades temáticas) con **v9 congelado**; paso 2
  (datos por unidad) con la entrada elegida y **base provisional de trabajo: la unidad más
  las referencias de v9 con sus respaldos**, que aclara sin ampliar y conserva las dudas.
  La ronda quedó **cerrada el 06-10** con el conteo rehecho por ítem sobre las expectativas
  registradas: recuperación estricta **95,4 % en desarrollo** (agregado DeepSeek + Muse) y
  **100 % en la reserva** (29/29); fidelidad **98,2 %** en desarrollo y **100 %** en la
  reserva. **La aceptación no se declara demostrada** (un juez, sin réplicas, reserva no
  independiente). Informe en `mvp/paso2/informe_paso2.md`; evaluación por ítem en
  `mvp/paso2/evaluacion_items.md`; crudos, tareas y costos en
  `mvp/paso2/inventario_y_costos.md`; la vía utilizable (entrada b, verificación sin API) en
  `mvp/paso2/README.md`; qué enseña, en `mvp/paso2/hallazgos.md`.
- **Hilo del MVP: `mvp/`.** Plan candidato del orquestador —sin índice de casos previo:
  alcance por dominio y reidentificación acreditada al consultar (decisión del 05-10)— y su
  **pieza mecánica** (la conexión mecánica pregunta–dominio–corpus), que es lo siguiente
  ejecutable y aún no está iniciada. Las mesas de la forma de A(Q) y la
  pieza 1 están cerradas y registradas en sus carpetas. El diseño de esa primera consulta
  está escrito en `mvp/consulta-diseno.md` (**borrador**) y queda **pendiente de revisión
  por Claude y Astra**; no está implementado.
- **La ficha.** `ficha_v1` está congelada y es la base del paso 2; en F5 midió 60/63 dentro
  de su contrato. F6 se ejecutó y sigue sin evaluar. Detalle en `unidades/PLAN.md`.

## 0. Dónde y cómo

- **Carpeta:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/` (Linux, máquina
  de Frat). **Repositorio:** `https://github.com/frquintero/jev-typesafe-spike`, rama
  `main`; los commits se suben al upstream en el mismo tramo (`política.md` §3).
- **Continuidad en nube:** ChatGPT Work trabaja desde una copia del repositorio público; lo
  publicado permite recuperar el trabajo con el PC apagado. Las claves viven en el
  `~/.bashrc` del PC y no se transfieren.
- **Roles:** Frat y Cowork planean; el trabajo lo hacen los agentes, y **delega el modelo
  que Frat designe como ORQUESTADOR** (`AGENTS.md`, «Agentes delegados»). El rol va con la
  tarea, no con el modelo.
- **Flujo de una ronda:** se discute y se conjetura; se corre solo si hay conjetura nueva;
  se escribe el prompt y la sección del `PLAN.md`; el ejecutor corre, reporta sin veredicto
  y hace commit y push de los crudos; Cowork los evalúa contra la conjetura y Frat decide.
- **Aviso de fin de tarea: ntfy (obligatorio).** Los envoltorios publican al terminar en el
  tema de `~/.config/dsh_tarea/ntfy_topic`; el ORQUESTADOR escucha ese tema o arma el
  Monitor de Claude. **Nada de `sleep` ni de sondear el repo.** Procedimiento, y la
  excepción de Codex: `otros documentos/agentes-delegados.md` §3.
- **Git:** Cowork lo hace con Desktop Commander, no con el shell aislado. Para detener
  procesos, `kill_process`.

## 1. Reglas de trabajo

- **Ockham:** empezar con lo que funciona. Cada elemento del prompt tiene que servir a la tarea; quitar lo que no se use.
- **Una cosa por ronda.** Varios cambios solo si aplican un mismo principio.
- **Planificar** es pensar y conjeturar; no se ofrecen corridas por reflejo.
- **No reinventar la rueda:** revisar la literatura antes de diseñar.
- **Mostrar el prompt antes de correr** y esperar el «adelante».
- **Sin ejemplos tomados de los documentos de prueba** (invalidan la prueba).
- No se editan los documentos vivos sin aprobación: los siete de la raíz (`README.md`, `AGENTS.md`, `CLAUDE.md`, esta memoria, `política.md`, `definiciones-del-marco.md`, `zettel-vision-operativa.md`) y, en `otros documentos/`, el vocabulario de Jev y la política de agentes delegados.
- **Crítica constructiva:** valorar la propuesta de Frat y mejorarla con razones, sin aceptar todo.
- **Generalizar, no particularizar (directriz de Frat, 01-10):** todo cambio al prompt se piensa para documentos de contenido general (divulgación, ensayo no especializado, opinión), no para resolver los textos de prueba. No se afina sobre textos de desarrollo; lo que mide es una reserva escrita por otro, con preguntas fijadas antes.

## 2. Lecciones vigentes

- **Leer el `reasoning_content` antes de proponer cambios:** localiza la causa (DeepSeek lo entrega entero; el de Grok no se puede leer).
- **Una sola corrida no separa el efecto del ruido;** con el mismo prompt el resultado puede variar tanto como el efecto buscado. Réplicas, y comparar prompts con el mismo `rN`.
- **No afinar sobre textos de desarrollo;** medir en una reserva escrita por otro, con preguntas fijadas antes. Un texto escrito por quien diseña el prompt sobreestima el acierto.
- **Un ejemplo enseña exactamente lo que muestra:** una lista vacía no enseña nada; un ejemplo tomado del texto de prueba enseña cautela justo en ese caso. Los ejemplos se eligen desde el marco, no desde las fallas.
- **Si dos señales del prompt se contradicen, el modelo oscila y delibera** (cuesta tokens). Remedio: un solo principio. Referencia implícita con un solo antecedente ≠ ambigüedad.
- **Cada «no va aquí» necesita un «va allá»;** una lista o campo sin forma declarada se inventa distinto en cada réplica; un campo obligatorio no filtra.
- **Un contrato más explícito estabiliza la forma pero no abarata:** abre decisiones nuevas (en qué lista va cada hecho) y el modelo registra más.
- **El género pesa más que el modelo:** un prompt preciso en un género puede no serlo en otro; probar siempre en varios géneros.
- **Al modelo el juicio, al código el cómputo:** numerar oraciones y verificar literalidad lo hace el código.
- **Cada ítem que se espera recuperar prueba una sola cosa** (contenido, identidad externa, condición o duda) y hay que poder señalar el registro que lo satisface: mezclarlos infla los porcentajes.
- **Lo que un paso no registra no llega al siguiente:** el paso 2 solo usa el contexto que el paso 1 le entrega.
- **Jev es posterior:** subtemas, inventario global y Jev siguen fuera de las pruebas del núcleo. La detección o recuperación posterior de omisiones no se ha probado aquí.
- **Operativo:** DeepSeek solo tiene razonamiento `high` y `max` (nuestro `low` se vuelve `high`); puede dejar el stream colgado (si pasa un minuto sin bytes, relanzar).

**Verificadas en el cierre del paso 2 (06-10).**

- **Una lista de ítems que no se registra no se puede auditar después:** el conteo se rehace
  solo sobre las expectativas escritas y guardadas antes de llamar; la lista fina que no se
  registró hubo que retirarla.
- **El conteo por ítem necesita tres estados:** cumple · parcial · no, y las expectativas
  defectuosas aparte; los parciales no suman a la recuperación.
- **Tiempo de tarea ≠ tiempo del modelo:** el envoltorio de Muse incluye arranque y reintentos
  (una tarea de 2 646 s traía un timeout de transporte de 47 s); esa duración no se atribuye al
  razonamiento, y si no es reconstruible se dice.
- **`reasoning_tokens` viene dentro de `completion_tokens`:** no se suma dos veces.
- **Los crudos tienen que permitir re-verificar sin API:** con el material enviado guardado, la
  verificación de literales se recompone (`mvp/paso2/comparacion.py verificar-todos`; 69/69 sin
  diferencias al 06-10).

## 3. Pendientes vigentes

**Orden (06-10):** el paso 2 quedó **cerrado** (entrada (b) como base provisional; ver «Dónde
quedamos»). **Lo siguiente es la conexión mecánica pregunta–dominio–corpus:** fijar el alcance
documental, recuperar unidades completas con sus datos y referencias y preparar la entrada del
orquestador; su primera comprobación es local, sin LLM, con los materiales existentes, y **antes
de implementarla hay que cotejar ese alcance con el plan vigente** (`mvp/orquestador-plan.md`,
F0). No está iniciada. **El diseño de esa primera consulta está en `mvp/consulta-diseno.md`;
lo revisan Claude y Astra antes de implementar.**

0. **Conexión mecánica pregunta–dominio–corpus (trabajo de ahora):** fijar el `dominio_consulta`
   de una pregunta, rechazar los ids fuera de alcance, recuperar la unidad completa (texto,
   datos, condiciones, respaldo, documento y radicación) y registrar los documentos admitidos;
   sin LLM y sin Jev, reutilizando `mvp/pieza1/pieza1.py` y las entradas de la mesa de dominio.
   Termina cuando, sobre las entradas de la mesa, un id de RIBERA en una consulta de MONTAÑA se
   rechaza por fuera de alcance, `M1:U1` devuelve `M1:S1–S4` y `M1:D1–M1:D3` completos, y la
   corrida anota `dominio_consulta: MONTAÑA` con su lista de documentos. **Antes de escribir
   código: revisión del diseño (`mvp/consulta-diseno.md`) por Claude y Astra, cotejo con el
   plan vigente y mostrar el plan.** Detalle en `mvp/mesa-dominio-resultado.md`, cierre; el
   plan del orquestador, en `mvp/orquestador-plan.md`.
1. **F6 ejecutada, pendiente de evaluación:** evaluar recuperación y ubicación de condiciones, orden temporal, regresiones, formato y costo, según `unidades/PLAN.md`, sección F6. Hasta entonces no se adopta `ficha_v2`.
2. **Agilidad:** comparar hipótesis de arquitectura, división y modelo/configuración. Vara de Frat: ≈90 % de contenido correcto y ejecución ágil. Falta demostrar el efecto sobre costo total.
3. **Generalización:** medir cualquier candidato prometedor con una reserva nueva e independiente; las observaciones de las rondas no autorizan cambios adicionales por sí solas.
4. **Vínculos de razón entre afirmaciones** («por esa razón», «porque»): niveles 1–2 del grafo de Zettel; fuera de la ficha de datos.
5. **Jev:** identidad de lo registrado, correferencias, omisiones; componente posterior.
6. Grok sin créditos de xAI: recargar si se quiere compararlo.
7. **Unidad temática con el eje de `v1`** (decisión de Frat, 02-10; registrada en `definiciones-del-marco.md`, parte B). El prompt vigente de `unidades/extraer_unidades.py` sigue siendo `unidades_v5`, con eje en el asunto; en pruebas está **v9**, que no cambia el eje sino la resolución de referencias externas. Falta un prompt que combine el eje de `v1` (núcleo, satélites y todas las oraciones que se refieren a ellos; el caso se reidentifica aunque se lo nombre de varias maneras) con la mecánica de `v5` (el código numera las oraciones). Discutirlo antes de escribirlo.
8. **Adoptar el candidato del paso 2:** `mvp/paso2/prompt_ficha_contexto.md` vive hoy en la carpeta de trabajo; si se adopta, le toca su sitio en `unidades/prompts/` con nombre propio, sin mezclarlo con `ficha_v2`.
