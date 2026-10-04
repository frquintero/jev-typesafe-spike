# Tareas — NotebookLM, grafo semántico

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| Diseñar el prompt 2 para NotebookLM | 2026-10-03 | Diseño en papel del paso 2 (datos por unidad): contenido (ficha o forma reducida) y superficie (chat JSON con `chat.configure`, o tabla). | Terminada | Decidido el 03-10 (Frat, Cowork, DeepSeek): chat con las reglas en `chat.configure` y `ficha_v1` tal cual. |
| Ronda FU1: primera corrida del paso 2 sobre gen1 | 2026-10-03 | Un cuaderno con las 5 unidades de DeepSeek como fuentes; una consulta por unidad con `source_ids`; medir tiempo por unidad y respeto del foco. | Terminada | Reporte en `reporte-FU1.md`. Contenido comparable (13/13 ambos); NotebookLM 461,8 s frente a 186,1 s de DeepSeek, deforma dos marcas y no registra dudas; aislamiento por `source_ids` correcto. La sonda se quitó del script después. |
| Calibración del paso 1 (opcional) | 2026-10-03 | `unidades_v5` casi intacto como tabla sobre gen1: ¿respeta celdas no contiguas (`5, 9`) y da partición válida? | Pendiente | Solo si sobra cuota. Verificador: `verificar_subtemas`. |
| FU2 exploratoria: ficha del documento entero | 2026-10-03 | `ficha_v1` de gen1 entero, una llamada por extractor, sin sonda, sin borrados, sin `LONGER` (pedido de Frat). | Terminada | DeepSeek 69,3 s, 13/13, fiel. NotebookLM 144,4 s: ciclo de agente (≈43 pasos de razonamiento, escribe y ejecuta código para revisar su JSON, se corrige) y devuelve dos fichas pegadas (JSON roto). Corrieron uno tras otro, no en paralelo. Verificado por DeepSeek contra los crudos. Script `fu2_doc_entero.py`; crudos `cache/fu2-gen1-nblm-ficha_v1-r1.json` (guarda el flujo completo, ~40 MB) y `unidades/cache/ficha-gen1-deepseek-ficha_v1-r1.json`. |
