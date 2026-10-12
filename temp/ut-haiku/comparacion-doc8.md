# Particiones de `doc8` (18 oraciones)

## Las corridas

| corrida | modelo | esfuerzo | unidades | segundos | tokens salida (pensando) | verificación |
|---|---|---|---|---|---|---|
| registro | deepseek-flash | low | 8 | 53.4 | 11260 (10973) | — |
| deepseek-low-r1 | deepseek-flash | low | 8 | 48.2 | 10288 (10002) | {"oraciones_del_texto": 18, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |
| haiku-high-r1 | claude-haiku-5-5 | high | 7 | 11.8 | 2405 (2079) | {"oraciones_del_texto": 18, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |
| haiku-high-r2 | claude-haiku-5-5 | high | 9 | 15.6 | 3012 (2647) | {"oraciones_del_texto": 18, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |
| haiku-high-r3 | claude-haiku-5-5 | high | 8 | 21.8 | 2753 (2399) | {"oraciones_del_texto": 18, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |
| haiku-high-r4 | claude-haiku-5-5 | high | 8 | 13.8 | 2939 (2536) | {"oraciones_del_texto": 18, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []} |

## La partición de cada una

**registro** (8 unidades)

- `[1,4]` la aparición de la vida y los primeros microorganismos en el océano
- `[2,3]` la extensión, la profundidad y la temperatura del océano
- `[5,6,7,8]` la explosión del Cámbrico y la evolución de los animales hasta la conquista de la tierra firme
- `[9,10]` el regreso al mar de los antepasados de las ballenas
- `[11,12,13]` el tamaño, el buceo y la alimentación de la ballena azul
- `[14,15,16]` el calentamiento y la acidificación actuales del mar y su efecto en los corales
- `[17]` la extensión y la biodiversidad de los arrecifes
- `[18]` la ampliación de una reserva del Pacífico

**deepseek-low-r1** (8 unidades)

- `[1,4]` el origen de la vida en el océano y los primeros microorganismos
- `[2,3]` la extensión, la profundidad y la temperatura del océano
- `[5,6]` la explosión cámbrica y la aparición de los primeros peces
- `[7,8]` la salida del agua y la conquista de la tierra firme
- `[9,10]` el regreso al mar de algunos linajes, como los antepasados de las ballenas
- `[11,12,13]` las características de la ballena azul: tamaño, buceo y alimentación
- `[14,15,16,17]` el cambio actual del mar y sus efectos en el calor, la acidez y los arrecifes
- `[18]` la ampliación de una reserva del Pacífico

**haiku-high-r1** (7 unidades)

- `[1,4]` el origen de la vida en el océano y su predominio durante miles de millones de años
- `[2,3]` la extensión, la profundidad y la temperatura del océano
- `[5,6,7,8]` la evolución de los animales desde el Cámbrico hasta la conquista de la tierra
- `[9,10]` el regreso de algunos linajes al mar
- `[11,12,13]` las características de la ballena azul
- `[14,15,16,17]` el cambio actual del mar y su efecto sobre los arrecifes de coral
- `[18]` el crecimiento de una reserva marina del Pacífico

**haiku-high-r2** (9 unidades)

- `[1,4]` el origen de la vida en el océano
- `[2,3]` la extensión y la temperatura profunda del océano
- `[5]` la explosión de la diversidad animal en el Cámbrico
- `[6,7,8]` la conquista de la tierra firme desde los peces
- `[9,10]` el regreso de algunos linajes al mar
- `[11,12,13]` las dimensiones y los hábitos de la ballena azul
- `[14,15,16]` los cambios del mar por el calor y la acidez
- `[17]` la importancia de los arrecifes de coral
- `[18]` el crecimiento de una reserva marina del Pacífico

**haiku-high-r3** (8 unidades)

- `[1,4]` la aparición de la vida en el mar
- `[2,3]` la extensión, la profundidad y la temperatura del océano
- `[5,6]` la aparición de los grandes grupos animales y de los primeros peces
- `[7,8,9,10]` la salida de los animales a tierra firme y el regreso de algunos linajes al mar
- `[11,12,13]` las características de la ballena azul
- `[14,15]` el mar absorbe el calor extra y cambia más rápido que antes
- `[16,17]` la acidez del agua y sus efectos sobre los arrecifes
- `[18]` el aumento de la reserva marina del Pacífico

**haiku-high-r4** (8 unidades)

- `[1,4]` el origen de la vida en el océano y los primeros seres vivos
- `[2,3]` la extensión y la profundidad del océano y la temperatura de su fondo
- `[5]` la explosión del Cámbrico y la aparición de los grandes grupos animales
- `[6,7,8]` la salida de los peces a tierra y la lenta conquista de la tierra firme
- `[9,10]` el regreso de algunos linajes al mar, con los antepasados de las ballenas
- `[11,12,13]` el tamaño, el buceo y la lactancia de la ballena azul
- `[14,15,16,17]` el calentamiento y la acidificación del mar actual y sus efectos sobre los corales y arrecifes
- `[18]` el crecimiento de una reserva marina del Pacífico

## Oración por oración (el grupo al que fue)

| oración | registro | deepseek-low-r1 | haiku-high-r1 | haiku-high-r2 | haiku-high-r3 | haiku-high-r4 |
|---|---|---|---|---|---|---|
| 1 | 1,4 | 1,4 | 1,4 | 1,4 | 1,4 | 1,4 |
| 2 | 2,3 | 2,3 | 2,3 | 2,3 | 2,3 | 2,3 |
| 3 | 2,3 | 2,3 | 2,3 | 2,3 | 2,3 | 2,3 |
| 4 | 1,4 | 1,4 | 1,4 | 1,4 | 1,4 | 1,4 |
| 5 | 5,6,7,8 | 5,6 | 5,6,7,8 | 5 | 5,6 | 5 |
| 6 | 5,6,7,8 | 5,6 | 5,6,7,8 | 6,7,8 | 5,6 | 6,7,8 |
| 7 | 5,6,7,8 | 7,8 | 5,6,7,8 | 6,7,8 | 7,8,9,10 | 6,7,8 |
| 8 | 5,6,7,8 | 7,8 | 5,6,7,8 | 6,7,8 | 7,8,9,10 | 6,7,8 |
| 9 | 9,10 | 9,10 | 9,10 | 9,10 | 7,8,9,10 | 9,10 |
| 10 | 9,10 | 9,10 | 9,10 | 9,10 | 7,8,9,10 | 9,10 |
| 11 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 |
| 12 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 |
| 13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 | 11,12,13 |
| 14 | 14,15,16 | 14,15,16,17 | 14,15,16,17 | 14,15,16 | 14,15 | 14,15,16,17 |
| 15 | 14,15,16 | 14,15,16,17 | 14,15,16,17 | 14,15,16 | 14,15 | 14,15,16,17 |
| 16 | 14,15,16 | 14,15,16,17 | 14,15,16,17 | 14,15,16 | 16,17 | 14,15,16,17 |
| 17 | 17 | 14,15,16,17 | 14,15,16,17 | 17 | 16,17 | 14,15,16,17 |
| 18 | 18 | 18 | 18 | 18 | 18 | 18 |

## Qué coincide y qué no

- Iguales a la del registro: registro.
- Particiones distintas entre sí: sí.
- Oraciones donde no todas coinciden: 5, 6, 7, 8, 9, 10, 14, 15, 16, 17.
- Grupos que aparecen en una sola corrida: `[7,8]` (deepseek-low-r1); `[7,8,9,10]` (haiku-high-r3); `[14,15]` (haiku-high-r3); `[16,17]` (haiku-high-r3)
