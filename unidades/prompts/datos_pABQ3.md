TAREA
Extrae los datos del `foco`. Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas.
- Unidad temática: un asunto y su desarrollo, en una o varias oraciones del documento, seguidas o separadas.
- Foco: conjunto de oraciones que forman una unidad temática, de las que se extraen los datos.
- Variable: aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor. El nombre de la variable dice el aspecto, aquello a lo que pertenece y sus circunstancias. Si el foco dice «este», «su» o «estos», el nombre usa aquello a lo que remiten en el documento.
- Valor: lo que la variable toma en el foco: una cantidad (medida, conteo, fracción, fecha, hora) o una cualidad (alta, floral, rosado). Los valores conservan los cuantificadores y matices del texto (pocos, muchos, unos, casi; «metales como…»).
- Unidad de medida: en las cantidades, la unidad en que se expresan, lleven cifra o no (120 → unidad; millones → unidad; décadas → década); en las cualidades, null.
- Dato: una variable con su valor y su unidad de medida. Se obtiene al responder: «¿qué valor toma esta variable que sale de este foco?».
- Formato: {"datos": [{"variable": "...", "valor": "...", "unidad_de_medida": "..." o null}]}

NO SON DATOS
- Lo que solo afirma o niega algo: su valor sería sí o no (abierto, vendido, sin interrupciones).
- Las relaciones entre cosas (recibe, atraviesa, anida en), también cuando se nombran con un sustantivo (origen, fuente, método, contenido).
- Los adjetivos que solo identifican o clasifican algo (antiguo muelle, piscina municipal, riesgos ambientales).
- Los enunciados genéricos: dicen cómo es una clase o qué suele pasar, no el valor que tomó algo individual (en verano, los arroyos se secan en pocos días).
- Lo que el texto no presenta como hecho: creencias, hipótesis, posibilidades (se creía que, podría, pudo).

EJEMPLOS DE DATOS

EJEMPLO 1
Valores numéricos con su unidad: una medida, un conteo («unidad») y un porcentaje; la variable dice de qué es cada valor.
`documento`
<<<
[1] La panadería La Espiga horneó 120 panes. [2] Cada pan pesa 250 gramos, y el 30 % de los panes lleva semillas.
>>>
`foco`: oraciones 1 y 2
{"datos": [
  {"variable": "número de panes horneados por la panadería La Espiga", "valor": "120", "unidad_de_medida": "unidad"},
  {"variable": "peso de cada pan de la panadería La Espiga", "valor": "250", "unidad_de_medida": "gramos"},
  {"variable": "porcentaje de panes de la panadería La Espiga con semillas", "valor": "30", "unidad_de_medida": "%"}]}

EJEMPLO 2
Valores de tiempo de un hecho: una fecha (unidad «fecha») y una hora (unidad «hora»); la variable nombra el hecho («apertura», «inicio de la charla»).
`documento`
<<<
[1] La feria del libro abrió el 3 de mayo. [2] La charla inaugural empezó a las 10 de la mañana.
>>>
`foco`: oraciones 1 y 2
{"datos": [
  {"variable": "fecha de apertura de la feria del libro", "valor": "3 de mayo", "unidad_de_medida": "fecha"},
  {"variable": "hora de inicio de la charla inaugural de la feria del libro", "valor": "10 de la mañana", "unidad_de_medida": "hora"}]}

EJEMPLO 3
Valores que son cualidades, dichas aparte («es fina») o pegadas al nombre («agua turbia»): la unidad es null y la variable nombra el aspecto (turbidez, textura).
`documento`
<<<
[1] El análisis del lago Verde encontró un agua turbia. [2] La arena de su orilla norte es fina.
>>>
`foco`: oraciones 1 y 2
{"datos": [
  {"variable": "turbidez del agua del lago Verde", "valor": "turbia", "unidad_de_medida": null},
  {"variable": "textura de la arena de la orilla norte del lago Verde", "valor": "fina", "unidad_de_medida": null}]}

EJEMPLO 4
Un foco con un solo dato. No se extraen: la creencia de los pescadores (no es un hecho), el origen del agua (es una relación), la pesca que podría ocurrir (es una posibilidad). «Las» se nombra como «truchas del lago Azul».
`documento`
<<<
[1] Los pescadores creían que el lago Azul tenía más de mil truchas. [2] Un censo del año pasado contó 300. [3] Su agua proviene de un manantial subterráneo. [4] Una pesca intensiva podría agotarlas.
>>>
`foco`: oraciones 1 a 4
{"datos": [
  {"variable": "número de truchas del lago Azul contadas por el censo del año pasado", "valor": "300", "unidad_de_medida": "unidad"}]}

ENTRADA
`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
