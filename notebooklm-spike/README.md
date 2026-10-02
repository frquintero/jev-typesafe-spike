# NotebookLM — exploración de acceso programático

Este subproyecto evalúa NotebookLM como posible extractor para Zettel/Jev. Primero exploramos conexión desde Python, carga de fuentes, respuestas y citas recuperables; después, formatos, tiempos, cupos y calidad. El criterio futuro es aproximadamente 90 % de contenido correcto y ejecución ágil. Un smoke de conectividad no demuestra ese nivel de calidad.

Scripts, textos sintéticos y resultados permanecen en esta carpeta, separados de las otras rondas del repositorio.

## Decisiones y razones

Decisiones tomadas con Frat el **2026-10-02**:

| Decisión | Razón |
|---|---|
| Trabajar con la cuenta web gratuita, sin gastos. | Frat rechazó la contratación de servicios para este spike. No asociar facturación ni activar licencias, suscripciones o pruebas de pago. |
| Detener la vía oficial NotebookLM Enterprise de Google Cloud. | La investigación no encontró una API pública oficial de acceso gratuito permanente para cuentas de consumidor. La vía Enterprise requiere configuración Cloud y licencias de pago; la habilitación intentada quedó bloqueada por falta de facturación. |
| Usar el cliente comunitario `teng-lin/notebooklm-py`. | Entre los clientes comparados tenía la mayor adopción en GitHub: 19.581 estrellas y 2.613 forks, frente a 6.211 y 938 del cliente anterior, según la consulta del 2026-10-02. Además ofrece un SDK Python asíncrono documentado y mantenimiento activo. Las cifras expresan adopción, no una garantía de fiabilidad. |
| Fijar `notebooklm-py==0.8.4` y usar el backend `web`. | Permite revisar y reproducir una versión concreta. Su transporte HTTP sirve para integrar nuestro código Python con la sesión de la cuenta gratuita. |
| Instalar en un entorno exclusivo fuera del repo. | Aísla dependencias y conserva el entorno del cliente anterior para revisar sus resultados. |
| Empezar por el SDK Python; evaluar MCP después. | Queremos comprobar que nuestro código autentica, carga, consulta y recupera respaldo. MCP es una capa de integración adicional. |
| Usar fuentes sintéticas y conservar cada intento. | Permite fijar lo esperado antes de consultar, evitar documentos personales y mantener evidencia reproducible. |

La selección se investigó con **Exa**, documentación de los proyectos y estadísticas consultadas directamente en GitHub. En la revisión de CI del cliente elegido, Linux con Python 3.12 pasó; hubo un fallo en Windows. El cliente consume APIs internas no documentadas oficialmente por Google, que pueden cambiar. Su utilización conserva los límites y la disponibilidad de funciones de la cuenta gratuita.

## Código: `notebooklm-py`

El componente adoptado es la **biblioteca `notebooklm-py`**, importada mediante `from notebooklm import NotebookLMClient`. `smoke_py.py` implementa S0–S3 con esta biblioteca. `smoke_api.py` conserva la prueba con el cliente anterior.

**Cómo se conecta.** `NotebookLMClient.from_storage(ruta, backend="web")` abre un cliente asíncrono con las cookies de una sesión Google guardadas en un `storage_state.json` externo al repositorio. La biblioteca obtiene los tokens de sesión necesarios y realiza peticiones HTTPS mediante `httpx` a `https://notebook.google.com`, usando las RPC internas `batchexecute` y el endpoint de chat. Durante estas operaciones no necesita controlar ventanas del navegador. Esta vía no usa gcloud, ADC, proyecto Cloud ni una clave de API; el inicio de sesión web proporciona la autenticación inicial. La sesión anterior debe adaptarse al formato del nuevo cliente y conservar la cuenta seleccionada (`authuser=1`).

**Funciones que ofrece.**

- **Cuadernos:** crear, leer, listar, copiar, renombrar, borrar y recuperar metadatos/resúmenes.
- **Fuentes:** cargar texto, archivos, URLs, YouTube y Drive; esperar procesamiento; gestionar fuentes y recuperar texto indexado, guías y pasajes relevantes.
- **Consultas:** preguntar sobre fuentes seleccionadas, recuperar respuestas y citas, continuar conversaciones, consultar historial y guardar respuestas como notas.
- **Organización:** gestionar notas, etiquetas de fuentes y colecciones de cuadernos.
- **Generación y exportación:** informes, tablas, mapas, quizzes, flashcards, audio, video, diapositivas e infografías; descargar resultados en los formatos correspondientes, entre ellos Markdown, CSV y JSON.
- **Investigación y administración:** búsqueda web/Drive e importación de resultados, permisos para compartir, ajustes y lectura de cupos cuando estén disponibles.

