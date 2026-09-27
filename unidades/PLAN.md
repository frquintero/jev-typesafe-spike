# unidades/ — paso 1: unidades temáticas (núcleo y satélites)

Sub-spike aparte. Prueba si un LLM divide un `texto` en unidades temáticas:
un hecho nuclear, sus satélites y las oraciones que se refieren a ellos, con
anáforas y alcances de procedencia resueltos. Es el primer paso del
procedimiento de extracción; el paso 2 (datos por unidad) viene después.

Aplican las reglas de ejecución de `AGENTS.md`.

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

## Ronda DU1: paso 2 (datos por unidad), smoke test con Grok

Prompt `prompts/datos_u1.md` (definiciones de unidad, dato, variable, valor y
escala; procedimiento: separar en unidades, variables, valores, escalas).
Cinco unidades temáticas sintéticas, una por llamada (`docs/ut1.md` a `ut5.md`):
ut1 y ut2 salen de tec2 (U3); ut3 trae un valor sin unidad y una fracción;
ut4 no tiene datos (solo hechos); ut5 trae escalas ordinal y nominal.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u1 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u1 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u1 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u1 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u1 r1
```

**Reporte:** por unidad, el JSON `parsed` verbatim; si venía con cerca o hubo
error de parseo; modelo efectivo; tokens (`prompt_tokens`,
`completion_tokens`, `reasoning_tokens`) y segundos. Sin veredicto.

## Ronda DU2: `datos_u2` sobre ut1-ut5 con Grok

Cambios respecto de `datos_u1`, a partir de DU1: vuelve el caso (con los
identificadores dentro del caso: «camión = 7», «cama = 12» en DU1); entran las
condiciones constitutivas (en DU1 «a las 8» quedó como variable suelta);
prueba del dominio en la definición de variable y en el procedimiento (en DU1,
ut4, sin datos, dio tres); la escala ya no puede ser null: todo valor
pertenece a una escala aunque `texto` no la nombre, y si no pertenece a
ninguna no hay dato (en DU1 null mezclaba «no nombrada» con «no existe»). Sin
ejemplos tomados de las unidades de prueba.

Conjetura: ut4 sin datos; «7» y «12» dentro del caso; «a las 8», «a las 6 de
la mañana» y «en la noche» como condiciones; ninguna escala null.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u2 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u2 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u2 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u2 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u2 r1
```

**Reporte:** el mismo de DU1. Sin veredicto.

## Ronda DU3: `datos_u3` sobre ut1-ut5 con Grok

Hallazgo de DU2: al afirmar que «todo valor pertenece a una escala», Grok
inventó escalas para llenar el campo («edificios», «espacios colindantes»,
«ubicaciones de mesas», «categorías de agua»): ut4 dio cuatro datos y en ut1
volvió «calienta el agua». Todos esos falsos datos tienen como valor otro caso
(un edificio, un parque, unas mesas, el agua): registran una relación entre
casos, no una determinación (ensayo l. 87, 135).

Dos cambios respecto de `datos_u2`:
1. Escala: «Todo valor pertenece a una escala, aunque `texto` no la nombre»
   pasa a «Puede recuperarse de la variable y de la forma del valor aunque
   `texto` no la nombre».
2. Regla nueva: «Un valor no es otro caso. Si la respuesta es algo concreto
   (un lugar, un objeto, una persona), `texto` registra una relación entre
   casos, no un dato».

Conjetura: ut4 sin datos; «calienta el agua» fuera; los datos verdaderos de
DU2 se mantienen.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u3 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u3 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u3 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u3 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u3 r1
```

**Reporte:** el mismo de DU1. Sin veredicto.

## Ronda DU4: `datos_u4` sobre ut1-ut5 con Grok

Dos cambios respecto de `datos_u3` (decisión de Frat):
1. Valor: «elemento cuantitativo (discreto o continuo) o cualitativo (nominal
   u ordinal) que adopta una variable», en lugar de «una posición o elemento de
   una escala que expresa una determinación bajo una variable».
2. Sin condiciones constitutivas: fuera su definición, el paso 5 del
   procedimiento, las condiciones en la definición de dato y en la pregunta
   `<variable>(<caso>) = ?`, y el campo `condiciones_constitutivas` del reporte.

Conjetura: sin formular (ronda exploratoria). A observar: qué hace el modelo
con los valores binarios («sin fallas», «trabado», «con fiebre») y dónde quedan
«a las 8» (ut5) y «en la noche» (ut2) sin el campo de condiciones.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u4 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u4 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u4 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u4 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u4 r1
```

**Reporte:** el mismo de DU1. Sin veredicto.
