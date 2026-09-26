# unidades/ — paso 1: unidades temáticas (núcleo y satélites)

Sub-spike aparte. Prueba si un LLM divide un `texto` en unidades temáticas:
un hecho nuclear, sus satélites y las oraciones que se refieren a ellos, con
anáforas y alcances de procedencia resueltos. Es el primer paso del
procedimiento de extracción; el paso 2 (datos por unidad) viene después.

Aplican las reglas de ejecución del `CLAUDE.md` raíz y de `MUSE.md`.

## Archivos (no editar sin aprobación de Frat)

- `docs/tec1.md`: documento técnico sintético; 4 núcleos, 2-3 satélites cada
  uno, anáforas y una procedencia que alcanza dos oraciones. Sin señuelos.
- `gold/tec1.json`: unidades esperadas, escritas antes de correr.
- `prompts/unidades_v1.md`: el prompt. Marcador `{{TEXTO}}`.
- `extraer_unidades.py`: orquesta, guarda el crudo con el tiempo total y
  verifica literalidad y cobertura (solo reporta).

## Ronda U1: `unidades_v1` sobre tec1 con Grok 4.7

`grok` = `grok-4.7`, `reasoning_effort: "low"`, `stream: true`,
`stream_options: {"include_usage": true}` (sin esto xAI no manda `usage` en
streaming; en D10g no quedaron tokens).

```
python3 unidades/extraer_unidades.py tec1 grok unidades_v1 r1
```

**Reporte:** el JSON `parsed` verbatim; si venía con cerca o hubo error de
parseo; la verificación (literalidad y cobertura) tal como la imprime el
script; modelo efectivo; tokens por separado (`prompt_tokens`,
`completion_tokens`, `reasoning_tokens`) y los segundos. Sin veredicto y sin
comparar contra el gold: eso lo hacen Frat y Cowork.
