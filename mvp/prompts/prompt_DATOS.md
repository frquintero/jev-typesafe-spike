[SISTEMA]
RELOJES (el «ahora» de la corrida y la fecha de radicación del documento; no son datos del documento)
{{RELOJES}}

CONTEXTO
Una UT es un caso —el núcleo, lo que la unidad dice que acaece, nombrado en su `caso`— junto con sus satélites, los casos de los que la UT habla por su relación con el núcleo, y todas las oraciones que se refieren a ellos.
Un DATO es el aspecto, el valor y su unidad de valor que se extrae de los satélites de cada UT y que establece algo particular acerca del caso de la UT. Los DATOS se encuentran formulando preguntas como: qué cosa particular se nombra, qué valor y qué unidades de valor se mencionan.

TAREA
De cada UT extrae todos los DATOS.
Responde solo con el JSON.

EJEMPLOS
caso: la renovación del faro de la isla y lo que se espera de ella
satélites:
[1] El faro de la isla alcanza los cuarenta metros de altura y se inauguró hace ciento veinte años.
[2] En dos mil diez, la alcaldía cambió su lámpara de queroseno por una lámpara de diodos.
[3] Ese cambio redujo el consumo de energía a la mitad.
[4] La luz gira cada doce segundos.
[5] El alcalde y el capitán del puerto recorrieron la obra; él prometió abrir el faro a los visitantes en mayo.
[6] Hoy el faro recibe unas tres mil visitas al mes.
[7] Según la cooperativa de pescadores, las capturas subirán cerca de un veinte por ciento si la luz alcanza las treinta millas.
[8] Faros automáticos como el de la isla se alimentan de energía solar, eólica y de la red eléctrica.

Los datos que se extraen son:
- altura del faro de la isla = cuarenta [metros]
- fecha de la inauguración del faro de la isla = hace ciento veinte [años]
- año del cambio de la lámpara del faro de la isla = dos mil diez [null]
- autor del cambio de la lámpara del faro de la isla = la alcaldía [null]
- lámpara que se reemplazó en el faro de la isla = su lámpara de queroseno [null]
- lámpara que se instaló en el faro de la isla = una lámpara de diodos [null]
- reducción del consumo de energía (del faro de la isla) por ese cambio (el de la lámpara de queroseno por una de diodos) = la mitad [null]
- período de giro de la luz (del faro de la isla) = doce [segundos]
- autor de la promesa de abrir el faro a los visitantes = él (el alcalde o el capitán del puerto) [null]
- fecha prometida para abrir el faro a los visitantes = mayo [null]
- número de visitas mensuales que recibe hoy el faro de la isla = unas tres mil [null]
- aumento previsto de las capturas (de los pescadores) = cerca de un veinte, si la luz alcanza las treinta millas, según la cooperativa de pescadores [por ciento]
- tipo de faros como el faro de la isla = automático [null]
- fuentes de energía de los faros automáticos = energía solar, eólica y de la red eléctrica [null]

caso: el rescate de dos pescadores perdidos cerca de la isla
satélites:
[1] Los guardacostas rescataron a dos pescadores perdidos a dieciocho millas de la costa, con una lancha del puerto.
[2] La búsqueda duró dos horas y cuarto, con vientos de treinta y cinco nudos.
[3] El agua estaba a catorce grados centígrados.
[4] Su luz guió la lancha de regreso al puerto.
[5] La lancha navega a cuarenta nudos, tres veces más rápido que la que tenía el puerto antes, y consume ciento veinte litros por hora.
[6] Lanchas semirrígidas como la del puerto resisten olas de hasta cuatro metros.

Los datos que se extraen son:
- número de pescadores perdidos rescatados por los guardacostas = dos [null]
- distancia de la costa a la que se rescató a los pescadores perdidos = dieciocho [millas]
- medio del rescate de los pescadores perdidos = una lancha del puerto [null]
- duración de la búsqueda (de los pescadores perdidos) = dos horas y cuarto [null]
- velocidad de los vientos durante la búsqueda = treinta y cinco [nudos]
- temperatura del agua (durante el rescate) = catorce [grados centígrados]
- lo que guió la lancha de regreso al puerto = su luz (la del faro de la isla) [null]
- velocidad de la lancha = cuarenta [nudos]
- velocidad de la lancha comparada con la de la que tenía el puerto antes = tres veces [null]
- consumo de la lancha = ciento veinte [litros por hora]
- tipo de lanchas como la lancha del puerto = semirrígida [null]
- altura de las olas que resisten las lanchas semirrígidas = hasta cuatro [metros]

FORMATO DE RESPUESTA
Una salida por UT, en el mismo orden de la lista, con su `caso`:

{"unidades": [
  {"n": <la posición de la UT en la lista>,
   "caso": "<el caso de la UT>",
   "datos": [
     {"aspecto": "<fragmento de información específico, independiente y que se explica por sí mismo>",
      "valor": "<qué valor tiene ese aspecto>",
      "unidad_valor": "<unidad de medida del aspecto>" o null}]}]}

[TAREA]
UNIDADES
{{UNIDADES}}
