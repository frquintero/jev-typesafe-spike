# AGENTS.md — reglas operativas del ejecutor

Ejecutores: Muse Code (lo carga solo), GPT-6 Luna (Codex lo carga solo; en el
chat de ChatGPT, leerlo al empezar) y Claude Code (`CLAUDE.md` apunta aquí).

Frat y Cowork planean; el ejecutor corre lo que el plan indica, informa con
números y crudos, y no decide diseño, prompts, umbrales ni veredictos. El
spike no concluye.

## Faro: el objetivo de Zettel

Todo lo que se hace aquí sirve a un objetivo: construir un **ecosistema de
unidades temáticas y datos** sobre el que operen **preguntas** y se obtenga
**información**. Información, en el marco, es el cambio en el conjunto de
respuestas admisibles a una pregunta, A(Q), cuando se consideran datos
conforme a reglas; no es un pasaje que se trae. **Recuperar no es
responder.** Cada unidad, dato, extractor o prueba se juzga por lo que
permite hacer a una pregunta. Detalle y ejemplo: `README.md`, «Visión»;
definición: `definiciones-del-marco.md`, A.8.

## Principio de trabajo

Lo único fijo, o casi fijo, es el marco filosófico (`marco filosófico/`) y lo
que se deriva directamente de él. Planes, arquitecturas, niveles, versiones de
prompts y anotaciones son ideas en desarrollo, no ley: antes de tomarlas como
base, validar que sigan vigentes y que se relacionen con lo que se está
haciendo. El camino se hace al andar.

**Proyectos en curso.** El `README.md` de la raíz lista los proyectos que se
trabajan («Fecha: AAAA-MM-DD · Proyecto: … (carpeta)»), solo como
referencia, no como bitácora. Si infieres o detectas que se está trabajando
un proyecto nuevo (carpeta nueva, línea de trabajo nueva en un mensaje o en
`memoria de trabajo y pendientes.md`), agrégalo a esa lista en el mismo
commit; si un proyecto se cierra o se suspende, quítalo. En el mismo
commit, actualiza también el «Mapa del repo» de este archivo y «Dónde
quedamos» en `memoria de trabajo y pendientes.md`: el mismo hecho vive en
los tres sitios.

## Arranque de cada sesión

1. `git status --short` + `git log --oneline -5` (rama de trabajo: `main`).
2. Leer `memoria de trabajo y pendientes.md`: fuente única del estado. No
   duplicarlo en ningún otro archivo.
3. Leer la sección de la ronda indicada en `unidades/PLAN.md` (o en el
   `PLAN.md` que indique el mensaje).
4. `diccionario.md` y `jev_typesafe_guia_pedagogica_v2.md` son el vocabulario
   de Jev; releer solo si la ronda cita una sección.
5. `definiciones-del-marco.md` es el vocabulario del marco (ensayo «¿Qué es un
   dato?») y las definiciones operativas del spike; ningún prompt redefine sus
   términos.

## Mapa del repo

- `unidades/`: **hilo activo**. Extracción de datos en dos pasos.
  - Paso 1, unidades temáticas: `extraer_unidades.py` (guarda el crudo y
    verifica; solo reporta). Con `{{TEXTO_NUMERADO}}` en el prompt (v3) numera
    las oraciones, reconstruye las unidades y verifica huecos, solapes y orden.
  - Paso 2, datos por unidad: `extraer_datos_u.py` (una unidad suelta; solo
    orquesta).
  - Cadena completa: `extraer_datos_doc.py` (paso 1, pegamento en código,
    paso 2 una llamada por unidad, crudos por unidad y consolidado
    `cache/doc-…json`).
  - `docs/` (sintéticos), `prompts/` (se leen de archivo; `{{TEXTO}}` o
    `{{TEXTO_NUMERADO}}` con `str.replace`, nunca `str.format`), `gold/` (esperado, escrito antes de
    correr; el de ut1-ut5 está en la sección DU5 de `PLAN.md`), `cache/`
    (crudos), `PLAN.md` (una sección por ronda), `mensaje_<RONDA>.txt` (mensaje
    de cada ronda para el ejecutor).
