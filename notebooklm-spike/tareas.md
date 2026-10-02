# Tareas — NotebookLM

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Adoptar notebooklm-py y revisar funcionalidades | 2026-10-02 | Incorporar el cliente seleccionado e inventariar operaciones y posibles smoke tests con cuenta gratuita. | Terminada | `0.8.4` instalado en entorno externo exclusivo; importación y `pip check` correctos. Revisión del tag y paquete; inventario y propuesta S0–S10 en `funcionalidades-notebooklm-py.md`. No llamadas a NotebookLM en esta revisión. |
| Smoke de SDK notebooklm-py — subtarea S0–S3 | 2026-10-02 | Autenticar Python, crear cuaderno sintético, cargar/recuperar texto, consultar con cita y reconectar desde otro proceso. | Pendiente | Intento autorizado `py-r1`: S0 detenido por HTTP 302 hacia login con la sesión guardada (cuenta 1). Dos GET, cero mutaciones y cero consultas; S1–S3 no ejecutados. Renovar sesión antes de nueva réplica. Crudos en `cache/py-r1/`; detalle en `reporte-py-r1.md`. |
| Smoke test de conectividad a NotebookLM (NBLM) | 2026-10-02 | Conectar código Python a la API oficial de Google Cloud, autenticar mediante OAuth y consumir operaciones de notebooks y fuentes sintéticas. | Pendiente | Configuración Cloud detenida: Frat rechaza gastos y no autoriza asociar facturación ni adquirir licencias. OAuth ADC verificado; proyecto `notebooklm-spike-20261002` ACTIVE (número `265423575040`), sin facturación. Habilitar Discovery Engine devolvió HTTP 400 `UREQ_PROJECT_BILLING_NOT_FOUND`; API deshabilitada y smoke no ejecutado. Enterprise tiene suscripción de pago; debió explicarse el costo antes de instalar/configurar. Crudos preservados y detalle en `reporte-cloud.md`. |
