# Extracción de datos de `doc9`: dos prompts, un modelo

| | `doc9-haiku-high-d1` | `doc9-haiku-high-d2` |
|---|---|---|
| prompt | temp/prompt_DATOS_test.md | mvp/prompts/prompt_DATOS.md |
| segundos | 19.8 | 14.0 |
| tokens de entrada | 5284 | 2389 |
| salida (pensando) | 5582 (3310) | 4182 (2014) |
| datos | 32 | 30 |
| con `unidad_valor` | 18 | 17 |
| verificación | sin problemas | sin problemas |

## El campo `unidad_valor`

- **doc9-haiku-high-d1**: 18 de 32 datos (56 %) con unidad
- **doc9-haiku-high-d2**: 17 de 30 datos (57 %) con unidad
- unidades de `doc9-haiku-high-d1`: «años», «años luz», «centímetros por año», «estrellas», «exoplanetas», «grados centígrados», «kilómetros», «radiotelescopios», «toneladas», «veces el diámetro de la Tierra»
- unidades de `doc9-haiku-high-d2`: «años», «años luz», «centímetros por año», «estrellas», «exoplanetas», «grados centígrados», «kilómetros», «toneladas», «veces el diámetro de la Tierra»

## Unidad por unidad

Emparejado aproximado por parecido de aspecto (Jaccard sobre las palabras). `=` par, `+` solo en el primero, `-` solo en el segundo.

### n=1 · la distancia del Sol, su edad, su energía y la vida de las estrellas

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | distancia del Sol a la Tierra = unos ciento cincuenta millones **[kilómetros]** | distancia del Sol a la Tierra = unos ciento cincuenta millones **[kilómetros]** |
| = | tiempo que tarda la luz del Sol en llegar a la Tierra = ocho minutos y veinte segundos | tiempo que tarda la luz del Sol en llegar a la Tierra = ocho minutos y veinte segundos |
| = | edad del Sol = unos cuatro mil seiscientos millones **[años]** | edad del Sol = unos cuatro mil seiscientos millones **[años]** |
| = | temperatura en el núcleo del Sol = quince millones **[grados centígrados]** | temperatura en el núcleo del Sol = quince millones **[grados centígrados]** |
| = | hidrógeno que el Sol convierte en helio cada segundo = unos seiscientos millones **[toneladas]** | cantidad de hidrógeno que el Sol convierte en helio cada segundo = unos seiscientos millones **[toneladas]** |
| = | lo que depende de la energía del Sol = toda la vida en la Tierra | relación de la energía del Sol con la vida en la Tierra = toda la vida en la Tierra depende de esa energía |
| = | modo en que las plantas capturan la energía del Sol = mediante la fotosíntesis | forma en que las plantas capturan la energía solar = mediante la fotosíntesis |
| = | duración de la vida de las estrellas más masivas = apenas unos pocos millones **[años]** | duración de la vida de las estrellas más masivas = unos pocos millones **[años]** |
| = | duración de la vida de las estrellas más pequeñas = decenas de miles de millones **[años]** | duración de la vida de las estrellas más pequeñas = decenas de miles de millones **[años]** |

### n=2 · el tamaño de Júpiter y los anillos de Saturno

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | posición de Júpiter por tamaño en el sistema solar = el planeta más grande del sistema solar | posición de Júpiter en el sistema solar = el planeta más grande del sistema solar |
| = | diámetro de Júpiter = ciento cuarenta y tres mil **[kilómetros]** | diámetro de Júpiter = ciento cuarenta y tres mil **[kilómetros]** |
| = | diámetro de Júpiter comparado con el de la Tierra = once **[veces el diámetro de la Tierra]** | diámetro de Júpiter comparado con el de la Tierra = once **[veces el diámetro de la Tierra]** |
| = | material de los anillos de Saturno = hielo y polvo | composición de los anillos de Saturno = hielo y polvo |
| = | extensión de los anillos de Saturno = unos doscientos ochenta mil **[kilómetros]** | extensión de los anillos de Saturno = unos doscientos ochenta mil **[kilómetros]** |

### n=3 · el alejamiento de la Luna respecto de la Tierra

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | ritmo de alejamiento de la Luna respecto de la Tierra = casi cuatro **[centímetros por año]** | velocidad de alejamiento de la Luna respecto de la Tierra = casi cuatro **[centímetros por año]** |
| = | forma de comprobar el alejamiento de la Luna = espejos dejados en su superficie | forma de comprobar el alejamiento de la Luna = con espejos dejados en su superficie |

### n=4 · la Vía Láctea, la galaxia Andrómeda y la expansión del universo

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | número de estrellas de la Vía Láctea = entre cien mil y cuatrocientos mil millones **[estrellas]** | cantidad de estrellas de la Vía Láctea = entre cien mil y cuatrocientos mil millones **[estrellas]** |
| = | diámetro del disco de la Vía Láctea = unos cien mil **[años luz]** | diámetro del disco de la Vía Láctea = unos cien mil **[años luz]** |
| = | tiempo que tarda el Sol en dar una vuelta alrededor del centro galáctico = cada doscientos treinta millones **[años]** | duración de una vuelta del Sol alrededor del centro galáctico = doscientos treinta millones **[años]** |
| = | galaxia más cercana a la Vía Láctea = Andrómeda | galaxia más cercana a la Vía Láctea = Andrómeda |
| = | distancia a la galaxia Andrómeda = dos millones y medio **[años luz]** | distancia a la galaxia Andrómeda = dos millones y medio **[años luz]** |
| = | movimiento de las galaxias = se alejan unas de otras | movimiento de las galaxias = se alejan unas de otras |
| = | tiempo de expansión del universo = desde hace casi catorce mil millones **[años]** | tiempo desde que el universo se expande = casi catorce mil millones **[años]** |

### n=5 · la luz antigua que captan los telescopios y lo que revela sobre el pasado

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | antigüedad de la luz que captan los telescopios actuales = hace más de trece mil millones **[años]** | antigüedad de la luz de galaxias lejanas captada por los telescopios actuales = más de trece mil millones **[años]** |
| + | origen de la luz que captan los telescopios actuales = galaxias lejanas |  |
| = | trabajo de la astronomía = con esa luz vieja | trabajo de la astronomía con esa luz = trabaja con esa luz vieja |
| = | lo que revela mirar lejos = mirar hacia atrás en el tiempo | lo que revela mirar lejos = mirar lejos es mirar hacia atrás en el tiempo |

### n=6 · los exoplanetas conocidos y la primera imagen de un agujero negro

| | doc9-haiku-high-d1 | doc9-haiku-high-d2 |
|---|---|---|
| = | fecha de confirmación del primer planeta fuera del sistema solar = mil novecientos noventa y dos | año de confirmación del primer planeta fuera del sistema solar = mil novecientos noventa y dos |
| = | número de exoplanetas conocidos hoy = más de cinco mil **[exoplanetas]** | cantidad de exoplanetas conocidos hoy = más de cinco mil **[exoplanetas]** |
| = | fecha de publicación de la primera imagen de un agujero negro = dos mil diecinueve | año de publicación de la primera imagen de un agujero negro = dos mil diecinueve |
| = | número de radiotelescopios que obtuvieron la primera imagen de un agujero negro = ocho **[radiotelescopios]** | instrumentos que obtuvieron la primera imagen de un agujero negro = ocho radiotelescopios coordinados de todo el planeta |
| + | alcance de la coordinación de los radiotelescopios = coordinados de todo el planeta |  |

**Pares: 30 · solo en `doc9-haiku-high-d1`: 2 · solo en `doc9-haiku-high-d2`: 0.**
