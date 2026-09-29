# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 29-09-2026 (tras las rondas de prototipos P1–P4; paso 2 casi cerrado con `datos_pAB`; el cuello de botella pasó al paso 1). No es bitácora: solo lo vigente. La historia está en `git log` y en los `PLAN.md`.

## 0. Dónde y cómo

- **Carpeta:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/` (máquina local de Frat, Linux). Trabajo activo en `unidades/`.
- **Repositorio:** `https://github.com/frquintero/jev-typesafe-spike`, rama `main`.
- **Roles:** Frat y Cowork (Claude) planean. La implementación y las corridas las hacen los ejecutores: Muse Code (Meta Muse Spark) en local, GPT-6 Luna (OpenAI, vía Codex o ChatGPT) y Claude Code en la nube como alternativa. El rol va con la tarea, no con el modelo.

**Flujo de una ronda.**
1. Frat y Cowork discuten y conjeturan. Se corre solo si hay una conjetura nueva.
2. Cowork escribe el prompt en `unidades/prompts/` y la sección de la ronda en `unidades/PLAN.md` (o en `prototipos/PLAN.md`) (cambio, conjetura, comandos, reporte), y hace commit y push.
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

Extraer los **datos** de un texto, en el sentido del ensayo de Frat «¿Qué es un dato?», con un LLM barato (Grok 4.7 o DeepSeek `deepseek-flash`, razonamiento `low`), en dos pasos encadenados (`unidades/`). Meta: un prompt que acierte cerca del 90 % de los casos; la zona gris la juzga después Jev.

1. **Subtemas** (`extraer_unidades.py`, prompt `unidades_v5`): el código parte el texto en oraciones y las numera; el LLM las agrupa en subtemas, `{"subtemas": [{"subtema", "oraciones": [n, …]}]}`.
2. **Datos por subtema** (prompts candidatos `datos_pAB` y `datos_pABF`): una llamada por subtema con el **documento completo numerado** y el **foco** (las oraciones del subtema, seguidas o separadas); el LLM devuelve `{"datos": [{"variable", "valor", "unidad_de_medida"}]}`.

**Cadena completa:** `extraer_datos_doc.py <doc> <modelo> <prompt_unidades> <prompt_datos> <rN>`: corre el paso 1 (o reutiliza su crudo si existe), arma documento y foco en código, envía `x-grok-conv-id` para la caché de prefijo en xAI y deja un consolidado `cache/doc-<doc>-…json`.

**Prototipos** (`prototipos/`): banco de prueba del paso 2 solo (foco = texto entero), con una batería de 15 textos cortos con respuestas escritas antes de correr y los ejemplos prototípicos como archivos sueltos (`ejemplos/A.md`…`F.md`) que se combinan (`correr.py`, `evaluar.py`).

**Para qué:** es la capa de datos (nivel 3) del grafo datos → argumentos → tesis de **Zettel**. Después, Jev (`jev-1.13.0`) auditará lo extraído y graduará la confianza; no empezado.

El objetivo original del spike (EEL) está suspendido. `niveles/` queda como antecedente.

## 2. Reglas de trabajo

- **Ockham:** empezar con lo que funciona. Cada elemento del prompt tiene que servir a la tarea; quitar lo que no se use.
- **Una cosa por ronda.** Varios cambios solo si aplican un mismo principio.
- **Planificar** es pensar y conjeturar; no se ofrecen corridas por reflejo.
- **No reinventar la rueda:** revisar la literatura antes de diseñar.
- **Mostrar el prompt antes de correr** y esperar el «adelante».
- **Sin ejemplos tomados de los documentos de prueba** (invalidan la prueba).
- Solo documentos sintéticos. No se editan README, diccionario ni guía sin aprobación.
- **Crítica constructiva:** valorar la propuesta de Frat y mejorarla con razones, sin aceptar todo.

## 3. Paso 1: subtemas

