# notebooklm-py 0.8.4: funcionalidades y propuesta de smoke tests

Revisión: 2026-10-02. Frat autorizó adoptar este cliente y pidió revisar sus funcionalidades y proponer pruebas iniciales. Búsqueda/lectura con Exa; contratos contrastados con documentación del tag `v0.8.4` y con el paquete instalado. Lo descrito como disponible en la biblioteca no equivale a funcionamiento verificado en nuestra cuenta.

## Instalación comprobada

- Python 3.12, entorno exclusivo externo al repo: `/home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/`.
- Paquete instalado: `notebooklm-py==0.8.4`; importación de `NotebookLMClient` comprobada; `pip check`: `No broken requirements found`.
- Dependencia fijada en `requirements-py.txt`. Se instaló el paquete base, sin los extras de navegador, Android, MCP ni servidor REST.
- La instalación inicial falló por verificación de certificados en pip. Se corrigió usando `PIP_CERT` con el certificado del proxy local; no se deshabilitó la verificación TLS.
- En esta revisión no se hicieron llamadas a NotebookLM ni se ejecutaron las pruebas propuestas. El resultado previo `cache/api-r1/` corresponde a otro cliente y se conserva.

## Acceso y contratos relevantes

El backend elegido es `web`, con HTTP directo mediante `httpx` y cookies de una sesión Google externa al repo. No requiere ADC, proyecto Cloud, habilitación de Discovery Engine ni una licencia Enterprise. Las operaciones usan la disponibilidad y los cupos de la cuenta del usuario; la biblioteca no amplía esos cupos.

Puntos de entrada documentados: `https://notebook.google.com` (base), RPC `batchexecute` y endpoint de chat transmitido por HTTP. No es una API REST pública de Google ni una API compatible con OpenAI: el SDK construye las llamadas internas. El servidor REST opcional es un adaptador local de la biblioteca, no una API oficial de Google.

`NotebookLMClient.from_storage(path, backend="web")` consume un `storage_state.json`. La exportación anterior `auth-import/iab-r1.json` tiene otro formato; su autenticación no se da por migrada. Antes de una corrida hay que convertirla al formato documentado, conservar todas sus cookies, guardar el archivo con permisos 0600 en directorio 0700 y fijar `notebooklm.account.authuser=1`, que fue la cuenta seleccionada. No imprimir cookies ni tokens, no introducirlos en git y no habilitar recuperación mediante navegador ni master token.

El cliente normalmente recupera CSRF/session ID desde la página autenticada; eso es parte del protocolo HTTP. Ofrece renovación de sesión, keepalive y varios mecanismos de reautenticación. Para nuestro smoke: sin keepalive, cero reintentos de 429/5xx, sin recuperación externa y detener un fallo de autenticación. La renovación automática de tokens del SDK debe configurarse/controlarse al implementar esa regla; los parámetros de reintentos por sí solos no la desactivan.

## Inventario funcional

