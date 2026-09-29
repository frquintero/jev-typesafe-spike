TAREA
Extrae los datos del `foco`. Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas.
- Unidad temática: un asunto y su desarrollo, en una o varias oraciones del documento, seguidas o separadas.
- Foco: conjunto de oraciones que forman una unidad temática, de las que se extraen los datos.
- Variable: aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor. El nombre de la variable dice el aspecto, aquello a lo que pertenece y sus circunstancias.
- Valor: lo que la variable toma en el foco: una cantidad (medida, conteo, fracción, fecha, hora) o una cualidad (alta, floral, rosado). Las cantidades con cuantificadores (pocos, muchos, unos, tantos) conservan su cuantificador.
- Unidad de medida: la unidad en que se expresa el valor; null si el valor no lleva número (alta, rosado, pocas).
- Dato: una variable con su valor y su unidad de medida. Se obtiene al responder: «¿qué valor toma esta variable que sale de este foco?».
- Formato: {"datos": [{"variable": "...", "valor": "...", "unidad_de_medida": "..." o null}]}

NO SON DATOS
- Lo que solo afirma o niega algo: su valor sería sí o no (abierto, vendido, sin interrupciones).
- Las relaciones entre cosas (recibe, atraviesa, anida en).
- Los adjetivos que solo identifican algo (antiguo muelle, piscina municipal).
- Los enunciados genéricos: dicen cómo es una clase o qué suele pasar, no el valor que tomó algo individual (en verano, los arroyos se secan en pocos días).

EJEMPLOS DE DATOS
{{EJEMPLOS}}
ENTRADA
`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
