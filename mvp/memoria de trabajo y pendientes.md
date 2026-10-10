# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 09-10-2026. **Fuente única del estado: solo lo que estamos trabajando y lo que
hace falta para trabajarlo.** El detalle de cada ronda vive en el `PLAN.md` de su
proyecto; lo superado, en `historico/`; el vocabulario y los informes sueltos, en
`otros documentos/`; la casa, la actualización de los tres sitios y los reportes, en
`política.md`.

## Dónde quedamos (leer primero)

- **Faro.** El objetivo es un ecosistema de unidades temáticas y datos sobre el que operen
  preguntas y se obtenga información: el cambio en A(Q) al considerar datos conforme a
  reglas. Recuperar no es responder. Detalle en `README.md`, «Visión», y en
  `definiciones-del-marco.md`.
- **Hilo activo: el MVP, `mvp/` — la base es el centro.** El código está en `mvp/código/`:
  `radicar.py` (radica el documento), `paso1_unidades.py` (UT), `paso2_datos.py` (DATOS), `base.py`
  (la base y su esquema), `mensajes.py` (parte el prompt en los dos mensajes), `proveedores/` (el
  transporte) y el orquestador (`orq/`, con `R.json`); los tres prompts de trabajo, en
  `mvp/prompts/`, cada uno en dos bloques: `[SISTEMA]` lo invariante y `[TAREA]` el material, que es
  lo que los actos mandan como `system` y como `user`. **El documento de trabajo es `preparación del
  café`** —las tres dinámicas de extracción—, **radicado el 09-10 23:33:31** (dominio `GENERAL`,
  sello `e00deb25…`) y **con UT hecha: 5 unidades, 0 datos** (`deepseek` `low`, 13,5 s, prompt
  `prompt_UT` con hash `d82a9bbb…`). El 09-10 la base se **reseteó dos veces** (se borró `corpus.db`
  y volvió a nacer con el esquema) para arrancar de cero con este documento; **`doc11` —«La anemia
  falciforme»— quedó fuera de la base**, aunque su texto sigue en `mvp/documentos/`: re-radicarlo lo
  devuelve con el mismo sello. Cada etapa es un acto aparte y a mano —DATOS, la batería en
  `mvp/consulta/preguntas_preparación del café.md` y la consulta—. El diseño y lo abierto están en
  `mvp/consulta-diseno.md`; los procedimientos, en `mvp/guía_UT.md` y `mvp/guía_DATOS.md`.
- **`mvp/temp/` es el archivo: no se corre desde ahí, no se lee, no se escribe.** Ahí quedaron los
  documentos `doc4` y `doc6` con sus baterías (`mvp/temp/documentos/`), el texto, la batería y la
  extracción de `doc7` (`mvp/temp/pruebas/` y `mvp/temp/extraccion/`), los crudos de las trece
  corridas de consulta y su medición (`mvp/temp/consulta/`). Nada de eso está radicado.
- **La base es el centro de datos (08-10).** `mvp/código/corpus.db` **es** la fuente: no se
  regenera, y **no hay archivos intermedios**. Se escribe con **actos manuales y separados**:
  **radicar** (`python3 mvp/código/radicar.py <doc>`) pone la fila del documento —nombre, dominio,
  ubicación y **la fecha y la hora que pone la base**—; **UT** (`paso1_unidades.py`) escribe su
  corrida y las **unidades** —el caso y los números de oración—; **DATOS** (`paso2_datos.py`)
  escribe su corrida y los **datos**; y la **consulta** (`orq/registrar_consulta.py`) escribe su
  corrida y la respuesta (`consultas` + `consulta_casos`). **Una corrida se escribe al terminar y
  una sola vez**: queda `exitoso`, o `fallido` con su motivo, y **narra la extracción que está en la
  base** —un reintento fallido no pisa la cita de lo que sigue ahí—. **Todo o nada, en una sola
  transacción**: si la llamada falla, si la respuesta se cortó o si el JSON no se pudo leer, no se
  escribe salida y la corrida queda `fallida` con su motivo (lo que volvió, recortado a la cabeza y
  la cola); y si el intento era un `--rehacer`, **lo anterior vuelve**. La fila del documento no se
  toca nunca: un documento radicado no se mueve (en pruebas, `radicar.py --rehacer <doc>`). El
  **sello** es el guardián del texto. La base **impone sus contratos** (`paso`, `estado`, `motivo`
  si falló, un `n` por documento, y las claves foráneas). **Lo que se lee son solo entradas**: el
  documento radicado, los prompts, R y la batería. **Cuánto hay radicado hoy, en la primera viñeta**
  —no se repite acá—. Las tablas se reconstruyeron el 08-10 para imponer los contratos, con la
  radicación intacta (misma fecha y sello), y el esquema quedó igual a su DDL en
  `mvp/consulta-diseno.md`.