| Familia | Funciones ofrecidas en esta versión | Interés para el spike |
|---|---|---|
| Cuadernos (`notebooks`) | Listar, crear, leer, copiar, renombrar, cambiar emoji, borrar, metadatos, resumen/descripción, sugerencias de preguntas/instrucciones, quitar de recientes, respuesta RPC sin procesar. | Crear un espacio sintético aislado y recuperarlo por ID. |
| Fuentes (`sources`) | Texto pegado; archivos; URL/YouTube; Google Drive y archivos de Drive; libros exportables de Google Play Books. Cargas individuales, en lote y en cola; listar/filtrar, leer, renombrar, copiar, borrar, refrescar y comprobar vigencia. Añadir texto a una fuente existente. | Carga reproducible, selección de fuentes y actualización. |
| Procesamiento de fuentes | Esperar registro o disponibilidad; esperar varias fuentes en paralelo o mediante una lectura conjunta por ciclo; estados y fallos por fuente. | Separar carga aceptada de texto listo para consultar. |
| Recuperación de fuentes | Texto indexado completo, documento estructurado, guía/resumen/palabras clave y búsqueda de pasajes con ranking y filtro por fuentes. | Saber qué leyó NotebookLM y recuperar respaldo textual. |
| Chat (`chat`) | Preguntas con fuentes seleccionadas; respuesta, citas, documento estructurado y sugerencias; seguimiento por conversación; historial; configuración de objetivo/persona/longitud; estado/cancelación; borrar historial; guardar respuesta como nota con citas. | Extracción, respuesta respaldada y control del contexto. |
| Citas | ID de fuente, número de cita, texto citado, offsets de fuente y anclas de respuesta; utilidad `resolve_chat_reference_passage` para recuperar contexto. | Vincular una respuesta con una fuente y un pasaje verificables. |
| Notas (`notes`) | Crear/listar/leer/actualizar/borrar notas, también borrado por lote. Helpers para mapas respaldados por notas. | Persistir resultados; una nota común no incorpora automáticamente citas interactivas. |
| Etiquetas (`labels`) | Crear/listar/leer/renombrar/borrar; agregar/quitar fuentes; agrupación temática por IA. Una fuente puede estar en varias etiquetas. | Organizar y delimitar conjuntos de fuentes. |
| Colecciones (`collections`) | Agrupar cuadernos a nivel de cuenta; listar/leer/renombrar, agregar/quitar cuadernos y borrar la agrupación. | Organización posterior. **Crear tiene una limitación documentada:** envía la mutación y puede lanzar `CollectionError` con resultado desconocido, porque no puede correlacionar inequívocamente lo creado. |
| Investigación (`research`) | Buscar en web/Drive, modos fast/deep; descubrimiento web; iniciar, consultar/esperar/cancelar, importar fuentes y reconciliar resultados inciertos. | Explorar descubrimiento posterior; fuentes reales quedan fuera de la primera prueba sintética. |
| Artefactos (`artifacts`) | Generar, listar/leer, esperar/poll, renombrar/borrar/copiar, reintentar un artefacto fallido; leer instrucciones, opciones de personalización, revisar una diapositiva. | Ejercitar trabajos asíncronos y exportación. |
| Mapas (`mind_maps`) | Dos clases: árbol JSON respaldado por nota y mapa interactivo de Studio. Generar/listar/leer árbol/renombrar/borrar. | Representación estructurada alternativa. |
| Compartir (`sharing`) | Leer estado, enlace público/privado, nivel de vista, altas/cambios/bajas de permisos, invitaciones opcionales. | No necesario en el smoke inicial; implica compartir información. |
| Ajustes/cupos (`settings`) | Leer idioma y límites de cuadernos/fuentes, ajustes conjuntos y medidor de uso cuando esté disponible; cambiar idioma. | Leer cupos. **El cambio de idioma es global para la cuenta.** |
| Integración | SDK asíncrono, CLI, skill para agentes, servidor MCP, servidor REST local opcional; perfiles/cuentas múltiples. | Usaremos el SDK. MCP/REST no hacen falta para conectar Python. |
| Transporte y diagnóstico | Configuración de timeouts/concurrencia/reintentos, telemetría RPC, errores tipados, registro con correlación, RPC cruda; backend Android opcional y transporte `curl_cffi` opcional. | Versionar la prueba y medir cada etapa; Web basta inicialmente. |

### Generación y exportación

| Artefacto | Controles y salidas documentadas |
|---|---|
| Audio | Formatos deep-dive/brief/critique/debate, longitud, idioma e instrucciones; descarga de audio MP3/MP4. |
| Video | Explainer/brief/cinematic, estilos e instrucciones; descarga MP4. |
| Diapositivas | Formato/longitud, instrucciones y revisión de diapositiva; PDF o PPTX. |
| Infografía | Orientación, detalle e instrucciones; PNG. |
| Quiz | Cantidad/dificultad; JSON, Markdown o HTML. |
| Flashcards | Cantidad/dificultad; JSON, Markdown o HTML. |
| Informe | Briefing, guía de estudio, blog o instrucciones propias; Markdown y exportación a Google Docs. |
| Tabla de datos | Estructura pedida mediante instrucciones; CSV y exportación a Google Sheets. |
| Mapa mental | Dos clases de mapa, lectura y exportación de árbol JSON. |

