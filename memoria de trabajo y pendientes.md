# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 07-10-2026. **Fuente única del estado: solo lo que estamos trabajando y lo que
hace falta para trabajarlo.** El detalle de cada ronda vive en el `PLAN.md` de su
proyecto; lo superado, en `historico/`; el vocabulario y los informes sueltos, en
`otros documentos/`; la casa, la actualización de los tres sitios y los reportes, en
`política.md`.

## Dónde quedamos (leer primero)

- **Faro.** El objetivo es un ecosistema de unidades temáticas y datos sobre el que operen
  preguntas y se obtenga información: el cambio en A(Q) al considerar datos conforme a
  reglas. Recuperar no es responder. Detalle en `README.md`, «Visión», y en
  `definiciones-del-marco.md`.
- **Hilo activo: `mvp/corpus/` (07-10).** La **consulta completa de Zettel** quedó construida
  y corrida: `doc4` y `doc6` radicados con su sello, extracción con `prompt_v10` +
  `prompt_datos_v1`, base SQLite (59 datos, 19 casos), orquestador por pasos
  (`mvp/corpus/consulta/orq/`) y **13 corridas** (doc4 q1–q5 y réplicas de q1, q2 y q5;
  doc6 q1–q5). Ocho entregaron respuesta; **cinco quedaron «sin JSON leído»** (doc4 q4,
  q5 r1, q5 r2; doc6 q2, q4). Lo construido, los huecos y lo abierto están en
  `mvp/consulta-diseno.md`; **lo que sigue: leer el JSON de entrega (§9) y evaluar las
  respuestas (§12).**
- **`unidades/`.** La ronda del paso 2 quedó **cerrada el 06-10** con la entrada
  elegida —**la unidad más las referencias de v9 con sus respaldos**, que aclara sin ampliar y
  conserva las dudas— y con **v9 congelado** (`mvp/pruebas/prompt_v9.md`). El conteo, rehecho por
  ítem sobre las expectativas registradas: recuperación estricta **95,4 % en desarrollo**
  (agregado DeepSeek + Muse) y **100 % en la reserva** (29/29); fidelidad **98,2 %** en
  desarrollo y **100 %** en la reserva. **La aceptación no se declara demostrada** (un juez, sin
  réplicas, reserva no independiente). Informe en `mvp/paso2/informe_paso2.md`; evaluación por
  ítem en `mvp/paso2/evaluacion_items.md`; crudos, tareas y costos en
  `mvp/paso2/inventario_y_costos.md`; la vía utilizable (entrada b, verificación sin API) en
  `mvp/paso2/README.md`; qué enseña, en `mvp/paso2/hallazgos.md`.
- **Los prompts de trabajo (07-10).** **Paso 1:** `mvp/pruebas/prompt_v10.md` —agrupa por
  asunto, sin referencias, con los ejemplos homogéneos y el boilerplate al final—; devuelve
  `subtemas` con `subtema` y `oraciones` (sin ids: los pone el código). **Paso 2:**
  `mvp/pruebas/prompt_datos_v1.md` —recibe **una unidad por turno** y devuelve los datos de esa
  unidad: `caso`, `datos` (`aspecto · valor · unidad_valor`) y `dudas`. El código arma la unidad
  que recibe el paso 2: `caso` = el `subtema` que devolvió el paso 1, `contenido` = sus oraciones
  unidas en un párrafo y sin numeración. Corridos con Muse: paso 1 sobre `doc5` (v10), `doc4`
  (v10) y `doc2` (v10); paso 2 sobre las cinco unidades de `doc4`, dos réplicas (`r1`, `r2`).
  Los dos prompts quedan **como versiones de trabajo**: no se siguen afinando. El prompt del
  AGENTE ENCARGADO quedó escrito e implementado
  (`mvp/corpus/consulta/orq/prompt_agente.md`); lo que sigue es cómo se lee su entrega
  (`mvp/consulta-diseno.md`, §9).
