# AGENTS.md — reglas operativas del ejecutor

Ejecutores: Muse Code (lo carga solo), GPT-6 Luna (Codex lo carga solo; en el
chat de ChatGPT, leerlo al empezar) y Claude Code (`CLAUDE.md` apunta aquí).

Frat y Cowork planean; el ejecutor corre lo que el plan indica, informa con
números y crudos, y no decide diseño, prompts, umbrales ni veredictos. El
spike no concluye.

## Arranque de cada sesión

1. `git status --short` + `git log --oneline -5` (rama de trabajo: `main`).
2. Leer `memoria de trabajo y pendientes.md`: fuente única del estado. No
   duplicarlo en ningún otro archivo.
3. Leer la sección de la ronda indicada en `unidades/PLAN.md` (o en el
   `PLAN.md` que indique el mensaje).
4. `diccionario.md` y `jev_typesafe_guia_pedagogica_v2.md` son el vocabulario
   de Jev; releer solo si la ronda cita una sección.

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
  `notebooklm-py` (sesión web de la cuenta gratuita; sin gcloud, ADC ni
  clave de API). La vía Cloud Enterprise quedó **detenida por costo** — no
  retomarla sin autorización expresa de Frat. Sesión/cookies/tokens
  siempre fuera del repo. **No probado desde Work Cloud:** el proxy local
  y la sesión del PC no se transfieren; hace falta configurar un acceso
  autorizado aparte. Detalle en su propio `README.md`/`PLAN.md`/
  `tareas.md`; no usa las credenciales de `proxy_local.py`.
- `proxy_local.py`: inyecta `Authorization` según host. `muse.sh`: arranque
  de Muse con el proxy.
- `deleted/`: snapshots históricos; no es fuente.
- Documentos vivos (no editar sin aprobación): `README.md`, `diccionario.md`,
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

- El código del repo **nunca** arma `Authorization` ni lee `*_API_KEY`.
  Solo `Content-Type` + `User-Agent: spike-jev/1.0`.
- Claves: `TYPESAFE_API_KEY` (api.typesafe.ai), `ZAI_API_KEY` (api.z.ai),
  `DEEPSEEK_API_KEY` (api.deepseek.com), `XAI_API_KEY` (api.x.ai). Viven en
  `~/.bashrc` (ZAI en `~/.config/zai/api_key.env`) y solo las lee el proxy.
- Verificar presencia sin imprimir valores:
  `bash -ic 'for v in TYPESAFE_API_KEY ZAI_API_KEY DEEPSEEK_API_KEY XAI_API_KEY; do
  [ -n "${!v}" ] && echo "$v: SET" || echo "$v: MISSING"; done'`
- Frat arranca Muse con `muse` (alias de `muse.sh`); Cowork puede lanzarlo sin
  terminal con `./muse.sh exec --prompt-file <archivo>`. `muse.sh` levanta el
  proxy en 127.0.0.1:8080 si no corre, lanza Muse con `--disable-sandbox`
  (red completa y `.git` escribible; las aprobaciones siguen) y apaga el proxy
  al salir. **No arrancar otro proxy** ni inspeccionar el entorno de su proceso.
- En cada comando que llame a una API, exportar antes:
  `export HTTPS_PROXY=http://127.0.0.1:8080
  SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem`.
  No exportarlas de forma global: el tráfico propio de Muse no pasa por el proxy.
- Si una llamada falla por autenticación, **detenerse y reportar**; no buscar
  la clave por otros medios.

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
