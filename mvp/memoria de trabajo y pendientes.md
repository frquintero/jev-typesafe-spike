# Memoria de trabajo y pendientes (spike-jev / Zettel)

**Para qué es este documento.** Es la **memoria de trabajo** del tramo, y viven acá **dos cosas
y nada más**: (1) las **lecciones útiles** para lo que se está trabajando y (2) el **todo list**
—lo que hay que hacer—. **Todo lo demás se va**, y cada cosa a su sitio: lo **decidido**, al
documento que lo aplica (el diseño, el vocabulario, el prompt, la guía); las **cifras**, a la
base; la **historia**, a git; y el detalle de cada ronda, al `PLAN.md` de su proyecto. Una cosa
ya decidida **no se anota acá: sale de acá**.

Estado al 13-10-2026. El vocabulario y los informes sueltos, en `otros documentos/`; la casa, la
actualización de los tres sitios y los reportes, en `política.md`.

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
- **Al modelo el juicio, al código el cómputo** (corregido el 11-10): el juicio es **dónde se corta y qué se agrupa** —el modelo devuelve las oraciones **literales**—, y el cómputo es ubicarlas en el texto, verificar el contrato y guardar los tramos. La **numeración de oraciones se jubiló**: el número depende de la regla con la que se cortó, y con otra regla dice otra cosa; la referencia es el tramo.
- **Cada ítem que se espera recuperar prueba una sola cosa** (contenido, identidad externa, condición o duda) y hay que poder señalar el registro que lo satisface: mezclarlos infla los porcentajes.
- **Lo que un paso no registra no llega al siguiente:** el paso 2 solo usa el contexto que el paso 1 le entrega.
- **Jev es posterior:** subtemas, inventario global y Jev siguen fuera de las pruebas del núcleo. La detección o recuperación posterior de omisiones no se ha probado aquí.
- **Operativo:** DeepSeek declara `low`, `high` y `max`, con `high` por defecto, así que el `low` que
  mandamos es un escalón declarado, no un alias de `high` (corregido el 08-10); en las líneas viejas,
  que usan streaming, puede dejar el stream colgado (si pasa un minuto sin bytes, relanzar). Y en xAI,
  **que la clave autentica no quiere decir que el equipo pueda llamar**: `GET /v1/api-key` separa las
  dos cosas (`team_blocked`), y con el equipo bloqueado todo endpoint de modelos contesta 403
  `permission-denied`. Y el **400** «Incorrect API key provided» es otra cosa todavía: la clave **no
  es de esa puerta** —las `grok_…` de agente que emite la consola no las acepta `api.x.ai`, que pide
  las `xai-…` de inferencia—.
- **El prefijo invariante se cachea entero:** con Luna el `system` entró casi todo en la segunda
  llamada —**1.839 de 1.842** tokens de entrada— y con MiMo **2.048 de 2.066**, sin mandar nada por
  un campo aparte (13-10). Por eso las reglas y los ejemplos van en el `system`, y lo que cambia por
  llamada, al final del `user`.

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
  (`mvp/diseño-mvp.md` §7.6).
- **Repite lecturas y no hay corte por ciclo:** `doc6` q2 pidió `doc6:U4` dos veces y gastó
  6 turnos y 5 llamadas; la guardia corta por número de turnos y de llamadas, no por
  repetición (`mvp/diseño-mvp.md` §7.8, D25).

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

**Verificadas con los nombres corregidos del primer ejemplo (10-10)**, en el scratch `temp/` y sin
tocar la base: seis particiones de `preparacion_cafe` (Haiku `low` ×2, `medium`, `high` ×2;
DeepSeek `low`) mandadas como el acto real, en dos mensajes.

- **Los cortes estables no se mueven; el que duda es la oración que vale para todo el texto.** Los
  tres bloques de métodos salieron idénticos en las seis; [3] —la molienda y la temperatura «para
  cualquier método»— quedó sola en tres y unida a [1, 2] en tres. En Haiku `high` quedó sola las dos
  veces, con el mismo nombre: **señala, no prueba**.
