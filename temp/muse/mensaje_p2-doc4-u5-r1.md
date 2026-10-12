TAREA
Ejecuta el prompt que va abajo sobre la unidad temática indicada y devuelve su
salida. Trabajas en el repo jev-typesafe-spike.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en la unidad.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `temp/prompt2-borrador.md`, con `{{UNIDAD}}` ya sustituido)
---------------------------------------------------------------------

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
   {"aspecto": "conservación de las muestras",
    "valor": "en sobres sellados",
    "unidad_valor": null},
   {"aspecto": "lo que lleva cada sobre",
    "valor": "la fecha de recolección y el nombre de quien recolectó",
    "unidad_valor": null}],
 "dudas": []}

EJEMPLO 2.

Para la siguiente unidad temática:
{"caso": "el corte similar al anunciado ocurrido el año pasado, que dejó sin servicio a dos colegios del sector y duró diecinueve horas", "contenido": "El año pasado, un corte similar dejó sin servicio a dos colegios del sector. Aquel episodio duró diecinueve horas."}

El json de salida con los datos es el siguiente:

{"caso": "el corte similar al anunciado ocurrido el año pasado, que dejó sin servicio a dos colegios del sector y duró diecinueve horas",
 "datos": [
   {"aspecto": "cuándo ocurrió",
    "valor": "el año pasado",
    "unidad_valor": null},
   {"aspecto": "a quiénes dejó sin servicio",
    "valor": "dos colegios del sector",
    "unidad_valor": null},
   {"aspecto": "duración del corte",
    "valor": "diecinueve",
    "unidad_valor": "horas"}],
 "dudas": []}

EJEMPLO 3.

Para la siguiente unidad temática:
{"caso": "la revisión del borrador del convenio y la firma pendiente", "contenido": "La interventora y la secretaria revisaron el borrador en junio. Ella pidió incluir una cláusula de salida. Su firma quedó pendiente hasta después de las elecciones de octubre."}

El json de salida con los datos es el siguiente:

{"caso": "la revisión del borrador del convenio y la firma pendiente",
 "datos": [
   {"aspecto": "quiénes revisaron el borrador",
    "valor": "la interventora y la secretaria",
    "unidad_valor": null},
   {"aspecto": "cuándo se revisó",
    "valor": "en junio",
    "unidad_valor": null},
   {"aspecto": "petición",
    "valor": "incluir una cláusula de salida",
    "unidad_valor": null},
   {"aspecto": "estado de la firma",
    "valor": "pendiente hasta después de las elecciones de octubre",
    "unidad_valor": null}],
 "dudas": [
   "No se establece si quien pidió incluir la cláusula fue la interventora o la secretaria.",
   "No se establece de quién es la firma pendiente."]}

{"caso": "el corte similar al anunciado ocurrido el año pasado, que dejó sin servicio a dos colegios del sector y duró diecinueve horas", "contenido": "El año pasado, un corte similar dejó sin servicio a dos colegios del sector. Aquel episodio duró diecinueve horas."}

FORMATO DE RESPUESTA


{"caso": "<el caso de la unidad>",
 "datos": [
   {"aspecto": "<bajo qué se considera>",
    "valor": "<lo que se establece>",
    "unidad_valor": la unidad del valor («kilómetros», «°C»), o null.}],
 "dudas": [{texto con descripción corta si hay alguna duda sobre el valor o la unidad o vacio si no hay dudas}]}
