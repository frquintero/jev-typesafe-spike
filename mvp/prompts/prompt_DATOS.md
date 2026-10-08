TAREA
Extraer los datos de la UNIDAD TEMÁTICA

UN DATO es lo que la UNIDAD TEMÁTICA establece acerca de algo bajo un aspecto.

REGLAS
1. Extrae solo del contenido de la unidad que recibes: la unidad es el alcance.
2. No inventes: registra lo que el texto dice, sin agregar saber externo.

EJEMPLO 1.

Para la siguiente unidad temática:
{"caso": "las muestras que conserva el banco y el etiquetado de los sobres", "contenido": "Conserva muestras de cuarenta y dos especies nativas en sobres sellados. Cada sobre lleva la fecha de recolección y el nombre de quien recolectó."}

El json de salida con los datos es el siguiente:

{"caso": "las muestras que conserva el banco y el etiquetado de los sobres",
 "datos": [
   {"aspecto": "especies nativas conservadas",
    "valor": "cuarenta y dos",
    "unidad_valor": null},
   {"aspecto": "forma de conservación",
    "valor": "en sobres sellados",
    "unidad_valor": null},
   {"aspecto": "datos anotados en cada sobre",
    "valor": "la fecha de recolección y el nombre de quien recolectó",
    "unidad_valor": null}]}

EJEMPLO 2.

Para la siguiente unidad temática:
{"caso": "el corte similar al anunciado ocurrido el año pasado, que dejó sin servicio a dos colegios del sector y duró diecinueve horas", "contenido": "El año pasado, un corte similar dejó sin servicio a dos colegios del sector. Aquel episodio duró diecinueve horas."}

El json de salida con los datos es el siguiente:

{"caso": "el corte similar al anunciado ocurrido el año pasado, que dejó sin servicio a dos colegios del sector y duró diecinueve horas",
 "datos": [
   {"aspecto": "fecha del corte",
    "valor": "el año pasado",
    "unidad_valor": null},
   {"aspecto": "afectados por el corte",
    "valor": "dos colegios del sector",
    "unidad_valor": null},
   {"aspecto": "duración del corte",
    "valor": "diecinueve",
    "unidad_valor": "horas"}]}

EJEMPLO 3.

Para la siguiente unidad temática:
{"caso": "la revisión del borrador del convenio y la firma pendiente", "contenido": "La interventora y la secretaria revisaron el borrador en junio. Ella pidió incluir una cláusula de salida. Su firma quedó pendiente hasta después de las elecciones de octubre."}

El json de salida con los datos es el siguiente:

{"caso": "la revisión del borrador del convenio y la firma pendiente",
 "datos": [
   {"aspecto": "responsables de la revisión",
    "valor": "la interventora y la secretaria",
    "unidad_valor": null},
   {"aspecto": "fecha de la revisión del borrador",
    "valor": "junio",
    "unidad_valor": null},
   {"aspecto": "petición de la Interventora",
    "valor": "incluir una cláusula de salida",
    "unidad_valor": null},
   {"aspecto": "estado de la firma de la petición",
    "valor": "pendiente hasta después de las elecciones de octubre",
    "unidad_valor": null}]}

{{UNIDAD}}

FORMATO DE RESPUESTA


{"caso": "<el caso de la unidad>",
 "datos": [
   {"aspecto": "<bajo qué se considera>",
    "valor": "<lo que se establece>",
    "unidad_valor": la unidad del valor («kilómetros», «°C»), o null.}]}
