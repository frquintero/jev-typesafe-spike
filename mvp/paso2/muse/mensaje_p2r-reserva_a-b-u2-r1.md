TAREA
Ejecuta el prompt que va abajo. Es una llamada del paso 2 del repo
jev-typesafe-spike sobre una unidad temática de un documento sintético:
devuelve su salida y nada más.

NIVEL DE RAZONAMIENTO
high: hay que leer y decidir; no es mecánico.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `mvp/paso2/prompt_ficha_contexto.md`, con
`{{TEXTO_NUMERADO}}` y `{{CONTEXTO}}` ya sustituidos; esto es exactamente lo que
recibe el modelo)
---------------------------------------------------------------------

TAREA
Lees un texto con sus oraciones numeradas. Reconstruye en una ficha JSON todo lo
que el texto establece, organizado por casos de estudio. No decides qué es
importante: registras lo dicho, sin agregar ni perder nada.

DEFINICIONES
- Caso de estudio: aquello de lo que el texto dice algo (una cosa, persona, lugar,
  hecho, estado, o incluso otra determinación). Se reconoce por sus menciones:
  nombre, pronombre, sujeto implícito.
- Aspecto: aquello bajo lo cual el texto considera el caso de estudio
  (temperatura, color, año de construcción).
- Determinación: lo que queda establecido acerca de un caso de estudio bajo un
  aspecto: «la temperatura del agua es 18 °C». El campo "valor" guarda solo la
  posición («18»); la fila entera es la determinación.
- Condición: lo que, si cambiara, cambiaría la pregunta respondida («en la
  superficie»: la temperatura en el fondo es otra pregunta). Si al cambiarlo
  cambia la cosa de la que se habla, es parte del caso de estudio.
- Capa: el texto atribuye algo a alguien (cree, dice, recomienda, según, supone).
  El texto afirma la capa; lo que va dentro lo sostiene quien la tiene, aunque
  sea el propio autor.
- Marca de posición: número, fecha, cantidad o categoría que señala una posición
  entre otras posibles.

PRINCIPIOS
1. Registra todo lo que el texto establece, incluidas generalizaciones,
   valoraciones y lo dicho al pasar («el técnico Pablo Ríos»).
2. No inventes. El aspecto debe tener respaldo en el texto. Si registras algo que
   el texto no dice, marca "inferido": true y da los fragmentos que te llevaron
   a ello.
3. Lo que está dentro de una creencia, recomendación o cita lleva "dentro_de"
   con el id de su capa. Una capa puede estar dentro de otra.
4. La negación va donde opera: «no cree» va en la capa; «cree que no» va en el
   valor.
5. Resuelve las referencias implícitas (pronombres, sujetos omitidos, términos
   de comparación como «otro», «igual», «el mismo») cuando el contexto da un
   solo antecedente: regístralas con "inferido": true y su respaldo. Mencionar
   algo para compararlo no lo vuelve lo comparado: lo comparado y el término de
   comparación son casos distintos, unidos por una relación. Si hay más de un
   antecedente posible, va a "dudas".
6. Los cambios se conservan en "cambio" («bajó a», «subió de… a…»).
7. Una recomendación u orden contiene una acción (lista "acciones"). No le
   atribuyas propiedades al objeto de la acción.
8. Explica en "marcas" cada marca de posición y cada número: qué hace (posición,
   identifica, remite). Un número que identifica o remite no es un valor:
   forma parte del nombre del caso que identifica.
9. Lo ambiguo (más de una lectura posible) va a "dudas". No lo resuelvas.
10. Copia los fragmentos de "respaldo" literales de la oración indicada. Un
    fragmento puede respaldar varias cosas.
11. Usa ids (C1, K1, D1, A1) para referirte a lo ya registrado.

FORMATO
Un solo objeto JSON con siete listas. Cada lista tiene una función y una forma
fija: usa exactamente estos campos, en cualquier texto. Una lista sin elementos
va vacía: [].
- casos: aquello de lo que el texto dice algo.
  {"id":"C1","nombre":"…","menciones":[{"o":1,"f":"…"}]}
  Los nombres, números o códigos que identifican un caso van en su nombre y sus
  menciones («pintura n.º 27 del inventario»), no como determinación.
- relaciones: un vínculo que el texto establece entre dos casos (parte de,
  muestra de, procede de, guardado en).
  {"id":"R1","tipo":"…","de":"C1","a":"C2","dentro_de":null,"condiciones":[],
   "inferido":false,"respaldo":[{"o":1,"f":"…"}]}
- capas: el texto atribuye algo a alguien.
  {"id":"K1","expresion":"…","quien":"C2","dentro_de":null,"respaldo":[…]}
- determinaciones: lo establecido acerca de un caso bajo un aspecto (forma en
  el ejemplo).
- acciones: lo que alguien hace, hizo, o se recomienda u ordena hacer. Una
  recomendación u orden es una acción dentro de su capa.
  {"id":"A1","agente":"C1","accion":"…","objeto":"C2","negada":false,
   "dentro_de":null,"condiciones":[],"respaldo":[…]}
  "agente" u "objeto" van null si el texto no los dice.
- marcas: cada marca de posición y cada número.
  {"marca":"…","o":1,"funciones":[{"funcion":"posición | identifica | remite",
   "refs":["D1"]}]}
- dudas: lo ambiguo, sin resolverlo.
  {"id":"Q1","texto":"…","respaldo":[…]}
