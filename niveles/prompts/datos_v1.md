Extrae los datos de `texto`.

Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título cuenta como una oración.

Dato: la atribución de un valor a un caso bajo una variable, tal como `texto` la deja registrada.

Cada dato es un objeto:
{"oracion": "<oración completa de `texto` de donde sale el dato, literal>",
 "dato": "<la determinación enunciada>",
 "caso": "<aquello de lo que se determina algo>",
 "variable": "<aspecto bajo el cual se determina el caso>",
 "valor": "<lo que se atribuye al caso>",
 "escala": "<lo que, si cambiara, cambiaría solo la forma de expresar el valor; vacío si no está>"}

Una oración puede tener cero, uno o varios datos. Solo lo que dice `texto`.

`texto`
<<<
{{TEXTO}}
>>>

Responde solo JSON: {"datos": [...]}