- **Un nombre que junta dos asuntos se vuelve un rótulo.** Cuando [3] va unida, el nombre dice de qué
  clase es («las claves generales», «los factores comunes»); sola, dice qué contiene («la molienda al
  momento y la temperatura ideal del agua») en dos de tres corridas.

**Verificadas con la sonda de Gemini (12-10) y el alias en el registro (13-10).**

- **La vía no cambia el tiempo; la pregunta sí.** La misma pregunta por `generateContent` y por la
  fachada compatible-OpenAI del mismo host contestó igual y tardó lo mismo (4,7 s y 4,1 s); otra
  pregunta, por la misma fachada, tardó 87,8 s. Una medición sola no dice nada: manda el pensamiento
  que pide la pregunta, no la puerta.
- **El pensamiento de Gemini se cobra por las dos vías y solo una lo declara:** mismo
  `total_tokens` (318) por las dos —`thoughtsTokenCount` 285 en `generateContent`, y en la fachada
  compatible un `usage` sin desglose (19 + 16)—, así que normalizar `thinking_tokens` por esa vía no
  lo ve. Y el `tool_calls` trae un `extra_content.google.thought_signature` que hay que devolver tal
  cual.

**Verificadas con la consulta en la base viva (12-10).**

- **Con entrega no basta: puede entregar sin leer nada.** Los cuatro actos de consulta de la base
  viva (`C000005`…`C000008`) entregaron, y uno —la pregunta tecleada— cerró en **1 turno y 0
  llamadas**, sin leer ningún caso, y quedó registrado como `respondida`: el JSON llegó, pero la
  respuesta es del modelo, no del corpus. El registro **no distingue «entregó» de «se sostiene»**:
  lo que ata la respuesta al documento es `casos_leídos`, y puede estar vacío.
- **La misma pregunta se radica tantas veces como se corra, y convive.** Tres réplicas de la batería
  1 quedaron como `q1`, `q3` y `q4`, con el mismo texto y su hora distinta: es la decisión —cada acto
  radica la suya y el `upsert` se retiró—, pero **nada lee `preguntas` todavía**: hoy es el registro
  de lo preguntado, y su consumidor es Zettel.

## 3. Pendientes vigentes

