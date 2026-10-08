# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 08-10-2026. **Fuente única del estado: solo lo que estamos trabajando y lo que
hace falta para trabajarlo.** El detalle de cada ronda vive en el `PLAN.md` de su
proyecto; lo superado, en `historico/`; el vocabulario y los informes sueltos, en
`otros documentos/`; la casa, la actualización de los tres sitios y los reportes, en
`política.md`.

## Dónde quedamos (leer primero)

- **Faro.** El objetivo es un ecosistema de unidades temáticas y datos sobre el que operen
  preguntas y se obtenga información: el cambio en A(Q) al considerar datos conforme a
  reglas. Recuperar no es responder. Detalle en `README.md`, «Visión», y en
  `definiciones-del-marco.md`.
- **Hilo activo: el MVP, `mvp/` — desde cero (08-10).** La estructura está armada y **vacía**:
  `mvp/documentos/` (los documentos que se radican) y `mvp/consulta/` (las baterías
  `preguntas_<doc>.md`) no tienen nada, y la base `mvp/código/corpus.db` no tiene nada inscrito
  (0 documentos · 0 datos). Lo que está listo es **el código y los procedimientos**: en
  `mvp/código/` los dos corredores de la extracción, la inscripción de la base y el orquestador
  (`mvp/código/orq/`, con `R.json`), y en `mvp/prompts/` los tres prompts de trabajo. El diseño y
  lo abierto están en `mvp/consulta-diseno.md`; los procedimientos, en `mvp/guía_UT.md` y
  `mvp/guía_DATOS.md`. **Lo que sigue: radicar el primer documento** —su texto a
  `mvp/documentos/`, su batería a `mvp/consulta/preguntas_<doc>.md` y su inscripción en la
  base— y después correr la consulta.
- **El material anterior quedó archivado en `mvp/temp/`:** los documentos `doc4` y `doc6` con sus
  baterías (`mvp/temp/documentos/`), el texto, la batería y la extracción de `doc7`
  (`mvp/temp/pruebas/` y `mvp/temp/extraccion/`), los crudos de extracción
  (`mvp/temp/extraccion/`) y los registros de las 13 corridas de consulta
  (`mvp/temp/consulta/`). **Nada de eso está inscrito**: el registro arranca limpio y crece solo
  por actos de radicación.
- **La base es el registro, no una vista derivada (08-10).** Se **reseteó**: arranca **vacía** (0
  documentos, 0 datos, 0 casos). Los documentos y los crudos de la extracción siguen en el repo
  (archivados en `mvp/temp/`), pero **no hay nada inscrito** y el catálogo del inscriptor está
  vacío: el primero en entrar será el que se radique. `cargar_corpus.py` dejó de borrar y
  recrear: **inscribe** un documento
  (`python3 mvp/código/cargar_corpus.py <doc>`) —su fila y sus datos— y lo inscrito no se vuelve a
  tocar (en pruebas, `--reinscribir <doc>` es el acto explícito que lo saca y lo vuelve a entrar).
  La **fecha y hora de radicación las pone la base**, en el momento de inscribir
  (`datetime('now','localtime')`). Mientras el registro esté vacío, la consulta no tiene de dónde
  leer; y como todavía no hay preguntas, el ORQ se detiene antes: «no está el archivo de
  preguntas».
- **Prompt 4 (08-10): la sonda de la herramienta de pregunta.** El prompt del agente suma
  `preguntar_al_usuario`: cuando la pregunta **admite dos o más respuestas plausibles**, el
  agente pregunta en vez de inventar. En este MVP **el ciclo termina ahí** (D26): el ORQ registra
  la pregunta en la salida y en el crudo, y no la responde. Es una sonda de **una sola
  hipótesis**: el `ROL`, el `ALCANCE` y el bloque `ESTRUCTURAS JSON DE SALIDA` que se discutieron
  quedaron fuera. Las preguntas que la ponen a prueba son de tres clases —dos referentes→
  preguntar, dato ausente→«no está en los datos», una sola respuesta→responder—; las corridas que
  las ejercitaron (`doc4`, `doc6`) quedaron archivadas en `mvp/temp/consulta/`, sin evaluar.
