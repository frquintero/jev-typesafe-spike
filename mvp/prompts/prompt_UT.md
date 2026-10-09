[SISTEMA]
TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y el ejemplo.
Responde solo con el JSON.
La forma es el contrato: no agregues claves fuera de las que define `SALIDA`.

DEFINICIONES
- Oración: el texto que va de un punto, signo de interrogación o signo de exclamación al siguiente. En `texto` va numerada ([1], [2], …).
- Subtema: un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas.
- Desarrollo: una oración desarrolla un subtema si lo detalla, lo explica, lo continúa, lo contradice o saca su consecuencia. Si abre un asunto que no depende de ninguno anterior, empieza un subtema nuevo.
- Nombrar el mismo lugar, objeto o persona no basta para unir oraciones: lo que las une es el asunto. Un cambio de párrafo no separa por sí solo un subtema.
- Nombre del subtema: una frase breve que dice qué se dice de las cosas, no solo cuáles son («el tamaño de la tripulación», no «la tripulación»).
- Cada oración va en un solo subtema.

EJEMPLO 1

Es el texto completo de un documento. Va numerado y debajo está la respuesta.

`texto`
<<<
[1] La vida apareció en el océano hace unos tres mil quinientos millones de años. [2] El agua cubre el setenta y uno por ciento de la superficie del planeta y su profundidad media es de tres mil setecientos metros. [3] En el fondo abisal la temperatura se mantiene cerca de los dos grados centígrados. [4] Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado.

[5] Hace quinientos treinta millones de años ocurrió la explosión del Cámbrico: en veinte millones de años aparecieron la mayoría de los grandes grupos de animales que conocemos. [6] Los primeros peces nadaban en el océano hace unos quinientos millones de años. [7] Hace trescientos setenta y cinco millones de años, un linaje de peces de aletas carnosas salió del agua y dio origen a los anfibios, que todavía dependían del agua para reproducirse. [8] La conquista de la tierra firme fue lenta: los primeros reptiles, con huevos de cáscara dura, aparecieron unos trescientos veinte millones de años después de aquella salida.

[9] Algunos linajes hicieron el camino de vuelta. [10] Los antepasados de las ballenas caminaban sobre la tierra hace cincuenta millones de años y volvieron al mar en unos diez millones de años. [11] La ballena azul mide hasta treinta metros y pesa ciento cincuenta toneladas: es el animal más grande que ha existido. [12] Puede bucear quinientos metros y aguantar la respiración cuarenta minutos. [13] Sus crías beben doscientos litros de leche al día.

[14] Hoy el mar cambia más rápido que en cualquier otro momento de esa historia. [15] Ha absorbido el noventa por ciento del calor extra que retuvo la atmósfera. [16] Desde la era preindustrial, la acidez del agua superficial aumentó un treinta por ciento, y eso altera a los corales, que crecen apenas un centímetro al año. [17] Los arrecifes ocupan menos del uno por ciento del fondo marino y albergan cerca de la cuarta parte de las especies marinas. [18] Una reserva del Pacífico pasó de mil quinientas a doce mil hectáreas en dos años.
>>>
{"subtemas": [
  {"subtema": "el origen de la vida en el océano y los primeros seres vivos", "oraciones": [1, 4]},
  {"subtema": "la extensión, la profundidad y la temperatura del océano", "oraciones": [2, 3]},
  {"subtema": "la evolución de los animales desde la explosión del Cámbrico hasta la conquista de la tierra firme", "oraciones": [5, 6, 7, 8]},
  {"subtema": "el regreso de algunos linajes al mar, como los antepasados de las ballenas", "oraciones": [9, 10]},
  {"subtema": "el tamaño, el buceo y la alimentación de las crías de la ballena azul", "oraciones": [11, 12, 13]},
  {"subtema": "el cambio actual del mar: el calor que absorbe y la acidificación que afecta a los corales", "oraciones": [14, 15, 16]},
  {"subtema": "la extensión y la diversidad de los arrecifes", "oraciones": [17]},
  {"subtema": "la ampliación de una reserva marina del Pacífico", "oraciones": [18]}]}

REFERENCIAS EXTERNAS

Una referencia es externa al subtema cuando necesita una expresión de otra
oración del documento que quedó en otro subtema para identificar de quién
o de qué se habla.

EJEMPLO 2
La apertura y el horario son asuntos distintos sobre la misma biblioteca.
El posesivo se resuelve citando el antecedente, sin cambiar los grupos.
La referencia ambigua permanece abierta.

Texto:
[1] La biblioteca del barrio Los Olmos abrió en 1998.
[2] Su horario de atención termina a las seis.
[3] Clara habló con Julia después de que ella regresara.

{"subtemas": [
  {"subtema": "la apertura de la biblioteca del barrio Los Olmos", "oraciones": [1]},
  {"subtema": "el horario de atención de la biblioteca del barrio Los Olmos", "oraciones": [2]},
  {"subtema": "la conversación de Clara y Julia después de un regreso", "oraciones": [3]}]}

EJEMPLO 3
La aclaración identifica solo la parte que depende del contexto: el archivo, no
el director. «Sus observaciones» se entiende dentro del propio grupo y no se
registra.

Texto:
[1] El archivo municipal conserva doce mil expedientes.
[2] Una comisión examinó algunos expedientes.
[3] El director del archivo recibió sus observaciones.

{"subtemas": [
  {"subtema": "los expedientes que conserva el archivo municipal", "oraciones": [1]},
  {"subtema": "el examen de algunos expedientes por una comisión y las observaciones que recibió el director del archivo", "oraciones": [2, 3]}]}

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
