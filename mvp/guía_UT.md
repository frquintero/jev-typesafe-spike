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

**Para qué cierra.** La UT es el **ámbito donde se cierran las referencias**: una oración que por
sí sola no cierra —«esa energía», «allí»— cierra en su unidad, porque el núcleo y los satélites son
los referentes que nombra y las oraciones que se refieren a ellos van juntas. El **nombre del caso**
es parte de ese mecanismo: nombra el núcleo y **trae su antecedente** («la energía solar en las
cadenas alimentarias…», no «esa energía»).

- Lo que une oraciones es **el asunto**, no el lugar, el objeto ni la persona.
- Un cambio de párrafo **no** separa por sí solo.
- **Cada oración va en una sola UT.**
- **El cierre es su función:** el antecedente de lo que sus oraciones dicen está en la unidad —en
  otra de sus oraciones o en el nombre del caso—. Si no está, la unidad queda abierta.

Manda la definición del **prompt vigente** (`mvp/prompts/prompt_UT.md`), que es la que este
procedimiento aplica. El marco (`definiciones-del-marco.md`) define la unidad temática como
núcleo **más sus satélites**, y los satélites son la mitad explícita de ese cierre: declararlos es
un pendiente declarado, y hoy el cierre lo carga el nombre.

## 2. Qué entra

- **El texto**: el **documento radicado**, `mvp/documentos/<doc>.md`. Un documento sintético, de
  contenido general (divulgación, noticia, nota de servicio), escrito para la prueba. Antes de
  trabajar se comprueba su **sello** contra la base: si el archivo cambió, eso es otro documento y
  se detiene.
- **El prompt**: `prompt_UT`, el que esté **vigente en `mvp/prompts/`**. Se lee del archivo; sus
  huecos son `{{RELOJES}}` —los dos relojes, en el `system`— y `{{TEXTO}}` —el documento, en el
  `user`—, y se sustituyen con `str.replace` (nunca `str.format`: el texto trae llaves). Es una
  versión de trabajo: no se afina en cada corrida.

**El texto entra entero, con sus títulos y subtítulos**: son contexto para interpretar, no
oraciones. El corte en oraciones lo hace el modelo al devolverlas **literales**, y el código las
ubica en el texto para quedarse con su tramo.

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
python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--esfuerzo E] [--prompt UT] [--rehacer]

# por ejemplo
python3 mvp/código/paso1_unidades.py doc8
```

Lo que hace, en orden:

1. **Toma el texto del documento radicado**, entero, sin numerar y sin marcar.
2. **Sustituye** `{{TEXTO}}` en el prompt: el prompt va como `system` y el texto —delimitado— como
   `user`.
3. **Llama al modelo** por `proveedores.llamar` (`mvp/código/proveedores/`; el alias del registro,
   p. ej. `luna`): una sola llamada de texto a JSON, sin agente de por medio.
4. **Lee la respuesta** con `extract_json` (tolera que el JSON venga dentro de una cerca de
   código).
5. **Ubica cada oración en el texto** con `verificar_particion` (de
   `mvp/código/extraer_unidades.py`) y verifica el contrato: que la oración esté en el texto tal
   cual, que el **cuerpo** quede cubierto sin huecos, que ninguna aparición se use dos veces y que
   el orden sea el del texto. Los títulos quedan fuera de la cuenta: no son oraciones.
6. **Escribe en la base**, en una sola transacción: la fila de la **corrida**, las **unidades** y
   **sus tramos** (§5).

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

**(b) Las unidades y sus tramos** — en `unidades`, una por UT: el id `<doc>:Un` y el nombre del
caso (`subtema`). Y en **`unidad_oraciones`**, una fila por oración: su orden dentro de la unidad,
su **tramo** (`desde`, `hasta`, en caracteres sobre el texto del documento) y la **oración literal**
tal como la devolvió el modelo. La literal es la **evidencia** de lo que devolvió el modelo; el
**tramo** es la referencia, y el sello del documento es el guardián: cortar el texto por el tramo
tiene que devolver la literal, palabra por palabra. **No hay números de oración**: un número depende
de la regla con la que se cortó, y con otra regla dice otra cosa; el tramo no.

```sql
-- así se lee una unidad, con sus oraciones y la corrida que las produjo
SELECT u.id, u.subtema, o.n, o.desde, o.hasta, o.texto, c.modelo, c.tokens_salida
FROM unidades u
JOIN unidad_oraciones o ON o.unidad_id = u.id
JOIN corridas c ON c.id = u.corrida_id
WHERE u.documento_id = 'doc8'
ORDER BY u.n, o.n;
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
