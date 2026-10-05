TAREA
Ejecuta el prompt del repo que va abajo sobre el documento indicado y devuelve
su salida. Trabajas en el repo jev-typesafe-spike.

NIVEL DE RAZONAMIENTO
high: hay que leer el documento y decidir; no es mecánico.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `mvp/pruebas/prompt_v6.md`, con `{{TEXTO_NUMERADO}}` ya sustituido;
esto es exactamente lo que recibe el modelo cuando corre
`python3 unidades/extraer_unidades.py`)
---------------------------------------------------------------------

TAREA
Agrupa las oraciones de `texto` en subtemas y resuelve sus referencias usando
el documento completo. Devuelve solo el JSON.

CRITERIO
Un subtema reúne un asunto y las oraciones que lo detallan, explican,
continúan, contradicen o expresan su consecuencia. Compartir una entidad
no basta para unir asuntos; cambiar de párrafo no basta para separarlos.
Cada oración pertenece a un solo subtema; pueden reunirse oraciones separadas.

REFERENCIAS
- Registra pronombres, posesivos, demostrativos, descripciones y sujetos
  omitidos que necesiten contexto para interpretarse. Para un sujeto
  omitido, cita el verbo.
- Busca el referente en todo el documento, antes o después. No lo elijas
  solo por cercanía. Puede ser una entidad, conjunto, hecho o afirmación.
- Incluye los fragmentos literales numerados que permitan entender y
  comprobar cada resolución dentro de la unidad. Si contienen otras
  referencias, incluye lo necesario para resolverlas. Citar una oración
  como respaldo no cambia su pertenencia.
- Si el referente no se establece, usa null y explica la ambigüedad o falta.
- Conserva alcance, modalidad y atribución. No añadas hechos ni relaciones
  no establecidos. No reescribas las oraciones originales ni extraigas datos.
- Nombra cada subtema diciendo qué se establece y acerca de qué; incorpora
  al nombre los referentes resueltos necesarios para entenderlo.
- Usa referencias: [] cuando no sean necesarias.

FORMATO
{"subtemas":[{
  "subtema":"nombre",
  "oraciones":[n],
  "referencias":[{
    "oracion":n,
    "expresion":"fragmento literal; verbo si el sujeto está omitido",
    "referente":"identificación explícita, o null",
    "respaldo":[{"oracion":n,"texto":"fragmento literal"}],
    "duda":"solo si el referente es null"
  }]
}]}

EJEMPLO 1
Asuntos distintos; referencia entre grupos y sujeto omitido.

Texto:
[1] El observatorio de Cerro Norte abrió en 1982.
[2] Su telescopio principal falló en junio.
[3] Volvió a funcionar en agosto.

{"subtemas":[
  {"subtema":"la apertura del observatorio de Cerro Norte",
   "oraciones":[1],"referencias":[]},
  {"subtema":"la avería y recuperación del telescopio principal del observatorio de Cerro Norte",
   "oraciones":[2,3],
   "referencias":[
     {"oracion":2,"expresion":"Su",
      "referente":"El observatorio de Cerro Norte",
      "respaldo":[
        {"oracion":1,"texto":"El observatorio de Cerro Norte"},
        {"oracion":2,"texto":"Su telescopio principal"}]},
     {"oracion":3,"expresion":"Volvió",
      "referente":"El telescopio principal del observatorio de Cerro Norte",
      "respaldo":[
        {"oracion":1,"texto":"El observatorio de Cerro Norte"},
        {"oracion":2,"texto":"Su telescopio principal falló en junio."},
        {"oracion":3,"texto":"Volvió a funcionar en agosto."}]}
   ]}
]}

EJEMPLO 2
Referencia ambigua: no escoger.

Texto:
[1] Clara habló con Julia después de que ella regresara.

{"subtemas":[
  {"subtema":"la conversación de Clara y Julia después de un regreso",
   "oraciones":[1],
   "referencias":[
     {"oracion":1,"expresion":"ella","referente":null,
      "respaldo":[{"oracion":1,
        "texto":"Clara habló con Julia después de que ella regresara."}],
      "duda":"No se establece si regresó Clara o Julia."}
   ]}
]}

TEXTO
<<<
[1] El molino de viento de la vereda La Esperanza dejó de girar el martes. [2] Su eje se agarrotó después de la tormenta. [3] El molino abastece de agua a doce familias.

[4] La escuela de la vereda tiene 34 alumnos. [5] Su techo se filtró en la misma tormenta. [6] El maestro recogió firmas para pedir materiales.

[7] Según la alcaldía, la tormenta fue la más fuerte del año.
>>>
