TAREA
Ejecuta el prompt del repo que va abajo sobre el documento indicado y devuelve
su salida. Trabajas en el repo jev-typesafe-spike.

NIVEL DE RAZONAMIENTO
high: hay que decidir el agrupamiento; no es mecánico.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `unidades/prompts/unidades_v1.md`, con `{{TEXTO}}` ya sustituido;
esto es exactamente lo que recibe el modelo cuando corre
`python3 unidades/extraer_unidades.py`)
---------------------------------------------------------------------

TAREA
Divide `texto` en unidades temáticas.

DEFINICIONES PARA CUMPLIR LA TAREA
- Oración: todo lo que va desde el inicio de `texto`, o desde un punto, signo de interrogación o signo de exclamación, hasta el siguiente. El título es una etiqueta: no pertenece a ninguna unidad.
- Caso: la unidad concreta, no una clase, que queda distinguida en `texto` y acerca de la cual `texto` dice algo. Es la misma unidad aunque `texto` la nombre de varias maneras o con pronombres.
- Núcleo: el caso principal de un tramo de `texto`: aquel del que trata el tramo y al que se subordinan los demás casos del tramo.
- Satélite: un caso del que `texto` habla por su relación con un núcleo.
- Unidad temática: un núcleo, sus satélites y todas las oraciones de `texto` que se refieren a ellos.
- Anáfora: una mención cuyo caso solo se identifica por otra parte de `texto`. Si el sujeto está omitido, la mención es el verbo.
- Procedencia: quien dice, informa o mide lo que `texto` registra. Su alcance son las oraciones que dependen de esa fuente, aunque no la vuelvan a nombrar.

REGLAS
1. Identifica primero los casos de `texto` y unifícalos. Luego decide cuáles son núcleos y de qué núcleo es satélite cada uno de los demás.
2. Cada satélite pertenece a un solo núcleo.
3. Cada oración pertenece a una sola unidad. Una unidad puede reunir oraciones que no están seguidas.
4. Copia las oraciones y las menciones tal como aparecen en `texto`.
5. No extraigas datos ni juzgues lo que dicen las oraciones: solo agrupa.

ESTRUCTURA DEL JSON DE RESPUESTA (responde solo con este JSON)
{"unidades": [
   {"nucleo": {"caso": "<nombre más completo que le da `texto`>",
               "menciones": ["<mención literal>"]},
    "satelites": [
       {"caso": "<nombre más completo que le da `texto`>",
        "relacion": "<cómo se relaciona con el núcleo>",
        "menciones": ["<mención literal>"]}],
    "oraciones": ["<oración literal>"]}
 ],
 "anaforas": [
   {"mencion": "<literal>", "oracion": "<oración literal>", "caso": "<caso al que remite>"}],
 "procedencias": [
   {"fuente": "<literal>", "oraciones": ["<oración literal de su alcance>"]}],
 "oraciones_sin_unidad": ["<oración literal>"]}

`texto`
<<<
# El molino y la escuela de la vereda La Esperanza

El molino de viento de la vereda La Esperanza dejó de girar el martes. Su eje se agarrotó después de la tormenta. El molino abastece de agua a doce familias.

La escuela de la vereda tiene 34 alumnos. Su techo se filtró en la misma tormenta. El maestro recogió firmas para pedir materiales.

Según la alcaldía, la tormenta fue la más fuerte del año.

>>>
