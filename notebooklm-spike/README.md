# NotebookLM — exploración de acceso programático

Evalúa NotebookLM (Google) como extractor alternativo o complementario a
DeepSeek para la capa de datos de Zettel. Criterio futuro: ≈90 % de
contenido correcto y ejecución ágil; un smoke de conectividad no lo
demuestra. Subproyecto separado de las demás rondas del repositorio.

**Estado actual:** ver `tareas.md` (tabla con fecha, objetivo y estado de
cada línea de trabajo). Al 02-10-2026:

- **Conexión resuelta.** Cliente `notebooklm-py==0.8.4`, sesión propia de la
  librería (perfil `nblm-spike`, cuenta principal de Frat, `authuser 0`).
  S0–S3 cubiertos con `py-r4` (sesión, carga, consulta con cita, reconexión).
- **Ejecución de código activa** en la cuenta Pro (`code-r1`); los archivos
  generados se bajan con `descargar_artefacto.py`.
- **Extracción en un solo paso, agotada.** FN1 (`ficha_v1` por el chat):
  rechazada por larga. FN2–FN4 (determinaciones como tabla de datos sobre
  jardin1): rápidas (~29 s) y literales, pero cada ajuste de reglas movió el
  error a otro lado (condiciones perdidas, casos inventados o nominalizados,
  omisiones). Además se estaba afinando sobre un texto de la reserva de F5.
- **Decisión (Frat, 02-10):** dejar de estirar la tabla de un solo paso y
  reintroducir lo que se excluyó el 01-10: subtemas, inventario de casos,
  ficha por foco, respaldo por componente y verificación (código + Jev). Cada
  paso con la herramienta cuya forma le calza. Rediseño en discusión
  (`PLAN.md`, sección «Rediseño»); se ajusta sobre textos de desarrollo, la
  reserva solo mide.

Vía Cloud Enterprise detenida por costo (ver más abajo).

## Dónde está cada cosa

- `tareas.md` — tabla de estado de cada línea de trabajo.
- `PLAN.md` — plan operativo e historial de decisiones.
- `reporte-api-r1.md`, `reporte-cloud.md`, `reporte-py-rN.md`,
  `reporte-code-r1.md` — reporte
  detallado de cada intento/vía, con su evidencia.
- `funcionalidades-notebooklm-py.md` — inventario de funciones del cliente
  adoptado y las pruebas S0–S10 propuestas.
- `cache/<intento>-rN/` — crudos de cada corrida (request/response/parsed/
  summary). Nunca se borran, mueven ni sobrescriben; una réplica nueva usa
  una carpeta `rN` nueva.
- `docs/`, `prompts/` — textos y preguntas sintéticas, fijados antes de
  correr.
- `smoke_api.py`, `smoke_cloud.py`, `smoke_py.py` — scripts de cada vía
  probada: cliente anterior (`notebooklm-mcp-cli`), API oficial Cloud
  Enterprise, cliente adoptado (`notebooklm-py`).
- `codigo_r1.py` (consulta que pide ejecutar código) y `descargar_artefacto.py`
  (baja archivos tipo `FILE`, que la librería no descarga).
- `ficha_nblm.py` — la ficha (`ficha_v1`) con NotebookLM; reutiliza la numeración
  y el verificador de `unidades/`.
- `tabla_nblm.py` — determinaciones como tabla de datos (CSV); instrucciones en
  `prompts/tabla_det_v1.md`.
- `requirements-cloud.txt`, `requirements-py.txt` — dependencias fijadas
  por vía.
- `crear_proyecto_cloud.py` — script usado para crear el proyecto Cloud
  durante la vía Enterprise (detenida).

## Reglas de este subproyecto (adicionales a `AGENTS.md`)

- **Vía vigente:** cliente comunitario `notebooklm-py` — SDK Python,
  backend `web`, sesión de la cuenta principal de Frat (plan Pro). Frat
  decidió no crear una cuenta dedicada hasta ver si NotebookLM promete
  valor. Sesión creada con `notebooklm -p nblm-spike login` y guardada en
  `~/.notebooklm/profiles/nblm-spike/storage_state.json` (fuera del repo,
  carpeta 0700, archivo 0600). El extra `[browser]` (Playwright) se instaló
  solo para ese login. Sin gcloud, ADC, proyecto Cloud ni clave de API.
- **Sin proxy local para NotebookLM:** no necesita claves, y así las cookies
  de Google no pasan por el proxy de 127.0.0.1:8080. No exportar
  `HTTPS_PROXY` ni `SSL_CERT_FILE` en estas corridas.
- **Vía Cloud Enterprise: detenida.** Requiere facturación y licencia de
  pago; Frat la rechazó explícitamente el 02-10-2026. No retomarla sin
  autorización expresa.
- Sesión, cookies y tokens siempre fuera del repo y de los crudos; nunca
  en código ni en registros. Un fallo de autenticación detiene el
  intento — no se reintenta a ciegas ni se repiten mutaciones.
- **Solo ejecución local (Muse).** Con la cuenta principal, la sesión no se
  transfiere a la nube; se descartó pasarla como secreto
  (`NOTEBOOKLM_AUTH_JSON`). Claude Code no ejecuta este subproyecto.
- Leer solo los cuadernos sintéticos que crea cada corrida; no listar la
  biblioteca personal.
- **Bajo volumen:** una réplica por ronda, salvo decisión expresa de Frat
  (02-10-2026), para no llamar la atención sobre la cuenta.

## Referencias

- [Cliente adoptado](https://github.com/teng-lin/notebooklm-py) y su
  [API Python v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/python-api.md).
- [Sesión, perfiles y configuración v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/configuration.md).
- [Cliente del smoke anterior](https://github.com/jacob-bd/gemini-notebook-mcp-cli).
- [API oficial Enterprise, vía detenida](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks).
