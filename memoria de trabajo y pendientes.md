# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 27-09-2026 (tras ENC3; U5 en curso: `unidades_v4`, subtemas). No es bitácora: solo lo vigente. La historia está en `git log` y en los `PLAN.md`.

## 0. Dónde y cómo

- **Carpeta:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/` (máquina local de Frat, Linux). Trabajo activo en `unidades/`.
- **Repositorio:** `https://github.com/frquintero/jev-typesafe-spike`, rama `main`.
- **Roles:** Frat y Cowork (Claude) planean. La implementación y las corridas las hacen los ejecutores: Muse Code (Meta Muse Spark) en local, GPT-6 Luna (OpenAI, vía Codex o ChatGPT) y Claude Code en la nube como alternativa. El rol va con la tarea, no con el modelo.

**Flujo de una ronda.**
1. Frat y Cowork discuten y conjeturan. Se corre solo si hay una conjetura nueva.
2. Cowork escribe el prompt en `unidades/prompts/` y la sección de la ronda en `unidades/PLAN.md` (cambio, conjetura, comandos, reporte), y hace commit y push.
3. Cowork deja el mensaje para el ejecutor en `unidades/mensaje_<RONDA>.txt` (commit incluido): Frat lo pega en su sesión, o Cowork lo lanza sin terminal con `./muse.sh exec --prompt-file <archivo>`.
4. El ejecutor (Muse, Luna o Claude Code) corre sin modificar nada, reporta sin veredicto y hace commit y push de los crudos.
5. Cowork lee los crudos (`unidades/cache/`) y los evalúa contra la conjetura. Frat decide.

**Aviso de fin de ronda (decisión de Frat):** cuando Cowork lanza a Muse (`nohup bash -ic './muse.sh exec --prompt-file …' &` por Desktop Commander), arma un Monitor que consulta `git ls-remote` del repo en GitHub cada 30 s y avisa cuando aparece el commit nuevo; entonces Cowork le manda a Frat una notificación de escritorio (PushNotification) con el resultado en una línea.

**Configuración** (detalle en el README, «Correr las pruebas con Muse Code»):
- `muse.sh` (alias `muse` en `~/.bashrc`) levanta el proxy de claves si no corre, arranca Muse sin sandbox en la carpeta actual y apaga el proxy al salir si lo arrancó él.
- Las reglas del ejecutor viven solo en `AGENTS.md`. Muse y Codex (donde corre Luna) lo cargan solos; en el chat de ChatGPT, Luna lo lee porque cada mensaje empieza con «Lee AGENTS.md». `CLAUDE.md` es una línea que apunta ahí (`@AGENTS.md`).
- Claves: `proxy_local.py` las inyecta por host (TypeSafe, Z.ai, DeepSeek, xAI); nunca van en archivos del repo.
- Cowork hace git con Desktop Commander, no con el shell aislado (no ve credenciales y deja bloqueos en `.git/`). Para detener procesos, la herramienta `kill_process` de Desktop Commander (`kill` desde la terminal está bloqueado).

## 1. Qué hacemos

Extraer los **datos** de un texto, en el sentido del ensayo de Frat «¿Qué es un dato?», con un LLM (Grok 4.7, `reasoning_effort: low`), en dos pasos encadenados (`unidades/`):

1. **Unidades temáticas** (`extraer_unidades.py`, prompt `unidades_v3`): segmentación lineal del texto por subtema; el código numera las oraciones y el LLM devuelve `{"unidades": [{"tema", "desde", "hasta"}]}`.
2. **Datos por unidad** (`extraer_datos_u.py` para una unidad suelta; prompt `datos_u7`): una llamada por unidad; el LLM devuelve `{"datos": [{"variable", "valor", "unidad_de_medida"}]}`.

**Cadena completa:** `extraer_datos_doc.py <doc> <modelo> <prompt_unidades> <prompt_datos> <rN>` corre el paso 1, arma el texto de cada unidad en código y llama al paso 2 una vez por unidad; deja un consolidado `cache/doc-<doc>-…json`.

**Para qué:** es la capa de datos (nivel 3, detalles de soporte) del grafo datos → argumentos → tesis de **Zettel**. Después, Jev (`jev-1.13.0`) auditará lo extraído y graduará la confianza; no empezado.

El objetivo original del spike (EEL) está suspendido. `niveles/` (Toulmin, `datos_v1`–`v8` sobre el texto entero) queda como antecedente, sin trabajo activo.

## 2. Reglas de trabajo

