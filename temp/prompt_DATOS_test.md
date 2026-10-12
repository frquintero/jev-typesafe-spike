TAREA
Extraer los datos de CADA unidad temática de la lista.

UN DATO es lo que la UNIDAD TEMÁTICA establece acerca de algo bajo un aspecto.

REGLAS
1. Extrae solo del contenido de la unidad: la unidad es el alcance.
2. No inventes: registra lo que el texto dice, sin agregar saber externo.
3. Una salida por unidad, en el mismo orden de la lista, con su `caso`; no mezcles datos de una unidad en otra.

EJEMPLO.

Para la siguiente lista de unidades temáticas:
[{"caso": "la aparición de la vida y los primeros microorganismos en el océano", "contenido": "La vida apareció en el océano hace unos tres mil quinientos millones de años. Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado."},
 {"caso": "la extensión, la profundidad y la temperatura del océano", "contenido": "El agua cubre el setenta y uno por ciento de la superficie del planeta y su profundidad media es de tres mil setecientos metros. En el fondo abisal la temperatura se mantiene cerca de los dos grados centígrados."},
 {"caso": "la explosión del Cámbrico y la evolución de los animales hasta la conquista de la tierra firme", "contenido": "Hace quinientos treinta millones de años ocurrió la explosión del Cámbrico: en veinte millones de años aparecieron la mayoría de los grandes grupos de animales que conocemos. Los primeros peces nadaban en el océano hace unos quinientos millones de años. Hace trescientos setenta y cinco millones de años, un linaje de peces de aletas carnosas salió del agua y dio origen a los anfibios, que todavía dependían del agua para reproducirse. La conquista de la tierra firme fue lenta: los primeros reptiles, con huevos de cáscara dura, aparecieron unos trescientos veinte millones de años después de aquella salida."},
 {"caso": "el regreso al mar de los antepasados de las ballenas", "contenido": "Algunos linajes hicieron el camino de vuelta. Los antepasados de las ballenas caminaban sobre la tierra hace cincuenta millones de años y volvieron al mar en unos diez millones de años."},
 {"caso": "el tamaño, el buceo y la alimentación de la ballena azul", "contenido": "La ballena azul mide hasta treinta metros y pesa ciento cincuenta toneladas: es el animal más grande que ha existido. Puede bucear quinientos metros y aguantar la respiración cuarenta minutos. Sus crías beben doscientos litros de leche al día."},
 {"caso": "el calentamiento y la acidificación actuales del mar y su efecto en los corales", "contenido": "Hoy el mar cambia más rápido que en cualquier otro momento de esa historia. Ha absorbido el noventa por ciento del calor extra que retuvo la atmósfera. Desde la era preindustrial, la acidez del agua superficial aumentó un treinta por ciento, y eso altera a los corales, que crecen apenas un centímetro al año."},
 {"caso": "la extensión y la biodiversidad de los arrecifes", "contenido": "Los arrecifes ocupan menos del uno por ciento del fondo marino y albergan cerca de la cuarta parte de las especies marinas."},
 {"caso": "la ampliación de una reserva del Pacífico", "contenido": "Una reserva del Pacífico pasó de mil quinientas a doce mil hectáreas en dos años."}]

El json de salida con los datos es el siguiente:

