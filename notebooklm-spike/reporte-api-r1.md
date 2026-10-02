# Smoke HTTP de NotebookLM — api-r1

**Corrección de alcance:** Frat precisó después de esta corrida que el objetivo es la API oficial de Google Cloud con OAuth. Esta prueba usó endpoints internos con sesión web y no cumple ese objetivo. Se conserva como evidencia de lo ejecutado, no como cierre de la tarea. La continuación Cloud está en `reporte-cloud.md`.

Ejecutado el 2026-10-02 a las 15:59:23 UTC (10:59:23 Bogotá). Se completaron seis peticiones HTTPS desde Python: lectura autenticada, creación de notebook, carga de texto, comprobación de procesamiento, consulta y recuperación de la fuente. Todas devolvieron HTTP 200. Además del estado HTTP, se comprobó el contenido y el vínculo de la cita.

## Entorno y autenticación

- Python 3.12.3; `notebooklm-mcp-cli==0.15.0`, `httpx==0.28.1`.
- Biblioteca instalada en `~/.local/share/nblm-spike/venv/`; no se ejecutó un servidor MCP.
- Cuenta Google con acceso web a NotebookLM, seleccionada mediante `authuser=1`.
- Sesión iniciada por Frat en el navegador interno y exportada a almacenamiento privado fuera del repo. El cliente HTTP recibe cookies de sesión, token CSRF `at` y `f.sid`. El navegador no participa en el transporte de esta corrida.
- Acceso por el proxy ya existente en `127.0.0.1:8080`, con su certificado de confianza exportado para este comando.
- Se inspeccionó el código instalado para construir y registrar estas llamadas. No se hizo una búsqueda web en esta corrida; Exa se había usado durante la preparación.

## Qué interfaz se comprobó y cómo funciona

Se usó la interfaz interna de NotebookLM para la cuenta de consumo. La API Enterprise enlazada en el README es otra vía y no se probó aquí.

Las operaciones de notebooks y fuentes envían `POST` a `https://notebook.google.com/_/LabsTailwindUi/data/batchexecute`. La URL selecciona el método mediante `rpcids`; el cuerpo es un formulario con `f.req` (JSON que contiene la llamada y sus parámetros serializados) y `at` (token CSRF). La sesión se acompaña con cookies y parámetros de sesión; `authuser=1` conserva la cuenta elegida. Los cuerpos llegan con prefijo XSSI y bloques JSON que el cliente decodifica.

La consulta usa otro `POST`, a `https://notebook.google.com/_/LabsTailwindUi/data/google.internal.labs.tailwind.orchestration.v1.LabsTailwindOrchestrationService/GenerateFreeFormStreamed`. Su `f.req` contiene la selección de fuentes, la pregunta y el identificador de conversación. El cuerpo recibido contiene bloques de la respuesta y las referencias. El cliente devuelve `answer`, `sources_used`, `citations` y `references`, incluido `cited_text`.

| Operación | RPC / endpoint | HTTP | Tiempo de etapa |
|---|---|---|---|
| Lectura de un notebook sintético existente | `rLM1Ne` | 200 | 0,690 s |
| Crear notebook exclusivo | `CCqFvf` | 200 | 0,393 s |
| Añadir texto sintético | `izAoDd` | 200 | 1,290 s |
| Consultar estado de procesamiento | `rLM1Ne` | 200 | 0,570 s |
| Preguntar con la fuente seleccionada | `GenerateFreeFormStreamed` | 200 | 9,469 s |
| Recuperar texto completo de la fuente | `hizoJc` | 200 | 0,417 s |

Total del proceso: **12,832 s**. La fuente ya figuraba como lista en la primera comprobación; no se midió el instante exacto en que terminó su procesamiento. Los tiempos incluyen transporte por el proxy local. No hubo reintentos ni nuevas llamadas para obtener estos resultados.

## Entradas exactas y salida

Texto enviado, fijado antes de la consulta:

```text
En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.
```

Pregunta exacta:

```text
Según la fuente, ¿cuántas fichas contenía Luma y de qué color eran? Incluye la cita que respalda la respuesta.
```

Respuesta completa decodificada por el cliente:

```text
El recipiente **Luma** contenía **17 fichas violetas** [1].

*Cita de la fuente:*
> «El recipiente Luma contenía 17 fichas violetas.» [1]

💡 ¿Te gustaría saber cuántas fichas tenía el recipiente Neri o explorar algún otro detalle de este ensayo?
```

- Notebook creado por Python: `f113873f-7fdb-416a-bb83-d429c4a3ce1b`.
- Fuente creada: `84fa991a-73de-4113-96a0-5a88818f9941`.
- `citations[1]` apunta exactamente a esa fuente; `sources_used` contiene su identificador.
- `references[0].cited_text` contiene el texto sintético completo. El pasaje devuelto incluye ambas oraciones; la cita mostrada en la respuesta reproduce la oración de Luma.
- `get_source_fulltext` recuperó el texto completo, coincidente con la entrada.
- [Abrir el notebook conservado](https://notebook.google.com/notebook/f113873f-7fdb-416a-bb83-d429c4a3ce1b?authuser=1).

## Evidencias y reproducción

`cache/api-r1/` conserva `inputs.json`, seis `http-XX-request.json` con el `f.req` exacto, seis cuerpos recibidos `http-XX-response.txt`, sus metadatos HTTP, los resultados decodificados por etapa y `summary.json`. Se omitieron cookies, `at`, `f.sid` y cabeceras de autenticación. Una búsqueda literal de los secretos de la sesión no encontró coincidencias en los archivos de esta carpeta del proyecto.

Comando ejecutado desde la raíz del repo:

```bash
export HTTPS_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
export NOTEBOOKLM_MCP_CLI_PATH="$HOME/.local/share/nblm-spike/auth"
/home/fratquintero/.local/share/nblm-spike/venv/bin/python notebooklm-spike/smoke_api.py api-r1 --session-file /home/fratquintero/.local/share/nblm-spike/auth-import/iab-r1.json --probe-notebook 6eb5fade-bdd1-45f7-bc28-5ea711771fa9
```

Para otra corrida, usar una réplica nueva (`api-r2`, etc.) y una sesión vigente fuera del repo. El script rechaza una carpeta de réplica existente y detiene fallos de autenticación. Comprobación del script: `python3 -m py_compile notebooklm-spike/smoke_api.py`.

Esta única ejecución acredita las operaciones descritas desde esta máquina y esta sesión. Quedan sin medir expiración y renovación de sesión, cupos, documentos mayores, calidad general de extracción y ejecución desde la nube con el PC apagado. El intento anterior de login en Chrome terminó en timeout tras un error de certificado; el recorrido anterior por la interfaz web se excluye de los resultados API.
