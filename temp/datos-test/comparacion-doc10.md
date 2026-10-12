# Extracción de datos de `doc10`: dos prompts, un modelo

| | `doc10-deepseek-low-d2` | `doc10-deepseek-low-b1` |
|---|---|---|
| prompt | temp/datos-decisiones/prompt_DATOS_decisiones_v7.md | mvp/prompts/prompt_DATOS.md |
| segundos | 55.9 | 22.2 |
| tokens de entrada | 2080 | 1761 |
| salida (pensando) | 14968 (13271) | 6919 (5181) |
| datos | 40 | 41 |
| con `unidad_valor` | 6 | 5 |
| verificación | sin problemas | sin problemas |

## El campo `unidad_valor`

- **doc10-deepseek-low-d2**: 6 de 40 datos (15 %) con unidad
- **doc10-deepseek-low-b1**: 5 de 41 datos (12 %) con unidad
- unidades de `doc10-deepseek-low-d2`: «años», «kilómetros», «kilómetros cuadrados», «metros»
- unidades de `doc10-deepseek-low-b1`: «años», «habitantes», «kilómetros», «kilómetros cuadrados»

## Unidad por unidad

Emparejado aproximado por parecido de aspecto (Jaccard sobre las palabras). `=` par, `+` solo en el primero, `-` solo en el segundo.

### n=1 · la época y la extensión de la civilización del Indo

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| + | época en que floreció la civilización del valle del Indo = entre el dos mil seiscientos y el mil novecientos antes de nuestra era |  |
| + | territorio donde floreció la civilización del valle del Indo, en la actualidad = en lo que hoy son Pakistán y el noroeste de la India |  |
| + | extensión ocupada por la civilización del valle del Indo = cerca de un millón **[kilómetros cuadrados]** |  |
| + | extensión de la civilización del valle del Indo comparada con la de Egipto y Mesopotamia juntas = mayor que la de Egipto y Mesopotamia juntas |  |
| - |  | periodo de florecimiento = entre el dos mil seiscientos y el mil novecientos antes de nuestra era |
| - |  | ubicación actual = en lo que hoy son Pakistán y el noroeste de la India |
| - |  | extensión = cerca de un millón **[kilómetros cuadrados]** |
| - |  | comparación de la extensión = mayor que la de Egipto y Mesopotamia juntas |

### n=2 · las ciudades de Harappa y Mohenjo-daro y la población de esta última

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| = | ciudades más estudiadas (de la civilización del valle del Indo) = Harappa y Mohenjo-daro | ciudades más estudiadas = Harappa y Mohenjo-daro |
| = | distancia entre Harappa y Mohenjo-daro = unos seiscientos **[kilómetros]** | distancia entre Harappa y Mohenjo-daro = unos seiscientos **[kilómetros]** |
| + | número de habitantes que llegó a tener Mohenjo-daro, según las estimaciones más citadas = unos cuarenta mil |  |
| - |  | población de Mohenjo-daro = unos cuarenta mil **[habitantes]** |
| - |  | base de la estimación de población = las estimaciones más citadas |

### n=3 · el urbanismo: calles en cuadrícula, desagües, ladrillos normalizados y el Gran Baño impermeabilizado

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| = | trazado de las calles = en cuadrícula | trazado de las calles = en cuadrícula |
| = | proporción de casas que tenían acceso a un desagüe cubierto = casi todas | acceso a desagüe cubierto = casi todas las casas tenían acceso a un desagüe cubierto |
| + | existencia de un equivalente de ese sistema (el de calles en cuadrícula y desagües cubiertos) en otras ciudades de la época = no tiene equivalente |  |
| = | proporción entre grosor, ancho y largo de los ladrillos cocidos = de uno a dos a cuatro | proporción de los ladrillos cocidos entre grosor, ancho y largo = uno a dos a cuatro |
| = | ubicación del llamado Gran Baño = en el centro de Mohenjo-daro | ubicación del Gran Baño = en el centro de Mohenjo-daro |
| = | dimensiones del llamado Gran Baño = doce por siete **[metros]** | dimensiones del Gran Baño = doce metros por siete y unos dos metros y medio de profundidad |
| = | profundidad del llamado Gran Baño = unos dos y medio **[metros]** | impermeabilización del Gran Baño = sellaron las juntas con betún |
| + | material con el que los constructores del Gran Baño sellaron las juntas para impermeabilizarlo = betún |  |
| - |  | comparación del sistema de desagüe = no tiene equivalente en otras ciudades de la época |

