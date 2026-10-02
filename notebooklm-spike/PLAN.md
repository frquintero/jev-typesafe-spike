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
