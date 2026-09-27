# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 27-09-2026 (tras DU5). No es bitácora: solo lo vigente. La historia está en `git log` y en los `PLAN.md`.

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

**Configuración** (detalle en el README, «Correr las pruebas con Muse Code»):
- `muse.sh` (alias `muse` en `~/.bashrc`) levanta el proxy de claves si no corre, arranca Muse sin sandbox en la carpeta actual y apaga el proxy al salir si lo arrancó él.
- Las reglas del ejecutor viven solo en `AGENTS.md`. Muse y Codex (donde corre Luna) lo cargan solos; en el chat de ChatGPT, Luna lo lee porque cada mensaje empieza con «Lee AGENTS.md». `CLAUDE.md` es una línea que apunta ahí (`@AGENTS.md`).
- Claves: `proxy_local.py` las inyecta por host (TypeSafe, Z.ai, DeepSeek, xAI); nunca van en archivos del repo.
- Cowork hace git con Desktop Commander, no con el shell aislado (no ve credenciales y deja bloqueos en `.git/`). Para detener procesos, la herramienta `kill_process` de Desktop Commander (`kill` desde la terminal está bloqueado).

## 1. Qué hacemos

Extraer los **datos** de un texto, en el sentido del ensayo de Frat «¿Qué es un dato?», con un LLM, en dos pasos (`unidades/`):

1. **Unidades temáticas:** el LLM agrupa las oraciones del texto alrededor de un núcleo con sus satélites.
2. **Datos por unidad:** una llamada por unidad; el LLM encuentra los datos de esa unidad y los devuelve como `{"datos": [{"variable", "valor", "unidad_de_medida"}]}`.

Después, Jev (`jev-1.13.0`) auditará lo extraído; no empezado.

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

- **Prompt vigente:** `unidades_v2`. Tres pasos (casos; núcleos y satélites; unidades temáticas). Salida por unidad: `nucleo`, `satelites`, `oraciones` literales. Un caso puede ser satélite de más de un núcleo; una unidad puede reunir oraciones no seguidas.
- **Probado** con Grok 4.7 y DeepSeek sobre `tec1` (párrafo = unidad) y `tec2` (párrafos no alineados, unidades no continuas): exacto en los dos, unos 20-35 s. `v2` dio el mismo resultado que `v1` con la mitad de tokens.
- **Abierto:** los casos compartidos entre núcleos (el jarabe en tec1) salen omitidos; los modelos leen «satélite» como componente. No urgente.
- **Límite conocido:** una procedencia cuyo alcance cruza dos unidades se pierde en el paso 2.

## 4. Paso 2: datos por unidad

- **Prompt vigente:** `datos_u5`. Sin definiciones, procedimiento ni reglas: una tarea de una línea («Encuentra los datos de `texto`, como en los ejemplos») y tres ejemplos de dominios ajenos a las unidades de prueba: uno con datos de varios tipos, uno con trampas (modificadores del nombre, relación entre casos, binario, cantidad dentro del nombre, conteo) y uno sin datos (`{"datos": []}`).
- **Formato:** `variable` (la magnitud individual, con su caso y sus circunstancias), `valor` (literal, sin la unidad), `unidad_de_medida` (`null` en los valores cualitativos). Sin campo `caso` ni nivel `unidades`.
- **Unidades de prueba:** `unidades/docs/ut1.md`–`ut5.md` (ut4 no tiene datos: solo hechos). Gold en la sección DU5 de `unidades/PLAN.md`. Ya son **conjunto de desarrollo**: vimos sus fallas y las discutimos, así que no miden generalización.
- **Historia corta:** `datos_u3` (definiciones) dejó seudodatos en ut4; `datos_u4` (valor con tipología cuantitativo/cualitativo, sin condiciones constitutivas) empeoró: «escala» se leyó como nivel de medición y ut4 dio «municipal» y «antiguo». `datos_u5` (ejemplos) dio ut4 vacío, los 13 valores del gold y un dato de más, con ~350–450 tokens de razonamiento (DU4: 900–3250) y ~6 s por unidad.
- **Diferencias de DU5 con el gold**, cada una atribuible a lo que los ejemplos no muestran: «6» sin «de la mañana»; variables sin identificador («camión de reparto» sin el 7, «caldera» sin C-2); «tres cuartos» con `null` (el gold dice «fracción»); «a las 8» como dato aparte («hora de la temperatura») en vez de dentro de la variable.
- **Vigente desde DU7: `datos_u7`** = definiciones de una línea + cinco ejemplos nodo (mediciones, cualidades con aspecto dicho y callado, nombres y relaciones, conteos y proporciones, sin datos). DU6 (sin el aspecto implícito) dio 13/13 valores pero «dolor abdominal»/«tos» sin aspecto; DU7, tres réplicas: **39/39 datos completos**, ut4 vacío en las tres; la única variación entre réplicas es de redacción («temperatura del termostato» / «temperatura marcada por el termostato»), no de contenido. Razonamiento 175–1277 tokens, 3–18 s por unidad. ut1–ut5 quedan saturados como conjunto de desarrollo.
- **Siguiente (en discusión):** los ejemplos deben ser **generales**, no ajustados a las fallas de ut1–ut5. Propuesta: listar desde el marco, sin mirar las unidades de prueba, las formas que puede tomar un dato (cantidad con unidad, conteo, proporción o porcentaje, hora o fecha, ordinal, nominal, caso con identificador, variable con circunstancia) y cubrir cada una en los ejemplos. Para medir generalización hacen falta unidades nuevas con gold escrito antes de correr.

