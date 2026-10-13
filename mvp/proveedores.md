# Proveedores de LLM en el MVP

Qué modelos puede llamar el MVP y por dónde. **El registro vivo es el código**:
`mvp/código/proveedores/__init__.py` (`ALIAS` resuelve alias → proveedor, `id`, URL, esfuerzo y
`extra`; cada transporte traduce a/desde su API). Este documento es el mapa, no su bitácora.

**El modelo y el esfuerzo de cada acto no se eligen acá**: viven en la tabla `ajustes` del corpus
(una fila por acto: `volcado`, `UT`, `DATOS`, `ORQ`), y la precedencia es **línea de comandos > base
> código**. Hoy las cuatro filas están en `luna`/`low`.

## 1. Los alias registrados

| Alias | Modelo | API y familia | Clave |
|---|---|---|---|
| `deepseek` | DeepSeek-V4.1-Flash | api.deepseek.com, `chat/completions` | `DEEPSEEK_API_KEY` |
| `glm` | GLM-5.3-Flash | api.z.ai, `chat/completions` | `ZAI_API_KEY` |
| `haiku` | Claude Haiku 5.5 | api.anthropic.com, `messages` | `ANTHROPIC_API_KEY` |
| `luna` | GPT 6 Luna | OpenCode Go, familia `responses` | `OPENCODE_API_KEY` |
| `grok` | Grok 4.7 | api.x.ai, `chat/completions` | `XAI_API_KEY` |
| `gemini` | Gemini 3.8 Flash | Google AI Studio, fachada compatible con OpenAI | `GEMINI_API_KEY` |

- Los transportes: `openai_compatible.py` (`deepseek`, `glm`, `grok`, `gemini`), `anthropic.py`
  (`haiku`) y `openai_responses.py` (`luna`). El esfuerzo se pide como `reasoning_effort`
  (`output_config.effort` en Anthropic); el defecto del registro es `low`, y `luna` —cuyo defecto
  propio es `medium`, y va por la familia `responses` con la cabecera de sesión de Go— lo pisa.
- **`glm` en `low` no razona**: la API acepta el nivel y devuelve 0 tokens de pensamiento; si se
  quiere razonamiento de GLM hay que pedir `max` explícito (medido el 10-10-2026; ver el informe, §2).
- **`grok` probado el 13-10-2026**: texto y herramientas, por `proveedores.llamar`, con una clave de
  **inferencia** (`xai-…`, ACLs `api-key:model:*`). Ojo con las dos trampas: **no toda clave que emite
  la consola es de inferencia** —las `grok_…` de agente no las acepta `api.x.ai`—, y el **equipo** de
  la clave tiene que tener cupo. El pensamiento vuelve en `completion_tokens_details.reasoning_tokens`
  (sin `reasoning_content`), y el modelo suma del orden de **1.260 tokens de prompt propio**, con caché.
- **`gemini` está declarado y sin etapa asignada**: probado con `proveedores.llamar` (texto y
  herramientas). Por esa fachada el pensamiento se cobra pero no se declara aparte.
- Lo que se probó y **no** quedó en el registro —Sonnet 5.5, MiMo-V2.6-Flash y las comparaciones de
  la etapa 2— está en `otros documentos/informe-proveedores-2026-10-10.md`.

## 2. La puerta de agregación: OpenCode Go

`https://opencode.ai/zen/go/v1/`, por suscripción y con una sola clave (`OPENCODE_API_KEY`, en
`~/.config/opencode-console/api_key.env`, que carga `~/.bashrc`: **correr con `bash -ic`**). Enruta a
modelos de varios proveedores y tiene tres familias: `responses` (`luna`), `chat/completions` (`mimo`,
`kimi`, `longcat`…) y `messages`; el MVP usa las dos primeras. Los modelos de Go **no** son nuestros
alias: salvo `luna`, los alias de arriba van a sus hosts directos.

## 3. Cómo se invoca cada acto

- **Volcado:** `python3 mvp/código/volcar.py <fuente>`.
- **Etapa 1 (UT):** `python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--esfuerzo E]
  [--prompt UT] [--rehacer]`.
- **Etapa 2 (DATOS):** `python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--esfuerzo E]
  [--rehacer]`.
- **Etapa 3 (ORQ):** `python3 mvp/código/orq/orquestador.py (--texto "…" | <archivo> [--numero N])
  --dominio E [--modelo M] [--esfuerzo E]`. La pregunta entra por el acto —el cargador es
  `mvp/código/cargar_pregunta.py`— y se radica al cerrar con entrega; `config.json` solo lleva rutas
  y guardias.

Sin `--modelo`/`--esfuerzo`, el acto usa su fila de `ajustes`. Cómo se arma el `system` y el `user`
de cada llamada: `mvp/diseño-mvp.md` §4.
