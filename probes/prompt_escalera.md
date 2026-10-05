TAREA
Encuentra el dato que se pide a partir de `texto`. Responde solo con el JSON.

REGLAS
- Usa solo los datos de `texto`.
- Si el dato pedido no está escrito de forma literal, derívalo con aritmética a partir de lo que sí está escrito.
- `valor` es el resultado, no la expresión que lo enuncia.
- `unidad_de_medida` es la unidad en que se expresa el resultado; null si no lleva.
- Si `texto` no contiene el dato y no se puede derivar, deja `valor` en null. No lo inventes ni lo estimes.
- Si el dato aparece con un cuantificador vago (cerca de, unos, pocas, muchos), y lo que se pide es una cantidad exacta, deja `valor` en null.

RESPUESTA
{"dato": {"variable": "<la variable pedida>", "valor": <número o null>, "unidad_de_medida": "<unidad o null>", "nota": "<de dónde sale, o vacío>"}}

`texto`
<<<
{{TEXTO}}
>>>

`dato_pedido`
<<<
{{PREGUNTA}}
>>>