- **Ockham:** empezar con lo que funciona. Cada elemento del prompt tiene que servir a la tarea; quitar lo que no se use.
- **Una cosa por ronda.** Varios cambios solo si aplican un mismo principio.
- **Planificar** es pensar y conjeturar; no se ofrecen corridas por reflejo.
- **No reinventar la rueda:** revisar la literatura antes de diseñar.
- **Mostrar el prompt antes de correr** y esperar el «adelante».
- **Sin ejemplos tomados de los documentos de prueba** (invalidan la prueba).
- Solo documentos sintéticos. No se editan README, diccionario ni guía sin aprobación.
- **Crítica constructiva:** valorar la propuesta de Frat y mejorarla con razones, sin aceptar todo.

## 3. Paso 1: unidades temáticas

- **Prompt vigente:** `unidades_v3`. Mismo esquema que el paso 2: tarea de una línea, definiciones cortas (oración numerada; unidad = oraciones seguidas que responden a la misma pregunta; frontera cuando cambia la pregunta, aunque se nombren las mismas cosas; el cambio de párrafo no es por sí solo frontera) y tres ejemplos nodo (párrafo con dos subtemas → se parte; subtema que cruza el párrafo → se une; mismas cosas en temas distintos → unidades distintas). Marcador `{{TEXTO_NUMERADO}}`: el código numera, reconstruye las unidades con el texto original y verifica huecos, solapes y orden.
- **Resultado (U4, r1):** bio1 → 8 unidades que siguen los subtemas de los párrafos, verificación limpia, 1605 tokens de razonamiento y 21 s (con v2: 11 065 y 158 s). tec2 → 1212 tokens, 16 s; 8 unidades en vez de 4, porque tec2 tiene temas que vuelven tras una interrupción.
- **Por qué cambió:** `unidades_v2` (núcleo y satélites, oraciones no seguidas) llamaba «temática» a la unidad pero la definía por un caso; en bio1 los casos cruzan los temas y el modelo osciló entre tema y entidad (visible en `reasoning_content`). El seguimiento de entidades pasa a después: la variable ya lleva su caso.
- **Límite conocido de v3:** un asunto que vuelve tras una interrupción queda en unidades separadas.
- **En prueba (U5): `unidades_v4`.** Decisiones de Frat: la unidad es el **subtema** = «un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas»; la **oración** es el texto de punto a punto (la corta el código, no el LLM); el **tema** es la unión de subtemas relacionados (nivel superior, para Zettel). El paso 1 intenta reunir también lo separado; si funciona, se evita un nivel extra. Criterio operativo: «desarrollo» (detalla, explica, continúa, contradice, saca la consecuencia; en la línea de la RST) en lugar de «misma pregunta», cuyo grano era ambiguo; regla contra agrupar por entidad; descripción de una línea en cada ejemplo; seis ejemplos (dos subtemas en un párrafo; subtema que cruza el párrafo; mismas cosas en asuntos distintos; afirmación y contradicción; hecho y consecuencia; subtema que vuelve). Salida `{"subtemas": [{"subtema", "oraciones": [n, …]}]}`. Smoke test sobre tec2.

## 4. Paso 2: datos por unidad

- **Prompt vigente:** `datos_u7` = tarea de una línea + definiciones de una línea (dato, variable, valor, unidad de medida, qué no es dato) + cinco ejemplos nodo (mediciones; cualidades con aspecto dicho y callado; nombres y relaciones; conteos y proporciones; sin datos).
- **Formato:** `variable` (la magnitud individual, completa: caso, circunstancias y método cuando define qué se midió), `valor` (literal, sin la unidad), `unidad_de_medida` (`null` en los valores cualitativos).
- **Resultados:** sobre ut1–ut5 (conjunto de desarrollo; gold en la sección DU5 de `unidades/PLAN.md`), DU7 con tres réplicas: 39/39 datos completos, ut4 vacío, variación solo de redacción. Sobre bio1 vía la cadena (U4): 14 datos en 8 unidades; las 10 cantidades del texto con su unidad, ningún dato inventado; revisados con Frat, bien construidos.
- **ENC3 (oxi1, documento de Frat, sin gold):** paso 1 bien (4 unidades, 14 s); paso 2: de 6 datos, 4 aceptables, 1 variable incompleta («fuente de este gas»: el antecedente «oxígeno» quedó en otra unidad), 1 de más («forma del oxígeno = libre», binario) y 1 omisión (metales de los nódulos). Causa principal: la **correferencia** cruza las unidades.
- **Diseño acordado para el paso 2 (`datos_u8`, opción A, sin guardar todavía):** una llamada por unidad con el **documento completo numerado** y el **foco** («oraciones 3 a 5»); el documento sirve para completar las variables, los datos se toman solo del foco; lo fijo primero (instrucciones, ejemplos, documento) y el foco al final, para aprovechar la caché de prefijo; descripción de una línea en cada ejemplo; ejemplo 6 nuevo (referencia cruzada: el caudal está fuera del foco y no se reporta). Descartada la opción B (una sola llamada con todo): es volver a `niveles/`.
- **Historia corta:** definiciones largas (`datos_u3`–`u4`) → seudodatos y «escala» leída como nominal/ordinal; solo ejemplos (`u5`) → mejor, con fallas donde los ejemplos no mostraban la forma; definiciones cortas + ejemplos nodo (`u6`) → 13/13 valores; + aspecto implícito (`u7`) → 39/39.

