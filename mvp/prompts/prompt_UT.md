[SISTEMA]
TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y los ejemplos.
Responde solo con el JSON.
La forma es el contrato: no agregues claves fuera de las que define `SALIDA`.

DEFINICIONES
- Oración: el texto que va de un punto, signo de interrogación o signo de exclamación al siguiente. En `texto` va numerada ([1], [2], …).
- Subtema: una o varias oraciones asociadas o correlacionadas con una idea o asunto nuclear dentro del `texto` dado.
- Nombre del subtema: una frase breve que describe por sí sola el contenido de las oraciones del subtema.
- Todas y cada una de las oraciones de `texto` van en un solo subtema.
- Lo que une oraciones bajo un mismo subtema es que forman parte de una misma idea o asunto nuclear.

EJEMPLO 1
Cada subtema junta las oraciones que desarrollan una misma idea.

`texto`
<<<
[1] El océano cubre el setenta y uno por ciento de la superficie del planeta. [2] Su profundidad media es de tres mil setecientos metros, y en los fondos abisales la temperatura ronda los dos grados centígrados.

[3] La vida apareció en él hace unos tres mil quinientos millones de años. [4] Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado. [5] El océano regula además el clima: absorbe el calor que la atmósfera retiene en el verano. [6] Las corrientes que lo recorren reparten ese calor por el planeta y lo devuelven en el invierno.
>>>
{"subtemas": [
  {"subtema": "el océano: su extensión, profundidad y temperatura", "oraciones": [1, 2]},
  {"subtema": "el origen de la vida en el océano", "oraciones": [3]},
  {"subtema": "los primeros seres vivos y el tiempo en que el mar fue el único lugar habitado", "oraciones": [4]},
  {"subtema": "el papel del océano en la regulación del clima", "oraciones": [5, 6]}]}

EJEMPLO 2
Es el texto completo de un documento. Mira cuatro cosas en la respuesta: un subtema
cruza el párrafo ([1] con [5]), otro junta oraciones separadas ([13] con [16]), uno
es de una sola oración ([4]), y el Sol aparece en dos subtemas distintos (en [1] y
en [10]).

`texto`
<<<
[1] El Sol está a unos ciento cincuenta millones de kilómetros de la Tierra, y su luz tarda ocho minutos y veinte segundos en llegar. [2] Júpiter es el planeta más grande del sistema solar: su diámetro mide ciento cuarenta y tres mil kilómetros, once veces el de la Tierra. [3] Saturno está rodeado por anillos de hielo y polvo que se extienden unos doscientos ochenta mil kilómetros. [4] La Luna se aleja de nosotros casi cuatro centímetros por año, una medida que se comprueba con espejos dejados en su superficie.

[5] El Sol tiene unos cuatro mil seiscientos millones de años y en su núcleo la temperatura alcanza los quince millones de grados centígrados. [6] Cada segundo convierte unos seiscientos millones de toneladas de hidrógeno en helio. [7] De esa energía depende toda la vida en la Tierra, y las plantas la capturan mediante la fotosíntesis. [8] Las estrellas más masivas viven apenas unos pocos millones de años, mientras que las más pequeñas duran decenas de miles de millones.

[9] La Vía Láctea contiene entre cien mil y cuatrocientos mil millones de estrellas. [10] Su disco mide unos cien mil años luz de diámetro, y el Sol completa una vuelta alrededor del centro galáctico cada doscientos treinta millones de años. [11] La galaxia más cercana es Andrómeda, a dos millones y medio de años luz. [12] Las galaxias se alejan unas de otras: el universo se expande desde hace casi catorce mil millones de años.

[13] Los telescopios actuales detectan la luz que salió de galaxias lejanas hace más de trece mil millones de años. [14] El primer planeta fuera del sistema solar se confirmó en mil novecientos noventa y dos, y hoy se conocen más de cinco mil. [15] En dos mil diecinueve se publicó la primera imagen de un agujero negro, obtenida por ocho radiotelescopios coordinados de todo el planeta. [16] La astronomía trabaja con esa luz vieja: mirar lejos es mirar hacia atrás en el tiempo.
>>>
{"subtemas": [
  {"subtema": "el Sol: su distancia a la Tierra y la energía que sostiene la vida", "oraciones": [1, 5, 6, 7]},
  {"subtema": "el tamaño de Júpiter", "oraciones": [2]},
  {"subtema": "la composición y la extensión de los anillos de Saturno", "oraciones": [3]},
  {"subtema": "el alejamiento de la Luna respecto de la Tierra", "oraciones": [4]},
  {"subtema": "la duración de las estrellas según su masa", "oraciones": [8]},
  {"subtema": "el tamaño de la Vía Láctea y el recorrido del Sol en ella", "oraciones": [9, 10]},
  {"subtema": "la distancia a la galaxia Andrómeda", "oraciones": [11]},
  {"subtema": "la expansión del universo", "oraciones": [12]},
  {"subtema": "la luz vieja que captan los telescopios y lo que revela del pasado", "oraciones": [13, 16]},
  {"subtema": "fecha de confirmación del primer planeta fuera del sistema solar y la cantidad conocida hoy en día", "oraciones": [14]},
  {"subtema": "la publicación de la primera imagen de un agujero negro", "oraciones": [15]}]}

SALIDA
Devuelve únicamente el JSON, con esta estructura:

{"subtemas": [
  {"subtema": "…", "oraciones": [1, 2]},
  {"subtema": "…", "oraciones": [3]}]}

[TAREA]
`texto`
<<<
{{TEXTO_NUMERADO}}
>>>
