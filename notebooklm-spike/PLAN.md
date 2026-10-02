# Smoke de conectividad — NBLM-SMOKE-001

## Alcance vigente desde 2026-10-02: notebooklm-py, cuenta web de Frat (Pro)

Frat eligió `notebooklm-py` y autorizó su adopción y la revisión completa de funciones con propuesta de pruebas iniciales. Paquete base `0.8.4` instalado en entorno exclusivo externo al repo; versión/importación/dependencias comprobadas. Vía: SDK Python, backend Web, sesión externa, sin gastos Cloud. Frat autorizó S0–S3: `smoke_py.py` ejecutó `py-r1`, detenido en S0 por HTTP 302 hacia login con la sesión guardada. Dos GET, cero mutaciones/consultas; S1–S3 pendientes de renovar sesión. Detalle en `reporte-py-r1.md` y `cache/py-r1/`. Inventario y propuesta S0–S10 en `funcionalidades-notebooklm-py.md`; primera secuencia propuesta S0–S3. Dependencia en `requirements-py.txt`.

## Ronda py-r2: S0–S3 con la sesión renovada

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local. Smoke
de conectividad y funcionalidad básica; no mide calidad de extracción ni
compara con DeepSeek.

**Cambios respecto de `py-r1`** (un mismo principio: usar la sesión creada
por la propia librería):

1. Sesión: `~/.notebooklm/profiles/nblm-spike/storage_state.json`, escrita
   por `notebooklm -p nblm-spike login` (cuenta principal de Frat,
   `authuser 0`). El script la lee tal cual; ya no convierte la exportación
   antigua ni recibe `--session-file`.
2. Cuenta fija `ACCOUNT = 0` (antes 1) en la comprobación de la sesión, en
   la ruta del cliente y en `summary.json`.
3. Sin proxy local: NotebookLM no necesita claves; las cookies de Google no
   pasan por 127.0.0.1:8080.

S0 sigue igual que en `py-r1`: abrir la sesión, leer el cuaderno sintético
`f113873f-7fdb-416a-bb83-d429c4a3ce1b` y `settings.get_account_limits`. Ese
cuaderno lo creó `api-r1` con el cliente anterior y Frat lo ve en su cuenta
Pro (sin `authuser` en la URL); leerlo con `notebooklm-py` comprueba lectura
de un cuaderno existente y que la cuenta es la misma. S1 se mantiene: es la
única prueba de que `notebooklm-py` crea y carga.

Se conservan: freno ante cualquier fallo de autenticación (`AUTH_STOP`),
recuperación automática desactivada, sin keepalive, cero reintentos de
429/5xx, registro HTTP redactado, crudos únicos y reconexión (S3) en un
proceso hijo.

**Conjetura:** con la sesión renovada, nuestro Python con `notebooklm-py`
autentica, crea un cuaderno, carga y recupera el texto, responde con cita a
la fuente cargada y reconecta desde otro proceso.

**Entradas (fijas, las de `py-r1`):** `docs/smoke-001.txt` y
`prompts/smoke-001.txt`. Esperado: 17 fichas violetas, con cita a la fuente
cargada y pasaje recuperable. Uso: un cuaderno nuevo, una fuente, una
consulta generativa. El cuaderno se conserva para revisión.

**Antes de ejecutar:**

- Leer `AGENTS.md`, `notebooklm-spike/README.md` y esta sección.
- `git pull --ff-only` sobre una copia limpia de `main`; si no se puede,
  detenerse y reportar. Comprobar que incluye el commit de preparación.
- Comprobar que no existe `notebooklm-spike/cache/py-r2/`. Si existe,
  detenerse y reportar.
- No correr `notebooklm auth check` ni ningún comando que liste cuadernos.
  No leer ni imprimir el archivo de sesión.

**Comando** (desde la raíz del repo; el script lanza solo la reconexión S3):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r2 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si termina con error (`AUTH_STOP`, comprobación fallida, tiempo agotado),
no reintentar ni cambiar código, sesión o réplica: conservar los crudos y
reportar. Cualquier reintento lo deciden Frat y Cowork, con un `rN` nuevo.

