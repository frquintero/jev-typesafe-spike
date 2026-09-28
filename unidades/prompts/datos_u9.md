TAREA
Extrae los datos del `foco` según las definiciones, como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas.
- Foco: conjunto de oraciones del documento de las que se extraen los datos. El resto del documento solo sirve para saber a qué se refiere cada expresión del foco.
- Variable: aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor. Se nombra junto con aquello a lo que pertenece y sus circunstancias.
- Valor: lo que la variable toma en el foco: una cantidad (medida, conteo, fracción, hora) o una cualidad (alta, floral, rosado). Una cantidad vaga o aproximada conserva su cuantificador (unos 60, pocas).
- Unidad de medida: la unidad en que se expresa un número; null si el valor no lleva número (alta, rosado, pocas).
- Dato: una variable con su valor y su unidad de medida.

NO SON DATOS
- Lo que solo afirma o niega algo: su valor sería sí o no (abierto, vendido, sin interrupciones).
- Las relaciones entre cosas (recibe, atraviesa, anida en).
- Los adjetivos que forman parte del nombre de algo (antiguo muelle).
- Los enunciados genéricos: dicen cómo es una clase o qué suele pasar, no el valor que tomó algo individual (en verano, los arroyos se secan en pocos días).

EJEMPLO 1
Muestra cantidades con unidad (decimales, porcentaje, horas con su parte del día) y cualidades con null; cada variable se nombra con aquello a lo que pertenece y sus circunstancias.
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
Muestra cualidades: la variable nombra el aspecto aunque el foco no lo diga (tamaño, grado); «vendido» solo afirma y no es dato.
`documento`
<<<
[1] El café del lote 14 tiene acidez alta y aroma floral. [2] Su grano es grande y el tueste es oscuro. [3] El lote ya está vendido. [4] La catadora le dio 86 puntos.
>>>
`foco`: oraciones 1, 2, 3 y 4
{"datos": [
  {"variable": "acidez del café del lote 14", "valor": "alta", "unidad_de_medida": null},
  {"variable": "aroma del café del lote 14", "valor": "floral", "unidad_de_medida": null},
  {"variable": "tamaño del grano del café del lote 14", "valor": "grande", "unidad_de_medida": null},
  {"variable": "grado de tueste del café del lote 14", "valor": "oscuro", "unidad_de_medida": null},
  {"variable": "puntaje de catación del café del lote 14", "valor": "86", "unidad_de_medida": "puntos"}]}

EJEMPLO 3
Muestra que «antiguo» y «recibe» no son datos y que los 800 kg dentro del nombre sí; «sin interrupciones» solo afirma.
`documento`
<<<
[1] El antiguo muelle pesquero recibe los barcos de la cooperativa. [2] Anoche descargaron allí un contenedor de 800 kg con la grúa G-4. [3] La grúa funcionó sin interrupciones.
>>>
`foco`: oraciones 1, 2 y 3
{"datos": [
  {"variable": "peso del contenedor descargado anoche en el antiguo muelle pesquero", "valor": "800", "unidad_de_medida": "kg"}]}

EJEMPLO 4
Muestra conteos y una fracción, con la fecha dentro de la variable; «unos 60» conserva su cuantificador y lleva unidad; «pocas» no lleva número y su unidad es null; «anidan en» es una relación.
`documento`
<<<
[1] El censo de aves del 12 de marzo contó 43 garzas en la laguna Negra; dos tercios eran juveniles. [2] Ese día también se vieron unos 60 patos y pocas cigüeñas. [3] Las garzas anidan en los juncos de la orilla.
>>>
`foco`: oraciones 1, 2 y 3
{"datos": [
  {"variable": "número de garzas contadas en la laguna Negra el 12 de marzo", "valor": "43", "unidad_de_medida": "unidad"},
  {"variable": "fracción de juveniles entre las garzas de la laguna Negra el 12 de marzo", "valor": "dos tercios", "unidad_de_medida": "fracción"},
  {"variable": "número de patos vistos en la laguna Negra el 12 de marzo", "valor": "unos 60", "unidad_de_medida": "unidad"},
  {"variable": "número de cigüeñas vistas en la laguna Negra el 12 de marzo", "valor": "pocas", "unidad_de_medida": null}]}

EJEMPLO 5
Muestra un foco sin datos: una relación, un binario, una recomendación y un enunciado genérico («pocos días» habla de los arroyos en general, no de algo individual).
`documento`
<<<
[1] El sendero del cerro atraviesa un bosque de robles. [2] El refugio de la cima estaba abierto. [3] Los guardabosques recomiendan llevar agua. [4] En verano, los arroyos de la zona se secan en pocos días.
>>>
`foco`: oraciones 1, 2, 3 y 4
{"datos": []}

EJEMPLO 6
Muestra un foco con oraciones separadas: el resto del documento completa las variables («Su», «Este manantial»); el caudal está en la oración 2, fuera del foco, y no se reporta.
`documento`
<<<
[1] El manantial Las Palmas nace en la ladera norte. [2] El laboratorio midió su caudal: 12 litros por segundo. [3] Su agua salió a 19 °C. [4] Este manantial abastece a tres veredas.
>>>
`foco`: oraciones 1, 3 y 4
{"datos": [
  {"variable": "temperatura del agua del manantial Las Palmas", "valor": "19", "unidad_de_medida": "°C"},
  {"variable": "número de veredas abastecidas por el manantial Las Palmas", "valor": "tres", "unidad_de_medida": "unidad"}]}

ENTRADA
`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
