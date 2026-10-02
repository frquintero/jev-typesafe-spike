# Ejecución de código en NotebookLM — code-r1

Prueba exploratoria autorizada por Frat el 2026-10-02, hecha por Cowork desde Python (`notebooklm-py` 0.8.4, sesión del perfil `nblm-spike`, sin proxy). Pregunta: ¿la ejecución de código anunciada para Gemini Notebook (antes NotebookLM) está activa en la cuenta Pro y es usable desde nuestro cliente?

## Antecedente

Ejecución de código lanzada el 2026-06-08 para Ultra/Workspace; el 2026-07-16 el producto pasó a llamarse Gemini Notebook y se anunció la extensión a Pro en la web. Fuentes en la conversación del 02-10 y en `funcionalidades-notebooklm-py.md`.

## Paso 1: consulta (`codigo_r1.py`)

- Cuaderno: `f113873f-7fdb-416a-bb83-d429c4a3ce1b` (el de `api-r1`, una fuente).
- Pregunta, verbatim: «Usa código para dividir la fuente en oraciones numeradas y entrégame un archivo JSON con ellas.»
- 19,869 s. Una consulta generativa.
- Respuesta (`cache/code-r1/result.json`, campo `answer`): dice haber procesado la fuente «mediante un script en Python» y generado `oraciones-numeradas.json`, «disponible en tu panel Studio»; lista las dos oraciones con marcas `[1]`, negritas y una sugerencia final con emoji.
- `raw_response` muestra la traza del modelo: «using coding techniques to break down the provided source material into numbered sentences and deliver a JSON file».
- Artefactos del cuaderno: 0 antes, 1 después — `oraciones-numeradas.json`, tipo interno 10 (`FILE`), estado 3 (listo), ligado a la fuente `84fa991a-…`.

## Paso 2: descarga (`descargar_artefacto.py`)

`notebooklm-py` 0.8.4 (última versión publicada; la rama `main` del 02-10 tampoco) no tiene descarga para el tipo `FILE`. La respuesta cruda del RPC `gArtLc` (lista de artefactos) sí trae, junto al nombre y el tipo MIME, un enlace `https://contribution.usercontent.google.com/download?...` (parámetros `c`, `filename`, `opi`). El script lo extrae y lo baja con las cookies de la sesión: HTTP 200, `application/json`, 309 bytes. Guardado en `cache/code-r1/oraciones-numeradas.json`:

```json
{
  "fuente": "NBLM-SMOKE-001",
  "total_oraciones": 2,
  "oraciones": [
    {"numero": 1, "texto": "En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas."},
    {"numero": 2, "texto": "El recipiente Neri contenía 8 fichas blancas."}
  ]
}
```

## Observaciones

- La ejecución de código está activa en la cuenta Pro y se dispara desde `chat.ask`.
- El archivo generado es JSON limpio, sin las marcas de la respuesta del chat.
- La descarga depende de un formato interno no documentado; puede romperse sin aviso.
- Es el modelo quien decide ejecutar código; no hay parámetro para forzarlo ni para fijar el modelo.

## Evidencia

`cache/code-r1/result.json` (pregunta, respuesta, referencias, `raw_response`, artefactos) y `cache/code-r1/oraciones-numeradas.json`. El enlace de descarga no se guarda (contiene un token). Sin cookies ni cabeceras privadas. Una exploración previa de la respuesta cruda (solo lectura) no dejó archivos.

Comandos (desde la raíz del repo):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE ~/.local/share/nblm-spike/venv-notebooklm-py/bin/python notebooklm-spike/codigo_r1.py notebooklm-spike/cache/code-r1
env -u HTTPS_PROXY -u SSL_CERT_FILE ~/.local/share/nblm-spike/venv-notebooklm-py/bin/python notebooklm-spike/descargar_artefacto.py notebooklm-spike/cache/code-r1
```
