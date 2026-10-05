# Pruebas del paso 1 (unidades temáticas) — registro

Carpeta de pruebas cortas del paso 1 del repo: el código numera o entrega las
oraciones y el prompt las agrupa. Cada prueba se corre sobre un documento
sintético inventado aquí y se guarda con su entrada, el mensaje enviado, la
salida cruda y la verificación.

---

## Prueba 1 · `unidades_v5` sobre un documento sintético · 5-10-2026

### 1. El documento (la entrada)

`doc1.md`, inventado para esta prueba. No viene de ningún documento real ni del
material de la mesa de dominio. Título como etiqueta y siete oraciones, en tres
párrafos de **una línea cada uno**:

> **# El molino y la escuela de la vereda La Esperanza**
>
> El molino de viento de la vereda La Esperanza dejó de girar el martes. Su eje se agarrotó después de la tormenta. El molino abastece de agua a doce familias.
>
> La escuela de la vereda tiene 34 alumnos. Su techo se filtró en la misma tormenta. El maestro recogió firmas para pedir materiales.
>
> Según la alcaldía, la tormenta fue la más fuerte del año.

### 2. El prompt

`unidades/prompts/unidades_v5.md`, **verbatim y sin cambios**. El mensaje que
recibió el agente lo lleva copiado entero, con el texto numerado en el lugar de
`{{TEXTO_NUMERADO}}`; el `.msg` exacto que se envió queda en
`mensaje_prueba1-v5_enviado.md`. La salida que pide es
`{"subtemas": [{"subtema", "oraciones": [n, …]}]}`.

### 3. Cómo se numeraron las oraciones

No se numeró a mano. El criterio está escrito en dos sitios y lo implementa el
código:

- `definiciones-del-marco.md`, parte B, fila **«Oración»**: «tramo de texto de un
  `.`, `?` o `!` al siguiente; el código la numera (`[1]`, `[2]`…). Ingenua ante
  abreviaturas, miles con punto y siglas». Origen: `unidades_v1`; código desde U4
  (`unidades_v3`).
- `unidades/PLAN.md`, **ronda U4**, «Implementación»: quitar las líneas de título
  (`#`), partir en párrafos por líneas en blanco, partir cada párrafo con la
  función `oraciones`, numerar las oraciones de 1 a N **en orden global**, unir
  las de un párrafo con un espacio (`[k] oración`) y los párrafos con una línea
  en blanco; sustituir con `str.replace`; guardar `texto_numerado` y
  `oraciones_numeradas` (lista `{"n", "oracion"}`).

El mensaje lo arma la herramienta de esta carpeta, que **importa la función del
repo** (`numerar_oraciones` de `unidades/extraer_unidades.py`) en vez de
reimplementarla, de modo que lo enviado es idéntico a lo que manda
`extraer_unidades.py`. Texto numerado resultante:

```
[1] El molino de viento de la vereda La Esperanza dejó de girar el martes. [2] Su eje se agarrotó después de la tormenta. [3] El molino abastece de agua a doce familias.

[4] La escuela de la vereda tiene 34 alumnos. [5] Su techo se filtró en la misma tormenta. [6] El maestro recogió firmas para pedir materiales.

[7] Según la alcaldía, la tormenta fue la más fuerte del año.
```

### 4. Quién lo corrió y cómo

- **Agente:** Muse Code **1.4.2** (`1.4.2-R4684.1`), vía `./muse_tarea.sh`.
- **Esfuerzo:** `high` (escala de `agentes-delegados.md` §8: hay que decidir
  fronteras entre asuntos, no es mecánico).
- **Comando:** el envoltorio exige el mensaje **fuera del repo** y etiqueta nueva.
  El mensaje se dejó en `$HOME/.cache/muse_tarea_msgs/` porque `/tmp` no persiste
  entre llamadas del sandbox del Harness:

```bash
cd /home/fratquintero/Documentos/Claude/jev-typesafe-spike
ESFUERZO=high ./muse_tarea.sh prueba1-v5 \
  "$HOME/.cache/muse_tarea_msgs/prueba1-v5.md" nueva
```

- **Resultado:** `exit 0`, **18 s**, sesión `f48099c5-a97a-4866-a002-468215c721e6`
  (`salida_prueba1-v5_meta.json`). Una sola tarea de Muse a la vez (candado del
  envoltorio).