- `prototipos/`: banco de prueba del paso 2 (ejemplos prototípicos).
  `base.md` + `ejemplos/<letra>.md`; `bateria.json` (textos cortos con su
  respuesta); `correr.py <modelo> <rN> [configs]` (crudos en `cache/`,
  idempotente) y `evaluar.py <modelo> <rN>` (sin API). Rondas en
  `prototipos/PLAN.md`; los prompts candidatos armados van a
  `unidades/prompts/datos_p<letras>.md`.
- `niveles/`: antecedente sin trabajo activo. Su `run_niveles.py` tiene
  `call_model` (streaming) y los alias de modelos que usan los scripts de
  `unidades/`.
- `probes/` + `cache/`: spike Jev original. Casi todos los scripts son
  autocontenidos; las baterías exponen `run` (idempotente) y `analyze` (sin
  API).
- `cutoff-spike/`: `run_cutoff.py smoke|coarse|coarse2|all`,
  `analyze.py v1|v2|delta|all`. No editar sus JSON de sondas sin releer su PLAN.
- `notebooklm-spike/`: exploración independiente de NotebookLM como
  extractor alternativo o complementario a DeepSeek. Vía vigente: cliente
  `notebooklm-py` (sesión web de la cuenta principal de Frat, perfil
  `nblm-spike`; sin gcloud, ADC ni clave de API). La vía Cloud Enterprise
  quedó **detenida por costo** — no retomarla sin autorización expresa de
  Frat. Sesión/cookies/tokens siempre fuera del repo. **Solo ejecución
  local (Muse):** la sesión no se transfiere a la nube.
  Detalle en su propio `README.md`/`PLAN.md`/
  `tareas.md`.
- `nblm-grafo-semantico/`: arquitectura mixta, paso 1 (subtemas) con
  DeepSeek y paso 2 (datos por unidad) con NotebookLM, cada unidad como
  fuente aparte en un cuaderno. Calibración del paso 1 en NotebookLM,
  opcional. Mismas
  reglas que `notebooklm-spike/` (solo local, bajo volumen).
  Estado en su `README.md` y `tareas.md`.
- `langextract-spike/`: frente **cerrado** el 03-10 (LangExtract de Google,
  evaluado y no adoptado); lección en su `README.md`, ideas rescatables en
  el `README.md` de la raíz.
- `proxy_local.py`: proxy de claves retirado el 04-10 (se conserva como
  antecedente; ya no se usa).
- `dsh_tarea.sh`: delega una tarea a DeepSeek Harness por terminal y avisa
  por ntfy.sh al terminar (ver «DeepSeek Harness por terminal»).
- `muse_tarea.sh`: lo mismo con Muse Code (ver «Muse como agente por terminal»).
- `deleted/`: snapshots históricos; no es fuente.
- Documentos vivos (no editar sin aprobación): `README.md`, `definiciones-del-marco.md`, `diccionario.md`,
  `jev_typesafe_guia_pedagogica_v2.md`.

## Comandos

- `python3 unidades/extraer_unidades.py <doc> <modelo> <prompt> <rN>`
- `python3 unidades/extraer_datos_u.py <doc> <modelo> <prompt> <rN>`
- `python3 unidades/extraer_datos_doc.py <doc> <modelo> <prompt_unidades> <prompt_datos> <rN>`
- `python3 prototipos/correr.py <modelo> <rN> [configs]` · `python3 prototipos/evaluar.py <modelo> <rN>`
- `python3 probes/<x>.py` · `python3 probes/<bateria>.py run|analyze`
- `python3 -m py_compile <archivo>` tras tocar código (no hay tests ni lint).
- Todos los scripts son idempotentes: si el crudo existe, no vuelven a llamar.
  **Nunca borrar, mover ni sobrescribir un crudo** para forzar una corrida:
  una réplica nueva lleva un `rN` nuevo (`r2`, `r3`…). Si el mensaje pide un
  `rN` que ya existe, detenerse y reportar.
- Al terminar una corrida: commit y push de los crudos (y del script si
  cambió) a `main`.

## Red y claves (regla dura)

Desde el 04-10 no hay proxy de claves (decisión de Frat: el código no
necesita correr igual en la nube y en el PC).