**Criterio de éxito (lo comprueba el script):** `completed: true` en
`summary.json` y en `reconnect-summary.json`, con todas las comprobaciones
en `true` — S1–S2: `fulltext_matches`, `answer_contains_17`,
`answer_contains_violetas`, `citation_matches_uploaded_source`,
`retrieved_passage_supports_answer`; S3: `notebook_id_matches`,
`source_content_matches`, `history_recovers_question_answer`.

**Reporte del ejecutor (sin veredicto), en `reporte-py-r2.md`** con el
formato de `reporte-py-r1.md`: hora de inicio; `completed` y paso final de
cada proceso; segundos por etapa (líneas que imprime el script) y total;
número de peticiones HTTP; título e ID del cuaderno leído en S0; cupos devueltos por S0 (los campos ausentes,
como ausentes); IDs de cuaderno y fuente; la respuesta de S2 verbatim; las
referencias (ID de fuente, texto citado) y los pasajes recuperados; el
valor de cada comprobación; el error con su paso, si lo hubo. Citar los
crudos detrás de cada dato. Nada de cookies, tokens ni cabeceras privadas.
Al terminar: commit de `cache/py-r2/` y `reporte-py-r2.md`, y push a
`main`; informar el commit.

## Ronda py-r3: réplica de py-r2 con la corrección del script

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local.

**Resultado de py-r2** (`reporte-py-r2.md`, `cache/py-r2/`): S0 pasó con la
sesión renovada (leyó `f113873f-…`, 1 fuente, `is_owner: true`; cupos
`notebook_limit` 500, `source_limit` 300, `tier` 2). S1 creó el cuaderno
`5eccd8bb-…` y se detuvo en `S1-add-text` con `NameError` sobre `text`:
error del script, no de la API. 4 peticiones HTTP 200, cero consultas.

**Cambio (uno):** en la rama de reconexión, la variable que guarda el texto
recuperado en S3 pasa de `text` a `fulltext3`. Asignar `text` dentro de
`execute` lo volvía local a toda la función y dejaba sin valor el texto de
entrada que usa S1. El error ya estaba en `py-r1`, que no llegó a S1. Nada
más cambia: sesión, entradas, pasos, comprobaciones y frenos son los de
`py-r2`.

**Conjetura, entradas, criterio de éxito y reporte:** los de la ronda
`py-r2`, con `py-r3` en lugar de `py-r2` (carpeta `cache/py-r3/`, reporte
`reporte-py-r3.md`). El cuaderno vacío `5eccd8bb-…` de `py-r2` se conserva;
no se reutiliza.

**Antes de ejecutar:** los mismos pasos de `py-r2`; comprobar que no existe
`notebooklm-spike/cache/py-r3/`.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r3 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si termina con error, no reintentar ni cambiar nada: conservar los crudos y
reportar.

## Ronda py-r4: réplica de py-r3 sin `idempotent=True`

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local.

**Resultado de py-r3** (`reporte-py-r3.md`, `cache/py-r3/`): S0 y S1-create
pasaron; se detuvo en `S1-add-text` con `NonIdempotentRetryError`, antes de
enviar la carga: la librería rechaza `add_text(..., idempotent=True)` porque
el servidor no deduplica textos. Error del script, no de la API. 4
peticiones HTTP 200, cero consultas.

**Cambio (uno):** `add_text` sin `idempotent=True`. La regla de no repetir
mutaciones se mantiene por `RetryOptions` en cero; el título del cuaderno ya
es único (réplica + hora), como recomienda la librería. El detalle n.º 6 de
`funcionalidades-notebooklm-py.md` leía esa opción como protección.

Antes de preparar esta ronda, Cowork contrastó con el paquete instalado las
llamadas restantes de S1–S3 (`wait_until_ready`, `get_fulltext`, `ask` con
`source_ids`, `references`/`source_id`, `resolve_chat_reference_passage`,
`get_history`): firmas y campos coinciden con el script.

**Conjetura, entradas, criterio de éxito y reporte:** los de la ronda
`py-r2`, con `py-r4` (carpeta `cache/py-r4/`, reporte `reporte-py-r4.md`).
Los cuadernos vacíos de `py-r2` y `py-r3` se conservan; no se reutilizan.

**Antes de ejecutar:** los mismos pasos de `py-r2`; comprobar que no existe
`notebooklm-spike/cache/py-r4/`.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r4 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si termina con error, no reintentar ni cambiar nada: conservar los crudos y
reportar.

