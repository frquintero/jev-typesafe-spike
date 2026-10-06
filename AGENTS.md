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
2. Leer `memoria de trabajo y pendientes.md`: fuente única del estado. No
   duplicarlo en ningún otro archivo.
3. Leer la sección de la ronda indicada en `unidades/PLAN.md` (o en el
   `PLAN.md` que indique el mensaje).
4. `otros documentos/diccionario.md` y
   `otros documentos/jev_typesafe_guia_pedagogica_v2.md` son el vocabulario
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
- `mvp/`: proyecto del MVP de Zettel (desde el 04-10). `mesa1/` y `mesa1b/`: pruebas de mesa
  de la forma de la tabla de A(Q), sin API (resultados en sus `resultado.md`).
  `pieza1/`: Q5 (conflicto) y Q6r (dato derivado) con el esquema 2 candidato
  (mundo = M; K solo capas de la ficha) y `pieza1.py` (verificador de forma,
  comparador, guardar, mantener); estado en `mvp/pieza1/registro.md`. `tensiones-vision-operativa-2026-10-04.md`
  recoge lo acordado y lo propuesto sobre la representación de A(Q), las
  premisas de K, el sostén frente al grado de Jev y el vocabulario operativo.
  Borrador cerrado el 04-10 (lo acordado está en `zettel-vision-operativa.md`
  y `definiciones-del-marco.md`); se conserva como antecedente.
  `orquestador-plan.md`: plan candidato del orquestador, con dos revisiones
  independientes (`orquestador-arquitectura-deepseek-2026-10-04.md`,
  `orquestador-arquitectura-muse-2026-10-04.md`). `mesa-dominio-plan.md`,
  `-materiales.md`, `-referencia.md` y `-resultado.md`: mesa de dominio del MVP
  (T1–T6, ejecutada el 05-10 en comprobación guiada); su cierre sustituyó
  (decisión de Frat, 05-10) el índice de casos previo de §4.1 del plan del
  orquestador por alcance por dominio y reidentificación acreditada al consultar.
  `pruebas/`: pruebas del paso 1 sobre documentos sintéticos; cinco documentos y
  nueve corridas con Muse Code, con entradas, mensajes, salidas y verificaciones.
  Candidato **v9 congelado** como base de trabajo del paso 1.
  `paso2/`: extracción de datos por unidad; comparación de tres entradas (unidad
  sola, unidad con las referencias de v9, unidad con el documento completo) con
  Muse Code y `deepseek-flash`; **entrada elegida y base de trabajo: la unidad más
  las referencias** (100 % de recuperación y 100 % de fidelidad en la reserva, donde
  se aplican las medidas; 85,1 % y 98,2 % en desarrollo, que solo elige la entrada).
  Candidato `prompt_ficha_contexto.md`, corredores y crudos ahí; informe en
  `mvp/paso2/informe_paso2.md`.
- `langextract-spike/`: frente **cerrado** el 03-10 (LangExtract de Google,
  evaluado y no adoptado); lección en su `README.md`, ideas rescatables en
  el `README.md` de la raíz.
- `utiliarios/`: los guiones que se invocan desde la raíz. `muse_tarea.sh` y
  `dsh_tarea.sh` delegan tareas a Muse y a DeepSeek Harness (ver «Agentes
  delegados»); `configurar_clave_xai.sh` pide la clave de xAI; `proxy_local.py`
  (retirado el 04-10) se conserva como antecedente. El repo se resuelve como el
  padre de esta carpeta.
- `otros documentos/`: documentos de referencia que no son de navegación: el
  vocabulario de Jev (`diccionario.md`, `jev_typesafe_guia_pedagogica_v2.md`) y los
  informes sueltos (p. ej. `mistral-large-4-verificacion-2026-10-06.md`).
- `deleted/`: snapshots históricos; no es fuente.
- Documentos vivos (no editar sin aprobación): los siete de la raíz (`README.md`,
  `AGENTS.md`, `CLAUDE.md`, `memoria de trabajo y pendientes.md`, `política.md`,
  `definiciones-del-marco.md`, `zettel-vision-operativa.md`) y, en
  `otros documentos/`, `diccionario.md` y `jev_typesafe_guia_pedagogica_v2.md`.

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
- **Muse usa la suscripción Muse Code Everyday, nunca pago por uso:** no
  cargar ni pasarle `META_API_KEY`. Cómo se arranca y se delega: `/home/fratquintero/Claude-memoria/memoria/agentes-delegados.md`.
- Las sondas viejas de `probes/` y `cutoff-spike/` arman sus propias
  cabeceras sin clave (pensadas para el proxy retirado); si se reanudan, se
  pasan por `call_model` o se les agrega la clave del mismo modo.
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
