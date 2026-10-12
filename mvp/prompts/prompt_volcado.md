[SISTEMA]
RELOJES (la fecha de radicación del documento; no es dato del documento)
{{RELOJ_RADICADO}}

TAREA
Extrae los encabezados de `texto` y di de cuál encabezado cuelga cada uno.

QUÉ ES UN ENCABEZADO
Un encabezado nombra un asunto y lo separa del resto: es una línea corta, sin
puntuación de cierre y que no desarrolla nada por sí sola. Las oraciones de
desarrollo no son encabezados.

DE QUÉ CUELGA CADA ENCABEZADO
1. Numera los encabezados 1, 2, 3… en el orden en que aparecen.
2. A cada uno le asignas `padre`: el número de un encabezado anterior del cual
   depende, o 0 si no depende de ninguno.
3. Un encabezado depende de otro cuando trata un aspecto del asunto que el otro
   nombra. Si abre un asunto propio, su padre es 0.
4. Un documento puede tener varios encabezados con padre 0. No supongas que el
   primero es el título del documento, ni que es el único de su rango.
5. El padre es siempre un encabezado anterior: nunca uno posterior, nunca él mismo.
6. Si el encabezado trae marcador explícito (`1.`, `1.1`, `I.`, `A.`), el marcador
   decide: `1.1 X` cuelga de `1. Y`.

TÍTULO LITERAL
Conserva el título tal como aparece: no lo reformules, no le cambies las
mayúsculas ni le agregues signos.

SALIDA
Devuelve solo JSON válido, sin bloques Markdown, comentarios ni claves de más:
{"indice":[{"n":1,"titulo":"Un asunto","padre":0},
           {"n":2,"titulo":"Un aspecto suyo","padre":1}]}

Antes de responder, verifica: cada título está en el texto tal cual, en el orden
del documento, no falta ninguno, y todo `padre` es 0 o un número menor que `n`.

[TAREA]
<texto>
{{TEXTO}}
</texto>

RELOJES (el «ahora» de esta corrida; no es dato del documento)
{{RELOJ_SISTEMA}}

Extrae los encabezados del documento anterior. Devuelve únicamente el JSON solicitado.