- Muse carga `AGENTS.md` del repo en cada sesión. En su `.err` avisó de que
  ignora `CLAUDE.md` porque `AGENTS.md` tiene precedencia en esa carpeta: aquí no
  molesta, porque `CLAUDE.md` es una línea que apunta a `AGENTS.md`.

### 5. La salida

`salida_prueba1-v5.md` (crudo, 402 bytes):

```json
{"subtemas": [{"subtema": "la detención del molino y su causa", "oraciones": [1, 2]}, {"subtema": "las familias que abastece el molino", "oraciones": [3]}, {"subtema": "el número de alumnos de la escuela", "oraciones": [4]}, {"subtema": "la filtración del techo y la petición de materiales", "oraciones": [5, 6]}, {"subtema": "la intensidad de la tormenta según la alcaldía", "oraciones": [7]}]}
```

### 6. La verificación

Con el verificador del propio repo, no a ojo: `extract_json` +
`es_caso_subtemas` + `verificar_subtemas` + `reconstruir_subtemas` de
`unidades/extraer_unidades.py`. Resultado en `verificacion_prueba1-v5.json`:

- `parseo ok`, `venia_con_cerca: false`, `error_parseo: null`, `es_caso_subtemas: true`.
- `{"oraciones_del_texto": 7, "huecos": [], "solapes": [], "fuera_de_rango": [], "no_enteros": []}`.

Es decir: las siete oraciones asignadas exactamente una vez, sin huecos, sin
solapes y sin números fuera de rango; la reconstrucción devuelve el texto
literal de cada oración.

### 7. Lectura

Muse siguió los propios ejemplos de v5: `[1, 2] + [3]` es el ejemplo 4 (la
represa y, aparte, los municipios que abastece), y `[5, 6]` aplica la regla de
desarrollo por consecuencia —la petición del maestro sigue a la filtración—.
Tres de los cinco subtemas son de una sola oración: con siete oraciones, el eje
asunto corta fino.

Y ahí se ve el eje: **con v5 salen cinco subtemas; con el eje de v1 saldrían dos
unidades** —el molino con su satélite «su eje» (1, 2, 3) y la escuela con «su
techo» (4, 5, 6)—. Contraste pendiente de correr; el mensaje ya está preparado en
`mensaje_contraste-v1.md`.

---

## Herramienta

`correr_muse.sh` deja la corrida en un comando, sin depender de `/tmp`:

```bash
./mvp/pruebas/correr_muse.sh seco    <doc> <prompt> <etiqueta>            # arma el mensaje y no lanza nada
./mvp/pruebas/correr_muse.sh correr  <doc> <prompt> <etiqueta> [esfuerzo] # arma, deja el mensaje fuera del repo y lanza
./mvp/pruebas/correr_muse.sh recoger <etiqueta>                          # trae la salida a esta carpeta y la verifica
```

`<doc>` acepta una ruta o un nombre suelto de `unidades/docs`; `<prompt>` es el
nombre sin `.md` de `unidades/prompts`. Detecta sola si el prompt usa
`{{TEXTO_NUMERADO}}` o `{{TEXTO}}`, así que sirve igual para v5 y para el eje de
v1. El encabezado de instrucciones que genera no es byte a byte el que se envió
en la prueba 1 —se conserva el enviado como registro—, pero el prompt y el texto
sí son idénticos.

## Archivos

| Archivo | Qué es |
|---|---|
| `doc1.md` | Documento sintético de la prueba 1. |
| `correr_muse.sh` | Herramienta: armar, lanzar y recoger la corrida. |
| `mensaje_prueba1-v5.md` | Mensaje generado con v5 (instrucciones + prompt con el texto numerado). |
| `mensaje_prueba1-v5_enviado.md` | Copia del `.msg` que Muse recibió de verdad en la prueba 1. |
| `mensaje_contraste-v1.md` | Mensaje preparado con `unidades_v1` para el contraste pendiente. |
| `salida_prueba1-v5.md` | Salida cruda de Muse (el JSON). |
| `salida_prueba1-v5.jsonl` | Traza completa de la sesión de Muse (46 KB). |
| `salida_prueba1-v5.err` | Diagnósticos de Muse, con el aviso de `CLAUDE.md`. |
| `salida_prueba1-v5_meta.json` | Etiqueta, sesión, esfuerzo, `exit` y segundos. |
| `verificacion_prueba1-v5.json` | Verificación del repo y unidades reconstruidas. |

