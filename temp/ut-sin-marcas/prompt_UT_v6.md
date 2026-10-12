[SISTEMA]

TAREA

Extrae unidades temáticas (UT) de `texto`. Una UT contiene un nombre de subtema y una o varias oraciones literales que desarrollan un mismo asunto específico.

CRITERIOS

1. Agrupa una afirmación con su explicación, los elementos de una comparación o los pasos de un mecanismo o relación causal. Separa asuntos distintos aunque compartan entidad, categoría general o secuencia histórica.
2. Los títulos y subtítulos aportan contexto y jerarquía, pero no son UT ni se incluyen en `oraciones`. Los encabezados, párrafos y cambios de fecha, persona o cantidad no determinan por sí solos los límites de las UT.
3. Lee el documento completo para interpretar referencias. Mantén juntas las oraciones necesarias para comprender una relación interna al subtema. Puedes explicitar en `subtema` un referente situado en otra parte del documento, incluidos los encabezados, si es inequívoco. Conserva las ambigüedades del original; no uses información externa.
4. Nombra cada subtema con una frase breve que identifique el asunto y sus referentes. No copies automáticamente el encabezado ni añadas afirmaciones o amplíes el alcance del texto.

CONSERVACIÓN

5. Incluye cada aparición de una oración del cuerpo del texto exactamente una vez. Cópiala sin reformularla, corregirla, completarla ni dividirla.
6. Para esta tarea, una oración es un enunciado completo delimitado por puntuación de cierre. No cortes por dos puntos, punto y coma ni puntos de abreviaturas o números. Interrogación y exclamación delimitan cuando cierran un enunciado independiente. Si una oración reúne varios asuntos, consérvala entera y nombra su contenido conjunto; no añadas otras oraciones solo por esa mezcla.
7. Conserva el orden de las oraciones dentro de cada UT y ordena las UT por su primera oración. No fijes un número de unidades.

SALIDA

Devuelve solo JSON válido, sin bloques Markdown, comentarios ni claves adicionales:

{"unidades":[{"subtema":"Nombre del subtema","oraciones":["Oración literal."]}]}

Antes de responder, verifica: agrupación coherente, oraciones literales, cobertura completa, ninguna aparición duplicada y encabezados excluidos.

EJEMPLO DE ENTRADA

<texto>
# El océano: características, origen de la vida y regulación del clima

El océano cubre el setenta y uno por ciento de la superficie del planeta. Su profundidad media es de tres mil setecientos metros, y en los fondos abisales la temperatura ronda los dos grados centígrados.

La vida apareció en él hace unos tres mil quinientos millones de años. Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado.

El océano regula además el clima: absorbe el calor que la atmósfera retiene en el verano. Las corrientes que lo recorren reparten ese calor por el planeta y lo devuelven en el invierno.
</texto>

EJEMPLO DE SALIDA

{
  "unidades": [
    {
      "subtema": "La proporción de la superficie del planeta cubierta por el océano",
      "oraciones": [
        "El océano cubre el setenta y uno por ciento de la superficie del planeta."
      ]
    },
    {
      "subtema": "La profundidad media del océano y la temperatura de sus fondos abisales",
      "oraciones": [
        "Su profundidad media es de tres mil setecientos metros, y en los fondos abisales la temperatura ronda los dos grados centígrados."
      ]
    },
    {
      "subtema": "La antigüedad de la aparición de la vida en el océano",
      "oraciones": [
        "La vida apareció en él hace unos tres mil quinientos millones de años."
      ]
    },
    {
      "subtema": "Los primeros seres vivos y el período en que el mar fue el único lugar habitado",
      "oraciones": [
        "Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado."
      ]
    },
    {
      "subtema": "La regulación del clima mediante la absorción y redistribución de calor por el océano",
      "oraciones": [
        "El océano regula además el clima: absorbe el calor que la atmósfera retiene en el verano.",
        "Las corrientes que lo recorren reparten ese calor por el planeta y lo devuelven en el invierno."
      ]
    }
  ]
}

[USUARIO]

<texto>
{{TEXTO}}
</texto>

Extrae las UT del documento anterior. Devuelve únicamente el JSON solicitado.
