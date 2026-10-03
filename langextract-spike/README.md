# LangExtract — frente de pruebas

Abierto y **cerrado el 2026-10-03: evaluado, no adoptado** (ver «Lección
aprendida»). Exploró si **LangExtract** sirve para la capa de datos de
Zettel: extraer lo que un texto establece y anclarlo al lugar exacto de
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

**Reparto de trabajo (hipótesis de partida, descartada).** LangExtract pone
la maquinaria de extracción, más sofisticada que nuestro código: trozos,
paralelo, varias pasadas, ubicación de cada extracción en el texto,
conectores, visualización. Nosotros ponemos
el **contrato** (qué es caso de estudio, capa, condición, dato: el marco y
`definiciones-del-marco.md`, que entran por la instrucción y los ejemplos) y
la **manera de medir** (crudos únicos, réplicas, preguntas fijadas antes de
correr). La calidad del modelo no la resuelve el código.

## Lección aprendida

Evaluado leyendo su código y su documentación (v1.7.0, instalada en
`~/.local/share/lx-spike/venv`), sin llamadas a modelos.

- **Para qué sirve:** extracciones locales (entidades, atributos, citas
  textuales) en textos largos, donde lo buscado cabe en un pedazo de texto
  y basta con no omitirlo.
- **Por qué no sirve para lo nuestro:** su unidad es el **trozo**, definido
  por tamaño (`max_char_buffer`, 1000 caracteres por defecto); cada trozo
  se procesa con la misma instrucción. Nuestro objetivo es estructura
  semántica: quién sostiene qué, la identidad del caso, cómo se desarrolla
  una idea a lo largo de varias oraciones. Eso exige unidades de sentido
  (unidad temática v1), no de tamaño. En biomar1, un trozo tocaba cuatro
  subtemas y el subtema 3 quedaba repartido entre trozos.
- **Lo demás tampoco lo compensa:** el contexto entre trozos se limita a la
  cola del trozo anterior (`context_window_chars`, apagado por defecto); las
  pasadas repiten la misma instrucción y se queda con lo primero que
  encontró; la salida es plana (clase, texto, atributos), sin
  identificadores ni relaciones entre extracciones.
- **La lección:** «estructurado» no es solo tener campos (forma); es tener
  lógica semántica. Antes de adoptar una herramienta, mirar qué unidad de
  texto usa y si coincide con la nuestra.

Ideas rescatables: anotadas en el `README.md` de la raíz.

## Estado

Cerrado. Las tres tareas de `tareas.md` quedan abandonadas.

## Referencias

- [Repositorio](https://github.com/google/langextract)
- [Presentación de Google](https://developers.googleblog.com/en/introducing-langextract-a-gemini-powered-information-extraction-library/)
