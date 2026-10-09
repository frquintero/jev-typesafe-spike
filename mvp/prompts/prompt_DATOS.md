[SISTEMA]
TAREA
Extrae los datos de CADA unidad temática de la lista.
Responde solo con el JSON.
La forma es el contrato: no agregues claves fuera de las que define `FORMATO DE RESPUESTA`.

UN DATO
Lo que la unidad establece acerca de algo, escrito para que se entienda sin el texto al lado:
- `aspecto`: qué se pregunta y de qué cosa, nombrada completa («altura del faro»).
- `valor`: lo que responde esa pregunta.
- `unidad_valor`: la unidad de medida, si el valor es un número con una sola unidad de medida; si no, null.

CÓMO SE DECIDE
1. Un dato por cada pregunta distinta que la unidad responde. No omitas ninguna.
2. Cada palabra va a un solo sitio: al valor, si cambia la respuesta; al aspecto, si acota la pregunta (cuándo, dónde, cada cuánto, de quién); fuera, si solo enlaza.
3. Fuera de los paréntesis, solo lo que dice el texto. Lo que agregues para que el dato se entienda —un antecedente que está en otra parte, lo que resume una expresión como «ese cambio», o lo que sabes del mundo— va entre paréntesis, junto a la expresión del texto. Un pronombre con un solo antecedente en la unidad se reemplaza, sin paréntesis. Si quedan dos posibles, aunque uno esté más cerca, escribe los dos.

CASOS
Las oraciones son inventadas. Cada caso es un precedente: cuando dudes, busca el parecido.

Caso 1. A dónde va cada palabra.
«El faro alcanza los cuarenta metros de altura.» → altura del faro = cuarenta [metros]
«El puente se inauguró hace cuarenta años.» → fecha de la inauguración del puente = hace cuarenta [años]
«Hoy el museo recibe unas tres mil visitas al mes.» → número de visitas mensuales que recibe hoy el museo = unas tres mil [null]
«Según la cooperativa, la cosecha subirá cerca de un veinte por ciento si llueve en abril.» → aumento previsto de la cosecha = cerca de un veinte, si llueve en abril, según la cooperativa [por ciento]
«Si cierran el puente, el tráfico se desviará por el norte.» → ruta del desvío del tráfico = por el norte, si cierran el puente [null]
Por qué: sin «hace», cuarenta años sería una duración; «hoy» y «al mes» acotan la pregunta; «si…» no establece que el puente se cierre: la condición va con la consecuencia y no es un dato aparte.

Caso 2. La unidad de medida.
«El tanque guarda doce mil litros. El glaciar retrocede diez metros por año. El cometa vuelve cada setenta y seis años. La travesía duró dos horas y cuarto. La isla tiene doce mil habitantes. La torre es tres veces más alta que la iglesia.»
→ capacidad del tanque = doce mil [litros] · retroceso anual del glaciar = diez [metros por año] · período de retorno del cometa = setenta y seis [años] · duración de la travesía = dos horas y cuarto [null] · número de habitantes de la isla = doce mil [null] · altura de la torre comparada con la de la iglesia = tres veces [null]
Por qué: «cada» acota la pregunta; dos horas y cuarto combina dos unidades; los habitantes se cuentan; tres veces compara.

Caso 3. Una pregunta, un dato; el valor es la respuesta.
«Los bomberos rescataron a dos excursionistas perdidos con un helicóptero de la gobernación.» → número de excursionistas perdidos rescatados por los bomberos = dos [null] · medio del rescate de los excursionistas = un helicóptero de la gobernación [null]
«De las lluvias de abril depende la cosecha del valle.» → fuente de la que depende la cosecha del valle = las lluvias de abril [null]
Por qué: «perdidos» dice cuáles excursionistas; el helicóptero responde otra pregunta.

Caso 4. Lo que se agrega va entre paréntesis.
«La fábrica cambió sus calderas de carbón por calderas de gas. Ese cambio redujo sus emisiones a la mitad.» → reducción de las emisiones de la fábrica por ese cambio (el de las calderas de carbón por calderas de gas) = la mitad [null]
«El alcalde inauguró la obra y el concejal la recorrió. Él prometió terminarla en mayo.» → autor de la promesa de terminar la obra = él (el alcalde o el concejal) [null]
«Su capital tiene dos puertos.» (la isla se nombra en otra unidad) → número de puertos de su capital (la de la isla) = dos [null]
Por qué: «sus emisiones» tiene un solo antecedente y se reemplaza; «ese cambio» no es un pronombre: resume lo dicho y lleva su referente entre paréntesis, aunque sea claro; «él» tiene dos posibles, aunque el concejal esté más cerca.

FORMATO DE RESPUESTA
Una salida por unidad, en el mismo orden de la lista, con su `caso`:

{"unidades": [
  {"n": <la posición de la unidad en la lista>,
   "caso": "<el caso de la unidad>",
   "datos": [
     {"aspecto": "<qué se pregunta y de qué cosa>",
      "valor": "<lo que responde>",
      "unidad_valor": "<la unidad de medida>" o null}]}]}

[TAREA]
UNIDADES
{{UNIDADES}}
