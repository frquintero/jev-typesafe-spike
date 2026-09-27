# unidades/ — paso 1: unidades temáticas (núcleo y satélites)

Sub-spike aparte. Prueba si un LLM divide un `texto` en unidades temáticas:
un hecho nuclear, sus satélites y las oraciones que se refieren a ellos, con
anáforas y alcances de procedencia resueltos. Es el primer paso del
procedimiento de extracción; el paso 2 (datos por unidad) viene después.

Aplican las reglas de ejecución del `CLAUDE.md` raíz y de `AGENTS.md`.

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

## Ronda U1d: `unidades_v1` sobre tec1 con DeepSeek

Igual que U1; solo cambia el LLM. `deepseek` = `deepseek-flash`
(DeepSeek-V4.1-Flash), `stream: true`, `thinking: {"type": "enabled"}`,
`reasoning_effort: "low"`. En DeepSeek los tokens de razonamiento van dentro de
`completion_tokens`.

```
python3 unidades/extraer_unidades.py tec1 deepseek unidades_v1 r1
```

**Reporte:** el mismo de U1. Sin veredicto.

## Ronda U2: `unidades_v2` sobre tec1, Grok y DeepSeek

Lecciones de U1/U1d que entran en el prompt: se quitan `relacion`, la lista de
anáforas, las menciones, las procedencias y `oraciones_sin_unidad` (no sirven
al paso 2 ni a la medición: el paso 2 es un LLM que lee la unidad entera, y la
cobertura la verifica el código); el prompt pasa a ser el procedimiento en tres
pasos (casos, núcleos y satélites, unidades temáticas); un caso puede ser
satélite de más de un núcleo (en U1 los dos modelos omitieron en silencio el
jarabe y las llenadoras, compartidos entre núcleos); nombre del caso sin
artículos ni posesivos.

Conjetura: mismas unidades que U1, ahora con los casos compartidos (jarabe,
llenadoras) como satélites en vez de omitidos, con menos tokens de salida.

```
python3 unidades/extraer_unidades.py tec1 grok unidades_v2 r1
python3 unidades/extraer_unidades.py tec1 deepseek unidades_v2 r1
```

**Reporte:** por modelo, el mismo de U1. Sin veredicto.

## Ronda U3: `unidades_v2` sobre tec2, Grok y DeepSeek

Mismo prompt que U2 (base: funciona sobre tec1). Documento nuevo `docs/tec2.md`
(sala de máquinas; 4 núcleos, 2 satélites cada uno) donde el párrafo no
coincide con la unidad: dos núcleos por párrafo, cada núcleo reaparece más
adelante (unidades no continuas) y un párrafo mezcla tres núcleos. Gold en
`gold/tec2.json`.

Conjetura: v2 agrupa por núcleo y no por párrafo; las cuatro unidades reúnen
oraciones no seguidas (1,2,9 / 3,4,10 / 5,6,11 / 7,8,12).

```
python3 unidades/extraer_unidades.py tec2 grok unidades_v2 r1
python3 unidades/extraer_unidades.py tec2 deepseek unidades_v2 r1
```

**Reporte:** por modelo, el mismo de U1. Sin veredicto.
