# El MVP de Zettel · diseño

**Qué es.** El diseño vigente del MVP: **el texto y las dos bases, los cuatro actos que las llenan,
la consulta completa y cómo se juzga**. El estado —qué hay radicado y qué sigue— vive en
`mvp/memoria de trabajo y pendientes.md`, que es la fuente única.

---

## 1. Las tres etapas y sus actos

Una **fuente** entra por el volcado y queda como **documento radicado** en el almacén; UT y DATOS lo
convierten en **unidades** y **datos** en el corpus; el ORQ recibe una **pregunta** y entrega una
**respuesta** con lo que el corpus establece —o dice con precisión que no está—.

| Etapa | Acto | Producto | Base dueña (asigna el token) |
|---|---|---|---|
| **I · volcado** | `volcar.py` | el markdown original, su sello y su procedencia | **almacén** |
| **II · extracción** | `paso1_unidades.py` (UT) | unidades y oraciones con sus tramos | **corpus** |
| **II · extracción** | `paso2_datos.py` (DATOS) | datos | **corpus** |
| **III · consulta** | `orq/orquestador.py` (ORQ) | la pregunta radicada, la respuesta, los casos leídos y las llamadas | **corpus** |

```bash
python3 mvp/código/volcar.py <fuente> [--id NOMBRE] [--coleccion E] [--modelo M] [--esfuerzo E]
python3 mvp/código/paso1_unidades.py <doc> [--modelo M] [--esfuerzo E] [--prompt UT] [--rehacer]
python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--esfuerzo E] [--rehacer]
python3 mvp/código/orq/orquestador.py (--texto "…" | <archivo> [--numero N]) --dominio E [--modelo M] [--esfuerzo E]
```

**El token es del acto, no de la etapa.** La etapa II tiene dos actos y cada uno inyecta su propio
reloj: con un token por etapa, «¿qué hora se inyectó?» devolvería dos. Cada acto **imprime su token**
al cerrar (`paso1 doc11 · corrida C000123`).

**Cada base numera sus tokens** (`A` el almacén, `C` el corpus): el prefijo no hace falta para que no
colisionen —no hay espejo de las **corridas** del volcado—, sino para poder **citar un token sin
ambigüedad**.

**Un acto, una fila.** Cada ejecución deja su corrida y su token: no se pisa ni se borra, y los
productos apuntan al acto que los produjo. **Cada etapa es un acto manual y separado, y nada se
dispara solo**; el modelo y el esfuerzo de cada uno se leen de la tabla `ajustes` del corpus
(`volcado`, `UT`, `DATOS`, `ORQ`) y se pueden pisar por llamada —**línea de comandos > base > código**—.

## 2. Las dos bases

1. **El archivo no puede ser el original.** El corpus se reseteó dos veces y se llevó los documentos
   con él: el archivo de Zettel tiene que ser un lugar, no un proyecto que se vacía.
2. **Radicar no debería ser copiar un archivo.** Un acto sobre la base no depende de dónde estaba el
   `.md`, ni de que nadie lo mueva, ni de que el sistema de archivos se acuerde de su fecha.
3. **Falta la procedencia.** Se guardaba la ruta y el sello, y no de qué archivo salió, ni con qué
   nombre, ni cuándo se lo modificó por última vez.

**El almacén** (`mvp/código/almacen.db`, cuatro tablas) guarda **el texto volcado en markdown —el
original para Zettel—**, su **sello** (sha256: guardián de que no se tocó) y su **procedencia** (el
nombre, la ruta y el mtime de la fuente). El archivo del que se volcó **no es fuente**. La plantilla
del volcado y el contador viven acá, en la base del acto: si el corpus se resetea, el almacén se
sigue explicando solo.

**El corpus** (`mvp/código/corpus.db`, doce tablas) **es el centro**: no hay archivos intermedios, y
todo lo que los actos producen queda ahí encadenado **por el token** para poder hacer la **traza
completa** —de una respuesta al dato, a la unidad, a la oración del documento, y a la corrida que lo
produjo—. El esquema, con las dos bases, está en el **apéndice A**.

**El vínculo: un espejo fino.** Entre archivos no hay claves foráneas, así que **el almacén es el
dueño** del texto, del sello y de la procedencia, y **el corpus conserva una fila fina** de
`documentos` (`id`, `dominio`, `sello`, `fecha_radicacion` y la ruta de la fuente) para que sus
propias claves foráneas existan y para que el ORQ resuelva un dominio y el reloj del radicado
funcione sin abrir dos bases. **El sello es lo que ata los dos**: si no coinciden, hay algo roto. Los
dos escritos van en **una sola transacción** (`ATTACH`), y por eso **ninguna de las dos bases usa
WAL**: con WAL la escritura entre archivos deja de ser atómica. Los actos de después leen el texto
del almacén (`almacen.texto_de`, que comprueba el sello antes de entregarlo).

**Radicar es fijar.** Un documento radicado no cambia: si su texto cambia, eso es **otro documento**,
con su radicación y su fila propias. Y si el texto guardado no coincide con su **sello**, el acto **se
detiene y reporta**.

**Cuándo se guarda un sello.** Cuando el texto vive **fuera de la base** —R, que es un archivo— o
cuando **el mismo hecho vive en dos sitios** y hay que atarlos: el del documento empareja el espejo
del corpus con el original del almacén. El de la plantilla **no se guarda**: su texto es la fila que
la identifica (`id` y versión), y una versión inscrita no se toca.

**Qué no guarda el corpus, y por qué:**

- **El texto del documento**: vive en el almacén. De cada oración guarda **la literal y su tramo**;
  **no hay números de oración**, porque el número depende de la regla con la que se cortó.
- **El crudo de las llamadas**: la petición se rearma con lo que ya está en la base. Se pierde lo que
  el modelo dijo de más: su razonamiento.
- **Los reintentos**: cada intento es su fila. La extracción **vigente no se guarda, se deriva** —la
  última corrida exitosa; en DATOS, la última sobre esa UT—.
- **La vigencia**: ni puntero, ni columna, ni índice parcial. Se **deriva** —la última corrida exitosa;
  en DATOS, la última sobre esa UT—, y el acto la resuelve una vez al abrir y la usa para leer (§9).

**Por qué SQLite.** La forma se elige por **forma de acceso**, y acá lo que manda es leer un caso
entero y filtrar por dominio y por caso: eso pide claves, foráneas y consultas, no un molde único.
SQLite viene en la biblioteca estándar, no tiene servidor y el archivo es uno. **No es un derivado
regenerable**: lo que entra, queda, y no se reproduce corriendo nada de nuevo —cada corrida se paga—.

**El vacío legítimo** es de nivel unidad: una unidad cuyas oraciones no establezcan nada. La carga
puede avisarlo.

## 3. Conservar y poder trazar

La decisión que sostiene todo lo demás: **la corrida nueva no borra la anterior**; la vigente se
**deriva**.

| | **A · conservar los productos** (elegida) | B · identificar sin conservar |
|---|---|---|
| Qué hace | la corrida nueva no borra la anterior; la vigente se deriva | se sigue borrando; el acto guarda sello y procedencia de su material |
| Qué promete | reconstruir la partición y los datos de cualquier intento, y **comparar rondas** | comprobar una reconstrucción, no hacerla |
| Costo | identidad por corrida; unas lecturas pasan a ser por token | nada |

**Por qué A, y no por elegancia:** comparar prompts y corridas **es la metodología** —acuerdo entre
particiones, «el ejemplo manda», el banco de DATOS—, y con B la corrida anterior se pierde.

**Cambia la identidad, no la tabla:** `unidades` es única por **`(corrida_id, n)`** en vez de
`(documento_id, n)`, y los ids llevan el token del acto (`<token_UT>:U<n>`,
`<token_DATOS>:U<n>:D<j>`). Sin eso, rehacer DATOS sobre la misma UT repite ids.

**`--rehacer` es correr otra vez**, no borrar: la partición o los datos anteriores **quedan** con su
corrida, y las dos se pueden comparar. **Todo o nada**: si la llamada falla, si la respuesta se cortó,
si el JSON no se pudo leer o si la partición no cierra, la corrida queda **fallida** con su motivo y
no se escribe ningún producto; un intento fallido no toca lo anterior.

**Qué se promete de un intento.** Se registran **éxitos y fallos controlados** (la fila se escribe al
cerrar el acto). Una muerte abrupta antes de escribir **no deja constancia**, y no se promete. Del
**código** tampoco se promete reconstrucción: el commit no conserva el árbol sucio; el día que haya
que auditar una corrida con árbol sucio, se guarda el diff **entonces**.

