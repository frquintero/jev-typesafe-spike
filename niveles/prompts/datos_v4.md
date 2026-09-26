TAREA
Identifica los casos de `texto` y, para cada caso, las oraciones de `texto` en que aparece y los datos que cada una de ellas le atribuye.

DEFINICIONES PARA CUMPLIR LA TAREA
- Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título es una etiqueta: no da datos.
- Caso: lo que queda fijado; aquello concreto (no una clase) de lo que se determina algo. Es una misma unidad en todo `texto`, aunque `texto` la nombre de varias maneras o con pronombres.
- Variable: el aspecto bajo el cual se determina el caso. Si algo es un aspecto de un caso, es variable de ese caso, no un caso propio.
- Dato: la atribución de un valor a un caso bajo una variable, tal como `texto` la deja registrada. Registra lo que es o lo que será, no lo que debería ser.

ESTRUCTURA DEL JSON DE RESPUESTA (responde solo con este JSON)
{"casos": [
   {"caso": "<nombre del caso, el más completo que le da `texto`>",
    "oraciones": [
      {"oracion": "<oración completa de `texto`, literal>",
       "datos": [
         {"dato": "<la determinación enunciada>",
          "variable": "<el aspecto bajo el cual se determina el caso>",
          "valor": "<lo que se atribuye al caso, sin la escala>",
          "escala": "<lo que, si cambiara, cambiaría solo la forma de expresar el valor, no el valor mismo; vacío si no está>"}
       ]}
    ]}
 ]}

`texto`
<<<
{{TEXTO}}
>>>
