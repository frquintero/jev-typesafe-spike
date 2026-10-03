# LangExtract — frente de pruebas

Abierto el 2026-10-03. Explora si **LangExtract** sirve para la capa de datos
de Zettel: extraer lo que un texto establece y anclarlo al lugar exacto de
donde sale. Subproyecto independiente; aplican `AGENTS.md` y
`definiciones-del-marco.md` (raíz).

## Qué es LangExtract

Biblioteca de Python de Google, de código abierto (Apache 2.0), que usa un
modelo de lenguaje para sacar información estructurada de un texto.

- **Entrada:** una instrucción corta, uno o varios **ejemplos resueltos** y el
  texto a procesar.
- **Salida:** cada extracción con su clase, su **texto literal** y atributos
  libres, más su **intervalo de caracteres** en el texto original. Si algo no
  puede ubicarse literalmente, el intervalo queda vacío.
- **Textos largos:** los parte en trozos (`max_char_buffer`), los procesa en
  paralelo (`max_workers`) y puede hacer varias pasadas para reducir
  omisiones (`extraction_passes`).
- **Revisión:** genera una página HTML con cada extracción resaltada en el
  texto.
- **Modelos:** Gemini por defecto; también OpenAI, Ollama (local) y servicios
  compatibles con la API de OpenAI.

**Es código, y se puede modificar.** Licencia Apache 2.0: se puede usar,
modificar y redistribuir conservando el aviso de licencia y señalando los
cambios. Tres niveles, de menos a más intrusivo: configurarlo (instrucción,
ejemplos, modelo, trozos, pasadas); extenderlo desde nuestro repo (por
ejemplo, un proveedor propio para DeepSeek con streaming y razonamiento); o
copiarlo y cambiar su código (*fork*), con el mantenimiento a nuestro cargo.

**Reparto de trabajo.** LangExtract pone la maquinaria de extracción, más
sofisticada que nuestro código: trozos, paralelo, varias pasadas, ubicación
de cada extracción en el texto, conectores, visualización. Nosotros ponemos
el **contrato** (qué es caso de estudio, capa, condición, dato: el marco y
`definiciones-del-marco.md`, que entran por la instrucción y los ejemplos) y
la **manera de medir** (crudos únicos, réplicas, preguntas fijadas antes de
correr). La calidad del modelo no la resuelve el código.

## Estado

Ver `tareas.md`. Tres preguntas, en orden: ¿funciona con nuestro modelo?,
¿representa nuestro contrato?, ¿gana algo frente a la ficha?

## Referencias

- [Repositorio](https://github.com/google/langextract)
- [Presentación de Google](https://developers.googleblog.com/en/introducing-langextract-a-gemini-powered-information-extraction-library/)