## Ronda py-r4-S3: reconexión sobre los datos de py-r4

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local.

**Resultado de py-r4** (`reporte-py-r4.md`, `cache/py-r4/`): S0, S1 y S2
ejecutados; 10 peticiones, 14,381 s. Respuesta: «El recipiente Luma contenía
**17 fichas** de color **violeta** [1].» más una sugerencia final; cita [1] a
la fuente cargada; pasaje recuperado. Comprobaciones en `true` salvo
`answer_contains_violetas`, que exigía la forma plural; el script abortó y
no lanzó S3.

**Cambio (uno, para corridas futuras):** la comprobación pasa a
`answer_contains_violeta` y acepta «violeta» o «violetas». No afecta a S3.

**Qué se corre:** solo la reconexión (S3) sobre `cache/py-r4/summary.json`:
otro proceso abre la sesión y recupera el cuaderno de py-r4
(`notebook_id` y `source_id` de su `summary.json`), el texto de la
fuente y el historial. Sin crear cuadernos, sin cargas, sin consultas
generativas. Excepción expresa a la regla de `rN` existente: los archivos
nuevos llevan el prefijo `reconnect-`, se abren en modo exclusivo y no
sobrescriben nada de `py-r4`.

**Antes de ejecutar:** los pasos de `py-r2`, salvo el de la carpeta:
comprobar que existe `cache/py-r4/summary.json` y que no existe
`cache/py-r4/reconnect-summary.json`; si no se cumple, detenerse y reportar.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r4 --reconnect \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

**Criterio de éxito (lo comprueba el script):** `completed: true` en
`cache/py-r4/reconnect-summary.json`, con `notebook_id_matches`,
`source_content_matches` y `history_recovers_question_answer` en `true`.

**Reporte (sin veredicto):** añadir a `reporte-py-r4.md` una sección «S3
(reconexión)» con `completed`, paso final, segundos por etapa y total,
peticiones HTTP, el valor de cada comprobación, el historial recuperado
(pregunta y respuesta verbatim) y el error con su paso, si lo hubo. Si
falla, no reintentar ni cambiar nada. Commit de los archivos `reconnect-*`
y del reporte, y push a `main`.

## Exploración code-r1: ejecución de código (hecha por Cowork)

**Estado:** autorizada por Frat el 02-10-2026 y hecha por Cowork desde Python,
fuera del flujo de rondas del ejecutor (una consulta y una descarga). Detalle
y crudos en `reporte-code-r1.md` y `cache/code-r1/`.

**Pregunta:** ¿la ejecución de código de Gemini Notebook está activa en la
cuenta Pro y su resultado es recuperable desde Python?

**Resultado:** sí. Con la pregunta «Usa código para dividir la fuente en
oraciones numeradas y entrégame un archivo JSON con ellas», NotebookLM
ejecutó Python y creó un artefacto tipo `FILE` (`oraciones-numeradas.json`).
`notebooklm-py` 0.8.4 no descarga ese tipo; `descargar_artefacto.py` extrae
el enlace de descarga de la respuesta cruda del RPC `gArtLc` y lo baja con
la sesión. Dependencia frágil: formato interno no documentado.

**Implicación:** la salida estructurada deja de depender del texto del chat
(negritas, `[n]`, sugerencias). Queda por decidir qué uso del proyecto
probar con esto.

## Ronda FN1: `ficha_v1` con NotebookLM sobre jardin1

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local.

**Pregunta:** ¿sirve NotebookLM como extractor de la ficha? Se le da la misma
tarea que a DeepSeek en F5 y se compara. Sin ejecución de código ni
autoverificación (descartadas por Frat: sin un para qué en esta prueba).

**Igual que F5:** prompt `unidades/prompts/ficha_v1.md` (congelado), documento
`unidades/docs/jardin1.md` (divulgación, 12 oraciones), numeración de
`numerar_oraciones`, `extract_json` y el verificador `verificar` de
`ficha_doc.py`, importados sin cambios.

**Diferencias (las que impone el extractor):**

1. El texto numerado va como **fuente** de un cuaderno nuevo; la pregunta es
   `ficha_v1` con `{{TEXTO_NUMERADO}}` reemplazado por «El texto con sus
   oraciones numeradas es la fuente de este cuaderno.».
