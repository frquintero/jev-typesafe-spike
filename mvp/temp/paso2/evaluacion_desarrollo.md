# Evaluación de la comparación de entradas · 06-10-2026 (corregida)

Corrige y sustituye las dos versiones anteriores. **Ninguna llamada nueva:**
todo sale de los crudos de `cache/` y de las expectativas fijadas antes de
llamar.

**El total agregado de esta ronda vive en `evaluacion_items.md`**, con una fila
por expectativa registrada y su respaldo. Aquí quedan la regla, los casos que
deciden y los defectos.

## Qué se retiró, y por qué

La «segunda cuenta» de la versión anterior daba 87 casillas (doc4 32 ítems,
doc5 23), con totales 67,8 % / 85,1 % / 81,6 %. **No es reproducible:**

- La lista de 55 ítems atómicos **nunca se registró**; solo quedaron las 42
  expectativas de `expectativas_desarrollo.md`, que son más gruesas (un ítem
  puede reunir contenido e identidad).
- Los denominadores por unidad de esa tabla son **inconsistentes**: U3 figura
  sobre 4 casillas con dos modelos (deberían ser 8) y U4 sobre 6 (deberían ser
  10); la suma de los denominadores de una columna (56) no da las 64 casillas
  del encabezado. Las tres filas «Total» son la suma de los numeradores de la
  tabla, no de casillas comparables.

Con la lista registrada y la regla de `evaluacion_items.md` —un ítem es
`cumple`, `parcial`, `no` o expectativa defectuosa; los `parcial` **no** se
suman a la recuperación—, los totales son los de la tabla siguiente. La
diferencia entre ambos conteos es grande y **no se puede zanjar con lo
guardado**; por eso el resultado de umbral se informa con esa salvedad.

## Recuperación estricta (65 casillas: doc4 24×2 + doc5 17)

| Entrada | Agregado (DeepSeek + Muse) | DeepSeek | Muse (solo doc4) |
|---|---|---|---|
| (a) unidad sola | 46/65 = **70,8 %** | 29/41 = 70,7 % | 17/24 = 70,8 % |
| **(b) unidad + referencias** | **62/65 = 95,4 %** | 39/41 = 95,1 % | 23/24 = 95,8 % |
| (c) unidad + documento | 55/65 = **84,6 %** | 34/41 = 82,9 % | 21/24 = 87,5 % |

- **Expectativas válidas:** 24 en doc4 (la 25 es defectuosa) y 17 en doc5.
- **Parciales** (aparte, no suman): doc4 (a) 5+5, (b) 1+1, (c) 3+1; doc5 (a) 5,
  (c) 4.
- **No evaluable:** la corrida `doc4 (c) U3` de Muse, por JSON inválido.
- **Agregado:** es el que Frat autorizó, con la composición de la tabla;
  DeepSeek corrió doc4 y doc5, Muse solo doc4.

**Con la cuenta auditable, (b) supera el 90 % también en desarrollo**, no solo
en la reserva. La conclusión anterior («ninguna entrada alcanza el 90 % en
desarrollo») era un artefacto de la lista de ítems no registrada.

## Fidelidad (por código, sobre las fichas guardadas)

| Entrada | Producidos | Fieles y del foco |
|---|---|---|
| (a) | 103 (DeepSeek 72 + Muse 31) | 103/103 = **100 %** |
| (b) | 113 (DeepSeek 76 + Muse 37) | 111/113 = **98,2 %** (DeepSeek 74/76, Muse 37/37) |
| (c) | 103 (DeepSeek 72 + Muse 31, 5 corridas) | 103/103 = **100 %** |

La única deformación es la de `doc4 (b) U5` con DeepSeek (funde los dos
cortes y le atribuye al de este año la duración y los efectos del otro): toca
dos afirmaciones producidas. La corrida `doc4 (c) U3` de Muse no produjo ficha
y queda fuera de producidos y de fidelidad.

## Las celdas que se comprobaron contra los crudos

1. `doc4 U2 (a)` y `(b)`: se esperaba la causa **del corte** y el crudo solo
   registra «causa → reparación de una tubería matriz»; v9 no registró esa
   relación en U2, y (c) sí la alcanza. Ítem 7 = `parcial` en (a) y (b), `cumple`
   en (c).
2. `doc4 U5 (a)`: se esperaba distinguir y relacionar dos cortes; el crudo tiene
   un solo corte, ninguna relación y una duda sobre el término de comparación.
   Ítem 19 = `no` en (a) con los dos modelos.
3. `doc4 U5 (b)`: examen de identidad, duración, semejanza y respaldo. DeepSeek
   **funde** los dos acontecimientos siguiendo el referente que v9 le dio; Muse
   los distingue y los une por la relación «similar a». No se da por probada una
   fusión por el nombre del caso, ni se cuenta como recuperada una relación
   ausente.
4. `doc4 U6` «la solicitud»: el documento admite `[8]`, `[14]` y `[15]`. La
   expectativa que exigía `[8]` como lectura única queda **defectuosa**
   (ítem 25); conservar la duda es lo correcto y ninguna corrida inventa una
   identificación.
5. `doc4 U3`, `U4` y `U6` en (a): las identidades externas no se resuelven (la
   empresa sin «de acueducto», los vecinos sin el barrio, la fecha sin el
   jueves), y por eso esos ítems son `parcial`, no `cumple`.

## Defectos que quedan dichos

- El juez es uno; ninguna casilla tiene segunda lectura.
- No hay réplicas por unidad y entrada: la estabilidad no está medida.
- `doc5` no tiene corridas de Muse.
- Los ítems de identidad externa que fallan en (b) son, en varios casos,
  **inalcanzables** con lo que v9 registró (U2 no tiene ninguna referencia):
  miden lo que el paso 1 entrega al paso 2, no un defecto de la entrada.
