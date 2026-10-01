# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 30-09-2026, fin de sesión. **Pruebas de extracción suspendidas.** No es bitácora: solo lo vigente. La historia está en `git log` y en los `PLAN.md` (`unidades/PLAN.md`, `prototipos/PLAN.md`).

## Dónde quedamos (leer primero)

- **Pruebas suspendidas (30-09, decisión de Frat).** Frat afinó el marco filosófico del ensayo «¿Qué es un dato?» y va a empezar desde cero en otra sesión: el enfoque del prompt probablemente cambie. Lo de abajo es el registro de lo aprendido hasta aquí, para llevar a la nueva sesión; nada está lanzado ni en curso.
- **Últimos prompts:** paso 1 `unidades_v5`; paso 2 `datos_pABQ5` (vigente formal) y `datos_pABQ6B` (mejor en las réplicas, no adoptado por la suspensión). Modelo: DeepSeek (xAI sin créditos).
- **Lo que vale la pena llevar al nuevo enfoque** (detalle en §4–§6):
  1. **Fallas por género:** en informes y ensayos `pABQ5` es preciso; en divulgación que describe clases (biomar1) saca de más: constantes de la definición, genéricos de clase en singular, variables fabricadas («importancia = crucial», «grado de delicadeza = delicado», «siglo = XXI») y adjetivos que clasifican.
  2. **La pregunta generadora** («¿qué valor toma esta variable…?») es una fuga: va de la expresión a la variable. Quitarla y exigir que el foco atribuya a algo individual un valor en un aspecto que el texto determina (`pABQ6B`) bajó las filas de más sin perder datos firmes.
  3. **Estructura propuesta, no probada (`pABQ7`):** cambiar la lista creciente de «No son datos» por tres condiciones de la fórmula del ensayo, `variable(caso, condiciones) = valor`: **caso** individual (no clase ni genérico), **aspecto** que podría haber sido otro sin que el caso dejara de ser el que es (esencial frente a accidental; excluye constantes, binarios, relaciones y valoraciones) y **hecho** (no creencia, hipótesis ni posibilidad). Un borde nuevo cae en una casilla en vez de sumar una línea.
  4. **Presuposición** (Karttunen, Heim; FactBank): lo que la voz del texto da por sentado está presentado como hecho; los condicionales filtran; los factivos comprometen al autor. Propuesta: regla gruesa en el prompt y fineza para Jev (Jev poda lo de más; nadie recupera lo omitido).
  5. **Método:** una corrida no basta (con el mismo prompt, biomar1 dio 13 y 7 filas no-dato); medir con réplicas, regresión y un texto de reserva con gold previa que no escriba quien diseña el prompt.

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
2. **Datos por subtema** (prompt vigente `datos_pABQ5`): una llamada por subtema con el **documento completo numerado** y el **foco** (las oraciones del subtema, seguidas o separadas); el LLM devuelve `{"datos": [{"variable", "valor", "unidad_de_medida"}]}`.

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