2. Modelo no expuesto ni configurable (Gemini Notebook); `chat.ask` con
   `source_ids=[fuente]`, conversación nueva en cuaderno nuevo.

**Conjetura:** NotebookLM devuelve por el chat una ficha JSON parseable con las
siete listas y respaldos literales según nuestro verificador, en menos tiempo
que DeepSeek.

**Referencia F5 (`unidades/cache/ficha-jardin1-deepseek-ficha_v1-r{1,2,3}.json`):**
126,5 / 102,6 / 113,1 s; fragmentos 147 / 114 / 114, no literales 0 / 0 / 0;
ninguna lista faltante. La calidad de contenido se evalúa después con
`unidades/gold/preguntas_reserva_F5.md` (Cowork y Frat), no en esta ronda.

**Script:** `notebooklm-spike/ficha_nblm.py`. Crea cuaderno, carga, espera,
comprueba que la fuente indexada es igual al texto numerado, pregunta una vez,
guarda la respuesta cruda, parsea y verifica. Mismos frenos que py-r2 (sin
reintentos, sin keepalive, recuperación de autenticación desactivada);
`chat_timeout` 600 s. Crudo único, nunca sobrescrito.

**Antes de ejecutar:** `git pull --ff-only` (copia limpia; si no, detenerse);
comprobar el commit de preparación; comprobar que no existe
`notebooklm-spike/cache/ficha-jardin1-nblm-ficha_v1-r1.json`. No correr
`notebooklm auth check` ni listar cuadernos; no leer el archivo de sesión.

**Comando** (desde la raíz):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/ficha_nblm.py jardin1 ficha_v1 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si termina con error (autenticación, pregunta rechazada, tiempo agotado), no
reintentar ni cambiar nada: conservar el crudo y reportar.

**Reporte del ejecutor (sin veredicto), en `reporte-FN1.md`:** ruta del crudo;
`completed` y error si lo hubo; segundos por etapa y total; si la fuente quedó
igual al texto numerado; si la respuesta venía con cerca, error de parseo;
verificación tal como la imprime el script (fragmentos, no literales con sus
rutas, listas faltantes, conteo de las siete listas); largo de la respuesta en
caracteres; si aparecen marcas tipo `[n]`, negritas o texto fuera del JSON
(citar solo lo necesario); número de referencias. Nada de cookies ni tokens.
Commit del crudo y del reporte, y push a `main`.

## Ronda FN2: determinaciones como tabla de datos (jardin1)

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local.

**Resultado de FN1** (`reporte-FN1.md`): el servidor rechazó la pregunta
(`ChatError`, status 3: pregunta demasiado larga; `ficha_v1` ≈ 6.500
caracteres). Sin ficha. Lección (Frat): no calcar el prompt de DeepSeek;
reformular la tarea según la forma de la herramienta.

**Cambios (un principio: usar la forma propia de NotebookLM):**

1. Salida por **tabla de datos** (`artifacts.generate_data_table`, CSV), no
   por el chat.
2. Solo **determinaciones**, el núcleo de la ficha; casos, capas, acciones y
   dudas quedan para después.
3. Columnas con el vocabulario del ensayo: caso de estudio, aspecto, valor,
   unidad, cambio, condición, quién lo sostiene, inferido, oración, fragmento
   literal.
4. Instrucciones breves (seis reglas destiladas de `ficha_v1`), en
   `prompts/tabla_det_v1.md` (≈ 1.800 caracteres).
5. Fuente sin cambios (jardin1 numerado); el script guarda además el texto
   recuperado, para ver en qué difiere (FN1 dio `false` sin guardarlo).

**Conjetura:** la tabla llega como CSV con las diez columnas, una fila por
determinación y fragmentos literales verificables por código.

**Referencia (DeepSeek, F5):** determinaciones de jardin1 en
`unidades/cache/ficha-jardin1-deepseek-ficha_v1-r{1,2,3}.json`: 27 / 23 / 19;
fragmentos no literales 0 en las tres; 102,6–126,5 s por ficha completa. El
contenido se compara después (Cowork y Frat).