- Las llamadas a modelos pasan por `call_model` (`niveles/run_niveles.py`),
  que lee la clave del entorno según el host y la pone en `Authorization`;
  sin la variable, no pone cabecera. Ningún otro código lee claves.
- Claves: `TYPESAFE_API_KEY` (api.typesafe.ai), `ZAI_API_KEY` (api.z.ai),
  `DEEPSEEK_API_KEY` (api.deepseek.com), `XAI_API_KEY` (api.x.ai). Viven en
  `~/.bashrc` (ZAI en `~/.config/zai/api_key.env`); los shells no
  interactivos no las cargan solos: correr con `bash -ic '…'`.
- **Una clave nunca se imprime, ni se escribe en crudos, reportes, logs o
  mensajes.** Los crudos guardan el cuerpo de la petición, no las cabeceras.
- Verificar presencia sin imprimir valores:
  `bash -ic 'for v in TYPESAFE_API_KEY ZAI_API_KEY DEEPSEEK_API_KEY XAI_API_KEY; do
  [ -n "${!v}" ] && echo "$v: SET" || echo "$v: MISSING"; done'`
- **Muse usa la suscripción Muse Code Everyday, nunca pago por uso.**
  `META_API_KEY` ya no se carga en las terminales (línea comentada en
  `~/.bashrc`; el archivo sigue en `~/.config/meta/api_key.env`): no
  cargarla ni pasarla a Muse. Frat arranca Muse con `muse` (alias de
  `command muse --disable-sandbox`: red completa y `.git` escribible; las
  aprobaciones siguen). Sin terminal:
  `command muse exec --disable-sandbox --prompt-file <archivo>` (el flag va
  después de `exec`).
- Las sondas viejas de `probes/` y `cutoff-spike/` arman sus propias
  cabeceras sin clave (pensadas para el proxy retirado); si se reanudan, se
  pasan por `call_model` o se les agrega la clave del mismo modo.
- Si una llamada falla por autenticación, **detenerse y reportar**; no buscar
  la clave por otros medios.

## DeepSeek Harness por terminal (dsh headless)

**Regla dura.** Comunicarse con DeepSeek Harness por `dsh headless`
requiere **autorización expresa y previa de Frat** en cada caso, y es
**exclusivo de Claude (Cowork o Claude Code) y ChatGPT (Luna)**. Muse u
otro agente no lo usan. Sin autorización, no se envía nada.

Pasos técnicos (en el PC de Frat; desde Cowork, con Desktop Commander, no
con el shell aislado):

1. Binario: `D=~/.npm/_npx/1e7f6d9597241db0/node_modules/.bin/dsh` (o
   `npx @deepseek-ai/dsh`). El Harness usa
   su propia clave en `~/.dsh/` (no leerla).
2. Ejecutar siempre **desde la raíz del repo**: una sesión solo se retoma
   desde la carpeta donde se creó.
3. Escribir el mensaje en un archivo temporal **fuera del repo** (p. ej.
   `/tmp/dsh_msg.txt`) y pasarlo por stdin con `-` (evita problemas de
   comillas).
4. **Crear una sesión** (solo si no hay una vigente):
   `$D headless --json - < /tmp/dsh_msg.txt > /tmp/dsh_out.jsonl`.
   El primer evento trae `"sessionId":"session-…"`; anotarlo en el README
   («Sesión de trabajo vigente»). Su primer mensaje carga el contexto
   (AGENTS.md, README, memoria, reportes pertinentes).
5. **Continuarla:**
   `$D headless --session-id <id> - < /tmp/dsh_msg.txt > /tmp/dsh_out.txt 2>/tmp/dsh_err.txt`.
   La respuesta final va a stdout; el razonamiento y los diagnósticos, a
   stderr. Con `--json`, stdout trae los eventos (texto, uso de tokens,
   fin de turno) y el final en `{"type":"final",…}`.
6. Tareas largas: lanzarlo en segundo plano (`nohup … &`) y leer los
   archivos de salida al terminar; las llamadas de Desktop Commander tienen
   tiempo límite.