### Decisiones de Frat sobre qué es dato (DU5–U4)

- **Variable = magnitud individual** (VIM4, nota 2: «the radius of circle a is an instance of length»): «peso de la caja», no «peso» con un caso aparte.
- **Valor literal**, tal como aparece en `texto`, sin la unidad: «30000», unidad «litros»; «6 de la mañana», unidad «hora».
- **`unidad_de_medida` en lugar de `escala`:** «escala» es polisémica (el modelo la leía como nominal/ordinal). Los valores cualitativos no tienen unidad de medida: `null`. Los conteos llevan «unidad» (magnitud de dimensión uno).
- **Binarios** (con fiebre, sin fallas, trabado): hechos, no datos. Hay valor cuando la palabra elige entre más alternativas que el sí y el no.
- **Modificadores cualitativos del nombre** (antiguo, municipal): parte del caso. Una **cantidad con unidad** es dato aunque vaya en el nombre («caja de 12 kg» → peso de la caja = 12, kg). Números y códigos sin unidad que identifican (camión 7, cama 12, C-2) son del caso.
- **Circunstancias** («a las 8», «en la noche»): dentro de la variable («temperatura del paciente a las 8»). Una hora es valor cuando responde a «¿cuándo?».
- **Completitud de la variable** (decisión de Frat tras U4/bio1): una variable está bien hecha cuando al leerla queda claro qué varía, con el contexto necesario. El método que define qué se midió («registrados por los censos visuales», «en marea baja») va en la variable; en metrología, reduce la incertidumbre definicional (VIM 2.27). La **procedencia** queda solo para la fuente del dicho («según el informe de…», «el técnico dijo…»): no cambia qué varía, y es lo que Jev podría pesar al graduar la confianza. En bio1 no hubo error de procedencia: «marcadas por los buzos» es el agente de lo contado, y «por los censos visuales», el método.
- **El valor puede ser un tipo, no un ejemplar** (decisión de Frat tras U4/bio1): la variable tiene la estructura del fenómeno (soporte, escala, distribución, momentos) y los valores son realizaciones. «Especie más abundante = pez loro» está bien construido: «pez loro» es un tipo (categoría del soporte de una variable nominal), no un caso concreto; además es la moda de «especie de cada pez» sobre la muestra del censo, un dato de segundo orden. Lo que no puede ser valor es un ejemplar (un individuo concreto): eso sigue siendo relación entre casos. «Estado del tejido = sano» también está bien: variable categórica con más de dos estados.

## 5. Marco: qué es un dato (ensayo)

- **Caso:** lo distinguido al observar; unidad individuada y reidentificable que reúne determinaciones. Nombres e identificadores sirven para reidentificarlo (l. 91): forman parte del caso, no son valores.
- **Variable:** aspecto del caso que admite diferencias; tiene un dominio de determinaciones admisibles. Un aspecto sin diferencias es una constante.
- **Escala:** sistema de unidades, categorías, orden, precisión y conversión. El dominio dice qué es admisible; la escala, cómo se expresa (l. 127-133).
- **Valor:** posición o elemento de una escala. No es otro caso: si la respuesta es un individuo concreto (un ejemplar), lo registrado es una relación entre casos. Un tipo (una especie, una categoría) sí puede ser valor (decisión de Frat, §4).
- **Determinación:** resultado de la atribución de un valor a un caso bajo una variable; **cierra una pregunta** `variable(caso, condiciones) = ?`.
- **Hecho y determinación:** una frase que solo distingue (algo es, una relación existe) registra un hecho, no un dato. Un hecho puede abrir preguntas cuya respuesta sí sería un dato («colinda con el pozo» abre `distancia(pozo, finca) = ?`).
- **Condiciones:** constitutivas (si cambian, cambia la pregunta), de representación, de procedencia.
- **Procedencia:** quien dice o cómo se obtuvo no forma parte del dato; es un dato de otro orden, sobre la ruta (l. 161-163, 293), y pesa en la robustez del sostén. En el extractor, precisado por la decisión de completitud (§4): el método que define qué se midió va en la variable; la procedencia es la fuente del dicho.
- **Dato:** determinación registrada de modo recuperable. **Información:** el cambio en las respuestas admisibles a una pregunta al considerar un dato.
- **Vocabulario del prompt y del ensayo:** el prompt usa «variable» (magnitud individual) y «unidad de medida»; en el ensayo, la variable es el aspecto y la escala es más amplia (unidades, categorías, orden, precisión). El nombre del campo es interfaz con el modelo, no la teoría; el código o `esquema.json` puede ubicar la unidad dentro de la escala. Las condiciones constitutivas viven hoy dentro de la variable.

