# Tareas — LangExtract

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| 1. ¿Funciona con nuestro modelo? | 2026-10-03 | Comprobar si LangExtract corre con DeepSeek (API compatible con OpenAI, clave inyectada por el proxy local) o si hace falta Gemini. | En Proceso | `langextract[openai]` 1.7.0 instalado en entorno aparte (`~/.local/share/lx-spike/venv`), `pip check` sin problemas; código revisado (sin llamadas a modelos). Falta la prueba de conexión con DeepSeek. |
| 2. ¿Representa nuestro contrato? | 2026-10-03 | Con un ejemplo resuelto (estanque), ver si extrae determinaciones con caso, aspecto, valor, condición y quién lo sostiene, ancladas literalmente; y qué pasa con lo que sale de partes distintas de la oración. | Pendiente | Depende de la tarea 1. |
| 3. ¿Gana algo frente a la ficha? | 2026-10-03 | Sobre un texto de desarrollo, comparar con `ficha_v1`: omisiones (varias pasadas), literalidad y tiempo. | Pendiente | Depende de las tareas 1 y 2. |
