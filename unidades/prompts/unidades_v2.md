TAREA
Agrupa las oraciones de `texto` en unidades temáticas. Hazlo en este orden:

1. Casos. Identifica los casos de `texto`: las unidades concretas, no clases, acerca de las cuales `texto` dice algo. Un mismo caso puede aparecer nombrado de varias maneras; trátalo como uno solo.

2. Núcleos y satélites. Elige como núcleos los casos de los que trata cada tramo de `texto`. Los demás casos son satélites del núcleo con el que `texto` los relaciona. Un caso puede ser satélite de más de un núcleo.

3. Unidades temáticas. Forma una unidad temática por núcleo y asígnale las oraciones que se refieren a él o a sus satélites. Oración es lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o signo de exclamación, hasta el siguiente; el título no es una oración. Cada oración va en una sola unidad temática. Una unidad temática puede reunir oraciones que no están seguidas.

ESTRUCTURA DEL JSON DE RESPUESTA (responde solo con este JSON)
{"unidades": [
   {"nucleo": "<nombre del caso, sin artículos ni posesivos>",
    "satelites": ["<nombre del caso, sin artículos ni posesivos>"],
    "oraciones": ["<oración literal>"]}]}

`texto`
<<<
{{TEXTO}}
>>>