**Script:** `tabla_nblm.py` (cuaderno nuevo, carga, espera, pide la tabla,
espera hasta 600 s, baja el CSV, verifica fragmentos). Mismos frenos que
py-r2. Crudos en `cache/tabla-jardin1-nblm-tabla_det_v1-r1/` (`crudo.json`,
`tabla.csv`); la carpeta no puede existir.

**Antes de ejecutar:** `git pull --ff-only` (copia limpia); comprobar el commit
de preparación y que no existe la carpeta de crudos. No correr `notebooklm
auth check` ni listar cuadernos; no leer el archivo de sesión.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v1 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si falla, no reintentar ni cambiar nada: conservar crudos y reportar.

**Reporte (sin veredicto), en `reporte-FN2.md`:** `completed` y error; segundos
por etapa y total; si la fuente quedó igual y, si no, en qué difiere (citar
lo mínimo); columnas recibidas y faltantes; número de filas; fragmentos no
literales con fila, oración y fragmento; el CSV completo si tiene hasta 40
filas (si no, las primeras 15). Commit de los crudos y del reporte, y push.

## Ronda FN3: tabla de determinaciones con ejemplo y regla 7 (jardin1)

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local. **Una
sola réplica** (decisión de Frat: bajo volumen en la cuenta).

**Resultado de FN2** (`reporte-FN2.md`): 29,2 s, 10 columnas pedidas (+ «Fuente»
agregada por NotebookLM), 18 filas, 18/18 fragmentos literales. Análisis de
Frat y Cowork: valores que no se entienden sin contexto («semejante», «allí»;
«más baja» resuelto en el aspecto), aproximador perdido («unos 20» → «20»),
condición repetida en el nombre del caso. DeepSeek r3 comete los mismos
errores en la misma oración; r1 los resuelve.

**Cambios (un principio: cada fila se entiende sola y fiel al texto):**

1. Regla 7: el valor conserva aproximadores y completa comparaciones y
   referencias con un solo antecedente (inferido = sí).
2. Un ejemplo resuelto con la represa (texto de desarrollo, §2.3 de la
   memoria): aproximador, condición fuera del nombre, comparación completada,
   atribución, identificador en el nombre, y «la mitad» sin completar por
   tener dos antecedentes.

Instrucciones: `prompts/tabla_det_v2.md` (v1 + regla 7 + ejemplo). Script,
fuente y frenos iguales a FN2.

**Conjetura:** con la regla 7 y el ejemplo, la tabla conserva «unos 20»,
completa «semejante» y «allí», y deja los casos sin la condición repetida, sin
perder literalidad ni las atribuciones de FN2.

**Criterios fijados antes de correr (los evalúan Cowork y Frat):** (1) «unos
20» conservado; (2) «semejante» completado («semejante a unos 20 litros» o
equivalente); (3) «allí» resuelto; (4) término de comparación de «más baja» en
el valor; (5) casos sin la condición repetida; (6) fragmentos literales
(verificador); (7) atribuciones a Clara Beltrán y condiciones de FN2
mantenidas.

**Antes de ejecutar:** `git pull --ff-only` (copia limpia); comprobar el commit
de preparación y que no existe
`notebooklm-spike/cache/tabla-jardin1-nblm-tabla_det_v2-r1/`. No correr
`notebooklm auth check` ni listar cuadernos; no leer el archivo de sesión.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v2 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si falla, no reintentar ni cambiar nada: conservar crudos y reportar.

**Reporte (sin veredicto), en `reporte-FN3.md`:** el mismo de FN2 (incluido el
CSV completo si tiene hasta 40 filas). Commit de los crudos y del reporte, y
push.

## Ronda FN4: tabla con la forma del marco (jardin1)

**Estado:** autorizada por Frat el 02-10-2026. Ejecuta Muse en local. Una
réplica.

**Resultado de FN3** (`reporte-FN3.md`): 29,5 s, 19 filas, 17/19 literales
(dos filas unen fragmentos con « / »). Resolvió «unos 20», «semejante a unos
20 litros», «allí» y «más baja que…», pero las condiciones bajaron de 5 a 1 y
«demostración» pasó a ser caso. Análisis (Frat y Cowork), tres causas a
corregir juntas:

1. El ejemplo enseñó lo que mostraba: caso = entidad grande con el contenido
   en el aspecto, y condición vacía en 4 de 5 filas.
