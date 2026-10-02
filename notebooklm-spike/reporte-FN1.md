# Ronda FN1 — ficha_v1 con NotebookLM sobre jardin1

Ronda autorizada (sección «Ronda FN1» de `notebooklm-spike/PLAN.md`), ejecutada
en local sin proxy el 2026-10-02. Sin modificaciones de código. No se corrió
`notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el
archivo de sesión. Todos los crudos anteriores se conservan.

Crudo: `notebooklm-spike/cache/ficha-jardin1-nblm-ficha_v1-r1.json` (único
archivo nuevo de la corrida; el script lo escribió con `open("x")`).

## Resultado

`completed: false`. La pregunta fue rechazada por el servidor antes de obtener
respuesta; no hay ficha que comparar con F5. Sin reintento ni cambio, según el
plan.

Error (`error`, verbatim del crudo y de la salida del script):

```json
{
  "type": "ChatError",
  "message": "Chat request was rejected by the server (status 3). This usually means the request was malformed or too large — most often an over-long question past the server-side size limit; shorten it and try again."
}
```

## Tiempos (líneas que imprimió el script; coinciden con el crudo)

- `crear`: 0,461 s.
- `cargar`: 1,201 s.
- `lista`: 0,285 s.
- `texto`: 0,261 s.
- Etapa `preguntar`: no registró tiempo; falló con el `ChatError` de arriba.
- Total hasta el error (`segundos_total`): 3,519 s.

Referencia F5 (DeepSeek, misma tarea): 126,5 / 102,6 / 113,1 s.

## Fuente

Cuaderno nuevo `c85cac34-bd5d-4042-9b0e-e0a313a4d450`, fuente nueva
`33548a81-8a04-4575-9d65-99260b0022c4` (título `FICHA jardin1 ficha_v1 r1 …`).
Texto cargado: el `jardin1` numerado en 12 oraciones (el `texto_numerado` del
crudo coincide con `unidades/docs/jardin1.md` numerado por
`numerar_oraciones`).

`fuente_igual_al_texto_numerado: false` (tal como lo dejó el script): el texto
completo recuperado con `get_fulltext` no es igual al texto numerado enviado.
El crudo no guarda ese texto recuperado; solo el booleano.

## Pregunta enviada

El `ficha_v1` congelado (`unidades/prompts/ficha_v1.md`) con
`{{TEXTO_NUMERADO}}` reemplazado por «El texto con sus oraciones numeradas es
la fuente de este cuaderno.» (remisión prevista en el plan; `pregunta_enviada`
íntegra en el crudo). Sin ejecución de código ni autoverificación, por
decisión de Frat.

## Respuesta y parseo

Sin respuesta: el crudo no trae `respuesta`, `conversation_id`, `referencias`
ni `raw_response`. En consecuencia:

- `venia_con_cerca: null`, `error_parseo: null` (tal como los imprime el
  script; `extract_json` no llegó a correr).
- Verificación (`verificar` de `ficha_doc.py`): no evaluada; el resumen
  impreso por el script no trae `fragmentos`, `no_literales`,
  `listas_faltantes` ni `conteo`. Salida impresa verbatim:

```json
{
  "completed": false,
  "error": {
    "type": "ChatError",
    "message": "Chat request was rejected by the server (status 3). This usually means the request was malformed or too large — most often an over-long question past the server-side size limit; shorten it and try again."
  },
  "segundos_total": 3.519,
  "etapas": {
    "crear": 0.461,
    "cargar": 1.201,
    "lista": 0.285,
    "texto": 0.261
  },
  "fuente_igual_al_texto_numerado": false,
  "venia_con_cerca": null,
  "error_parseo": null
}
```

- Largo de la respuesta en caracteres: no aplica (sin respuesta).
- Marcas tipo `[n]`, negritas o texto fuera del JSON: no aplica (sin
  respuesta; nada que citar).
- Número de referencias: 0 (sin respuesta; el crudo no trae `referencias`).

## Comando ejecutado (sin proxy, como fija el plan)

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/ficha_nblm.py jardin1 ficha_v1 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Salida de `HTTPS_PROXY`/`SSL_CERT_FILE` no exportadas; el comando las quita
con `env -u`. Sin cookies ni tokens en el crudo ni en este reporte.
