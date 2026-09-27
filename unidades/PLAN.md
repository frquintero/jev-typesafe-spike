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

## Ronda DU5: `datos_u5` (ejemplos en lugar de definiciones) sobre ut1-ut5 con Grok

Hallazgo de DU4: «escala» se leía como nivel de medición (nominal, ordinal) y
todo adjetivo cabía en una; ut4 dio dos seudodatos («municipal», «antiguo»).

Un cambio de principio: mostrar en lugar de definir. Se quitan definiciones,
procedimiento y reglas; quedan una tarea de una línea y tres ejemplos de
dominios ajenos a ut1-ut5 (uno con datos de varios tipos, uno con trampas,
uno sin datos). Formato nuevo: `{"datos": [{"variable", "valor",
"unidad_de_medida"}]}`, sin `caso` ni nivel `unidades`.

Decisiones de Frat que los ejemplos enseñan:
- La variable es la magnitud individual (VIM): «peso de la caja», con su caso
  y sus circunstancias («temperatura del paciente de la cama 12 a las 8»).
- Valor literal, tal como aparece en `texto`, sin la unidad.
- `unidad_de_medida` en lugar de `escala`; los valores cualitativos llevan
  `null`; los conteos, «unidad»; las horas, «hora».
- Binarios (con fiebre, sin fallas, trabado): hechos, no datos.
- Modificadores cualitativos del nombre (antiguo, municipal): parte del caso.
  Una cantidad con unidad es dato aunque vaya en el nombre («caja de 12 kg»).

Gold (esperado):
- ut1: hora de encendido del quemador de la caldera C-2 = 6 de la mañana
  (hora); temperatura del circuito de retorno de la caldera C-2 = 55 (°C).
- ut2: capacidad del tanque de agua potable = 30000 (litros); número de
  arranques de la bomba de llenado del tanque en la noche = dos (unidad);
  posición del flotador del tanque = alta (null).
- ut3: hora de salida del camión de reparto 7 del depósito = 5:40 (hora);
  nivel del tanque de combustible del camión 7 = tres cuartos (fracción);
  presión de las llantas delanteras = 32 (psi); de las traseras = 35 (psi).
- ut4: ninguno.
- ut5: temperatura del paciente de la cama 12 a las 8 = 38,7 (°C);
  intensidad del dolor abdominal = moderado (null); tipo de tos = seca (null).

