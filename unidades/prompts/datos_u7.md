TAREA
Encuentra los datos de `texto`, según las definiciones y como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Dato: un valor que `texto` le atribuye a una variable.
- Variable: la magnitud o cualidad considerada, nombrada con su caso y sus circunstancias («peso del contenedor descargado anoche», no «peso»). Los nombres, números y códigos que identifican el caso van en la variable. Si `texto` no nombra el aspecto, la variable lo nombra (tamaño, tipo, grado).
- Valor: lo que toma la variable, copiado tal como aparece en `texto`, sin la unidad. Elige entre más alternativas que el sí y el no.
- Unidad de medida: la unidad del valor («kg», «hora», «%», «fracción»; «unidad» en los conteos). Es null si el valor es una cualidad.
- No son datos: lo que solo afirma o niega algo (abierto, certificado, sin interrupciones), las relaciones entre casos (recibe, atraviesa, anida en) y los adjetivos que forman parte del nombre de algo («antiguo muelle»).

EJEMPLO 1
`texto`
<<<
La parcela 3B del viñedo rindió 4,2 toneladas de uva. La vendimia empezó a las 7 de la mañana y terminó a las 3 de la tarde. A las 10, la humedad del suelo era de 18 %. La lluvia de la tarde fue ligera y el mosto salió de color rosado.
>>>
{"datos": [
  {"variable": "rendimiento de uva de la parcela 3B del viñedo", "valor": "4,2", "unidad_de_medida": "toneladas"},
  {"variable": "hora de inicio de la vendimia en la parcela 3B", "valor": "7 de la mañana", "unidad_de_medida": "hora"},
  {"variable": "hora de fin de la vendimia en la parcela 3B", "valor": "3 de la tarde", "unidad_de_medida": "hora"},
  {"variable": "humedad del suelo de la parcela 3B a las 10", "valor": "18", "unidad_de_medida": "%"},
  {"variable": "intensidad de la lluvia de la tarde", "valor": "ligera", "unidad_de_medida": null},
  {"variable": "color del mosto", "valor": "rosado", "unidad_de_medida": null}]}

EJEMPLO 2
`texto`
<<<
El café del lote 14 tiene acidez alta y aroma floral. Su grano es grande y el tueste es oscuro. El lote está certificado como orgánico. La catadora le dio 86 puntos.
>>>
{"datos": [
  {"variable": "acidez del café del lote 14", "valor": "alta", "unidad_de_medida": null},
  {"variable": "aroma del café del lote 14", "valor": "floral", "unidad_de_medida": null},
  {"variable": "tamaño del grano del café del lote 14", "valor": "grande", "unidad_de_medida": null},
  {"variable": "grado de tueste del café del lote 14", "valor": "oscuro", "unidad_de_medida": null},
  {"variable": "puntaje de catación del café del lote 14", "valor": "86", "unidad_de_medida": "puntos"}]}

EJEMPLO 3
`texto`
<<<
El antiguo muelle pesquero recibe los barcos de la cooperativa. Anoche descargaron allí un contenedor de 800 kg con la grúa G-4. La grúa funcionó sin interrupciones.
>>>
{"datos": [
  {"variable": "peso del contenedor descargado anoche en el antiguo muelle pesquero", "valor": "800", "unidad_de_medida": "kg"}]}

EJEMPLO 4
`texto`
<<<
El censo de aves del 12 de marzo contó 43 garzas en la laguna Negra; dos tercios eran juveniles. Las garzas anidan en los juncos de la orilla.
>>>
{"datos": [
  {"variable": "número de garzas contadas en la laguna Negra el 12 de marzo", "valor": "43", "unidad_de_medida": "unidad"},
  {"variable": "fracción de juveniles entre las garzas de la laguna Negra el 12 de marzo", "valor": "dos tercios", "unidad_de_medida": "fracción"}]}

EJEMPLO 5
`texto`
<<<
El sendero del cerro atraviesa un bosque de robles. El refugio de la cima estaba abierto. Los guardabosques recomiendan llevar agua.
>>>
{"datos": []}

`texto`
<<<
{{TEXTO}}
>>>
