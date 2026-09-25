Vas a analizar la estructura argumentativa de `texto` según el modelo de Toulmin. Primero divides y clasificas `texto`; al final formulas su tesis.

UNIDAD
`texto` se divide en oraciones: cada oración va desde el inicio, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. Cada oración es un elemento completo: nunca la cortes. Si una oración mezcla funciones, clasifícala por su función principal.
Cada elemento es una cita EXACTA de `texto`, copiada carácter por carácter: sin corregir, sin parafrasear, sin unir oraciones.
El título es una etiqueta, no parte del argumento: clasifícalo como TÍTULO.

FUNCIONES
Cada oración cumple una de estas funciones. Los ejemplos son de otro texto, sobre el agua de un pozo:
- DATO: un hecho que se presenta como evidencia.
  Ej.: "El agua del pozo tiene tres veces el límite de arsénico."
- CONCLUSIÓN: una afirmación que se defiende apoyándose en otras.
  Ej.: "El agua del pozo no es apta para beber."
- GARANTÍA: una regla general que no se prueba con datos.
  Ej.: "El agua que supera el límite de arsénico no es apta para el consumo."
- RESPALDO: evidencia general: un estudio, una norma, la experiencia acumulada.
  Ej.: "La norma sanitaria fija ese límite por el riesgo de cáncer."
- RESERVA: una condición bajo la cual una conclusión no vale.
  Ej.: "Nada de esto aplica si el agua se filtra antes de beberla."
- CONTRAARGUMENTO: una posición contraria que se presenta para rebatirla.
  Ej.: "Algunos vecinos dicen que el agua del pozo siempre se ha bebido sin problemas."
- CONCESIÓN: algo en contra de la propia conclusión que se admite como cierto, sin abandonarla.
  Ej.: "Instalar filtros en cada casa es costoso."
- TÍTULO: el título de `texto`.

CUALIFICADOR Y RESERVA DENTRO DE UNA CONCLUSIÓN
No son elementos aparte. Si una conclusión trae palabras que marcan su fuerza ("probablemente", "casi siempre", "en principio"), cópialas literalmente en su campo "cualificador". Si trae una condición dentro de la misma oración ("a menos que…", "salvo que…", "siempre que…"), copia esa parte literalmente en su campo "reserva". Si no, deja esos campos vacíos.
  Ej.: en "El agua del pozo probablemente no es apta para beber, a menos que se filtre." el cualificador es "probablemente" y la reserva es "a menos que se filtre".

RELACIONES
En "sirve_a" lista los ids de los elementos a los que sirve cada elemento:
- DATO, GARANTÍA y CONCLUSIÓN: las conclusiones que ayudan a sostener, o los contraargumentos que rebaten.
- RESPALDO: las garantías que sostiene.
- RESERVA: las conclusiones que limita.
- CONTRAARGUMENTO y CONCESIÓN: las conclusiones a las que se oponen.
- TÍTULO, o una conclusión que no sostiene a ninguna otra: lista vacía.

REGLAS
1. Todo `texto`, incluido el título, debe quedar asignado a algún elemento, en orden.
2. Clasifica por la función que cada oración cumple en `texto`, no por si es verdadera. No uses conocimiento externo.
3. Si dudas entre dos funciones, marca "duda": true y explica en "nota" en una línea.

TESIS (después de clasificar)
4. Formula tú la tesis: lo que `texto` en su conjunto sostiene, construida a partir de los elementos que clasificaste. Una sola oración de máximo 25 palabras, que pueda ser discutida; no vale una descripción del tema.
5. No copies una conclusión: la tesis es la síntesis de lo que las conclusiones sostienen en conjunto.
6. La tesis dice qué sostiene `texto`, no por qué. No incluyas sus razones: nada de "porque", "ya que", "debido a".
7. En "cercana_a", pon el id de la conclusión cuyo sentido más se parece a tu tesis, o null si ninguna se parece.
8. En "proposito", di en una oración qué busca el autor de `texto` (convencer de, denunciar, explicar, refutar…).
9. En "sostenida_por" y "fuera", lista qué conclusiones sostienen la tesis y cuáles no.
10. Si las conclusiones no convergen en una sola tesis, pon "sin_tesis": true y explica por qué en "nota".

`texto`
<<<
{{TEXTO}}
>>>

Responde solo con JSON, en este orden:
{"elementos":[{"id":"E1","cita":"...","tipo":"titulo|dato|conclusion|garantia|respaldo|reserva|contraargumento|concesion","cualificador":"","reserva":"","sirve_a":["E3"],"duda":false,"nota":""}],
 "tesis":{"texto":"...","cercana_a":"E3","proposito":"...","sostenida_por":["E3"],"fuera":[],"sin_tesis":false,"nota":""}}
