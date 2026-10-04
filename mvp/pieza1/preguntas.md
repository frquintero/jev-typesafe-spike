# Pieza 1 — preguntas, premisas y criterio de aceptación

Esquema: `esquema2.md` (candidato).
**Aviso:** las notas de `documento.md` hablan de «la Q2» y «la Q6» de la mesa
1b; aquí no existen. En esta pieza solo hay Q5 (conflicto) y Q6r (derivado,
sin revisión). Ficha: `ficha_mano.json` (borrador hasta
su revisión). Documento: `mvp/mesa1b/documento.md`, radicado el 4-10-2026.

## Q5 — conflicto de fuentes

**Pregunta:** ¿Cuántas mantas guarda el club en el refugio de Peña Alta?
**R:** `libre`.
**Premisa del mundo (simulada):** M2 · origen mundo · mundo fuente · tipo dato ·
lo que dice la fuente: «el club tiene 55 mantas en el refugio de Peña
Alta» · en la tabla: «refugio de Peña Alta · número de mantas · 55»,
condición «las que guarda el club» (ref C2) · procedencia: inventario del
club (premisa simulada) · consulta 1-10-2026.
**Encabezado:** caso C3 · aspecto «número de mantas» · condición «las que
guarda el club» (ref C2). Las dos filas (D6 y M2) llevan esa condición: sin
ella no son la misma determinación y no hay conflicto (ensayo, l. 229).
**Tablas esperadas:** inicial, final (solo D6), revisada (D6 y M2).
**Desenlace esperado de la revisada:** `en conflicto`, `conflicto: [D6, M2]`.

*Cambio frente a la mesa 1b:* la pregunta y la premisa decían «cuántas mantas
hay en el refugio». El documento solo dice cuántas guarda **el club**: 40 del
club y 55 en total no chocan. Para que el conflicto sea real, las dos
determinaciones tienen que estar bajo la misma condición (ensayo, l. 229).

## Q6r — dato derivado con dependencias

**Pregunta:** ¿Qué día reabre la senda de acceso al refugio de Peña Alta tras
las obras?
**R:** `sin externas, con el mundo del orquestador`.
**Dependencias esperadas:**
- D3 (cierre del 15 al 31 de octubre, oración 3) y D1 (aviso del 20-9-2026,
  oración 1).
- M1 · orquestador · regla: «un cierre "del X al Y" deja cerrado el día Y; se
  reabre el día Y + 1» (resuelve la duda Q2).
- M3 · orquestador · regla: «un mes sin año en un texto fechado es la próxima
  ocurrencia de ese mes desde la fecha del texto» (resuelve la duda Q1).
- M4 · código · regla: aritmética de calendario, con la versión del código.
**Tablas esperadas:** inicial y final. **Posición:** 1-11-2026. **Desenlace:**
`cerrada`.
**Dato derivado esperado:** C4 · fecha de reapertura · 1-11-2026, guardado en
`corpus.jsonl` con la forma de `esquema2.md` §5.

## Criterio de aceptación (tres réplicas)

1. 0 errores del verificador de forma.
2. Cada diferencia con la tabla de referencia se clasifica a mano como formato
   (se espera 0), regla abierta (se anota) o error de fondo. Se acepta con 0
   errores de fondo. Error de fondo incluye una ruta que no alcanza su
   posición.
3. La respuesta de la Q5 menciona 40 y 55, la procedencia de cada una (oración
   5; inventario consultado el 1-10-2026) y no elige.
4. El dato derivado queda en `corpus.jsonl` y pasa la prueba de mantenimiento
   en los dos sentidos usando solo ese archivo: si D3 pasa a «del 15 al 25 de
   octubre», el 1-11-2026 pierde sostén y el 26-10-2026 pasa a ser admisible.
