# NotebookLM — exploración de acceso programático

Evalúa NotebookLM (Google) como extractor alternativo o complementario a
DeepSeek para la capa de datos de Zettel. Criterio futuro: ≈90 % de
contenido correcto y ejecución ágil; un smoke de conectividad no lo
demuestra. Subproyecto separado de las demás rondas del repositorio.

**Estado actual:** ver `tareas.md` (tabla con fecha, objetivo y estado de
cada línea de trabajo). Al 02-10-2026: cliente `notebooklm-py==0.8.4`
adoptado; smoke `py-r1` detenido en S0 (autenticación) por sesión no
aceptada — pendiente renovar sesión y reintentar en `py-r2`. Vía Cloud
Enterprise detenida por costo (ver más abajo).

## Dónde está cada cosa

- `tareas.md` — tabla de estado de cada línea de trabajo.
- `PLAN.md` — plan operativo e historial de decisiones.
- `reporte-api-r1.md`, `reporte-cloud.md`, `reporte-py-r1.md` — reporte
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
- `requirements-cloud.txt`, `requirements-py.txt` — dependencias fijadas
  por vía.
- `crear_proyecto_cloud.py` — script usado para crear el proyecto Cloud
  durante la vía Enterprise (detenida).

## Reglas de este subproyecto (adicionales a `AGENTS.md`)

- **Vía vigente:** cliente comunitario `notebooklm-py` — SDK Python,
  backend `web`, sesión de la cuenta gratuita (cookies en un
  `storage_state.json` externo al repo). Sin gcloud, ADC, proyecto Cloud
  ni clave de API.
- **Vía Cloud Enterprise: detenida.** Requiere facturación y licencia de
  pago; Frat la rechazó explícitamente el 02-10-2026. No retomarla sin
  autorización expresa.
- Sesión, cookies y tokens siempre fuera del repo y de los crudos; nunca
  en código ni en registros. Un fallo de autenticación detiene el
  intento — no se reintenta a ciegas ni se repiten mutaciones.
- **Acceso desde Work Cloud (Claude Code) no probado:** el proxy local
  (127.0.0.1) y la sesión del PC no se transfieren automáticamente; hace
  falta configurar un acceso autorizado aparte antes de ejecutar nada de
  este subproyecto desde la nube.

## Referencias

- [Cliente adoptado](https://github.com/teng-lin/notebooklm-py) y su
  [API Python v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/python-api.md).
- [Sesión, perfiles y configuración v0.8.4](https://github.com/teng-lin/notebooklm-py/blob/v0.8.4/docs/configuration.md).
- [Cliente del smoke anterior](https://github.com/jacob-bd/gemini-notebook-mcp-cli).
- [API oficial Enterprise, vía detenida](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks).
