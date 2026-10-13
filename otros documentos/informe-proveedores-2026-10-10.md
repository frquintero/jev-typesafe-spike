# Informe de proveedores del MVP — comparación de modelos y medidas (10-10-2026)

**Qué es esto.** Las pruebas comparativas de modelos que se hicieron para el MVP de Zettel: qué se
midió, con qué corredores, qué costó y qué defectos se vieron. Se mudó acá el 13-10-2026 desde
`mvp/proveedores.md`, que quedó como el mapa de los alias vivos: **las cifras son las del día en que
se midieron y no se reescriben**; lo que se decidió a partir de ellas vive en su sitio (la base, la
memoria, el diseño).

**De dónde salen.** De corridas del 09-10 y el 10-10-2026 sobre `preparacion_cafe` (5 UT), con el
prompt experimental `temp/prompt_DATOS_v1.md` y los corredores en seco de `temp/datos-test/`, **sin
escribir en la base**. Los crudos y los corredores viven en el scratch `temp/`, que **no se
versiona** (memoria, pendiente 11): de aquella evidencia solo queda este informe.

Las secciones y los números de sección son los del documento original: DATOS (§1), GLM (§2),
Luna (§3) y MiMo (§4).

---

## 1. Etapa 2 (extracción de DATOS): resultados de las pruebas

**Aviso (10-10): las columnas «Cobertura» y «Estabilidad» de §1.1 se puntuaron por conteo de datos y
por una lista de aspectos esperados, y esa no es la vara del proyecto** —la vara es si el caso y sus
datos bastan para responder una pregunta—. Quedan pendientes de re-puntuación con una batería de
preguntas escrita a ciegas de las extracciones (pendiente 17 en
`mvp/memoria de trabajo y pendientes.md`); el costo y el tiempo sí son medidas directas y se
sostienen. El default es configurable —vive en la base—, pero elegirlo por calidad sin re-puntuar
sigue siendo elegir a ciegas.

### 1.1 Qué se probó

Todas las pruebas corrieron sobre el mismo documento (`preparacion_cafe`, 5 UT) y el mismo prompt
experimental (`temp/prompt_DATOS_v1.md`, nunca versionado al repo), en modo solo lectura
(`temp/datos-test/paso2_seco_v1.py` y sus variantes), sin escribir en la base. Se midió cobertura
de aspectos esperados (sobre 5), estabilidad entre réplicas, costo y tiempo de respuesta.

| Modelo / esfuerzo | Cobertura | Estabilidad | Costo aprox. (USD) | Tiempo aprox. |
|---|---|---|---|---|
| DeepSeek-flash, low | 5/5 | estable en 2 réplicas | 0.004–0.006 | 22–32 s |
| Sonnet 5.5, sin razonamiento / low | 4/5 (falta «fundamental») | estable | 0.020–0.025 | ~10 s (el más rápido) |
| GLM-5.3-Flash, max | 3.5–5/5 | variable | 0.003–0.005 | 48–104 s (muy variable) |
| Haiku 5.5, high | 1.5–3/5 | muy variable en 4 réplicas («muy versátil» nunca se cubrió) | ~0.002 (el más barato) | ~11–13 s |
| Haiku 5.5, max | 5/5 | estable | ~0.022 (13× más que high) | 143–166 s |

GLM-5.3-Flash en `low` y `high` no se incluye en la tabla de cobertura porque en esos niveles no
razona (ver §2): las pruebas de cobertura de GLM se hicieron en `max`, el único nivel en el que el
modelo piensa de forma consistente el 10-10-2026.

### 1.2 Por qué DeepSeek-flash low

Ningún candidato domina en los tres ejes (efectividad, costo, rapidez) a la vez; es una frontera de
Pareto, no un ganador absoluto:

- **Sonnet 5.5 sin razonamiento** es el más rápido y con aspectos mejor redactados, pero cuesta
  4–6× más que DeepSeek y no cubre el aspecto «fundamental» de forma estable.
- **Haiku max** llega a cobertura completa, pero a 13× el costo de Haiku high y 5–7× el tiempo de
  DeepSeek: no compensa frente a DeepSeek low para un MVP que corre muchas UT.