Conjetura: con los ejemplos, Grok se acerca al gold; en particular, ut4 sin
datos y sin «escalas» nominal/ordinal.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u5 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u5 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u5 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u5 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u5 r1
```

**Reporte:** el mismo de DU1. Sin veredicto.

**Réplicas:** r1 la corrió Muse (commit fc2feef). r2 es una réplica con el mismo
request, corrida por Luna (ChatGPT), que la guardó por error como r1 (commit
59f6469); se restauró r1 y la de Luna quedó como r2.

## Ronda DU6: `datos_u6` (definiciones cortas + cinco ejemplos nodo) sobre ut1-ut5 con Grok

Hallazgo de DU5 (r1 y r2): los ejemplos rinden (ut4 vacío, los 13 valores),
pero cada falla corresponde a una forma de dato que los ejemplos no mostraban
(identificador en la variable, hora con «de la mañana», fracción, hora como
circunstancia) y lo inestable entre réplicas es donde la señal era débil
(identificador, conteo, binario).

Un cambio de principio, apoyado en la literatura (guías de anotación concisas
+ ejemplos representativos y contrastivos: GoLLIE, GuideNER, muestreo por
diversidad, *near miss*): definiciones de una línea, con las mismas palabras
de los ejemplos, y cinco ejemplos nodo (prototípicos) elegidos desde el marco,
no desde las fallas; cada uno agrupa formas que ningún otro cubre:

1. Mediciones (viñedo): unidades, decimales, %, horas con mañana/tarde,
   identificador, hora como circunstancia.
2. Cualidades (café): ordinales, nominal, puntaje; casi-dato binario
   («certificado»).
3. Nombres y relaciones (muelle): cantidad dentro del nombre; casi-datos:
   adjetivo del nombre, relación entre casos, binario.
4. Conteos y proporciones (aves): conteo con «unidad», fracción, fecha como
   circunstancia; casi-dato: relación.
5. Sin datos (sendero): hechos, relación, binario, recomendación.

Fuera por ahora (Ockham, smoke test): rangos, aproximaciones, valores negados.

Gold: el de DU5. Aviso: ut1-ut5 son conjunto de desarrollo; su acierto aquí
sale inflado. El 90 % se medirá después en unidades nuevas.

Conjetura: sobre ut1-ut5, Grok acierta en ambas réplicas ≥ 12 de los 13 datos
completos (variable con su identificador y circunstancia, valor literal,
unidad), ut4 vacío, sin «sin fallas», «6 de la mañana» completo, «tres cuartos»
con «fracción» y «a las 8» dentro de la variable.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u6 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u6 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u6 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u6 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u6 r1
python3 unidades/extraer_datos_u.py ut1 grok datos_u6 r2
python3 unidades/extraer_datos_u.py ut2 grok datos_u6 r2
python3 unidades/extraer_datos_u.py ut3 grok datos_u6 r2
python3 unidades/extraer_datos_u.py ut4 grok datos_u6 r2
python3 unidades/extraer_datos_u.py ut5 grok datos_u6 r2
```

**Reporte:** el mismo de DU1, por unidad y réplica. Sin veredicto.

## Ronda DU7: `datos_u7` (aspecto implícito en el nodo de cualidades) sobre ut1-ut5 con Grok, tres réplicas

Hallazgo de DU6: 13/13 valores con su unidad, ut4 vacío, réplicas casi
idénticas; pero en ut5 las variables cualitativas nombran la entidad y no el
aspecto («dolor abdominal» = moderado, «tos» = seca; gold: «intensidad del
dolor abdominal», «tipo de tos»). En la literatura: atributo implícito.

Un ajuste dentro del nodo 2 (cualidades), no un nodo nuevo:
- Ejemplo 2: «acidez alta y aroma floral» (aspecto dicho) junto a «grano
  grande» y «tueste oscuro» (aspecto callado: «tamaño del grano», «grado de
  tueste»); sale «cuerpo medio».
- Definición de variable: + «Si `texto` no nombra el aspecto, la variable lo
  nombra (tamaño, tipo, grado).»

Gold: el de DU5. Conjetura: en las tres réplicas, 13/13 completos (con el
aspecto en ut5) y ut4 vacío, sin romper lo que DU6 acertó.

Tres réplicas (r1, r2, r3) para medir después la variación entre corridas; el
request no fija `temperature` (usa la del proveedor). El análisis lo hace
Cowork; el ejecutor solo corre y reporta.

```
python3 unidades/extraer_datos_u.py ut1 grok datos_u7 r1
python3 unidades/extraer_datos_u.py ut2 grok datos_u7 r1
python3 unidades/extraer_datos_u.py ut3 grok datos_u7 r1
python3 unidades/extraer_datos_u.py ut4 grok datos_u7 r1
python3 unidades/extraer_datos_u.py ut5 grok datos_u7 r1
python3 unidades/extraer_datos_u.py ut1 grok datos_u7 r2
python3 unidades/extraer_datos_u.py ut2 grok datos_u7 r2
python3 unidades/extraer_datos_u.py ut3 grok datos_u7 r2
python3 unidades/extraer_datos_u.py ut4 grok datos_u7 r2
python3 unidades/extraer_datos_u.py ut5 grok datos_u7 r2
python3 unidades/extraer_datos_u.py ut1 grok datos_u7 r3
python3 unidades/extraer_datos_u.py ut2 grok datos_u7 r3
python3 unidades/extraer_datos_u.py ut3 grok datos_u7 r3
python3 unidades/extraer_datos_u.py ut4 grok datos_u7 r3
python3 unidades/extraer_datos_u.py ut5 grok datos_u7 r3
```