- **doc7 (08-10).** Documento de divulgación, distinto de `doc4` y `doc6`, con sus cinco preguntas:
  texto, batería (`mvp/temp/pruebas/preguntas_doc7.md`) y extracción completa —6 unidades, 28
  datos— **archivados en `mvp/temp/`**. Es el material listo si se decide que sea el primero en
  radicarse. Se corrieron los dos pasos con los corredores: paso 1, 13 oraciones → 6 unidades,
  **58,3 s**; paso 2 **en tanda** (D27), **24,4 s y 8.759 tokens** contra **52,2 s y 18.481** de a
  una. Los procedimientos quedaron escritos en `mvp/guía_UT.md` y `mvp/guía_DATOS.md`.
- **`unidades/`.** La ronda del paso 2 quedó **cerrada el 06-10** con la entrada
  elegida —**la unidad más las referencias de v9 con sus respaldos**, que aclara sin ampliar y
  conserva las dudas— y con **v9 congelado**. El conteo, rehecho por
  ítem sobre las expectativas registradas: recuperación estricta **95,4 % en desarrollo**
  (agregado DeepSeek + Muse) y **100 % en la reserva** (29/29); fidelidad **98,2 %** en
  desarrollo y **100 %** en la reserva. **La aceptación no se declara demostrada** (un juez, sin
  réplicas, reserva no independiente). El informe, la evaluación por ítem, los crudos y costos, la
  vía utilizable (entrada b, verificación sin API) y los hallazgos de esa ronda quedaron
  **archivados** con el proyecto, fuera de las fuentes vivas.
- **Los prompts de trabajo (07-10).** **Paso 1:** `prompt_UT` (`mvp/prompts/prompt_UT.md`) —agrupa por
  asunto, sin referencias, con los ejemplos homogéneos y el boilerplate al final—; devuelve
  `subtemas` con `subtema` y `oraciones` (sin ids: los pone el código). **Paso 2:**
  `prompt_DATOS` (`mvp/prompts/prompt_DATOS.md`) —recibe **todas las unidades del documento en una
  sola llamada** (tanda) y devuelve, por unidad, `caso` y `datos` (`aspecto · valor · unidad_valor`). El código arma cada unidad
  que recibe el paso 2: `caso` = el `subtema` que devolvió el paso 1, `contenido` = sus oraciones
  unidas en un párrafo y sin numeración. Corridos con Muse: paso 1 sobre `doc5` (v10), `doc4`
  (v10) y `doc2` (v10); paso 2 sobre las cinco unidades de `doc4`, dos réplicas (`r1`, `r2`).
  Los dos prompts quedan **como versiones de trabajo**: no se siguen afinando. **08-10: se quitó el
  campo `dudas` de `prompt_DATOS`** —no lo leía nadie: no entra a la base ni lo ve el agente, y
  aparecía en 2 de 21 unidades—, **el paso 2 pasó a correr por la API** y **después a la tanda**
  (una llamada por documento): en `doc7`, 24,4 s y 8.759 tokens contra 52,2 s y 18.481 de a una
  (D27). El prompt del
  AGENTE ENCARGADO quedó escrito e implementado
  (`mvp/prompts/prompt_ORQ.md`); lo que sigue es cómo se lee su entrega
  (`mvp/consulta-diseno.md`, §9).
