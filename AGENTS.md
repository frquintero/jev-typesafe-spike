# AGENTS.md — reglas operativas del ejecutor

## Faro: el objetivo de Zettel

Todo lo que se hace aquí sirve a un objetivo: construir un **ecosistema de
unidades temáticas y datos** sobre el que operen **preguntas** y se obtenga
**información**. Información, en el marco, es el cambio en el conjunto de
respuestas admisibles a una pregunta, A(Q), cuando se consideran datos
conforme a reglas; no es un pasaje que se trae. **Recuperar no es
responder.** Cada unidad, dato, extractor o prueba se juzga por lo que
permite hacer a una pregunta. Detalle y ejemplo: `README.md`, «Visión»;
definición: `definiciones-del-marco.md`, A.8. Cómo lo soñamos de punta a
punta (pregunta, mundo, orquestador, Jev): `zettel-vision-operativa.md`.

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
commit; si un proyecto se cierra o se suspende, quítalo.

**Casa y actualización.** Qué se actualiza, cuándo, y dónde vive cada archivo
(raíz, `otros documentos/`, `utiliarios/`) está en `política.md`. Se lee antes de
mover un archivo o de tocar el estado del repo.

## Arranque de cada sesión

1. `git status --short` + `git log --oneline -5` (rama de trabajo: `main`).
2. Leer `README.md`.
3. Leer `política.md`.
4. Leer `memoria de trabajo y pendientes.md`: fuente única del estado. No
   duplicarlo en ningún otro archivo.
5. Leer `zettel-vision-operativa.md`.
6. `definiciones-del-marco.md` es el vocabulario del marco (ensayo «¿Qué es un
   dato?») y las definiciones operativas del spike; ningún prompt redefine sus
   términos.

## Mapa del repo

- `unidades/`: extracción de datos en dos pasos (unidades temáticas →
  datos por unidad). Prompts en `prompts/` (se leen de archivo; `{{TEXTO}}` o
  `{{TEXTO_NUMERADO}}` con `str.replace`, nunca `str.format`), textos en `docs/`,
  esperado en `gold/`, crudos en `cache/`; comandos y rondas en `PLAN.md`. Rondas
  F1–F5 evaluadas y F6 corrida sin evaluar; `ficha_v1`, congelada.
- `prototipos/`: banco de prueba del paso 2 (ejemplos prototípicos). Rondas y
  comandos en su `PLAN.md`.
- `niveles/`: sin trabajo activo. `run_niveles.py` tiene `call_model` (streaming) y los
  alias de modelos que usan los guiones de `unidades/`.
- `probes/` + `cache/`: spike Jev original.
- `cutoff-spike/`: sondas de ventana y recorte. No editar sus JSON de sondas sin releer
  su `PLAN.md`.
- `notebooklm-spike/`: NotebookLM como extractor alternativo o complementario (cliente
  `notebooklm-py`, sesión de Frat; **solo local**, nunca en la nube). La vía Cloud quedó
  detenida por costo: no retomarla sin autorización. Detalle en su `README`/`PLAN`.
- `nblm-grafo-semantico/`: mixto: subtemas con DeepSeek y datos por unidad con
  NotebookLM, cada unidad como fuente aparte. Mismas reglas que `notebooklm-spike/`.
- `mvp/`: MVP de Zettel. Mesas de la forma de A(Q), pieza 1 (conflicto y dato
  derivado), mesa de dominio, pruebas del paso 1 (`pruebas/`) y
  paso 2 (`paso2/`: ronda cerrada; entrada «unidad + referencias» como base
  provisional, con `README.md` para la vía y la verificación sin API). `corpus/` es la
  **consulta completa**: documentos radicados (`doc4`, `doc6`), la base SQLite, los
  crudos de la extracción y el orquestador (`corpus/consulta/orq/`); **los tres prompts de
  trabajo viven en `mvp/prompts/`** (`prompt_UT`, `prompt_DATOS` y `prompt_ORQ`). Lo
  construido y lo abierto está en `mvp/consulta-diseno.md`, y los procedimientos de la
  extracción, en `mvp/guía_UT.md` (paso 1, unidades temáticas) y `mvp/guía_DATOS.md`
  (paso 2, datos por unidad). **Su estado vive en la memoria**; el
  detalle, en el `README`, `PLAN` o diseño de cada subcarpeta. Sigue: correr prompt 4 (la sonda
  de la herramienta de pregunta) y evaluar las respuestas (`mvp/consulta-diseno.md` §12).
- `test_tool_calling/`: la mecánica del bucle con herramientas en DeepSeek
  (`call_model` con `messages` y `tools`), corrida el 07-10; lecciones en su
  `README.md` y crudos en `cache/`.