**Orden.** **La base viva tiene dos documentos radicados**, los dos por el acto del volcado (12-10):
`sol` (token `A000001`, sello `c9c3de7534d3…` — el **mismo texto** que estaba radicado antes, mismo
sello) y `aviacion` (`A000002`, sello `e546d95e8b13…`, de `mvp/documentos/aviacion.txt`, ocho
encabezados). Lo demás —`preparacion_cafe`, las baterías y las corridas anteriores— **vive en el
scratch** (`temp/ut-sin-marcas/out/sol-ut-vieja.db`), no en la base. **El substrato de la traza está
hecho** (12-10): el token por acto, la conservación de los productos, las plantillas en la base y la
guardia del esquema (`mvp/diseño-mvp.md` §3). **Las dos UT y los dos DATOS están hechos** (12-10, con `luna`/`low`, el default de la base):
`sol` → UT `C000001` (6 unidades, 16 oraciones) y DATOS `C000003` (23 datos); `aviacion` → UT
`C000002` (11 unidades, 17 oraciones) y DATOS `C000004` (36 datos). Los cuatro actos con el contrato
y la forma limpios, y las plantillas `UT` y `DATOS` v1 registradas solas. La base está en la **versión 4**, y la consulta **ya corrió en la base viva** (12-10): cuatro actos ORQ,
`C000005`…`C000008`, todos `exitoso` y todos con su pregunta radicada al cerrar —tres **réplicas de
la batería 1** (`q1` y `q3` con `luna low`, `q4` con `deepseek-flash low`) y **una tecleada** que no
está en la batería (`q2`)—; las preguntas 2 a 5 de la batería **no** corrieron sobre la base viva.
Sigue: **evaluar** esas cuatro con la vara de §8 del diseño —no pide llamadas nuevas—, o el volcado de
`preparacion_cafe` por las etapas (punto 0). El **modelo y el esfuerzo de cada acto se leen del corpus** (`ajustes`, cuatro filas; el almacén va
por la **versión 3** y esa tabla no está: la política tiene un solo lugar), hoy `luna` / `low` por
decisión de Frat, y se pueden pisar por llamada (`--modelo`, `--esfuerzo`).
0. **`preparacion_cafe`, por las etapas,** en actos sueltos y a mano, **después del volcado**: no está
   en la base viva —el reseteo se llevó lo radicado y la UT de Haiku `high`—, así que primero se radica
   con el acto del volcado (punto 18); siguen **UT**
   (`paso1_unidades.py preparacion_cafe`) y **DATOS** (`paso2_datos.py preparacion_cafe`) —corren
   contra la API real y escriben en la base; el modelo y el esfuerzo son la elección abierta, ver
   `otros documentos/informe-proveedores-2026-10-10.md` y el pendiente 17—,
   su batería ya está escrita (`mvp/consulta/preguntas_preparacion_cafe.md`, 11-10) y falta correr
   la consulta; evaluarla con la vara del contenido —qué le pasa a A(Q)—, distinguiendo «no está en
   los datos extraídos» de «el documento no lo dice»
   (`mvp/diseño-mvp.md` §8). `doc11` está en `mvp/documentos/`, fuera de la base: vuelve con dos
   actos, radicarlo (el sello sale igual) y correrle UT. Las baterías de
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
7. **Grok: probado el 13-10, y las dos trampas del camino.** El primer intento chocó con un equipo
   bloqueado (`203d5213…`: **403** `permission-denied`, «credits or spending limit», con
   `team_blocked: true` en `GET /v1/api-key`). Con una clave de **inferencia** (`xai-…`, ACLs
   `api-key:model:*`) de **otro equipo** (`d12ef41d…`, `team_blocked: false`) el alias `grok`
   (`grok-4.7`) contesta: **texto** (2,5 s, `finish_reason: stop`) y **herramientas**
   (`finish_reason: tool_calls`, en la forma que consume el ORQ). Ojo: la clave `grok_…` de agente
   que emite la consola **no** sirve contra `api.x.ai` (**400** «Incorrect API key provided»).
   **Lo que queda:** compararlo por calidad con la batería si se lo quiere para algún acto —el default
   de los cuatro sigue en `luna`/`low`—.
8. **Unidad temática con el eje de `v1`** (decisión de Frat, 02-10; registrada en `definiciones-del-marco.md`, parte B). Los prompts de trabajo (`prompt_UT` y `prompt_DATOS`) producen la unidad con el eje en el asunto: el `subtema` **nombra el núcleo** —el caso de la unidad— y las oraciones que lo desarrollan van juntas. Falta **declarar los satélites**, los casos de los que el texto habla por su relación con el núcleo, que hoy se leen de las relaciones y acciones. Discutirlo antes de escribirlo.
9. **Adoptar el candidato del paso 2:** `mvp/temp/paso2/prompt_ficha_contexto.md` vive hoy en la carpeta de trabajo; si se adopta, le toca su sitio en `mvp/prompts/` con nombre propio, sin mezclarlo con `ficha_v2`.
10. **Cerrar la forma del dato del paso 2:** si vuelven el `sostiene` (quién lo sostiene) y el `respaldo` (la ruta al fragmento), y si `unidad_valor` se queda como campo propio o la unidad va dentro del valor. Hoy el dato viaja sin fuente ni ruta.
11. **El scratch.** `temp/` —las pruebas de particiones de UT y de extracción de DATOS, con sus
    crudos— **no se versiona**: vive solo en el disco. La base, en cambio, sí se commitea.
12. **Sin decidir: ¿el corpus quiere una partición estable?** Medido el 09-10 sobre `doc11` con
    DeepSeek `low` y el mismo documento: el prompt **no** mueve la partición —entre prompts el
    acuerdo es 97-98 %, y dentro de la primera versión de `v1`, 95-100 %—, y con el ejemplo fino el
    acuerdo entre corridas del mismo prompt bajó a **93 %**. Queda la pregunta: agregar por
    co-pertenencia, o quedarse con la tirada que fija el registro.
