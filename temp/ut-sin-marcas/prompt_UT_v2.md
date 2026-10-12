[SISTEMA]
TAREA
Crea unidades temáticas (UT).
Responde solo con el JSON.

OBSERVACIONES:
- Lee `texto` completo antes de formar las unidades temáticas.
- Conserva literalmente cada oración: no la reformules, completes, corrijas ni dividas en cláusulas.
- Asigna cada aparición de una oración a una sola UT. No omitas ni dupliques ninguna.
- Conserva el orden original de las oraciones dentro de cada UT. Ordena las UT por la primera aparición de sus oraciones.
- Agrupa oraciones cuando desarrollen un mismo asunto específico: una afirmación y su explicación, una comparación, un mecanismo, o una relación de causa y consecuencia. Cada oración incorporada debe contribuir a ese desarrollo.
- Abre otra UT cuando comience un asunto específico diferente. Compartir una entidad, una categoría general o un período histórico no basta para agrupar oraciones.
- La continuidad cronológica no basta para constituir una UT. Conserva una secuencia en la misma unidad únicamente cuando sus pasos desarrollen un mismo asunto específico.
- Si una oración contiene varios aspectos, consérvala completa y nombra su contenido conjunto. Esa indivisibilidad no justifica incorporar otras oraciones sobre asuntos diferentes.
- Los párrafos y los cambios de fecha, persona o cantidad son indicios; no constituyen por sí solos límites entre UT. No fijes de antemano un número de unidades.
- Interpreta las referencias utilizando únicamente `texto`. Conserva juntas las oraciones necesarias para comprender una relación interna al subtema. Si un referente se presenta en otra parte del documento, puedes explicitarlo en el nombre del subtema cuando el texto lo sustente inequívocamente.
- Si una referencia continúa siendo ambigua en el texto completo, conserva esa ambigüedad. No inventes antecedentes ni uses conocimiento externo para resolverla.
- Antes de responder, comprueba la literalidad, la cobertura completa, la asignación exclusiva y la coherencia temática de cada UT.
- La forma es el contrato: devuelve únicamente el JSON definido en `SALIDA`, sin comentarios ni claves adicionales.

DEFINICIONES:
- Oración, para esta tarea: un enunciado escrito completo delimitado por puntuación de cierre. Puede contener varias cláusulas coordinadas o subordinadas. Los dos puntos y el punto y coma no la dividen; los puntos de abreviaturas y números tampoco. Los signos de interrogación o exclamación delimitan una oración cuando cierran un enunciado independiente.
- Subtema: un asunto específico desarrollado en el texto acerca de una entidad, un conjunto de entidades, un proceso o una relación. Identifica tanto aquello de lo que se habla como el aspecto o la relación que se desarrolla.
- Unidad temática (UT): un nombre de subtema y una o varias oraciones literales que desarrollan conjuntamente ese asunto. Puede incluir varias afirmaciones vinculadas por una explicación, comparación, mecanismo o relación causal. Si una sola oración reúne asuntos distintos, se conserva íntegra como unidad mínima de extracción.
- Nombre del subtema: una frase breve y descriptiva que identifica el contenido específico de la UT y sus referentes principales. Puede explicitar contexto recuperado del documento, pero no añadir afirmaciones, resolver ambigüedades ni ampliar el alcance de lo dicho.
- Referencia recuperable: aquella cuyo referente puede identificarse mediante las oraciones de la UT y el contexto textual explicitado en su nombre. Una referencia no se considera resuelta solo porque resulte plausible.

EJEMPLO 1

`texto`
<<<
El océano cubre el setenta y uno por ciento de la superficie del planeta. Su profundidad media es de tres mil setecientos metros, y en los fondos abisales la temperatura ronda los dos grados centígrados.

La vida apareció en él hace unos tres mil quinientos millones de años. Los primeros seres vivos fueron microorganismos de unas pocas micras, y durante casi tres mil millones de años el mar fue el único lugar habitado. El océano regula además el clima: absorbe el calor que la atmósfera retiene en el verano. Las corrientes que lo recorren reparten ese calor por el planeta y lo devuelven en el invierno.
>>>
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

EJEMPLO 2

`texto`
<<<
La anemia falciforme se debe al cambio de una sola letra en el gen de la beta globina, que está en el cromosoma once. En la posición seis de la proteína, un ácido glutámico queda sustituido por una valina. La hemoglobina que resulta, llamada hemoglobina S, se agrupa en fibras rígidas cuando le falta oxígeno. Esas fibras deforman los glóbulos rojos, que pierden su forma de disco y toman la de una hoz. Un glóbulo rojo sano vive unos ciento veinte días; uno falciforme, entre diez y veinte.

La enfermedad se describió hace más de un siglo, en mil novecientos diez, cuando un médico de Chicago observó glóbulos alargados en la sangre de un estudiante. En mil novecientos cuarenta y nueve, Linus Pauling mostró que la hemoglobina de los enfermos migraba de otro modo en un campo eléctrico. Vernon Ingram identificó en mil novecientos cincuenta y siete el aminoácido sustituido. Él la llamó una enfermedad molecular. Ese hallazgo convirtió a la anemia falciforme en la primera enfermedad explicada por un cambio en una proteína.

