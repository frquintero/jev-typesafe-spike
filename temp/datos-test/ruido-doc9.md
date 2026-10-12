# Ruido de la extracción de `doc9` (mismo modelo, mismas unidades)

| corrida | prompt | datos | con `unidad_valor` | segundos | entrada | salida (pensando) |
|---|---|---|---|---|---|---|
| `d1` | `temp/prompt_DATOS_test.md` | 32 | 18 | 19.8 | 5284 | 5582 (3310) |
| `d1r2` | `temp/prompt_DATOS_test.md` | 32 | 17 | 21.6 | 5284 | 6004 (3723) |
| `d2` | `mvp/prompts/prompt_DATOS.md` | 30 | 17 | 14.0 | 2389 | 4182 (2014) |
| `d2r2` | `mvp/prompts/prompt_DATOS.md` | 31 | 15 | 20.1 | 2389 | 5668 (3490) |
| `d3` | `temp/prompt_DATOS_test.md` | 32 | 16 | 24.1 | 3710 | 6779 (5470) |
| `d4` | `mvp/prompts/prompt_DATOS.md` | 31 | 15 | 28.6 | 1661 | 7890 (6469) |

## Par por par

`pares` = datos que se corresponden · `sueltos` = los que quedan sin par · `acuerdo` = pares / el mayor de los dos.

| par | tipo | pares | sueltos | acuerdo |
|---|---|---|---|---|
| `d1` vs `d1r2` | dentro del prompt | 31 | 1 + 1 | 97 % |
| `d1` vs `d2` | entre prompts | 30 | 2 + 0 | 94 % |
| `d1` vs `d2r2` | entre prompts | 28 | 4 + 3 | 88 % |
| `d1` vs `d3` | otro modelo | 27 | 5 + 5 | 84 % |
| `d1` vs `d4` | otro modelo | 28 | 4 + 3 | 88 % |
| `d1r2` vs `d2` | entre prompts | 29 | 3 + 1 | 91 % |
| `d1r2` vs `d2r2` | entre prompts | 30 | 2 + 1 | 94 % |
| `d1r2` vs `d3` | otro modelo | 26 | 6 + 6 | 81 % |
| `d1r2` vs `d4` | otro modelo | 30 | 2 + 1 | 94 % |
| `d2` vs `d2r2` | dentro del prompt | 29 | 1 + 2 | 94 % |
| `d2` vs `d3` | otro modelo | 23 | 7 + 9 | 72 % |
| `d2` vs `d4` | otro modelo | 27 | 3 + 4 | 87 % |
| `d2r2` vs `d3` | otro modelo | 26 | 5 + 6 | 81 % |
| `d2r2` vs `d4` | otro modelo | 27 | 4 + 4 | 87 % |
| `d3` vs `d4` | entre prompts | 27 | 5 + 4 | 84 % |

## La cuenta

- **Dentro del mismo prompt** (2 pares): 30 datos en pareja, 2 sueltos, acuerdo 95 %.
- **Entre prompts** (5 pares): 29 datos en pareja, 5 sueltos, acuerdo 90 %.

**El ruido de adentro mide 95 % y la diferencia entre prompts 90 %** — el prompt nuevo no se distingue del temblor.

Los datos de cada corrida: `d1` 32, `d1r2` 32, `d2` 30, `d2r2` 31, `d3` 32, `d4` 31.