### n=4 · los sellos, la escritura sin descifrar y las pesas como pruebas del comercio

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| = | material de los sellos usados por los comerciantes del Indo = esteatita | material de los sellos = esteatita |
| = | tallado de los sellos usados por los comerciantes del Indo = con animales y signos | tallado de los sellos = con animales y signos |
| = | número de inscripciones conocidas = unas cuatro mil | número de inscripciones conocidas = unas cuatro mil |
| = | extensión de casi todas las inscripciones conocidas = muy breves | extensión de las inscripciones = casi todas muy breves |
| = | número de signos distintos en las inscripciones conocidas = cerca de cuatrocientos | número de signos distintos = cerca de cuatrocientos |
| + | estado de desciframiento de esa escritura (la de las inscripciones del Indo) = no ha sido descifrada |  |
| = | nombre del país mencionado en textos mesopotámicos = Meluhha | mención en textos mesopotámicos = un país llamado Meluhha, de donde llegaban barcos con cornalina y marfil |
| + | procedencia de los barcos con cornalina y marfil = de Meluhha |  |
| + | carga de los barcos que llegaban de Meluhha = cornalina y marfil |  |
| = | identificación de Meluhha según la mayoría de los historiadores = con el valle del Indo | identificación de Meluhha por la mayoría de los historiadores = con el valle del Indo |
| = | patrón que seguían las pesas de piedra en toda la región = un mismo patrón | patrón de las pesas = cada una pesaba el doble de la anterior, hasta llegar a sesenta y cuatro veces la más pequeña |
| + | peso de cada pesa de piedra respecto de la anterior = el doble de la anterior |  |
| + | peso máximo de las pesas de piedra respecto de la más pequeña = sesenta y cuatro veces |  |
| - |  | usuarios de los sellos = los comerciantes del Indo |
| - |  | estado de la escritura = no ha sido descifrada |
| - |  | material de las pesas = piedra |

### n=5 · las excavaciones de Marshall y Wheeler y la hipótesis de la invasión

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| = | fecha del anuncio del descubrimiento de Mohenjo-daro por John Marshall = mil novecientos veinticuatro | fecha del anuncio del descubrimiento de Mohenjo-daro = mil novecientos veinticuatro |
| = | fecha en que Mortimer Wheeler retomó las excavaciones = en los años cuarenta | fecha de retoma de las excavaciones = los años cuarenta |
| + | autor de la atribución del final (de la civilización del Indo) a una invasión = él (John Marshall o Mortimer Wheeler) |  |
| + | causa a la que él (John Marshall o Mortimer Wheeler) atribuyó el final (de la civilización del Indo) = una invasión |  |
| + | apoyo actual a la idea de que el final (de la civilización del Indo) se debió a una invasión = casi nadie la sostiene |  |
| - |  | anunciante del descubrimiento de Mohenjo-daro = John Marshall |
| - |  | responsable de retomar las excavaciones = Mortimer Wheeler |
| - |  | atribución del final por Wheeler = a una invasión |
| - |  | vigencia de la hipótesis de la invasión = hoy casi nadie la sostiene |

### n=6 · el abandono de las grandes ciudades y sus causas climáticas

| | doc10-deepseek-low-d2 | doc10-deepseek-low-b1 |
|---|---|---|
| = | época en que se fueron vaciando las grandes ciudades = hacia el mil novecientos antes de nuestra era | proceso de las grandes ciudades = se fueron vaciando |
| = | causa del abandono de las grandes ciudades a la que apuntan los estudios recientes = un debilitamiento del monzón | causa apuntada por estudios recientes = un debilitamiento del monzón |
| = | duración de la sequía sugerida por los sedimentos de los lagos = unos doscientos **[años]** | duración de la sequía = unos doscientos **[años]** |
| + | efecto de una sequía de unos doscientos años, como sugieren los sedimentos de los lagos = los campos de cereal no pudieron sostener a las ciudades |  |
| = | cambio en el río Ghaggar-Hakra = dejó de llevar agua todo el año | cambio del río Ghaggar-Hakra = dejó de llevar agua todo el año |
| = | fecha del cambio en el río Ghaggar-Hakra (dejar de llevar agua todo el año) = hace unos cuatro mil **[años]** | fecha del cambio del río Ghaggar-Hakra = hace unos cuatro mil **[años]** |
| = | ubicación del río Ghaggar-Hakra = al este del Indo | ubicación del río Ghaggar-Hakra = al este del Indo |
| - |  | fecha del vaciado de las grandes ciudades = hacia el mil novecientos antes de nuestra era |
| - |  | evidencia de la sequía = los sedimentos de los lagos |
| - |  | consecuencia de la sequía = los campos de cereal no pudieron sostener a las ciudades |

**Pares: 24 · solo en `doc10-deepseek-low-d2`: 16 · solo en `doc10-deepseek-low-b1`: 17.**
