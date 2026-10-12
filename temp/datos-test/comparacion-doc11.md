# Extracción de datos de `doc11`: dos prompts, un modelo

| | `doc11-deepseek-low-d1` | `doc11-deepseek-low-b1` |
|---|---|---|
| prompt | temp/datos-decisiones/prompt_DATOS_decisiones_v7.md | mvp/prompts/prompt_DATOS.md |
| segundos | 52.5 | 18.1 |
| tokens de entrada | 2033 | 1714 |
| salida (pensando) | 13790 (12304) | 5403 (3778) |
| datos | 34 | 35 |
| con `unidad_valor` | 4 | 4 |
| verificación | sin problemas | sin problemas |

## El campo `unidad_valor`

- **doc11-deepseek-low-d1**: 4 de 34 datos (12 %) con unidad
- **doc11-deepseek-low-b1**: 4 de 35 datos (11 %) con unidad
- unidades de `doc11-deepseek-low-d1`: «días», «dólares», «por ciento»
- unidades de `doc11-deepseek-low-b1`: «días», «dólares», «por ciento»

## Unidad por unidad

Emparejado aproximado por parecido de aspecto (Jaccard sobre las palabras). `=` par, `+` solo en el primero, `-` solo en el segundo.

### n=1 · la mutación de una letra del gen de la hemoglobina que deforma los glóbulos rojos y acorta su vida

| | doc11-deepseek-low-d1 | doc11-deepseek-low-b1 |
|---|---|---|
| = | causa de la anemia falciforme = el cambio de una sola letra en el gen de la beta globina | causa de la anemia falciforme = el cambio de una sola letra en el gen de la beta globina |
| = | ubicación del gen de la beta globina = el cromosoma once | ubicación del gen de la beta globina = el cromosoma once |
| = | aminoácido sustituido en la posición seis de la proteína = un ácido glutámico | posición en la proteína de la sustitución = seis |
| + | aminoácido que sustituye en la posición seis de la proteína = una valina |  |
| + | nombre de la hemoglobina que resulta (del cambio de una sola letra en el gen de la beta globina) = hemoglobina S |  |
| = | comportamiento de la hemoglobina S cuando le falta oxígeno = se agrupa en fibras rígidas | comportamiento de la hemoglobina S = se agrupa en fibras rígidas cuando le falta oxígeno |
| + | efecto de esas fibras (las fibras rígidas de la hemoglobina S) = deforman los glóbulos rojos |  |
| + | cambio de forma de los glóbulos rojos deformados = pierden su forma de disco y toman la de una hoz |  |
| = | duración de la vida de un glóbulo rojo sano = unos ciento veinte **[días]** | vida de un glóbulo rojo sano = unos ciento veinte **[días]** |
| = | duración de la vida de un glóbulo rojo falciforme = entre diez y veinte **[días]** | vida de un glóbulo falciforme = entre diez y veinte **[días]** |
| - |  | sustitución en la proteína = un ácido glutámico queda sustituido por una valina |
| - |  | hemoglobina resultante = hemoglobina S |
| - |  | efecto de las fibras en los glóbulos rojos = deforman los glóbulos rojos, que pierden su forma de disco y toman la de una hoz |

### n=2 · la historia del diagnóstico, desde la descripción de 1910 hasta el hallazgo de la proteína alterada

| | doc11-deepseek-low-d1 | doc11-deepseek-low-b1 |
|---|---|---|
| = | fecha de la descripción de la enfermedad = hace más de un siglo, en mil novecientos diez | fecha de la descripción = mil novecientos diez |
| + | autor de la observación de glóbulos alargados en la sangre de un estudiante (en mil novecientos diez) = un médico de Chicago |  |
| + | hallazgo de la observación (en mil novecientos diez) = glóbulos alargados en la sangre de un estudiante |  |
| = | fecha del hallazgo de Linus Pauling (sobre la migración de la hemoglobina de los enfermos) = mil novecientos cuarenta y nueve | hallazgo de Linus Pauling = la hemoglobina de los enfermos migraba de otro modo en un campo eléctrico |
| + | autor del hallazgo de que la hemoglobina de los enfermos migraba de otro modo en un campo eléctrico = Linus Pauling |  |
| + | comportamiento de la hemoglobina de los enfermos en un campo eléctrico = migraba de otro modo |  |
| + | fecha de la identificación del aminoácido sustituido = mil novecientos cincuenta y siete |  |
| + | autor de la identificación del aminoácido sustituido = Vernon Ingram |  |
| + | denominación que Vernon Ingram dio a la anemia falciforme = una enfermedad molecular |  |
| + | efecto de ese hallazgo (la identificación del aminoácido sustituido por Vernon Ingram) sobre la anemia falciforme = convirtió a la anemia falciforme en la primera enfermedad explicada por un cambio en una proteína |  |
| - |  | antigüedad de la descripción = más de un siglo |
| - |  | autor de la descripción = un médico de Chicago |
| - |  | observación del médico de Chicago = glóbulos alargados en la sangre de un estudiante |
| - |  | año del hallazgo de Linus Pauling = mil novecientos cuarenta y nueve |
| - |  | año de la identificación de Vernon Ingram = mil novecientos cincuenta y siete |
| - |  | hallazgo de Vernon Ingram = identificó el aminoácido sustituido |
| - |  | denominación de Ingram para la enfermedad = una enfermedad molecular |
| - |  | importancia del hallazgo = convirtió a la anemia falciforme en la primera enfermedad explicada por un cambio en una proteína |