- **GLM max** es barato pero con tiempo muy variable (48–104 s) y cobertura inestable.
- **DeepSeek-flash low** pasa el piso de cobertura exigido (5/5, estable en las réplicas hechas) al
  costo y tiempo más razonables de todos los candidatos que lo pasan. Es la opción por defecto
  mientras no se sumen más réplicas que cambien esta lectura.

Nota de alcance: todas las conclusiones de cobertura/estabilidad se basan en pocas réplicas (2–4)
sobre un solo documento; no se generalizan sin pruebas adicionales.

## 2. Discrepancia observada en GLM-5.3-Flash (z.ai)

La documentación de z.ai dice que el razonamiento no se puede apagar (`thinking.type` solo admite
`enabled`, que es el valor por defecto), que «GLM-5.3 y GLM-5.3-FLASH siempre piensan cuando está
habilitado» y que `reasoning_effort` admite `low` / `high` / `max` (por defecto y recomendado:
`max`).

Lo observado NO coincide con eso:

- **09-10-2026:** sobre doc10 (prompt DATOS v7), `low` razonó 516 y 877 tokens; `high`, 4.921 y
  6.401.
- **10-10-2026:** `low` devolvió `reasoning_tokens: 0` y sin `reasoning_content` en todas las
  pruebas —el café con DATOS v1 (system + user, un solo mensaje, y con `thinking: enabled`
  explícito), doc10 repetido con v7, y «qué es una variable en python», también por `curl` directo
  con `max_tokens` 256 y 8.000—; `high` dio 0 en la pregunta y 5 tokens en el café («Extract data
  per UT.»); solo `max` razonó (298 a 472 tokens en la pregunta, 3.088 en el café). La API aceptó
  los tres niveles (HTTP 200).

El transporte no es la causa: el `curl` directo da lo mismo. Si se quiere razonamiento de GLM, hay
que pedir `max` explícito; con el `low` de este alias, el 10-10-2026 no razona.

Esta nota vivía como comentario en `mvp/código/proveedores/__init__.py`, junto al alias `glm`; ahí
queda el puntero a esta sección.

## 3. GPT 6 Luna por OpenCode Go: contrato, costo y medidas (10-10)

**Modelo válido para la etapa 2**, con las pruebas de forma hechas y las de calidad pendientes.

**Ruta.** `POST https://opencode.ai/zen/go/v1/responses`, familia `responses` (Responses API de
OpenAI), clave `OPENCODE_API_KEY` en `Authorization: Bearer`. Go pide `User-Agent` propio y un
`x-opencode-session` estable por conversación. La clave vive en
`~/.config/opencode-console/api_key.env`, que `~/.bashrc` carga: **correr con `bash -ic '…'`**.

**Corredor aparte, y por qué.** `temp/datos-test/paso2_seco_v1_luna.py <doc> <modelo> <esfuerzo> <rN>`
—misma base en solo lectura, mismas unidades, mismo `temp/prompt_DATOS_v1.md`, misma verificación con
`forma()`, sin escribir en la base—. Hace falta porque esta familia devuelve otra forma:
`output[].content[].text` y `usage.input_tokens` / `output_tokens_details.reasoning_tokens`, no
`choices[0].message`; `openai_compatible` no la parsea. El `[SISTEMA]` va como `instructions` y el
`[TAREA]` como `input`. **Adoptado:** el transporte propio está en
`mvp/código/proveedores/openai_responses.py` (`21be6b1`, y manda `tools` desde `06931d6`), el alias
es `luna` en `ALIAS`, y por ahí va el ORQ.

**Esfuerzos: `none`, `low`, `medium`, `high`, `xhigh`, `max`.** Lo dijo la propia API al rechazar
`minimal` con HTTP 400 y enumerar los válidos; la documentación de Go no documenta el parámetro.
**El defecto es `medium`** (la respuesta devuelve `reasoning: {effort: "medium", mode: "standard",
context: "all_turns"}` cuando no se manda). Nuestros cinco esfuerzos pasan **1:1** a
`reasoning.effort`, sin tabla de traducción, y además ofrece `none`: acá el razonamiento **sí** se
puede apagar, al contrario de GLM (§2). Otras perillas que la respuesta devuelve y no hemos tocado:
`text.verbosity`, `reasoning.mode`, `reasoning.summary`.