7. Al leer la respuesta, descartar las líneas de razonamiento que a veces
   se filtran al final del texto (en inglés).

**Delegar sin quedarse esperando: `dsh_tarea.sh` + aviso por ntfy.sh**
(vigente desde el 03-10). Para mandar a DeepSeek a investigar, programar o
probar mientras la conversación con Frat sigue:

- `./dsh_tarea.sh <etiqueta> <archivo_mensaje> [<session-id>|nueva]`
  (raíz del repo). Lanza `dsh headless` en segundo plano y devuelve el
  control al instante. Sin tercer argumento usa la sesión vigente, guardada
  en `~/.config/dsh_tarea/sesion`; `nueva` crea otra (su id queda en el
  `.json` de la tarea; si pasa a ser la de trabajo, actualizar ese archivo y
  el README).
- Al terminar DeepSeek, el envoltorio deja en `~/.cache/dsh_tareas/`:
  `<etiqueta>.out` (respuesta), `.err` (razonamiento y diagnósticos),
  `.json` (`session_id`, `exit`, `segundos`) y `.msg` (copia del mensaje), y
  publica en ntfy.sh el aviso `"<etiqueta> exit=<código> <segundos>s"`. Una
  etiqueta ya usada se rechaza (no sobrescribe).
- **El aviso no lo manda DeepSeek:** el envoltorio corre `dsh` y, cuando
  ese proceso termina, ejecuta un `curl` a ntfy.sh. ntfy.sh reenvía el
  aviso al instante a quien esté suscrito al tema.
- **El tema es privado:** su nombre aleatorio vive solo en
  `~/.config/dsh_tarea/ntfy_topic` (0600). El repo es público: nunca
  escribir el tema en el repo, en mensajes ni en reportes. Por ntfy.sh solo
  viaja el aviso; las respuestas no salen del PC.
- **Cómo se entera Claude (Cowork):** al empezar, lee el tema con Desktop
  Commander (`cat ~/.config/dsh_tarea/ntfy_topic`) y arma una vigilancia
  (herramienta Monitor, en la nube) suscrita al flujo del tema:
  `curl -s -N https://ntfy.sh/<tema>/raw`, una línea por aviso; vence a los
  30 min y se rearma. Con el aviso, lee `<etiqueta>.out` con Desktop
  Commander. Mientras tanto no consulta nada.
- **Cómo se entera ChatGPT (Codex):** Codex no tiene un mecanismo que lo
  despierte con un evento externo (su `notify` solo avisa a la persona
  cuando Codex termina un turno). Opciones: lanzar la tarea y, cuando
  convenga, revisar si existe `~/.cache/dsh_tareas/<etiqueta>.json`; o
  esperarla bloqueando:
  `until [ -f ~/.cache/dsh_tareas/<etiqueta>.json ]; do sleep 5; done`.
  ChatGPT en el chat web no tiene shell local y no usa este canal.

Restricciones (código de `@deepseek-ai/dsh-headless`): rechaza toda
sesión con preset de agente (todas las creadas en la ventana web llevan
«standard»; un `--patch` no lo evita), las de subagentes y las de otra
carpeta. Una sesión creada por terminal puede abrirse luego en la ventana
web, pero no conviene usar las dos a la vez (bloqueo `session.lock`).

El mensaje dice qué hacer y qué no (por defecto: solo lectura, sin
commit, sin llamar a APIs de modelos) y pide respuesta corta. Lo que
DeepSeek responde es un reporte de ejecutor: se verifica contra los
crudos antes de tomarlo como hecho.

## Muse como agente por terminal (muse_tarea.sh)

Misma regla dura que DeepSeek Harness: **autorización expresa y previa de
Frat** en cada caso; **exclusivo de Claude y ChatGPT**.

- `./muse_tarea.sh <etiqueta> <archivo_mensaje> [<uuid>|nueva]` (raíz del
  repo). Lanza `muse exec` en segundo plano y devuelve el control al
  instante. Sin tercer argumento usa la sesión de `~/.config/muse_tarea/sesion`;
  `nueva` crea una con un uuid propio (Muse acepta el id que le damos con
  `--session-id`, así que siempre se conoce).
