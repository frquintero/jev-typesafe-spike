Vas a analizar la estructura argumentativa del TEXTO según el modelo de Toulmin. Primero divides y clasificas el texto; al final formulas su tesis.

UNIDAD
El texto se divide en oraciones: cada oración va desde el inicio del texto, o desde un punto, signo de interrogación o de exclamación, hasta el siguiente. El título cuenta como una oración. Cada oración es un elemento, salvo que contenga partes con funciones distintas: entonces se corta en una parte por función.
Cada elemento es una cita EXACTA del texto, copiada carácter por carácter: sin corregir, sin parafrasear, sin unir partes separadas.

FUNCIONES
Cada elemento cumple una de estas funciones. Los ejemplos son de otro texto, sobre el agua de un pozo:
- DATO: el hecho del que se parte; la evidencia.
  Ej.: "El agua del pozo tiene tres veces el límite de arsénico."
- CONCLUSIÓN: lo que el texto quiere establecer.
  Ej.: "El agua del pozo no es apta para beber."
- GARANTÍA: la regla que autoriza a pasar del dato a la conclusión. Responde: ¿qué te permite concluir eso?
  Ej.: "El agua que supera el límite de arsénico no es apta para el consumo."
- RESPALDO: lo que sostiene a la garantía: una norma, un estudio, la experiencia. Responde: ¿y por qué vale esa regla?
  Ej.: "La norma sanitaria fija ese límite por el riesgo de cáncer."
- RESERVA: las condiciones bajo las cuales la conclusión no vale.
  Ej.: "a menos que se filtre antes de beberla."
- OTRO: no cumple ninguna de las funciones anteriores.

CUALIFICADOR: la fuerza con que se afirma una conclusión ("probablemente", "casi siempre", "en principio"). No es un elemento aparte: si una conclusión lo trae, copia esas palabras literalmente en su campo "cualificador"; si no, déjalo vacío.
  Ej.: en "El agua del pozo probablemente no es apta para beber", el cualificador es "probablemente".

Para distinguir CONCLUSIÓN de GARANTÍA no te fijes en si la frase es general o particular:
- si el texto ofrece datos para sostenerla, es CONCLUSIÓN;
- si el texto la usa como puente sin ofrecer datos para ella, es GARANTÍA.

RELACIONES
En "sirve_a" lista los ids de los elementos a los que sirve cada elemento:
- DATO, GARANTÍA y CONCLUSIÓN: las conclusiones que ayudan a sostener.
- RESPALDO: las garantías que sostiene.
- RESERVA: las conclusiones que limita.
- OTRO, o una conclusión que no sostiene a ninguna otra: lista vacía.

REGLAS
1. Los conectores (sin embargo, por eso, además, mientras tanto, porque, como…) van pegados a la parte que introducen.
2. Todo el texto, incluido el título, debe quedar asignado a algún elemento, en orden.
3. Clasifica por la función que cada elemento cumple en este texto, no por si es verdadero. No uses conocimiento externo.
4. Si dudas entre dos funciones, marca "duda": true y explica en "nota" en una línea.

TESIS (después de clasificar)
5. Formula tú la tesis: lo que el texto en su conjunto sostiene, construida a partir de los elementos que clasificaste. Una sola oración de máximo 25 palabras, que pueda ser discutida; no vale una descripción del tema.
6. No copies una conclusión: la tesis es la síntesis de lo que las conclusiones sostienen en conjunto.
7. La tesis dice qué sostiene el texto, no por qué. No incluyas sus razones: nada de "porque", "ya que", "debido a".
8. En "cercana_a", pon el id de la conclusión cuyo sentido más se parece a tu tesis, o null si ninguna se parece.
9. En "proposito", di en una oración qué busca el autor con el texto (convencer de, denunciar, explicar, refutar…).
10. En "sostenida_por" y "fuera", lista qué conclusiones sostienen la tesis y cuáles no.
11. Si las conclusiones no convergen en una sola tesis, pon "sin_tesis": true y explica por qué en "nota".

TEXTO
<<<
{{TEXTO}}
>>>

Responde solo con JSON, en este orden:
{"elementos":[{"id":"E1","cita":"...","tipo":"dato|conclusion|garantia|respaldo|reserva|otro","cualificador":"","sirve_a":["E3"],"duda":false,"nota":""}],
 "tesis":{"texto":"...","cercana_a":"E3","proposito":"...","sostenida_por":["E3"],"fuera":[],"sin_tesis":false,"nota":""}}
