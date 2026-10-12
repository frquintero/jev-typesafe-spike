TAREA
Ejecuta el prompt del repo que va abajo sobre el documento indicado y devuelve
su salida. Trabajas en el repo jev-typesafe-spike.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `mvp/pruebas/prompt_v10.md`, con `{{TEXTO_NUMERADO}}` ya sustituido;
esto es exactamente lo que recibe el modelo)
---------------------------------------------------------------------

TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y los
ejemplos.
Responde solo con el JSON.

DEFINICIONES
- Oración: el texto que va de un punto, signo de interrogación o signo de exclamación al siguiente. En `texto` va numerada ([1], [2], …).
- Subtema: un asunto nuclear y su desarrollo, en una o varias oraciones, seguidas o separadas.
- Desarrollo: una oración desarrolla un subtema si lo detalla, lo explica, lo continúa, lo contradice o saca su consecuencia. Si abre un asunto que no depende de ninguno anterior, empieza un subtema nuevo.
- Nombrar el mismo lugar, objeto o persona no basta para unir oraciones: lo que las une es el asunto. Un cambio de párrafo no separa por sí solo un subtema.
- Nombre del subtema: una frase breve que dice qué se dice de las cosas, no solo cuáles son («el tamaño de la tripulación», no «la tripulación»).
- Cada oración va en un solo subtema.

EJEMPLO 1
Muestra un subtema que sigue después del cambio de párrafo: sus oraciones van juntas.
`texto`
<<<
[1] El ferri sale del puerto a las 7. [2] El cruce dura cuarenta minutos.

[3] Con mal tiempo, el cruce puede tardar el doble. [4] La tripulación tiene seis personas.
>>>
{"subtemas": [
  {"subtema": "el horario y la duración del cruce", "oraciones": [1, 2, 3]},
  {"subtema": "el tamaño de la tripulación", "oraciones": [4]}]}

EJEMPLO 2
Muestra las mismas cosas (la escuela, los alumnos) en asuntos distintos: van en subtemas distintos; la falla de la estufa desarrolla la calefacción.
`texto`
<<<
[1] La escuela rural tiene 60 alumnos. [2] Sus aulas se calientan con estufas de leña. [3] En invierno, la estufa del aula 2 falló dos veces. [4] Los alumnos de la escuela ganaron el concurso regional de lectura. [5] Su maestra preparó al equipo durante tres meses.
>>>
{"subtemas": [
  {"subtema": "el número de alumnos de la escuela", "oraciones": [1]},
  {"subtema": "la calefacción de las aulas y sus fallas", "oraciones": [2, 3]},
  {"subtema": "el triunfo en el concurso de lectura", "oraciones": [4, 5]}]}

EJEMPLO 3
Muestra una afirmación y la que la contradice: forman un solo subtema.
`texto`
<<<
[1] El manual de 1990 fijaba en 20 toneladas la carga máxima del puente del río Seco. [2] La inspección de este año la redujo a 12 toneladas por unas grietas en las vigas. [3] El puente fue construido en 1962 con vigas de concreto.
>>>
{"subtemas": [
  {"subtema": "la capacidad de carga del puente", "oraciones": [1, 2]},
  {"subtema": "la construcción del puente", "oraciones": [3]}]}

EJEMPLO 4
Muestra un hecho y su consecuencia: forman un solo subtema.
`texto`
<<<
[1] Las lluvias de mayo fueron escasas en la cuenca alta. [2] Por eso el embalse bajó al 40 % de su capacidad. [3] La represa abastece de agua a dos municipios.
>>>
{"subtemas": [
  {"subtema": "el descenso del embalse por la sequía", "oraciones": [1, 2]},
  {"subtema": "los municipios que abastece la represa", "oraciones": [3]}]}

EJEMPLO 5
Muestra un subtema que vuelve después de otro: sus oraciones separadas van juntas, aunque todo el texto hable del mismo mercado.
`texto`
<<<
[1] El mercado municipal abre a las 6. [2] Los puestos de frutas ocupan la nave central. [3] Los de pescado están en el ala norte. [4] Los sábados abre a las 5.
>>>
{"subtemas": [
  {"subtema": "el horario del mercado", "oraciones": [1, 4]},
  {"subtema": "la ubicación de los puestos", "oraciones": [2, 3]}]}

REFERENCIAS EXTERNAS

Una referencia es externa al subtema cuando necesita una expresión de otra
oración del documento que quedó en otro subtema para identificar de quién
o de qué se habla.

EJEMPLO 6
La apertura y el horario son asuntos distintos sobre la misma biblioteca.
El posesivo se resuelve citando el antecedente, sin cambiar los grupos.
La referencia ambigua permanece abierta.

Texto:
[1] La biblioteca del barrio Los Olmos abrió en 1998.
[2] Su horario de atención termina a las seis.
[3] Clara habló con Julia después de que ella regresara.

{"subtemas": [
  {"subtema": "la apertura de la biblioteca del barrio Los Olmos", "oraciones": [1]},
  {"subtema": "el horario de atención de la biblioteca del barrio Los Olmos", "oraciones": [2]},
  {"subtema": "la conversación de Clara y Julia después de un regreso", "oraciones": [3]}]}

EJEMPLO 7
La aclaración identifica solo la parte que depende del contexto: el archivo, no
el director. «Sus observaciones» se entiende dentro del propio grupo y no se
registra.

Texto:
[1] El archivo municipal conserva doce mil expedientes.
[2] Una comisión examinó algunos expedientes.
[3] El director del archivo recibió sus observaciones.

{"subtemas": [
  {"subtema": "los expedientes que conserva el archivo municipal", "oraciones": [1]},
  {"subtema": "el examen de algunos expedientes por una comisión y las observaciones que recibió el director del archivo", "oraciones": [2, 3]}]}

`texto`
<<<
[1] El primer tranvía de la ciudad empezó a rodar en 1893. [2] Lo operaba una compañía inglesa con capital privado. [3] La red llegó a tener veintiocho kilómetros de vías, según los planos de la época.

[4] En 1927, un incendio destruyó las caballerizas de la compañía. [5] El fuego se originó en un depósito de forraje. [6] La compañía no repuso los animales. [7] La ciudad tardó dos años en restablecer el servicio.

[8] En 1948, la municipalidad compró la red. [9] La compra incluyó los talleres y los vehículos que aún servían. [10] El municipio prometió modernizar las líneas. [11] Nunca ejecutó esa promesa.

[12] Los últimos tranvías circularon hasta 1965. [13] Su retiro coincidió con la ampliación de la avenida central. [14] La historiadora y la archivista revisaron los planos del taller. [15] Ella encontró un plano fechado en 1911. [16] Su hallazgo se publicó en la revista municipal. [17] La historiadora, Elvira Sanmiguel, atribuyó el cierre a la presión de los transportadores.
>>>

SALIDA
Devuelve únicamente el JSON, con esta estructura:

{"subtemas": [
  {"subtema": "…", "oraciones": [1, 2]},
  {"subtema": "…", "oraciones": [3]}]}
