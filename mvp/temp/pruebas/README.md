# Pruebas del paso 1 (unidades temáticas) — registro

Carpeta de pruebas cortas del paso 1 del repo: el código numera o entrega las
oraciones y el prompt las agrupa. Cada prueba se corre sobre un documento
sintético inventado aquí y se guarda con su entrada, el mensaje enviado, la
salida cruda y la verificación.

**Nota (08-10-2026):** este registro conserva los prompts de su momento (`prompt_v5` a
`v9`, en esta carpeta). Los **prompts de trabajo vigentes** —paso 1, paso 2 y el agente de
la consulta— viven ahora en `mvp/prompts/` (`prompt_UT.md`, `prompt_DATOS.md` y
`prompt_ORQ.md`).

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
- **Esfuerzo:** `high` (escala de `otros documentos/agentes-delegados.md` §8: hay que
  decidir fronteras entre asuntos, no es mecánico).
- **Comando:** el envoltorio exige el mensaje **fuera del repo** y etiqueta nueva.
  El mensaje se dejó en `$HOME/.cache/muse_tarea_msgs/` porque `/tmp` no persiste
  entre llamadas del sandbox del Harness:

```bash
cd /home/fratquintero/Documentos/Claude/jev-typesafe-spike
ESFUERZO=high ./muse_tarea.sh prueba1-v5 \
  "$HOME/.cache/muse_tarea_msgs/prueba1-v5.md" nueva
```

(Registro de la corrida tal como se hizo. Hoy el envoltorio vive en
`utiliarios/muse_tarea.sh`; el comando vigente es
`./utiliarios/muse_tarea.sh <etiqueta> <mensaje> nueva`.)

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

**El hallazgo de esta prueba es la referencia que queda fuera de su grupo.** El
subtema `[5, 6]` empieza con «Su techo…», pero la oración que dice de quién es el
techo —«La escuela de la vereda tiene 34 alumnos»— quedó en `[4]`, otro subtema.
Con `[2]`, «Su eje», no pasa: su referente está en `[1]` y quedaron juntos. No es
un descuido del modelo: v5 **no tiene campo** para anotar la referencia —su salida
solo trae `subtema` y `oraciones`—, así que cuando el corte deja el antecedente
afuera no hay dónde dejarlo dicho: que las dos oraciones queden juntas o separadas
depende de dónde cayó la frontera del asunto, no de un registro.

**Esta corrida deja una partición formalmente correcta y un hallazgo: la
referencia que el grupo deja fuera.** Sobre ese hallazgo se hicieron las dos
variantes del prompt que vienen abajo.

---

## Prueba 2 · dos variantes del prompt, sobre el mismo documento · 5-10-2026

Se cambiaron solo los prompts; el documento, el agente y el esfuerzo fueron los
mismos (Muse Code, `high`, sesión nueva cada vez). El punto era resolver la
referencia externa **sin tocar la partición**.

### Variante A · `prompt_v6.md` — agrupar y resolver a la vez

Prompt nuevo: una sola tarea que agrupa y resuelve referencias, con `referencias`
anidado en cada subtema, un ejemplo de referencia entre grupos y otro de
referencia ambigua.

- Resultado: `exit 0`, **46 s**; 3 subtemas —`[1,2,3] [4,5,6] [7]`—.
- **Resolvió las referencias y rompió la partición.** La oración [4] se fue con
  [5,6], y la [3] con [1,2]: las dos fusiones son por entidad compartida, que el
  propio criterio prohíbe («compartir una entidad no basta»).
- La cláusula «citar una oración como respaldo no cambia su pertenencia» valió
  para los enlaces —la tormenta entre [2], [5] y [7]— y no valió para el dueño
  del techo: el camino barato era absorber.
- Lo mecánico quedó limpio —cobertura y reconstrucción por el verificador del
  repo; literalidad y `null`/`duda`, a mano—, así que el fallo era semántico.

### Variante B · `prompt_v7.md` — v5 íntegro más una tarea acotada después

**v5 conservado byte a byte** —los cinco ejemplos incluidos—, la TAREA
sustituida por «agrupa y después conserva ese agrupamiento», y un bloque
`REFERENCIAS EXTERNAS` (procedimiento, alcance, registro, ejemplo adicional)
insertado entre el ejemplo 5 y `texto`.

- Resultado: `exit 0`, **36 s**; 5 subtemas —`[1,2] [3] [4] [5,6] [7]`—,
  **idénticos a los de v5**.
- `referencias` presente en los cinco: el campo nuevo no fue desplazado por los
  ejemplos viejos.
- «Su» de [5] → «La escuela de la vereda La Esperanza», con respaldo que cita
  **[1], [4] y [5]**: el antecedente viaja y [4] no se mueve.
