# Guía de las unidades temáticas (UT)

Cómo se obtienen las unidades temáticas de un documento: qué entra, de dónde viene, cómo se
procesa, qué se entrega y cómo se entrega. Es el procedimiento vigente del MVP: el código en
`mvp/código/` y lo que produce en la base (`mvp/código/corpus.db`). El estado del trabajo vive en
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

- **El texto**: el **documento radicado**, `mvp/documentos/<doc>.md`. Un documento sintético, de
  contenido general (divulgación, noticia, nota de servicio), escrito para la prueba. Antes de
  trabajar se comprueba su **sello** contra la base: si el archivo cambió, eso es otro documento y
  se detiene.
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
python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--prompt UT] [--rehacer]

# por ejemplo
python3 mvp/código/paso1_unidades.py doc8
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
6. **Escribe en la base**, en una sola transacción: la fila de la **corrida** y las **unidades**
   (§5).

Si el documento **ya tiene unidades**, no llama al modelo. Rehacerlas es un acto explícito:
`--rehacer` (se rehacen las unidades y los datos que cuelgan de ellas). **Todo o nada:** si la
llamada falla, si la respuesta se cortó o si el JSON no se pudo leer, la corrida queda **fallida**
con su motivo y no se escribe ninguna unidad; y si el intento era un `--rehacer`, **lo anterior
vuelve** —el borrado y la escritura nueva van en una sola transacción—, así que un intento fallido no
se come la extracción buena.

**Antecedente.** `doc4` y `doc6` se hicieron por Muse: se pegaba el prompt con el texto ya
numerado en un mensaje y se le delegaba la tarea a un agente. Lo medido:
51 s por Muse en `doc6` y 58,3 s por llamada directa en `doc7`; la diferencia no está en el
envoltorio, está en el razonamiento del modelo con este prompt. El procedimiento vigente es el
comando directo.

## 5. Qué se entrega

**Dos cosas en la base** (`mvp/código/corpus.db`), y nada en archivos:

**(a) La corrida** — en `corridas`, con el id `<doc>:UT`: el modelo y su esfuerzo, el prompt y su
hash, los tokens (entrada, salida y pensamiento), los segundos, la fecha, y el `estado`
(`exitoso`, o `fallido` con su motivo si el JSON no se pudo leer).

**(b) Las unidades** — en `unidades`, una por UT: el id `<doc>:Un`, el nombre del caso (`subtema`)
y **los números de oración** que agrupa («1,4»). Las oraciones literales no se guardan: se leen del
documento radicado, y el sello es el guardián.

```sql
-- así se lee una unidad, con la corrida que la produjo
SELECT u.id, u.subtema, u.oraciones, c.modelo, c.tokens_salida
FROM unidades u JOIN corridas c ON c.id = u.corrida_id
WHERE u.documento_id = 'doc8' ORDER BY u.n;
```

Si la corrida falla —no se pudo leer el JSON—, **no se escribe ninguna unidad**: queda la corrida
marcada como fallida, con su motivo.

## 6. Cómo se entrega

**Nombre y lugar.** En la base, siempre. El id de la unidad es `<doc>:Un` —la **posición en el
arreglo** que devolvió el modelo, no el orden de lectura: el corte no es contiguo—, y `oraciones`
son los números del texto.

**Qué pasa después con lo que se entrega.** El paso 2 lee esas unidades **de la base** y escribe
los datos. Nada se escribe en `mvp/temp/`: ese es el archivo y no se toca.

**Cierre de la corrida.** Si se tocó código, `python3 -m py_compile <archivo>`. Al terminar, se
commitea y se sube **la base** (ahí quedó todo).

## 7. Qué no hace este procedimiento

No decide qué es pertinente, no juzga el contenido de las unidades, no radica el documento, no
extrae datos y no mide calidad. Verifica **forma**: que la cobertura esté completa y que no haya
solapes. El contenido se lee y se juzga aparte.
