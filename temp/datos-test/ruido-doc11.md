# Ruido de la extracción de `doc11` (mismo modelo, mismas unidades)

| corrida | prompt | datos | con `unidad_valor` | segundos | entrada | salida (pensando) |
|---|---|---|---|---|---|---|
| `doc11-deepseek-low-d1` | `temp/datos-decisiones/prompt_DATOS_decisiones_v7.md` | 34 | 4 | 52.5 | 2033 | 13790 (12304) |
| `doc11-deepseek-low-d1r2` | `temp/datos-decisiones/prompt_DATOS_decisiones_v7.md` | 31 | 4 | 41.6 | 2033 | 11416 (9836) |
| `doc11-deepseek-low-b1` | `mvp/prompts/prompt_DATOS.md` | 35 | 4 | 18.1 | 1714 | 5403 (3778) |

## Par por par

`pares` = datos que se corresponden · `sueltos` = los que quedan sin par · `acuerdo` = pares / el mayor de los dos.

| par | tipo | pares | sueltos | acuerdo |
|---|---|---|---|---|
| `doc11-deepseek-low-d1` vs `doc11-deepseek-low-d1r2` | dentro del prompt | 29 | 5 + 2 | 85 % |
| `doc11-deepseek-low-d1` vs `doc11-deepseek-low-b1` | entre prompts | 19 | 15 + 16 | 54 % |
| `doc11-deepseek-low-d1r2` vs `doc11-deepseek-low-b1` | entre prompts | 19 | 12 + 16 | 54 % |

## La cuenta

- **Dentro del mismo prompt** (1 pares): 29 datos en pareja, 7 sueltos, acuerdo 85 %.
- **Entre prompts** (2 pares): 19 datos en pareja, 30 sueltos, acuerdo 54 %.

**El ruido de adentro mide 85 % y la diferencia entre prompts 54 %** — hay separación entre los dos.

Los datos de cada corrida: `doc11-deepseek-low-d1` 34, `doc11-deepseek-low-d1r2` 31, `doc11-deepseek-low-b1` 35.
