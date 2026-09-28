TAREA
Extrae los datos del `foco` según las definiciones, como en los ejemplos. Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas.
- Foco: conjunto de oraciones del documento de las que se extraen los datos. El resto del documento solo sirve para saber a qué se refiere cada expresión del foco.
- Variable: aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor. Se nombra junto con aquello a lo que pertenece y sus circunstancias.
- Valor: lo que la variable toma en el foco: una cantidad (medida, conteo, fracción, fecha, hora) o una cualidad (alta, floral, rosado). Una cantidad vaga o aproximada conserva su cuantificador (unos 60, pocas).
- Unidad de medida: la unidad en que se expresa un número; null si el valor no lleva número (alta, rosado, pocas).
- Dato: una variable con su valor y su unidad de medida.
- Formato: {"datos": [{"variable": "...", "valor": "...", "unidad_de_medida": "..." o null}]}

NO SON DATOS
- Lo que solo afirma o niega algo: su valor sería sí o no (abierto, vendido, sin interrupciones).
- Las relaciones entre cosas (recibe, atraviesa, anida en).
- Los adjetivos que forman parte del nombre de algo (antiguo muelle).
- Los enunciados genéricos: dicen cómo es una clase o qué suele pasar, no el valor que tomó algo individual (en verano, los arroyos se secan en pocos días).

EJEMPLO 1
Números con su unidad: una medida, un conteo («unidad») y un porcentaje; la variable dice de qué es cada número.
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
La fecha o la hora de un hecho es un dato; el hecho mismo («abrió») no lo es.
`documento`
<<<
[1] La feria del libro abrió el 3 de mayo. [2] La charla inaugural empezó a las 10 de la mañana.
>>>
`foco`: oraciones 1 y 2
{"datos": [
  {"variable": "fecha de apertura de la feria del libro", "valor": "3 de mayo", "unidad_de_medida": "fecha"},
  {"variable": "hora de inicio de la charla inaugural de la feria del libro", "valor": "10 de la mañana", "unidad_de_medida": "hora"}]}

ENTRADA
`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