13. **Los papeles, al día (09-10 · actualizado 13-10).** **Hecho:** `mvp/diseño-mvp.md` §4 dice qué va en cada
    mensaje, §7.2 cómo se reparten los relojes (el del radicado en el `system`, el del sistema en el
    `user`), §6 los huecos y los tramos, y §6.2 que el paso 2 va **en tanda**; las medidas de caché
    que sostienen la regla viven en el §2 de esta memoria. **Y el 11-10:** la base **sí** guarda la
    literal de cada oración con su tramo, y la causa de un corte va en `motivo`, que es la columna que
    existe (§7.8). **Falta:** el tú y el vos de `prompt_ORQ`; y el desenlace en prosa (§7.9). Lo que
    el diseño describe —el JSON tolerando prosa— **no es un desfase**: es la decisión D20, y el ORQ lo
    ubica. Lo de la etapa 3 —sin comparación propia— y lo de los
    proveedores quedaron resueltos el 13-10: `mvp/proveedores.md` es el mapa de los alias, las
    mediciones se mudaron a `otros documentos/informe-proveedores-2026-10-10.md`, y la etapa 3 está en
    el pendiente 16.
14. **Dónde van las notas de una corrida exitosa —y el texto del prompt—.** La verificación de UT
    (huecos, solapes, rango, enteros) y los avisos de DATOS (dónde va la unidad) se imprimen y no
    tienen campo en la base: el registro no los guarda. **El texto de la plantilla ya está en la
    base** (12-10): `prompts` guarda cada versión y `corridas` apunta a su `prompt_id` y
    `prompt_version`, así que no se pierde. Falta decidir si las notas de la verificación van a
    alguna columna —o a un campo de la unidad— y hacerlo **antes de que la base crezca**: hoy está
    en cero, así que todavía es gratis.
15. **La entrada de la consulta (resuelto el 12-10 y el 13-10: se carga y se radica al entregar).**
    Está escrito donde vive lo decidido: `mvp/diseño-mvp.md` §7.2 y la decisión **D28**. La
    pregunta entra por el acto —de un archivo o tecleada, con `mvp/código/cargar_pregunta.py`—, el
    **dominio** lo lleva el comando, y el acto la radica **al cerrar, solo con la entrega**. El
    cargador se llamó `radicar_pregunta.py` hasta el 13-10: el nombre prometía lo que ya no hacía.
    **Lo que sigue abierto:** la entrada como JSON con `pregunta` y `dominio` —la forma en que Zettel
    dará la pregunta— y el **alcance por documento** (`resolver_dominio` solo sabe de etiquetas,
    `WHERE dominio = ?`).
16. **La consulta, corrida y sin evaluar.** La batería del Sol tiene cinco preguntas. En el scratch
    de la línea vieja **las cinco se corrieron** con `luna low` —la 1 y la 3 el 10-10, la 2 el 11-10
    05:31 (`b3098df`), la 4 y la 5 el 11-10 05:55 (`1e639dc`, «batería completa: 5/5 respondida»)— y
    **no están en la base viva**: el reseteo del 11-10 se las llevó. De ahí, lo que ya se vio
    entonces: la q1 leyó **un** caso (`sol:U2`) y la q3 **dos** (`sol:U4` y `sol:U1`), **y `sol:U1`
    sobró** —nada de lo que respondió sale de ahí—; las dos cerraron en **2 turnos**, sin corte, con
    el JSON como todo el mensaje; y con `luna low` el modelo gastó **0 tokens de pensamiento** en los
    cuatro turnos y el **caché no se reusó** entre turnos (`cached_tokens: 0`).
    En la **base viva** hay otras **cuatro** (12-10, `C000005`…`C000008`): las tres réplicas de la
    batería 1 —`luna low` ×2 y `deepseek-flash low`— y la tecleada. **Falta evaluarlas**: la vara es
    `mvp/diseño-mvp.md` §8 (que la respuesta se sostenga en lo que el documento establece, y
    distinguir «no está en los datos extraídos» de «el documento no lo dice»), el material para
    juzgar es la batería **con sus respuestas de referencia**
    (`mvp/consulta/batería_sol_respuestas.md`, escritas **a ciegas de las extracciones**), y evaluar
    no pide llamadas nuevas. **Lo primero que hay que mirar:** la tecleada (`q2`) **entregó sin leer
    un solo caso** y quedó `respondida` (ver §2). Y las preguntas 2 a 5 de la batería **no** se
    corrieron sobre la base viva: si lo que se quiere es la batería en la base, eso falta.