La disponibilidad depende de la cuenta, del backend y de Google. La lista de capacidades implementadas no demuestra que la cuenta tenga acceso a cada generación. Un resultado `disabled`, `skipped`, `unavailable` o un campo ausente no se convierte en cero ni en éxito.

## Detalles que cambian cómo probamos

1. `ask(..., conversation_id=None)` puede continuar la conversación más reciente. No garantiza contexto limpio. Para las comparaciones independientes, usar cuadernos nuevos; no borrar el historial para forzar una prueba.
2. La respuesta es `AskResult`, no JSON con un esquema elegido por nosotros. Se puede pedir JSON en el prompt, pero después hay que parsearlo y verificar campos; no hay aquí una garantía equivalente a JSON Schema estricto.
3. Las posiciones de citas son unidades UTF-16 del documento estructurado. No cortar `answer` ni `fulltext.content` con esos números usando índices Python. Usar `fulltext.document.slice(...)` y la utilidad de resolución, y conservar texto citado e IDs.
4. `AskResult.raw_response` es un fragmento limitado, no un registro HTTP completo. Para crudos completos habrá que instrumentar el transporte y redactar secretos; no habilitar DEBUG indiscriminadamente.
5. Aceptación de una generación no equivale a terminación. Hay que comprobar el estado final y después validar el archivo descargado.
6. Algunas mutaciones pueden quedar con resultado desconocido después de un fallo. No reintentar a ciegas. En particular, `add_text(..., idempotent=True)` no se puede usar: la librería lo rechaza (`NonIdempotentRetryError`) porque el servidor no deduplica textos; recomienda un título único y deduplicar del lado del cliente (comprobado en `py-r3`).
7. El chat maneja streaming internamente y `ask()` devuelve la respuesta completa. No suponer que el API pública exponga un iterador de tokens.
8. Las lecturas de cuaderno pueden actualizar su marca de acceso reciente. Leer solamente cuadernos sintéticos conocidos y no listar la biblioteca personal en la primera prueba.
9. La respuesta del chat trae Markdown, marcas `[n]` y una sugerencia final con emoji (`py-r4`, `code-r1`). Con un texto corto, la cita cubre la fuente entera (un solo trozo), no la oración (`py-r4`).
10. Ejecución de código (Gemini Notebook, activa en la cuenta Pro desde Python, `code-r1`): pedida en `chat.ask`, crea un artefacto tipo `FILE` (código 10). La librería no lo descarga; el enlace está en la respuesta cruda de `gArtLc` (`descargar_artefacto.py`). El modelo decide si ejecuta código.

## Smoke tests propuestos (todavía no ejecutados)

Objetivo de los primeros cuatro: demostrar que **nuestro Python con este SDK** autentica, ingiere, consulta y recupera respaldo. Las pruebas posteriores exploran conducta útil para Zettel; no certifican calidad general ni el umbral del 90 %.

