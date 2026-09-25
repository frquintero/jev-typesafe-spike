Vas a analizar la estructura argumentativa del TEXTO. No resumas ni interpretes: solo cita y clasifica. Un programa verificará que cada cita aparezca literalmente en el texto.

TIPOS
- DATO: un hecho particular que el texto presenta como evidencia: cifra, fecha, caso, observación, resultado de una fuente o cita de otro autor.
- CONCLUSIÓN: lo que el autor sostiene sobre el asunto del texto: juicio, valoración, diagnóstico, predicción o recomendación. Se apoya en datos, en garantías o en otras conclusiones.
- GARANTÍA: un principio general que el autor usa para pasar de los datos a una conclusión. Vale más allá de este caso y normalmente no se apoya en datos del texto.
- OTRO: lo que no afirma nada: fórmulas, frases de relleno.

Para distinguirlos: si informa un hecho particular, es DATO. Si enuncia una regla general que conecta datos con una conclusión, es GARANTÍA. Si valora o diagnostica este caso concreto, o recomienda algo sobre él, es CONCLUSIÓN.

REGLAS
1. Cada elemento es una cita EXACTA del TEXTO, copiada carácter por carácter. No corrijas, no parafrasees, no unas fragmentos separados.
2. Una oración puede contener dos tipos. En ese caso, córtala en dos citas.
   Ejemplo: "Como el 40% de los contratos se adjudicó sin licitación, el proceso es opaco"
   → DATO: "Como el 40% de los contratos se adjudicó sin licitación," / CONCLUSIÓN: "el proceso es opaco"
3. Los conectores (sin embargo, por eso, además, mientras tanto, porque, como…) van pegados al fragmento que introducen. No los cites aparte.
4. Todo el texto debe quedar asignado a algún elemento, en orden. El título también se clasifica por su función: si enuncia una posición, es CONCLUSIÓN.
5. Clasifica por la función que el fragmento cumple EN ESTE TEXTO, no por si es verdadero. No uses conocimiento externo.
6. Si dudas entre dos tipos, marca "duda": true y explica en "nota" en una línea.
7. Para cada CONCLUSIÓN, lista en qué se apoya dentro del texto: datos, garantías y otras conclusiones. Puede no apoyarse en nada.

EJEMPLO (de otro texto, solo para ilustrar los tipos)
"El año pasado cerraron 14 bibliotecas escolares en la región. Un niño que no tiene libros cerca lee menos. Por eso, el cierre perjudica la formación lectora."
→ E1 DATO: "El año pasado cerraron 14 bibliotecas escolares en la región."
→ E2 GARANTÍA: "Un niño que no tiene libros cerca lee menos."
→ E3 CONCLUSIÓN: "Por eso, el cierre perjudica la formación lectora." — se apoya en E1 (dato) y E2 (garantía).

TEXTO
<<<
{{TEXTO}}
>>>

Responde solo con JSON:
{"elementos":[{"id":"E1","cita":"...","tipo":"dato|conclusion|garantia|otro","duda":false,"nota":""}],
 "apoyos":[{"conclusion":"E3","datos":["E1"],"garantias":["E2"],"conclusiones":[]}]}
