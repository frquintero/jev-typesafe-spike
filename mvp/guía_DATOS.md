# Guía de los datos (paso 2)

Cómo se obtienen los datos de las unidades temáticas: qué entra, de dónde viene, cómo se
procesa, qué se entrega y cómo se entrega. Es el procedimiento vigente del MVP (código en
`mvp/código/`, crudos en `mvp/temp/extraccion/`). El estado del trabajo vive en
`mvp/memoria de trabajo y pendientes.md`; el paso 1
—de dónde salen las unidades— está en [guía_UT.md](guía_UT.md); acá está el paso 2, en detalle.

**Va en tanda:** las unidades del documento se mandan en **una sola llamada**, y la respuesta se
reparte en un archivo por unidad.

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

- **Las unidades**, armadas por el código (no por el modelo), **en una lista**:
  - `caso`: el `subtema` que devolvió el paso 1,
  - `contenido`: sus oraciones unidas en un párrafo, sin numeración.
  Van **solo las que todavía no tienen su salida**; las demás se saltan.
- **El archivo de unidades** del paso 1: `mvp/temp/extraccion/<doc>/p1-…out`.
- **El texto del documento**: `mvp/temp/pruebas/<doc>.md`. Se usa para volver a numerar las oraciones
  y sacar de ahí las de cada unidad; la unidad que recibe el modelo no lleva números.
- **El prompt**: `prompt_DATOS`, el que esté **vigente en `mvp/prompts/`**. Su único hueco es
  `{{UNIDADES}}`, que se sustituye con la lista de unidades.

## 3. De dónde viene

- **Las unidades** vienen del paso 1, con su procedimiento en [guía_UT.md](guía_UT.md): el
  documento se numera, el prompt las agrupa y el resultado queda en `p1-…out`.
- El mismo documento entra después al corpus como **documento radicado**; el detalle está en
  `mvp/consulta-diseno.md` §2–§3.

## 4. Cómo se procesa

Un comando, desde la raíz del repo:

```bash
python3 mvp/código/paso2_datos.py <doc> <unidades> <modelo> <rN>

# por ejemplo
python3 mvp/código/paso2_datos.py doc7 p1-doc7-v10-deepseek-r1.out deepseek r1
```

`<unidades>` es el archivo de paso 1: una ruta, o el nombre suelto dentro de
`mvp/temp/extraccion/<doc>/`. `<rN>` es la réplica con su `r` (`r1`, `r2`…).

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
6. **Reparte**: escribe un `.out` por unidad, más el crudo de la llamada (§5).

Si **todas** las unidades ya tienen su `.out`, **no llama al modelo**. Si faltan algunas, manda
solo esas: una corrida cortada se retoma sin repetir —ni volver a pagar— lo hecho. Una repetición
se pide con otro `rN` (`r2`, `r3`…): un crudo no se borra ni se sobrescribe.

**Por qué en tanda.** Medido el 08-10 sobre las seis unidades de `doc7`:

| | De a una (6 llamadas) | En tanda (1 llamada) |
|---|---|---|
| Tiempo | 52,2 s | **24,4 s** |
| Tokens (prompt + completion) | 18.481 | **8.759** |
| Datos | 28 | 27 |

Los mismos datos salvo **granularidad**: en una unidad la tanda juntó en un valor lo que de a una
salieron dos («firmado con la alcaldía en febrero» contra «la alcaldía» y «febrero» separados).
Lo que se gana en tiempo y tokens se puede perder en finura; por eso el reparto se revisa.

**Antecedente.** Los datos de `doc4` y `doc6` se hicieron por Muse, a mano, con un mensaje por
unidad. `doc7` fue el primero por la API: primero de a una (los `.out` que hay), y después la
medición de la tanda que fijó esta vía.

## 5. Qué se entrega

En `mvp/temp/extraccion/<doc>/`:

**(a) El resultado, un archivo por unidad** — `p2-<doc>-u<n>-<rN>.out`:

```json
{"caso": "el nombre de la unidad",
 "datos": [
   {"aspecto": "bajo qué se considera", "valor": "lo que se establece", "unidad_valor": null}]}
```

Es lo que lee el cargador del corpus. `n` es el número de la unidad.

**(b) El crudo de la llamada** — `p2-<doc>-tanda-<rN>.json`: las unidades enviadas, la petición,
la respuesta, los **segundos** y los tokens, y la verificación de forma. Sirve para volver a
verificar sin llamar a la API, y para revisar la granularidad de lo que trajo la tanda.

Un ejemplo real: `mvp/temp/extraccion/doc7/p2-doc7-u3-r1.out` —5 datos, 7,7 s—. El crudo de una
tanda es `p2-<doc>-tanda-<rN>.json`.

## 6. Cómo se entrega

**Nombre y lugar.** `mvp/temp/extraccion/<doc>/p2-<doc>-u<n>-<rN>.{out}` (uno por unidad, el
resultado) y `p2-<doc>-tanda-<rN>.json` (el crudo de la llamada).

**Qué pasa después con lo que se entrega.** Cada dato es una **fila** del corpus:

- su id es `<doc>:U<n>:D<j>`, donde `j` es la **posición en la lista `datos`** (no un número que
  venga del texto),
- lleva `unidad_id`, `caso`, `aspecto`, `valor` y `unidad_valor`,
- y entra a la base cuando se corre `python3 mvp/código/cargar_corpus.py`, que lee el `.out` de
  cada unidad del documento radicado. Si a una unidad le falta su `.out`, el cargador **se
  detiene en el medio** —la reconstruye entera, así que queda a medio armar—; se vuelve a
  correr cuando el archivo esté.

**Cierre de la corrida.** Si se tocó código, `python3 -m py_compile <archivo>`. Al terminar, se
commitea y se sube: los `.out`, el crudo de la tanda y, si el paso cambió, los «sigue» de
`README.md`, `AGENTS.md` y la memoria.

## 7. Qué no hace este procedimiento

No decide si un dato es pertinente, no comprueba que el `valor` sea literal en el texto, no
resuelve ambigüedades, no arma la unidad (la arma el código), no garantiza la **granularidad** de
los datos y no radica el documento. Verifica **forma**: que estén todas las unidades enviadas y
que cada una traiga caso y datos con aspecto y valor. El contenido se lee y se juzga aparte.
