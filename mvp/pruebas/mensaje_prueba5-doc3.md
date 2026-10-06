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
PROMPT (verbatim de `mvp/pruebas/prompt_v7.md`, con `{{TEXTO_NUMERADO}}` ya sustituido;
esto es exactamente lo que recibe el modelo cuando corre
`python3 unidades/extraer_unidades.py`)
---------------------------------------------------------------------

TAREA
Agrupa las oraciones de `texto` en subtemas, según las definiciones y los
ejemplos. Después, conserva ese agrupamiento y añade a cada subtema las
aclaraciones necesarias para interpretar sus referencias externas.
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

PROCEDIMIENTO
1. Decide primero los subtemas por asunto, aplicando las definiciones y
   los ejemplos anteriores.
2. Revisa después cada subtema como si fuera a leerse por separado.
   Si una referencia necesita un antecedente de otro subtema, aclárala
   usando el documento completo.
3. Añade la aclaración sin mover, añadir ni quitar oraciones de los grupos.
   Una referencia compartida no es motivo para fusionar asuntos.
4. Ajusta el nombre del subtema cuando la aclaración permita identificar
   mejor de qué trata. El nombre no tiene que resumir todos sus detalles.

ALCANCE
- Revisa pronombres, posesivos, demostrativos, sujetos omitidos y expresiones
  como «el mismo», «el anterior» o «este último». Incluye otras expresiones
  solo cuando necesiten un antecedente externo para identificar su referente.
- No registres referencias que ya se entiendan dentro del propio subtema.
- Resolver es recuperar una identificación dada por el texto, no completar
  la descripción de una entidad. «Según la alcaldía» puede conservarse como
  fuente aunque el documento no diga su municipio.
- Si hay varios antecedentes posibles o falta uno necesario, no elijas:
  registra la referencia como no resuelta.
- No deduzcas identidades solo por cercanía, género gramatical o conocimiento
  general. Conserva las distinciones, la incertidumbre y la atribución del texto.

REGISTRO
Cada subtema añade `referencias`, vacía cuando no necesita aclaraciones.

Para cada referencia externa:
- `oracion`: número de la oración que contiene la referencia.
- `expresion`: expresión literal; para un sujeto omitido, el verbo.
- `referente`: identificación explícita recuperada del documento, o null.
- `respaldo`: fragmentos literales con sus números de oración, suficientes
  para comprobar la identificación. Incluye la expresión referida y su
  antecedente. Si este depende de otro antecedente, incluye también ese
  enlace; detente cuando la identificación quede explícita.
- `duda`: solo cuando `referente` sea null; indica qué no puede resolverse.

El respaldo queda dentro del registro del subtema, aunque proceda de otro.
No cambia la pertenencia de las oraciones ni sustituye su texto original.

EJEMPLO ADICIONAL
La apertura y el horario son asuntos distintos sobre la misma biblioteca.
El posesivo se resuelve citando el antecedente, sin cambiar los grupos.
La referencia ambigua permanece abierta.

Texto:
[1] La biblioteca del barrio Los Olmos abrió en 1998.
[2] Su horario de atención termina a las seis.
[3] Clara habló con Julia después de que ella regresara.

{
  "subtemas": [
    {
      "subtema": "la apertura de la biblioteca del barrio Los Olmos",
      "oraciones": [1],
      "referencias": []
    },
    {
      "subtema": "el horario de atención de la biblioteca del barrio Los Olmos",
      "oraciones": [2],
      "referencias": [
        {
          "oracion": 2,
          "expresion": "Su",
          "referente": "La biblioteca del barrio Los Olmos",
          "respaldo": [
            {"oracion": 1, "texto": "La biblioteca del barrio Los Olmos"},
            {"oracion": 2, "texto": "Su horario de atención"}
          ]
        }
      ]
    },
    {
      "subtema": "la conversación de Clara y Julia después de un regreso",
      "oraciones": [3],
      "referencias": [
        {
          "oracion": 3,
          "expresion": "ella",
          "referente": null,
          "respaldo": [
            {
              "oracion": 3,
              "texto": "Clara habló con Julia después de que ella regresara."
            }
          ],
          "duda": "No se establece si regresó Clara o Julia."
        }
      ]
    }
  ]
}

SALIDA
Usa la estructura del ejemplo adicional para todos los subtemas.
Devuelve únicamente el JSON.

`texto`
<<<
[1] El programa de comedores comunitarios de la provincia abrió su primera sede en 2015. [2] Hoy funciona en dieciocho municipios con sesenta y cuatro comedores. [3] Atiende a unos nueve mil usuarios diarios, según la secretaría de bienestar.

[4] La universidad departamental evaluó el programa entre 2023 y 2025. [5] Su informe midió la asistencia y el estado nutricional de los usuarios. [6] Encontró que la asistencia creció un doce por ciento en el período. [7] No encontró cambios en el estado nutricional.

[8] La secretaría de bienestar cuestionó esa conclusión. [9] Sostiene que las mediciones se hicieron solo en dos municipios. [10] El equipo de la universidad respondió que esos dos municipios se eligieron por sorteo. [11] La discusión sigue abierta.

[12] En marzo, la asamblea provincial aprobó ampliar el programa a seis municipios más. [13] La ampliación depende de un convenio que aún no se firma. [14] El convenio compromete recursos de la provincia y de los municipios. [15] La interventora y la secretaria revisaron el borrador en junio. [16] Ella pidió incluir una cláusula de salida. [17] Su firma quedó pendiente hasta después de las elecciones de octubre.
>>>
