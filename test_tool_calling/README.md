# test_tool_calling

Directorio de trabajo para probar la **configuración y operación de tools en
DeepSeek v4.1** (`deepseek-flash` en la API): cómo se declaran, cómo vuelven en la
respuesta, cómo se contesta cada llamada y qué exige el bucle cuando hay razonamiento.

Fuente de lo que sigue: [Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/)
(leído el 07-10-2026).

## Lo que dice la guía

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

## Qué vamos a probar

- Que una tool declarada por nosotros vuelva en `tool_calls`, con argumentos parseables.
- Que el bucle cierre: asistente con `tool_calls` → mensaje `role: "tool"` con su
  `tool_call_id` → respuesta.
- Varias llamadas en un mismo turno: cada una con su `tool_call_id`.
- Con razonamiento activado y `tools` en la petición: que el `reasoning_content` vuelva en los
  turnos siguientes y no dé 400.
- `strict`: qué esquemas acepta el servidor y qué rechaza.

## Archivos

- `system_prompt.md` — el system prompt del LLM (se lee de archivo).
- `tool_calling.py` — las tres herramientas, sus definiciones y el bucle; pide por consola la operación y los números.
- `cache/` — el crudo de cada corrida (cuerpos enviados y respuestas, sin cabeceras).