- **Las particiones, probadas fuera de la base (08-10).** En el scratch `temp/ut-haiku/` —**sin
  versionar y sin tocar la base**— un corredor llama a `proveedores.llamar` con el mismo prompt, el
  mismo documento y la misma verificación que el acto real, y guarda su JSON; otro compara
  particiones oración por oración. **`doc8`: seis corridas, seis particiones distintas** —DeepSeek
  `low` ×2 (48-53 s, ~10.500 tokens de salida) y Haiku `high` ×4 (12-22 s, 2.400-3.000)—.
  Coinciden en 1-4, 11-13 y 18 —y 9-10 en 5 de 6—, y **titubean siempre en los mismos dos cortes**:
  si la explosión del Cámbrico (5) y la conquista de la tierra firme (6-8) son uno o dos asuntos, y
  si los arrecifes (17) entran en el cambio del mar (14-16). La cola unida la dieron Haiku y
  DeepSeek, y la separada también los dos: **la partición no la decide el modelo, la decide la
  tirada**. Con un ejemplo que **es** el documento, los dos modelos **transcriben** el ejemplo (6,1 s
  y 6,7 s, nombres incluidos); con un documento nuevo —`doc333`, inventado en `temp/`: la Segunda
  Guerra Mundial, tres párrafos, 14 oraciones con valores y unidades— **deciden otra vez** y no
  coinciden: Haiku 6 unidades en 22,3 s, DeepSeek 8 en 45,9 s. Los detalles, en `temp/ut-haiku/`
  (`comparacion-doc8.md`, `comparacion-doc333.md`, un JSON por corrida).
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
- **Los prompts de trabajo (07-10).** **Paso 1:** `prompt_UT` (`mvp/prompts/prompt_UT.md`) —el 09-10
  se **reemplazó por `v1`**: cinco definiciones (el subtema como oraciones correlacionadas con una
  idea, el nombre como frase que describe el contenido), **dos ejemplos** —un texto marino de seis
  oraciones y `doc9` entero en once unidades— y **sin la sección de `REFERENCIAS EXTERNAS`**—;
  devuelve `subtemas` con `subtema` y `oraciones` (sin ids: los pone el código). **Paso 2:**
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
  y hace commit y push (en el MVP, de la base); Cowork evalúa contra la conjetura y Frat decide.
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
- **Operativo:** DeepSeek declara `low`, `high` y `max`, con `high` por defecto, así que el `low` que
  mandamos es un escalón declarado, no un alias de `high` (corregido el 08-10); en las líneas viejas,
  que usan streaming, puede dejar el stream colgado (si pasa un minuto sin bytes, relanzar).

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
- **La base y el documento tienen que permitir re-verificar sin API:** con lo producido en la base
  y el texto radicado (y el prompt en `mvp/prompts/`), la
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

**Verificadas con las pruebas de partición (08-10).**

- **La partición no la decide el modelo, la decide la tirada.** Seis corridas de `doc8` con dos
  modelos dieron seis particiones distintas; las dos formas de la cola 14-17 aparecieron en los dos
  modelos. Donde el texto no deja dudas la distribución está picuda —1-4, 11-13, 18— y todas las
  corridas coinciden; donde admite dos lecturas, la tirada elige. Y no hay perilla: **con el
  pensamiento encendido, Anthropic exige `temperature` 1 —y en los Claude 5 la deprecó— y DeepSeek la
  ignora**; temperatura 0 tampoco sería determinista (variaciones medidas de hasta 15 % entre
  corridas idénticas, por la invariancia por lote del servidor). Lo que el registro hace es **fijar
  la tirada**: la unidad inscrita no se mueve, y la corrida guarda con qué modelo, esfuerzo y prompt
  salió.