2. La regla 7 pedía que **el valor** se entendiera solo, contra la decisión
   de que el campo valor guarda solo la posición (y contra el ensayo: ninguna
   marca determina por sí sola).
3. La tabla de datos tiende a una fila por entidad (formato ancho); la nuestra
   es una fila por determinación (formato largo).

**Cambios (un principio: que la tabla tenga la forma del marco):**

1. Ejemplo nuevo (estanque, texto de desarrollo ampliado): el caso es la cosa;
   condiciones en 3 de 5 filas; comparación completada en su columna;
   referencia resuelta sin agregar de más; un «semejante» sin completar por
   tener dos antecedentes.
2. Valor = solo la posición, con aproximadores; columna nueva **respecto de**
   para el término de comparación; la regla de autosuficiencia pasa a la fila
   completa (regla 3).
3. Primera frase «una fila por cada determinación… un mismo caso puede ocupar
   muchas filas» y regla 7 «una determinación por fila». Fragmentos múltiples
   permitidos con « / » (el verificador los separa). «Sin información» y la
   columna «Fuente» son de la plantilla de la herramienta: se ignoran.

Instrucciones: `prompts/tabla_det_v3.md` (≈ 3.900 caracteres). Script: el de
FN2/FN3, con dos ajustes (columnas esperadas leídas de las instrucciones;
fragmentos con « / »).

**Conjetura:** la tabla conserva los logros de FN3 (aproximadores,
comparaciones, referencias) y recupera las condiciones de FN2, con el caso
como la cosa y una determinación por fila.

**Criterios fijados antes de correr (los evalúan Cowork y Frat):** (1) «unos
20» en el valor; (2) «semejante» con «respecto de» = el agua vertida en el
jardín (unos 20 litros); (3) «allí» resuelto; (4) «más baja» con «respecto de»
= el camino; (5) condiciones: «durante una demostración», «cuando llueve»,
«si llega más de la que el terreno admite», solo en su columna; (6) caso = la
cosa, no «demostración»; (7) oración 12 en dos filas; (8) fragmentos
literales; (9) atribuciones a Clara Beltrán; (10) palabras agregadas que el
texto no dice.

**Antes de ejecutar:** `git pull --ff-only` (copia limpia); comprobar el commit
de preparación y que no existe
`notebooklm-spike/cache/tabla-jardin1-nblm-tabla_det_v3-r1/`. No correr
`notebooklm auth check` ni listar cuadernos; no leer el archivo de sesión.

**Comando:**

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v3 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Si falla, no reintentar ni cambiar nada: conservar crudos y reportar.

**Reporte (sin veredicto), en `reporte-FN4.md`:** el mismo de FN2 (incluido el
CSV completo si tiene hasta 40 filas). Commit de los crudos y del reporte, y
push.

## Rediseño tras FN4 (en discusión, 02-10-2026)

**Diagnóstico.** La tabla de un solo paso sobre el texto entero no rinde más:
FN2–FN4 corrigieron fallas puntuales y abrieron otras. Causas comunes: el
modelo decide los casos sobre la marcha; el alcance es el texto entero; un
fragmento por fila no respalda la fila completa; nadie verifica lo que el
modelo marca como inferido. Error de método: se afinaba sobre jardin1, texto
de la reserva de F5.

**Decisión de Frat:** reintroducir los elementos excluidos el 01-10 (ronda
F1: «sin subtemas, sin inventario y sin Jev»), porque ahora se necesitan.

**Propuesta de Cowork (a discutir):**

0. Código: oraciones numeradas (luego, un segmentador real: pySBD o spaCy).
1. Subtemas: `unidades/prompts/unidades_v5.md` (probado con DeepSeek, U7–U9).
2. Inventario de casos de estudio: tabla de datos de NotebookLM, una fila por
   caso (su forma natural), con menciones y oraciones.
3. Determinaciones por subtema: tabla con los casos fijados de antemano y solo
   las oraciones del foco.
4. Respaldo por componente: fragmentos para valor, condición y «respecto de».
5. Verificación: literalidad por código; juicio fino con Jev.

**Método:** construir paso a paso (primero el inventario); ajustar sobre
textos de desarrollo; la reserva de F5 solo mide al final; una réplica por
ronda salvo decisión de Frat.