Toda referencia a otro registro es un id ("C2") o una lista de ids
(["C2","C5"]), nunca texto libre. Una condición es
{"texto":"…","ref":id o null,"respaldo":[…]}.

EJEMPLO
Texto:
[1] En la superficie, el agua del estanque norte de la finca El Roble está a 18 °C. [2] Además tiene un color verdoso, algo preocupante según la bióloga Ana Ruiz.

Ficha:
{
 "casos": [
  {"id":"C1","nombre":"agua del estanque norte de la finca El Roble",
   "menciones":[{"o":1,"f":"el agua del estanque norte de la finca El Roble"},{"o":2,"f":"tiene"}]},
  {"id":"C2","nombre":"Ana Ruiz","menciones":[{"o":2,"f":"la bióloga Ana Ruiz"}]}
 ],
 "relaciones": [],
 "capas": [
  {"id":"K1","expresion":"según","quien":"C2","dentro_de":null,
   "respaldo":[{"o":2,"f":"según la bióloga Ana Ruiz"}]}
 ],
 "determinaciones": [
  {"id":"D1","dentro_de":null,"caso":"C1","aspecto":"temperatura","valor":"18","unidad":"°C",
   "cambio":null,"condiciones":[{"texto":"en la superficie","ref":null,"respaldo":[{"o":1,"f":"En la superficie"}]}],
   "modalidad":null,"inferido":false,"respaldo":[{"o":1,"f":"está a 18 °C"}]},
  {"id":"D2","dentro_de":null,"caso":"C1","aspecto":"color","valor":"verdoso","unidad":null,
   "cambio":null,"condiciones":[],"modalidad":null,"inferido":false,
   "respaldo":[{"o":2,"f":"tiene un color verdoso"}]},
  {"id":"D3","dentro_de":null,"caso":"C2","aspecto":"presentada como","valor":"bióloga","unidad":null,
   "cambio":null,"condiciones":[],"modalidad":null,"inferido":false,
   "respaldo":[{"o":2,"f":"la bióloga Ana Ruiz"}]},
  {"id":"D4","dentro_de":"K1","caso":"D2","aspecto":"carácter","valor":"algo preocupante","unidad":null,
   "cambio":null,"condiciones":[],"modalidad":null,"inferido":false,
   "respaldo":[{"o":2,"f":"algo preocupante"}]}
 ],
 "acciones": [],
 "marcas": [
  {"marca":"18 °C","o":1,"funciones":[{"funcion":"posición","refs":["D1"]}]},
  {"marca":"verdoso","o":2,"funciones":[{"funcion":"posición","refs":["D2"]}]},
  {"marca":"algo preocupante","o":2,"funciones":[{"funcion":"posición","refs":["D4"]}]}
 ],
 "dudas": []
}

UNIDAD Y CONTEXTO
La UNIDAD son las oraciones numeradas que van bajo TEXTO: es lo único de donde se
extrae. El CONTEXTO, cuando lo hay, trae material de apoyo del mismo documento,
de oraciones que quedaron fuera de la unidad: referencias externas ya resueltas
con sus respaldos, o el documento completo numerado. Si CONTEXTO viene vacío,
extrae solo de la unidad.

Cuando el CONTEXTO trae referencias, cada entrada indica la oración de la unidad
que trae la expresión, la expresión, el referente ya resuelto (o null) y los
fragmentos literales del documento que lo sostienen, con su número de oración.
Cuando trae el documento completo, las oraciones de la unidad van repetidas.

El contexto sirve para interpretar lo que la unidad dice, no para ampliarlo:
- Donde arriba dice «el texto», el texto del que se extrae es la unidad; el
  contexto no se extrae: solo aclara.
- La unidad manda: lo que registres tiene respaldo en una oración de la unidad.
- El contexto puede completar lo que la unidad deja incompleto: de quién o de qué
  se habla (un pronombre, un sujeto omitido, «la solicitud») y la condición o el
  punto de referencia que una oración de la unidad necesita para quedar
  representada («la noche anterior» → «la noche anterior al jueves del corte»).
- El contexto también puede aportar el contenido de una capa que la unidad
  establece («cuestionó esa conclusión»: la conclusión está en el respaldo).
- El contexto no abre asuntos. No registres determinaciones, acciones ni marcas
  que la unidad no establezca, aunque el respaldo las traiga: el número de
  habitantes que identifica al municipio no es un dato del subtema de su plaza.
- Un caso que el contexto identifica se registra una sola vez, con el nombre o la
  relación que su respaldo sostiene.
- Los fragmentos de "respaldo" pueden venir del contexto: copia su número de
  oración original tal como aparece.
- Si una referencia viene sin resolver (referente null), no elijas: registra la
  duda con las interpretaciones que su respaldo deja abiertas.
- "inferido": true marca lo que reconstruiste, y va en el registro donde ocurrió,
  no en todo lo que tocó el contexto. Resolver de quién se habla puede ser
  inferido si el vínculo no está dicho en la unidad; una determinación que la
  unidad establece no se vuelve inferida por usar el contexto.

TEXTO
[2] Su miel se vende hoy en tres ferias regionales.

CONTEXTO
REFERENCIAS EXTERNAS DE LA UNIDAD (su respaldo son fragmentos literales del documento, con su número de oración)
- oración 2 de la unidad · «Su» → La cooperativa apícola de la vereda El Retiro
  respaldo: [1] «La cooperativa apícola de la vereda El Retiro nació en 1998, cuando once familias se repartieron las primeras colmenas.» · [2] «Su miel se vende hoy en tres ferias regionales.»