- **El ejemplo manda, pero no reemplaza la decisión.** Un ejemplo tomado del documento que se analiza
  se transcribe literal —los dos modelos, nombres incluidos, y con la mitad del pensamiento—; con un
  documento nuevo el mismo ejemplo **no** evita que el modelo decida, y lo que enseña es la **forma**:
  agrupar por asunto a través de párrafos y con oraciones no contiguas, y nombrar diciendo qué se
  dice.
- **`max`, con el techo de 16.384, se lo come el pensamiento.** Haiku en `max` gastó los 16.384
  tokens en pensar y devolvió la respuesta **vacía** (`finish_reason: length`); el modelo aguanta
  hasta 128.000. El corredor real lo habría registrado **fallido** por el corte; el del scratch
  guardó el JSON vacío, sin marcarlo.
- **El costo sí separa a los modelos; la partición, no.** En `doc8`, Haiku `high` tardó 12-22 s y
  gastó 2.400-3.000 tokens de salida contra 48-53 s y ~10.500 de DeepSeek `low`; en `doc333`, 22,3 s
  y 4.332 contra 45,9 s, 10.227 y **35.782 caracteres de razonamiento** (nueve veces el de Haiku).

**Verificadas con la revisión de los prompts y de la base (09-10).**

- **Las reglas pueden viajar dentro de los ejemplos.** Al reemplazar los ejemplos de un prompt se
  recortan reglas sin verlo: la sección `REFERENCIAS EXTERNAS` de `prompt_UT` quedó como definición
  suelta al pasar al ejemplo único, y un modelo lo dijo con esas palabras —«seems to just be
  definitional context»—; el costo se vio en `doc11`, donde el nombre de la unidad no citó el
  antecedente y el paso 2 tuvo que agregarlo entre paréntesis. Antes de recortar ejemplos, revisar
  qué más cargaban.
- **Un chequeo de forma no juzga contenido.** `forma()` **decide** (claves de más, posiciones, tipos)
  y **avisa** (dónde va la unidad de medida, que es redacción). Lo que decide es la forma y la
  consistencia; lo que se juzga, se reporta. Con eso, 41 de los 42 crudos guardados pasan y el que
  falla falla por lo que debe: devolvió cinco unidades donde se enviaron seis.
- **Una partición rota no se inscribe.** Huecos, solapes, números fuera de rango o no enteros hacen
  fallar UT, como DATOS es todo o nada. Distinto es una partición que cubre todo y agrupa distinto:
  eso es una lectura, y ahí el acto no opina.
- **Los totales de tokens de Anthropic con caché son la suma de tres campos** (`input_tokens` solo
  cuenta lo que va después del corte): con `cache_control`, `input_tokens` + `cache_creation` +
  `cache_read`. Si no, la corrida registra menos entrada de la real.

**Verificadas con el prompt v1 de UT (09-10).**

- **El ejemplo enseña por masa, y también con lo que omite.** La primera versión de `v1` —con la
  sección `REFERENCIAS EXTERNAS` y sus dos casos— nombró las unidades citando el antecedente en
  **19 de 20** nombres (DeepSeek `low`: 7/8, 6/6, 6/6; Haiku `low`: 5/5). La misma versión, ya sin
  esa sección y con los ejemplos rehechos, citó **4 de 27** (1/7, 2/10, 1/10), y el prompt anterior
  citaba 2 de 7. La deliberación acompaña: 5.385-8.768 tokens de pensamiento con la regla,
  1.151-3.012 sin ella. Son tres corridas por versión, con los ejemplos cambiados a la vez que la
  sección: **señala, no prueba**.
- **La granularidad del ejemplo sí se traslada** (corrige lo dicho el 09-10 con el ejemplo grueso).
  Con el ejemplo de once unidades —seis de ellas de una sola oración— las particiones de `doc11`
  pasaron de 6-8 unidades a 7, 10 y 10, y el acuerdo entre corridas del mismo prompt bajó de 95-100 %
  a **93 %**. El ejemplo fino afina la partición y la vuelve más inestable.
- **Un nombre describe el contenido: no es el objeto ni una pregunta.** «Los exoplanetas conocidos»
  nombra el objeto; «cuántos exoplanetas se conocen y desde cuándo» pregunta. La definición que lo
  cierra —«una frase breve que describe por sí sola el contenido de las oraciones del subtema»—
  atrapa los dos casos.