**La consecuencia, en código:** sin borrado no hay restauración. El acto es «llamo; si falla, escribo
la corrida fallida; si no, escribo corrida y productos en una transacción». Se cayó maquinaria
—`conservar_efectiva`, `borrar_corridas`, el `rollback` de restauración, los ids determinísticos—, no
se agregó.

## 4. La llamada: dos mensajes y dos relojes

Rige para **todos** los prompts —`paso1_unidades.py`, `paso2_datos.py`, `orq/armar_prompt.py`— y quien
la implementa es `mvp/código/mensajes.py` (`partir`).

1. **Dos marcas.** Un prompt de trabajo trae `[SISTEMA]` para lo invariante y, para el material de la
   llamada, `[TAREA]` **o** `[USUARIO]` (las dos valen). Las marcas **no llegan al modelo**.
2. **Qué va en cada uno.** El `system` lleva la tarea, las reglas, el formato de salida **y los
   ejemplos** —todo lo que no cambia de una llamada a otra—. El `user` lleva **el material de esta
   llamada** —el documento, las unidades, los casos, la pregunta— **y el pedido, al final**.
3. **Por qué así.** El `system` es el **prefijo invariante**, y es lo que se puede cachear (el reparto
   medido está en la memoria). Poner en el `system` algo que cambia por llamada se paga en cada
   corrida. En la familia `responses` viaja como `instructions`, y en las otras dos como el primer
   mensaje del sistema. **En las corridas de la base el `hit` aparece solo con DeepSeek; con Luna es 0
   en todas** (§9).
4. **Los relojes, en todo prompt, y cada uno en su lugar.** Dos, con el mismo formato
   —`[día-mes-año: hora]`—, armados por `mvp/código/relojes.py`:
   - **el del radicado** (`{{RELOJ_RADICADO}}`): cuándo entró el documento a Zettel
     (`documentos.fecha_radicacion`). Es **invariante por documento**: va en el `system`.
   - **el del sistema** (`{{RELOJ_SISTEMA}}`): el «ahora» de la corrida. **Cambia en cada corrida**:
     va en el `user`, con el material y **al final, después del texto**, para que el prefijo común se
     siga reusando y lo que cambia quede al final.

   Van **etiquetados**: ninguno es dato del documento, y el prompt lo dice. Lo propio de la consulta
   —los relojes de **todos** los documentos del dominio, y el del sistema congelado una sola vez al
   abrirla— está en §7.2.
5. **Los huecos se rellenan con `str.replace`**, nunca con `str.format`: el texto del documento puede
   traer llaves. Cada acto pasa los suyos: `RELOJ_RADICADO`, `RELOJ_SISTEMA`, `TEXTO`, `UNIDADES`,
   `CASOS`, `PREGUNTA`.
6. **El material va delimitado** (`<texto> … </texto>`) y **el pedido, al final del `user`**.

**El sistema es el único canal**: lo que el acto no ponga, el agente no lo sabe. Y si el prompt pide un
hueco que el acto no llena, el acto **se detiene**: no se llama al modelo con el hueco crudo.

## 5. Etapa I · El volcado (el almacén)

El volcado es un acto: toma una fuente en cualquier forma, le **marca los encabezados** con la
jerarquía que decide el modelo (plantilla `prompt_volcado`) y guarda ese markdown. **Ese markdown es
el original para Zettel**: todo lo de después —las oraciones, los tramos, los datos— se cuenta sobre
él. **Este acto es la radicación.**

Lo que hace, en orden:

1. **Lee la fuente** y su procedencia (nombre, ruta, mtime). Si ya es markdown, la normaliza igual.
2. **Pide el índice** con `prompt_volcado` (los encabezados, con su `padre`).
3. **Verifica y arma el markdown.** Nada del texto se reescribe: solo se le insertan las marcas `#`.
4. **Escribe, en una sola transacción**: la fila del almacén y **el espejo en el corpus**.
5. **Idempotente por id**: si el id ya está con el **mismo sello**, no hace nada; si está con otro
   texto, **se detiene** —eso es otro documento, y va con otro nombre—. **La fuente no es candado**:
   volver a volcar la misma fuente, con otro id, es otro documento; los distingue la fecha.

**Qué verifica, antes de escribir:**

| chequeo | qué protege |
|---|---|
| cada título está en el texto, **literal** y en orden | el modelo no reformula |
| `n` = 1..k y `padre` = 0 o un número anterior | la única regla mecánica del prompt |
| **los subárboles son contiguos** | que la jerarquía sea representable como niveles de markdown |
| **quitar las marcas devuelve la fuente, byte a byte** | el volcado no inventa ni pierde nada |
| **idempotencia**: re-armar un markdown ya marcado no lo cambia | volcar dos veces no lo toca |
| índice **vacío** | un documento sin encabezados es un documento válido |

Si algo falla, la corrida queda `fallida` con su motivo **y no se escribe nada**.

**Las marcas: qué se toca y qué no.** Se inserta `#` (una por nivel) al principio de la línea del
encabezado; si la línea ya traía un marcador markdown, **se descarta y se pone el canónico**. **Nada
más se toca**: ni los saltos, ni los espacios, ni los números que el texto ya traía. No se normaliza
el texto: eso sería *reescribir* y rompería el chequeo de ida y vuelta.

**Lo que se decidió, y por qué:**

| decisión | por qué |
|---|---|
| **el id es el nombre** que se da al volcar, y **la identidad es el volcado y su fecha** | un id derivado del contenido haría ilegibles las referencias (`sol:U1`); el sello es guardián del texto, no identidad: el mismo texto volcado en otra fecha es otro documento |
| **el corpus conserva una fila fina** | sus claves foráneas necesitan un `documentos` vivo, y el ORQ necesita resolver dominios |
| **`coleccion` es una etiqueta por documento** | una tabla de colecciones con pertenencia es para cuando un documento tenga que estar en varias; hoy no lo necesita |
| **el índice no se guarda** | se deriva del markdown: las líneas que empiezan con `#` y su nivel |
| **no hay versión del volcado** | el markdown es el documento y no tiene versiones; y el armador es el commit de git, que ya está versionado |
| **el volcado no tiene `--rehacer`** | un documento radicado no se mueve: re-volcar con otra cosa es radicar otro documento |

**Tres tiempos, y no se mezclan:** la fecha propia del documento (si el texto la declara) es un
**dato**; el `fecha_modificacion` de la fuente es **procedencia**; la `fecha_radicacion` es el
**tiempo de transacción** y la pone la base.

## 6. Etapa II · La extracción (UT y DATOS)

### 6.1. Las unidades temáticas (UT)

Una UT es **un asunto y todo lo que el texto dice de ese asunto**: una o varias oraciones que
desarrollan el mismo núcleo, aunque estén separadas en el texto. El nombre de la UT dice **qué se
dice** de las cosas, no solo cuáles son («el tamaño de la tripulación», no «la tripulación»).

**Para qué cierra.** La UT es el **ámbito donde se cierran las referencias**: una oración que por sí
sola no cierra —«esa energía», «allí»— cierra en su unidad, porque el núcleo y sus satélites son los
referentes que nombra y las oraciones que se refieren a ellos van juntas. **El nombre del caso es
parte de ese mecanismo**: nombra el núcleo y **trae su antecedente**.

- Lo que une oraciones es **el asunto**, no el lugar, el objeto ni la persona.
- Un cambio de párrafo **no** separa por sí solo.
- **Cada oración va en una sola UT.**
- **El cierre es su función:** si el antecedente de lo que sus oraciones dicen está en la unidad —en
  otra de sus oraciones o en el nombre del caso—, la unidad cierra; si no, queda abierta.

**Qué entra.** El **documento radicado** —el texto se lee del almacén, entero, con sus títulos y
subtítulos: son contexto para interpretar, no oraciones— y la plantilla `prompt_UT` **vigente**: la
última versión inscrita en la base (`prompts`), que es donde vive y de donde el acto la lee. Sus
huecos son `{{RELOJ_RADICADO}}`,
`{{TEXTO}}` y `{{RELOJ_SISTEMA}}`.

**Cómo se procesa.** Un comando, desde la raíz del repo:

```bash
python3 mvp/código/paso1_unidades.py <doc>        # por ejemplo: paso1_unidades.py sol
```

1. **Toma el texto** del documento radicado, entero, sin numerar y sin marcar.
2. **Sustituye** `{{TEXTO}}`: el prompt va como `system` y el texto —delimitado— como `user`.
3. **Llama al modelo** por `proveedores.llamar`: una sola llamada de texto a JSON, sin agente.
4. **Lee la respuesta** con `extract_json` (tolera que el JSON venga dentro de una cerca de código).
5. **Ubica cada oración en el texto** con `verificar_particion` (`extraer_unidades.py`) y verifica el
   contrato: literalidad, cuerpo cubierto sin huecos, ninguna aparición usada dos veces y orden del
   texto. Los títulos quedan fuera de la cuenta.