**Precio, cupo y retención** (página de Go, 10-10-2026). Entrada US$0.10/1M hasta 272K de contexto y
US$0.20/1M por encima; salida US$0.50 y US$0.75; **lectura de caché US$0.01/1M**. Cupo de US$15/mes en
el plan Go, que por esos precios da del orden de 21.000 peticiones al mes según la estimación de la
propia página: **el US$15 es poco precio, no poco cupo**. No se usa para entrenar; retiene 30 días.

**El caché funciona por `instructions`.** `prompt_cache_retention` es de 24 h, y como el `[SISTEMA]` es
invariante, la segunda llamada cacheó **1.839 de 1.842** tokens de entrada. En una fase de extracción
sobre muchos documentos con el mismo prompt, el costo de entrada casi desaparece.

**Medido sobre `preparacion_cafe`** (5 UT, `temp/prompt_DATOS_v1.md`), cuatro corridas:

| esfuerzo | tiempo | costo (USD) | razonamiento | forma |
|---|---|---|---|---|
| `low` ×2 | 8,4 s · 11,3 s | 0.00081 · 0.00076 | 132 · 275 tok | parseo ok, 0 problemas, 0 avisos |
| `high` ×2 | 23,0 s · 26,8 s | 0.00137 · 0.00150 | 1.055 · 1.359 tok | parseo ok, 0 problemas, 0 avisos |

En `low` es el más rápido y el más barato de todo el banco; en `high` el tiempo queda a la par de
DeepSeek y conserva 3–4× de ventaja en costo.

**Lo que no está medido: la calidad de la extracción.** Las cuatro corridas se leyeron por conteo de
datos y por aspectos esperados, que es la vara equivocada (aviso de §1). Lo único que quedó
establecido de la salida es su **forma**, limpia en las cuatro. La suficiencia —si el caso y sus datos
bastan para responder una pregunta— está pendiente de la batería, y sin ella no se compara con
DeepSeek ni se propone como defecto.

## 4. MiMo-V2.6-Flash por OpenCode Go: contrato, costo y medidas (10-10)

**Modelo válido para la etapa 2**, con el contrato establecido y la calidad pendiente de la batería.

**Ruta, y es la fácil.** `POST https://opencode.ai/zen/go/v1/chat/completions`, que es la forma que
**ya consume nuestro transporte `openai_compatible`**: no hace falta transporte nuevo, al contrario
que Luna (§3). Clave `OPENCODE_API_KEY`; correr con `bash -ic '…'`.

**Corredor.** `temp/datos-test/paso2_seco_v1_mimo.py <doc> mimo <esfuerzo> <rN>`, que envuelve a
`paso2_seco_v1.py` y declara todo en memoria: el alias, el host en `CLAVE_POR_HOST` y la cabecera
`x-opencode-session`. **Si se adopta**, al registro le falta **una** cosa: **poner cabeceras por
alias** —hoy no existe: el `extra` del registro va al cuerpo, no a las cabeceras—. El alias con la
URL de Go y `opencode.ai → OPENCODE_API_KEY` en `claves.py` ya están, y la sesión de Go la pone el
transporte de `responses` (`openai_responses.py`), que es por donde va `luna`; el de
`chat/completions` (`openai_compatible.py`), por donde iría mimo, no la manda. Eso vale para
cualquier modelo que se adopte por Go, no solo para mimo.

**Esfuerzos: `none`, `low`, `medium`, `high`.** Rechaza con 400 `minimal`, `xhigh`, `max` y cualquier
valor inventado. **El contrato hubo que sacarlo enumerando**, porque —a diferencia de Luna— **Go
opaca el error del upstream**: devuelve `{"error":{"param":"","type":"server_error","message":
"Upstream request failed: [400] Invalid request parameters"}}`, sin `param` y sin la lista de válidos.
De ahí una lección sobre el método: **la sonda del error no sirve igual en todas las familias de Go**.

Lo llamativo es que `reasoning_effort` **no está documentado en ninguna de las dos páginas** —Xiaomi
solo documenta `thinking`, y Go no documenta parámetros de razonamiento— y sin embargo **se valida**.
Hay un conjunto real detrás que nadie publica.

