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

- `unidades/`: **hilo activo**. Extracción de datos en dos pasos (unidades temáticas →
  datos por unidad). Prompts en `prompts/` (se leen de archivo; `{{TEXTO}}` o
  `{{TEXTO_NUMERADO}}` con `str.replace`, nunca `str.format`), textos en `docs/`,
  esperado en `gold/`, crudos en `cache/`; comandos y rondas en `PLAN.md`.
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
  derivado), plan del orquestador, mesa de dominio, pruebas del paso 1 (`pruebas/`) y
  paso 2 (`paso2/`). **Su estado vive en la memoria**; el detalle, en el `README` o
  `PLAN` de cada subcarpeta.
- `marco filosófico/`: el ensayo «¿Qué es un dato?» y su marco.
- `langextract-spike/`: cerrado (LangExtract, evaluado y no adoptado).
- `utiliarios/`: los guiones que se invocan desde la raíz. `muse_tarea.sh` y
  `dsh_tarea.sh` delegan tareas a Muse y a DeepSeek Harness (ver «Agentes
  delegados»); `configurar_clave_xai.sh` pide la clave de xAI; `proxy_local.py`
  (retirado) se conserva como antecedente. El repo se resuelve como el
  padre de esta carpeta.
- `otros documentos/`: documentos de referencia que no son de navegación: el
  vocabulario de Jev (`diccionario.md`, `jev_typesafe_guia_pedagogica_v2.md`) y los
  informes sueltos (p. ej. `mistral-large-4-verificacion-2026-10-06.md`).
- `deleted/`: snapshots históricos; no es fuente.
- Documentos vivos (no editar sin aprobación): los siete de la raíz (`README.md`,
  `AGENTS.md`, `CLAUDE.md`, `memoria de trabajo y pendientes.md`, `política.md`,
  `definiciones-del-marco.md`, `zettel-vision-operativa.md`) y, en
  `otros documentos/`, `diccionario.md` y `jev_typesafe_guia_pedagogica_v2.md`.

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
  cargar ni pasarle `META_API_KEY`. Cómo se arranca y se delega: `/home/fratquintero/Claude-memoria/memoria/agentes-delegados.md`.
- Las sondas de `probes/` y `cutoff-spike/` arman sus propias
  cabeceras sin clave: si se reanudan, se pasan por `call_model` o se les agrega
  la clave del mismo modo.
- Si una llamada falla por autenticación, **detenerse y reportar**; no buscar
  la clave por otros medios.

## Agentes delegados (DeepSeek Harness, Muse, NotebookLM)

Todo lo de los agentes a los que Claude y ChatGPT delegan trabajo
(`utiliarios/dsh_tarea.sh`, `utiliarios/muse_tarea.sh`, NotebookLM: cómo se lanzan, avisos,
sesiones, ubicaciones y reglas) está en un solo documento, fuera del repo:
`/home/fratquintero/Claude-memoria/memoria/agentes-delegados.md`. Leerlo antes de usarlos. Regla dura: **autorización expresa y
previa de Frat** en cada uso; **exclusivo de Claude y ChatGPT**.

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
