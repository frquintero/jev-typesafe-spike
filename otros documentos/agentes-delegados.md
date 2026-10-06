# Agentes delegados: DeepSeek Harness, Muse Code, NotebookLM y Jev

> **Copia del original** que vive en `~/Claude-memoria/memoria/agentes-delegados.md`
> (traída el 06-10-2026). Para Claude y ChatGPT manda el original; el §1 es el mismo en
> los dos (delega el ORQUESTADOR que designe Frat, actualizado el 06-10-2026). Si
> cambia el original, se vuelve a copiar aquí.

Documento único sobre los agentes a los que **el modelo de LLM que Frat denomine
ORQUESTADOR** les delega trabajo en el iMac de Frat. Los `README.md` y `AGENTS.md` del
repo apuntan a la copia. Creado 2026-10-04.

## 1. Regla de uso (vale para todos)

- **Autorización expresa y previa de Frat** para cada uso. Sin ella no se
  envía nada.
- **Solo delega el ORQUESTADOR** (el modelo de LLM que Frat denomine así).
  Ningún otro agente lanza a otro agente.
- Cada mensaje dice qué hacer y qué no (por defecto: solo lectura, sin
  commit, sin llamar a APIs de modelos) y pide respuesta corta.
- **Lo que un agente reporta se verifica** contra los archivos o las fuentes
  antes de tomarlo como hecho.
- Git en los repos de Frat: solo con Desktop Commander (ni siquiera
  `git status` desde el shell aislado de Cowork: deja `index.lock`).
- Ninguna clave, token, cookie ni el nombre del tema de ntfy se escribe en
  un repo, reporte o mensaje.

## 2. Los tres, de un vistazo

(Jev, el cuarto, juzga en vez de hacer; tiene su propia sección, la 7.)

| | DeepSeek Harness | Muse Code | NotebookLM |
|---|---|---|---|
| Qué es | agente de DeepSeek (`deepseek-flash`, razonamiento alto) con herramientas: archivos, shell, búsqueda web | agente de Meta (Muse Spark) con herramientas: archivos, shell, git | cuaderno de Google (Gemini) sobre fuentes cargadas; su chat es un agente interno (piensa, busca, ejecuta código) |
| Papel | investigar, razonar, verificar | implementar y correr | procesar fuentes (extraer, tablas); en evaluación |
| ¿Agente delegable? | sí | sí | **no del mismo modo**: es una herramienta que se usa por script; no recibe tareas sobre el repo ni conserva conversación entre corridas |
| Cómo se lanza | `dsh_tarea.sh` | `muse_tarea.sh` | scripts de Python del repo |
| Aviso al terminar | ntfy.sh | ntfy.sh | no (el script termina y devuelve) |
| Costo | API de DeepSeek (barata) | suscripción Muse Code Everyday (límite semanal) | cuenta Pro de Frat; bajo volumen |
| Velocidad medida | 4–120 s por tarea corta o investigación | 12–20 s por tarea corta | 29 s (tabla); 144 s (ficha por chat) |

## 3. ntfy: el canal de avisos

### Qué es

ntfy («notify») es un servicio de avisos por HTTP, de código abierto: un
programa publica un mensaje corto en un **tema** (un nombre, como un canal
de radio) y todos los que están suscritos a ese tema lo reciben al
instante. Publicar es un `curl -d "texto" https://ntfy.sh/<tema>`;
escuchar es mantener abierta una conexión a `https://ntfy.sh/<tema>/raw`
(o usar sus apps). Usamos el servidor público `ntfy.sh`: no pide cuenta ni
instalación. Fuentes: docs.ntfy.sh y su FAQ.

Lo que hay que saber del servidor público (FAQ oficial):

- **Los temas son públicos: el nombre del tema es la contraseña.** Quien lo
  conozca puede leer y publicar. Por eso el nuestro es un nombre aleatorio
  largo y solo vive en `~/.config/dsh_tarea/ntfy_topic` (0600).
