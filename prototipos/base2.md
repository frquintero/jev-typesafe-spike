TAREA
{{TAREA}} Responde solo con el JSON.

DEFINICIONES
- Documento: el texto completo, con sus oraciones numeradas.
- Foco: conjunto de oraciones del documento de las que se extraen los datos. El resto del documento solo sirve para saber a qué se refiere cada expresión del foco.
- Variable: aspecto de una cosa, lugar, persona o hecho individual en el que caben diferencias de valor. Se nombra junto con aquello a lo que pertenece y sus circunstancias.
- Valor: lo que la variable toma en el foco: una cantidad (medida, conteo, fracción, fecha, hora) o una cualidad (alta, floral, rosado). Una cantidad vaga o aproximada conserva su cuantificador (unos 60, pocas).
- Unidad de medida: la unidad en que se expresa un número; null si el valor no lleva número (alta, rosado, pocas).
- Dato: una variable con su valor y su unidad de medida. El valor puede venir dicho aparte (la presión es extrema) o pegado al nombre (presiones extremas, contenedor de 800 kg). La fecha o la hora de un hecho también es un dato (abrió el 3 de mayo).
- Formato: {"datos": [{"variable": "...", "valor": "...", "unidad_de_medida": "..." o null}]}

NO SON DATOS
- Lo que solo afirma o niega algo: su valor sería sí o no (abierto, vendido, sin interrupciones).
- Las relaciones entre cosas (recibe, atraviesa, anida en).
- Los adjetivos que solo identifican algo (antiguo muelle, piscina municipal).
- Los enunciados genéricos: dicen cómo es una clase o qué suele pasar, no el valor que tomó algo individual (en verano, los arroyos se secan en pocos días).
{{EJEMPLOS}}
ENTRADA
`documento`
<<<
{{DOCUMENTO_NUMERADO}}
>>>
`foco`: {{FOCO}}
