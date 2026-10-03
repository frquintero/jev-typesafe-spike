# Tareas — LangExtract

La fecha corresponde al registro de la tarea. Estados: Pendiente, En Proceso, Terminada, Abandonada.

**Frente cerrado el 2026-10-03** (evaluado, no adoptado; motivo en `README.md`, «Lección aprendida»).

| Tarea | Fecha | Objetivo | Estado | Observaciones |
|---|---|---|---|---|
| 1. ¿Funciona con nuestro modelo? | 2026-10-03 | Comprobar si LangExtract corre con DeepSeek (API compatible con OpenAI, clave inyectada por el proxy local) o si hace falta Gemini. | Abandonada | `langextract[openai]` 1.7.0 instalado en entorno aparte (`~/.local/share/lx-spike/venv`), `pip check` sin problemas; código revisado (sin llamadas a modelos). No se hizo la prueba de conexión: la revisión del código mostró que su unidad (trozo por tamaño) no sirve para lo nuestro. |
| 2. ¿Representa nuestro contrato? | 2026-10-03 | Con un ejemplo resuelto (estanque), ver si extrae determinaciones con caso, aspecto, valor, condición y quién lo sostiene, ancladas literalmente; y qué pasa con lo que sale de partes distintas de la oración. | Abandonada | Respondida por lectura del código: salida plana (clase, texto, atributos), sin identificadores ni relaciones; no representa quién sostiene qué ni la identidad del caso entre trozos. |
| 3. ¿Gana algo frente a la ficha? | 2026-10-03 | Sobre un texto de desarrollo, comparar con `ficha_v1`: omisiones (varias pasadas), literalidad y tiempo. | Abandonada | Sin objeto tras las tareas 1 y 2. Ideas rescatables (anclaje exacto, página de revisión, contexto del documento) anotadas en el `README.md` de la raíz. |
