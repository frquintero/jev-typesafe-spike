# Smoke notebooklm-py — py-r4

Intento autorizado (sección «Ronda py-r4» de `notebooklm-spike/PLAN.md`; réplica de py-r3 sin `idempotent=True` en `add_text`), iniciado a las 20:24:32 UTC del 2026-10-02 (15:24:32 Bogotá; `summary.json`: `started_utc`). **S0–S3 incompleto: S0, S1 y S2-ask pasaron; detenido por comprobación fallida en S2-passage-1.**

## Procesos y pasos finales

- Proceso principal: `completed: false`, paso final `S2-passage-1` (`cache/py-r4/summary.json`).
- Reconexión S3 (proceso hijo): no se lanzó; no existe `cache/py-r4/reconnect-summary.json`.

## Tiempos (líneas que imprimió el script; coinciden con `summary.json`)

- `S0-notebook`: 0,525 s.
- `S0-limits`: 0,272 s.
- `S1-create`: 0,370 s.
- `S1-add-text`: 1,787 s.
- `S1-ready`: 0,488 s.
- `S1-fulltext`: 0,353 s.
- `S2-ask`: 9,331 s.
- `S2-passage-1`: 0,329 s.
- Total hasta el error: 14,381 s.

## Peticiones HTTP

10 peticiones, todas HTTP 200 (`summary.json`: `http_requests`; `cache/py-r4/http-*-request.json` / `http-*-response.json`):

1. `GET /?authuser=0` (S0-open): 200, 499.233 bytes en 0,550 s; cuerpo no guardado (HTML de arranque con datos de cuenta/sesión).
2. `POST /_/LabsTailwindUi/data/batchexecute` `rpcids=rLM1Ne` (S0-notebook): 200, 5.695 bytes en 0,471 s; cuerpo en `http-02-response.txt`.
3. `POST …/batchexecute` `rpcids=ZwVcOc` (S0-limits): 200, 320 bytes en 0,267 s; cuerpo en `http-03-response.txt`.
4. `POST …/batchexecute` `rpcids=CCqFvf` (S1-create): 200, 388 bytes en 0,366 s; cuerpo en `http-04-response.txt`.
5. `POST …/batchexecute` `rpcids=izAoDd` (S1-add-text): 200, 421 bytes en 1,783 s; cuerpo en `http-05-response.txt`.
6. `POST …/batchexecute` `rpcids=rLM1Ne` (S1-ready): 200, 5.766 bytes en 0,395 s; cuerpo en `http-06-response.txt`.
7. `POST …/batchexecute` `rpcids=hizoJc` (S1-fulltext): 200, 5.644 bytes en 0,304 s; cuerpo en `http-07-response.txt`.
8. `POST …/batchexecute` `rpcids=khqZz` (S2-ask, preparación): 200, 141 bytes en 0,313 s; cuerpo en `http-08-response.txt`.
9. `POST …/LabsTailwindOrchestrationService/GenerateFreeFormStreamed` (S2-ask, consulta generativa): 200, 20.620 bytes en 8,991 s; cuerpo en `http-09-response.txt`.
10. `POST …/batchexecute` `rpcids=hizoJc` (S2-passage-1): 200, 5.645 bytes en 0,273 s; cuerpo en `http-10-response.txt`.

Cero mutaciones reintentadas. S3 no emitió peticiones.

## S0: cuaderno leído y cupos

Cuaderno leído (`cache/py-r4/S0-notebook.json`, parseado tal como llegó):

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

Cupos (`cache/py-r4/S0-limits.json`, íntegro):

```json
{
  "notebook_limit": 500,
  "source_limit": 300,
  "raw_limits": [6, 500, 300, 500000, 2],
  "tier": 2
}
```

No hay otros campos de cupos en el crudo; los ausentes constan como ausentes.

## S1: cuaderno creado y fuente cargada

Cuaderno nuevo (`cache/py-r4/S1-create.json`):

- ID: `bdcc07c8-a114-4a86-bb95-3c57e256b993`.
- Título: `NBLM-SMOKE-001 py-r4 2026-10-02T20:24:32.303236+00:00`.
- `sources_count: 0` al crearlo; sesión de chat `19f40a45-26d1-4b2e-97eb-4ce930706931`.

Fuente cargada (`cache/py-r4/S1-add-text.json`): ID `0e063965-f331-4bf5-b2c3-4e4de17128cb`, mismo título que el cuaderno, `word_count: 19`, `status: 2`. El `NonIdempotentRetryError` de `py-r3` ya no aparece; la carga emitió su petición (n.º 5) y devolvió 200.

Texto recuperado (`cache/py-r4/S1-fulltext.json`, `content` verbatim): «En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.» (`char_count: 131`). Los cuadernos de `api-r1`, `py-r2` y `py-r3` se conservan; no se reutilizó ninguno.

## S2: respuesta con cita; comprobación fallida en el pasaje

Respuesta (`cache/py-r4/S2-ask.json`, campo `answer`, verbatim):

```text
El recipiente Luma contenía **17 fichas** de color **violeta** [1].

💡 ¿Te gustaría saber más información sobre las fichas del recipiente Neri o algún otro detalle de este ensayo?
```

Referencia (`S2-ask.json`, única entrada de `references`):

- `source_id`: `0e063965-f331-4bf5-b2c3-4e4de17128cb` (la fuente cargada en S1).
- `citation_number`: 1; `chunk_id`: `a74ffb67-d278-4076-9d07-6f6620d85b0c`; `score`: 1.0; `start_char`: 0, `end_char`: 131.
- `cited_text` (verbatim): «En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.»

Pasaje recuperado (`cache/py-r4/S2-passage-1.json`, verbatim): «En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.»

Comprobaciones S1–S2 (`summary.json`, campo `checks`):

- `fulltext_matches`: true.
- `answer_contains_17`: true.
- `answer_contains_violetas`: false (la respuesta dice «violeta», en singular).
- `citation_matches_uploaded_source`: true.
- `retrieved_passage_supports_answer`: true.

## S3: no ejecutado

Comprobaciones `notebook_id_matches`, `source_content_matches`, `history_recovers_question_answer`: no evaluadas; no existe `reconnect-summary.json`.

## Error y su paso

Paso `S2-passage-1` (`summary.json`, campo `error`, verbatim):

```json
{
  "type": "RuntimeError",
  "step": "S2-passage-1",
  "message": "S2 content/citation check failed"
}
```

La detención ocurre después de recuperar el pasaje (10 peticiones emitidas, todas 200), al evaluar las comprobaciones de contenido/cita. Sin reintento ni cambio de código, sesión o réplica, según el plan. Se conservan `py-r1`, `py-r2`, `py-r3` y todos los crudos anteriores.

## Entradas enviadas

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

`cache/py-r4/` contiene las diez peticiones con sus metadatos de respuesta, los cuerpos redactados de las nueve RPC (`http-02/03/04/05/06/07/08/09/10-response.txt`), `S0-notebook.json`, `S0-limits.json`, `S1-create.json`, `S1-add-text.json`, `S1-ready.json`, `S1-fulltext.json`, `S2-ask.json`, `S2-passage-1.json`, `inputs.json` y `summary.json`. Sin `reconnect-summary.json`. Sin cookies, tokens ni cabeceras privadas en los crudos.

Comando ejecutado (sin proxy, como fija el plan):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/smoke_py.py py-r4 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

No se corrió `notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el archivo de sesión.