**`thinking` también pasa, y manda, pero no se valida.** `thinking: {"type": "disabled"}` da 0 tokens
de razonamiento y `reasoning_content` vacío; con `disabled` más `reasoning_effort: low`, el
razonamiento sigue en 0, o sea que `thinking` pisa al esfuerzo. Pero `thinking: {"type": "pepino"}`
devuelve **200 y piensa** (16 tokens): un error de tipeo ahí se acepta en silencio. **Por eso, para
apagar el razonamiento conviene `reasoning_effort: "none"`, que sí está validado:** un parámetro
validado falla de frente, uno sin validar miente.

**Precio, cupo y retención** (página de Go, 10-10-2026). Entrada US$0.14/1M, salida US$0.28/1M,
lectura de caché US$0.0028/1M, sin tramos por contexto. Cupo de **US$60/mes** en el plan Go, del orden
de 150.400 peticiones al mes según la estimación de la página. **No entrena y retiene 0 días**: el
mejor perfil de privacidad de todos los candidatos hasta hoy.

**El caché de Go funciona también en `chat/completions`, y sin hacer nada.** Desde la segunda llamada
reusó 2.048 de 2.066 tokens de entrada; no hizo falta mandar el `[SISTEMA]` por un campo aparte como
en `responses`: el prefijo invariante de `messages` basta.

**Medido sobre `preparacion_cafe`** (5 UT, `temp/prompt_DATOS_v1.md`), ocho corridas:

| esfuerzo | réplica | tiempo | salida | razonamiento | costo (USD) | datos |
|---|---|---|---|---|---|---|
| `low` | s4 | 29,0 s | 2.497 | 932 | 0.00099 | 32 |
| `low` | s4r2 | 26,7 s | 2.467 | 1.130 | 0.00070 | 30 |
| `low` | s4r3 | 20,0 s | 1.443 | **11** | 0.00041 | 31 |
| `medium` | s4 | 29,8 s | 2.583 | 1.355 | 0.00073 | 26 |
| `medium` | s4r2 | 38,4 s | 2.681 | 1.300 | 0.00076 | 30 |
| `high` | s4 | 31,0 s | 2.318 | 1.010 | 0.00066 | 28 |
| `high` | s4r2 | 18,5 s | 1.385 | **12** | 0.00040 | 29 |
| `high` | s4r3 | 40,6 s | 2.414 | 1.157 | 0.00068 | 27 |

Forma limpia en las ocho: parseo bien, 0 problemas, 0 avisos. Costo plano entre US$0.0004 y
US$0.0010 en todo el rango.

**Tres cosas que las ocho corridas sí establecen, y no son sobre calidad:**

**El nivel de esfuerzo no ordena el razonamiento.** `medium` pensó más que `high` en la mayoría de las
comparaciones posibles entre esos dos niveles, y la dispersión entre réplicas del mismo nivel es del
mismo orden que la dispersión entre niveles. El interruptor fiable es `none` frente a cualquier otro;
entre `low`, `medium` y `high` no hay escalera que subir con esta muestra.

**El modelo a veces decide no pensar, con independencia del nivel pedido:** 11 tokens en `low` s4r3 y
12 en `high` s4r2, en los dos casos con salida normal (31 y 29 datos, forma limpia) y la mitad de
tiempo y de costo. Es intermitente, no un rasgo del nivel.

**El tiempo es el más disperso del banco:** de 18,5 a 40,6 s con el mismo modelo y el mismo esfuerzo,
más del doble entre la más rápida y la más lenta. Para una fase que va a correr sobre muchos
documentos, esa dispersión pesa tanto como la media.

**Dos defectos observados, menores pero registrables.** En `high` s4r3 un valor salió con una falta de
ortografía —«por gravadad» donde el texto dice «gravedad»—: `forma()` no lo detecta ni puede, porque
no juzga contenido, así que es un fallo que **pasa la verificación sin ser visto** y rompe el cotejo
del valor con el texto. Y la notación de la unidad varía entre corridas: `°C` en siete y «grados
Celsius» en una, más un «minutos» en plural con el valor «menos de medio». Si la unidad va a servir
para comparar o convertir, habrá que normalizarla.

**La calidad de la extracción no está medida**, por lo que dice el aviso de §1: solo la **forma** quedó
establecida. Lo que sí hay es una **lectura de Frat (10-10): `low` le parece de más calidad** que
`medium` y `high`. Es el juicio de quien trae el interés, no una medición, y queda pendiente de
confirmación con la batería de preguntas.
