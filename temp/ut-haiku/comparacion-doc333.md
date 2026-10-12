# Particiones de `doc333` (14 oraciones)

## Las corridas

| corrida | modelo | esfuerzo | unidades | segundos | tokens salida (pensando) | verificación |
|---|---|---|---|---|---|---|
| doc333-deepseek-low-tr1 | deepseek-flash | low | 8 | 45.9 | 10227 (9971) | {"oraciones_del_texto": 14, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |
| doc333-haiku-high-tr1 | claude-haiku-5-5 | high | 6 | 22.3 | 4332 (4020) | {"oraciones_del_texto": 14, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |

## La partición de cada una

**doc333-deepseek-low-tr1** (8 unidades)

- `[1,2]` el inicio de la guerra y la ocupación de Europa continental por el Eje
- `[3]` la resistencia del Reino Unido a los bombardeos alemanes
- `[4,8]` la invasión alemana de la Unión Soviética y la extensión del frente oriental
- `[5,6,7]` la extensión, la duración y la mortalidad de la contienda
- `[9]` la producción industrial de Estados Unidos durante la guerra
- `[10,11]` el final de la guerra y la destrucción de ciudades
- `[12,13]` la creación de la ONU y el plan de reconstrucción para Europa
- `[14]` la división de los antiguos aliados en dos bloques

**doc333-haiku-high-tr1** (6 unidades)

- `[1,2,3]` el inicio de la guerra en 1939 y la ocupación de casi toda Europa por el Eje
- `[4,8]` la apertura del frente oriental en 1941 y la extensión de su línea de batalla
- `[5,6,7,9]` la magnitud de la guerra: países, duración, víctimas y producción industrial de armamento
- `[10,11,13]` el fin de la guerra, la destrucción de Alemania y el plan de reconstrucción de Europa
- `[12]` la fundación de la ONU
- `[14]` la división de los antiguos aliados en dos bloques enfrentados

## Oración por oración (el grupo al que fue)

| oración | doc333-deepseek-low-tr1 | doc333-haiku-high-tr1 |
|---|---|---|
| 1 | 1,2 | 1,2,3 |
| 2 | 1,2 | 1,2,3 |
| 3 | 3 | 1,2,3 |
| 4 | 4,8 | 4,8 |
| 5 | 5,6,7 | 5,6,7,9 |
| 6 | 5,6,7 | 5,6,7,9 |
| 7 | 5,6,7 | 5,6,7,9 |
| 8 | 4,8 | 4,8 |
| 9 | 9 | 5,6,7,9 |
| 10 | 10,11 | 10,11,13 |
| 11 | 10,11 | 10,11,13 |
| 12 | 12,13 | 12 |
| 13 | 12,13 | 10,11,13 |
| 14 | 14 | 14 |

## Qué coincide y qué no

- Iguales a la del registro: doc333-deepseek-low-tr1.
- Particiones distintas entre sí: sí.
- Oraciones donde no todas coinciden: 1, 2, 3, 5, 6, 7, 9, 10, 11, 12, 13.
- Grupos que aparecen en una sola corrida: `[1,2]` (doc333-deepseek-low-tr1); `[1,2,3]` (doc333-haiku-high-tr1); `[3]` (doc333-deepseek-low-tr1); `[5,6,7]` (doc333-deepseek-low-tr1); `[5,6,7,9]` (doc333-haiku-high-tr1); `[9]` (doc333-deepseek-low-tr1); `[10,11]` (doc333-deepseek-low-tr1); `[10,11,13]` (doc333-haiku-high-tr1); `[12,13]` (doc333-deepseek-low-tr1); `[12]` (doc333-haiku-high-tr1)
