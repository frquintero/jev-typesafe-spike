TAREA
Identifica los datos registrados en `texto`.

DEFINICIONES PARA CUMPLIR LA TAREA
- Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o signo de exclamación, hasta el siguiente. El título es una etiqueta: no registra datos.
- Caso: la unidad concreta, no una clase, que queda distinguida y acerca de la cual `texto` determina algo. Es una misma unidad en todo `texto`, aunque `texto` la nombre de varias maneras o con pronombres.
- Variable: el aspecto bajo el cual se considera un caso, que admite más de un valor y fija qué diferencias cuentan.
- Escala: el sistema al que pertenece todo valor: sus unidades, categorías, orden o precisión.
- Valor: la posición o elemento de una escala que se atribuye al caso bajo una variable.
- Condiciones constitutivas: lo que, además del caso y la variable, queda fijado en la determinación y cuyo cambio haría que se determinara otra cosa.
- Dato: la determinación de un caso bajo una variable y sus condiciones constitutivas, mediante un valor, registrada en una oración de `texto`.

REGLAS
1. Identifica primero los casos y unifícalos. Luego, para cada caso, las variables bajo las cuales `texto` lo determina. Luego, para cada variable, los datos.
2. Si algo es un aspecto de un caso, es variable de ese caso, no un caso propio.
3. Solo hay dato si puede formularse la pregunta <variable>(<caso>, <condiciones constitutivas>) = ? y `texto` da un valor que la cierra. Si falta el caso, la variable, el valor o su escala, no hay dato.
4. Registra lo que es, fue o será, no lo que debería ser.
5. Un plan o una intención es una determinación de quien lo tiene, no del caso sobre el que recae.
6. Cada determinación va una sola vez, bajo el caso del que se determina. Un caso sin datos no va en el JSON.
7. Solo lo que `texto` registra: no infieras ni completes valores ni condiciones.

ESTRUCTURA DEL JSON DE RESPUESTA (responde solo con este JSON)
{"casos": [
   {"caso": "<nombre más completo que le da `texto`>",
    "oraciones": [
      {"oracion": "<oración completa de `texto`, literal>",
       "datos": [
         {"dato": "<la determinación, fiel a `texto`>",
          "variable": "<el aspecto bajo el cual se determina el caso>",
          "valor": "<el valor, tal como `texto` lo expresa>",
          "escala": "<el sistema al que pertenece el valor>",
          "condiciones_constitutivas": ["<condición fijada por `texto`>"]}
       ]}
    ]}
 ]}

`texto`
<<<
{{TEXTO}}
>>>
