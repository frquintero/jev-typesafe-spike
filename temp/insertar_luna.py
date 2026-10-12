#!/usr/bin/env python3
"""Inserta GPT 6 Luna en mvp/proveedores.md. Idempotente."""
import pathlib

RUTA = pathlib.Path("mvp/proveedores.md")
t = RUTA.read_text(encoding="utf-8")

# --- 1) nota de la ruta de OpenCode Go, antes de la tabla de §1 ---
ANCLA_TABLA = """Modelos probados hasta ahora (todos con alias ya registrado en `ALIAS`, salvo Sonnet 5.5, que se
declaró como alias temporal solo en los corredores de prueba de `temp/datos-test/`):"""
NOTA_GO = """Además de los hosts de cada proveedor, hay una **puerta de agregación**: **OpenCode Go**
(suscripción; base `https://opencode.ai/zen/go/v1/`, clave `OPENCODE_API_KEY`), que enruta a modelos
de varios proveedores con una sola clave. Tiene tres familias de API y cada modelo usa una sola:
`chat/completions` (forma OpenAI: deepseek, glm, kimi, mimo, longcat…), `messages` (forma Anthropic:
claude-haiku-5-5, minimax, qwen) y `responses` (Responses API de OpenAI: gpt-6-luna, grok,
muse-spark). Las dos primeras las parsean los transportes que ya existen; la tercera, no (§6).

Modelos probados hasta ahora (todos con alias ya registrado en `ALIAS`, salvo Sonnet 5.5 y
GPT 6 Luna, que se declaran solo en los corredores de prueba de `temp/datos-test/`):"""
if "puerta de agregación" not in t:
    assert ANCLA_TABLA in t, "no encontré el ancla de la tabla de §1"
    t = t.replace(ANCLA_TABLA, NOTA_GO, 1)

# --- 2) fila en la tabla de §1 ---
FILA_SONNET = "| Claude Sonnet 5.5 (sin alias fijo en `ALIAS`) | api.anthropic.com | Etapa 2 (pruebas en `temp/`: sin razonamiento, low) |\n"
FILA_LUNA = "| `gpt-6-luna` — GPT 6 Luna (sin alias fijo en `ALIAS`) | OpenCode Go, familia `responses` | Etapa 2 (pruebas en `temp/`: low ×2, high ×2) |\n"
if "gpt-6-luna` — GPT 6 Luna" not in t:
    assert FILA_SONNET in t, "no encontré la fila de Sonnet"
    t = t.replace(FILA_SONNET, FILA_SONNET + FILA_LUNA, 1)

# --- 3) aviso sobre la vara, al abrir §2 ---
ANCLA_2 = """## 2. Etapa 2 (extracción de DATOS): resultados de las pruebas y proveedor por defecto

**Proveedor por defecto:"""
AVISO = """## 2. Etapa 2 (extracción de DATOS): resultados de las pruebas y proveedor por defecto

**Aviso (10-10): las columnas «Cobertura» y «Estabilidad» de §2.1 se puntuaron por conteo de datos y
por una lista de aspectos esperados, y esa no es la vara del proyecto** —la vara es si el caso y sus
datos bastan para responder una pregunta—. Quedan pendientes de re-puntuación con una batería de
preguntas escrita a ciegas de las extracciones (ver «Encargo a otro modelo» en
`mvp/memoria de trabajo y pendientes.md`); el costo y el tiempo sí son medidas directas y se
sostienen. El proveedor por defecto no se cambia mientras no se re-puntúe.

**Proveedor por defecto:"""
if "Aviso (10-10)" not in t:
    assert ANCLA_2 in t, "no encontré el ancla de §2"
    t = t.replace(ANCLA_2, AVISO, 1)

# --- 4) sección propia de Luna, al final ---
SECCION = """
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
"""
if "## 6. GPT 6 Luna" not in t:
    t = t.rstrip("\n") + "\n" + SECCION

RUTA.write_text(t, encoding="utf-8")
print("listo")