- **Prompt vigente:** `unidades_v5`. Subtema = «un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas» (decisión de Frat); oración = texto de punto a punto (la corta el código); tema = unión de subtemas relacionados (nivel de Zettel, no de este paso). Definiciones: desarrollo (detalla, explica, continúa, contradice o saca la consecuencia; en la línea de la RST); «nombrar el mismo lugar, objeto o persona no basta para unir oraciones»; el nombre del subtema dice qué se dice de las cosas, no cuáles son. Cinco ejemplos con descripción de una línea. `{{TEXTO_NUMERADO}}`; el código reconstruye y verifica huecos, solapes, fuera de rango y no enteros.
- **Resultados:** tec2 y bio1 bien (bio1: 9 subtemas que separan asunto de entidad). oxi1: 4 subtemas con Grok, 3 con DeepSeek. **tec1 (ENC7):** Grok hizo 13 subtemas de una oración cada uno en 57 s y 2298 tokens de razonamiento; DeepSeek, 4 subtemas razonables (uno por equipo) en 4 s. La regla contra agrupar por entidad, aplicada al pie de la letra, fragmenta los informes de inspección. **evals1** (texto real, metodológico; U7, DeepSeek): 6 subtemas que siguen la estructura del artículo (introducción, plan y cuatro principios), 8576 tokens de razonamiento; el nombre del subtema 1 enumera tres asuntos, señal de dos subtemas pegados.
- **Es el cuello de botella actual** (tiempo de Grok y granularidad). Siguiente: llevar al paso 1 el método de prototipos (§4).
- Historia: v2 (núcleo y satélites) osciló entre tema y entidad (11 065 tokens); v3 (tramos contiguos) no reunía lo separado; v4 nombraba los subtemas por la entidad; v5 lo corrigió.

## 4. Paso 2: datos por subtema

- **Prompts candidatos: `datos_pAB`** (429 palabras) y **`datos_pABF`** (525; + prototipo F, ver P4) = `prototipos/base.md` (definiciones y «No son datos» de `datos_u10` + línea de formato) + dos ejemplos prototípicos: **A** número con unidad (medida, conteo con «unidad», porcentaje) y **B** fecha u hora de un hecho. Pendiente de guardar como `datos_u11` cuando Frat lo apruebe.
- **Definiciones vigentes** (desde `datos_u9`): Documento; Foco (conjunto de oraciones de las que se extraen los datos; el resto del documento solo sirve para saber a qué se refiere cada expresión); Variable (aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor; se nombra con aquello a lo que pertenece y sus circunstancias); Valor (cantidad —medida, conteo, fracción, fecha, hora— o cualidad; lo vago o aproximado conserva su cuantificador); Unidad de medida (la unidad en que se expresa un número; null si el valor no lleva número); Dato (variable + valor + unidad). **No son datos:** lo que solo afirma o niega (su valor sería sí o no), las relaciones entre cosas, los adjetivos del nombre y los enunciados genéricos. La sección se llama «No son datos», no «Reglas»: solo excluye.
- **Prototipos (P1, Grok, batería de 15 textos, 29 datos):** k0 (sin ejemplos) 19/29, A 23/29, AB 29/29 y ABC, ABCD, ABCDE también 29/29. Los 10 fallos de k0 fueron todos de convención de unidad («cajas» por «unidad»; null por «fecha» u «hora»); ningún falso dato en ninguna configuración. Decidir que no hay nada fue lo más caro (1175–1957 tokens por texto).
- **Documentos reales (P2, Grok, contra `datos_u10`):** tec1 igual (9 datos, 58 s); oxi1 mejor (recupera «millones», 6 datos); bio1 casi igual (14 datos, 93 s frente a 118): vuelve «especie más abundante = pez loro»; pierde «finos» y los metales; saca «hora = al mediodía» de una medición. ABE quedó incompleto (créditos de xAI agotados en bio1); en oxi1 no mejoró a AB.
- **DeepSeek (P3):** con AB bien en informes (bio1 mejor que u9, 96 s; tec1 gana «lunes» pero saca «filtro = saturado»); en el ensayo oxi1 sacó de más (17 datos, 24 773 tokens): lo que se creía, lo que podría pasar, comparaciones, lugares y el tono del autor. **P4:** prototipo **F** (negativo de ensayo: lo que se creía, lo que podría pasar y una comparación, junto a un dato real) → `datos_pABF` (525 palabras) con DeepSeek sobre oxi1: de 17 a 9 datos, de 106 a 71 s y de 24 773 a 16 316 tokens; desaparecen creencias, hipótesis, comparaciones, lugares y tono, y el foco 3 queda vacío (1688 tokens frente a 10 279). Quedan «fuente del oxígeno = proceso electroquímico geológico» (tesis explicativa, pendiente 7) y «forma del oxígeno = libre». Candidato para ensayos: ABF.
- **Texto genérico (ENC9, DeepSeek, `datos_pABQ5` sobre evals1):** un texto metodológico lleno de números y cuantificadores pero sin casos individuales. 5 de 6 focos vacíos; rechazó «100 %», «dos expertos», «un cambio a la vez», los nombres de los comandos y «alta/baja variación»; el único dato fue «cantidad de ejemplos… = algunos» (zona gris). ChatGPT, aplicando el prompt a mano, llegó a lo mismo salvo ese dato. Los tokens de razonamiento se dispararon justo en los focos con bordes (2173–3310 frente a 457–879). «Un cambio a la vez» es un principio de método (OFAT) que el texto anuncia como tal (or. 5), no una propiedad del comando. «Algunos ejemplos» y la or. 5 son metadiscurso (el texto hablando de sí mismo); DeepSeek extrajo del primero y no de la segunda.
- **Formato:** `variable` (completa: caso, circunstancias y método cuando define qué se midió), `valor` (literal, sin la unidad), `unidad_de_medida`.
- **Historia corta:** definiciones largas (`u3`–`u4`) → seudodatos; solo ejemplos (`u5`) → mejor; definiciones cortas + ejemplos nodo (`u6`–`u7`) → 39/39 en ut1–ut5; documento completo + foco (`u8`); definiciones reestructuradas, «No son datos», genéricos y cantidades vagas (`u9`); fecha de un hecho es dato (`u10`); prototipos mínimos (`pAB`).

