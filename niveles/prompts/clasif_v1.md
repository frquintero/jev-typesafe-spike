Extrae los datos y las afirmaciones de `texto`.

Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título es una etiqueta: no da datos ni afirmaciones.

Dato: la atribución de un valor a un caso concreto (no a una clase) bajo una variable, tal como `texto` la deja registrada. Registra lo que es o lo que será, no lo que debería ser.

Cada dato es un objeto:
{"oracion": "<oración completa de `texto` de donde sale el dato, literal>",
 "dato": "<la determinación enunciada>",
 "caso": "<aquello concreto de lo que se determina algo>",
 "variable": "<aspecto bajo el cual se determina el caso>",
 "valor": "<lo que se atribuye al caso>",
 "escala": "<lo que, si cambiara, cambiaría solo la forma de expresar el valor; vacío si no está>"}

Afirmación: un enunciado mediante el cual se asegura o sostiene algo.

Cada afirmación es un objeto:
{"oracion": "<oración completa de `texto` de donde sale la afirmación, literal>",
 "afirmacion": "<lo que se asegura o sostiene, enunciado>"}

Una oración puede tener cero, uno o varios datos, y cero, una o varias afirmaciones. Solo lo que dice `texto`.

`texto`
<<<
{{TEXTO}}
>>>

Responde solo JSON: {"datos": [...], "afirmaciones": [...]}
