TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Oración: el texto que va de un punto, signo de interrogación o signo de exclamación al siguiente. En `texto` va numerada ([1], [2], …).
- Subtema: un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas.
- Desarrollo: una oración desarrolla un subtema si lo detalla, lo explica, lo continúa, lo contradice o saca su consecuencia. Si abre un asunto que no depende de ninguno anterior, empieza un subtema nuevo.
- Nombrar el mismo lugar, objeto o persona no basta para unir oraciones: lo que las une es el asunto. Un cambio de párrafo no separa por sí solo un subtema.
- Nombre del subtema: una frase breve que nombra el asunto.
- Cada oración va en un solo subtema. Los subtemas se listan en el orden de su primera oración.

EJEMPLO 1
Muestra un párrafo con dos subtemas: sus oraciones se reparten en dos.
`texto`
<<<
[1] El horno principal de la panadería alcanza 250 °C en veinte minutos. [2] Su puerta de vidrio permite vigilar el dorado del pan. [3] Los clientes prefieren el pan integral. [4] Los sábados las ventas se duplican.
>>>
{"subtemas": [
  {"subtema": "el horno de la panadería", "oraciones": [1, 2]},
  {"subtema": "la demanda de los clientes", "oraciones": [3, 4]}]}

EJEMPLO 2
Muestra un subtema que sigue después del cambio de párrafo: sus oraciones van juntas.
`texto`
<<<
[1] El ferri sale del puerto a las 7. [2] El cruce dura cuarenta minutos.

[3] Con mal tiempo, el cruce puede tardar el doble. [4] La tripulación tiene seis personas.
>>>
{"subtemas": [
  {"subtema": "horario y duración del cruce", "oraciones": [1, 2, 3]},
  {"subtema": "la tripulación", "oraciones": [4]}]}

EJEMPLO 3
Muestra las mismas cosas (la escuela, los alumnos) en asuntos distintos: van en subtemas distintos; la falla de la estufa desarrolla la calefacción.
`texto`
<<<
[1] La escuela rural tiene 60 alumnos. [2] Sus aulas se calientan con estufas de leña. [3] En invierno, la estufa del aula 2 falló dos veces. [4] Los alumnos de la escuela ganaron el concurso regional de lectura. [5] Su maestra preparó al equipo durante tres meses.
>>>
{"subtemas": [
  {"subtema": "la matrícula de la escuela", "oraciones": [1]},
  {"subtema": "la calefacción de las aulas", "oraciones": [2, 3]},
  {"subtema": "el concurso de lectura", "oraciones": [4, 5]}]}

EJEMPLO 4
Muestra una afirmación y la que la contradice: forman un solo subtema.
`texto`
<<<
[1] El manual de 1990 fijaba en 20 toneladas la carga máxima del puente del río Seco. [2] La inspección de este año la redujo a 12 toneladas por unas grietas en las vigas. [3] El puente fue construido en 1962 con vigas de concreto.
>>>
{"subtemas": [
  {"subtema": "la capacidad de carga del puente", "oraciones": [1, 2]},
  {"subtema": "la construcción del puente", "oraciones": [3]}]}

EJEMPLO 5
Muestra un hecho y su consecuencia: forman un solo subtema.
`texto`
<<<
[1] Las lluvias de mayo fueron escasas en la cuenca alta. [2] Por eso el embalse bajó al 40 % de su capacidad. [3] La represa abastece de agua a dos municipios.
>>>
{"subtemas": [
  {"subtema": "el descenso del embalse", "oraciones": [1, 2]},
  {"subtema": "el abastecimiento de agua", "oraciones": [3]}]}

EJEMPLO 6
Muestra un subtema que vuelve después de otro: sus oraciones separadas van juntas, aunque todo el texto hable del mismo mercado.
`texto`
<<<
[1] El mercado municipal abre a las 6. [2] Los puestos de frutas ocupan la nave central. [3] Los de pescado están en el ala norte. [4] Los sábados abre a las 5.
>>>
{"subtemas": [
  {"subtema": "el horario del mercado", "oraciones": [1, 4]},
  {"subtema": "la distribución de los puestos", "oraciones": [2, 3]}]}

`texto`
<<<
{{TEXTO_NUMERADO}}
>>>