- «la alcaldía» no se registró, como pedía el ALCANCE.
- Sin problemas mecánicos: cobertura y reconstrucción por el verificador del repo;
  y comprobados a mano, literalidad de `expresion` y `respaldo`, pertenencia al
  propio subtema y `null`/`duda` coherentes.

### Las tres corridas

| | v5 | v6 | v7 |
|---|---|---|---|
| Partición | `[1,2][3][4][5,6][7]` | `[1,2,3][4,5,6][7]` | `[1,2][3][4][5,6][7]` |
| `referencias` | no | sí | sí |
| «Su» del techo | no registrada | resuelta, **[4] absorbida** | **resuelta citando [4], [4] quieta** |
| «la alcaldía» | — | `null` + duda | no registrada |
| Segundos | 18 | 46 | 36 |
| Razonamiento (tokens) | 1 115 | 5 310 | 4 539 |
| Salida (tokens) | 1 293 | 6 241 | 5 492 |

Los conteos salen del diario de la sesión, no del `.jsonl` del envoltorio.

### El resumen de razonamiento

Muse deja un **resumen** de su razonamiento —no la cadena completa, que viene
cifrada— en
`~/.local/share/muse/sessions/AÑO/MES/DÍA/<session_id>/session.jsonl`. De la v7:

> Separating the water-supply function from the roof-leak and petition as distinct subtemas.
> Resolving the 'la misma tormenta' reference to the [2] mention and **marking 'El maestro' as null due to missing explicit antecedent**.

Es un **indicio** de lo que hizo, no una prueba de que siguiera la secuencia del
prompt: es lo que el modelo cuenta de sí mismo.

### Dos observaciones de la v7, sin corregir

1. **«El maestro» quedó `null` y «la alcaldía» ni se registró.** No son la misma
   figura: uno es un papel ligado a una escuela ya mencionada; el otro introduce
   una fuente. Y el texto **no dice** que el maestro sea el de esa escuela, así
   que el `null` es defendible. Una regla general —«papel sin institución no es
   referencia sin resolver»— taparía ambigüedades reales.
2. **«la tormenta» de [7], con referente «la tormenta».** El `referente` repite
   la expresión, pero el **respaldo** cita [2] y [7], y eso establece que es el
   mismo acontecimiento en dos subtemas. Lo que importa es si leyendo el subtema
   aislado se identifica el referente; citando [2], se identifica.

## Cierre del ensayo · 5-10-2026

**Resultado favorable, no estabilidad demostrada.** v7 consiguió en este
documento lo que se buscaba: conservar la partición de v5 y llevar dentro de cada
subtema el respaldo de sus referencias externas, con menos tiempo y menos
razonamiento que v6.

**El candidato vigente es `prompt_v9.md`**, congelado el 5-10-2026. La cadena: v7
sobre `doc1`, `doc2` y `doc3`; v8 con la regla de identificación mínima; v9 con
las tres correcciones de la revisión —el ejemplo del archivo sin la referencia
interna, la fidelidad por delante de la brevedad, y la duda que conserva las
interpretaciones abiertas—. Con v9 se corrieron `doc4` y `doc5`, con los criterios
fijados antes; la evaluación está en `evaluacion_doc4-doc5.md`.

**Límites de lo probado:** cinco documentos y nueve corridas, una por documento y
versión de prompt, y un solo agente. Nada de esto dice cómo se comporta con otros
textos ni si repite el resultado: sin réplicas por documento, la estabilidad no se
midió. Que el resumen de razonamiento describa la secuencia del prompt tampoco lo
prueba.

**Decisión (5-10-2026): v9 queda congelado como base de trabajo del paso 1.** Sin
v10 y sin más corridas dedicadas a pulirlo. El prompt se reabre solo si aparece un
problema recurrente que afecte las respuestas, o una mejora concreta de rendimiento
que merezca probarse.

**Criterio de aceptación: la vara de Frat, ≈90 % de contenido correcto.** Aquí
**no se mide**: no hay esperado fijado antes ni denominador consistente —en `doc5`
se cumplieron los cuatro criterios fijados, y en `doc4` hubo un fallo y tres casos
no evaluables—. Eso es un conteo con un hueco, no una medición. El esperado y las
réplicas se piden cuando lo que se busca es medir (fricción 4).

**Huecos conocidos, no bloqueantes:** la referencia hacia adelante quedó sin
ejercitar, y quedó una referencia externa sin registrar. Congelar es dejar de
iterar, no dar por resuelto.

**Siguiente paso:** usar estas unidades y sus referencias en la extracción de
datos. Lo primero ahí no es extraer, sino decidir **cómo llega el contexto externo
de la unidad a la ficha**, que es por documento y no tiene dónde llevar las
`referencias`.

**Si se adopta** como prompt del paso 1, le correspondería `unidades/prompts/`
con el número siguiente a `unidades_v5`; hoy vive en esta carpeta de pruebas y esa
decisión no está tomada.

