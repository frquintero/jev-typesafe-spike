# Pruebas NotebookLM — grafo semántico

Subproyecto para llevar a NotebookLM la extracción en dos pasos de Zettel:

- **Prompt 1 (paso 1):** unidades temáticas o subtemas.
- **Prompt 2 (paso 2):** datos por unidad.

Sirve a la visión de Zettel (`README.md` de la raíz, «Visión»): un ecosistema
de unidades temáticas y datos sobre el que operen preguntas. En el marco,
información no es traer un pasaje: es el cambio en A(Q). NotebookLM se usa por
su fuerza en recuperar con cita (respaldo literal), sin confundir recuperar con
responder.

## Por qué NotebookLM

1. Modelo frontera con un arnés pensado para trabajo semántico sobre fuentes.
2. Rápido: unos 29 s por consulta en FN2–FN4, frente a unos 100 s de DeepSeek
   con `ficha_v1`.

Riesgo asumido (Frat): cliente no oficial (`notebooklm-py`), cuenta personal,
solo local, modelo sin versión fija.

## Plan

1. **Prompt 1.** Adaptar `unidades/prompts/unidades_v5.md` (el último usado,
   estable con DeepSeek en U7–U9 y ENC5–ENC14) a la forma de NotebookLM y
   compararlo con lo que hizo DeepSeek sobre los mismos textos.
   - Referencia: crudos de DeepSeek en `unidades/cache/unidades-*-deepseek-unidades_v5-r*.json`
     (réplicas de biomar1, gen1, oxi1 y evals1).
   - Juez: Frat y Cowork leyendo. La variación de DeepSeek entre sus propias
     réplicas sirve de medida de lo que cuenta como «similar».
2. **Si el prompt 1 rinde parecido:** migrarlo a NotebookLM y construir un
   prompt 2 propio de NotebookLM, ajustado a lo que la herramienta pide y hace.

## Lecciones que traemos (`notebooklm-spike/`)

- FN1: el servidor rechaza consultas largas. Reformular según la forma de la
  herramienta; no calcar el prompt de DeepSeek.
- FN2–FN4: la tabla de datos es rápida y literal; afinar un solo paso sobre el
  texto entero solo movió el error de lugar.
- Ajustar sobre textos de desarrollo; la reserva solo mide.

## Reglas

Las de `AGENTS.md` y las de `notebooklm-spike/README.md`: cliente
`notebooklm-py` con el perfil `nblm-spike`, sin proxy local, solo ejecución
local, sesión y cookies fuera del repo, bajo volumen, crudos que nunca se
borran ni se sobrescriben (una réplica nueva lleva un `rN` nuevo).

Estado de cada tarea: `tareas.md`.