## Alcance anterior: API oficial Google Cloud (detenido)

**Restricción vigente de Frat (2026-10-02): sin gastos.** Configuración Cloud detenida; no asociar facturación ni activar/comprar suscripciones. El smoke oficial no se ejecutó. Las operaciones anteriores y sus crudos se conservan; no continuar con los pasos de habilitación que siguen documentados históricamente.

Frat precisó que el smoke debe conectar Python a la API oficial de Google Cloud, autenticarse por OAuth y consumirla. `smoke_cloud.py` implementa creación/lectura de notebook y carga/lectura de la fuente sintética usando `google-auth` y credenciales ADC externas al repo. Frat instaló gcloud y configuró ADC; luego eligió crear el proyecto exclusivo «NotebookLM Spike» (`notebooklm-spike-20261002`, número `265423575040`). Ya está ACTIVE; requiere asociación de facturación, habilitación de Discovery Engine y configuración/licencia Enterprise antes del smoke. Endpoint, autenticación y contratos se contrastaron con documentación oficial mediante Exa. La documentación de administración de notebooks no presenta un método de chat/consulta; no se sustituye con endpoints internos.

La corrida anterior de sesión web que sigue documentada abajo no cumple el alcance Cloud. Se conserva sin alterar sus crudos.

Fecha: 2026-10-02. Inicio autorizado por Frat. Solo texto sintético.

## Entrada fijada antes de consultar

- Texto: `docs/smoke-001.txt`.
- Consulta: `prompts/smoke-001.txt`.
- Esperado: Luma contenía 17 fichas violetas; referencia recuperable al pasaje que lo establece.
- Notebook exclusivo de prueba, una única fuente; conservarlo para revisión.

## Pasos y evidencias

1. Comprobar acceso autenticado de lectura.
2. Crear notebook exclusivo con identificador único.
3. Cargar el texto y esperar a que esté disponible.
4. Consultar con el texto exacto del prompt.
5. Recuperar por API la referencia de la cita y el texto de la fuente vinculada.
6. Registrar operaciones, respuestas, tiempos observados y errores sin credenciales ni información de notebooks personales. Preservar cada intento en una carpeta nueva.

## Vías

- Cliente local aislado: `notebooklm-mcp-cli==0.15.0`, instalado fuera del repo en `~/.local/share/nblm-spike/venv/`; perfil previsto `nblm-spike` en almacenamiento externo al repo. El primer intento de login terminó con `Login timeout` tras 300 s; Frat mostró un error de certificado en el Chrome lanzado. No se demostró autenticación del cliente.
- Frat indicó usar el navegador interno y completó allí el inicio de sesión. La prueba por interfaz web se registra por separado: no acredita acceso HTTP autónomo desde Python ni continuidad con el PC apagado.
- La configuración de acceso desde la nube queda para una prueba posterior.

## Corrida HTTP autorizada

Frat pidió ejecutar el smoke de API el 2026-10-02. `smoke_api.py` usa el cliente comunitario como biblioteca y `httpx` como transporte HTTPS. La sesión que Frat inició en el navegador interno se exportó a un archivo privado fuera del repo (directorio 0700, archivo 0600); durante la corrida no se usa control del navegador. Se conserva la cuenta elegida con `authuser=1`, también en la petición de consulta, cuyo cliente HTTP es distinto del empleado por las RPC.

- Réplica: `api-r1`; carpeta exclusiva `cache/api-r1/`.
- Lectura inicial: solo el notebook sintético de la prueba previa; no listar notebooks personales.
- Peticiones: `Content-Type` de formulario y `User-Agent: spike-jev/1.0`; autenticación de sesión gestionada por la biblioteca. Sin claves de API ni construcción de `Authorization` en código del repo.
- Sin transporte CDP, renovación automática de autenticación ni repetición de mutaciones ante fallos. Un fallo de autenticación detiene el intento.
- Proxy y certificado locales exportados solo para el comando de corrida.
- Conservar cuerpos recibidos y `f.req` exacto, omitiendo cookies, `at`, `f.sid` y cabeceras de autenticación; respuestas con eventual información de sesión redactada.
- El resultado de esta corrida se documenta en `reporte-api-r1.md` y en sus crudos; no mide calidad general de extracción ni disponibilidad desde la nube.