- **El MVP: `mvp/`.** Sin índice de casos previo: alcance por dominio y
  reidentificación acreditada al consultar (decisión del 05-10). Las mesas de la forma de
  A(Q) y la pieza 1 están cerradas y registradas en sus carpetas. La **pieza mecánica** (la
  conexión pregunta–dominio–corpus) quedó construida y corrida el 07-10 (`mvp/corpus/`); su
  diseño, reescrito a lo implementado, está en `mvp/consulta-diseno.md`. **Sin ejercitar:**
  el rechazo de un id fuera del dominio (el caso de la mesa, un id de RIBERA en una consulta
  de MONTAÑA).
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

**Verificadas con los prompts de trabajo (07-10).**

- **Manda el ejemplo, no la regla.** Los aspectos salían como preguntas —«quién anunció el
  corte», «qué pidió», «cuándo será el corte»— porque los ejemplos del prompt los mostraban así;
  corregidos los ejemplos a nombres («anunciante del corte», «fecha del corte»), salieron nombres.
- **El corte del paso 1 no es contiguo.** Una unidad puede contener oraciones posteriores a las
  de la unidad siguiente (`doc4`: `[8, 9, 10, 13–17]` antes de `[11, 12]`; `doc2`:
  `[4–7, 13–17]` antes de `[8–12]`). El código numera por el orden del arreglo, así que el id no
  indica orden de lectura: no suponer contigüidad ni «U4 antes que U5 en el texto».
- **El paso 1 agrupa más grueso que antes:** con el mismo texto, 4 unidades contra 7 de `v8` en
  `doc2`, y 5 contra 6 en `doc4`, con una unidad de ocho oraciones. Los nombres se vuelven
  enumeraciones largas cuando la unidad crece.
- **Un ejemplo tomado de una unidad contamina esa unidad:** `doc4:U5` salió idéntico al ejemplo
  del paso 2, en las dos réplicas. La regla «sin ejemplos de los documentos de prueba» es, en
  rigor, **por unidad**: si el ejemplo sale del mismo texto, esa unidad queda fuera del juicio.
- **`unidad_valor` se usa poco:** solo hay magnitud medida en 2 de los 14 datos de `doc5` y en 9
  de los 26 de `doc4`; en el resto el valor es un nombre, una fecha, un carácter o un conteo.
- **La atribución no tiene dónde ir:** la versión de trabajo del paso 2 no registra quién
  sostiene un dato, y el modelo lo resolvió solo —partiéndolo en «quién dijo» y «qué dijo», o
  metiendo la fuente en el aspecto («afectados por el corte» con el «según la empresa» perdido)—.

**Verificadas con la consulta (07-10).**

- **La entrega se pierde si no empieza con `{`:** con la entrega por mensaje final, el
  agente envolvió el JSON en una cerca o lo puso detrás de la prosa, y el ORQ lo registró
  «sin entrega» aunque la respuesta esté ahí (doc4 q5 r1 y r2; doc6 q2 y q4). Las tres
  respuestas que empiezan con `{` sí se leyeron.
- **Corridas de una misma tabla pueden venir de versiones distintas del código:** las seis
  primeras de `doc4` entregaban con la herramienta `entregar` (su crudo trae `datos` y
  `reporte`); de esas seis, doc4 q4 —la única sin desenlace— escribió el JSON como texto y
  no llamó la herramienta. El campo `herramientas` del crudo dice con cuál se hizo cada una.
- **El agente nunca pidió todos los casos:** filtra por el umbral del 80 % sobre el nombre
  del caso (leyó de 1 a 4 de los 19); un aspecto que el nombre no anuncia no lo mira
  (`consulta-diseno.md`, §8).
- **Repite lecturas y no hay corte por ciclo:** `doc6` q2 pidió `doc6:U4` dos veces y gastó
  6 turnos y 5 llamadas; la guardia corta por número de turnos y de llamadas, no por
  repetición (`consulta-diseno.md`, §11, D25).

## 3. Pendientes vigentes

