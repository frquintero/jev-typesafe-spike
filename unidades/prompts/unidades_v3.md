TAREA
Divide `texto` en unidades temáticas, según las definiciones y como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Oración: cada tramo numerado de `texto` ([1], [2], …).
- Unidad temática: una o más oraciones seguidas que tratan el mismo subtema, es decir, que responden a la misma pregunta sobre el asunto de `texto`.
- Frontera: empieza una unidad nueva cuando cambia la pregunta, aunque se sigan nombrando las mismas cosas. Un mismo lugar, objeto o persona puede aparecer en varias unidades. Un cambio de párrafo no es por sí solo una frontera.
- Tema: una frase breve que nombra la pregunta de la unidad.
- Cada oración va en una sola unidad, y las unidades siguen el orden de `texto`.

EJEMPLO 1
`texto`
<<<
[1] El horno principal de la panadería alcanza 250 °C en veinte minutos. [2] Su puerta de vidrio permite vigilar el dorado del pan. [3] Los clientes prefieren el pan integral. [4] Los sábados las ventas se duplican.
>>>
{"unidades": [
  {"tema": "el horno de la panadería", "desde": 1, "hasta": 2},
  {"tema": "la demanda de los clientes", "desde": 3, "hasta": 4}]}

EJEMPLO 2
`texto`
<<<
[1] El ferri sale del puerto a las 7. [2] El cruce dura cuarenta minutos.

[3] Con mal tiempo, el cruce puede tardar el doble. [4] La tripulación tiene seis personas.
>>>
{"unidades": [
  {"tema": "horario y duración del cruce", "desde": 1, "hasta": 3},
  {"tema": "la tripulación", "desde": 4, "hasta": 4}]}

EJEMPLO 3
`texto`
<<<
[1] La escuela rural tiene 60 alumnos. [2] Sus aulas se calientan con estufas de leña. [3] En invierno, la estufa del aula 2 falló dos veces. [4] Los alumnos de la escuela ganaron el concurso regional de lectura. [5] Su maestra preparó al equipo durante tres meses.
>>>
{"unidades": [
  {"tema": "la matrícula de la escuela", "desde": 1, "hasta": 1},
  {"tema": "la calefacción de las aulas", "desde": 2, "hasta": 3},
  {"tema": "el concurso de lectura", "desde": 4, "hasta": 5}]}

`texto`
<<<
{{TEXTO_NUMERADO}}
>>>
