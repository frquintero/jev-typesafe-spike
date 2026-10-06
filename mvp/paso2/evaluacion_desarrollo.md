# Evaluación de la comparación de entradas · 06-10-2026

Candidato `prompt_ficha_contexto.md` (sha256 `889e2ecb…`), partición congelada de v9,
mismas unidades para las tres entradas. Expectativas fijadas antes en
`expectativas_desarrollo.md` (42 ítems: 25 de doc4 y 17 de doc5).

## Qué se corrió

**51 crudos**, sin separar por modelo en la decisión (pedido de Frat, 06-10):

| Modelo | doc4 (a/b/c) | doc5 (a/b/c) | total |
|---|---|---|---|
| Muse Code (high, una tarea por unidad) | 6/6/6 | — | 18 |
| DeepSeek `deepseek-flash` | 6/6/6 | 5/5/5 | 33 |

- **Un fallo mecánico:** `doc4 c u3` con Muse no parseó (JSON inválido en la línea 13).
  Queda como 0 ítems en esa celda y se informa aparte.
- **Citas fuera de la unidad** (uso del contexto): (a) 0 en los 22 crudos; (b) 14
  (4 DeepSeek + 10 Muse); (c) 18. Nunca hubo un respaldo no verificable: 0 en los 51.
- **Una deformación de contenido:** DeepSeek `doc4 (b) U5` fundió «un corte similar»
  con el corte de este año y le atribuyó la duración de diecinueve horas y los dos
  colegios. Es el fallo que la expectativa 19 anticipaba.
- Sin agregados: los casos que entraron desde fuera (por ejemplo `la causa de → el
  corte` en `doc4 (c) U2`) son identificaciones necesarias, marcadas `inferido`.

## Recuperación (ítems esperados recuperados fielmente)

Denominador: 42 ítems × los crudos de cada entrada. doc4 tiene 2 crudos por unidad
(Muse y DeepSeek) → 50 casillas; doc5 tiene 1 (DeepSeek) → 17 casillas.

| Unidad (ítems) | (a) | (b) | (c) |
|---|---|---|---|
| doc4 U1 (6) | 12/12 | 12/12 | 12/12 |
| doc4 U2 (5) | 10/10 | 10/10 | 10/10 |
| doc4 U3 (2) | 0/4 | 4/4 | 1/4 |
| doc4 U4 (4) | 6/8 | 8/8 | 7/8 |
| doc4 U5 (3) | 6/6 | 5/6 | 6/6 |
| doc4 U6 (5) | 10/10 | 10/10 | 10/10 |
| doc5 U1 (3) | 3/3 | 3/3 | 3/3 |
| doc5 U2 (4) | 1/4 | 4/4 | 3/4 |
| doc5 U3 (4) | 3/4 | 4/4 | 3/4 |
| doc5 U4 (3) | 2/3 | 3/3 | 2/3 |
| doc5 U5 (3) | 2/3 | 3/3 | 3/3 |
| **Total** | **55/67 = 82,1 %** | **66/67 = 98,5 %** | **60/67 = 89,6 %** |

Lo que separa a las entradas es **la identidad que vive fuera de la unidad**: en (a)
quedan «la empresa», «los vecinos», «la ciudad», «el servicio», «la red» sin
identificar (y la condición «la noche anterior» colgando, con duda); en (b) el
referente viene dado y se conserva; en (c) el modelo tiene el documento entero y
**no siempre completa la identificación** («los vecinos» sin el barrio, «la ciudad»
sin el tranvía, «la red» sin el tranvía), y en un caso no parseó.

## Fidelidad (ítems producidos fieles y del foco)

Denominador: ítems contados en las fichas (determinaciones, capas, acciones y
relaciones; las marcas no se cuentan porque van dentro de su determinación).

| | (a) | (b) | (c) |
|---|---|---|---|
| Ítems producidos | 103 | 113 | 103 |
| Fieles y del foco | 103 | 112 | 103 |
| **Fidelidad** | **100 %** | **99,1 %** | **100 %** |

## Expectativas de referencia (aparte, no suman a los 42)

Conservadas / evaluables:

| Modelo | (a) | (b) | (c) |
|---|---|---|---|
| DeepSeek (19 referencias) | 2/19 | 18/19 | 11/19 |
| Muse (11 referencias de doc4) | 2/11 | 11/11 | 8/11 |

En (a) solo se conservan las dos referencias sin resolver (como duda); ninguna
identidad externa se resuelve. En (b) se conservan todas menos la fusión de
DeepSeek en `doc4 U5`. En (c) se pierden las identificaciones que el modelo no
completó y, con Muse, las tres de `doc4 U3` por el JSON inválido.

## Costo

| | (a) | (b) | (c) |
|---|---|---|---|
| Tiempo, 51 crudos | 1 244 s | **1 171 s** | 3 792 s |
| Tokens de salida (33 de DeepSeek) | 147 967 | **145 171** | 148 630 |

El tiempo de Muse es muy desigual (de 65 s a 2 646 s en una misma entrada): la
entrada (c) arrastra la tarea de 44 minutos de `doc4 U6`.

## Selección

- (a) 82,1 % de recuperación: **no alcanza** el 90 %.
- (c) 89,6 % de recuperación: **no alcanza** el 90 % por un ítem.
- (b) 98,5 % de recuperación y 99,1 % de fidelidad: **alcanza las dos medidas**, y
  además es la más barata en tiempo y en tokens.

**Entrada seleccionada: (b), unidad más las referencias de v9 con sus respaldos.**
El caso de contexto que no debe importarse y las dudas se comportaron como se
esperaba: en (b) ninguna ficha importó contenido ajeno y las dos referencias sin
resolver se conservaron como duda.

## Límite de esta evaluación

- Un juez (yo), no dos; el conteo es por ítem y está sujeto a mis llamadas de
  identidad, sobre todo al decidir si un caso sin identificar cuenta como
  recuperado. Está aplicado igual en las tres entradas.
- `doc5` no tiene corridas de Muse; la mitad del peso de doc4 sí las tiene, así que
  el reparto no es idéntico entre textos.
- La entrada (c) quedó a 0,4 puntos del umbral: con un ítem más habría pasado.
  La conclusión «(b) gana» no depende de esa frontera (gana también en costo),
  pero «(c) no alcanza el 90 %» sí es una diferencia de un solo ítem.