17. **Re-puntuar el banco de DATOS con preguntas.** La vara no es el conteo de datos: una unidad es
    adecuada para una pregunta si **leer su caso y sus datos reduce el conjunto de respuestas
    admisibles** (no se puntúa por contar datos ni por si la extracción conservó las palabras: una
    paráfrasis puede responder y una transcripción fiel puede no responder nada). Toda la comparación
    de modelos de DATOS se hizo con conteo, así que hay que rehacerla: las corridas están en disco
    (`temp/datos-test/`, con sus corredores en seco `paso2_seco_v1.py`, `…_luna.py`, `…_mimo.py`) y
    **re-puntuar no cuesta llamadas nuevas**; lo que falta es la batería. Se escribe **a ciegas de
    las extracciones**: quien la escribe después de ver las salidas redacta preguntas que ya sabe si
    pasan (*HARKing*), y por eso **no es quien puntúa**. Antes de puntuar hay que decidir **la
    unidad**: la UT sola (suficiencia local) o el documento entero, donde una pregunta puede quedar
    respondida por datos de dos unidades. Mientras no se re-puntúe, no se cambia el proveedor por
    defecto de DATOS (`otros documentos/informe-proveedores-2026-10-10.md` §1).
18. **El almacén: el acto del volcado, y que los pasos lean de ahí.** **Hecho** (11-10; corregido el
    12-10): el diseño (`mvp/diseño-mvp.md` §2 y §5), la base (`mvp/código/almacen.db`, cuatro tablas
    —`documentos`, `volcados`, `prompts` y `contador`—, limpia) y el módulo (`mvp/código/almacen.py`:
    `escribir` con el espejo del corpus en la misma transacción, `texto_de` con el sello comprobado,
    `registrar_fallo`). **La identidad del documento es su volcado y su fecha; el sello es guardián y
    la fuente es traza** —el `UNIQUE (sello)` se retiró: el mismo texto volcado en otra fecha es otro
    documento (`mvp/diseño-mvp.md` §5)—. **Hecho (12-10):** el acto
    **`volcar.py`** —fuente → `prompt_volcado` → el índice → la verificación → el markdown → el
    almacén—, que **es la radicación** (y con él se retiró `radicar.py`), y **`paso1` y `paso2` leen
    el texto del almacén**. La cadena se probó antes en el scratch (`temp/estructura/`: cinco
    textos —sin marcas, numerado, mixto, `Anexos` pegado y separado—), y el armador quedó en
    `mvp/código/armar_volcado.py`.
19. **Gemini: declarado, sin etapa y sin corrida real.** Entró al registro el 13-10 (alias `gemini`
    → `gemini-3.8-flash`, por la fachada compatible-OpenAI de Google AI Studio; la clave,
    `GEMINI_API_KEY`, mapeada por host en `mvp/código/proveedores/claves.py`). Probado desde
    `proveedores.llamar`: texto (ok, 2,5 s), herramientas (`finish_reason: tool_calls`) y sin clave,
    que falla limpio. Falta **una corrida real del ORQ** —ahí se prueba que el `thought_signature`
    vuelva en el segundo turno— y decidir si algún acto lo usa: los cuatro siguen en `luna`/`low`, y
    elegirlo es un `UPDATE` en `ajustes`.
