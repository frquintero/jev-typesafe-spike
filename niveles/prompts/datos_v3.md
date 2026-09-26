Extrae los datos de `texto`.

Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título es una etiqueta: no da datos.

Caso: lo que queda fijado; aquello concreto (no una clase) de lo que se determina algo. Es una misma unidad en todo `texto`, aunque `texto` la nombre de varias maneras o con pronombres.

Variable: el aspecto bajo el cual se determina el caso.

Dato: la atribución de un valor a un caso bajo una variable, tal como `texto` la deja registrada. Registra lo que es o lo que será, no lo que debería ser.

Primero identifica los casos de todo `texto` y unifícalos. Después, oración por oración, registra los datos de cada caso.

{"casos": [
   {"caso": "<nombre del caso, el más completo que le da `texto`>",
    "menciones": ["<cada forma literal en que `texto` lo nombra, incluidos pronombres>"]}
 ],
 "oraciones": [
   {"oracion": "<oración completa de `texto`, literal>",
    "casos": [
      {"caso": "<nombre del caso, tal como está en la lista de casos>",
       "datos": [
         {"dato": "<la determinación enunciada>",
          "variable": "<el aspecto bajo el cual se determina el caso>",
          "valor": "<lo que se atribuye al caso, sin la escala>",
          "escala": "<lo que, si cambiara, cambiaría solo la forma de expresar el valor; vacío si no está>"}
       ]}
    ]}
 ]}

Solo lo que dice `texto`. Solo las oraciones que tienen datos.

`texto`
<<<
{{TEXTO}}
>>>

Responde solo JSON con esa forma.