## 6. Lecciones

- Un campo obligatorio no filtra: el modelo inventa algo para llenarlo (seudoescalas en D6; escalas inventadas en DU2).
- «Puede formularse una pregunta» es una fuga: a cualquier hecho se le fabrica una.
- Menos prompt rinde más: `unidades_v2` dio lo mismo que `v1` con la mitad de tokens.
- Si dos señales del prompt se contradicen, el modelo oscila; el remedio es un solo principio.
- Para que el modelo omita con confianza, omitir tiene que ser parte de la tarea.
- Citar el criterio del ensayo casi literal; parafrasear introduce errores.
- Una sola corrida no separa el efecto del prompt del ruido.
- El `reasoning_content` es el mejor instrumento de diagnóstico.
- Jev corrige lo que el modelo afirma de más, no lo que omite.
- Operativo: DeepSeek puede dejar el stream colgado; si pasa un minuto sin bytes, matar la llamada y relanzar solo ese modelo.
- Una palabra polisémica en el prompt («escala») arrastra al modelo a su sentido más frecuente; mejor el término que el modelo tiene fijado («unidad de medida»).
- «Encuentra los datos» presupone que hay: sin un ejemplo sin datos, el modelo busca reemplazos (ut4 en DU4, visible en `reasoning_content`).
- Mostrar rinde más que definir (DU5), y la ostensión enseña exactamente lo que muestra: cada falla señala un rasgo que los ejemplos no traen. Por eso los ejemplos se eligen desde el marco, no desde las fallas de la prueba.
- `reasoning_content` de xAI llega recortado: es menos que los `reasoning_tokens` facturados.
- Caché de prefijo en xAI: sin el encabezado `x-grok-conv-id`, 77 de 98 llamadas solo cachearon 1152 tokens (un prefijo del proveedor, igual para todo prompt); desde ENC4, `extraer_datos_doc.py` lo envía por cadena (`<doc>-<prompt_unidades>-<prompt_datos>-<rN>`). La caché baja costo y tiempo de prefill, no el tiempo de razonamiento (decodificación).
- La contradicción entre señales también cuesta tiempo: en el paso 1, «temática» contra «núcleo = caso» llevó a 11 065 tokens de razonamiento; con una sola señal (tema), 1605.
- Al modelo el juicio, al código el cómputo: con oraciones numeradas, el modelo devuelve índices y el código garantiza la literalidad.
- Un documento de prueba escrito por quien diseñó los ejemplos, y evaluado sin gold previo, sobreestima el acierto (sesgo retrospectivo).

## 7. Pendientes

1. U5 en curso: smoke test de `unidades_v4` (subtemas, seguidas o separadas) sobre tec2; lo implementa Luna (listas de números en `extraer_unidades.py`).
2. Guardar `datos_u8` (opción A: documento completo + foco) y adaptar `extraer_datos_doc.py` (marcadores `{{DOCUMENTO_NUMERADO}}` y `{{FOCO}}`, foco como lista de oraciones); correr oxi1 y bio1.
3. Nivel de **tema** (unión de subtemas relacionados) para Zettel: si `unidades_v4` no reúne bien lo separado, hacerlo ahí (embeddings proponen candidatos, Jev juzga si tratan el mismo asunto).
4. Prueba de verdad de la cadena: documento ajeno con gold escrito antes de correr, más desordenado (tablas, abreviaturas, rangos, negaciones, fechas), del tipo que recibirá Zettel.
5. Zona gris: cualitativos dentro del nombre que informan algo («estructuras de acero»); composición con valores de tipo («níquel, cobalto y manganeso»).
6. Frontera entre dato y afirmación (ENC3: «fuente del gas = proceso electroquímico» es una tesis explicativa): objetos información y afirmación, niveles 1 y 2 del grafo de Zettel.
7. Escala: documentos largos (ventanas superpuestas, partición recursiva).
8. Jev: auditoría de los datos, graduación de confianza, canonicalización de variables (paráfrasis), reidentificación de casos entre textos, procedencia (fuente del dicho) como capa propia; `esquema.json` y §20.1 del borrador principal.