- **Prompt vigente: `datos_pABQ5`** (P14, escrito por Frat). Base `prototipos/base3.md` + ejemplos 1–4: números con unidad, tiempo de un hecho, cualidades (Q, dichas aparte o pegadas al nombre) y un ejemplo con un solo dato (lago Azul, frente a lo que creían los pescadores). Respecto de lo anterior: F salió (mezclaba cinco fenómenos y empujaba a «dato = número»); la Variable debe entenderse sin leer el documento (aspecto, de qué es, circunstancias del documento que hagan falta para identificarlo); el Valor conserva cuantificadores y matices, admite cualidades dadas por comparación; la Unidad vale para cantidades con o sin cifra (millones → unidad; siglos → siglo); «No son datos» suma las relaciones nombradas con sustantivo (origen, fuente, método), los adjetivos que identifican o clasifican y el contenido de creencias, hipótesis o posibilidades.
- **Rondas P5–P14 (oxi1, 28-09):** GLM 5.3 Flash se abstiene de más (3–5 datos, aun en `high`); DeepSeek osciló entre 5 y 18 datos con ABF y variantes. Gold de oxi1 validada por Frat (`unidades/gold/oxi1.json`, 18 datos) sobre la salida de P11 (`datos_pABQ2`, que la reprodujo completa). **P14 (`pABQ5`): 9 datos, los 9 en la gold, ninguno de más**; faltan los que las decisiones de `pABQ3`–`5` excluyen a propósito (lo que se creía: «prácticamente todo», «décadas»; fuente; método «electrólisis»; «nombre del fenómeno»; todo el foco 3: «crítico», «ambientales», «gran escala», «masiva»). La gold es anterior a esas decisiones: hay que reconciliarlas.
- **Antecedente (P1–P4): `datos_pAB`** (429 palabras) y **`datos_pABF`** (525; + prototipo F, ver P4) = `prototipos/base.md` (definiciones y «No son datos» de `datos_u10` + línea de formato) + dos ejemplos prototípicos: **A** número con unidad (medida, conteo con «unidad», porcentaje) y **B** fecha u hora de un hecho. Pendiente de guardar como `datos_u11` cuando Frat lo apruebe.
- **Definiciones vigentes** (desde `datos_u9`): Documento; Foco (conjunto de oraciones de las que se extraen los datos; el resto del documento solo sirve para saber a qué se refiere cada expresión); Variable (aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor; se nombra con aquello a lo que pertenece y sus circunstancias); Valor (cantidad —medida, conteo, fracción, fecha, hora— o cualidad; lo vago o aproximado conserva su cuantificador); Unidad de medida (la unidad en que se expresa un número; null si el valor no lleva número); Dato (variable + valor + unidad). **No son datos:** lo que solo afirma o niega (su valor sería sí o no), las relaciones entre cosas, los adjetivos del nombre y los enunciados genéricos. La sección se llama «No son datos», no «Reglas»: solo excluye.
- **Prototipos (P1, Grok, batería de 15 textos, 29 datos):** k0 (sin ejemplos) 19/29, A 23/29, AB 29/29 y ABC, ABCD, ABCDE también 29/29. Los 10 fallos de k0 fueron todos de convención de unidad («cajas» por «unidad»; null por «fecha» u «hora»); ningún falso dato en ninguna configuración. Decidir que no hay nada fue lo más caro (1175–1957 tokens por texto).
- **Documentos reales (P2, Grok, contra `datos_u10`):** tec1 igual (9 datos, 58 s); oxi1 mejor (recupera «millones», 6 datos); bio1 casi igual (14 datos, 93 s frente a 118): vuelve «especie más abundante = pez loro»; pierde «finos» y los metales; saca «hora = al mediodía» de una medición. ABE quedó incompleto (créditos de xAI agotados en bio1); en oxi1 no mejoró a AB.
- **DeepSeek (P3):** con AB bien en informes (bio1 mejor que u9, 96 s; tec1 gana «lunes» pero saca «filtro = saturado»); en el ensayo oxi1 sacó de más (17 datos, 24 773 tokens): lo que se creía, lo que podría pasar, comparaciones, lugares y el tono del autor. **P4:** prototipo **F** (negativo de ensayo: lo que se creía, lo que podría pasar y una comparación, junto a un dato real) → `datos_pABF` (525 palabras) con DeepSeek sobre oxi1: de 17 a 9 datos, de 106 a 71 s y de 24 773 a 16 316 tokens; desaparecen creencias, hipótesis, comparaciones, lugares y tono, y el foco 3 queda vacío (1688 tokens frente a 10 279). Quedan «fuente del oxígeno = proceso electroquímico geológico» (tesis explicativa, pendiente 7) y «forma del oxígeno = libre». Candidato para ensayos: ABF.
- **Texto genérico (ENC9, DeepSeek, `datos_pABQ5` sobre evals1):** un texto metodológico lleno de números y cuantificadores pero sin casos individuales. 5 de 6 focos vacíos; rechazó «100 %», «dos expertos», «un cambio a la vez», los nombres de los comandos y «alta/baja variación»; el único dato fue «cantidad de ejemplos… = algunos» (zona gris). ChatGPT, aplicando el prompt a mano, llegó a lo mismo salvo ese dato. Los tokens de razonamiento se dispararon justo en los focos con bordes (2173–3310 frente a 457–879). «Un cambio a la vez» es un principio de método (OFAT) que el texto anuncia como tal (or. 5), no una propiedad del comando. «Algunos ejemplos» y la or. 5 son metadiscurso (el texto hablando de sí mismo); DeepSeek extrajo del primero y no de la segunda; los dos resultados son correctos (decisión del metadiscurso, abajo).
- **Rondas ENC10–ENC14 (29/30-09, DeepSeek):**
  - **banrep1** (informe de pronóstico, ENC10): 5 datos, todos dentro de la propuesta de ChatGPT (8); omitió la fecha de la reunión, «menos favorable» y la presuposición del 12,0 %.
  - **biomar1** (divulgación, ENC11): 31 filas; ~8 datos firmes y ~13 no-dato (límites de profundidad de las zonas, «dos categorías», genéricos de clase, adjetivos que clasifican, valoraciones fabricadas).
  - **A = `datos_pABQ6A`** (genéricos también en singular + valores que definen una clase): sin efecto claro; los límites de las zonas siguieron.
  - **B = `datos_pABQ6B`** (= A + sin la pregunta generadora; el dato exige atribución a algo individual en un aspecto que el texto determina; no se inventa aspecto para alojar una valoración). Réplicas r1–r3 (ENC14): gen1 (reserva, volcanes, gold previa de Cowork) 6/6 firmes y **0 de más** en las tres (pABQ5: 2·1·2); biomar1 no-dato media **6** (5·5·8) frente a **10** (13·7·10), firmes 7/8 en ambas; banrep1 sin diferencia (ruido). Regresión sin pérdidas (oxi1 idéntico, evals1 «algunos», cont1 7/7).
  - Sin resolver por ninguna versión: los límites de profundidad de las zonas y «dos categorías» (constantes de la definición). «Colosales masas» de CO₂ se perdió en 5 de 6 corridas con ambas versiones.
  - Golds provisionales: `gold/biomar1.json` (desarrollo, escrita después de ENC11), `gold/gen1.json` (reserva), `gold/cont1.json` (contrastes de ChatGPT).