### n=3 · la herencia recesiva y la protección que ofrecen los portadores frente a la malaria

| | doc11-deepseek-low-d1 | doc11-deepseek-low-b1 |
|---|---|---|
| = | tipo de herencia de la enfermedad = recesiva | tipo de herencia = recesiva |
| = | condición de quien recibe una sola copia alterada = es portador | efecto de recibir una sola copia alterada = es portador y casi nunca enferma |
| + | frecuencia con que enferma quien recibe una sola copia alterada = casi nunca |  |
| = | probabilidad por embarazo de que dos padres portadores tengan un hijo enfermo = uno en cuatro | probabilidad por embarazo si ambos padres son portadores = uno en cuatro de dar un hijo enfermo |
| + | efecto de ser portador sobre la malaria grave = resisten mejor la malaria grave |  |
| = | reducción del riesgo de malaria grave en los portadores por esa ventaja (la mejor resistencia a la malaria grave) = cerca de un noventa, según los estudios de campo **[por ciento]** | reducción del riesgo de malaria grave en portadores = cerca de noventa **[por ciento]** |
| = | proporción de habitantes que llevan la mutación en algunas regiones de África = hasta uno de cada cuatro | frecuencia de la mutación en algunas regiones de África = hasta uno de cada cuatro habitantes lleva la mutación |
| - |  | resistencia de los portadores = resisten mejor la malaria grave |
| - |  | fuente de la ventaja de los portadores = los estudios de campo |

### n=4 · la cifra anual de niños que nacen con formas graves de la enfermedad

| | doc11-deepseek-low-d1 | doc11-deepseek-low-b1 |
|---|---|---|
| = | número anual de niños que nacen con formas graves de la enfermedad = unos trescientos mil, según la Organización Mundial de la Salud | cifra de niños que nacen con formas graves de la enfermedad = unos trescientos mil |
| - |  | fuente de la cifra = la Organización Mundial de la Salud |
| - |  | periodicidad de los nacimientos = cada año |

### n=5 · los tratamientos: la hidroxiurea, la terapia CRISPR aprobada en 2023 y su costo

| | doc11-deepseek-low-d1 | doc11-deepseek-low-b1 |
|---|---|---|
| = | tratamiento clásico de la anemia falciforme (la enfermedad) = la hidroxiurea | tratamiento clásico = la hidroxiurea |
| = | efecto de la hidroxiurea = aumenta la hemoglobina fetal | efecto de la hidroxiurea = aumenta la hemoglobina fetal |
| = | fecha de aprobación de la hidroxiurea para adultos = mil novecientos noventa y ocho | aprobación de la hidroxiurea = para adultos en mil novecientos noventa y ocho |
| = | fecha de aprobación de la primera terapia basada en la edición genética con CRISPR = diciembre de dos mil veintitrés | aprobación de la primera terapia basada en la edición genética con CRISPR = diciembre de dos mil veintitrés |
| + | proporción de pacientes en el ensayo principal que pasaron al menos un año sin crisis de dolor = veintinueve de treinta |  |
| = | costo de cada tratamiento (de la terapia CRISPR) = unos dos millones **[dólares]** | costo de cada tratamiento = unos dos millones **[dólares]** |
| - |  | resultado del ensayo principal = veintinueve de treinta pacientes pasaron al menos un año sin crisis de dolor |

**Pares: 19 · solo en `doc11-deepseek-low-d1`: 15 · solo en `doc11-deepseek-low-b1`: 16.**