**Reporte:** el mismo de DU1, por unidad y réplica. Sin veredicto ni cálculos.

## Ronda ENC1: cadena completa (paso 1 + paso 2) sobre un documento nuevo, con Grok

Primera prueba de punta a punta: entra un documento, salen sus datos.
Documento sintético nuevo, `docs/bio1.md` (biología marina: monitoreo de un
arrecife; cinco párrafos, 19 oraciones, uno o dos subtemas por párrafo).
Prompts vigentes: `unidades_v2` (paso 1) y `datos_u7` (paso 2). Sin gold, a
propósito: lo analizamos Frat y Cowork cuando vuelvan los crudos, para no
sesgarnos. Ronda exploratoria, sin conjetura formal.

### Implementación (la hace el ejecutor): `unidades/extraer_datos_doc.py`

Uso: `python3 unidades/extraer_datos_doc.py <doc> <modelo> <prompt_unidades> <prompt_datos> <rN>`

1. **Paso 1.** Llamar a `extraer_unidades.run(doc, modelo, prompt_unidades, rN)`
   (importándolo; es idempotente y guarda
   `cache/unidades-<doc>-<modelo>-<prompt_unidades>-<rN>.json`). Leer ese
   crudo. Si `parsed` es null, detenerse y reportar.
2. **Pegamento (código, sin LLM).** Para cada unidad del paso 1, en el orden en
   que vienen (k = 1, 2, …): `texto_unidad` = sus `oraciones` unidas con un
   espacio, ordenadas por su posición en el documento (`texto.find`); las que
   no se encuentren literales van al final, en el orden dado.
3. **Paso 2, una llamada por unidad** (nunca en bloque): `prompt_datos` leído de
   archivo, `{{TEXTO}}` sustituido con `str.replace` por `texto_unidad`;
   `call_model("toulmin", modelo, ...)` y `extract_json` de
   `niveles/run_niveles.py`, como en `extraer_datos_u.py`. Crudo por unidad en
   `cache/datos-<doc>-u<k>-<modelo>-<prompt_datos>-<rN>.json`, con los mismos
   campos que `extraer_datos_u.py` (`doc`, `modelo`, `prompt`, `segundos`,
   `request`, `response`, `parsed`, `venia_con_cerca`, `error_parseo`) más
   `unidad_n`, `nucleo`, `satelites` y `texto_unidad`. Idempotente: si el crudo
   existe, no llama.
4. **Consolidado** (solo se arma con los crudos, sin llamadas):
   `cache/doc-<doc>-<modelo>-<prompt_unidades>-<prompt_datos>-<rN>.json` con
   `{"doc", "modelo", "prompt_unidades", "prompt_datos", "rep",
   "unidades": [{"unidad_n", "nucleo", "satelites", "texto_unidad",
   "datos", "error_parseo"}]}`, donde `datos` es `parsed["datos"]` (o null si
   no parseó). Se regenera en cada ejecución.
5. Imprimir por unidad: número de datos y segundos.

Reglas: no tocar `extraer_unidades.py`, `extraer_datos_u.py` ni los prompts;
nada de `Authorization` ni lectura de claves (el proxy las pone);
`python3 -m py_compile` al terminar.

### Corrida

```
python3 unidades/extraer_datos_doc.py bio1 grok unidades_v2 datos_u7 r1
```

**Reporte:** la verificación del paso 1 (la que imprime `extraer_unidades`),
las unidades (núcleo y oraciones) y, por unidad, el JSON `parsed` del paso 2
verbatim, con modelo efectivo, tokens y segundos. Sin veredicto ni cálculos.