- `marco filosófico/`: el ensayo «¿Qué es un dato?» y su marco.
- `langextract-spike/`: cerrado (LangExtract, evaluado y no adoptado).
- `utiliarios/`: los guiones que se invocan desde la raíz. `muse_tarea.sh` y
  `dsh_tarea.sh` delegan tareas a Muse y a DeepSeek Harness (ver «Agentes
  delegados»); `configurar_clave_xai.sh` pide la clave de xAI; `jev.py` arma y envía
  el protocolo de Jev (`seco` no llama a la API); `proxy_local.py` (retirado) se
  conserva como antecedente. El repo se resuelve como el padre de esta carpeta.
- `otros documentos/`: documentos de referencia que no son de navegación: el
  vocabulario de Jev (`diccionario.md`, `jev_typesafe_guia_pedagogica_v2.md`), la
  política de agentes delegados (`agentes-delegados.md`, copia del original que vive
  en `~/Claude-memoria/memoria/`) y los informes sueltos (p. ej.
  `mistral-large-4-verificacion-2026-10-06.md`).
- `deleted/`: snapshots históricos; no es fuente.
- Documentos vivos (no editar sin aprobación): los siete de la raíz (`README.md`,
  `AGENTS.md`, `CLAUDE.md`, `memoria de trabajo y pendientes.md`, `política.md`,
  `definiciones-del-marco.md`, `zettel-vision-operativa.md`) y, en
  `otros documentos/`, `diccionario.md`, `jev_typesafe_guia_pedagogica_v2.md` y
  `agentes-delegados.md`.

## Reglas de corrida

Los comandos de cada proyecto están en su `PLAN.md` o `README.md` (los de `unidades/`,
en `unidades/PLAN.md`).

- Los guiones son idempotentes: si el crudo existe, no vuelven a llamar.
- **Nunca borrar, mover ni sobrescribir un crudo** para forzar una corrida: una réplica
  nueva lleva un `rN` nuevo (`r2`, `r3`…). Si el mensaje pide un `rN` que ya existe,
  detenerse y reportar.
- Tras tocar código: `python3 -m py_compile <archivo>` (no hay tests ni lint).
- Al terminar una corrida: commit y push de los crudos (y del guion si cambió).

## Git y remoto

- **Upstream:** `origin` = `https://github.com/frquintero/jev-typesafe-spike.git`.
  Es la copia pública desde la que se recupera el trabajo (ChatGPT Work consulta
  `main` sin el PC). No hay otro remoto.
- **`main` sigue a `origin/main`** (`branch.main.remote = origin`): `git status -sb`
  lo muestra como `## main...origin/main` con los commits por delante o por detrás.
- El trabajo se hace en `main`. Hay ramas sueltas de otras herramientas que no son la
  rama de trabajo: no se trabaja en ellas.
- `git push origin main` al terminar cada tramo: la obligación y sus excepciones
  están en `política.md` §3.

## Red y claves (regla dura)

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
- **Muse usa la suscripción Muse Code Everyday, nunca pago por uso:** no
  cargar ni pasarle `META_API_KEY`. Cómo se arranca y se delega:
  `otros documentos/agentes-delegados.md`.
- Las sondas de `probes/` y `cutoff-spike/` arman sus propias
  cabeceras sin clave: si se reanudan, se pasan por `call_model` o se les agrega
  la clave del mismo modo.
- Si una llamada falla por autenticación, **detenerse y reportar**; no buscar
  la clave por otros medios.

## Agentes delegados

El modelo de LLM que sea denominado **ORQUESTADOR** por Frat delega trabajo
(`utiliarios/dsh_tarea.sh`, `utiliarios/muse_tarea.sh`, NotebookLM: cómo se lanzan,
avisos, sesiones, ubicaciones y reglas). El documento único, con la regla de uso y el
detalle, está en `otros documentos/agentes-delegados.md`.

**Avisos por ntfy: obligatorio.** El ORQUESTADOR **no espera a un agente con `sleep` ni
sondeando**: lanza la tarea y espera el aviso. El envoltorio publica al terminar en el
tema de `~/.config/dsh_tarea/ntfy_topic` (0600; el tema nunca se escribe en el repo) y
el ORQUESTADOR escucha ese tema (`https://ntfy.sh/<tema>/raw`, o el Monitor de Claude;
procedimiento en `otros documentos/agentes-delegados.md` §3). **Si el agente que va a
usar no publica aviso, el ORQUESTADOR lo implementa —o manda a un agente a
implementarlo— antes de usarlo.** El aviso lleva solo etiqueta, `exit` y segundos; el
resultado se lee donde quedó.