6. **Escribe, en una sola transacción**, la corrida, las unidades y sus tramos.

Si el documento **ya tiene una UT vigente**, no llama al modelo. Correr otra partición es explícito:
`--rehacer`.

**Qué entrega.** Dos cosas en la base, y nada en archivos:

- **La corrida** (`corridas`), con el token del acto (`C000001`…): el paso (`UT`), el documento, el
  modelo y su esfuerzo, la plantilla y su versión, los **dos relojes** tal como entraron al
  prompt, los tokens, los segundos, `iniciado` y `terminado`, y el `estado`.
- **Las unidades y sus tramos**: en `unidades`, una por UT —id `<token_UT>:U<n>`, su `n`, el `subtema`
  y su `corrida_id`—; y en `unidad_oraciones`, una fila por oración con su orden, su **tramo**
  (`desde`, `hasta`, en caracteres sobre el texto del documento) y la **oración literal** tal como la
  devolvió el modelo. La literal es la **evidencia**; el tramo es la **referencia**: cortar el texto
  por el tramo tiene que devolver la literal, palabra por palabra. **No hay números de oración.**

```sql
-- así se lee una unidad, con sus oraciones y la corrida que las produjo
SELECT u.id, u.subtema, o.n, o.desde, o.hasta, o.texto, c.modelo, c.tokens_salida
FROM unidades u
JOIN unidad_oraciones o ON o.unidad_id = u.id
JOIN corridas c ON c.id = u.corrida_id
WHERE u.documento_id = 'sol'
ORDER BY u.n, o.n;
```

**Nombre y lugar.** El id de la unidad es `<token_UT>:U<n>`: `n` es la **posición en el arreglo** que
devolvió el modelo, no el orden de lectura —el corte no es contiguo—, así que no se supone
contigüidad. **Qué no hace:** no decide qué es pertinente, no juzga el contenido, no radica el
documento, no extrae datos y no mide calidad: verifica **forma**.

### 6.2. Los datos (DATOS)

Un dato es **lo que la unidad establece acerca de algo bajo un aspecto**: el `aspecto` dice bajo qué
se considera, el `valor` lo que se establece, y `unidad_valor` la unidad del valor («hectáreas»,
«pesos»), o `null` si no tiene.

- **El alcance es la unidad**, no el documento: se extrae solo de las oraciones de esa unidad.
- **No se inventa**: se registra lo que el texto dice, sin agregar saber externo.

**Va en tanda:** las unidades del documento se mandan en **una sola llamada**, y la respuesta se
reparte por la **posición en la lista enviada**. Una sola llamada por documento sale más barata y más
rápida que una por unidad, con los mismos datos salvo **granularidad** —la tanda puede juntar en un
valor lo que de a una salen dos—; por eso el reparto se revisa (la medición, en la memoria).

**Qué entra:** **todas** las unidades del documento —la corrida es todo o nada— armadas en bloques,
un bloque por unidad: `caso:` el `subtema`, y `satélites:` sus oraciones, **una por línea** y
numeradas desde `[1]` dentro del bloque. Esa numeración es del bloque, no del documento: **el paso 2
no corta ni numera nada**. Antes de trabajar comprueba el **sello** con `almacen.texto_de`. Y la
plantilla `prompt_DATOS` vigente, con los huecos `{{RELOJ_RADICADO}}`, `{{UNIDADES}}` y
`{{RELOJ_SISTEMA}}`.

**Cómo se procesa:**

```bash
python3 mvp/código/paso2_datos.py <doc>           # por ejemplo: paso2_datos.py sol
```

1. **Arma la lista** de **todas** las unidades del documento —la corrida es todo o nada—: `caso` = el
   `subtema`, `contenido` = sus oraciones.
2. **Sustituye** `{{UNIDADES}}` en el prompt.
3. **Llama al modelo** por `proveedores.llamar`: **una sola llamada** con todas las unidades.
4. **Lee la respuesta** con `extract_json`.
5. **Verifica la forma**: que `unidades` sea una lista, que estén todas las posiciones enviadas, y que
   cada unidad traiga `n`, `caso` y `datos` con `aspecto` y `valor`. **No juzga el contenido.**
6. **Escribe, en una sola transacción**, la corrida y los datos.

Si el documento **ya tiene una tanda vigente**, no llama al modelo; correr otra es `--rehacer`.

**Qué entrega.** La corrida (`DATOS`), con la **corrida de UT de la que salieron las unidades**
(`corrida_origen`), los dos relojes, los tokens y el estado; y **los datos** en `datos`, una fila por
dato —id `<token_DATOS>:U<n>:D<j>`, la unidad de la que sale, el `caso`, el `aspecto`, el `valor` y la
`unidad_valor`—. `j` es la **posición en la lista `datos`** que devolvió el modelo, no un número del
texto.

```sql
-- así se lee un dato, con su unidad y la corrida que lo produjo
SELECT d.id, d.caso, d.aspecto, d.valor, d.unidad_valor, u.id, u.subtema,
       c.modelo, c.tokens_salida
FROM datos d JOIN unidades u ON u.id = d.unidad_id
JOIN corridas c ON c.id = d.corrida_id
WHERE d.id = 'C000003:U1:D1';
```

**Qué no hace:** no decide si un dato es pertinente, no comprueba que el `valor` sea literal en el
texto, no resuelve ambigüedades, no arma la unidad, no garantiza la **granularidad** y no radica el
documento. Verifica **forma**; el contenido se lee y se juzga aparte.

### 6.3. Lo que comparten

- **El sello manda**: antes de trabajar, el acto comprueba que el texto del almacén coincida con el
  sello del documento. Si no coincide, se detiene y reporta.
- **Leen de la base, no de archivos**: UT lee el texto del almacén; DATOS lee las unidades de
  `unidades` y `unidad_oraciones`.
- **Todo o nada, y el fallo no toca lo anterior**: la corrida queda `fallida` con su motivo y no se
  escribe ningún producto.
- **Vigencia derivada**: la vigente es la última corrida exitosa —en DATOS, la última sobre esa UT—.
- **Cierre**: si se tocó código, `python3 -m py_compile <archivo>`; al terminar, se commitea y se sube
  **la base** (ahí quedó todo). `mvp/temp/` es archivo: no se corre desde ahí, no se lee, no se
  escribe.

## 7. Etapa III · La consulta

El **primer recorrido completo** de Zettel sobre el corpus: recibir una pregunta y entregar una
respuesta con lo que el corpus establece —o decir con precisión que no está—, con el recorrido
registrado. Sin Jev y sin búsqueda externa.

### 7.1. Los papeles

**El código es el ORQUESTADOR y el LLM es el AGENTE ENCARGADO** (D1). El agente es **stateless**: cada
llamada es una interacción nueva y solo sabe lo que va en el prompt; el orquestador lleva la memoria y
compone cada llamada.

| | Orquestador (el código) | Agente encargado (el LLM) |
|---|---|---|
| Prepara | configuración y rutas; el dominio y sus documentos; las anclas; la lista de casos; el prompt de cada llamada | — |
| Sirve | los datos del caso que el agente pide (la única herramienta) | — |
| Hace | ejecuta la herramienta, lleva los mensajes, registra la corrida y la respuesta | — |
| Piensa | **nada**: no interpreta la pregunta, no elige casos, no juzga la entrega | qué casos pedir; qué responder; cuándo parar |
| **Memoria** | los mensajes de la consulta | **ninguna** |
| Propone | — | la respuesta, en el JSON de `RESPUESTA_JSON` |
| Juzga | **no juzga** | no ejecuta ni calcula |

El juicio no se pierde: vive en la **evaluación** (§8), fuera del ORQ.

### 7.2. Las entradas

**La pregunta: se carga, y se radica al entregar.** Entra por el acto: de un archivo
(`mvp/consulta/preguntas_<doc>.md`, una pregunta por línea) o **tecleada**, con `cargar_pregunta.py`
(`cargar`), y el **dominio** lo lleva el acto por línea de comandos. El archivo es una **fuente**, no
el canal: de un archivo se carga **una** pregunta (si trae varias, se dice cuál con `--numero N`).

