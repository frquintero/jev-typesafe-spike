# Paso 2 · informe · 06-10-2026

Candidato `prompt_ficha_contexto.md` (derivado de `ficha_v1`, que no se toca),
partición congelada de v9, misma unidad para las tres entradas. Especificación en
`especificacion_comparacion.md`; expectativas fijadas antes en
`expectativas_desarrollo.md` y `expectativas_reserva.md`.

## Qué se hizo

1. **Comparación de tres entradas** sobre las 11 unidades de doc4 y doc5 (sin volver
   a correr el paso 1): (a) unidad sola; (b) unidad más las referencias de v9 con sus
   respaldos; (c) unidad más el documento completo como contexto. Mismo prompt.
2. **51 crudos** en el análisis, sin separar por modelo (decisión de Frat, 06-10):
   18 de Muse Code (doc4 completo) y 33 de `deepseek-flash` (doc4 y doc5).
   Los 33 de DeepSeek incluyen 27 que se corrieron primero por un error mío de
   modelo: se conservan íntegros y entran al análisis por decisión de Frat.
3. **Selección** de la entrada con las dos medidas sobre 42 ítems esperados.
4. **Reserva**: dos documentos sintéticos nuevos, con expectativas fijadas antes de
   cualquier llamada, unidades de v9 congelado y la entrada elegida.

## Resultado de la comparación

| | (a) unidad sola | (b) + referencias | (c) + documento |
|---|---|---|---|
| Recuperación esperada | 55/67 = 82,1 % | **66/67 = 98,5 %** | 60/67 = 89,6 % |
| Fidelidad de lo producido | 103/103 = 100 % | **112/113 = 99,1 %** | 103/103 = 100 % |
| Referencias conservadas (DeepSeek / Muse) | 2/19 · 2/11 | 18/19 · 11/11 | 11/19 · 8/11 |
| Tiempo (51 crudos) | 1 244 s | **1 171 s** | 3 792 s |
| Tokens de salida (33 de DeepSeek) | 147 967 | **145 171** | 148 630 |

Lo que decide: en (a) las identidades externas quedan sin resolver; en (c) el modelo
tiene el documento entero y **no siempre completa** la identificación («los vecinos»
sin el barrio, «la ciudad» sin el tranvía, «la red» sin el tranvía); en (b) el
referente viene dado y se conserva. Detalle por unidad en
`evaluacion_desarrollo.md`.

**Entrada seleccionada: (b).** Alcanza las dos medidas y además es la más barata.

## Resultado de la reserva (entrada b, DeepSeek)

| Medida | Resultado | Umbral |
|---|---|---|
| Recuperación fiel del contenido esperado | 30/30 = **100 %** | ≥ 90 % |
| Contenido producido fiel y del foco | 70/70 = **100 %** | ≥ 90 % |

Sin importaciones indebidas (los cuatro controles «no debe importarse» se
cumplieron) y sin respaldos no verificables. Detalle en `evaluacion_reserva.md`.

**La reserva la escribió el mismo que diseñó el candidato: no es validación
independiente.**

## Costo

- API DeepSeek: 51 llamadas del paso 2 (33 de desarrollo + 6 que completaron el set
  + 12 de la reserva), 316 000 tokens de salida en las 33, 36–81 s por unidad.
- Muse Code: 18 tareas de desarrollo (4 303 s, muy desiguales: de 65 s a 2 646 s),
  2 tareas de v9 sobre la reserva (72 s y 65 s) y 12 tareas de la reserva con la
  entrada (b), en curso al cerrar este informe.
- Un fallo de parseo en 51 crudos (Muse, `doc4 c u3`) y una deformación de contenido
  (DeepSeek, `doc4 b U5`: fundió «un corte similar» con el corte de este año).

## Limitaciones

- **Un juez, no dos.** El conteo es por ítem y depende de mis llamadas al decidir si
  un caso sin identificar cuenta como recuperado; se aplicó igual en las tres
  entradas.
- **`doc5` no tiene corridas de Muse**; el reparto entre modelos no es idéntico
  entre textos.
- **(c) quedó a 0,4 puntos del umbral**: con un ítem más habría pasado. «(b) gana»
  no depende de esa frontera (gana también en costo); «(c) no alcanza el 90 %» sí
  es una diferencia de un solo ítem.
- **Una expectativa mía era imprecisa** (reserva B, «del mismo autor»): v9 la
  resolvió como relación, que es lo correcto. Corregida en la evaluación.
- La reserva de Muse con la entrada (b) sigue corriendo; sus resultados se agregan
  aparte cuando terminen, sin cambiar lo ya medido.

## Disposición final

- **Base de trabajo del paso 2: entrada (b)** —la unidad extraída de sus oraciones,
  más las referencias de v9 con sus respaldos como contexto que aclara y no amplía—.
  El prompt candidato queda como base, sin abrir otra cadena de versiones.
- **v9 y `ficha_v1` siguen congelados.** `ficha_v2` no se toca.
- **Lo que falta:** si el candidato se adopta como prompt del paso 2, le toca su
  sitio (hoy vive en `mvp/paso2/`); y sigue después la pieza mecánica del orquestador
  (orden del 06-10).
- **Lo que no se toca:** el esquema de salida (siete listas), el paso 1, el
  orquestador.

## Archivos

| Archivo | Qué es |
|---|---|
| `prompt_ficha_contexto.md` | El candidato: `ficha_v1` + sección UNIDAD Y CONTEXTO + `{{CONTEXTO}}`. |
| `especificacion_comparacion.md` | Especificación de la comparación y regla de conteo. |
| `expectativas_desarrollo.md` / `expectativas_reserva.md` | Los 42 + 30 ítems, fijados antes de llamar. |
| `evaluacion_desarrollo.md` / `evaluacion_reserva.md` | Las dos medidas, por unidad. |
| `comparacion.py` | Arma las entradas, corre y verifica con el corpus de cada una. |
| `correr_desarrollo.sh`, `comparacion_muse.sh`, `muse_unidad.py`, `muse_reserva.sh`, `reserva_muse.sh` | Corredores y recolección (DeepSeek y Muse). |
| `cache/comp-*.json` | Los crudos: prompt enviado, respuesta, informe y costo. |
| `reserva_a.md`, `reserva_b.md` | La reserva y las salidas de v9 sobre ella. |
