#!/usr/bin/env python3
"""Inserta la sección del encargo en la memoria y ajusta el pendiente 0. Idempotente."""
import pathlib

RUTA = pathlib.Path("mvp/memoria de trabajo y pendientes.md")
texto = RUTA.read_text(encoding="utf-8")

SECCION = """## Encargo a otro modelo: documentos y baterías de preguntas para la etapa 2 (10-10)

**Qué se está decidiendo.** Con qué modelo y qué esfuerzo se corre la **etapa 2** —DATOS: de cada
unidad temática salen datos `aspecto` · `valor` · `unidad_valor`—. Las corridas de prueba viven en el
scratch `temp/datos-test/` y **no tocan la base**.

**La vara, y lo que no es la vara.** Una unidad es adecuada para una pregunta si **leer su caso y sus
datos reduce el conjunto de respuestas admisibles** a esa pregunta. No se puntúa por conteo de datos,
ni por si la extracción conservó las palabras o los constituyentes de la oración: una paráfrasis que
pierde palabras puede responder, y una transcripción fiel puede no responder nada. Toda la comparación
entre modelos del 10-10 se hizo con conteo de datos y listas de aspectos esperados, así que **hay que
rehacerla con preguntas** y las conclusiones de `mvp/proveedores.md` §2 quedan pendientes de
re-puntuación. Las 29 corridas sobre `preparacion_cafe` están en disco con sus salidas completas:
re-puntuar no cuesta llamadas nuevas, lo que falta es la batería.

**El encargo.** (a) Escribir documentos de trabajo para el corpus, al estilo de
`mvp/documentos/preparacion_cafe.md` —prosa expositiva de cuatro párrafos, con cantidades, unidades de
medida, comparaciones, pronombres con antecedente y modificadores incrustados en el sujeto—. (b)
Escribir para cada documento una batería de preguntas **que el documento sí responda**, tres o cuatro
por unidad.

**La restricción que hace válida la batería: a ciegas.** Las preguntas se escriben **viendo solo el
documento** —y, si hace falta, los nombres de los casos—, **nunca las extracciones**. Quien las
escriba después de leer las salidas redacta preguntas que ya sabe si pasan o fallan, y la batería
queda viciada (*HARKing*: formular la hipótesis después de conocer el resultado). Por eso quien
escribe las preguntas no es quien puntúa.

**Dónde vive qué.** Documentos: `mvp/documentos/`. Prompts de trabajo: `mvp/prompts/`, cada uno en dos
bloques, `[SISTEMA]` lo invariante y `[TAREA]` el material. El prompt de DATOS que se está probando es
el scratch `temp/prompt_DATOS_v1.md`. Crudos de las pruebas: `temp/datos-test/*.json`. Baterías de
consulta del MVP: `mvp/consulta/preguntas_<doc>.md`.

**Cómo se lanzan los modelos.** Las claves viven en `~/.bashrc`; los shells no interactivos no las
cargan, así que **todo va con `bash -ic '…'`**. Los guiones son idempotentes: si el crudo existe no
vuelven a llamar, y una réplica nueva lleva un `rN` nuevo.

- Etapa 1 (UT), escribe en la base: `python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--esfuerzo E] [--prompt UT] [--rehacer]`
- Etapa 2 (DATOS), escribe en la base: `python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--esfuerzo E] [--rehacer]`
- Etapa 2 en seco, **no toca la base**: `python3 temp/datos-test/paso2_seco_v1.py <doc> <alias> <esfuerzo> <rN>`
- Etapa 2 en seco por la familia `responses` de OpenCode Go: `python3 temp/datos-test/paso2_seco_v1_luna.py <doc> <modelo> <esfuerzo> <rN>`

**Modelos disponibles.** Los alias del registro (`mvp/código/proveedores/__init__.py`): `deepseek`
(deepseek-flash), `glm` (glm-5.3-flash), `haiku` (claude-haiku-5-5) y `grok` (sin créditos de xAI).
Esfuerzos: `low`, `medium`, `high`, `xhigh`, `max`. Por **OpenCode Go** (clave `OPENCODE_API_KEY`, base
`https://opencode.ai/zen/go/v1/`) hay tres familias y cada modelo usa una sola: `chat/completions`
(deepseek, glm, kimi, mimo, longcat…), `messages` (claude-haiku-5-5, minimax, qwen) y `responses`
(gpt-6-luna, grok, muse-spark). `gpt-6-luna` admite `none`, `low`, `medium`, `high`, `xhigh` y `max`,
con defecto `medium`; la familia `responses` devuelve otra forma —`output[].content[].text`— y por eso
tiene corredor aparte. **Muse Spark entrena con los prompts: no se usa.**

**Lo abierto.** Si la unidad de puntuación es la UT por separado —suficiencia local— o el documento
entero, donde una pregunta puede quedar respondida por datos de dos unidades, que es el caso
interesante del faro. Decidirlo antes de puntuar.

"""

ANCLA = "## 3. Pendientes vigentes"
if "## Encargo a otro modelo" not in texto:
    assert ANCLA in texto, "no encontré el ancla de pendientes"
    texto = texto.replace(ANCLA, SECCION + ANCLA, 1)

VIEJO = """sigue **DATOS** (`paso2_datos.py preparacion_cafe`) —corre
   contra la API real y escribe en la base—,"""
NUEVO = """sigue **DATOS** (`paso2_datos.py preparacion_cafe`) —corre
   contra la API real y escribe en la base; **espera la elección de modelo y esfuerzo**, ver
   «Encargo a otro modelo»—,"""
if NUEVO not in texto:
    assert VIEJO in texto, "no encontré el texto del pendiente 0"
    texto = texto.replace(VIEJO, NUEVO, 1)

RUTA.write_text(texto, encoding="utf-8")
print("listo")
