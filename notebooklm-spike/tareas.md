# Tareas — NotebookLM

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Smoke test de conectividad a NotebookLM (NBLM) | 2026-10-02 | Conectar código Python a la API oficial de Google Cloud, autenticar mediante OAuth y consumir operaciones de notebooks y fuentes sintéticas. | En Proceso | Endpoint y contratos oficiales verificados con Exa: Discovery Engine v1alpha. `smoke_cloud.py` preparado. Frat instaló gcloud 587.0.0 y configuró ADC; Python autenticó en Cloud Resource Manager (HTTP 200, 14 proyectos). Pendientes: elegir proyecto/ubicación, asociar cuota y comprobar acceso a NotebookLM Enterprise. La corrida interna `api-r1` no satisface el alcance Cloud. Ver `reporte-cloud.md` y `cache/cloud-auth-r1/observations.json`. |
