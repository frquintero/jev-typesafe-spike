# test_tool_calling

Directorio de trabajo para probar la **configuración y operación de tools en
DeepSeek v4.1** (`deepseek-flash` en la API): cómo se declaran, cómo vuelven en la
respuesta, cómo se contesta cada llamada y qué exige el bucle cuando hay razonamiento.

Fuentes, leídas el 07-10-2026:
[Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/) y
[Chat Completions API](https://api-docs.deepseek.com/api/create-chat-completion/).

## Lo que dice la guía de tools

- **El modelo no ejecuta nada.** Devuelve la llamada —nombre de la función y argumentos— y la
  ejecución la hace el cliente.
- **El flujo tiene cuatro pasos:** el usuario pregunta → el modelo devuelve
  `get_weather({location: 'Hangzhou'})` → el cliente ejecuta la función y le da el resultado →
  el modelo responde en lenguaje natural.
- **Los dos apéndices del bucle**, tal como los muestra el ejemplo:
  `messages.append(message)` —el mensaje del asistente, con sus `tool_calls`— y
  `messages.append({"role": "tool", "tool_call_id": tool.id, "content": "24℃"})`; después se
  vuelve a llamar con `tools`.
- **Declaración de una tool:** `tools=[{"type": "function", "function": {name, description,
  parameters}}]`, donde `parameters` es un JSON Schema.
- **Modo razonamiento:** desde DeepSeek-V3.2 la API admite tools en modo razonamiento; el
  detalle del bucle está en
  [Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode#tool-calls).
- **No se pueden insertar llamadas a mitad de la conversación.** Chat Completions no lo admite
  —sí admite insertar mensajes `system` en medio—; la API de Anthropic y la Responses API
  admiten las dos cosas.
- **`strict` (Beta):** se activa con `base_url="https://api.deepseek.com/beta"` y `strict: true`
  en **todas** las funciones; el servidor valida el esquema y devuelve error si no cumple.
  Tipos admitidos: `object`, `string`, `number`, `integer`, `boolean`, `array`, `enum`, `anyOf`
  (más `$ref` y `$def`). En cada `object`, **todas** las propiedades van en `required` y
  `additionalProperties` va en `false`. No se admiten `minLength`, `maxLength`, `minItems` ni
  `maxItems`.

## Lo que dice la referencia de la API

**Petición**

- `messages` (obligatorio, ≥ 1) admite los roles `system`, `user`, `assistant` y `tool`.
- `model`: `deepseek-flash` o `deepseek-v4-pro`.
- `tools`: solo `function`; **los nombres tienen que ser únicos**, hasta 128 caracteres de
  `a-zA-Z0-9_-`. Cada tool lleva `description`, `name`, `parameters` (JSON Schema; **omitirlo
  define una función sin argumentos**) y `strict` (`false` por defecto, **Beta**).
- `tool_choice`: `none` · `auto` · `required` · una función nombrada. **`none` es el defecto sin
  `tools` y `auto` el defecto con `tools`**; **`required` y la nombrada no se admiten en modo
  razonamiento: la API devuelve 400.**
- `function.arguments` es un **string** con JSON, y el modelo **no siempre genera JSON válido ni
  respeta el esquema**: hay que validarlo antes de ejecutar.
- `stream_options.include_usage` exige `stream: true` (si no, 400). El **último chunk** antes de
  `data: [DONE]` trae el `finish_reason` no nulo y el `usage`, sobre el último chunk de
  contenido; no hay chunk aparte solo de usage.
- `reasoning_effort`: `none` · `low` · `high` · `max`, por defecto `high`; `minimal`→`low` y
  `medium`/`xhigh`→`high`. **`low` es `low`: no se convierte en `high`.**
- `max_tokens`: 1–393216; por defecto 8K sin razonamiento y 64K con razonamiento (128K con
  `max`).
- `response_format: {"type": "json_object"}` garantiza JSON válido, pero **hay que pedirlo
  también en el prompt**; con `finish_reason: "length"` el contenido puede venir cortado.
- `temperature` no tiene efecto en modo razonamiento; `top_p` solo actúa ahí (recortado a
  0.95–1.0) y en modo normal queda en 1.0. `frequency_penalty` y `presence_penalty` están
  **retirados**: se aceptan y no hacen nada.
- `user_id` (hasta 512, `[a-zA-Z0-9-_]`): identifica al usuario y sirve para **aislar el
  KVCache**, además de rate limit y revisión de contenido.

**Respuesta**

- `choices[0].finish_reason`: `stop` · `length` · `content_filter` · `tool_calls` ·
  `insufficient_system_resource` · `aborted`.
- `choices[0].message`: `content` (puede ser `null`), `reasoning_content` (**solo en modo
  razonamiento**) y `tool_calls[]` con `{id, type, function{name, arguments}}`.
- `usage`: `prompt_tokens` = `prompt_cache_hit_tokens` + `prompt_cache_miss_tokens`;
  `prompt_tokens_details.cached_tokens` es el hit, y
  `completion_tokens_details.reasoning_tokens` va dentro de la completion.

El detalle de los mensajes `user`, `assistant` y `tool` no vino en la extracción de la página
(vienen en pestañas): el `assistant` con `reasoning_content` y el `tool` con `tool_call_id` se
leen en las otras dos guías.

## Cómo queda el guion contra esto

- **`tool_choice`**: no se manda → `auto` por defecto, que es lo único válido con razonamiento
  encendido (el alias `v2/deepseek` lo enciende).
- **Validación de argumentos**: `ejecutar()` parsea el string, exige `numeros` no vacío y
  devuelve el error como resultado de la tool, en vez de reventar.
- **`finish_reason` y `usage`**: el ensamblador de stream los captura en el último chunk.
- **`strict`**: queda en `false`; activarlo exige `base_url="https://api.deepseek.com/beta"` y
  `additionalProperties: false` con todo en `required` (los tres esquemas ya cumplen esa forma).

## Qué vamos a probar

- Que una tool declarada por nosotros vuelva en `tool_calls`, con argumentos parseables.
- Que el bucle cierre: asistente con `tool_calls` → mensaje `role: "tool"` con su
  `tool_call_id` → respuesta.
- Varias llamadas en un mismo turno: cada una con su `tool_call_id`.
- Con razonamiento activado y `tools` en la petición: que el `reasoning_content` vuelva en los
  turnos siguientes y no dé 400.
- `strict`: qué esquemas acepta el servidor y qué rechaza.

## Archivos

- `prompt.json` — **el prompt**: el `system` y las definiciones de las `tools`, en un solo artefacto.
- `tool_calling.py` — implementa las tres herramientas y lleva el bucle; pide por consola la operación y los números.
- `cache/` — el crudo de cada corrida (cuerpos enviados y respuestas, sin cabeceras).
