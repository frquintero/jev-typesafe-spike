TAREA
Extrae los datos de CADA unidad temática de la lista.
Responde solo con el JSON.

UN DATO
Un dato es lo que la unidad establece acerca de algo bajo un aspecto, escrito para que se entienda sin el texto al lado.
- `aspecto`: qué se pregunta y de qué cosa, con la cosa nombrada completa: «altura del faro», «fecha de la reapertura del museo».
- `valor`: lo que responde esa pregunta, según la unidad.
- `unidad_valor`: la unidad de medida, si el valor es un número con una sola unidad de medida; si no, null.

CÓMO SE DECIDE
1. Registra todo lo que la unidad establece: un dato por cada pregunta que la unidad responde. Si dos datos se parecen, registra los dos.
2. En el valor se quedan las palabras que cambian lo que se responde y salen las que solo enlazan la oración. Prueba: si al quitar una palabra la respuesta cambia, la palabra se queda.
3. Usa todo lo que la unidad dice para que el dato se entienda solo. Nada que la unidad no diga.
4. Las referencias:
   - un pronombre o un posesivo con un solo antecedente en la unidad: reemplázalo por el antecedente;
   - una expresión que resume algo dicho antes, o un pronombre con dos antecedentes posibles: déjala como está y escribe entre paréntesis a qué remite según la unidad; si son dos, los dos;
   - si la unidad no dice a qué remite: déjala como está.

CASOS
Las oraciones son inventadas. Cada caso es un precedente: cuando dudes, busca el caso parecido.

Caso 1. Lo que solo enlaza sale del valor.
«El faro alcanza los cuarenta metros de altura.»
{"aspecto": "altura del faro", "valor": "cuarenta", "unidad_valor": "metros"}
Por qué: sin «alcanza los», la respuesta es la misma.

Caso 2. Lo que cambia la respuesta se queda en el valor.
«El puente se inauguró hace cuarenta años.»
{"aspecto": "fecha de la inauguración del puente", "valor": "hace cuarenta", "unidad_valor": "años"}
«Según la cooperativa, la cosecha subirá cerca de un veinte por ciento si llueve en abril.»
{"aspecto": "aumento previsto de la cosecha", "valor": "cerca de un veinte, si llueve en abril, según la cooperativa", "unidad_valor": "por ciento"}
Por qué: sin «hace», cuarenta años sería una duración y no una fecha; sin «cerca de», «si llueve en abril» o «según la cooperativa», el dato afirmaría otra cosa.

Caso 3. La unidad de medida.
«El tanque guarda doce mil litros. El glaciar retrocede diez metros por año. La travesía duró dos horas y cuarto, con doce pasajeros. La torre es tres veces más alta que la iglesia.»
{"aspecto": "capacidad del tanque", "valor": "doce mil", "unidad_valor": "litros"}
{"aspecto": "retroceso anual del glaciar", "valor": "diez", "unidad_valor": "metros por año"}
{"aspecto": "duración de la travesía", "valor": "dos horas y cuarto", "unidad_valor": null}
{"aspecto": "número de pasajeros de la travesía", "valor": "doce", "unidad_valor": null}
{"aspecto": "altura de la torre comparada con la de la iglesia", "valor": "tres veces más alta", "unidad_valor": null}
Por qué: litros y metros por año son una sola unidad de medida; dos horas y cuarto combina dos; doce cuenta pasajeros; tres veces compara.

Caso 4. Una pregunta, un dato.
«Los bomberos rescataron a dos excursionistas perdidos.»
{"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
«Los bomberos rescataron a dos excursionistas con un helicóptero de la gobernación.»
{"aspecto": "número de excursionistas rescatados por los bomberos", "valor": "dos", "unidad_valor": null}
{"aspecto": "medio del rescate de los excursionistas", "valor": "un helicóptero de la gobernación", "unidad_valor": null}
Por qué: «perdidos» solo dice cuáles excursionistas; el helicóptero responde otra pregunta: con qué.

Caso 5. El valor es lo que responde la pregunta, no lo que sobra de la oración.
«De las lluvias de abril depende la cosecha del valle.»
{"aspecto": "fuente de la que depende la cosecha del valle", "valor": "las lluvias de abril", "unidad_valor": null}
Por qué: la pregunta es de qué depende la cosecha; la respuesta son las lluvias de abril.

Caso 6. Las referencias.
«La fábrica cambió sus calderas de carbón por calderas de gas. Ese cambio redujo sus emisiones a la mitad.»
{"aspecto": "reducción de las emisiones de la fábrica por ese cambio (el de las calderas de carbón por calderas de gas)", "valor": "la mitad", "unidad_valor": null}
«El alcalde y el concejal visitaron la obra. Él prometió terminarla en mayo.»
{"aspecto": "autor de la promesa de terminar la obra", "valor": "él (el alcalde o el concejal)", "unidad_valor": null}
{"aspecto": "plazo prometido para terminar la obra", "valor": "mayo", "unidad_valor": null}
«Esa medida redujo los accidentes a la mitad.»
{"aspecto": "reducción de los accidentes por esa medida", "valor": "la mitad", "unidad_valor": null}
Por qué: «sus» tiene un solo antecedente y se reemplaza; «ese cambio» resume lo dicho antes y queda con su referente entre paréntesis; «él» tiene dos antecedentes posibles; «esa medida» no se resuelve dentro de la unidad.

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
     {"aspecto": "<qué se pregunta y de qué cosa>",
      "valor": "<lo que responde, según la unidad>",
      "unidad_valor": "<la unidad de medida>" o null}]}]}
