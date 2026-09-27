DEFINICIONES
- Unidad: una porción de `texto` que introduce, desarrolla o cierra un subtema o una idea específica.
- Dato: una unidad bajo una variable mediante un valor.
- Variable: el aspecto bajo el cual se considera una unidad. Admite más de una determinación y fija qué diferencias cuentan. Un aspecto que no admite diferencias no es una variable.
- Valor: una posición o un elemento admitido dentro de una escala, usado para expresar una determinación bajo una variable.
- Escala: el sistema de unidades, categorías, orden o precisión en que se expresan los valores de una variable.

TAREA
Encuentra los datos en `texto`.

PROCEDIMIENTO
Separa `texto` en unidades.
En cada unidad, determina si existen variables.
Por cada variable encontrada, determina si existen valores.
Por cada valor encontrado, determina su escala.

CONDICIONES
Es posible que `texto` solo tenga una unidad.
Es factible que una unidad no tenga variables.
Es factible que una unidad no contenga los valores de una variable.
Es factible que una unidad no contenga la escala de un valor.
Si una unidad no tiene variables, o sus variables no tienen valores, NO es un dato.

REPORTE
Reporta los DATOS que encuentres en la siguiente estructura (responde solo con este JSON):
{"unidades": [
   {"unidad": "<porción literal de `texto`>",
    "variables": [
       {"variable": "<aspecto>",
        "valores": [
           {"valor": "<tal como aparece en `texto`>",
            "escala": "<escala, o null si la unidad no la contiene>"}]}]}]}

`texto`
<<<
{{TEXTO}}
>>>