- **El texto de un ejemplo tiene que sostener su respuesta.** Un texto de oraciones que no se
  desarrollan entre sí deja la partición como una decisión arbitraria: el modelo no tiene qué
  correlacionar. La prueba, barata: leer el texto e intentar reconstruir la respuesta sin mirarla.

## 3. Pendientes vigentes

**Orden (09-10).** El código, los prompts y los procedimientos están listos; **`preparación del café`
ya está radicado y con sus unidades** (primera viñeta) y lo que sigue es **pasarlo por las etapas
que restan**, cada una como acto aparte (punto 0). El material anterior —documentos, baterías,
extracción y corridas— está archivado en `mvp/temp/`.
0. **`preparación del café`, por las etapas que restan,** en actos sueltos y a mano: **UT ya corrió**
   (5 unidades, 13,5 s, `deepseek` `low`); sigue **DATOS** (`paso2_datos.py "preparación del café"`)
   —corre contra la API real y escribe en la base—, escribir su batería en
   `mvp/consulta/preguntas_preparación del café.md` y correr la consulta; evaluarla con la vara de los
   números de oración, distinguiendo «no está en los datos extraídos» de «el documento no lo dice»
   (`mvp/consulta-diseno.md`, §12). **`doc11` queda fuera de la base**: si se quiere de vuelta, son
   dos actos, radicarlo otra vez (el texto está, y el sello sale igual) y correrle UT. Las baterías de
   `doc4`/`doc6` están archivadas y **sin evaluar** —el registro de esa ronda, con su medición, en
   `mvp/temp/consulta/medicion-primera-ronda.md`—: si se quiere evaluación, o se escribe la lista de
   expectativas antes de correr, o se declara posterior.
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
11. **El ejemplo de `prompt_UT` (cerrado el 09-10).** Era **un solo ejemplo, y era un documento
    entero** —el que era `doc8`—: para un documento nuevo enseñaba la forma, pero sobre ese mismo
    texto el acto **transcribía el ejemplo**. `v1` tiene **dos ejemplos** y **ninguno es el documento
    que se analiza**: un texto marino de seis oraciones y `doc9` entero. `doc8` sigue fuera de
    `mvp/documentos/`.
12. **El scratch.** `temp/` —las pruebas de particiones de UT y de extracción de DATOS, con sus
    crudos— **no se versiona**: vive solo en el disco. La base, en cambio, sí se commitea.
13. **Sin decidir: ¿el corpus quiere una partición estable?** Medido el 09-10 sobre `doc11` con
    DeepSeek `low` y el mismo documento: el prompt **no** mueve la partición —entre prompts el
    acuerdo es 97-98 %, y dentro de la primera versión de `v1`, 95-100 %—, y con el ejemplo fino el
    acuerdo entre corridas del mismo prompt bajó a **93 %**. Queda la pregunta: agregar por
    co-pertenencia, o quedarse con la tirada que fija el registro.
14. **Los papeles, al día (09-10).** El diseño (§8 dice que el `system` son las anclas: ya no), las
    dos guías (los actos ahora mandan dos mensajes, y describen el `prompt_UT` viejo —la definición
    de «desarrollo», el ejemplo único, la sección de referencias— que `v1` reemplazó), la estructura
    de los tres prompts, y los desfases que encontró la revisión: el diseño §5/§10/§11 («una unidad
    por turno», las tareas 5 y 6, la columna `corte` que no existe, el desenlace en prosa), y el tú y
    el vos de `prompt_ORQ`.
15. **Dónde van las notas de una corrida exitosa.** La verificación de UT (huecos, solapes, rango,
    enteros) y los avisos de DATOS (dónde va la unidad) se imprimen y no tienen campo en la base:
    el registro no los guarda. Decidir si se agrega una columna —o un campo en la unidad— antes de
    que la base crezca: hoy tiene 5 unidades y 0 datos, así que es cambiar el esquema, no migrar.

**Cerrado el 08-10: alineación con prompt 3.** El ORQ ubica el JSON del mensaje final donde
prompt 3 lo ponga (`orq/leer_entrega.py`; `entrega.forma` en `config.json`, que el ORQ valida) y
la relectura de los crudos guardados deja los 13 con desenlace, sin volver a llamar al modelo.
En el mismo tramo: el tope de herramientas se respeta de verdad, la causa del corte queda
registrada, la traza ya no revienta con un JSON que no sea objeto y la salida no confunde «no
hubo JSON» con «se cortó».