### Decisiones de Frat sobre qué es dato (DU5)

- **Variable = magnitud individual** (VIM4, nota 2: «the radius of circle a is an instance of length»): «peso de la caja», no «peso» con un caso aparte.
- **Valor literal**, tal como aparece en `texto`, sin la unidad: «30000», unidad «litros»; «6 de la mañana», unidad «hora».
- **`unidad_de_medida` en lugar de `escala`:** «escala» es polisémica (el modelo la leía como nominal/ordinal). Los valores cualitativos no tienen unidad de medida: `null`. Los conteos llevan «unidad» (magnitud de dimensión uno).
- **Binarios** (con fiebre, sin fallas, trabado): hechos, no datos. Hay valor cuando la palabra elige entre más alternativas que el sí y el no.
- **Modificadores cualitativos del nombre** (antiguo, municipal): parte del caso. Una **cantidad con unidad** es dato aunque vaya en el nombre («caja de 12 kg» → peso de la caja = 12, kg). Números y códigos sin unidad que identifican (camión 7, cama 12, C-2) son del caso.
- **Circunstancias** («a las 8», «en la noche»): dentro de la variable («temperatura del paciente a las 8»). Una hora es valor cuando responde a «¿cuándo?».

## 5. Marco: qué es un dato (ensayo)

- **Caso:** lo distinguido al observar; unidad individuada y reidentificable que reúne determinaciones. Nombres e identificadores sirven para reidentificarlo (l. 91): forman parte del caso, no son valores.
- **Variable:** aspecto del caso que admite diferencias; tiene un dominio de determinaciones admisibles. Un aspecto sin diferencias es una constante.
- **Escala:** sistema de unidades, categorías, orden, precisión y conversión. El dominio dice qué es admisible; la escala, cómo se expresa (l. 127-133).
- **Valor:** posición o elemento de una escala. No es otro caso: si la respuesta es algo concreto, lo registrado es una relación entre casos.
- **Determinación:** resultado de la atribución de un valor a un caso bajo una variable; **cierra una pregunta** `variable(caso, condiciones) = ?`.
- **Hecho y determinación:** una frase que solo distingue (algo es, una relación existe) registra un hecho, no un dato. Un hecho puede abrir preguntas cuya respuesta sí sería un dato («colinda con el pozo» abre `distancia(pozo, finca) = ?`).
- **Condiciones:** constitutivas (si cambian, cambia la pregunta), de representación, de procedencia.
- **Procedencia:** quien dice o cómo se obtuvo no forma parte del dato; es un dato de otro orden, sobre la ruta (l. 161-163, 293), y pesa en la robustez del sostén.
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

## 7. Pendientes

1. Unidades nuevas de prueba (conjunto reservado) con gold escrito antes de correr, para medir el ~90 % con `datos_u7`.
2. Ronda U4 en curso: `unidades_v3` (paso 1 por tema, segmentación lineal con oraciones numeradas, mismo esquema que el paso 2) sobre tec2 y bio1, y cadena ENC2; implementa Luna. ENC1 (v2) mostró que el paso 1 oscilaba entre tema y entidad (11 065 tokens de razonamiento, 158 s).
3. Casos compartidos entre núcleos en el paso 1.
4. La procedencia como capa propia, incluido su alcance entre unidades.
5. Objetos información y afirmación.
6. Auditoría de Jev sobre los datos; reidentificación de casos entre textos (sin campo `caso`, se recupera en un paso aparte); catálogo único de definiciones (`esquema.json`) y §20.1 del borrador principal.