### Decisiones de Frat sobre qué es dato (DU5–P4)

- **Texto genérico sin datos es resultado correcto** (ENC9): el dato es de un caso, no de una clase; las generalizaciones y reglas de un texto metodológico son garantías (nivel de los argumentos), no datos. No se amplía «dato» para que entren.
- **Pertinencia:** en los bordes, que algo sea dato depende de la práctica que haga pertinente la variable (ensayo l. 121). «Cantidad de ejemplos que trae el artículo = algunos»: a primera vista no; zona gris para Jev.
- **Modo de una acción no es propiedad del objeto:** «mejorar… un cambio a la vez» es el método de la acción (excluido con las relaciones), no un atributo del comando, a diferencia de «capacidad del tanque = 30000 litros».
- **Variable = magnitud individual** (VIM4, nota 2: «the radius of circle a is an instance of length»): «peso de la caja», no «peso» con un caso aparte.
- **Valor literal**, tal como aparece en `texto`, sin la unidad: «30000», unidad «litros»; «6 de la mañana», unidad «hora».
- **`unidad_de_medida` en lugar de `escala`:** «escala» es polisémica (el modelo la leía como nominal/ordinal). Los valores cualitativos no tienen unidad de medida: `null`. Los conteos llevan «unidad» (magnitud de dimensión uno).
- **Binarios** (con fiebre, sin fallas, trabado): hechos, no datos. Hay valor cuando la palabra elige entre más alternativas que el sí y el no; el criterio es cuántos valores admite la variable, no la forma de la frase.
- **Enunciados genéricos** (sobre una clase o lo que suele pasar) no dan datos: el dato es de algo individual.
- **Cantidades vagas o aproximadas** («pocas», «unos 5», «cerca de 300») se copian con su cuantificador y nunca se cambian por un número; resolverlas es trabajo de Zettel con el contexto (variable lingüística de Zadeh; clase de comparación). Unidad solo si el valor lleva número («unos 60» → unidad; «pocas» → null).
- **La fecha u hora de un hecho es dato** (opción A de Frat), aunque además vaya como circunstancia en otras variables («fecha del censo = 12 de marzo»). Borde abierto: la hora de una medición («al mediodía») parece circunstancia, no hecho; los modelos la sacan a veces.
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
- **Las definiciones enseñan los conceptos; los ejemplos, las convenciones** (P1): sin ejemplos, los únicos errores fueron de convención de unidad. Un buen prototipo enseña lo que la definición no deja deducir, con un solo fenómeno y una línea de descripción.
- **Los ejemplos cargados meten ruido** (P2): el pez loro y el foco de los nódulos se perdieron con `u9`–`u10` (ejemplos con cinco lecciones cada uno) y volvieron con AB. Más ejemplos no es mejor (*over-prompting*); el número lo decide la curva.
- **El tiempo depende del documento más que del prompt:** acortar el prompt a la mitad casi no cambió los tiempos; el razonamiento se va en los focos dudosos del texto, y decidir que no hay dato cuesta más que extraerlo.
- **El género del texto pesa más que el modelo** (P3): en informes, Grok y DeepSeek andan bien con AB; en el ensayo, DeepSeek extrae creencias, hipótesis, comparaciones y tono. Los textos de Zettel serán ensayos.
- Una regla que deja un borde sin cerrar le cuesta al modelo miles de tokens aunque no cambie el resultado (ENC8: la regla de fechas llevó un foco de 492 a 3156 tokens).
- El razonamiento completo de Grok no se puede leer (solo un resumen corto o el cifrado); para diagnosticar dudas sirve DeepSeek, que lo entrega entero.
- **Nivel de razonamiento efectivo** (docs oficiales, 28-09): DeepSeek solo tiene `high` y `max`; nuestro `low` se convierte en `high`. GLM 5.3 Flash tiene `low`, `high` y `max` (por defecto `max`, siempre razona); con `low` razonó 0–87 tokens por foco. Grok corre en `low`. Los puntajes de Artificial Analysis se miden en `max`: no se trasladan a nuestras corridas.
- **Cada modelo tiene su temperamento ante el mismo prompt:** GLM se abstiene cuando duda («Conservative: depth»; AA-Omniscience +7) y necesita un ejemplo positivo de cualidades; DeepSeek afirma de más (AA-Omniscience −5) y necesita el negativo de ensayo (F).

