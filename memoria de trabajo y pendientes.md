# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 27-09-2026. No es bitácora: solo lo vigente. La historia está en `git log` y en los `PLAN.md`.

## 0. Dónde y cómo

- **Carpeta:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/` (máquina local de Frat, Linux). Trabajo activo en `unidades/`.
- **Repositorio:** `https://github.com/frquintero/jev-typesafe-spike`, rama `main`.
- **Roles:** Frat y Cowork planean. Muse Code (Meta Muse Spark) ejecuta en local; Claude Code en la nube es la alternativa. El rol va con la tarea, no con el modelo.

**Flujo de una ronda.**
1. Frat y Cowork discuten y conjeturan. Se corre solo si hay una conjetura nueva.
2. Cowork escribe el prompt en `unidades/prompts/` y la sección de la ronda en `unidades/PLAN.md` (cambio, conjetura, comandos, reporte), y hace commit y push.
3. Cowork entrega el mensaje para Muse: Frat lo pega en su sesión, o Cowork lo lanza sin terminal con `./muse.sh exec --prompt-file <archivo>`.
4. Muse corre sin modificar nada, reporta sin veredicto y hace commit y push de los crudos.
5. Cowork lee los crudos (`unidades/cache/`) y los evalúa contra la conjetura. Frat decide.

**Configuración** (detalle en el README, «Correr las pruebas con Muse Code»):
- `muse.sh` (alias `muse` en `~/.bashrc`) levanta el proxy de claves si no corre, arranca Muse sin sandbox en la carpeta actual y apaga el proxy al salir si lo arrancó él.
- Las reglas del ejecutor viven solo en `AGENTS.md`, que Muse carga solo; `CLAUDE.md` es una línea que apunta ahí (`@AGENTS.md`).
- Claves: `proxy_local.py` las inyecta por host (TypeSafe, Z.ai, DeepSeek, xAI); nunca van en archivos del repo.
- Cowork hace git con Desktop Commander, no con el shell aislado (no ve credenciales y deja bloqueos en `.git/`). Para detener procesos, la herramienta `kill_process` de Desktop Commander (`kill` desde la terminal está bloqueado).

## 1. Qué hacemos

Extraer los **datos** de un texto, en el sentido del ensayo de Frat «¿Qué es un dato?», con un LLM, en dos pasos (`unidades/`):

1. **Unidades temáticas:** el LLM agrupa las oraciones del texto alrededor de un núcleo con sus satélites.
2. **Datos por unidad:** una llamada por unidad; el LLM encuentra los datos de esa unidad.

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

- **Prompt vigente:** `datos_u3`. Estructura DEFINICIONES / TAREA / PROCEDIMIENTO / REGLAS / REPORTE. Definiciones: unidad textual, caso (nombres, números y códigos que lo distinguen van dentro del caso), variable (prueba del dominio), condiciones constitutivas, escala (recuperable aunque `texto` no la nombre), valor, dato. Reglas clave: un valor no es otro caso; sin escala no hay dato. Reporta solo unidades con datos.
- **Unidades de prueba:** `unidades/docs/ut1.md`–`ut5.md` (ut4 no tiene datos: solo hechos).
- **Estado (DU3, Grok):** identificadores y condiciones bien; escalas reales; ut4 casi sin datos (queda «antiguo» del «antiguo edificio de la estación»); se perdió «ingresó con fiebre».
- **Siguiente (DU4, propuesto, no decidido):**
  1. variable binaria: «la variable no puede construirse convirtiendo en pregunta de sí o no la afirmación de `texto`», en lugar de «no se reducen a afirmar o negar»;
  2. los modificadores que forman parte del nombre del caso pertenecen al caso.

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

## 7. Pendientes

1. DU4 (los dos ajustes de §4).
2. Encadenar los pasos: correr el paso 2 sobre las unidades que produce el paso 1 (hoy ut1-ut5 se armaron a mano).
3. Casos compartidos entre núcleos en el paso 1.
4. La procedencia como capa propia, incluido su alcance entre unidades.
5. Objetos información y afirmación.
6. Auditoría de Jev sobre los datos; reidentificación de casos entre textos; catálogo único de definiciones (`esquema.json`) y §20.1 del borrador principal.
