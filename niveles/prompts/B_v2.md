Tienes la estructura argumentativa de un texto que no verás: sus conclusiones, garantías y datos, y lo que apoya a cada conclusión. Con base SOLO en ellos:

1. TESIS: la posición central del texto, en una sola oración breve (máximo 25 palabras). Tiene que poder ser discutida; no vale una descripción del tema.
   La tesis dice QUÉ sostiene el autor, no POR QUÉ: no incluyas sus razones, porque ya están en las conclusiones, garantías y datos.
   Ejemplo (de otro texto):
   - mal: "El cierre de bibliotecas perjudica la lectura porque los niños sin libros cerca leen menos y ya cerraron 14."
   - bien: "El cierre de bibliotecas escolares perjudica la formación lectora."
2. Si una de las conclusiones recibidas ya enuncia la tesis, puedes usarla tal cual; indícalo en "coincide_con" con su id. Si no, deja null.
3. PROPÓSITO: en una oración, qué busca el autor con el texto (convencer de, denunciar, explicar, refutar…).
4. Lista qué conclusiones sostienen la tesis y cuáles quedan fuera.
5. Si las conclusiones no convergen en una sola tesis, responde "sin_tesis": true y explica por qué en "nota".
No agregues conocimiento externo.

CONCLUSIONES
{{CONCLUSIONES}}

GARANTÍAS
{{GARANTIAS}}

DATOS
{{DATOS}}

Responde solo con JSON:
{"tesis":"...","coincide_con":null,"proposito":"...","sostenida_por":["C1"],"fuera":["C4"],"sin_tesis":false,"nota":""}
