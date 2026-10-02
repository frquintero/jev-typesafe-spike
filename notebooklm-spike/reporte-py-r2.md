# Smoke notebooklm-py — py-r2

Intento autorizado (sección «Ronda py-r2» de `notebooklm-spike/PLAN.md`), iniciado a las 20:15:06 UTC del 2026-10-02 (15:15:06 Bogotá; `summary.json`: `started_utc`). **S0–S3 incompleto: S0 y S1-create pasaron; detenido por error del script en S1-add-text antes de cargar la fuente.**

## Procesos y pasos finales

- Proceso principal: `completed: false`, paso final `S1-add-text` (`cache/py-r2/summary.json`).
- Reconexión S3 (proceso hijo): no se lanzó; no existe `cache/py-r2/reconnect-summary.json`.

## Tiempos (líneas que imprimió el script; coinciden con `summary.json`)

- `S0-notebook`: 0,559 s.
- `S0-limits`: 0,255 s.
- `S1-create`: 0,414 s.
- Total hasta el error: 2,177 s (`S1-add-text`).

## Peticiones HTTP

4 peticiones, todas HTTP 200 (`summary.json`: `http_requests`; `cache/py-r2/http-0*-request.json` / `http-0*-response.json`):

1. `GET /?authuser=0` (S0-open): 200, 499.233 bytes en 0,597 s; cuerpo no guardado (HTML de arranque con datos de cuenta/sesión).
2. `POST /_/LabsTailwindUi/data/batchexecute` `rpcids=rLM1Ne` (S0-notebook): 200, 5.695 bytes en 0,502 s; cuerpo en `http-02-response.txt`.
3. `POST …/batchexecute` `rpcids=ZwVcOc` (S0-limits): 200, 320 bytes en 0,25 s; cuerpo en `http-03-response.txt`.
4. `POST …/batchexecute` `rpcids=CCqFvf` (S1-create): 200, 389 bytes en 0,41 s; cuerpo en `http-04-response.txt`.

Cero mutaciones reintentadas, cero consultas generativas. S1-add-text, S2 y S3 no emitieron peticiones.

## S0: cuaderno leído y cupos

Cuaderno leído (`cache/py-r2/S0-notebook.json`, parseado tal como llegó):

```json
{
  "id": "f113873f-7fdb-416a-bb83-d429c4a3ce1b",
  "title": "NBLM-SMOKE-001 · api-r1-2026-10-02T15:59:23.610609+00:00",
  "sources_count": 1,
  "is_owner": true,
  "role": 1,
  "emoji": "🪩"
}
```

Es el cuaderno sintético creado por `api-r1`, con una fuente; la sesión renovada (cuenta `authuser=0`) lo leyó.

Cupos (`cache/py-r2/S0-limits.json`, íntegro):

```json
{
  "notebook_limit": 500,
  "source_limit": 300,
  "raw_limits": [6, 500, 300, 500000, 2],
  "tier": 2
}
```

No hay otros campos de cupos en el crudo; los ausentes constan como ausentes.

## S1: cuaderno creado; fuente no cargada

Cuaderno nuevo (`cache/py-r2/S1-create.json`):

- ID: `5eccd8bb-9ad5-4797-9c05-e51d3b5a579d`.
- Título: `NBLM-SMOKE-001 py-r2 2026-10-02T20:15:06.999327+00:00`.
- `sources_count: 0`; sesión de chat `d5c7ddde-1dab-428c-b4d2-7981f4d13898`.

ID de fuente: ninguno (la carga falló antes de crearla). Se conserva el cuaderno nuevo para revisión, igual que el de `api-r1`.

## S2: no ejecutado

Sin respuesta (nada verbatim que citar), sin referencias, sin pasajes recuperados. Comprobaciones `fulltext_matches`, `answer_contains_17`, `answer_contains_violetas`, `citation_matches_uploaded_source`, `retrieved_passage_supports_answer`: no evaluadas; `summary.json` no trae campo de comprobaciones.

## S3: no ejecutado

Comprobaciones `notebook_id_matches`, `source_content_matches`, `history_recovers_question_answer`: no evaluadas; no existe `reconnect-summary.json`.

## Error y su paso

Paso `S1-add-text` (`summary.json`, campo `error`, verbatim):

```json
{
  "type": "NameError",
  "step": "S1-add-text",
  "message": "cannot access free variable 'text' where it is not associated with a value in enclosing scope"
}
```

Error del propio script al preparar la carga del texto, no de autenticación ni de la API: S0 había autenticado y leído con la sesión renovada. Sin reintento ni cambio de código, sesión o réplica, según el plan. Se conservan `py-r1` y todos los crudos anteriores.

## Entradas previstas, no enviadas

Texto (`docs/smoke-001.txt`, registrado en `inputs.json` y `summary.json`):

```text
En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.
```

Pregunta (`prompts/smoke-001.txt`):

```text
Según la fuente, ¿cuántas fichas contenía Luma y de qué color eran? Incluye la cita que respalda la respuesta.
```

Esperado: 17 fichas violetas con fuente/pasaje recuperables.

## Evidencia y reproducción

`cache/py-r2/` contiene las cuatro peticiones con sus metadatos de respuesta, los cuerpos redactados de las tres RPC (`http-02/03/04-response.txt`), `S0-notebook.json`, `S0-limits.json`, `S1-create.json`, `inputs.json` y `summary.json`. Sin `reconnect-summary.json`. Sin cookies, tokens ni cabeceras privadas en los crudos.

Comando ejecutado (sin proxy, como fija el plan):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r2 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

No se corrió `notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el archivo de sesión.