- **Formato:** `variable` (completa: caso, circunstancias y método cuando define qué se midió), `valor` (literal, sin la unidad), `unidad_de_medida`.
- **Historia corta:** definiciones largas (`u3`–`u4`) → seudodatos; solo ejemplos (`u5`) → mejor; definiciones cortas + ejemplos nodo (`u6`–`u7`) → 39/39 en ut1–ut5; documento completo + foco (`u8`); definiciones reestructuradas, «No son datos», genéricos y cantidades vagas (`u9`); fecha de un hecho es dato (`u10`); prototipos mínimos (`pAB`).

### Decisiones de Frat sobre qué es dato (DU5–P4)

- **Texto genérico sin datos es resultado correcto** (ENC9): el dato es de un caso, no de una clase; las generalizaciones y reglas de un texto metodológico son garantías (nivel de los argumentos), no datos. No se amplía «dato» para que entren.
- **La pertinencia sale del extractor, sin excepción** (29-09): el extractor reinscribe toda determinación bien formada que el texto presenta como hecho, dentro de su alcance; la pertinencia respecto de la práctica (ensayo l. 121, también en los bordes) la juzga Jev después. Principio operativo en §5.
- **Constante de la definición frente a valor** (29-09, IMPORTANTE, decisión de Frat): la pregunta de prueba es **¿podría haber sido otro el valor sin que cambiara qué es el caso? Si no, es una constante de la definición**, no un dato («un aspecto sin diferencias es una constante», §5). Ej. (biomar1): «la Zona Epipelágica se extiende hasta los 200 metros» define la capa (constante); «temperaturas que oscilan entre 1 y 4 grados» en la zona abisal es un valor empírico. Borde asociado: la referencia a clases con singular definido («el plancton se divide…», Carlson 1977) es genérica aunque no lo parezca.
- **El metadiscurso no es criterio** (29-09), ni a favor ni en contra: el texto puede ser caso. «Cantidad de ejemplos de esos comandos que el artículo mostrará al cerrar = algunos» (evals1) es dato; el futuro se conserva (atribución presente, contenido futuro: el anuncio es un compromiso del autor sobre su propio texto, verificable en el mismo documento, no una creencia). La or. 5 no da dato por razones propias: el orden de las partes es una relación, y «partes del artículo = 2» exigiría un conteo que el texto no dice.
- **Modo de una acción no es propiedad del objeto:** «mejorar… un cambio a la vez» es el método de la acción (excluido con las relaciones), no un atributo del comando, a diferencia de «capacidad del tanque = 30000 litros». Además es un principio general (OFAT) que el texto anuncia como tal (or. 5): una garantía, no un dato. ChatGPT lo defendió como dato; no se aceptó.
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
- **Dato:** determinación registrada de modo recuperable. Una misma determinación en dos inscripciones es un solo dato («contar filas es contar marcas»: distinción tipo/ejemplar). **Información:** el cambio en las respuestas admisibles a una pregunta al considerar un dato.
- **Vocabulario del prompt y del ensayo:** el prompt usa «variable» (magnitud individual) y «unidad de medida»; en el ensayo, la variable es el aspecto y la escala es más amplia (unidades, categorías, orden, precisión). El nombre del campo es interfaz con el modelo, no la teoría; el código o `esquema.json` puede ubicar la unidad dentro de la escala. Las condiciones constitutivas viven hoy dentro de la variable.

