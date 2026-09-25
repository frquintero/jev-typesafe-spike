Vas a analizar la estructura argumentativa del TEXTO según el modelo de Toulmin. Primero divides y clasificas el texto; al final formulas su tesis.

UNIDAD
El texto se divide en oraciones: cada oración va desde el inicio del texto, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. Cada oración es un elemento completo: nunca la cortes. Si una oración mezcla funciones, clasifícala por su función principal.
Cada elemento es una cita EXACTA del texto, copiada carácter por carácter: sin corregir, sin parafrasear, sin unir oraciones.
El título es una etiqueta, no parte del argumento: clasifícalo como TÍTULO.

FUNCIONES
Cada oración cumple una de estas funciones. Los ejemplos son de otro texto, sobre el agua de un pozo:
- DATO: el hecho del que se parte; la evidencia.
  Ej.: "El agua del pozo tiene tres veces el límite de arsénico."
- CONCLUSIÓN: lo que el texto quiere establecer.
  Ej.: "El agua del pozo no es apta para beber."
- GARANTÍA: la regla que autoriza a pasar del dato a la conclusión. Responde: ¿qué te permite concluir eso?
  Ej.: "El agua que supera el límite de arsénico no es apta para el consumo."
- RESPALDO: lo que sostiene a la garantía: una norma, un estudio, la experiencia. Responde: ¿y por qué vale esa regla?
  Ej.: "La norma sanitaria fija ese límite por el riesgo de cáncer."
- RESERVA: una oración que establece las condiciones bajo las cuales una conclusión no vale.
  Ej.: "Nada de esto aplica si el agua se filtra antes de beberla."
- CONTRAARGUMENTO: una posición o explicación contraria que el texto presenta para rebatirla.
  Ej.: "Algunos vecinos dicen que el agua del pozo siempre se ha bebido sin problemas."
- CONCESIÓN: algo en contra de la propia conclusión que el texto admite como cierto, sin abandonar la conclusión.
  Ej.: "Instalar filtros en cada casa es costoso."
- TÍTULO: el título del texto.
- OTRO: no cumple ninguna de las funciones anteriores.

CUALIFICADOR Y RESERVA DENTRO DE UNA CONCLUSIÓN
No son elementos aparte. Si una conclusión trae palabras que marcan su fuerza ("probablemente", "casi siempre", "en principio"), cópialas literalmente en su campo "cualificador". Si trae una condición de excepción dentro de la misma oración ("a menos que…", "salvo que…"), copia esa parte literalmente en su campo "reserva". Si no, deja esos campos vacíos.
  Ej.: en "El agua del pozo probablemente no es apta para beber, a menos que se filtre." el cualificador es "probablemente" y la reserva es "a menos que se filtre".

Para distinguir CONCLUSIÓN de GARANTÍA no te fijes en si la frase es general o particular:
- si el texto ofrece datos para sostenerla, es CONCLUSIÓN;
- si el texto la usa como puente sin ofrecer datos para ella, es GARANTÍA.

RELACIONES
En "sirve_a" lista los ids de los elementos a los que sirve cada elemento:
- DATO, GARANTÍA y CONCLUSIÓN: las conclusiones que ayudan a sostener, o los contraargumentos que rebaten.
- RESPALDO: las garantías que sostiene.
- RESERVA: las conclusiones que limita.
- CONTRAARGUMENTO y CONCESIÓN: las conclusiones a las que se oponen.
- TÍTULO, OTRO, o una conclusión que no sostiene a ninguna otra: lista vacía.

REGLAS
1. Todo el texto, incluido el título, debe quedar asignado a algún elemento, en orden.
2. Clasifica por la función que cada oración cumple en este texto, no por si es verdadera. No uses conocimiento externo.
3. Si dudas entre dos funciones, marca "duda": true y explica en "nota" en una línea.

TESIS (después de clasificar)
4. Formula tú la tesis: lo que el texto en su conjunto sostiene, construida a partir de los elementos que clasificaste. Una sola oración de máximo 25 palabras, que pueda ser discutida; no vale una descripción del tema.
5. No copies una conclusión: la tesis es la síntesis de lo que las conclusiones sostienen en conjunto.
6. La tesis dice qué sostiene el texto, no por qué. No incluyas sus razones: nada de "porque", "ya que", "debido a".
7. En "cercana_a", pon el id de la conclusión cuyo sentido más se parece a tu tesis, o null si ninguna se parece.
8. En "proposito", di en una oración qué busca el autor con el texto (convencer de, denunciar, explicar, refutar…).
9. En "sostenida_por" y "fuera", lista qué conclusiones sostienen la tesis y cuáles no.
10. Si las conclusiones no convergen en una sola tesis, pon "sin_tesis": true y explica por qué en "nota".

TEXTO
<<<
{{TEXTO}}
>>>

Responde solo con JSON, en este orden:
{"elementos":[{"id":"E1","cita":"...","tipo":"titulo|dato|conclusion|garantia|respaldo|reserva|contraargumento|concesion|otro","cualificador":"","reserva":"","sirve_a":["E3"],"duda":false,"nota":""}],
 "tesis":{"texto":"...","cercana_a":"E3","proposito":"...","sostenida_por":["E3"],"fuera":[],"sin_tesis":false,"nota":""}}