La herencia es recesiva: quien recibe una sola copia alterada es portador y casi nunca enferma. Si ambos padres son portadores, cada embarazo tiene una probabilidad de uno en cuatro de dar un hijo enfermo. Los portadores, en cambio, resisten mejor la malaria grave. Según los estudios de campo, esa ventaja reduce su riesgo de malaria grave en cerca de un noventa por ciento. Por eso, en algunas regiones de África, hasta uno de cada cuatro habitantes lleva la mutación.

Según la Organización Mundial de la Salud, cada año nacen unos trescientos mil niños con formas graves de la enfermedad. Su tratamiento clásico es la hidroxiurea, que aumenta la hemoglobina fetal, aprobada para adultos en mil novecientos noventa y ocho. En diciembre de dos mil veintitrés se aprobó la primera terapia basada en la edición genética con CRISPR. En el ensayo principal, veintinueve de treinta pacientes pasaron al menos un año sin crisis de dolor. Cada tratamiento cuesta unos dos millones de dólares.
>>>
{
  "unidades": [
    {
      "subtema": "La alteración molecular que produce la deformación de los glóbulos rojos en la anemia falciforme",
      "oraciones": [
        "La anemia falciforme se debe al cambio de una sola letra en el gen de la beta globina, que está en el cromosoma once.",
        "En la posición seis de la proteína, un ácido glutámico queda sustituido por una valina.",
        "La hemoglobina que resulta, llamada hemoglobina S, se agrupa en fibras rígidas cuando le falta oxígeno.",
        "Esas fibras deforman los glóbulos rojos, que pierden su forma de disco y toman la de una hoz."
      ]
    },
    {
      "subtema": "La duración de la vida de los glóbulos rojos sanos y falciformes",
      "oraciones": [
        "Un glóbulo rojo sano vive unos ciento veinte días; uno falciforme, entre diez y veinte."
      ]
    },
    {
      "subtema": "La descripción clínica de la anemia falciforme en 1910",
      "oraciones": [
        "La enfermedad se describió hace más de un siglo, en mil novecientos diez, cuando un médico de Chicago observó glóbulos alargados en la sangre de un estudiante."
      ]
    },
    {
      "subtema": "El hallazgo de Pauling sobre la migración eléctrica de la hemoglobina en la anemia falciforme",
      "oraciones": [
        "En mil novecientos cuarenta y nueve, Linus Pauling mostró que la hemoglobina de los enfermos migraba de otro modo en un campo eléctrico."
      ]
    },
    {
      "subtema": "La identificación del aminoácido sustituido y su importancia para la explicación molecular de la anemia falciforme",
      "oraciones": [
        "Vernon Ingram identificó en mil novecientos cincuenta y siete el aminoácido sustituido.",
        "Él la llamó una enfermedad molecular.",
        "Ese hallazgo convirtió a la anemia falciforme en la primera enfermedad explicada por un cambio en una proteína."
      ]
    },
    {
      "subtema": "La herencia recesiva de la anemia falciforme y el riesgo para los hijos de padres portadores",
      "oraciones": [
        "La herencia es recesiva: quien recibe una sola copia alterada es portador y casi nunca enferma.",
        "Si ambos padres son portadores, cada embarazo tiene una probabilidad de uno en cuatro de dar un hijo enfermo."
      ]
    },
    {
      "subtema": "La ventaja frente a la malaria de los portadores de la mutación falciforme como explicación de su frecuencia en algunas regiones de África",
      "oraciones": [
        "Los portadores, en cambio, resisten mejor la malaria grave.",
        "Según los estudios de campo, esa ventaja reduce su riesgo de malaria grave en cerca de un noventa por ciento.",
        "Por eso, en algunas regiones de África, hasta uno de cada cuatro habitantes lleva la mutación."
      ]
    },
    {
      "subtema": "Los nacimientos anuales de niños con formas graves de anemia falciforme",
      "oraciones": [
        "Según la Organización Mundial de la Salud, cada año nacen unos trescientos mil niños con formas graves de la enfermedad."
      ]
    },
    {
      "subtema": "El tratamiento de la anemia falciforme con hidroxiurea",
      "oraciones": [
        "Su tratamiento clásico es la hidroxiurea, que aumenta la hemoglobina fetal, aprobada para adultos en mil novecientos noventa y ocho."
      ]
    },
    {
      "subtema": "La aprobación, los resultados y el costo de la terapia con CRISPR para la anemia falciforme",
      "oraciones": [
        "En diciembre de dos mil veintitrés se aprobó la primera terapia basada en la edición genética con CRISPR.",
        "En el ensayo principal, veintinueve de treinta pacientes pasaron al menos un año sin crisis de dolor.",
        "Cada tratamiento cuesta unos dos millones de dólares."
      ]
    }
  ]
}

SALIDA
Devuelve únicamente el JSON, con esta estructura:

{"unidades": [
  {"subtema": "…", "oraciones": ["…", "…"]},
  {"subtema": "…", "oraciones": ["…"]}]}

[TAREA]
`texto`
<<<
{{TEXTO}}
>>>
