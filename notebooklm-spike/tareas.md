# Tareas — NotebookLM

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Smoke test de conectividad a NotebookLM (NBLM) | 2026-10-02 | Conectar código Python a la API oficial de Google Cloud, autenticar mediante OAuth y consumir operaciones de notebooks y fuentes sintéticas. | En Proceso | Frat precisó la vía oficial Cloud. Endpoint y contratos verificados con Exa en documentación de Google: Discovery Engine v1alpha. `smoke_cloud.py` preparado con OAuth ADC; faltan proyecto/ubicación y credenciales Cloud en esta máquina. La corrida anterior `api-r1` accedió a endpoints internos con sesión web: se conserva su evidencia, pero no satisface el smoke Cloud solicitado. Ver `reporte-api-r1.md` y `reporte-cloud.md`. |
