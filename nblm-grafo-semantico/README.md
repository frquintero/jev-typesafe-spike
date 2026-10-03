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
2. Rápido donde DeepSeek es lento: la tabla de determinaciones de FN2–FN4
   tardó unos 29 s por documento, frente a unos 100 s de la ficha completa de
   DeepSeek (`ficha_v1`, F5). Ojo con el alcance: la tabla cubre solo
   determinaciones (una lista frente a siete). En el paso 1 DeepSeek ya es
   rápido y estable (`unidades_v5`: 4,4–62,3 s, media 22,8 s; 17/17 corridas
   sin huecos ni solapes), así que ahí NotebookLM no tiene ventaja.

Riesgo asumido (Frat): cliente no oficial (`notebooklm-py`), cuenta personal,
solo local, modelo sin versión fija.

## Plan (revisado el 03-10, decisión de Frat)

La decisión está en el paso 2, donde DeepSeek es lento. Arquitectura mixta:
**paso 1 con DeepSeek, paso 2 con NotebookLM.**

1. **Diseño en papel del prompt 2 para NotebookLM.** Decidir el contenido
   (la ficha o una forma reducida) y la superficie (chat con salida JSON y
   reglas en `chat.configure`, o tabla de datos).
2. **Primera corrida, en el paso 2:** gen1 con sus unidades de DeepSeek
   (`unidades/cache/unidades-gen1-deepseek-unidades_v5-r*.json`: 5 unidades,
   idénticas en las tres réplicas, incluida la no contigua `[5, 9]`). Un solo
   cuaderno con cada unidad como fuente aparte; cada consulta con
   `source_ids=[esa unidad]`, para que la herramienta acote el foco.
   Posible fuente extra: un mapa breve del documento (idea rescatada de
   LangExtract). Se mide el tiempo real por unidad y si el foco se respeta.
3. **Calibración del paso 1 (opcional, si sobra cuota):** `unidades_v5`
   casi intacto (solo cambian la salida a filas, una línea que traduce los
   ejemplos y el verificador `verificar_subtemas` sobre el CSV), sobre gen1,
   una réplica. Mide si la tabla respeta celdas no contiguas y entrega una
   partición válida; no mide calidad semántica.

Juez: Frat y Cowork leyendo. gen1 es reserva: si se itera un prompt sobre
él, queda quemado como reserva.

`unidades_v1` (eje núcleo y satélites) no es una partición con nombre sino
una estructura de dos niveles; su lugar natural sería el paso de inventario
de casos. Discusión aparte (pendiente 7 de la memoria).

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

Estado de cada tarea: `tareas.md`. Rondas: `PLAN.md`.