## Revisión de las fricciones · 5-10-2026

**1. `/tmp` no persiste entre llamadas del sandbox.** Es del sandbox del Harness,
no del repo ni del flujo de Muse: para Claude o Cowork `/tmp` funciona.
**Resuelto:** `correr_muse.sh` arma el mensaje, lo deja en `~/.cache/muse_tarea_msgs/`
y lanza, todo en un proceso; `/tmp` deja de importar.

**2. Escribir fuera del workspace estaba bloqueado.** No era un defecto: era el
sandbox de la sesión del Harness, y el envoltorio escribe en
`~/.cache/muse_tareas/` por diseño (`muse_tarea.sh` no se toca). **Resuelto:** la
sesión pasó a acceso completo, así que desde aquí `correr_muse.sh correr` funciona
sin pedir nada. Era un permiso de la sesión, no un asunto del repo.

**3. Oraciones con salto interno. Mi diagnóstico anterior estaba mal.** No son
oraciones partidas en varias líneas al escribir el documento: son tramos que la
definición **une a través de un corte de párrafo**. La definición de «Oración»
corta solo en `.`, `?` o `!`; una línea que empieza después de dos puntos
—«…de desplazamiento:» y «Organismos Bentónicos: …»— no abre oración nueva, así
que la oración los abarca a los dos y el texto numerado lleva el corte dentro del
ítem.

Medido: afecta a **2 de 21** documentos del repo —`biomar1.md` (33 oraciones, 3
afectadas) y `evals1.md` (22, 1)—. Y verificado el daño real: la oración oficial
**sí** es literal en el documento, mientras que una copia sin el salto **no** lo
es; por eso el camino sin numerar (v1/v2), cuya verificación comprueba
literalidad, marcaría `no_literales` sobre una copia fiel. En el camino numerado
(v5) la verificación no mira literalidad, así que ahí es cosmético.

**Qué no se toca:** colapsar los blancos de la oración rompería la literalidad
del respaldo, que es la garantía del repo. El código queda como está.
**Aparcado (5-10-2026):** no vale la pena atacarlo ahora. Queda anotado con lo
medido —afecta a 2 de 21 documentos— y con las tres salidas posibles para cuando
llegue el momento: que un corte de párrafo también termine oración, que la
convención de documentos evite las listas con dos puntos, o que la comparación de
literales sea insensible a blancos.

**4. El verificador es de forma, no de contenido.** No es una fricción: es el
reparto del marco —al código el cómputo, al modelo el juicio, y el agente no se
juzga a sí mismo—.

Escribí aquí que faltaba un gold previo, y era un requisito sin para qué. El gold
sirve para **medir**: es el resultado que se fija antes de correr para poder
comparar un candidato —un prompt, un modelo— contra un esperado y no justificarlo
a posteriori; el repo lo usa en sus rondas de extracción, donde la pregunta es
«¿qué tan fiel es este prompt?». En esta prueba no hay candidato que medir: solo
queríamos ver el prompt, la entrada y la salida del paso 1 con Muse. Poner gold
aquí sería cumplir un procedimiento sin evaluar nada. **Se pide cuando lo que
queramos sea medir, y entonces vendrá con su pregunta y su criterio**; igual las
réplicas, que sirven para separar efecto de ruido cuando hay un efecto que medir.

## Política aplicada

Frat autorizó expresamente esta prueba. La política de
`/home/fratquintero/Claude-memoria/memoria/agentes-delegados.md` §1 reserva
lanzar a Muse a **Claude y ChatGPT** («ningún otro agente lanza a otro agente»),
de modo que esta corrida es una excepción autorizada por el dueño de la política;
el documento de política, que vive fuera del repo, no se modificó.

## Pendiente

- **Commit** de la carpeta (y, por ser carpeta nueva, la sincronía de los tres
  sitios que pide `AGENTS.md`: README, «Mapa del repo» y memoria).
- Si quieres ver la diferencia de eje, el mensaje para v1 ya está preparado
  (`mensaje_contraste-v1.md`) y `correr_muse.sh correr doc1.md unidades_v1 …` lo
  lanza. No es un pendiente de método: es una comparación disponible.
- **Aparcado:** el límite de la oración (punto 3).