{"unidades": [
  {"n": 1,
   "caso": "la aparición de la vida y los primeros microorganismos en el océano",
   "datos": [
     {"aspecto": "lugar de aparición de la vida",
      "valor": "el océano",
      "unidad_valor": null},
     {"aspecto": "fecha de aparición de la vida",
      "valor": "hace unos tres mil quinientos millones",
      "unidad_valor": "años"},
     {"aspecto": "naturaleza de los primeros seres vivos",
      "valor": "microorganismos",
      "unidad_valor": null},
     {"aspecto": "tamaño de los primeros seres vivos",
      "valor": "unas pocas",
      "unidad_valor": "micras"},
     {"aspecto": "único lugar habitado",
      "valor": "el mar",
      "unidad_valor": null},
     {"aspecto": "duración del mar como único lugar habitado",
      "valor": "casi tres mil millones",
      "unidad_valor": "años"}
   ]},
  {"n": 2,
   "caso": "la extensión, la profundidad y la temperatura del océano",
   "datos": [
     {"aspecto": "superficie del planeta cubierta por el agua",
      "valor": "setenta y uno",
      "unidad_valor": "por ciento"},
     {"aspecto": "profundidad media del agua",
      "valor": "tres mil setecientos",
      "unidad_valor": "metros"},
     {"aspecto": "temperatura en el fondo abisal",
      "valor": "se mantiene cerca de los dos",
      "unidad_valor": "grados centígrados"}
   ]},
  {"n": 3,
   "caso": "la explosión del Cámbrico y la evolución de los animales hasta la conquista de la tierra firme",
   "datos": [
     {"aspecto": "fecha de la explosión del Cámbrico",
      "valor": "hace quinientos treinta millones",
      "unidad_valor": "años"},
     {"aspecto": "lapso de la explosión del Cámbrico",
      "valor": "veinte millones",
      "unidad_valor": "años"},
     {"aspecto": "lo que apareció en la explosión del Cámbrico",
      "valor": "la mayoría de los grandes grupos de animales que conocemos",
      "unidad_valor": null},
     {"aspecto": "fecha en que nadaban los primeros peces en el océano",
      "valor": "hace unos quinientos millones",
      "unidad_valor": "años"},
     {"aspecto": "fecha de la salida del agua de un linaje de peces",
      "valor": "hace trescientos setenta y cinco millones",
      "unidad_valor": "años"},
     {"aspecto": "linaje que salió del agua",
      "valor": "un linaje de peces de aletas carnosas",
      "unidad_valor": null},
     {"aspecto": "descendencia del linaje que salió del agua",
      "valor": "los anfibios",
      "unidad_valor": null},
     {"aspecto": "dependencia de los anfibios",
      "valor": "todavía dependían del agua para reproducirse",
      "unidad_valor": null},
     {"aspecto": "ritmo de la conquista de la tierra firme",
      "valor": "lenta",
      "unidad_valor": null},
     {"aspecto": "rasgo de los primeros reptiles",
      "valor": "huevos de cáscara dura",
      "unidad_valor": null},
     {"aspecto": "tiempo entre la salida del agua y la aparición de los primeros reptiles",
      "valor": "unos trescientos veinte millones",
      "unidad_valor": "años"}
   ]},
  {"n": 4,
   "caso": "el regreso al mar de los antepasados de las ballenas",
   "datos": [
     {"aspecto": "linajes que hicieron el camino de vuelta",
      "valor": "algunos",
      "unidad_valor": null},
     {"aspecto": "fecha en que los antepasados de las ballenas caminaban sobre la tierra",
      "valor": "hace cincuenta millones",
      "unidad_valor": "años"},
     {"aspecto": "medio al que volvieron los antepasados de las ballenas",
      "valor": "el mar",
      "unidad_valor": null},
     {"aspecto": "duración del regreso al mar de los antepasados de las ballenas",
      "valor": "unos diez millones",
      "unidad_valor": "años"}
   ]},
  {"n": 5,
   "caso": "el tamaño, el buceo y la alimentación de la ballena azul",
   "datos": [
     {"aspecto": "longitud de la ballena azul",
      "valor": "hasta treinta",
      "unidad_valor": "metros"},
     {"aspecto": "peso de la ballena azul",
      "valor": "ciento cincuenta",
      "unidad_valor": "toneladas"},
     {"aspecto": "tamaño de la ballena azul frente a otros animales",
      "valor": "el animal más grande que ha existido",
      "unidad_valor": null},
     {"aspecto": "profundidad de buceo de la ballena azul",
      "valor": "quinientos",
      "unidad_valor": "metros"},
     {"aspecto": "tiempo que la ballena azul aguanta la respiración",
      "valor": "cuarenta",
      "unidad_valor": "minutos"},
     {"aspecto": "leche que beben las crías de la ballena azul",
      "valor": "doscientos",
      "unidad_valor": "litros al día"}
   ]},
  {"n": 6,
   "caso": "el calentamiento y la acidificación actuales del mar y su efecto en los corales",
   "datos": [
     {"aspecto": "ritmo actual de cambio del mar",
      "valor": "más rápido que en cualquier otro momento de esa historia",
      "unidad_valor": null},
     {"aspecto": "parte del calor extra retenido por la atmósfera que ha absorbido el mar",
      "valor": "noventa",
      "unidad_valor": "por ciento"},
     {"aspecto": "aumento de la acidez del agua superficial desde la era preindustrial",
      "valor": "treinta",
      "unidad_valor": "por ciento"},
     {"aspecto": "efecto del aumento de la acidez",
      "valor": "altera a los corales",
      "unidad_valor": null},
     {"aspecto": "crecimiento de los corales",
      "valor": "apenas un",
      "unidad_valor": "centímetro al año"}
   ]},
  {"n": 7,
   "caso": "la extensión y la biodiversidad de los arrecifes",
   "datos": [
     {"aspecto": "parte del fondo marino que ocupan los arrecifes",
      "valor": "menos del uno",
      "unidad_valor": "por ciento"},
     {"aspecto": "especies marinas que albergan los arrecifes",
      "valor": "cerca de la cuarta parte de las especies marinas",
      "unidad_valor": null}
   ]},
  {"n": 8,
   "caso": "la ampliación de una reserva del Pacífico",
   "datos": [
     {"aspecto": "ubicación de la reserva",
      "valor": "el Pacífico",
      "unidad_valor": null},
     {"aspecto": "superficie inicial de la reserva",
      "valor": "mil quinientas",
      "unidad_valor": "hectáreas"},
     {"aspecto": "superficie final de la reserva",
      "valor": "doce mil",
      "unidad_valor": "hectáreas"},
     {"aspecto": "plazo de la ampliación de la reserva",
      "valor": "dos",
      "unidad_valor": "años"}
   ]}]}

UNIDADES
{{UNIDADES}}

Convenciones aplicadas:

Las fechas «hace…»: el «hace» va en el valor y «años» en la unidad. Así no se confunde una fecha con una duración: «hace cincuenta millones» frente a «unos diez millones».
Los matices del texto se quedan en el valor: «unos», «casi», «cerca de», «hasta», «menos del», «apenas» y «se mantiene». Son condiciones de lo que el texto establece, no adornos.

FORMATO DE RESPUESTA


{"unidades": [
  {"n": <la posición de la unidad en la lista>,
   "caso": "<el caso de la unidad>",
   "datos": [
     {"aspecto": "<bajo qué se considera>",
      "valor": "<lo que se establece>",
      "unidad_valor": la unidad del valor («kilómetros», «°C»), o null.}]}]}
