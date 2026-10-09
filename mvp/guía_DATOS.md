# Guía de los datos (paso 2)

Cómo se obtienen los datos de las unidades temáticas: qué entra, de dónde viene, cómo se
procesa, qué se entrega y cómo se entrega. Es el procedimiento vigente del MVP (código en
`mvp/código/`, y lo que produce en la base `mvp/código/corpus.db`). El estado del trabajo vive en
`mvp/memoria de trabajo y pendientes.md`; el paso 1
—de dónde salen las unidades— está en [guía_UT.md](guía_UT.md); acá está el paso 2, en detalle.

**Va en tanda:** las unidades del documento se mandan en **una sola llamada**, y la respuesta se
reparte por la **posición en la lista enviada**.

## 1. Qué es un dato

Un dato es **lo que la unidad establece acerca de algo bajo un aspecto**: el `aspecto` dice
bajo qué se considera, el `valor` lo que se establece, y `unidad_valor` la unidad del valor
(«hectáreas», «pesos»), o `null` si no tiene.

- **El alcance es la unidad**, no el documento: se extrae solo de las oraciones de esa unidad.
- **No se inventa**: se registra lo que el texto dice, sin agregar saber externo.
- Lo que la unidad dice de más, o de menos, no se completa desde otro lado.

Un campo `dudas` existió hasta el 08-10 y **se quitó**: nadie lo leía —no entra a la base ni lo
ve el agente— y aparecía en 2 de 21 unidades.

## 2. Qué entra

- **Las unidades de la base** (las escribió el paso 1), armadas en una lista:
  - `caso`: el `subtema` de la unidad,
  - `contenido`: sus oraciones unidas en un párrafo, sin numeración.
  Van **todas** las unidades del documento: la corrida es todo o nada.
- **El texto del documento radicado**: `mvp/documentos/<doc>.md`. Se usa para volver a numerar las
  oraciones y sacar de ahí las de cada unidad (del número a la oración); la unidad que recibe el
  modelo no lleva números. Antes de trabajar se comprueba su **sello** contra la base.
- **El prompt**: `prompt_DATOS`, el que esté **vigente en `mvp/prompts/`**. Su único hueco es
  `{{UNIDADES}}`, que se sustituye con la lista de unidades.

## 3. De dónde viene

- **Las unidades** vienen del paso 1, con su procedimiento en [guía_UT.md](guía_UT.md): el
  documento se numera, el prompt las agrupa y el resultado queda en la base (`unidades`).
- El documento tiene que estar **radicado**: su texto en `mvp/documentos/<doc>.md` y su fila en la
  base. El detalle está en `mvp/consulta-diseno.md` §2–§3.

## 4. Cómo se procesa

Un comando, desde la raíz del repo:

```bash
python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--rehacer]

# por ejemplo
python3 mvp/código/paso2_datos.py doc8
```

Lo que hace:

1. **Arma la lista** de las unidades que faltan: `caso` = el `subtema`, `contenido` = sus
   oraciones en un párrafo.
2. **Sustituye** `{{UNIDADES}}` en el prompt.
3. **Llama al modelo** por `proveedores.llamar` (`mvp/código/proveedores/`; el alias del registro,
   p. ej. `deepseek`): **una sola
   llamada** con todas las unidades, sin agente de por medio.
4. **Lee la respuesta** con `extract_json` (tolera que el JSON venga dentro de una cerca).
5. **Verifica la forma**: que `unidades` sea una lista, que estén todas las posiciones enviadas,
   y que cada unidad traiga `n`, `caso` y `datos` con `aspecto` y `valor`. **No juzga el
   contenido.**
6. **Escribe en la base**, en una sola transacción: la fila de la **corrida** y los **datos**
   (§5). Si lo que volvió no sirve, no escribe ningún dato y deja la corrida marcada como fallida.

Si el documento **ya tiene datos**, no llama al modelo. Rehacerlos es un acto explícito:
`--rehacer`. **Todo o nada:** si la llamada falla, si la respuesta se cortó, si lo que volvió no
sirve o si una unidad no se pudo armar, la corrida queda **fallida** con su motivo y no se escribe
ningún dato; y si el intento era un `--rehacer`, **lo anterior vuelve** —el borrado y la escritura
nueva van en una sola transacción—, así que un intento fallido no se come la extracción buena.

**Por qué en tanda.** Una sola llamada por documento sale más barata y más rápida que una por
unidad, con los mismos datos salvo **granularidad**: la tanda puede juntar en un valor lo que de a
una salen dos («firmado con la alcaldía en febrero» contra «la alcaldía» y «febrero» separados). Lo
que se gana en tiempo y tokens se puede perder en finura; por eso el reparto se revisa. La medición
que fijó esta vía está en `mvp/memoria de trabajo y pendientes.md`.

**Antecedente.** Los datos de `doc4` y `doc6` se hicieron por Muse, a mano, con un mensaje por
unidad; `doc7` fue el primero por la API.

## 5. Qué se entrega

**Dos cosas en la base** (`mvp/código/corpus.db`), y nada en archivos:

**(a) La corrida** — en `corridas`, con el id `<doc>:DATOS`: el modelo y su esfuerzo, el prompt y su
hash, los tokens, los segundos, la fecha, y el `estado` (`exitoso`, o `fallido` con su motivo).

**(b) Los datos** — en `datos`, una fila por dato: el id `<doc>:U<n>:D<j>`, la unidad, el `caso`, el
`aspecto`, el `valor` y la `unidad_valor`. `j` es la **posición en la lista `datos`** que devolvió
el modelo, no un número que venga del texto.

```sql
-- así se lee un dato, con su unidad y la corrida que lo produjo
SELECT d.id, d.caso, d.aspecto, d.valor, d.unidad_valor, u.subtema, u.oraciones,
       c.modelo, c.tokens_salida
FROM datos d JOIN unidades u ON u.id = d.unidad_id
JOIN corridas c ON c.id = d.corrida_id
WHERE d.id = 'doc8:U1:D1';
```

## 6. Cómo se entrega

**Nombre y lugar.** En la base, siempre. La unidad es la que ya estaba (`<doc>:U<n>`), y el dato se
numera por su posición en la lista.

**Qué pasa después con lo que se entrega.** No hay paso siguiente: el dato ya está en la base, y de
ahí lo lee la consulta. Nada se escribe en `mvp/temp/`: ese es el archivo y no se toca.

**Cierre de la corrida.** Si se tocó código, `python3 -m py_compile <archivo>`. Al terminar, se
commitea y se sube **la base** (ahí quedó todo).

## 7. Qué no hace este procedimiento

No decide si un dato es pertinente, no comprueba que el `valor` sea literal en el texto, no
resuelve ambigüedades, no arma la unidad (la arma el código), no garantiza la **granularidad** de
los datos y no radica el documento. Verifica **forma**: que estén todas las unidades enviadas y
que cada una traiga caso y datos con aspecto y valor. El contenido se lee y se juzga aparte.