- **El MVP: `mvp/`.** Sin índice de casos previo: alcance por dominio y
  reidentificación acreditada al consultar (decisión del 05-10). Las mesas de la forma de
  A(Q), la pieza 1, las pruebas del paso 1 y la ronda cerrada del paso 2 están **archivadas en
  `mvp/temp/`**. La **pieza mecánica** (la conexión pregunta–dominio–corpus) está construida y
  corrida; su diseño, reescrito a lo implementado, en `mvp/consulta-diseno.md`; su estructura y su
  estado, en la primera viñeta. **Sin ejercitar:** el rechazo de un id fuera del dominio (el caso
  de la mesa, un id de RIBERA en una consulta de MONTAÑA).
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
- No se editan los documentos vivos sin aprobación: los seis de la raíz (`README.md`, `AGENTS.md`, `CLAUDE.md`, `política.md`, `definiciones-del-marco.md`, `zettel-vision-operativa.md`), esta memoria (en `mvp/`) y, en `otros documentos/`, el vocabulario de Jev y la política de agentes delegados.
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
  verificación de literales se recompone (`mvp/temp/paso2/comparacion.py verificar-todos`; 69/69 sin
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

- **La entrega se pierde si el ORQ exige más de lo que el prompt pide:** el ORQ pedía que
  **todo** el mensaje final fuera JSON, y prompt 3 pide la prosa (tarea 5) **y** el JSON
  (tarea 6); el agente hizo lo que el prompt manda y el ORQ registró «sin entrega» aunque el
  JSON estuviera a la vista (doc4 q5 r1 y r2; doc6 q2 y q4). **El prompt manda: el ORQ se
  alinea a él**, no al revés.
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

**Orden (08-10).** La estructura quedó armada y **desde cero**: código, prompts y procedimientos
listos; `mvp/documentos/`, `mvp/consulta/` y la base, vacíos. Lo que sigue es **radicar el primer
documento** (punto 0). El material anterior —documentos, baterías, extracción y corridas— está
archivado en `mvp/temp/`.
0. **Radicar el primer documento:** decidir cuál es, poner su texto en `mvp/documentos/`, escribir
   su batería en `mvp/consulta/preguntas_<doc>.md`, extraerlo (paso 1 y paso 2) e inscribirlo
   (`python3 mvp/código/cargar_corpus.py <doc>`); después, correr la consulta y evaluarla con la
   vara de los números de oración, distinguiendo «no está en los datos extraídos» de «el documento
   no lo dice» (`mvp/consulta-diseno.md`, §12). Las baterías de `doc4`/`doc6` están archivadas y
   **sin evaluar**: si se quiere evaluación, o se escribe la lista de expectativas antes de correr,
   o se declara posterior.
1. **El rechazo por dominio, sin ejercitar:** la consulta valida cada id contra los casos del
   dominio y la traza anota el dominio con sus documentos, pero el caso de la mesa —un id de
   RIBERA en una consulta de MONTAÑA— no se ha corrido: el corpus tiene un solo
   dominio (`GENERAL`). El detalle quedó en el cierre de la mesa de dominio.
2. **F6 ejecutada, pendiente de evaluación:** evaluar recuperación y ubicación de condiciones, orden temporal, regresiones, formato y costo, según `unidades/PLAN.md`, sección F6. Hasta entonces no se adopta `ficha_v2`.
3. **Agilidad:** comparar hipótesis de arquitectura, división y modelo/configuración. Vara de Frat: ≈90 % de contenido correcto y ejecución ágil. Falta demostrar el efecto sobre costo total.
4. **Generalización:** medir cualquier candidato prometedor con una reserva nueva e independiente; las observaciones de las rondas no autorizan cambios adicionales por sí solas.
5. **Vínculos de razón entre afirmaciones** («por esa razón», «porque»): niveles 1–2 del grafo de Zettel; fuera de la ficha de datos.
6. **Jev:** identidad de lo registrado, correferencias, omisiones; componente posterior.
7. Grok sin créditos de xAI: recargar si se quiere compararlo.
8. **Unidad temática con el eje de `v1`** (decisión de Frat, 02-10; registrada en `definiciones-del-marco.md`, parte B). Los prompts de trabajo (`prompt_UT` y `prompt_DATOS`) producen la unidad con el eje en el asunto: el `subtema` **nombra el núcleo** —el caso de la unidad— y las oraciones que lo desarrollan van juntas. Falta **declarar los satélites**, los casos de los que el texto habla por su relación con el núcleo, que hoy se leen de las relaciones y acciones. Discutirlo antes de escribirlo.
9. **Adoptar el candidato del paso 2:** `mvp/temp/paso2/prompt_ficha_contexto.md` vive hoy en la carpeta de trabajo; si se adopta, le toca su sitio en `mvp/prompts/` con nombre propio, sin mezclarlo con `ficha_v2`.
10. **Cerrar la forma del dato del paso 2:** si vuelven el `sostiene` (quién lo sostiene) y el `respaldo` (la ruta al fragmento), y si `unidad_valor` se queda como campo propio o la unidad va dentro del valor. Hoy el dato viaja sin fuente ni ruta.

**Cerrado el 08-10: alineación con prompt 3.** El ORQ ubica el JSON del mensaje final donde
prompt 3 lo ponga (`orq/leer_entrega.py`; `entrega.forma` en `config.json`, que el ORQ valida) y
la relectura de los crudos guardados deja los 13 con desenlace, sin volver a llamar al modelo.
En el mismo tramo: el tope de herramientas se respeta de verdad, la causa del corte queda
registrada, la traza ya no revienta con un JSON que no sea objeto y la salida no confunde «no
hubo JSON» con «se cortó».
