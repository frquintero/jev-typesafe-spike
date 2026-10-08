# Paso 2 · informe · 06-10-2026 (cierre de la ronda)

Candidato `prompt_ficha_contexto.md` (derivado de `ficha_v1`, que no se toca),
partición congelada de v9, misma unidad para las tres entradas. Especificación en
`especificacion_comparacion.md`; expectativas fijadas antes en
`expectativas_desarrollo.md` y `expectativas_reserva.md`.

**Cierre corregido (06-10):** se reconciliaron los documentos con los crudos, se
rehízo el conteo por ítem con las expectativas registradas y se retiró el total
que no era reproducible. **Ninguna llamada nueva, ninguna delegación.**

## Qué se hizo

1. **Comparación de tres entradas** sobre las 11 unidades de doc4 y doc5, sin
   volver a correr el paso 1: (a) unidad sola; (b) unidad más las referencias de
   v9 con sus respaldos; (c) unidad más el documento completo como contexto.
   Mismo prompt.
2. **69 crudos guardados**: 33 de `deepseek-flash` y 18 de Muse Code en
   desarrollo (doc4 completo en los dos; doc5 solo DeepSeek), más 12 de DeepSeek
   en la reserva, más 6 de Muse de la reserva **sin uso** (corrida interrumpida).
   **En el análisis entran 63.** Detalle: `inventario_y_costos.md`.
3. **Evaluación por ítem** sobre las 42 expectativas registradas de desarrollo
   (25 de doc4 y 17 de doc5) y las 30 de la reserva: `evaluacion_items.md`.

## Resultado de desarrollo

Recuperación estricta (65 casillas: doc4 24×2 + doc5 17; los `parcial` no suman):

| Entrada | Agregado (DeepSeek + Muse) | DeepSeek | Muse (solo doc4) | Fidelidad |
|---|---|---|---|---|
| (a) unidad sola | 46/65 = 70,8 % | 29/41 = 70,7 % | 17/24 = 70,8 % | 103/103 = 100 % |
| **(b) + referencias** | **62/65 = 95,4 %** | 39/41 = 95,1 % | 23/24 = 95,8 % | **111/113 = 98,2 %** |
| (c) + documento | 55/65 = 84,6 % | 34/41 = 82,9 % | 21/24 = 87,5 % | 103/103 = 100 % |

(b) es la mejor de las tres y la más barata en tiempo de llamada. Lo que decide,
mirando las casillas: en (a) las identidades externas no se resuelven («la
empresa» sin «de acueducto», «la red» sin «del tranvía»); en (c) el modelo tiene
el documento entero y **no completa todas** esas identificaciones —aunque sí
alcanza algunas que (b) no podía, como «la causa del corte» en `doc4 U2`—; en (b)
el referente viene dado y se conserva, salvo la fusión de DeepSeek en `doc4 U5`.

**Se retira el total anterior** (67,8 % / 85,1 % / 81,6 %): la lista de 55 ítems
de la «segunda cuenta» no se registró y sus denominadores por unidad son
inconsistentes. El motivo, en `evaluacion_desarrollo.md`.

## Resultado de la reserva (entrada b, DeepSeek)

| Medida | Resultado | Umbral |
|---|---|---|
| Recuperación estricta del contenido esperado | **29/29 = 100 %** | ≥ 90 % |
| Afirmaciones producidas fieles y del foco | **70/70 = 100 %** | ≥ 90 % |

Una expectativa (B11, «del mismo autor») es **defectuosa** y se informa aparte,
con su corrección posterior: el crudo la resuelve como relación, que es lo que
manda el prompt. Sin importaciones indebidas (los cuatro controles «no debe
importarse» se cumplieron) y sin respaldos no verificables. **La reserva la
escribió el mismo que diseñó el candidato y es breve: no es validación
independiente.**

## Costo, conciliado con los crudos

- **API DeepSeek: 45 llamadas** (33 de desarrollo + 12 de la reserva),
  **590 789 tokens de salida** (441 768 en desarrollo, 149 021 en la reserva);
  129 837 de entrada. **91 % del texto generado es razonamiento**, y viene
  **incluido** en `completion_tokens` (no se suma dos veces).
- **Tiempo de llamada (DeepSeek):** 1 903,9 s en desarrollo (29,0–84,2 s por
  corrida) y 646,2 s en la reserva.