- Cómo corre Muse: suscripción Everyday (el envoltorio además quita
  `META_API_KEY` por si acaso), `--disable-sandbox`, **`--disable-approval`**
  (decisión de Frat, 04-10: sin terminal no hay quién apruebe), `--json`,
  tope de tiempo `MUSE_TAREA_TIMEOUT` (1800 s por defecto) y
  `MUSE_NO_AUTO_UPDATE=1`. **Una sola tarea de Muse a la vez:** un candado
  rechaza la segunda (código 3).
- Deja en `~/.cache/muse_tareas/`: `<etiqueta>.out` (texto final, del evento
  `run_terminal`), `.jsonl` (eventos), `.err`, `.json` (`session_id`, `exit`,
  `segundos`) y `.msg`. Una etiqueta ya usada se rechaza.
- Aviso: el mismo tema privado de ntfy.sh que `dsh_tarea.sh`, con prefijo
  `muse:` (`"muse:<etiqueta> exit=<código> <segundos>s"`). Claude lo recibe
  con la misma vigilancia; ChatGPT revisa o espera el `.json`.
- Códigos de salida de `muse exec`: 0 turno completo (no garantiza que el
  trabajo esté bien), 1 fallo o cancelación (incluye tope de pasos), 2 error
  de uso, 124 tope de tiempo (`timeout`), 130/143 señales.
- Una sesión nueva no sabe nada del proyecto: el primer mensaje le pide leer
  `AGENTS.md`, la memoria y lo que la tarea necesite. Lo que Muse reporta se
  verifica contra los archivos antes de tomarlo como hecho.
- Reparto sugerido: DeepSeek para investigar, razonar y verificar; Muse para
  implementar y correr.

## Modelos

- `grok` = `grok-4.7` (`reasoning_effort: "low"`, `stream_options` con
  `include_usage`). En xAI `completion_tokens` no incluye `reasoning_tokens`.
- `deepseek` = `deepseek-flash` (thinking, `reasoning_effort: "low"`). Su
  razonamiento va dentro de `completion_tokens`. Puede dejar el stream
  colgado: si pasa un minuto sin datos, reportarlo.
- `flash` = `glm-5.3-flash`; Z.ai tarda ~50 s aun en llamadas mínimas.
- Jev: `jev-1.13.0` fijo (ver abajo).
- Comparar siempre el modelo efectivo de la respuesta con el esperado y avisar
  si difiere.

## Protocolo Jev (para cuando se use)

`POST https://api.typesafe.ai/v1/systemone`, sin SDK (`urllib` + dicts):

```python
body = {
    "model": "jev-1.13.0",   # fijo; avisar si usage.model no coincide
    "state": ...,            # el expediente: string, dict o array
    "questions": {
        "q1": {              # claves neutras; el modelo no las usa
            "type": "noul" | "choice" | "score",
            "instructions": "...",       # el juicio (Noul) o el marco (Choice/Score)
            "criteria": {...} | [...],   # solo Choice/Score
        },
    },
}
```

- **Noul:** un juicio → grado 0–1, leído por bandas; la franja 0,30–0,65 es
  señal de diseño.
- **Choice:** juicios alternativos sin orden; siempre con opción de salida.
- **Score:** juicios como niveles ordenados; `score` = posición media.
- Varias preguntas en una llamada se resuelven en paralelo (fan-out): no cambia
  el resultado, solo la latencia. Sin `temperature`: la estabilidad se mide con
  réplicas (`r1`/`r2`/`r3`; respiran ±0,01–0,02).

## Reportes

- Prompts y campos enviados, verbatim (regla 22). El JSON `parsed` tal como
  llegó, el crudo detrás de cada afirmación.
- Sin veredicto (regla 15); sin mecanismos inventados para un grado concreto
  (regla 26); solo documentos sintéticos (regla 20).

## Lecciones operativas

- El costo dominante es la deliberación del ejecutor, no la API (salvo modelos
  con razonamiento largo): pasos grandes y en paralelo; no re-verificar lo que
  la salida ya mostró.
- `pgrep -af` vuelca entornos completos: usar `pgrep -x` o sondas de puerto.
