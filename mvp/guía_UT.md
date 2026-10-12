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

- **El texto**: el **documento radicado**, que vive en el **almacén** (`mvp/código/almacen.db`, tabla
  `documentos`): el markdown que dejó el acto del volcado. Un documento sintético, de contenido
  general (divulgación, noticia, nota de servicio), escrito para la prueba. `almacen.texto_de`
  comprueba su **sello** contra el texto guardado antes de entregarlo; el archivo del que salió
  (`mvp/documentos/<doc>.md` o `.txt`) quedó como **procedencia**, no como fuente.
- **El prompt**: `prompt_UT`, el que esté **vigente**. El `.md` de `mvp/prompts/` es la **puerta**: se
  registra solo en la base la primera vez que corre, con su versión, y el acto lee de ahí la
  plantilla. Sus huecos son `{{RELOJ_RADICADO}}` —la fecha del radicado, en el `system`—, y
  `{{TEXTO}}` y `{{RELOJ_SISTEMA}}` —el documento y el «ahora», en el `user`—, y se sustituyen con
  `str.replace` (nunca `str.format`: el texto trae llaves). Es una versión de trabajo: no se afina en
  cada corrida.

**El texto entra entero, con sus títulos y subtítulos**: son contexto para interpretar, no
oraciones. El corte en oraciones lo hace el modelo al devolverlas **literales**, y el código las
ubica en el texto para quedarse con su tramo.

## 3. De dónde viene

- El texto lo escribe la planificación (Frat y Cowork), no el ejecutor. Reglas: sintético, de
  contenido general, y sin ejemplos tomados de los documentos de prueba.
- El mismo texto entra al corpus como **documento radicado**, en un acto aparte y a mano:
  `python3 mvp/código/volcar.py <fuente> [--id NOMBRE] [--coleccion E]` —el markdown queda en el
  almacén, con su sello y su procedencia, y el corpus anota su fila—. El detalle del corpus está en
  `mvp/consulta-diseno.md` §2–§3.

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

Si el documento **ya tiene una UT vigente**, no llama al modelo. Correr otra partición es un acto
explícito: `--rehacer` —la partición anterior **queda** en la base, con su corrida, y la vigente es
la última exitosa—. **Todo o nada:** si la llamada falla, si la respuesta se cortó, si el JSON no se
pudo leer o si la partición no cierra (huecos, solapes, números fuera de rango), la corrida queda
**fallida** con su motivo y no se escribe ninguna unidad; un intento fallido no toca lo anterior.

**Antecedente.** `doc4` y `doc6` se hicieron por Muse: se pegaba el prompt con el texto ya
numerado en un mensaje y se le delegaba la tarea a un agente. Lo medido:
51 s por Muse en `doc6` y 58,3 s por llamada directa en `doc7`; la diferencia no está en el
envoltorio, está en el razonamiento del modelo con este prompt. El procedimiento vigente es el
comando directo.

## 5. Qué se entrega

**Dos cosas en la base** (`mvp/código/corpus.db`), y nada en archivos:

**(a) La corrida** — en `corridas`, con el id **token** del acto (`C000001`…, del contador del
corpus): el paso (`UT`), el documento, el modelo y su esfuerzo, la plantilla (`prompt_id`,
`prompt_version`) y su hash, los **dos relojes** tal como entraron al prompt, los tokens (entrada,
salida y pensamiento), los segundos, el `iniciado` y el `terminado`, y el `estado` (`exitoso`, o
`fallido` con su motivo si el JSON no se pudo leer).

**(b) Las unidades y sus tramos** — en `unidades`, una por UT: el id `<token_UT>:U<n>`
(`C000001:U1`), su `n`, el nombre del caso (`subtema`) y la corrida de la que cuelga
(`corrida_id`). Y en **`unidad_oraciones`**, una fila por oración: su orden dentro de la unidad,
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

**Nombre y lugar.** En la base, siempre. El id de la unidad es `<token_UT>:U<n>` —`n` es la
**posición en el arreglo** que devolvió el modelo, no el orden de lectura: el corte no es contiguo—,
y cada oración se guarda con su **tramo** (`desde`, `hasta`) y su literal.

**Qué pasa después con lo que se entrega.** El paso 2 lee esas unidades **de la base** y escribe
los datos. Nada se escribe en `mvp/temp/`: ese es el archivo y no se toca.

**Cierre de la corrida.** Si se tocó código, `python3 -m py_compile <archivo>`. Al terminar, se
commitea y se sube **la base** (ahí quedó todo).

## 7. Qué no hace este procedimiento

No decide qué es pertinente, no juzga el contenido de las unidades, no radica el documento, no
extrae datos y no mide calidad. Verifica **forma**: que la cobertura esté completa y que no haya
solapes. El contenido se lee y se juzga aparte.