### Principio operativo: cadena y terminología (29-09)

- **Subtema:** un asunto nuclear y su desarrollo, en una o varias oraciones del documento, seguidas o separadas.
- **Foco:** ese subtema cuando se entrega al extractor; el resto del documento solo sirve para saber a qué se refiere cada expresión.
- **Caso:** aquello individuado y reidentificable a lo que una atribución le fija un valor; puede nombrarse dentro o fuera del foco, e incluso contenerlo (el artículo en evals1). En el foco no está el caso sino enunciados.
- **Atribución:** la operación (medir, clasificar, aplicar una regla, informar) que fija un valor a una variable de un caso; en el foco está su enunciado.
- **Determinación:** el resultado de la atribución; cierra la pregunta `variable(caso, condiciones) = ?`.
- **Dato:** la determinación registrada de modo recuperable. El documento es su primera inscripción.
- **Salida JSON:** una nueva inscripción del dato, `{variable, valor, unidad_de_medida}`, legible fuera del documento (el caso y las condiciones van comprimidos en la variable). Por eso puede agregar o perder algo.

**Cadena:** Documento (primera inscripción) → subtemas → cada uno pasa a ser foco → en el foco, enunciados → el extractor reconstruye las determinaciones que el documento **presenta como hecho** y que están bien formadas (lo que excluye «No son datos», criterio de alcance) → las registra en una **nueva inscripción** JSON → Jev juzga (a) **identidad**: si la inscripción recupera la misma determinación, sin agregar ni perder, y (b) **pertinencia** respecto de la práctica.

**El extractor no crea el dato: lo reinscribe.** No filtra por pertinencia, ni siquiera en los bordes.