- Los mensajes quedan en caché en el servidor **12 horas** por defecto.
- Es de código abierto y se puede montar un servidor propio, con usuarios y
  permisos (ACL), si alguna vez hiciera falta más privacidad.
- Hay apps para Android (Google Play, F-Droid), iOS (App Store) y una
  versión web.

### Cómo lo usamos

```
tu iMac                                   nube (Cowork)
-------                                   -------------
dsh_tarea.sh / muse_tarea.sh
  └─ corre al agente en segundo plano
  └─ cuando el agente termina:
     curl -d "<etiqueta> exit=0 93s" ──►  ntfy.sh ──► Monitor de Claude ──► aviso en la conversación
```

- **Quien publica es el envoltorio, no el agente:** el envoltorio corre al
  agente y, cuando ese proceso se cierra, ejecuta el `curl`. Mensaje:
  `"<etiqueta> exit=<código> <segundos>s"` (Muse lleva prefijo `muse:`).
- **Solo viaja el aviso.** Las respuestas, los razonamientos y los archivos
  se quedan en el iMac (`~/.cache/dsh_tareas/`, `~/.cache/muse_tareas/`);
  quien recibe el aviso los lee allí. Nunca publicar contenido del trabajo,
  claves ni rutas sensibles en el tema.
- **Si ntfy.sh no responde**, el aviso se pierde pero la tarea no: el
  resultado y su `.json` quedan igual en disco (el `curl` falla en silencio,
  con tope de 15 s).

### Integración con el Monitor de Claude (Cowork)

Monitor es una herramienta de Claude que corre un script en la nube y
convierte cada línea que el script imprime en un aviso dentro de la
conversación, sin que Claude tenga que preguntar. Procedimiento:

1. Leer el tema en el iMac con Desktop Commander:
   `cat ~/.config/dsh_tarea/ntfy_topic`.
2. Armar el Monitor (descripción: «avisos de tareas DeepSeek y Muse vía
   ntfy»; tiempo máximo 30 min):
   ```bash
   while true; do
     curl -s -N --max-time 1700 https://ntfy.sh/<tema>/raw |
       while IFS= read -r l; do [ -n "$l" ] && echo "terminó: $l"; done
     sleep 2
   done
   ```
3. Lanzar las tareas (`dsh_tarea.sh`, `muse_tarea.sh`) y seguir
   conversando con Frat.
4. Con cada aviso, leer `<etiqueta>.out` con Desktop Commander, verificar y
   resumir.
5. El Monitor vence a los 30 min: rearmarlo solo si quedan tareas en curso.

Un Monitor sirve para todas las tareas a la vez: cada aviso trae su
etiqueta.

