TAREA
Extraer los datos de CADA unidad temática de la lista.
Responde solo con el JSON.

QUÉ ES UN DATO
Un dato es lo que la unidad establece acerca de algo bajo un aspecto. Cada dato cumple tres condiciones:
- Distinto: responde una sola pregunta. Juntos, los datos de una unidad recogen todo lo que la unidad establece.
- Mínimo: no se puede partir en dos datos que respondan preguntas distintas.
- Autónomo: leído solo, sin el texto al lado, se entiende de qué habla y qué dice.

LA FRONTERA
Puedes usar todo lo que la unidad dice para que el dato se entienda solo. Nada que la unidad no diga.

CÓMO SE EXTRAE
1. Recorre la unidad y separa cada cosa que establece: un dato por cada pregunta distinta que la unidad responde.
2. Escribe el `aspecto` como esa pregunta, sin signos: primero la dimensión (fecha, duración, número, lugar, tamaño, causa, efecto, responsable…) y después la cosa, nombrada completa. «temperatura en el núcleo del Sol» es la pregunta «¿cuál es la temperatura en el núcleo del Sol?».
3. Escribe el `valor` como la respuesta mínima a esa pregunta: sin el verbo ni la preposición que la introducen en el texto, y con sus marcas. Las marcas cambian lo que se establece y no se quitan: aproximación (unos, casi, cerca de), límite (hasta, más de, menos de), tiempo (hace, desde hace), atribución (según…) y condición (si…, cuando…).
4. Escribe la `unidad_valor` solo si la respuesta es una cantidad medida con una sola unidad (metros, años, toneladas, por ciento, litros al día). Si la respuesta cuenta cosas, combina unidades o no es una medida, va completa en el valor y la unidad es null.
5. Comprueba que el dato se entiende solo. Si una palabra remite a otra parte (él, ella, su, ese, esa, este, aquel…):
   - si la unidad dice a qué remite —una cosa o un hecho dicho antes—, reemplázala por eso;
   - si la unidad deja dos posibilidades, déjala y nombra las dos entre paréntesis;
   - si la unidad no lo dice, déjala tal cual.

EJEMPLOS
Cada uno muestra un paso; las oraciones son inventadas.

Muestra la respuesta mínima (paso 3): el verbo del texto no entra en el valor.
«El faro alcanza los cuarenta metros de altura.»
{"aspecto": "altura del faro", "valor": "cuarenta", "unidad_valor": "metros"}

Muestra un dato que se parte (paso 1): el medio responde otra pregunta.
«Los bomberos rescataron a dos excursionistas con un helicóptero de la gobernación.»
{"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
{"aspecto": "medio del rescate de los excursionistas", "valor": "un helicóptero de la gobernación", "unidad_valor": null}

Muestra la unidad (paso 4): una medida con una unidad, una medida que combina unidades y un conteo.
«El tanque guarda doce mil litros. La travesía duró dos horas y cuarto, con doce pasajeros a bordo.»
{"aspecto": "capacidad del tanque", "valor": "doce mil", "unidad_valor": "litros"}
{"aspecto": "duración de la travesía", "valor": "dos horas y cuarto", "unidad_valor": null}
{"aspecto": "número de pasajeros a bordo en la travesía", "valor": "doce", "unidad_valor": null}

Muestra las marcas (paso 3): la atribución y la condición se quedan en el valor.
«Según la cooperativa, la cosecha subirá un veinte por ciento si llueve en abril.»
{"aspecto": "aumento previsto de la cosecha", "valor": "un veinte, si llueve en abril, según la cooperativa", "unidad_valor": "por ciento"}

Muestra una palabra que remite a un hecho dicho antes (paso 5): la unidad lo dice, así que se reemplaza.
«La fábrica cambió sus calderas de carbón por calderas de gas. Ese cambio redujo sus emisiones a la mitad.»
{"aspecto": "reducción de las emisiones de la fábrica por el cambio de las calderas de carbón por calderas de gas", "valor": "la mitad", "unidad_valor": null}

Muestra dos posibilidades (paso 5): la unidad no decide, así que se nombran las dos.
«El alcalde y el concejal visitaron la obra. Él prometió terminarla en mayo.»
{"aspecto": "autor de la promesa de terminar la obra", "valor": "él (el alcalde o el concejal)", "unidad_valor": null}
{"aspecto": "plazo prometido para terminar la obra", "valor": "mayo", "unidad_valor": null}

Muestra una palabra que la unidad no resuelve (paso 5): se deja tal cual.
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
     {"aspecto": "<la pregunta: la dimensión y la cosa>",
      "valor": "<la respuesta mínima, con sus marcas>",
      "unidad_valor": "<la unidad de medida>" o null}]}]}