- **Alcance no es ontología:** «número de truchas que los pescadores creían que había en el lago = más de mil» es una determinación bien formada (su caso son los pescadores); el extractor la excluye por alcance (pendiente 7), no porque no sea determinación.
- **Vocabulario partido:** `unidades_v5` dice «subtema»; `datos_pABQ5` dice «unidad temática» y llama «Dato» a la terna (lo que aquí es la inscripción). Es interfaz con el modelo; se unifica en la próxima ronda que toque el prompt (pendiente 2).

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

- **El ruido entre corridas puede ser tan grande como el efecto** (ENC13–14): con el mismo prompt, biomar1 dio 13 y 7 filas no-dato. Cada `rN` corre también su paso 1; comparar prompts con el mismo `rN` (pareado).
- **Un prompt preciso en un género puede no serlo en otro:** sin falsos en informes y ensayos, muchos en divulgación que describe clases.
- **El singular definido nombra clases** («el plancton», «la zona abisal»; Carlson 1977): un genérico que no parece genérico.
- **Una pregunta que va del valor a la variable fabrica variables** («grado de delicadeza = delicado»): confirma la lección de la pregunta como fuga.
- **Un texto sin datos mide una sola cara del extractor** (ENC9; evals1 conserva un dato tras la decisión del metadiscurso): que no invente. Un prompt que siempre devolviera vacío sacaría 100 %; vale junto a un gold con datos (oxi1).
- **Hipótesis H1 (no probada): los tokens de razonamiento delatan los bordes.** En ENC9 se dispararon justo en los focos que el análisis previo marcó como riesgosos, pero son seis focos y una corrida. Confusor posible: esos focos son también los que traen números o cuantificadores en la superficie. Si se confirma, sería una señal barata para mandar a revisión (como la franja central de Jev).

## 7. Pendientes

**Suspendidos (30-09)** hasta el nuevo enfoque de la sesión que empieza desde cero; se conservan como referencia.


1. **Reconciliar la gold de oxi1** con las decisiones de `datos_pABQ3`–`5` (creencias, fuente, método, adjetivos que clasifican, foco 3) y con el principio operativo (§5): se excluye por forma o alcance, nunca por pertinencia. Con la gold actual, P14 da 9/18 sin falsos; con la reconciliada se sabrá cuánto falta de verdad.
2. **Unificar el vocabulario de los prompts** («subtema» frente a «unidad temática»; «Dato» como terna) en la próxima ronda que toque `datos_pABQ*`; no justifica una ronda propia.
3. **Paso 1 con el método de prototipos:** batería corta, curva de ejemplos, medir tokens; resolver la fragmentación de Grok en informes (tec1) y su lentitud. En evals1 el subtema 1 salió con dos asuntos pegados.
4. Prueba de verdad de la cadena: documento ajeno con gold escrito antes de correr, más desordenado (tablas, abreviaturas, rangos, negaciones, fechas), del tipo que recibirá Zettel; de preferencia un ensayo, con un anuncio metadiscursivo con cantidad (la decisión del metadiscurso se tomó viendo la salida). Probar `pABQ5` también en un informe (tec1 o bio1).
5. Nivel de **tema** (unión de subtemas relacionados) para Zettel: embeddings proponen candidatos, Jev juzga.
6. Zona gris (terreno de Jev, no del prompt): «finos», composición con valores de tipo («níquel, cobalto y manganeso»), «millones», hora de una medición, superlativos (dato de segundo orden).
7. Frontera entre dato y afirmación (creencias, hipótesis, tesis explicativas): niveles 1 y 2 del grafo de Zettel.
8. Escala: documentos largos (ventanas superpuestas, partición recursiva).
9. Jev: auditoría de los datos, graduación de confianza, canonicalización de variables, reidentificación de casos entre textos, procedencia como capa propia.
10. H1 (§6), solo si llega a importar para Jev: repetir focos con y sin números en la superficie.
11. Grok sin créditos de xAI: recargar antes de volver a compararlo.
