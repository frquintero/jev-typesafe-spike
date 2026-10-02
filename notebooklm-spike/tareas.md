# Tareas — NotebookLM

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Smoke test de conectividad a NotebookLM (NBLM) | 2026-10-02 | Conectar código Python a la API oficial de Google Cloud, autenticar mediante OAuth y consumir operaciones de notebooks y fuentes sintéticas. | En Proceso | OAuth ADC verificado; proyecto «NotebookLM Spike» ACTIVE: `notebooklm-spike-20261002`, número `265423575040`. Crear/comprobar proyecto: cinco HTTP 200. Habilitar Discovery Engine: HTTP 400 `UREQ_PROJECT_BILLING_NOT_FOUND`; crudos en `cache/cloud-enable-r1/`. Pendiente autorización para asociar cuenta de facturación «My Billing Account 1», después habilitar API, configurar Enterprise/licencia y ejecutar smoke. Ver `reporte-cloud.md`. |