**Orden (07-10).** La **conexión mecánica pregunta–dominio–corpus** quedó construida y corrida
(ver «Dónde quedamos»): base, orquestador y dos baterías de preguntas. Lo que sigue, en este
orden: **leer el JSON de entrega** (punto 0) y **evaluar las respuestas** (punto 1). La
extracción está fijada (`prompt_v10`, `prompt_datos_v1`) y el diseño vigente, en
`mvp/consulta-diseno.md`.

0. **Leer el JSON de entrega (trabajo de ahora):** hoy el ORQ exige que el mensaje final
   empiece con `{`, y pierde la entrega cuando viene con prosa o cerca de código: cuatro
   corridas con la entrega actual (doc4 q5 r1 y r2; doc6 q2 y q4) más doc4 q4, que escribió
   el JSON como texto en vez de llamar la herramienta `entregar` del mecanismo viejo.
   Termina cuando las cinco quedan con su desenlace leído **sin volver a llamar al modelo**
   (los crudos ya traen la respuesta). Dos vías, sin decidir: extraer el primer `{…}` bien
   formado en el ORQ, o exigir en el prompt que el mensaje final sea solo el JSON
   (`mvp/consulta-diseno.md`, §9).
1. **Evaluar las respuestas de la consulta (07-10):** juzgar las 13 corridas contra lo que el
   documento establece, con la vara de los números de oración y distinguiendo «no está en los
   datos extraídos» de «el documento no lo dice» (`mvp/consulta-diseno.md`, §12). **No hay
   lista de expectativas por pregunta guardada antes de correr** (ni de doc4 ni de doc6): la
   evaluación tiene que decirlo así, o escribirla y marcarla como posterior.
2. **El rechazo por dominio, sin ejercitar:** la consulta valida cada id contra los casos del
   dominio y la traza anota el dominio con sus documentos, pero el caso de la mesa —un id de
   RIBERA en una consulta de MONTAÑA— no se ha corrido: el corpus radicado tiene un solo
   dominio (`GENERAL`). Antes era el punto 0; el detalle, en `mvp/mesa-dominio-resultado.md`,
   cierre.
3. **F6 ejecutada, pendiente de evaluación:** evaluar recuperación y ubicación de condiciones, orden temporal, regresiones, formato y costo, según `unidades/PLAN.md`, sección F6. Hasta entonces no se adopta `ficha_v2`.
4. **Agilidad:** comparar hipótesis de arquitectura, división y modelo/configuración. Vara de Frat: ≈90 % de contenido correcto y ejecución ágil. Falta demostrar el efecto sobre costo total.
5. **Generalización:** medir cualquier candidato prometedor con una reserva nueva e independiente; las observaciones de las rondas no autorizan cambios adicionales por sí solas.
6. **Vínculos de razón entre afirmaciones** («por esa razón», «porque»): niveles 1–2 del grafo de Zettel; fuera de la ficha de datos.
7. **Jev:** identidad de lo registrado, correferencias, omisiones; componente posterior.
8. Grok sin créditos de xAI: recargar si se quiere compararlo.
9. **Unidad temática con el eje de `v1`** (decisión de Frat, 02-10; registrada en `definiciones-del-marco.md`, parte B). Los prompts de trabajo (`prompt_v10` y `prompt_datos_v1`) producen la unidad con el eje en el asunto: el `subtema` **nombra el núcleo** —el caso de la unidad— y las oraciones que lo desarrollan van juntas. Falta **declarar los satélites**, los casos de los que el texto habla por su relación con el núcleo, que hoy se leen de las relaciones y acciones. Discutirlo antes de escribirlo.
10. **Adoptar el candidato del paso 2:** `mvp/paso2/prompt_ficha_contexto.md` vive hoy en la carpeta de trabajo; si se adopta, le toca su sitio en `unidades/prompts/` con nombre propio, sin mezclarlo con `ficha_v2`.
11. **Cerrar la forma del dato del paso 2:** si vuelven el `sostiene` (quién lo sostiene) y el `respaldo` (la ruta al fragmento), y si `unidad_valor` se queda como campo propio o la unidad va dentro del valor. Hoy el dato viaja sin fuente ni ruta.