**ChatGPT (Codex)** no tiene un equivalente: Codex no puede ser despertado
por un evento externo (su `notify` y sus hooks van de Codex hacia afuera;
verificado el 03-10 en sus docs de hooks y en los issues openai/codex
#15723 y #20312, abiertos). Revisa si existe el `.json` de la tarea o
espera bloqueando: `until [ -f <ruta>.json ]; do sleep 5; done`.

### Otros dispositivos (posible, no configurado)

Como cualquiera suscrito al tema recibe los avisos, Frat podría recibirlos
también, por ejemplo cuando deja una tarea larga corriendo:

- **Celular:** instalar la app ntfy (Android o iOS) y suscribirse al tema
  (servidor `ntfy.sh`). Llega una notificación por cada tarea terminada.
- **Navegador:** abrir `https://ntfy.sh/<tema>` y permitir notificaciones.
- **Escritorio del iMac:** un suscriptor local que convierta cada aviso en
  una notificación del sistema (`notify-send`), por ejemplo con la CLI de
  ntfy (`ntfy subscribe <tema> 'notify-send "$m"'`) o un `curl` como el del
  Monitor.

Cuidado: suscribir un dispositivo exige escribir en él el nombre del tema,
que es la contraseña. Si el tema llega a otras manos, se cambia por uno
nuevo en `~/.config/dsh_tarea/ntfy_topic` (y en el Monitor y los
dispositivos).

## 4. DeepSeek Harness (`dsh`)

**Instalación.** `dsh` 0.2.0-rc.2 vía `npx`; binario
`~/.npm/_npx/1e7f6d9597241db0/node_modules/.bin/dsh`. Datos y clave en
`~/.dsh/` (no leer la clave). App de escritorio propia (pywebview) en
`~/Documentos/Claude/dsh-desktop-app/` (ver `software.md`). No usa proxy.

**Delegar una tarea** (desde la raíz del repo jev-typesafe-spike):

```bash
# el mensaje va en un archivo fuera del repo
ESFUERZO=off|low|high|max ./dsh_tarea.sh <etiqueta> /tmp/mensaje.txt [<session-id>|nueva]
```

- Esfuerzo de razonamiento por tarea: ver §8.

- Sin tercer argumento usa la sesión vigente, guardada en
  `~/.config/dsh_tarea/sesion`: hoy `session-c19a1631-6349-46f8-9b9a-84dd5d7e7ab3`
  (creada el 03-10 en jev-typesafe-spike, con el contexto del proyecto
  cargado). `nueva` crea otra; su id queda en el `.json`.
- Resultado en `~/.cache/dsh_tareas/<etiqueta>.{out,err,json,msg}`: `.out`
  es la respuesta, `.err` el razonamiento y diagnósticos, `.json`
  (`session_id`, `exit`, `segundos`). Una etiqueta usada se rechaza.
- Al leer `.out`, descartar líneas de razonamiento que a veces se filtran al
  final (en inglés).

**Por debajo** (`dsh headless`): crear sesión `dsh headless --json - < msg`
(el primer evento trae `sessionId`); continuar
`dsh headless --session-id <id> - < msg`.

**Restricciones del Harness** (código de `@deepseek-ai/dsh-headless`):
rechaza toda sesión con preset de agente (todas las creadas en la ventana
web llevan «standard»; `--patch` no lo evita), las de subagentes y las de
otra carpeta (hay que lanzarlo desde la carpeta donde se creó la sesión).
No usar la misma sesión a la vez en la terminal y en la ventana web
(`session.lock`).
Comprobado el 04-10: con la app de escritorio abierta, la sesión vigente
falla al instante («already owned by an active write handle»), porque la
app la toma al arrancar aunque no se use; con `nueva` funciona (3 s). Con
la app abierta, delegar en una sesión nueva o en una que la app no tenga.

**Uso probado:** investigaciones con búsqueda web y fuentes exactas en
90–120 s (03-10: monitor en Codex; Muse como agente). Patrón: DeepSeek
busca, Claude verifica unas fuentes y decide.

## 5. Muse Code (`muse`)

**Instalación.** Muse Code 1.4.2, binario `~/.local/bin/muse`. Suscripción
**Muse Code Everyday** (límite semanal); el pago por uso fue eliminado por
Frat el 04-10. `META_API_KEY` ya no se carga en las terminales (línea
comentada en `~/.bashrc`; el archivo sigue en
`~/.config/meta/api_key.env`): nunca cargarla ni pasarla a Muse. Sin proxy
ni `muse.sh` desde el 04-10.

**Interactivo (Frat):** `muse` = alias de `command muse --disable-sandbox`
(red completa y `.git` escribible; las aprobaciones siguen).

**Delegar una tarea** (raíz del repo jev-typesafe-spike):

```bash
ESFUERZO=off|low|high|max ./muse_tarea.sh <etiqueta> /tmp/mensaje.txt [<uuid>|nueva]
```

- Esfuerzo de razonamiento por tarea: ver §8.

- Corre `muse exec --disable-sandbox --disable-approval --json
  --session-id <uuid> --prompt-file …` en segundo plano, sin
  `META_API_KEY`, con `MUSE_NO_AUTO_UPDATE=1` y tope de tiempo
  `MUSE_TAREA_TIMEOUT` (1800 s). **Sin aprobaciones** (decisión de Frat,
  04-10: sin terminal no hay quién apruebe).
- **Una sola tarea de Muse a la vez** (candado; la segunda sale con código 3).
- Sesión vigente en `~/.config/muse_tarea/sesion`: hoy
  `7e5a253d-068c-4713-9fe5-e76bf5c5f196` (creada el 04-10 solo con pruebas:
  **sin contexto del proyecto**; el primer trabajo real debe pedirle leer
  `AGENTS.md` y la memoria). `nueva` crea una con uuid propio (Muse acepta
  el id que le damos).
- Resultado en `~/.cache/muse_tareas/<etiqueta>.{out,jsonl,err,json,msg}`;
  `.out` sale del evento `run_terminal` del JSONL.
- Códigos: 0 turno completo (no garantiza que el trabajo esté bien), 1 fallo
  o cancelación (incluye tope de pasos), 2 error de uso, 124 tope de tiempo,
  130/143 señales, 3 candado ocupado.
- Muse carga `AGENTS.md` del repo en cada sesión (sus reglas de ejecutor).
- Fuente oficial: `muse resume` es interactivo; la continuación sin terminal
  es `muse exec --session-id` (dev.meta.ai/docs/muse-code/extending.md).

## 6. NotebookLM

**Acceso.** Cliente comunitario `notebooklm-py==0.8.4` (API web interna, no
oficial) en `~/.local/share/nblm-spike/venv-notebooklm-py/`; sesión de la
cuenta principal de Frat (Pro, `authuser 0`), perfil `nblm-spike` en
`~/.notebooklm/profiles/nblm-spike/storage_state.json` (0600; nunca leerla,
copiarla ni pasarla a la nube). Sin gcloud ni clave de API. La vía Cloud
Enterprise quedó detenida por costo (no retomarla sin autorización).

**Cómo se usa:** con los scripts del repo jev-typesafe-spike, corridos en
local y sin proxy:
`notebooklm-spike/` (`ficha_nblm.py`, `tabla_nblm.py`, `codigo_r1.py`,
`descargar_artefacto.py`) y `nblm-grafo-semantico/` (`ficha_unidad_nblm.py`,
`fu2_doc_entero.py`, `hitos_flujo.py`). Cada corrida crea un cuaderno nuevo.

**Superficies:** chat (`chat.ask`; reglas largas en `chat.configure`, hasta
10.000 caracteres), tabla de datos (~29 s casi fijos), ejecución de código
(archivo `FILE` que se baja con `descargar_artefacto.py`).

**Lo aprendido (FU1/FU2, 03-10):** el chat es un agente interno (≈43 pasos
de razonamiento, busca, escribe y ejecuta código para revisar su salida):
lento y no controlable (144 s una ficha, frente a 69 s de DeepSeek); a
veces devuelve dos respuestas pegadas; tiende a completar y a no registrar
dudas; el aislamiento por `source_ids` funciona. Detalle en
`jev-typesafe-spike/nblm-grafo-semantico/tareas.md`.

**Reglas:** bajo volumen (una réplica por ronda salvo decisión de Frat);
leer solo los cuadernos que crea cada corrida, no la biblioteca personal;
un fallo de autenticación detiene la corrida (no reintentar). Sin envoltorio
de aviso: el script termina y devuelve.

## 7. Jev (TypeSafe)

**Qué es.** El modelo juez de TypeSafe (`jev-1.13.0`, fijo). No investiga
ni implementa: mira un expediente (`state`) y dice cuánto soporta un juicio
(Noul, Choice o Score). Agregado el 2026-10-04: desde el orquestador es un
agente más, aunque su papel sea juzgar.

**Cómo se llama.** `POST https://api.typesafe.ai/v1/systemone`, sin SDK.
Clave `TYPESAFE_API_KEY` en `~/.bashrc` (scripts con `bash -ic`). El
protocolo completo (cuerpo, tipos de pregunta, bandas, réplicas) vive en
`jev-typesafe-spike/AGENTS.md`, «Protocolo Jev»; el vocabulario, en
`diccionario.md` y la guía pedagógica del mismo repo.

**Papel en Zettel.** Quien consume a Jev es el código, no el usuario: el
orquestador le presenta cada respuesta candidata como juicio sobre el
expediente (datos del corpus más lo traído del mundo) y su banda gradúa el
sostén y el tono de la respuesta. Ejemplo completo en
`jev-typesafe-spike/zettel-vision-operativa.md`.

**Reglas:** las de la sección 1 (autorización previa de Frat); el modelo
efectivo de la respuesta se compara con `jev-1.13.0` y se avisa si difiere.

## 8. Esfuerzo de razonamiento (DeepSeek y Muse)

**Decisión de Frat (04-10):** Claude ajusta el esfuerzo de razonamiento de
cada tarea delegada según lo que la tarea exige. Escala común, variable
`ESFUERZO` de `dsh_tarea.sh` y `muse_tarea.sh`, **obligatoria**: no hay
valor por defecto (los scripts se niegan a correr sin ella); el nivel se
elige en cada corrida y el mensaje al agente lleva una línea con el nivel y
su razón (p. ej., «max: auditar el esquema antes de adoptarlo»). El `.json`
de cada tarea registra el esfuerzo usado. Esta política se lee al arrancar
cada sesión de Cowork (`CLAUDE.md`).

| Nivel | Cuándo | DeepSeek (dsh) | Muse |
|---|---|---|---|
| `off` | Mecánico, sin inferir nada: confirmar conexión, correr un script ya escrito y devolver su salida, copiar o formatear. | `off`: sin razonamiento. | `minimal` (no hay «sin razonar»). |
| `low` | Rutinario, con poco juicio: leer y resumir un archivo, verificar rutas o consistencia entre documentos, búsquedas puntuales. | `low` (en la práctica, como `high`: ver abajo). | `low`. |
| `high` | Implementar, escribir o ajustar un verificador de forma, llenar tablas de una mesa, revisar un documento contra el marco. | `high`. | `high`. |
| `max` | Lo difícil y lo que decide: diseñar casos de prueba, auditar un esquema antes de adoptarlo, investigación compleja. | `max`. | `max` (Muse acepta también `xhigh` y `ultra`; no usados). |

**Cómo funciona.**

- **DeepSeek:** el Harness acepta `reasoningEffort` (off, low, high, max) en
  la configuración del modelo. `dsh_tarea.sh` lo aplica por llamada con
  `--patch ~/.config/dsh_tarea/esfuerzo/<nivel>.yml` (fuera del repo). El
  perfil `headless` no fija nada, así que sin parche corría en `high`.
- **Muse:** `muse exec --reasoning-effort <nivel>` (minimal, low, medium,
  high, xhigh, max, ultra; por defecto high). `none` no está disponible con
  la suscripción («not supported with --provider meta»).

**Lo comprobado (04-10, una réplica por nivel).**

- DeepSeek, acertijo de solución única: `off` respondió en 1 token y
  **falló**; `low`, `high` y `max` acertaron con 220, 248 y 222 tokens de
  salida (4, 5 y 19 s). `low` no ahorra frente a `high` (ya visto en el
  spike: la API trata low como high). Pregunta trivial: `off` sin bloque de
  razonamiento.
- DeepSeek, sesiones: el esfuerzo se aplica por llamada aunque la sesión se
  haya creado con otro (creada en off y continuada en high razonó; creada
  en high y continuada en off no razonó).
- Muse, mismo acertijo: `minimal` 9 s, `low` 12 s, `high` 20 s, `max` 18 s;
  todos acertaron. Su JSON no expone tokens de razonamiento: el efecto solo
  se ve en el tiempo.
- `off` nunca para algo que exija inferir: con DeepSeek falla en lógica
  simple.