**La radicación es el cierre.** Mientras el ciclo corre, la base se abre **en solo lectura**: de esa
pregunta no hay nada escrito. Al cerrar **con el JSON de `RESPUESTA_JSON`**, el acto escribe —en una
sola transacción— la fila de `preguntas` (texto, dominio, fuente y la fecha y la hora del cierre), la
corrida y la respuesta. Si el ciclo **no entrega**, escribe **solo la cédula**: `fallido`, con su
motivo, el texto en `pregunta_texto` y `pregunta_id` nulo. **No hay pregunta radicada**, y con eso no
quedan preguntas sin respuesta. La misma pregunta se radica tantas veces como se corra y **convive**
(`q1`, `q2`…, la hora las distingue). Hoy **nadie lee `preguntas`**: es el registro de lo preguntado,
y su consumidor es Zettel.

**R.** `mvp/código/R.json` es **un JSON que lee el ORQUESTADOR**. El agente **no lo ve**: R se aplica
ofreciendo —qué fuentes se admiten, qué herramientas se ofrecen, qué operaciones existen—, no se le
explica.

| Clave | Qué dice | Quién la aplica |
|---|---|---|
| `fuentes_admitidas` | la única fuente es el documento radicado | el ORQ |
| `herramientas` | qué se le ofrece; lo que no está, no se le da | el ORQ, al armar `tools` |
| `operaciones` | ninguna: sin aritmética ni fechas calculadas | el ORQ, no ofreciendo nada |

Se fija antes de la corrida y queda registrada en la fila de la corrida. **Los topes de turnos y de
llamadas no son R**: son guardias del orquestador (§7.8). **Las condiciones que el código no puede
aplicar** —«tu saber no es premisa», «los conflictos se muestran y no se eligen», «lo que no se cierra
se entrega explícito, con la brecha», «no hay interacción con el usuario»— no van en R: son reglas del
agente, y hoy **no están escritas en ninguna parte** (§9).

**El dominio es una entrada, no una inferencia.** El ORQ no lee la pregunta: no saca palabras clave ni
elige documentos. Recibe el dominio elegido (`GENERAL`), lo **resuelve por pertenencia** a la tabla y
le pasa al agente **todos** los casos de ese dominio. El que une la pregunta con la base es el
**agente**. El sentido de `dominio` es el de la tabla de homónimos del marco: la **etiqueta** que
designa el conjunto de documentos que el usuario elige consultar; de él salen los casos que se ofrecen
y con ellos el corpus **acota** qué respuestas puede sostener, pero **no fija las posiciones
admisibles** —eso es del aspecto—. Dos cosas del código, para no leerlo de más: `documentos.dominio`
lleva **una** etiqueta por documento (no hay tabla de grupos), y el límite lo aplica **la lista de
casos** (`obtener_datos_del_caso` rechaza un id que no esté), no R.

**Los relojes.** La regla general está en §4. Acá, lo propio de la consulta: **el del radicado** van
los de **todos** los documentos del dominio, una línea por documento, en el `system`; **el del
sistema** se toma **una sola vez al abrir** la consulta (`orq/anclas.py`) y queda **congelado** —si
cambiara entre turnos, rompería el prefijo y la consulta razonaría con dos «ahora» distintos—, va en
el `user`, después del material, y queda en la traza.

### 7.3. El recorrido

| # | Paso | Archivo | Qué hace |
|---|---|---|---|
| 1 | Leer la configuración | `orq/leer_config.py` | las rutas de entrada y las guardias |
| 2 | Cargar la pregunta | `cargar_pregunta.py` (`cargar`) | el texto y su **fuente**: un archivo, o el chat |
| 3 | Leer R | `orq/leer_r.py` | el JSON del orquestador |
| 4 | Abrir la base | `orq/abrir_db.py` | `corpus.db`, **solo lectura** |
| 5 | Resolver el dominio | `orq/resolver_dominio.py` | la etiqueta → sus documentos (pertenencia, sin juicio) |
| 6 | Listar los casos | `orq/listar_casos.py` | `unidad_id` y `caso`, sin aspectos ni valores |
| 7 | Armar las herramientas | `orq/armar_herramientas.py` | R ∩ las que existen |
| 8 | Armar los mensajes | `orq/armar_prompt.py` + la plantilla `ORQ` | el `system` (radicados y lógica) y el `user` (casos, pregunta, ahora) |
| 9 | El bucle | `orq/llamar_modelo.py`, `ejecutar_herramienta.py`, `obtener_datos_del_caso.py`, `bucle.py` | llama, ejecuta lo que el agente pide, apila, y termina con la respuesta |
| 10 | Registrar | `orq/registrar_consulta.py` | la corrida y la respuesta, en la base |

`orq/orquestador.py` es el `main`: los llama en ese orden y nada más. Cada paso vive en su archivo;
`orq/config.json` tiene las rutas de **entrada** y las guardias —la pregunta, el dominio y el modelo
no van ahí: la pregunta se carga, el dominio lo lleva el comando, y el modelo y el esfuerzo salen de
la fila `ORQ` de `ajustes`—. Lo que el ORQ produce no se configura: va a la base.

**La petición.** El `system` lleva lo que no cambia entre turnos: los radicados, la lógica del agente y
la forma de la respuesta. El `user`, el material de la consulta: los casos del dominio, la pregunta y
el «ahora», al final. En cada turno siguiente el historial crece con el `assistant` y los mensajes
`tool`:

```
turno 1: ['system', 'user']
turno 2: ['system', 'user', 'assistant', 'tool', 'tool', …]
```

### 7.4. La memoria es del orquestador (el agente es stateless)

El agente no recuerda nada entre llamadas: es una función pura, `agente(prompt + mensajes) -> acción`
(patrón *stateless reducer*, factor 12 de 12-Factor Agents). **La API también es stateless**: cada
turno **reenvía todo** el historial —en DeepSeek no hay `previous_response_id` ni estado del lado del
servidor—; lo que abarata el reenvío es el **caché de prefijo**, y lo que se paga es **cada resultado
nuevo**.

**La mecánica del bucle**, verificada en `test_tool_calling/` con llamadas reales:

- **El orquestador no tiene estado entre turnos.** El mensaje del asistente vuelve tal cual —con sus
  `tool_calls` y su `reasoning_content`, que la API **exige** devolver cuando hay `tools`— y el
  resultado de la herramienta entra como un mensaje `role: "tool"` con su `tool_call_id`.
- **El LLM no calcula: pide.** Y no encadena por sí solo: si una respuesta pidiera dos pasos, el valor
  intermedio lo lleva el agente en la conversación, no el código. Cada paso cuesta un turno.
- **El código valida la forma, no la intención**: los argumentos de una herramienta pueden ser JSON
  inválido o traer un id inventado; eso vuelve por el canal `tool` como error, y el agente puede
  corregirse.

### 7.5. Las herramientas: dos

```json
{"type": "function",
 "function": {
   "name": "obtener_datos_del_caso",
   "description": "Devuelve todos los datos de un caso del dominio. Se pide por su id.",
   "parameters": {
     "type": "object",
     "properties": {"unidad_id": {"type": "string",
       "description": "El id del caso, tal como figura en la lista de casos."}},
     "required": ["unidad_id"],
     "additionalProperties": false}}}
```

Devuelve el caso completo: `unidad_id`, `caso` y **todos** sus datos, cada uno con su id (`aspecto`,
`valor`, `unidad_valor`). La lectura es por caso entero: el agente no filtra por aspecto antes de
leer. La segunda es la pregunta al usuario, y el agente la usa cuando la pregunta **admite dos o más
respuestas plausibles**:

```json
{"type": "function",
 "function": {
   "name": "preguntar_al_usuario",
   "description": "Pregunta al usuario cuando la pregunta admite dos o más respuestas plausibles. Poné la situación y las respuestas posibles.",
   "parameters": {
     "type": "object",
     "properties": {"pregunta": {"type": "string"},
                    "opciones": {"type": "array", "items": {"type": "string"}}},
     "required": ["pregunta", "opciones"],
     "additionalProperties": false}}}
```

**El ciclo termina ahí** (D26): no la responde y no ejecuta nada —la respuesta del usuario sería K de
la consulta, no un dato del corpus—. **La pregunta no queda registrada**: sin entrega no hay fila en
`consultas` ni en `consulta_llamadas`, y del pedido del agente queda solo el `motivo` de la cédula
(§9).

**No hay herramienta de entrega**: la respuesta es el **mensaje final** del agente, y el ORQ la lee de
ahí (§7.7).

**R se aplica al ofrecer.** La lista de `tools` es R ∩ lo que existe: lo restringido no se da, así que
el agente no puede pedirlo; y si la herramienta no existe, no se ofrece aunque R la admita. **El
dominio va cerrado por el código, no por argumento**: la herramienta no acepta `dominio`; el ORQ lo
resuelve por pertenencia y valida cada id contra los casos del dominio, así que el agente no puede
ampliar el alcance cambiando un argumento.

