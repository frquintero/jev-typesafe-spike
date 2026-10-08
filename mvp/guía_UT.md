# Guía de las unidades temáticas (UT)

Cómo se obtienen las unidades temáticas de un documento: qué entra, de dónde viene, cómo se
procesa, qué se entrega y cómo se entrega. Es el procedimiento vigente del MVP: el código en
`mvp/código/` y los crudos que produce en `mvp/temp/extraccion/`. El estado del trabajo vive en
`mvp/memoria de trabajo y pendientes.md`; acá está
el procedimiento, en detalle.

## 1. Qué es una unidad temática

Una UT es **un asunto y todo lo que el texto dice de ese asunto**: una o varias oraciones que
desarrollan el mismo núcleo, aunque estén separadas en el texto. El nombre de la UT dice **qué
se dice** de las cosas, no solo cuáles son («el tamaño de la tripulación», no «la tripulación»).

- Lo que une oraciones es **el asunto**, no el lugar, el objeto ni la persona.
- Un cambio de párrafo **no** separa por sí solo.
- **Cada oración va en una sola UT.**

Manda la definición del **prompt vigente** (`mvp/prompts/prompt_UT.md`), que es la que este
procedimiento aplica. El marco (`definiciones-del-marco.md`) define la unidad temática como
núcleo **más sus satélites**; los satélites todavía no se registran: es un pendiente declarado.

## 2. Qué entra

- **El texto**: `mvp/temp/pruebas/<doc>.md`. Un documento sintético, de contenido general
  (divulgación, noticia, nota de servicio), escrito para la prueba.
- **El prompt**: `prompt_UT`, el que esté **vigente en `mvp/prompts/`**. Se lee del archivo; su
  único hueco es `{{TEXTO_NUMERADO}}`, que se sustituye con `str.replace` (nunca `str.format`:
  el texto trae llaves). Es una versión de trabajo: no se afina en cada corrida.

El título del documento (la línea que empieza con `#`) no es una oración y queda fuera.

## 3. De dónde viene

- El texto lo escribe la planificación (Frat y Cowork), no el ejecutor. Reglas: sintético, de
  contenido general, y sin ejemplos tomados de los documentos de prueba.
- El mismo texto entra al corpus como **documento radicado**, en un acto aparte y a mano:
  `python3 mvp/código/radicar.py <doc>` —el texto queda en `mvp/documentos/<doc>.md` y la base
  anota su nombre, su fecha y su hora—. El detalle del corpus está en `mvp/consulta-diseno.md`
  §2–§3.

## 4. Cómo se procesa

Un comando, desde la raíz del repo:

```bash
python3 mvp/código/paso1_unidades.py <doc> <prompt> <modelo> <rN>

# por ejemplo
python3 mvp/código/paso1_unidades.py doc7 UT deepseek r1
```

Lo que hace, en orden:

1. **Numera las oraciones** del texto con `numerar_oraciones` (de `mvp/código/extraer_unidades.py`,
   la copia propia del MVP):
   quita las líneas de título, parte en párrafos por líneas en blanco y numera de 1 a N en
   orden global. Una oración va de un `.`, `?` o `!` al siguiente.
2. **Sustituye** `{{TEXTO_NUMERADO}}` en el prompt.
3. **Llama al modelo** por `proveedores.llamar` (`mvp/código/proveedores/`; el alias del registro,
   p. ej. `deepseek`): una sola llamada de texto a JSON, sin agente de por medio.
4. **Lee la respuesta** con `extract_json` (tolera que el JSON venga dentro de una cerca de
   código).
5. **Verifica la forma** con `verificar_subtemas`: que ninguna oración quede sin asignar, que
   ninguna esté en dos UT, que no haya números fuera de rango ni valores que no sean enteros.
6. **Escribe** los dos archivos de la §5.

Si el `.out` ya existe, **no vuelve a llamar**. Una repetición se pide con otro `rN` (`r2`,
`r3`…): un crudo no se borra ni se sobrescribe.

**Antecedente.** `doc4` y `doc6` se hicieron por Muse: se pegaba el prompt con el texto ya
numerado en un mensaje y se le delegaba la tarea a un agente. Lo medido:
51 s por Muse en `doc6` y 58,3 s por llamada directa en `doc7`; la diferencia no está en el
envoltorio, está en el razonamiento del modelo con este prompt. El procedimiento vigente es el
comando directo.

## 5. Qué se entrega

Dos archivos, en `mvp/temp/extraccion/<doc>/`:

**(a) El resultado** — `p1-<doc>-<prompt>-<modelo>-rN.out`:

```json
{"subtemas": [
  {"subtema": "el nombre del asunto", "oraciones": [1, 2]},
  {"subtema": "otro asunto", "oraciones": [3]}]}
```

Es lo que lee el cargador del corpus y lo que usa el paso 2 (los datos por unidad).

**(b) El crudo** — el mismo nombre con `.json`: la petición enviada, la respuesta, el texto
numerado, las oraciones numeradas, los **segundos** que tardó y la verificación. Sirve para
volver a verificar sin llamar a la API.

Un ejemplo real: `mvp/temp/extraccion/doc7/p1-doc7-v10-deepseek-r1.{out,json}`
—13 oraciones → 6 unidades, sin huecos ni solapes, 58,3 s—. El nombre lleva el prompt como se
llamaba entonces (`v10`); los crudos no se renombran.

## 6. Cómo se entrega

**Nombre y lugar.** `mvp/temp/extraccion/<doc>/p1-<doc>-<prompt>-<modelo>-rN.{out,json}`.
`<prompt>` es el nombre corto del archivo en `mvp/prompts/` (`UT` para `prompt_UT.md`) y
`<modelo>` la vía que se usó (`deepseek` hoy; `muse` en doc4 y doc6).

**Qué pasa después con lo que se entrega.** Cada UT es una fila del corpus:

- la unidad **n** es la **posición en el arreglo**, no el orden de lectura —el corte no es
  contiguo—,
- su id es `<doc>:Un` (por ejemplo `doc7:U3`),
- sus datos son los que produce el paso 2 en `p2-<doc>-u{n}-r{k}.out`. Si ese archivo falta, el
  cargador no puede armar la base y se detiene.

**Cierre de la corrida.** Si se tocó código, `python3 -m py_compile <archivo>`. Al terminar, se
commitea y se sube: el `.out`, el crudo y, si el paso cambió, los «sigue» de `README.md`,
`AGENTS.md` y la memoria.

## 7. Qué no hace este procedimiento

No decide qué es pertinente, no juzga el contenido de las unidades, no radica el documento, no
extrae datos y no mide calidad. Verifica **forma**: que la cobertura esté completa y que no haya
solapes. El contenido se lee y se juzga aparte.
