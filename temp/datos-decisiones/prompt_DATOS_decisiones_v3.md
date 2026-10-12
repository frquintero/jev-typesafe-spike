TAREA
Extraer los datos de CADA unidad temática de la lista: recorre la unidad y, por cada cosa que establece, escribe un dato.
Responde solo con el JSON.

QUÉ ES UN DATO
Un dato es lo que la unidad establece acerca de algo bajo un aspecto: una posición en una escala.
- `aspecto`: la cosa de la que se habla y la escala en que se la considera: «la altura del faro», «la fecha de la reapertura del museo», «la causa del cierre de la vía». La cosa va nombrada completa, como se entendería sin el texto.
- `valor`: la posición que la unidad establece en esa escala, con sus calificadores. Es la respuesta mínima a la pregunta que plantea el aspecto: no repite el aspecto ni trae el verbo o la preposición que la introducen en el texto.
- `unidad_valor`: la unidad que hace falta para comparar este valor con otro del mismo aspecto; si no hace falta, null.

Lo que define la escala se nombra una sola vez: en el aspecto o en el valor. Los calificadores de la posición —cuánto se aproxima, qué límite fija, quién lo sostiene, bajo qué condición vale— van siempre en el valor: sin ellos el dato diría otra cosa.

Cada dato cumple tres condiciones:
- Distinto: responde una sola pregunta. Juntos, los datos de una unidad recogen todo lo que la unidad establece.
- Mínimo: no se puede partir en dos datos que respondan preguntas distintas.
- Autónomo: leído solo, sin el texto al lado, se entiende de qué habla y qué dice.

LA FRONTERA
Usa todo lo que la unidad dice para que el dato se entienda solo. Nada que la unidad no diga.

LAS REFERENCIAS
- Un pronombre o un posesivo con un solo antecedente en la unidad: reemplázalo por el antecedente.
- Una expresión que resume algo dicho antes, o un pronombre con dos antecedentes posibles: déjala como está y escribe entre paréntesis a qué remite según la unidad; si son dos, los dos.
- Si la unidad no dice a qué remite: déjala como está.

SI DOS COSAS CHOCAN
Manda, en este orden: primero, que el dato diga lo mismo que la unidad; segundo, que se entienda solo; tercero, la forma.

EJEMPLOS
Las oraciones son inventadas; cada ejemplo muestra un principio.

Muestra la escala nombrada una sola vez: estas dos formas dicen lo mismo; se escribe una, no las dos.
«El puente se inauguró hace cuarenta años.»
{"aspecto": "fecha de la inauguración del puente", "valor": "hace cuarenta", "unidad_valor": "años"}
o bien
{"aspecto": "tiempo transcurrido desde la inauguración del puente", "valor": "cuarenta", "unidad_valor": "años"}

Muestra los calificadores: se quedan en el valor.
«Según la cooperativa, la cosecha subirá cerca de un veinte por ciento si llueve en abril.»
{"aspecto": "aumento previsto de la cosecha", "valor": "cerca de un veinte, si llueve en abril, según la cooperativa", "unidad_valor": "por ciento"}

Muestra el dato distinto: el medio responde otra pregunta.
«Los bomberos rescataron a dos excursionistas con un helicóptero de la gobernación.»
{"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
{"aspecto": "medio del rescate de los excursionistas", "valor": "un helicóptero de la gobernación", "unidad_valor": null}

Muestra las referencias: una expresión que resume, un pronombre con dos antecedentes y una expresión que la unidad no resuelve.
«La fábrica cambió sus calderas de carbón por calderas de gas. Ese cambio redujo sus emisiones a la mitad.»
{"aspecto": "reducción de las emisiones de la fábrica por ese cambio (el de las calderas de carbón por calderas de gas)", "valor": "la mitad", "unidad_valor": null}
«El alcalde y el concejal visitaron la obra. Él prometió terminarla en mayo.»
{"aspecto": "autor de la promesa de terminar la obra", "valor": "él (el alcalde o el concejal)", "unidad_valor": null}
{"aspecto": "plazo prometido para terminar la obra", "valor": "mayo", "unidad_valor": null}
«Esa medida redujo los accidentes a la mitad.»
{"aspecto": "reducción de los accidentes por esa medida", "valor": "la mitad", "unidad_valor": null}

EJEMPLO COMPLETO

Para la siguiente lista de unidades temáticas:
[{"caso": "la reapertura del museo y lo que espera su directora", "contenido": "El museo reabrió en septiembre tras ocho meses de obras. Según su directora, las visitas se duplicarán si se mantiene la entrada gratuita."}]

El json de salida con los datos es el siguiente:

{"unidades": [
  {"n": 1,
   "caso": "la reapertura del museo y lo que espera su directora",
   "datos": [
     {"aspecto": "fecha de la reapertura del museo", "valor": "septiembre", "unidad_valor": null},
     {"aspecto": "duración de las obras del museo", "valor": "ocho", "unidad_valor": "meses"},
     {"aspecto": "cambio previsto en las visitas al museo", "valor": "se duplicarán, si se mantiene la entrada gratuita, según la directora del museo", "unidad_valor": null}]}]}

UNIDADES
{{UNIDADES}}

FORMATO DE RESPUESTA
Una salida por unidad, en el mismo orden de la lista, con su `caso`:

{"unidades": [
  {"n": <la posición de la unidad en la lista>,
   "caso": "<el caso de la unidad>",
   "datos": [
     {"aspecto": "<la cosa y la escala>",
      "valor": "<la posición, con sus calificadores>",
      "unidad_valor": "<la unidad para comparar>" o null}]}]}