**Qué le queda al código:** solo lo **mecánico** —parsear los argumentos y saber qué herramienta
ejecutar—. No comprueba la entrega, ni la cobertura, ni que un dato citado exista. El ORQ orquesta; no
juzga.

### 7.6. El prompt del agente

Vive en la base —la plantilla `ORQ`, con su versión—, **un solo texto** con dos partes marcadas:
`[SISTEMA]` (lo que se conserva entre turnos) y `[TAREA]` (lo que depende del dominio y de la
pregunta). `armar_prompt.py` lo parte y devuelve los dos mensajes. Los huecos son `{{RELOJ_RADICADO}}`, `{{CASOS}}`, `{{PREGUNTA}}`
y `{{RELOJ_SISTEMA}}`, rellenados con `str.replace`.

**Prompt 3 y prompt 4.** El prompt del agente es el que Frat llama **prompt 3**: la plantilla `ORQ` v1,
la única inscrita, que es la que corre y la que se cita abajo. **Prompt 4** —la sonda de
`preguntar_al_usuario`— **no está inscrito**: no es lo que corre, y su reparto era otro (la lógica al
final del `[TAREA]`, después del «ahora»).

```
[SISTEMA]
RELOJES (la fecha de radicación de los documentos del dominio; no es dato del documento)
{{RELOJ_RADICADO}}

LÓGICA DEL AGENTE ENCARGADO:
1. Escoge los id de los casos que con probabilidad mayor al 80% contengan la respuesta a la pregunta.
2. Si no hay casos que cumplan la condición anterior, pasa al punto 5.
3. Utiliza la HERRAMIENTA obtener_datos_del_caso para obtener los datos de los casos seleccionados. Podés pedir varios casos en un mismo turno.
4. Analiza los datos: si hay una respuesta plausible, armá la respuesta; si hay dos o más respuestas plausibles, usá la HERRAMIENTA preguntar_al_usuario; si no hay ninguna, pasa al punto 5.
5. Diligencia el JSON en RESPUESTA_JSON.

Responde solo con el JSON.

RESPUESTA_JSON:
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_los_datos", "respuesta": ""}

[TAREA]
CASOS:
{{CASOS}}

Pregunta: {{PREGUNTA}}

RELOJES (el «ahora» de esta consulta; no es dato de ningún documento)
{{RELOJ_SISTEMA}}
```

**Lo que el prompt no lleva, a propósito:** no hay bloques `ROL`, `REGLAS` ni `ALCANCE`; no lleva R (la
aplica el ORQ); no lleva el esquema de las herramientas (viaja en `tools`); no dice el dominio ni los
documentos —los casos son lo que el agente necesita para elegir—.

**El umbral del 80%** es el criterio de selección: el agente mira los nombres de los casos y pide los
que podrían contener la respuesta. Los nombres son resúmenes: hay aspectos que el nombre del caso no
nombra, así que una pregunta puede quedar sin caso que la contenga aunque el dato exista. Los casos
leídos quedan en `consulta_casos`, así que se pueden auditar.

### 7.7. La respuesta

El agente entrega un JSON con dos estados:

```json
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_los_datos", "respuesta": ""}
```

El valor es `no_esta_en_los_datos` (así lo trae la plantilla `ORQ` vigente); **el lector acepta también
el viejo** (`no_esta_en_el_corpus`), que es el que traían los crudos de la primera ronda
(`orq/leer_entrega.py`, `ESTADOS`).

**El JSON no tiene campo propio**: como no hay herramienta de entrega, vive **dentro** del mensaje
final. En la superficie puede venir solo, dentro de una cerca de código, detrás de la etiqueta
`RESPUESTA_JSON:` o al final, después de la prosa; el lector no distingue esas cuatro formas, sino
**dos**: `todo_el_mensaje` —el mensaje es el JSON— y `dentro_del_mensaje` —está adentro, con lo que
venga alrededor—. Recorre los tramos `{…}` balanceados y se queda con el que sigue a la etiqueta, o
con el último que traiga un `desenlace` de los dos estados. No es juzgar: es leer. La forma de lectura
está declarada en `config.json` (`entrega.forma`, hoy `json_en_mensaje_final`) y el ORQ se detiene si
no la conoce.

Si el mensaje no trae ningún JSON, la salida escribe el mensaje tal cual y dice que no hubo JSON; si
la corrida la cortó una guardia, dice cuál —no que «el agente no contestó»—. **Sin JSON no hay
pregunta**: el acto no radica nada y la cédula guarda el motivo, con un extracto de lo que vino, para
diagnosticar. **El ORQ no juzga la entrega**: la registra tal como vino y la escribe en la salida.

**Lo que el sobre mínimo no lleva:** ni los datos que sostienen la respuesta (la ruta), ni un reporte
de lo recorrido. **Entregar no es sostener**: una corrida puede entregar sin leer ningún caso, y el
registro no distingue «entregó» de «se sostiene» —lo que ata la respuesta al documento es
`consulta_casos`, y puede estar vacío—. El sostén —que el usuario vea de dónde salió— queda para
cuando el usuario lo pida (§9).

### 7.8. Guardias y presupuesto

Las guardias **no son R**: R dice qué se puede usar; esto solo corta si el bucle se enreda.

- **Modelo:** el acto toma el alias y el esfuerzo de la fila `ORQ` de `ajustes` (hoy `luna` = GPT 6
  Luna, por OpenCode Go, familia `responses`, `reasoning.effort: low`) y se puede pisar por llamada.
  El transporte es el del MVP (`mvp/código/proveedores/`, **sin streaming**): la respuesta llega
  entera y se entrega en la forma de siempre —`choices[0].message` con `content`, `reasoning_content`,
  `tool_calls` y `finish_reason`—. Los alias declarados y sus claves están en `mvp/proveedores.md`.
- **De a una:** se manda una pregunta; la siguiente, cuando termina la corrida.
- **Guardias implementadas:** `max_turnos: 8` y `max_herramientas: 20`, y **el tope de herramientas
  se respeta de verdad**: el bucle mira el tope antes de ejecutar y corta la corrida. La causa del
  corte queda en el `motivo` de la fila de la corrida —**no hay columna `corte`**— y un corte se
  registra como **fallido**. **No hay corte por ciclo** (misma acción con los mismos argumentos dos
  veces); el agente repite lecturas y eso gasta turnos (§9).
- **El consumo** (`prompt_tokens = hit + miss`): el precio se calcula con la tarifa publicada el día de
  la corrida y se registra; no se estima a ojo. Los totales de cada corrida están en `corridas`. **El
  caché no se puede dar por hecho**: en las corridas de la base el `hit` aparece con DeepSeek y con
  Luna es 0 en todas (§9).
- **La plantilla no se resuelve ni se guarda**: la corrida apunta a su `prompt_id` y su
  `prompt_version`, y el prompt se re-arma cuando se pide.

### 7.9. Salidas

Todo lo que produce la consulta queda **en la base**, y nada en archivos:

- **`consultas`**: una fila por acto **con entrega** (`q<n>`: el número de la pregunta radicada) —el dominio, los documentos
  ofrecidos, la pregunta y su texto, el desenlace y la respuesta, tal como vino—. **No se reescribe.**
- **`consulta_casos`**: los casos que el agente leyó: es lo que permite la **traza**, de la respuesta a
  la unidad y al dato.
- **`consulta_llamadas`**: la **operación** de la corrida, una fila por llamada de herramienta —el
  turno, el orden dentro del turno, qué herramienta, con qué argumentos, y si volvió error, con lo que
  dijo el canal `tool`—. Permite auditar **cómo operó** el agente sin guardar su prosa ni su
  razonamiento; el orden de las lecturas, que antes solo se recuperaba del `rowid` de `consulta_casos`
  y por casualidad, ahora es un dato.
- **`corridas`**: la cédula —modelo, esfuerzo, el prompt y su versión, R y su hash, los tokens, los
  segundos, los turnos, las llamadas, y el `estado` con su motivo—.

**Cómo se lee una respuesta.** Con una consulta, no con un archivo: el ORQ no escribe `salida.md`, ni
`traza.jsonl`, ni crudos. Quien quiera ver una respuesta la lee de la base —las ocho tablas del corpus
y el almacén—: `consultas`, `consulta_casos` y `consulta_llamadas` dan la respuesta, los casos leídos
y la operación; `unidades`, `unidad_oraciones` y `datos` el corpus; `corridas` la cédula de cada
llamada; y **el texto radicado, del almacén** (`almacen.documentos`; el corpus solo guarda el espejo,
con el sello).

## 8. Cómo se evalúa

Se juzga **lo que la corrida entrega**, leyendo el documento. El juicio es nuestro, no del ORQ:

