Extrae los datos de `texto`.

Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título es una etiqueta: no da datos.

Dato: la atribución de un valor a un caso concreto (no a una clase) bajo una variable, tal como `texto` la deja registrada. Registra lo que es o lo que será, no lo que debería ser.

De una oración pueden salir varios casos, y de cada caso varios datos. Cada oración con datos es un objeto:
{"oracion": "<oración completa de `texto`, literal>",
 "casos": [
   {"caso": "<aquello concreto de lo que se determina algo>",
    "datos": [
      {"dato": "<la determinación enunciada>",
       "variable": "<aspecto bajo el cual se determina el caso>",
       "valor": "<lo que se atribuye al caso>",
       "escala": "<lo que, si cambiara, cambiaría solo la forma de expresar el valor; vacío si no está>"}
    ]}
 ]}

Solo lo que dice `texto`.

`texto`
<<<
{{TEXTO}}
>>>

Responde solo JSON: {"oraciones": [...]}
