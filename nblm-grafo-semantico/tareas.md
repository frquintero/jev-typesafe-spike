# Tareas — NotebookLM, grafo semántico

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Diseñar el prompt 2 para NotebookLM | 2026-10-03 | Diseño en papel del paso 2 (datos por unidad): contenido (ficha o forma reducida) y superficie (chat JSON con `chat.configure`, o tabla). | En Proceso | Plan revisado el 03-10: paso 1 con DeepSeek, paso 2 con NotebookLM. En discusión; nada escrito. |
| Primera corrida del paso 2 sobre gen1 | 2026-10-03 | Un cuaderno con las 5 unidades de DeepSeek como fuentes; una consulta por unidad con `source_ids`; medir tiempo por unidad y respeto del foco. | Pendiente | Depende del diseño. Una réplica. |
| Calibración del paso 1 (opcional) | 2026-10-03 | `unidades_v5` casi intacto como tabla sobre gen1: ¿respeta celdas no contiguas (`5, 9`) y da partición válida? | Pendiente | Solo si sobra cuota. Verificador: `verificar_subtemas`. |