- la respuesta se sostiene en lo que el documento establece;
- lo que no se puede establecer se dice con precisión: qué falta y por qué;
- **no cuenta** acertar por casualidad ni citar texto que no sostiene la respuesta;
- se distingue «no está en los datos extraídos» de «el documento no lo dice»: la extracción puede
  haber dejado algo afuera, y una unidad vacía es un hueco nuestro, no del documento;
- las **unidades examinadas** quedan registradas (los casos leídos están en `consulta_casos`), y se
  distinguen del campo;
- **no interviene Jev**: el juicio es nuestro y se registra.

La **vara** para distinguir el hueco del documento del hueco de la extracción son los **tramos** de la
partición del paso 1: viven en `unidad_oraciones` (el `desde`, el `hasta` y la oración literal) y el
texto sobre el que se cuentan está en el documento radicado, sellado.

Una ejecución se considera terminada cuando corre acotada, sobre un dominio y con las baterías
fijadas antes, y se la juzga contra lo que se dejó escrito: si la respuesta es fiel, si se sostiene en
lo que el documento establece, y si lo que no se puede establecer se dice con precisión.

## 9. Lo abierto

- **El conflicto entre fuentes, sin ejercitar.** Ejercitarlo pide un hecho disputado entre dos
  documentos del mismo dominio; el corpus tiene hoy un solo dominio.
- **Las condiciones que el código no puede aplicar** (premisa, conflictos, brecha, no interactuar):
  son reglas del agente y **no están escritas en ninguna parte** (D21). Decidir si vuelven, y dónde.
- **`fuentes_admitidas` y `operaciones` son declarativas**: ningún módulo las lee; R es operativa hoy
  solo en `herramientas`.
- **No hay corte por ciclo**: el agente puede repetir la misma lectura con los mismos argumentos
  (D25). El tope de herramientas sí se respeta y la causa del corte se registra.
- **El sostén de la respuesta** (los datos citados, el reporte de lo recorrido): diferido hasta que el
  usuario pida ver la fuente (D24). El registro no distingue «entregó» de «se sostiene» (§7.7).
- **La compactación del historial** (D11): no implementada; el historial crece por turno y por eso
  está el tope de turnos.
- **El umbral del 80%** mira solo el nombre del caso: decidir si el criterio debe mirar algo más.
- **`unidad_valor`**: se usa poco, y no se decidió si merece campo propio (D16).
- **`documento_id` en `datos`**, en vez del prefijo del id (D22).
- **`documentos.ubicacion_upstream`**: los pasos ya leen el texto del almacén, así que la ruta del
  espejo quedó sin uso; decidir si se retira.
- **La numeración derivada del volcado** (`1`, `1.1`, `2`…) no siempre coincide con la que el
  documento trae (una introducción o unos anexos sin número). No se guarda, y en el informe del acto
  se muestra **como lo que es: una etiqueta del código**, no una corrección del documento.
- **El alcance por documento**: `resolver_dominio` solo sabe de etiquetas (`WHERE dominio = ?`); la
  entrada de la pregunta como JSON con `pregunta` y `dominio` es la forma prevista.
- **La extracción que leyó una consulta no se registra.** `listar_casos` fija el `datos_token` de cada
  documento al abrir y de ahí lee `obtener_datos_del_caso`, pero `consulta_casos` guarda solo
  `unidad_id`: «qué datos leyó esa consulta» se **deriva** —la última tanda exitosa sobre esa UT con
  token anterior al de la consulta— y no hay columna que lo diga. Decidir si se guarda.
- **El pedido de `preguntar_al_usuario` no se registra.** Sin entrega no hay `consultas` ni
  `consulta_llamadas`: la pregunta y las opciones que formuló el agente quedan solo en el `motivo`.
- **El caché con Luna**: `cache_hit` es 0 en todas sus corridas, y con DeepSeek hubo hit. Sin explicar.
- **El `usage` de la familia `responses`**: una corrida de un turno y cero lecturas (`q2`, `C000006`)
  registró 100 tokens de entrada donde las otras rondan 980 por turno. O el agregador declara solo lo
  nuevo —y entonces `cache_hit` no es de fiar—, o el prompt salió casi vacío: sin crudos, los totales
  no lo distinguen.
- **El reloj del radicado y los tres tiempos.** Los prompts rotulan el radicado «no es dato del
  documento», y §4 le hace además resolver un deíctico **del texto** («ayer»); pero la fecha propia del
  documento —si la declara— es un **dato**, y el `fecha_modificacion` de la fuente es **procedencia**,
  que hoy ningún prompt usa. Las tres cosas están mezcladas: decidir cuál resuelve qué, y escribirlo.
- **La evaluación, pendiente**: las corridas de la base viva están sin juzgar con la vara de §8; y una
  entregó **sin leer ningún caso** y quedó `respondida` —la respuesta coincide con una oración de `sol`,
  pero el prompt no lleva el texto: no salió del corpus—.

## 10. Lo que no se construye

- Nada de **espejo de las corridas del volcado** en el corpus, ni prefijos para evitar colisiones: cada
  base numera lo suyo y la vista unificada se hace cuando haga falta.
- Nada de **vigencia almacenada** (puntero o columna) ni índice parcial: se deriva.
- Nada de **sello del material**, **efecto** ni **versión del código** guardados: el material se
  reconstruye, «qué cambió» es un `COUNT` por token, y el instrumento que se compara es la plantilla
  versionada, no el commit.
- Nada de **event sourcing, outbox, CDC ni proyecciones**: el patrón es una tabla de actos y las filas
  producidas apuntando a su acto.
- Nada de **framework de migraciones**: `PRAGMA user_version` con guardia —si la base no está en la
  versión esperada y está vacía, se recrea; con datos, **se detiene y reporta**—.
- Nada de **guardar el prompt resuelto**: la plantilla y el material se reconstruyen.
- Nada de **uuid/ULID** ni dependencias nuevas: contador.
- Nada de **`traza.py` ni comandos nuevos** hasta que la consulta duela.
- **Es un MVP, y se diseña como tal**: nada se pre-construye «por si acaso», y lo que se agrega tiene
  que pagarse en la ronda en que se usa. **JIT**: nada entra al esquema —ni tabla ni columna— si no
  hay una pregunta que hoy no se pueda responder sin eso; después, toda transformación es un
  `ALTER TABLE` chico y explícito.
- **Nada de frameworks**: biblioteca estándar y SQLite.

---

## Apéndice A · Esquema de las dos bases

**El corpus** (`mvp/código/corpus.db`, versión 5): ocho tablas del corpus y cuatro del expediente.

