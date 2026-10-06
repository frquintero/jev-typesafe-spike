# Paso 2 · informe · 06-10-2026 (corregido)

Candidato `prompt_ficha_contexto.md` (derivado de `ficha_v1`, que no se toca),
partición congelada de v9, misma unidad para las tres entradas. Especificación en
`especificacion_comparacion.md`; expectativas fijadas antes en
`expectativas_desarrollo.md` y `expectativas_reserva.md`.

**Versión corregida tras la revisión de Astra (06-10):** se rehízo la cuenta con
ítems atómicos y correspondencia por casilla, se corrigieron los costos y se
rebajaron cinco afirmaciones que excedían lo observado. Ninguna llamada nueva.

## Qué se hizo

1. **Comparación de tres entradas** sobre las 11 unidades de doc4 y doc5, sin volver a
   correr el paso 1: (a) unidad sola; (b) unidad más las referencias de v9 con sus
   respaldos; (c) unidad más el documento completo como contexto. Mismo prompt.
2. **63 crudos**: 33 de `deepseek-flash` y 18 de Muse Code en desarrollo (doc4
   completo en los dos; doc5 solo DeepSeek), más 12 de DeepSeek en la reserva.
3. **Selección** con las dos medidas sobre 57 ítems esperados en desarrollo (32 de
   doc4 y 23 de doc5) y 30 en la reserva.

## Resultado de desarrollo

| Entrada | Recuperación (87 casillas) | Fidelidad | Tiempo (DeepSeek) | Tokens de salida (DeepSeek) |
|---|---|---|---|---|
| (a) unidad sola | 59/87 = 67,8 % | 103/103 = 100 % | 636,9 s | 147 967 |
| **(b) + referencias** | **74/87 = 85,1 %** | 111/113 = **98,2 %** | **616,3 s** | **145 171** |
| (c) + documento | 71/87 = 81,6 % | 103/103 = 100 % | 650,7 s | 148 630 |

**Ninguna entrada alcanza el 90 % de recuperación en desarrollo.** (b) es la mejor: le
faltan 5 puntos para el umbral, y saca 3,5 puntos a (c) y 17 a (a).

Lo que decide, mirando las casillas: en (a) las identidades externas no se resuelven
(«la empresa» sin «de acueducto», «la red» sin «del tranvía», y la condición «la noche
anterior» colgando); en (c) el modelo tiene el documento entero y **no completa todas**
esas identificaciones —aunque sí algunas que (b) no podía alcanzar, como «la causa del
corte» en `doc4 U2`, porque v9 no registró esa relación—; en (b) el referente viene
dado y se conserva, salvo la fusión de DeepSeek en `doc4 U5`.

## Resultado de la reserva (entrada b, DeepSeek)

| Medida | Resultado | Umbral |
|---|---|---|
| Recuperación fiel del contenido esperado | 30/30 = **100 %** | ≥ 90 % |
| Contenido producido fiel y del foco | 70/70 = **100 %** | ≥ 90 % |

Sin importaciones indebidas (los cuatro controles «no debe importarse» se cumplieron)
y sin respaldos no verificables. **La reserva la escribió el mismo que diseñó el
candidato: no es validación independiente**, y es más fácil que el desarrollo (sus
referencias venían completas).

## Costo, conciliado

- **API DeepSeek: 45 llamadas** (33 de desarrollo + 12 de la reserva), **590 789 tokens
  de salida** (441 768 en desarrollo, 149 021 en la reserva). 29–84 s por unidad, y
  85–90 % del texto generado es razonamiento.
- **Reserva:** 12 llamadas, **646,2 s**.
- **Muse Code:** 18 tareas de desarrollo (4 303 s; de 65 s a 2 646 s, con una tarea de
  44 minutos), 2 tareas de v9 sobre la reserva (72 s y 65 s) y 12 tareas de la reserva
  con la entrada (b), interrumpidas a la mitad (5 recolectadas, sin uso).
- **Tiempo comparado:** en DeepSeek, (b) saca 20–34 s a las otras dos (3–5 %). La
  diferencia grande que aparecía en la primera versión (1 171 s frente a 3 792 s) venía
  de la tarea de Muse de 44 minutos, no de la entrada.

## Incidencias

- Un fallo de parseo en 63 crudos (Muse, `doc4 c u3`, JSON inválido).
- Una deformación de contenido (DeepSeek, `doc4 b U5`: fundió «un corte similar» con el
  corte de este año y le atribuyó la duración y los efectos del otro). Afecta a dos
  ítems producidos.
- Los 27 primeros crudos de DeepSeek se corrieron por un error mío de modelo; entran al
  análisis por decisión de Frat y se conservan íntegros.

## Limitaciones

- **Un juez** (yo), sin segunda lectura de las casillas.
- **Sin réplicas por unidad y entrada:** la estabilidad no está medida.
- `doc5` no tiene corridas de Muse; el reparto entre modelos no es idéntico.
- Varios ítems de identidad que fallan en (b) son **inalcanzables** con lo que v9
  registró: miden el techo del paso 1.
- Todos los textos son cortos (14–17 oraciones) y la referencia hacia adelante sigue
  sin ejercitarse.

## Disposición final

- **Base de trabajo provisional del paso 2: entrada (b)** —la unidad extraída de sus
  oraciones más las referencias de v9 con sus respaldos, como contexto que aclara y no
  amplía—. Provisional porque el 90 % no se alcanza en desarrollo; el candidato queda
  como base sin abrir otra cadena de versiones.
- **v9 y `ficha_v1` siguen congelados.** `ficha_v2` no se toca.
- **Antes de dar el paso 2 por cerrado** hay que decidir qué hacer con el techo del
  paso 1 (las referencias que v9 no registra) y con la cuenta: hoy la medida depende de
  un solo juez.
- **Después:** la pieza mecánica del orquestador (orden del 06-10).

## Archivos

| Archivo | Qué es |
|---|---|
| `prompt_ficha_contexto.md` | El candidato: `ficha_v1` + sección UNIDAD Y CONTEXTO + `{{CONTEXTO}}`. |
| `especificacion_comparacion.md` | Especificación de la comparación y regla de conteo. |
| `expectativas_desarrollo.md` / `expectativas_reserva.md` | Los ítems, fijados antes de llamar. |
| `evaluacion_desarrollo.md` / `evaluacion_reserva.md` | Las dos medidas, con la segunda cuenta. |
| `hallazgos.md` | Qué aprendimos, con las afirmaciones corregidas. |
| `comparacion.py`, `correr_desarrollo.sh`, `comparacion_muse.sh`, `muse_unidad.py`, `muse_reserva.sh`, `reserva_muse.sh` | Corredores y recolección. |
| `cache/comp-*.json` | Los crudos: prompt enviado, respuesta, informe y costo. |
| `reserva_a.md`, `reserva_b.md` | La reserva y las salidas de v9 sobre ella. |
