DEFINICIONES
- Unidad textual: una porción de `texto` que introduce, desarrolla o cierra un subtema o una idea específica. Sirve únicamente para segmentar `texto`.
- Caso: lo concreto acerca de lo cual `texto` determina algo. Conserva su identidad aunque `texto` lo nombre de distintas maneras o con pronombres. Un nombre, número o código que sirve para distinguirlo forma parte del caso.
- Variable: el aspecto bajo el cual se considera un caso. Admite respuestas distintas que no se reducen a afirmar o negar lo que `texto` dice. Un aspecto que no admite diferencias no es una variable.
- Condiciones constitutivas: lo que, además del caso y la variable, fija la pregunta; si cambiara, la pregunta sería otra. Quién lo dice o cómo se obtuvo no es condición.
- Escala: el sistema al que pertenece un valor: unidades, categorías, orden, proporción, fechas u horas. Puede recuperarse de la variable y de la forma del valor aunque `texto` no la nombre.
- Valor: una posición o elemento de una escala que expresa una determinación bajo una variable.
- Dato: la determinación registrada en `texto` de un caso bajo una variable y sus condiciones constitutivas, mediante un valor.

TAREA
Encuentra los datos en `texto`.

PROCEDIMIENTO
1. Separa `texto` en unidades textuales.
2. En cada unidad, identifica los casos y unifica las expresiones que se refieren al mismo caso.
3. Para cada caso, identifica los aspectos que podrían ser variables.
4. Acepta una variable solo si admite respuestas distintas que no se reducen a afirmar o negar lo que `texto` dice.
5. Identifica las condiciones constitutivas.
6. Determina si `texto` da un valor que cierre la pregunta <variable>(<caso>, <condiciones>) = ?
7. Identifica la escala de ese valor.

REGLAS
- Cuando `texto` nombra algo y le atribuye un grado o una cualidad, la variable es ese grado o esa cualidad, no el nombre.
- Un valor no es otro caso. Si la respuesta es algo concreto (un lugar, un objeto, una persona), `texto` registra una relación entre casos, no un dato.
- Si un valor no pertenece a ninguna escala, no hay dato.
- Si falta caso, variable o valor, no hay dato.
- No infieras nada que `texto` no permita recuperar.
- Una misma determinación aparece una sola vez.

REPORTE
Reporta únicamente las unidades que contienen DATOS, con esta estructura (responde solo con este JSON):
{"unidades": [
   {"unidad": "<porción literal de `texto`>",
    "datos": [
       {"caso": "<caso>",
        "variable": "<aspecto>",
        "valor": "<tal como aparece en `texto`>",
        "escala": "<sistema al que pertenece el valor>",
        "condiciones_constitutivas": ["<condición fijada por `texto`>"]}]}]}

`texto`
<<<
{{TEXTO}}
>>>