```sql
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre del documento radicado
  dominio            TEXT NOT NULL,      -- el alcance al que pertenece
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base, al radicar
  ubicacion_upstream TEXT NOT NULL,      -- dónde vive la fuente en el repo (procedencia)
  sello              TEXT NOT NULL       -- sha256 del texto radicado: guardián de que no cambió
);

CREATE TABLE preguntas (   -- las preguntas radicadas: la única entrada de la consulta
  id               INTEGER PRIMARY KEY,  -- el número de la pregunta (1, 2, 3…)
  dominio          TEXT NOT NULL CHECK (trim(dominio) <> ''),  -- el alcance: la unidad semántica
  texto            TEXT NOT NULL CHECK (trim(texto) <> ''),    -- sin texto no hay pregunta
  fuente           TEXT NOT NULL,        -- 'tecleada', o la ruta del archivo del que se leyó
  fecha_radicacion TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE corridas (
  id              TEXT PRIMARY KEY,      -- el token del acto: C000123
  paso            TEXT NOT NULL CHECK (paso IN ('UT', 'DATOS', 'ORQ')),
  documento_id    TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- UT y DATOS
  dominio         TEXT,                  -- ORQ: el alcance de la consulta
  pregunta_id     INTEGER REFERENCES preguntas(id),  -- ORQ: la pregunta radicada
  pregunta_texto  TEXT,                  -- ORQ: el texto tal como se leyó
  prompt_id       TEXT,                  -- la plantilla que corrió (en `prompts`)
  prompt_version  INTEGER,
  hash_r          TEXT,                  -- ORQ: sha256 de R.json
  modelo          TEXT NOT NULL,         -- el id del modelo
  esfuerzo        TEXT,
  reloj_radicado  TEXT,                  -- los relojes, tal como entraron al prompt
  reloj_sistema   TEXT,
  corrida_origen  TEXT REFERENCES corridas(id),  -- DATOS: la corrida de UT que usó
  tokens_entrada  INTEGER,
  tokens_salida   INTEGER,               -- incluye el pensamiento: no se suma aparte
  tokens_pensando INTEGER,               -- detalle de lo anterior
  cache_hit       INTEGER,
  segundos        REAL,
  turnos          INTEGER,
  llamadas        INTEGER,
  estado          TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo          TEXT,                  -- si falló: sin JSON · cortada por… · error de la API
  iniciado        TEXT,                  -- cuándo empezó el acto
  terminado       TEXT,                  -- cuándo cerró
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL),                    -- un fallo dice por qué
  CHECK ((paso = 'ORQ' AND dominio IS NOT NULL AND documento_id IS NULL)
      OR (paso <> 'ORQ' AND documento_id IS NOT NULL))                 -- el alcance de cada paso
);

CREATE TABLE prompts (     -- las plantillas del corpus, con su versión: 'UT' · 'DATOS' · 'ORQ'
  id       TEXT NOT NULL,
  version  INTEGER NOT NULL,
  texto    TEXT NOT NULL,                -- el texto de la plantilla: es su identidad
  fecha    TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  PRIMARY KEY (id, version)
);

CREATE TABLE contador (    -- el token de esta base
  id     INTEGER PRIMARY KEY CHECK (id = 1),
  ultimo INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE ajustes (     -- el modelo y el esfuerzo de cada acto (la política)
  paso     TEXT PRIMARY KEY,             -- 'volcado' · 'UT' · 'DATOS' · 'ORQ'
  modelo   TEXT NOT NULL,                -- un alias del registro de proveedores
  esfuerzo TEXT                          -- el escalón, o null para el del alias
);

CREATE TABLE unidades (                  -- la salida de UT
  id           TEXT PRIMARY KEY,         -- <token_UT>:U<n>
  documento_id TEXT NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,
  subtema      TEXT NOT NULL,            -- el nombre del caso
  corrida_id   TEXT NOT NULL REFERENCES corridas(id),
  UNIQUE (corrida_id, n)                 -- una partición por corrida; las anteriores conviven
);

CREATE TABLE unidad_oraciones (          -- las oraciones de la unidad, con su tramo
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  n            INTEGER NOT NULL,         -- el orden dentro de la unidad
  desde        INTEGER NOT NULL,         -- offsets en caracteres sobre el texto del documento
  hasta        INTEGER NOT NULL,
  texto        TEXT NOT NULL,            -- la oración literal, tal como la devolvió el modelo
  PRIMARY KEY (unidad_id, n)
);

CREATE TABLE datos (                     -- la salida de DATOS
  id           TEXT PRIMARY KEY,         -- <token_DATOS>:U<n>:D<j>
  unidad_id    TEXT NOT NULL REFERENCES unidades(id) ON DELETE CASCADE,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT,
  corrida_id   TEXT NOT NULL REFERENCES corridas(id)
);
CREATE INDEX idx_datos_unidad ON datos(unidad_id);

CREATE TABLE consultas (
  id             TEXT PRIMARY KEY,       -- q<n>
  corrida_id     TEXT NOT NULL REFERENCES corridas(id),
  dominio        TEXT NOT NULL,
  documentos     TEXT NOT NULL,          -- los documentos del dominio que se ofrecieron
  pregunta_texto TEXT NOT NULL,
  desenlace      TEXT,                   -- respondida · no_esta_en_los_datos (los dos de la plantilla ORQ)
  respuesta      TEXT,                   -- la respuesta, tal como vino
  fecha          TEXT NOT NULL DEFAULT (datetime('now','localtime'))
);

CREATE TABLE consulta_casos (
  consulta_id TEXT NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
  unidad_id   TEXT NOT NULL,             -- el id de la unidad: <token_UT>:U<n>
  PRIMARY KEY (consulta_id, unidad_id)
);

CREATE TABLE consulta_llamadas (         -- la operación: qué herramienta pidió, en qué turno
  consulta_id TEXT NOT NULL REFERENCES consultas(id) ON DELETE CASCADE,
  turno       INTEGER NOT NULL,          -- la vuelta del bucle (1..max_turnos)
  orden       INTEGER NOT NULL,          -- la posición de la llamada dentro del turno (1..n)
  herramienta TEXT NOT NULL,
  argumentos  TEXT,                      -- tal como los mandó el modelo (puede no ser JSON válido)
  ok          INTEGER NOT NULL,          -- 1 la ejecutó · 0 volvió error por el canal `tool`
  error       TEXT,                      -- qué devolvió el canal `tool` cuando no fue ok
  PRIMARY KEY (consulta_id, turno, orden)
);
```

**El almacén** (`mvp/código/almacen.db`, versión 4):

```sql
CREATE TABLE documentos (
  id                 TEXT PRIMARY KEY,   -- el nombre con que se radica ('sol')
  coleccion          TEXT NOT NULL,      -- la etiqueta que en el corpus se llama `dominio`
  texto              TEXT NOT NULL,      -- el markdown volcado: el original
  sello              TEXT NOT NULL,      -- sha256 del texto: guardián de que no se tocó
  nombre_fuente      TEXT,               -- el nombre del archivo del que se volcó (procedencia)
  ruta_fuente        TEXT,               -- dónde estaba, en el sistema de archivos (procedencia)
  fecha_modificacion TEXT,               -- el mtime que el sistema registra, tomado al volcar
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime'))  -- la pone la base
);

CREATE TABLE volcados (    -- el intento de volcado: la cédula del acto
  id             TEXT PRIMARY KEY,       -- el token del acto: A000123
  documento_id   TEXT REFERENCES documentos(id) ON DELETE CASCADE,  -- **nulo si falló**
  modelo         TEXT NOT NULL,
  esfuerzo       TEXT,
  prompt_id      TEXT NOT NULL,          -- la plantilla que corrió ('volcado')
  prompt_version INTEGER NOT NULL,
  reloj_radicado TEXT,                   -- los relojes, tal como entraron al prompt
  reloj_sistema  TEXT,
  sello_fuente   TEXT,                   -- sha256 de la fuente: identificada, no conservada
  tokens_entrada INTEGER,
  tokens_salida  INTEGER,                -- incluye el pensamiento
  tokens_pensando INTEGER,
  cache_hit      INTEGER,
  segundos       REAL,
  estado         TEXT NOT NULL CHECK (estado IN ('exitoso', 'fallido')),
  motivo         TEXT,
  iniciado       TEXT,
  terminado      TEXT,
  CHECK (estado = 'exitoso' OR motivo IS NOT NULL)
);

CREATE TABLE prompts (     -- las plantillas del volcado, con su versión: 'volcado'
  id       TEXT NOT NULL,
  version  INTEGER NOT NULL,
  texto    TEXT NOT NULL,                -- el texto de la plantilla: es su identidad
  fecha    TEXT NOT NULL DEFAULT (datetime('now','localtime')),
  PRIMARY KEY (id, version)
);

CREATE TABLE contador (    -- el token de esta base
  id     INTEGER PRIMARY KEY CHECK (id = 1),
  ultimo INTEGER NOT NULL DEFAULT 0
);
```

**Por qué `volcados` tiene id propio y `documento_id` admite nulo:** un volcado **fallido no deja
documento** —es justo el que más interesa—, así que su fila tiene que poder existir sola. Es el único
lugar donde la cédula del acto no cuelga de lo que produjo.

**Las identidades, de un vistazo:**

| id | Qué nombra |
|---|---|
| `<token_UT>:U<n>` | la unidad: la corrida de UT que la produjo, y su posición en el arreglo |
| `<token_DATOS>:U<n>:D<j>` | el dato: su corrida, su unidad y su posición en la lista |
| `q<n>` | la consulta: el número de la pregunta radicada |

## Apéndice B · Las rondas y la prueba de aceptación

| # | Qué | Criterio de aceptación |
|---|---|---|
| **R0** | Cerrar las decisiones. Sin código. | las respuestas escritas y el plan actualizado |
| **R1 · la fuente** | token, conservación con los ids nuevos, `prompts` con la inscripción, `contador` y `user_version` | `leer_prompt(db,'UT')` devuelve el texto vivo; una UT deja su corrida con los dos relojes, plantilla y versión, y un token; una segunda UT sobre el mismo documento **no borra** la primera |
| **R2 · los actos** | `acto.py` (`abrir()` → token e inicio; `cerrar()` → estado, motivo y fin); `paso1` y `paso2` lo usan; `volcar.py` nace con todo | las etapas I y II corren con el modelo simulado, cada acto imprime su token, y DATOS queda encadenado a su corrida y a la de UT |
| **R3 · la consulta** | registrar **la extracción que se leyó** y lo ofrecido; la radicación al cerrar | rehacer **solo DATOS** y comprobar que la consulta anterior sigue mostrando **exactamente** los datos que leyó |
| **R4 · auditar** | las preguntas de abajo | — |

**R3 y R4 siguen abiertas**: lo que falta está en §9.