- **Muse Code:** 18 tareas de desarrollo (4 303 s de envoltorio; de 65 s a
  2 646 s), 2 tareas de v9 sobre la reserva (72 s y 65 s) y 7 tareas de la
  reserva con la entrada (b) lanzadas, 6 con crudo, 1 sin resultado. **El tiempo
  de Muse es del envoltorio, no del razonamiento:** la tarea de 2 646 s
  (`9d818528…`) incluye un timeout de transporte; la duración del modelo no es
  reconstruible de los archivos guardados.
- **No se calcula costo monetario.**

## Incidencias

- Un fallo de parseo: `comp-doc4-c-u3-muse-r1.json` (JSON inválido).
- Una deformación de contenido: DeepSeek en `doc4 (b) U5` fundió «un corte
  similar» con el corte de este año y le atribuyó la duración y los efectos del
  otro; afecta a dos afirmaciones producidas.
- Los 27 primeros crudos de DeepSeek se corrieron en una primera pasada que el
  informe registra como «un error mío de modelo»; entran al análisis por decisión
  de Frat y se conservan íntegros.
- Muse `p2r-reserva_a-b-u7`: lanzada sin resultado; la reserva B de Muse no
  llegó a lanzarse.

## Limitaciones

- **Un juez** (el ejecutor), sin segunda lectura de las casillas.
- **Sin réplicas por unidad y entrada:** la estabilidad no está medida.
- **La lista fina de 55 ítems no se registró:** el conteo auditable usa las 42
  expectativas registradas, más gruesas; un ítem que reúne contenido e identidad
  se califica `parcial` si falta una parte.
- `doc5` no tiene corridas de Muse; el reparto entre modelos no es idéntico.
- Varios ítems de identidad que fallan en (b) son **inalcanzables** con lo que
  v9 registró: miden lo que el paso 1 entrega al paso 2.
- Todos los textos son cortos (14–17 oraciones) y la referencia hacia adelante
  sigue sin ejercitarse.

## Disposición, separada de la aceptación

- **Base provisional de trabajo del paso 2: la entrada (b)** —la unidad extraída
  de sus oraciones más las referencias de v9 con sus respaldos, como contexto que
  aclara y no amplía—, conforme a lo acordado con Frat. No es una adopción: en
  desarrollo la comparación elige la entrada y la reserva da un indicio, no una
  validación externa.
- **Resultado de aceptación:** con los conteos corregidos, (b) alcanza los dos
  umbrales del 90 % en desarrollo (95,4 % de recuperación, 98,2 % de fidelidad) y
  en la reserva (100 % y 100 %). **No se declara demostrada la aceptación:**
  reserva no independiente, un solo juez, sin réplicas y con una lista de ítems
  más gruesa que la que se retiró.
- **v9 y `ficha_v1` siguen congelados.** `ficha_v2` no se toca.
- **Después:** la conexión mecánica pregunta–dominio–corpus (fijar el alcance
  documental, recuperar unidades completas con sus datos y referencias, y
  preparar la entrada del orquestador). Su primera comprobación será local, sin
  LLM, con los materiales existentes, **después de cotejar ese alcance con el
  plan vigente**. No se inicia aquí.

## Archivos

| Archivo | Qué es |
|---|---|
| `README.md` | Requisitos, comandos y salidas de la vía de la entrada (b). |
| `inventario_y_costos.md` | Crudos, tareas, fallos, tiempos y tokens verificados. |
| `evaluacion_items.md` | Evaluación por ítem y totales corregidos. |
| `evaluacion_desarrollo.md` / `evaluacion_reserva.md` | Detalle de las dos medidas. |
| `hallazgos.md` | Qué aprendimos, con la observación separada de la hipótesis. |
| `prompt_ficha_contexto.md` | El candidato: `ficha_v1` + sección UNIDAD Y CONTEXTO + `{{CONTEXTO}}`. |
| `especificacion_comparacion.md` | Especificación de la comparación y regla de conteo. |
| `expectativas_desarrollo.md` / `expectativas_reserva.md` | Los ítems, fijados antes de llamar. |
| `comparacion.py` | Corredor, resumen y verificación offline (`seco`, `correr`, `resumen`, `comparar`, `verificar`, `verificar-todos`). |
| `comparacion_muse.sh`, `muse_unidad.py`, `correr_desarrollo.sh`, `muse_reserva.sh`, `reserva_muse.sh` | Corredores y recolección (Muse y DeepSeek). |
| `cache/comp-*.json` | Los crudos: procedencia, enviado, recibido, modelo, tokens e informe. |
| `muse/`, `salida_reserva*-v9.*` | Tareas de Muse y salidas de v9 sobre la reserva. |
