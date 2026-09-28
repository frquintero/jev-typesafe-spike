TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Oración: el texto que va de un punto, signo de interrogación o signo de exclamación al siguiente. En `texto` va numerada ([1], [2], …).
- Subtema: un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas.
- Desarrollo: una oración desarrolla un subtema si lo detalla, lo explica, lo continúa, lo contradice o saca su consecuencia. Si abre un asunto que no depende de ninguno anterior, empieza un subtema nuevo.
- Nombrar el mismo lugar, objeto o persona no basta para unir oraciones: lo que las une es el asunto. Un cambio de párrafo no separa por sí solo un subtema.
- Nombre del subtema: una frase breve que dice qué se dice de las cosas, no solo cuáles son («el tamaño de la tripulación», no «la tripulación»).
- Cada oración va en un solo subtema.

EJEMPLO 1
Muestra un subtema que sigue después del cambio de párrafo: sus oraciones van juntas.
`texto`
<<<
[1] El ferri sale del puerto a las 7. [2] El cruce dura cuarenta minutos.

[3] Con mal tiempo, el cruce puede tardar el doble. [4] La tripulación tiene seis personas.
>>>
{"subtemas": [
  {"subtema": "el horario y la duración del cruce", "oraciones": [1, 2, 3]},
  {"subtema": "el tamaño de la tripulación", "oraciones": [4]}]}

EJEMPLO 2
Muestra las mismas cosas (la escuela, los alumnos) en asuntos distintos: van en subtemas distintos; la falla de la estufa desarrolla la calefacción.
`texto`
<<<
[1] La escuela rural tiene 60 alumnos. [2] Sus aulas se calientan con estufas de leña. [3] En invierno, la estufa del aula 2 falló dos veces. [4] Los alumnos de la escuela ganaron el concurso regional de lectura. [5] Su maestra preparó al equipo durante tres meses.
>>>
{"subtemas": [
  {"subtema": "el número de alumnos de la escuela", "oraciones": [1]},
  {"subtema": "la calefacción de las aulas y sus fallas", "oraciones": [2, 3]},
  {"subtema": "el triunfo en el concurso de lectura", "oraciones": [4, 5]}]}

EJEMPLO 3
Muestra una afirmación y la que la contradice: forman un solo subtema.
`texto`
<<<
[1] El manual de 1990 fijaba en 20 toneladas la carga máxima del puente del río Seco. [2] La inspección de este año la redujo a 12 toneladas por unas grietas en las vigas. [3] El puente fue construido en 1962 con vigas de concreto.
>>>
{"subtemas": [
  {"subtema": "la capacidad de carga del puente", "oraciones": [1, 2]},
  {"subtema": "la construcción del puente", "oraciones": [3]}]}

EJEMPLO 4
Muestra un hecho y su consecuencia: forman un solo subtema.
`texto`
<<<
[1] Las lluvias de mayo fueron escasas en la cuenca alta. [2] Por eso el embalse bajó al 40 % de su capacidad. [3] La represa abastece de agua a dos municipios.
>>>
{"subtemas": [
  {"subtema": "el descenso del embalse por la sequía", "oraciones": [1, 2]},
  {"subtema": "los municipios que abastece la represa", "oraciones": [3]}]}

EJEMPLO 5
Muestra un subtema que vuelve después de otro: sus oraciones separadas van juntas, aunque todo el texto hable del mismo mercado.
`texto`
<<<
[1] El mercado municipal abre a las 6. [2] Los puestos de frutas ocupan la nave central. [3] Los de pescado están en el ala norte. [4] Los sábados abre a las 5.
>>>
{"subtemas": [
  {"subtema": "el horario del mercado", "oraciones": [1, 4]},
  {"subtema": "la ubicación de los puestos", "oraciones": [2, 3]}]}

`texto`
<<<
{{TEXTO_NUMERADO}}
>>>