**La prueba de aceptación.** Sobre una corrida **vieja**, después de rehacer DATOS (con la UT intacta)
y de repetir la consulta:
1. «¿Con qué plantilla y versión corrió?» — y el material se reconstruye exacto.
2. «¿Qué hora se inyectó en el prompt?»
3. «¿Qué datos leyó esa consulta?» — y siguen siendo **los mismos**, aunque DATOS se haya rehecho
   después.

Las tres se responden sobre la corrida vieja, no sobre la última. La cuarta —«¿qué código la
ensambló?»— **no se promete**.

**La plantilla se inscribe.** El acto que corre la **lee de la base**: la vigente es la última versión
inscrita. Una nueva se inscribe con un acto aparte
(`python3 mvp/código/prompts.py inscribir <id> <archivo>`), que lee el texto de un borrador —un
archivo que vive donde se esté escribiendo, no en el repo— y deja la versión con su fecha. Es
idempotente por texto: si es el mismo texto, no agrega nada. **Una versión inscrita no se toca**:
editarla es inscribir otra.

**Los papeles se actualizan en el commit de cada ronda**: `AGENTS.md`, `README.md`, esta sección y la
memoria.

## Apéndice C · Las piezas del código

| Archivo | Qué hace |
|---|---|
| `mvp/código/base.py` | el corpus: el registro, el esquema y las consultas |
| `mvp/código/esquema.py` | la versión del esquema y el token del acto |
| `mvp/código/acto.py` | abrir y cerrar un acto: token, tiempos, estado y motivo |
| `mvp/código/prompts.py` | las plantillas de la base: leer la vigente e inscribir una versión nueva |
| `mvp/código/ajustes.py` | el modelo y el esfuerzo de cada acto, leídos de la base |
| `mvp/código/almacen.py` | el almacén: `escribir` (con el espejo, en una transacción), `texto_de` (con el sello comprobado), `registrar_fallo` |
| `mvp/código/volcar.py` | el acto del volcado: **es la radicación** |
| `mvp/código/armar_volcado.py` | del texto y el índice al markdown marcado |
| `mvp/código/paso1_unidades.py` | el acto UT |
| `mvp/código/paso2_datos.py` | el acto DATOS |
| `mvp/código/extraer_unidades.py` | `ubicar` y `verificar_particion`: ubica las oraciones y verifica el contrato |
| `mvp/código/cargar_pregunta.py` | carga la pregunta: un archivo o el chat; la radica el acto, al entregar |
| `mvp/código/respuesta.py` | `extract_json` |
| `mvp/código/mensajes.py` | `partir`: el `system` y el `user` de cada llamada |
| `mvp/código/relojes.py` | los dos relojes, con su formato |
| `mvp/código/proveedores/` | el transporte: el registro de alias, `llamar` con `prompt` o `mensajes` y `tools`, y la única lectura de claves (`claves.py`) |
| `mvp/código/orq/` | el orquestador, un archivo por paso (§7.3); `leer_entrega.py` lee el JSON de la entrega |
| `mvp/código/R.json` | lo que se admite y se ofrece |

**De fuera del MVP se reutiliza:** `test_tool_calling/` (las corridas que fijaron la mecánica del
bucle) y, para la evaluación, `mvp/temp/pieza1/pieza1.py` (`verificar` y `comparar`) y
`unidades/ficha_doc.py` (`verificar` y `fragmentos`). `mvp/temp/` es archivo: no se corre desde ahí.
El mapa de los alias de modelo y sus APIs está en `mvp/proveedores.md`.

## Apéndice D · Decisiones y fuentes

| # | Decisión |
|---|---|
| **D1** | Nombres: código = ORQUESTADOR, LLM = AGENTE ENCARGADO (§7.1) |
| **D2** | El corpus admite varios documentos por dominio (§7.2); el conflicto entre fuentes sigue sin ejercitarse (§9) |
| **D3** | Bucle con herramienta, no todo inyectado en una llamada |
| **D4** | Sin datos derivados en esta versión |
| **D5** | R: `solo el documento`, sin mundo del LLM ni anclas como premisa |
| **D6** | Nombre y sitio de los archivos: el código, `R.json` y la base en `mvp/código/` (`orq/` el orquestador); los documentos que se radican, en `mvp/documentos/`; las baterías, en `mvp/consulta/preguntas_<doc>.md` —son fuentes—; las plantillas, en la base (`prompts`, con su versión); y lo que se produce, en la base. `mvp/temp/` es archivo |
| **D7** | Las dos bases con claves foráneas y contratos (`paso`, `estado`, `motivo` si falló, un `n` por corrida) |
| **D8** | Derivados: fuera de esta versión |
| **D11** | Compactación del historial: no implementada (§9) |
| **D12** | «Mundo del agente» en los documentos vivos: sigue como vocabulario, sin efecto en el código |
| **D13** | Herramientas: (B) nativas, aditivo sobre el transporte del MVP |
| **D14** | Prompts de la extracción: `prompt_UT` y `prompt_DATOS` |
| **D15** | Salida del paso 2: `caso` y `datos`; el 08-10 se quitó `dudas` y el paso 2 pasó a la tanda (D27) |
| **D16** | `unidad_valor`: campo propio o dentro del `valor` — **abierta** (§9) |
| **D17** | El agente lee solo los datos extraídos, no el texto del documento |
| **D18** | El ORQ no juzga la entrega; el juicio vive en la evaluación (§8) |
| **D19** | La entrega va por mensaje final, no por herramienta |
| **D20** | El ORQ ubica el JSON del mensaje final donde prompt 3 lo ponga (§7.7) |
| **D21** | Las condiciones que el código no puede aplicar — **abierta**: no están escritas (§9) |
| **D22** | `documento_id` en `datos`, en vez del prefijo del id — **abierta** (§9) |
| **D23** | La declaración del esquema (partición, prompt y versión, modelo) va en la fila de `corridas` |
| **D24** | El sostén en la respuesta: diferido hasta que el usuario pida ver la fuente (§9) |
| **D25** | Tope y corte: el de herramientas se respeta y la causa se registra; **no hay corte por repetición** (§9) |
| **D26** | Con `preguntar_al_usuario` el ciclo termina: no se reanuda, el acto no radica pregunta y la pregunta no se registra (queda el `motivo`) |
| **D27** | El paso 2 va **en tanda**, una llamada por documento (§6.2; la medición, en la memoria) |
| **D28** | La pregunta se radica **al cerrar con entrega**, en la misma transacción que la corrida y la respuesta (§7.2) |

**Superadas:** D9 (idioma de los `tipo`: no hay tipos) y D10 (documento R: R es un JSON que lee el
ORQ).

**Las mediciones no viven acá**: los números —tokens, segundos, caché, tanda contra unidad— están en
`mvp/memoria de trabajo y pendientes.md` y en las bases.

**Fuentes de la forma de la base:** [flat files vs SQLite](https://sqlite.org/forum/forumpost/c43b208884?t=h)
y [el hilo sobre JSON y SQLite](https://github.com/kody-w/rappterbook/discussions/3742) —elegir por
forma de acceso—; [`PRAGMA user_version`](https://sqlite.org/pragma.html#pragma_user_version) y
[migraciones sin framework](https://levlaz.org/sqlite-db-migrations-with-pragma_user_version/);
y [atomicidad entre archivos con `ATTACH`](https://sqlite.org/lang_attach.html) —y por qué ninguna de
las dos bases usa WAL—.

**De la operación del agente:** [12-Factor Agents](https://github.com/humanlayer/12-factor-agents)
—factores 2, 3, 9 y 12, y el
[stateless reducer](https://github.com/humanlayer/12-factor-agents/blob/main/content/factor-12-stateless-reducer.md)—;
[Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
y [Building effective agents](https://www.anthropic.com/engineering/building-effective-agents);
[Writing effective tools for agents](https://www.anthropic.com/engineering/writing-tools-for-agents)
—buscar, no listar; pocas herramientas con propósitos distintos—.

**De la API:** [Chat Completions](https://api-docs.deepseek.com/api/create-chat-completion/) y
[Tool Calls](https://api-docs.deepseek.com/guides/tool_calls/) —el `role: "tool"` y el `tool_call_id`—;
[Thinking Mode](https://api-docs.deepseek.com/guides/thinking_mode/) —con `tools`, el
`reasoning_content` tiene que volver en todos los turnos—; [Context Caching](https://api-docs.deepseek.com/guides/kv_cache)
—caché por prefijo y `prompt_cache_hit_tokens` / `prompt_cache_miss_tokens`—; y
[Responses API](https://api-docs.deepseek.com/guides/responses_api) —la API es stateless: sin
`previous_response_id`—.
