TAREA
Encuentra los datos del `foco`, según las definiciones y como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas. Sirve para saber a qué se refiere cada expresión.
- Foco: las oraciones del `documento`, seguidas o separadas, de las que se extraen los datos. Los datos se toman únicamente del foco; lo que está fuera del foco no se reporta.
- Dato: un valor que el foco le atribuye a una variable.
- Variable: la magnitud o cualidad considerada, nombrada con su caso y sus circunstancias («peso del contenedor descargado anoche», no «peso»). Los nombres, números y códigos que identifican el caso van en la variable. Si el foco no nombra el aspecto, la variable lo nombra (tamaño, tipo, grado). La variable nombra las cosas completas aunque el foco diga «su», «este» o «esa»: su nombre está en el `documento`.
- Valor: lo que toma la variable, copiado tal como aparece en el foco, sin la unidad. Elige entre más alternativas que el sí y el no.
- Unidad de medida: la unidad del valor («kg», «hora», «%», «fracción»; «unidad» en los conteos). Es null si el valor es una cualidad.
- No son datos: lo que solo afirma o niega algo (abierto, certificado, sin interrupciones), las relaciones entre casos (recibe, atraviesa, anida en) y los adjetivos que forman parte del nombre de algo («antiguo muelle»).

EJEMPLO 1
Muestra mediciones con unidad (decimales, porcentaje, horas con su parte del día) y cualidades con null; la variable lleva el identificador del caso y sus circunstancias.
`documento`
<<<
[1] La parcela 3B del viñedo rindió 4,2 toneladas de uva. [2] La vendimia empezó a las 7 de la mañana y terminó a las 3 de la tarde. [3] A las 10, la humedad del suelo era de 18 %. [4] La lluvia de la tarde fue ligera y el mosto salió de color rosado.
>>>
`foco`: oraciones 1, 2, 3 y 4
{"datos": [
  {"variable": "rendimiento de uva de la parcela 3B del viñedo", "valor": "4,2", "unidad_de_medida": "toneladas"},
  {"variable": "hora de inicio de la vendimia en la parcela 3B", "valor": "7 de la mañana", "unidad_de_medida": "hora"},
  {"variable": "hora de fin de la vendimia en la parcela 3B", "valor": "3 de la tarde", "unidad_de_medida": "hora"},
  {"variable": "humedad del suelo de la parcela 3B a las 10", "valor": "18", "unidad_de_medida": "%"},
  {"variable": "intensidad de la lluvia de la tarde", "valor": "ligera", "unidad_de_medida": null},
  {"variable": "color del mosto", "valor": "rosado", "unidad_de_medida": null}]}

EJEMPLO 2
Muestra cualidades: si el foco no nombra el aspecto, la variable lo nombra; lo que solo afirma o niega (certificado) no es dato.
`documento`
<<<
[1] El café del lote 14 tiene acidez alta y aroma floral. [2] Su grano es grande y el tueste es oscuro. [3] El lote está certificado como orgánico. [4] La catadora le dio 86 puntos.
>>>
`foco`: oraciones 1, 2, 3 y 4
{"datos": [
  {"variable": "acidez del café del lote 14", "valor": "alta", "unidad_de_medida": null},
  {"variable": "aroma del café del lote 14", "valor": "floral", "unidad_de_medida": null},
  {"variable": "tamaño del grano del café del lote 14", "valor": "grande", "unidad_de_medida": null},
  {"variable": "grado de tueste del café del lote 14", "valor": "oscuro", "unidad_de_medida": null},
  {"variable": "puntaje de catación del café del lote 14", "valor": "86", "unidad_de_medida": "puntos"}]}

EJEMPLO 3
Muestra que un adjetivo del nombre y una relación entre casos no son datos, y que una cantidad dentro del nombre sí lo es.
`documento`
<<<
[1] El antiguo muelle pesquero recibe los barcos de la cooperativa. [2] Anoche descargaron allí un contenedor de 800 kg con la grúa G-4. [3] La grúa funcionó sin interrupciones.
>>>
`foco`: oraciones 1, 2 y 3
{"datos": [
  {"variable": "peso del contenedor descargado anoche en el antiguo muelle pesquero", "valor": "800", "unidad_de_medida": "kg"}]}

EJEMPLO 4
Muestra un conteo con «unidad» y una fracción, con la fecha dentro de la variable; una relación entre casos no es dato.
`documento`
<<<
[1] El censo de aves del 12 de marzo contó 43 garzas en la laguna Negra; dos tercios eran juveniles. [2] Las garzas anidan en los juncos de la orilla.
>>>
`foco`: oraciones 1 y 2
{"datos": [
  {"variable": "número de garzas contadas en la laguna Negra el 12 de marzo", "valor": "43", "unidad_de_medida": "unidad"},
  {"variable": "fracción de juveniles entre las garzas de la laguna Negra el 12 de marzo", "valor": "dos tercios", "unidad_de_medida": "fracción"}]}

EJEMPLO 5
Muestra un foco sin datos: hechos, relaciones, recomendaciones y un binario.
`documento`
<<<
[1] El sendero del cerro atraviesa un bosque de robles. [2] El refugio de la cima estaba abierto. [3] Los guardabosques recomiendan llevar agua.
>>>
`foco`: oraciones 1, 2 y 3
{"datos": []}

EJEMPLO 6
Muestra un foco con oraciones separadas: el `documento` sirve para completar las variables («Su», «Este manantial»), pero los datos se toman únicamente del foco; el caudal está en la oración 2, fuera del foco, y no se reporta.
`documento`
<<<
[1] El manantial Las Palmas nace en la ladera norte. [2] El laboratorio midió su caudal: 12 litros por segundo. [3] Su agua salió a 19 °C. [4] Este manantial abastece a tres veredas.
>>>
`foco`: oraciones 1, 3 y 4
{"datos": [
  {"variable": "temperatura del agua del manantial Las Palmas", "valor": "19", "unidad_de_medida": "°C"},
  {"variable": "número de veredas abastecidas por el manantial Las Palmas", "valor": "tres", "unidad_de_medida": "unidad"}]}

`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
