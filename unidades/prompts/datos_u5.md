TAREA
Encuentra los datos de `texto`, como en los ejemplos. Responde solo con el JSON.

EJEMPLO 1
`texto`
<<<
La parcela norte del viñedo rindió 4,2 toneladas de uva. La vendimia empezó a las 7 y terminó a las 15. La lluvia de la tarde fue ligera y el mosto salió de color rosado.
>>>
{"datos": [
  {"variable": "rendimiento de uva de la parcela norte del viñedo", "valor": "4,2", "unidad_de_medida": "toneladas"},
  {"variable": "hora de inicio de la vendimia", "valor": "7", "unidad_de_medida": "hora"},
  {"variable": "hora de fin de la vendimia", "valor": "15", "unidad_de_medida": "hora"},
  {"variable": "intensidad de la lluvia de la tarde", "valor": "ligera", "unidad_de_medida": null},
  {"variable": "color del mosto", "valor": "rosado", "unidad_de_medida": null}]}

EJEMPLO 2
`texto`
<<<
El antiguo muelle pesquero recibe los barcos de la cooperativa. Anoche descargaron allí un contenedor de 800 kg. La grúa del muelle funcionó sin interrupciones. Su operador trabajó tres turnos esta semana.
>>>
{"datos": [
  {"variable": "peso del contenedor descargado anoche en el antiguo muelle pesquero", "valor": "800", "unidad_de_medida": "kg"},
  {"variable": "número de turnos trabajados esta semana por el operador de la grúa del muelle", "valor": "tres", "unidad_de_medida": "unidad"}]}

EJEMPLO 3
`texto`
<<<
El sendero del cerro atraviesa un bosque de robles. Los guardabosques recomiendan llevar agua. Desde la cima se ve el lago.
>>>
{"datos": []}

`texto`
<<<
{{TEXTO}}
>>>