| ID | Operación/prueba | Entrada y comprobación | Evidencia |
|---|---|---|---|
| S0 | Sesión y lectura | Migrar sesión externa con cuenta 1; `notebooks.get` sobre el cuaderno sintético previo. Leer `settings.get_account_limits`; opcional `get_usage`, registrando si no está disponible. | ID coincidente, lectura efectiva, límites reportados, errores y latencia. Ninguna consulta generativa. |
| S1 | Crear + cargar + recuperar | Cuaderno con título único; `sources.add_text` con `docs/smoke-001.txt`; esperar READY; `sources.get_fulltext`. | IDs, estados, texto indexado, igualdad con el contenido fijado normalizando únicamente saltos de línea y espacios externos. |
| S2 | Pregunta + cita | `chat.ask` con `prompts/smoke-001.txt` y `source_ids=[id_cargado]`. | Respuesta 17 fichas violetas; referencia a la fuente cargada; pasaje recuperado que respalde cantidad y color. Una consulta. |
| S3 | Reconectar desde otro proceso | Cerrar cliente/proceso y volver a abrirlo con el storage externo. Recuperar el cuaderno, fuente e historial de S2. | Sesión reutilizable sin manejar ventanas, IDs estables y pregunta/respuesta recuperadas. No acredita ejecución en nube ni sesión indefinida. |
| S4 | Dos fuentes contradictorias y selección | Fuente A: «En el ensayo ficticio, Luma contenía 17 fichas violetas.» Fuente B: «En el ensayo ficticio, Luma contenía 23 fichas verdes.» En cuadernos nuevos para contexto independiente, preguntar primero con selección de A, luego B y después ambas. | A: 17/violetas/cita A; B: 23/verdes/cita B; ambas: conflicto atribuido y citas A/B. Guardar historial para detectar contaminación. Tres consultas. |
| S5 | Pregunta sin respuesta | Cuaderno nuevo con el texto original. Pregunta: «¿Quién fabricó el recipiente Luma? Responde únicamente con lo que establece la fuente; si no lo establece, indícalo.» | Registrar si indica ausencia de información o inventa un fabricante. Una observación no prueba una garantía de abstención. Una consulta. |
| S6 | Salida JSON | Cuaderno nuevo con el texto original. Pregunta: «Devuelve únicamente un objeto JSON con las claves recipiente, cantidad y color para Luma, según la fuente. No agregues claves ni Markdown.» | JSON parseable, claves exactas, recipiente=Luma, cantidad=17 como número, color=violetas. Citas se examinan por separado en las referencias del SDK. Una consulta. |
| S7 | Archivo local + recuperación | Subir `docs/smoke-001.txt` mediante `add_file` en otro cuaderno; esperar READY, recuperar contenido y repetir la pregunta original. Después, PDF sintético breve como prueba distinta. | Archivo aceptado, texto recuperado, respuesta/cita; separar duración de transferencia, procesamiento y consulta. |
| S8 | Trabajo asíncrono + descarga | Un solo informe breve o una tabla sobre las dos entidades del texto; fijar instrucciones antes de correr. Generar, esperar, descargar Markdown/CSV. | Estado terminal completed, archivo legible, contenido, IDs y tiempos; esta prueba usa cupo de generación de la cuenta. |
| S9 | Persistir respuesta | `chat.save_answer_as_note` con el resultado citado de S2; leer/listar solamente notas del cuaderno sintético. | Nota recuperable, contenido y representación de citas; leer no basta para acreditar hover visual. |
| S10 | Fallos locales controlados | Sesión ausente/incompleta y réplica ya existente; simular timeout/429 en transporte local sin provocar bloqueo de la cuenta real. | Error claro, ningún secreto en salida, cero llamadas con sesión inválida y cero sobrescrituras/reintentos de mutaciones. |

**Comienzo recomendado:** S0 → S1 → S2 → S3, con un cuaderno nuevo y una pregunta. Luego S4 → S5 → S6 (selección, ausencia de respuesta y estructura), antes de generaciones multimedia. Audio/video, investigación externa, compartir y cambios globales quedan como exploraciones posteriores.

Por intento: nueva carpeta `cache/py-rN/` con `exist_ok=False`, entradas/selección de fuentes/prompt exactos, cliente y versiones efectivas, respuestas HTTP redactadas, objetos parseados, IDs, errores, tiempos por etapa y duración total. No reutilizar `api-r1` ni presentar el smoke antiguo como resultado del cliente nuevo. Conservar los cuadernos sintéticos para revisión.

## Fuentes primarias de la versión revisada

- [README v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/README.md).
- [API Python v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/python-api.md): contratos, familias, errores, citas e idempotencia.
- [CLI v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/cli-reference.md).
- [Configuración v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/configuration.md): sesión/cuenta, backends, transporte y servidor REST.
- [Instalación v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/installation.md) y [extras del paquete](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/pyproject.toml).
- [MCP v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/mcp-guide.md).
- [Diferencias Web/Android](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/web-android-public-behavior.md), [estabilidad](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/stability.md) y [cupos](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/quota-limits.md).
