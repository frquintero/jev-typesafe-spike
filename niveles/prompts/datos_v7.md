TAREA
Identifica los datos registrados en `texto`.

DEFINICIONES PARA CUMPLIR LA TAREA
- Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o signo de exclamación, hasta el siguiente. El título es una etiqueta: no registra datos.
- Caso: la unidad concreta, no una clase, que queda distinguida y acerca de la cual `texto` determina algo. Es una misma unidad en todo `texto`, aunque `texto` la nombre de varias maneras o con pronombres.
- Variable: el aspecto bajo el cual se considera un caso, que admite más de un valor y fija qué diferencias cuentan.
- Escala: el sistema de representación bajo el cual puede expresarse una variable. Incluye, según el caso, unidades (°C, kg, metros), categorías (rojo, azul, verde), orden (bajo, medio, alto), precisión (21 °C, 21,4 °C, 21,37 °C) y reglas de conversión (de °C a °F, de metros a centímetros). La escala establece de qué manera se expresan los posibles valores de una variable.
- Valor: el nombre o expresión de una posición o elemento admitido dentro de una escala, utilizado para expresar una determinación bajo una variable. Puede ser una cantidad (21,4 °C, 70 kg), una categoría (rojo, casado), un nivel ordenado (bajo, medio, alto), una fecha (25 de septiembre de 2026) o cualquier otra expresión permitida por la escala de esa variable.
- Condiciones constitutivas: lo que, además del caso y la variable, fija la pregunta; si cambiara, la pregunta sería otra. No es de dónde proviene el valor.
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
