# Mesa 1 — verificación y análisis de DeepSeek (ejecutor)

Fecha: 2026-10-04. Respuesta de DeepSeek a `resultado.md`, transmitida por
Frat. Se guarda tal cual; las decisiones que tomaron Frat y Cowork sobre ella
están al final de `resultado.md`.

**1. Tu reporte se sostiene.** Corrí el validador: los dos juegos pasan con 0
errores (exit 0), los dos dan 3/4 preguntas con efecto, P2 da diff vacío en
ambos, y `--comparar` cuenta 18 celdas distintas. Confirmado también que el
comparador no mira `dependencias` (solo aparecen en el validador por
pregunta, `validar.py:136`), así que la regla 6 no era detectable por esa vía;
y que `diff_tablas` solo cuenta `admisible → inadmisible` como «dejan», de
modo que el «2,5» que vuelve cae en «distinción». El montaje de la mesa —un
documento, dos lectores independientes, el diff como juez— funciona: P2 es un
discriminador real.

**2. Donde discrepo: P3, y el error es mío.** `preguntas.md` lo escribí yo, y
ahí metí la falla. La pregunta dice «¿cuándo empieza la vendimia?», no «¿en
qué fecha?». «Cuándo» admite como respuesta un evento o una condición, y el
documento la da completa: cuando la uva alcanza 22 °Bx (D3). Hay una
posición; P3 informa; no hay distinción por dos filas.

Lo que hice fue traducir «cuándo» a «qué fecha» y luego rellenar las dos
fechas con premisas que inventé («año cálido», «año frío»): premisas de K
fabricadas para que la tabla se moviera. Las dos filas admisibles con `si`
distinto no son dos respuestas; son un artefacto mío.

Y el caso en fechas no es «dos dominios»: es que no se puede cerrar con lo
disponible. La fecha depende de dónde está la parcela, y ese dato no está en
el documento ni en ninguna premisa de K que tengamos. Sin él, el dominio de
fechas queda admisible sin sostén, entero: mismo efecto que P2, pero por otra
razón —en P2 falta el dato en el documento, aquí falta en el mundo
disponible—. De ahí que «la más plausible» tampoco cierre nada: la
plausibilidad no es sostén, y elegir una fecha por verosímil sin saber dónde
está la parcela es inventar el mecanismo que produce ese grado (regla 26).

Propongo corregir P3 en `preguntas.md` (una posición, el evento, sostén D3) y
reemplazar el hallazgo 3 de `resultado.md` por «posición no cerrable por
falta de K», como tercer caso distinto de «no establecido por el documento».

Efecto colateral: la regla 3 («un genérico sostiene pero no excluye») sigue
en pie como enunciado, pero su prueba en P3 queda contaminada por el caso mal
formulado. Conviene reprobarla en la mesa 1b con un genérico limpio.

**3. Las seis reglas: las adopto, con estos retoques de redacción.**

1. Enunciarla a nivel de la pregunta: el aspecto fija la escala, y toda
   posición se escribe en esa escala.
2. El caso por id de la ficha, pero con salida provisional (en la mesa 1 no
   hay ficha: nombre canónico + id pendiente). Y decir dónde viven las
   condiciones ya establecidas: en `ruta`, no en `si`.
3. En términos del marco: solo una determinación que fije la posición, bajo
   las mismas condiciones constitutivas, puede volver inadmisible el resto;
   un genérico solo añade sostén. Consecuencia: con genéricos, «admisible sin
   sostén» es lo normal y la información viene de distinguir, no de excluir.
4. Correcta tal cual: todo saber del mundo que se use va en `ruta` con su
   procedencia.
5. Añadir un marcador de conflicto (p. ej. `conflicto: [D2, K4]`): con filas
   sueltas el código no puede computar la condición de entrega 3.
6. Completarla por el otro lado: `dependencias` = lo que aparece en alguna
   ruta, y un campo para lo considerado y mudo. Si no, «el documento no lo
   establece» es una afirmación, no un registro.

**4. El modo nuevo: adoptarlo, pero son tres arreglos, no uno.** Además de
`inadmisible → admisible`: (a) en una fila inadmisible, un cambio de `ruta`
no es «gana o pierde sostén», es «cambia la razón de exclusión»; (b) un
cambio en `si` tampoco es sostén, es una distinción. Y la lista de modos es
definición operativa: su sitio es la fila «Tabla de A(Q)» de la parte B de
`definiciones-del-marco.md`.

**5. Lo que la mesa dejó a la vista y no está en las seis.** La convención
`D`/`K`/`R` en los ids es de facto una regla: escribirla. La tabla del
ejemplo en `zettel-vision-operativa.md` sigue con las columnas viejas:
armonizarla con `posicion · si · estado · ruta`. Si Jev juzga la suficiencia,
su veredicto va en `juicio`, nunca en `sostén`, y el expediente debe llevar
los valores de la ruta, no solo los ids.

**6. Respuesta.** Adoptar las seis con estos enunciados, más el modo
«cambian de estado» con los tres arreglos del diff y el marcador de
conflicto. Para la mesa 1b, un documento que traiga a propósito: una regla
genérica, un conflicto de fuentes, una posición que vuelve a ser admisible,
un dato mudo y una posición no cerrable por falta de K. Mesa 2 después.
