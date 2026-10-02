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
12. Conserva las circunstancias del acto de sostener algo en "condiciones" de
    su capa, y las del contenido atribuido en los registros correspondientes.
    Conserva las expresiones temporales y su orden con la precisión del texto.

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
  {"id":"K1","expresion":"…","quien":"C2","dentro_de":null,"condiciones":[],"respaldo":[…]}
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
  {"id":"K1","expresion":"según","quien":"C2","dentro_de":null,"condiciones":[],
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

TEXTO
{{TEXTO_NUMERADO}}
