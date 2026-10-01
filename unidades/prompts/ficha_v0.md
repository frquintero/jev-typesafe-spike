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
5. Mencionar algo para compararlo no lo vuelve lo comparado: «otra sequía igual
   a la de 2024» no es la sequía de 2024.
6. Los cambios se conservan en "cambio" («bajó a», «subió de… a…»).
7. Una recomendación u orden contiene una acción (lista "acciones"). No le
   atribuyas propiedades al objeto de la acción.
8. Explica en "marcas" cada marca de posición y cada número: qué hace (posición,
   identifica, remite). Un número que identifica o remite no es un valor.
9. Lo ambiguo va a "dudas". No lo resuelvas.
10. Copia los fragmentos de "respaldo" literales de la oración indicada. Un
    fragmento puede respaldar varias cosas.
11. Usa ids (C1, K1, D1, A1) para referirte a lo ya registrado.

FORMATO
Un solo objeto JSON con las listas: casos, relaciones, capas, determinaciones,
acciones, marcas, dudas. Una lista sin elementos va vacía: [].

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
  {"marca":"18 °C","o":1,"funciones":[{"funcion":"posición","ref":"D1"}]},
  {"marca":"verdoso","o":2,"funciones":[{"funcion":"posición","ref":"D2"}]},
  {"marca":"algo preocupante","o":2,"funciones":[{"funcion":"posición","ref":"D4"}]}
 ],
 "dudas": []
}

TEXTO
{{TEXTO_NUMERADO}}
