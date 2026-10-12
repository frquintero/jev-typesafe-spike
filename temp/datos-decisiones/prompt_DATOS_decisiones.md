TAREA
Extraer los datos de CADA unidad temática de la lista.
Responde solo con el JSON.

QUÉ ES UN DATO
Un dato es lo que la unidad establece acerca de algo bajo un aspecto. Tiene tres partes:
- `aspecto`: bajo qué se considera la cosa. Nombra primero la dimensión (fecha, duración, número, cantidad, lugar, tamaño, causa, efecto, responsable…) y después la cosa de la que se habla: «fecha de la inauguración del mercado».
- `valor`: lo que la unidad establece bajo ese aspecto, con las palabras del texto. No repite el aspecto.
- `unidad_valor`: la unidad de medida del valor, o null.

Las MARCAS que acompañan lo que se establece se quedan en el valor: aproximación (unos, casi, cerca de), límite (hasta, más de, menos de), tiempo (hace, desde hace), atribución (según…) y condición (si…, cuando…). Cambian lo que el dato dice: «hace diez» años es una fecha; «diez» años, una duración.

REGLAS
1. La unidad es el alcance: extrae solo de su contenido.
2. Registra lo que el texto dice, sin agregar saber externo.
3. Una salida por unidad, en el mismo orden de la lista, con su `caso`.

DECISIONES
Antes de escribir cada dato, respóndete estas preguntas.

1. ¿Uno o dos datos?
Un dato por cada cosa que alguien podría preguntar por separado. Lo que solo dice cuál es la cosa va con ella; lo que agrega otro hecho sobre ella (cómo, con qué, dónde, cuándo, para qué) es otro dato.
- «Los bomberos rescataron a dos excursionistas perdidos.»
  {"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
- «Los bomberos rescataron a dos excursionistas con un helicóptero prestado por la gobernación.»
  {"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
  {"aspecto": "medio del rescate de los excursionistas", "valor": "un helicóptero", "unidad_valor": null}
  {"aspecto": "procedencia del helicóptero del rescate", "valor": "prestado por la gobernación", "unidad_valor": null}

2. ¿Resuelvo la referencia?
Resuélvela si su antecedente está dentro de la unidad y es uno solo: eso es leer, no inventar. Si hay dos candidatos dentro de la unidad, déjala literal y nombra los candidatos entre paréntesis. Si el antecedente está fuera de la unidad, déjala literal.
- «La planta potabilizadora trata trescientos litros por segundo. Su construcción costó ocho millones de dólares.» (un solo antecedente)
  {"aspecto": "costo de la construcción de la planta potabilizadora", "valor": "ocho millones", "unidad_valor": "dólares"}
- «El alcalde y el concejal visitaron la obra. Él prometió terminarla en mayo.» (dos candidatos)
  {"aspecto": "autor de la promesa de terminar la obra", "valor": "él (el alcalde o el concejal)", "unidad_valor": null}
  {"aspecto": "plazo prometido para terminar la obra", "valor": "en mayo", "unidad_valor": null}
- «Esa medida redujo los accidentes a la mitad.» (antecedente fuera de la unidad)
  {"aspecto": "efecto de esa medida sobre los accidentes", "valor": "los redujo a la mitad", "unidad_valor": null}

3. ¿Lleva unidad?
Solo si el valor es una medida: metros, años, toneladas, por ciento, litros al día. Si el valor cuenta cosas, lo contado va en el aspecto («número de…») y la unidad es null.
- «El tanque guarda doce mil litros.»
  {"aspecto": "capacidad del tanque", "valor": "doce mil", "unidad_valor": "litros"}
- «El colegio tiene seiscientos cuarenta estudiantes.»
  {"aspecto": "número de estudiantes del colegio", "valor": "seiscientos cuarenta", "unidad_valor": null}

4. ¿Cómo nombro el aspecto?
Primero la dimensión y después la cosa. El valor llena el aspecto; no lo repite.
- «Leer el mapa es entender la ciudad.»
  {"aspecto": "lo que significa leer el mapa", "valor": "entender la ciudad", "unidad_valor": null}
  y no {"aspecto": "lo que significa leer el mapa", "valor": "leer el mapa es entender la ciudad", "unidad_valor": null}

5. ¿Dónde van la atribución y la condición?
En el valor, como marcas: sin ellas el dato diría otra cosa.
- «Según la cooperativa, la cosecha subirá un veinte por ciento si llueve en abril.»
  {"aspecto": "aumento previsto de la cosecha", "valor": "un veinte, si llueve en abril, según la cooperativa", "unidad_valor": "por ciento"}

EJEMPLO COMPLETO

Para la siguiente lista de unidades temáticas:
[{"caso": "la huerta comunitaria del parque y su cosecha", "contenido": "La huerta comunitaria ocupa unos ochocientos metros cuadrados del parque. Desde hace dos años la cuidan treinta vecinos. Su cosecha de este año superó los trescientos kilos de hortalizas."},
 {"caso": "la reapertura del museo y lo que espera su directora", "contenido": "El museo reabrió en septiembre tras ocho meses de obras. Según su directora, las visitas se duplicarán si se mantiene la entrada gratuita."}]

El json de salida con los datos es el siguiente:

{"unidades": [
  {"n": 1,
   "caso": "la huerta comunitaria del parque y su cosecha",
   "datos": [
     {"aspecto": "superficie de la huerta comunitaria", "valor": "unos ochocientos", "unidad_valor": "metros cuadrados"},
     {"aspecto": "lugar de la huerta comunitaria", "valor": "el parque", "unidad_valor": null},
     {"aspecto": "número de vecinos que cuidan la huerta comunitaria", "valor": "treinta", "unidad_valor": null},
     {"aspecto": "tiempo que los vecinos llevan cuidando la huerta comunitaria", "valor": "desde hace dos", "unidad_valor": "años"},
     {"aspecto": "cosecha de hortalizas de la huerta comunitaria este año", "valor": "superó los trescientos", "unidad_valor": "kilos"}]},
  {"n": 2,
   "caso": "la reapertura del museo y lo que espera su directora",
   "datos": [
     {"aspecto": "fecha de la reapertura del museo", "valor": "septiembre", "unidad_valor": null},
     {"aspecto": "duración de las obras del museo", "valor": "ocho", "unidad_valor": "meses"},
     {"aspecto": "cambio previsto en las visitas al museo", "valor": "se duplicarán, si se mantiene la entrada gratuita, según la directora del museo", "unidad_valor": null}]}]}

UNIDADES
{{UNIDADES}}

FORMATO DE RESPUESTA

{"unidades": [
  {"n": <la posición de la unidad en la lista>,
   "caso": "<el caso de la unidad>",
   "datos": [
     {"aspecto": "<la dimensión y la cosa>",
      "valor": "<lo que se establece, con sus marcas>",
      "unidad_valor": "<la unidad de medida>" o null}]}]}
