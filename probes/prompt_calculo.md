TAREA
Calcula el dato que se pide a partir de `texto`. Responde solo con el JSON.

REGLAS
- Usa solo los datos de `texto`.
- Si el dato pedido no está escrito de forma literal en `texto`, hay que derivarlo con aritmética a partir de lo que sí está escrito.
- `valor` es el resultado, no la expresión que lo enuncia.
- `unidad_de_medida` es la unidad en que se expresa el resultado; null si no lleva.
- Si no se puede calcular, deja `valor` en null y explica en `nota`.

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
