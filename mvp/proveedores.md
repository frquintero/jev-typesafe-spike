# Proveedores de LLM en el MVP

Registro de qué modelos se usan, por dónde se activan en cada etapa, y qué muestran las pruebas
comparativas hechas sobre la Etapa 2 (extracción de DATOS). El registro vivo de proveedores —el
código que resuelve alias y llama a cada API— es `mvp/código/proveedores/__init__.py`; este
documento es su bitácora de decisión, no un duplicado.

## 1. Modelos usados y rutas de activación por etapa

El MVP tiene tres etapas, cada una con su propio corredor y su propio alias de modelo (los alias
viven en `ALIAS` dentro de `mvp/código/proveedores/__init__.py`; `resolver(alias, esfuerzo)` fija
el esfuerzo pedido sobre el de defecto del alias, `low`):

- **Etapa 1 — extracción de unidades temáticas (UT).** Corredor: `mvp/código/paso1_unidades.py`.
  Se invoca `python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--esfuerzo E] [--prompt UT]
  [--rehacer]`; sin `--modelo`/`--esfuerzo`, usa el valor por defecto fijado en `main()`.
- **Etapa 2 — extracción de datos (DATOS).** Corredor: `mvp/código/paso2_datos.py`. Misma forma de
  invocación (`--modelo`, `--esfuerzo`, `--rehacer`), mismo patrón de defecto en `main()`.
- **Etapa 3 — respuesta a la consulta/pregunta.** Corredor: `mvp/código/orq/orquestador.py`
  (bucle en `bucle.py`, llamada en `llamar_modelo.py`). El modelo no se pasa por línea de comandos:
  se fija en `mvp/código/orq/config.json`, bajo `modelo.alias` / `modelo.esfuerzo`.

Además de los hosts de cada proveedor, hay una **puerta de agregación**: **OpenCode Go**
(suscripción; base `https://opencode.ai/zen/go/v1/`, clave `OPENCODE_API_KEY`), que enruta a modelos
de varios proveedores con una sola clave. Tiene tres familias de API y cada modelo usa una sola:
`chat/completions` (forma OpenAI: deepseek, glm, kimi, mimo, longcat…), `messages` (forma Anthropic:
claude-haiku-5-5, minimax, qwen) y `responses` (Responses API de OpenAI: gpt-6-luna, grok,
muse-spark). Las dos primeras las parsean los transportes que ya existen; la tercera, no (§6).

Modelos probados hasta ahora (todos con alias ya registrado en `ALIAS`, salvo Sonnet 5.5 y
GPT 6 Luna, que se declaran solo en los corredores de prueba de `temp/datos-test/`):

| Alias / modelo | Proveedor (API) | Dónde se probó |
|---|---|---|
| `deepseek` — DeepSeek-V4.1-Flash | api.deepseek.com | Etapa 1 (real), Etapa 2 (real y pruebas en `temp/`) |
| `haiku` — Claude Haiku 5.5 | api.anthropic.com | Etapa 1 (real, high), Etapa 2 (pruebas en `temp/`: medium, high, max) |
| `glm` — GLM-5.3-Flash | api.z.ai | Etapa 2 (pruebas en `temp/`: low, high, max) |
| Claude Sonnet 5.5 (sin alias fijo en `ALIAS`) | api.anthropic.com | Etapa 2 (pruebas en `temp/`: sin razonamiento, low) |
| `gpt-6-luna` — GPT 6 Luna (sin alias fijo en `ALIAS`) | OpenCode Go, familia `responses` | Etapa 2 (pruebas en `temp/`: low ×2, high ×2) |
| `grok` — Grok 4.7 | api.x.ai | Declarado, sin probar (sin créditos en xAI) |

## 2. Etapa 2 (extracción de DATOS): resultados de las pruebas y proveedor por defecto

**Aviso (10-10): las columnas «Cobertura» y «Estabilidad» de §2.1 se puntuaron por conteo de datos y
por una lista de aspectos esperados, y esa no es la vara del proyecto** —la vara es si el caso y sus
datos bastan para responder una pregunta—. Quedan pendientes de re-puntuación con una batería de
preguntas escrita a ciegas de las extracciones (ver «Encargo a otro modelo» en
`mvp/memoria de trabajo y pendientes.md`); el costo y el tiempo sí son medidas directas y se
sostienen. El proveedor por defecto no se cambia mientras no se re-puntúe.

**Proveedor por defecto: `deepseek` (DeepSeek-V4.1-Flash), esfuerzo `low`.**

### 2.1 Qué se probó

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
razona (ver §3): las pruebas de cobertura de GLM se hicieron en `max`, el único nivel en el que el
modelo piensa de forma consistente el 10-10-2026.

### 2.2 Por qué DeepSeek-flash low

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

## 3. Etapa 1 (extracción de UT): proveedor por defecto

**Proveedor por defecto: `deepseek` (DeepSeek-V4.1-Flash), esfuerzo `low`** (mismo valor por
defecto de `main()` en `paso1_unidades.py`; no se ha hecho para Etapa 1 la misma batería
comparativa que para Etapa 2 — la corrida real registrada en la base usó Haiku 5.5 high por
decisión puntual, no por sustituir este defecto).

## 4. Etapa 3 (respuesta a consulta/pregunta): proveedor por defecto — abierto

`orq/config.json` fija hoy `modelo.alias: "deepseek"`, `modelo.esfuerzo: "low"`, pero **esta
elección no se ha probado**: ninguna de las pruebas comparativas de esta sesión corrió sobre la
Etapa 3 (que tiene su propio bucle de herramientas, distinto del paso directo de UT/DATOS). El
proveedor por defecto para Etapa 3 queda abierto hasta hacer pruebas específicas sobre el
orquestador.

## 5. Nota: discrepancia observada en GLM-5.3-Flash (z.ai)

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

Esta nota vivía como comentario en `mvp/código/proveedores/__init__.py`, junto al alias `glm`; se
trasladó aquí y se quitó de ese archivo.

## 6. GPT 6 Luna por OpenCode Go: contrato, costo y medidas (10-10)

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
`[TAREA]` como `input`. **Si se adopta, le toca un transporte propio** (`openai_responses`) en
`mvp/código/proveedores/`; hoy no existe y el registro no tiene alias para él.

**Esfuerzos: `none`, `low`, `medium`, `high`, `xhigh`, `max`.** Lo dijo la propia API al rechazar
`minimal` con HTTP 400 y enumerar los válidos; la documentación de Go no documenta el parámetro.
**El defecto es `medium`** (la respuesta devuelve `reasoning: {effort: "medium", mode: "standard",
context: "all_turns"}` cuando no se manda). Nuestros cinco esfuerzos pasan **1:1** a
`reasoning.effort`, sin tabla de traducción, y además ofrece `none`: acá el razonamiento **sí** se
puede apagar, al contrario de GLM (§5). Otras perillas que la respuesta devuelve y no hemos tocado:
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
datos y por aspectos esperados, que es la vara equivocada (aviso de §2). Lo único que quedó
establecido de la salida es su **forma**, limpia en las cuatro. La suficiencia —si el caso y sus datos
bastan para responder una pregunta— está pendiente de la batería, y sin ella no se compara con
DeepSeek ni se propone como defecto.