- **Un texto sin datos mide una sola cara del extractor** (ENC9): que no invente. Un prompt que siempre devolviera vacío sacaría 100 %; vale junto a un gold con datos (oxi1).
- **Hipótesis H1 (no probada): los tokens de razonamiento delatan los bordes.** En ENC9 se dispararon justo en los focos que el análisis previo marcó como riesgosos, pero son seis focos y una corrida. Confusor posible: esos focos son también los que traen números o cuantificadores en la superficie. Si se confirma, sería una señal barata para mandar a revisión (como la franja central de Jev).

## 7. Pendientes

1. Decidir `datos_u11`: ABF parece la mejor base (F no debería dañar informes); falta confirmarlo con Grok y con un informe (tec1 o bio1).
2. Completar ABE sobre bio1 con Grok cuando haya créditos de xAI (baja prioridad: nada indica que E haga falta).
3. **Paso 1 con el método de prototipos:** batería corta, curva de ejemplos, medir tokens; resolver la fragmentación de Grok en informes (tec1) y su lentitud.
4. Prueba de verdad de la cadena: documento ajeno con gold escrito antes de correr, más desordenado (tablas, abreviaturas, rangos, negaciones, fechas), del tipo que recibirá Zettel; de preferencia un ensayo.
5. Nivel de **tema** (unión de subtemas relacionados) para Zettel: embeddings proponen candidatos, Jev juzga.
6. Zona gris (terreno de Jev, no del prompt): «algunos ejemplos» (evals1), «finos», composición con valores de tipo («níquel, cobalto y manganeso»), «millones», hora de una medición, superlativos (dato de segundo orden).
7. Frontera entre dato y afirmación (creencias, hipótesis, tesis explicativas): niveles 1 y 2 del grafo de Zettel.
8. Escala: documentos largos (ventanas superpuestas, partición recursiva).
9. Jev: auditoría de los datos, graduación de confianza, canonicalización de variables, reidentificación de casos entre textos, procedencia como capa propia.