---

## Herramienta

`correr_muse.sh` deja la corrida en un comando, sin depender de `/tmp`:

```bash
./mvp/temp/pruebas/correr_muse.sh seco    <doc> <prompt> <etiqueta>            # arma el mensaje y no lanza nada
./mvp/temp/pruebas/correr_muse.sh correr  <doc> <prompt> <etiqueta> [esfuerzo] # arma, deja el mensaje fuera del repo y lanza
./mvp/temp/pruebas/correr_muse.sh recoger <etiqueta> [<doc>]                  # trae la salida, la verifica y reconstruye
```

`<doc>` acepta una ruta o un nombre suelto de `unidades/docs`; `<prompt>` es el
nombre sin `.md` de `unidades/prompts`, o una ruta a un archivo. Detecta sola si
el prompt usa `{{TEXTO_NUMERADO}}` o `{{TEXTO}}`, así que sirve igual con el
prompt de v5 y con el de v7. Cada corrida deja `corrida_<etiqueta>.json` con el
documento y el prompt usados, y `recoger` verifica contra **ese** documento; el
`<doc>` solo hace falta si el archivo de la corrida no está. El encabezado de
instrucciones que genera no es byte a byte el que se envió en la prueba 1 —se
conserva el enviado como registro—, pero el prompt y el texto sí son idénticos.

## Archivos

Todo lo que deja una corrida lleva la etiqueta en el nombre
(`<tipo>_<etiqueta>`). Etiquetas: `prueba1-v5`, `prueba2-v6` y `prueba3-v7` (doc1);
`consulta1` (la pregunta a Muse por su propia salida); `prueba4-doc2` y
`prueba5-doc3` (con v7); `prueba6-v8-doc2` y `prueba7-v8-doc3` (con v8);
`prueba8-v9-doc4` y `prueba9-v9-doc5` (con v9).

| Archivo | Qué es |
|---|---|
| `doc1.md` … `doc5.md` | Los cinco documentos sintéticos. |
| `correr_muse.sh` | Herramienta: armar, lanzar y recoger en un comando. |
| `prompt_v6.md` | Variante A: agrupar y resolver a la vez. |
| `prompt_v7.md` | Variante B: v5 íntegro más el bloque de referencias externas. |
| `prompt_v8.md` | v7 con la regla de identificación mínima y el ejemplo del archivo. |
| `prompt_v9.md` | **Candidato congelado**: ejemplo corregido, fidelidad por delante de la brevedad, duda que conserva las interpretaciones abiertas. |
| `criterios_doc4-doc5.md` | Criterios fijados **antes** de correr doc4 y doc5. |
| `evaluacion_doc4-doc5.md` | Evaluación de v9 en esos dos textos, por fidelidad y economía. |
| `mensaje_<etiqueta>.md` | Mensaje preparado (instrucciones + prompt con el texto numerado). |
| `mensaje_<etiqueta>_enviado.md` | Copia del `.msg` que Muse recibió de verdad. |
| `corrida_<etiqueta>.json` | Documento y prompt de la corrida, para que `recoger` verifique contra el correcto. |
| `salida_<etiqueta>.md` | Salida cruda de Muse. |
| `salida_<etiqueta>.jsonl` | Traza del `muse exec`. |
| `salida_<etiqueta>.err` | Diagnósticos de Muse. |
| `salida_<etiqueta>_meta.json` | Etiqueta, sesión, esfuerzo, `exit` y segundos. |
| `verificacion_<etiqueta>.json` | Verificación del repo y unidades reconstruidas. |

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
es; por eso el camino sin numerar, cuya verificación comprueba
literalidad, marcaría `no_literales` sobre una copia fiel. En el camino numerado
la verificación no mira literalidad, así que ahí es cosmético.

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

**Nota (06-10-2026):** esa regla cambió. Ahora delega **el ORQUESTADOR que designe
Frat**; la copia vigente está en `otros documentos/agentes-delegados.md` (su §1), y
esta corrida se conserva como se registró.

## Pendiente

- **Paso 2 con estas unidades y referencias — es el trabajo de ahora:** decidir
  cómo llega el contexto externo de la unidad a la extracción de datos. La
  extracción ya corre por unidad (`unidades/extraer_datos_doc.py`); lo que no
  entra en esa entrada es el campo `referencias`. Después, la pieza mecánica del
  orquestador (memoria, «Pendientes vigentes»).
- **Reabrir v9** solo por un problema recurrente que afecte las respuestas, o por
  una mejora concreta de rendimiento. Las réplicas y la referencia hacia adelante
  quedan como huecos conocidos, no como tareas de pulido.
- **Aparcado:** el límite de la oración (punto 3 de la revisión de fricciones).

Historial de la carpeta: `git log -- mvp/temp/pruebas/`.