La existencia de un método no confirma que esa función esté habilitada para nuestra cuenta. El [inventario completo y los contratos relevantes](funcionalidades-notebooklm-py.md) detallan esas limitaciones, los formatos de exportación y las pruebas propuestas. Dos precauciones para el spike: las consultas pueden continuar el historial existente, y pedir JSON en el prompt no garantiza un esquema estricto. Las citas deben resolverse sobre el documento estructurado con las utilidades del cliente.

## Evidencia obtenida y pendientes

- **Cliente anterior:** `smoke_api.py`, con `notebooklm-mcp-cli==0.15.0`, completó el smoke HTTP `api-r1`: creó un cuaderno, cargó texto, respondió «17 fichas violetas» y recuperó una cita vinculada a la fuente. Duración total: 12,832 s. Evidencia en [reporte-api-r1.md](reporte-api-r1.md) y `cache/api-r1/`. Esto demuestra ese intento con ese cliente.
- **Google Cloud:** OAuth ADC funcionó y se creó el proyecto «NotebookLM Spike» (`notebooklm-spike-20261002`). Habilitar Discovery Engine devolvió HTTP 400 `UREQ_PROJECT_BILLING_NOT_FOUND`. El smoke Enterprise no se ejecutó. La configuración quedó detenida; detalles en [reporte-cloud.md](reporte-cloud.md).
- **Cliente elegido:** `notebooklm-py==0.8.4` está instalado en `/home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/`. Importación comprobada y `pip check` correcto; dependencia fijada en [requirements-py.txt](requirements-py.txt). El intento `py-r1` se detuvo en S0 por redirección hacia login; S1–S3 pendientes de renovar sesión. Detalle en [reporte-py-r1.md](reporte-py-r1.md). Los resultados anteriores no se atribuyen a esta biblioteca.
- **Acceso desde nube:** no probado. El proxy local y la sesión del PC no se transfieren automáticamente; reconectar localmente tampoco acredita funcionamiento con el PC apagado.

## Pruebas iniciales propuestas

| Secuencia | Qué comprobar | Evidencia esperada |
|---|---|---|
| S0 — Autenticación | Adaptar la sesión y leer el cuaderno sintético conocido desde Python; consultar límites. | Cuenta correcta, lectura efectiva y límites reportados. |
| S1 — Ingesta | Crear un cuaderno nuevo, cargar `docs/smoke-001.txt`, esperar disponibilidad y recuperar el texto indexado. | IDs, fuente lista y contenido coincidente con el enviado. |
| S2 — Consulta y cita | Consultar con `prompts/smoke-001.txt`, restringiendo la pregunta a la fuente cargada. | 17 fichas violetas y pasaje recuperable que respalde cantidad y color. |
| S3 — Reconexión | Cerrar el proceso y abrir otro con la sesión guardada. | Recuperar el cuaderno, la fuente y el historial sin operar ventanas. |

Esta primera secuencia requiere un cuaderno nuevo y una sola pregunta generativa. Después se propone explorar selección de fuentes contradictorias, preguntas sin respuesta, salida JSON, carga de archivos, generación/exportación y persistencia de notas. La secuencia inicial se intentó en `py-r1`, detenida en S0; las pruebas posteriores siguen **propuestas**. El detalle S0–S10 está en [funcionalidades-notebooklm-py.md](funcionalidades-notebooklm-py.md); el plan operativo y su historial, en [PLAN.md](PLAN.md), y la tabla de tareas, en [tareas.md](tareas.md).

## Registro de cada intento

Conservar texto y prompt exactos, fuentes seleccionadas, versiones del cliente, respuestas HTTP redactadas, resultados parseados, citas, IDs, tiempos por etapa y errores. Cada corrida usa una carpeta nueva `cache/py-rN/`; nunca borrar, mover ni sobrescribir crudos anteriores. Cookies y tokens permanecen fuera del repo y de los registros. Un fallo de autenticación detiene la corrida; no repetir mutaciones a ciegas.

## Referencias

- [Cliente elegido](https://github.com/teng-lin/notebooklm-py) y [API Python de v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/python-api.md).
- [Sesión, perfiles y configuración de v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/configuration.md).
- [CI revisada para la selección](https://github.com/teng-lin/notebooklm-py/actions/runs/37008541217).
- [Cliente del smoke anterior](https://github.com/jacob-bd/gemini-notebook-mcp-cli).
- [API oficial Enterprise, vía detenida](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks).
