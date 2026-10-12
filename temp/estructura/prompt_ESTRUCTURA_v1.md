[SISTEMA]
RELOJES (la fecha de radicación del documento; no es dato del documento)
{{RELOJ_RADICADO}}

TAREA
Extrae la estructura lógica de `texto`: su índice. Un nodo del índice es un encabezado del documento —el título y su nivel—.

CRITERIOS
1. Un encabezado nombra un asunto y lo separa del resto: es una línea corta, sin puntuación de cierre y que no desarrolla nada por sí sola. Las líneas de desarrollo (las oraciones) no son encabezados.
2. El nivel dice la jerarquía: 1 es el asunto del documento, 2 sus secciones, 3 sus subsecciones. El primer nodo es de nivel 1, y un nodo no baja más de un nivel de golpe.
3. Conserva el título literal, tal como aparece: no lo reformules, no le cambies las mayúsculas ni le agregues signos.
4. El índice va en el orden del documento y cada encabezado entra una sola vez.

SALIDA
Devuelve solo JSON válido, sin bloques Markdown, comentarios ni claves de más:
{"indice":[{"nivel":1,"titulo":"Título del documento"},{"nivel":2,"titulo":"Título de una sección"}]}

Antes de responder, verifica: cada título está en el texto tal cual, en el orden del documento, sin faltar ninguno y sin saltos de nivel.

[TAREA]
<texto>
{{TEXTO}}
</texto>

RELOJES (el «ahora» de esta corrida; no es dato del documento)
{{RELOJ_SISTEMA}}

Extrae el índice del documento anterior. Devuelve únicamente el JSON solicitado.
