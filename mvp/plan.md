# Plan: la traza y la fuente (MVP de Zettel)

**Qué es.** El plan de la línea que hace que **cada etapa se pueda auditar** y que las
**plantillas de los prompts** vivan en la base. El detalle de las rondas vive acá; el estado
—qué hay hecho y qué sigue— sigue viviendo en `mvp/memoria de trabajo y pendientes.md`, que es
la fuente única.

**Estado (12-10):** **R0 cerrado** y **R1 hecho**, con los actos de UT, DATOS y el ORQ encima
(`57eaf4f`); las dos bases están en la versión 1, vacías. **Falta:** `volcar.py` (el acto de la
etapa I), **R3** (el expediente del ORQ) y **R4** (auditar).

**Es un MVP, y se diseña como tal.** Alcance reducido: lo que hace falta para que la próxima
etapa corra y para poder **comparar corridas**. No es un producto: nada se pre-construye «por
si acaso», y lo que se agrega tiene que pagarse en la ronda en que se usa.

---

## 0. Principios

1. **JIT, y la pregunta manda.** Nada entra al esquema —ni tabla ni columna— si no hay una
   pregunta que hoy no se pueda responder sin eso. La ventana barata no se cierra con «base
   vacía» sino con el primer dato real, y después toda transformación es un `ALTER TABLE` chico
   y explícito, sin framework. No hay que pre-construir por miedo a la ventana.
2. **La base es la fuente de verdad.** Lo que los actos usan y lo que producen se lee y se
   escribe en la base. Los archivos son **puertas y borradores**, no fuentes.
3. **No se duplica lo que puede reconstruirse desde evidencia conservada e identificable.**
   Un sello **comprueba** una reconstrucción; no la hace posible. Por eso lo primero es
   **conservar**; lo que no se conserve se declara y no se promete.
4. **Un acto, una fila.** Cada ejecución deja su fila y su **token**: no se pisa ni se borra.
   Los productos apuntan al acto que los produjo.
5. **Nada de frameworks.** Biblioteca estándar y SQLite. Sin dependencias nuevas.

---

## 1. Las tres etapas, sus actos y quién manda

| Etapa | Acto | Producto | Base dueña (asigna el token) |
|---|---|---|---|
| **I · volcado** | `volcar.py` (a escribir) | el markdown original, su sello y su procedencia | **almacén** |
| **II · extracción** | `paso1_unidades.py` (UT) | unidades y oraciones con sus tramos | **corpus** |
| **II · extracción** | `paso2_datos.py` (DATOS) | datos | **corpus** |
| **III · consulta** | `orq/orquestador.py` (ORQ) | la respuesta, los casos leídos y las llamadas | **corpus** |

**El token es del acto, no de la etapa.** La etapa II tiene dos actos y cada uno inyecta su
propio reloj; con un token por etapa, «¿qué hora se inyectó?» devolvería dos. Cada acto
**imprime su token** al cerrar: `paso1 doc11 · corrida C000123`.

**Cada base numera sus tokens** (`A` el almacén, `C` el corpus). El prefijo no hace falta para
que no colisionen —no hay espejo—, sino para poder **citar un token sin ambigüedad**: la cédula
del volcado ya vive en `almacen.volcados`, y la etapa I no necesita nada más que su token.

**En el volcado, los dos relojes coinciden casi**: todavía no hay documento, así que el reloj
del radicado **es** el del acto. Se registran igual los dos, por simetría.

---

## 2. R0-a: qué sobrevive a `--rehacer`

Es la decisión que va primero, porque de ella dependen los ids, el esquema y lo que el
expediente puede prometer. Hoy **`--rehacer` borra**:

- ~~`radicar.py --rehacer`~~: **ya no existe**; lo retiró `volcar.py` (12-10), que no tiene
  `--rehacer`;
- `paso1 --rehacer` borra las unidades y sus oraciones ([`borrar_unidades`](código/base.py));
- `paso2 --rehacer` borra los datos;
- y el ORQ **pisa** la consulta ([`registrar_consulta`](código/orq/registrar_consulta.py)).

| | **A · conservar los productos** (elegida) | B · identificar sin conservar |
|---|---|---|
| Qué hace | la corrida nueva **no borra** la anterior; la vigente se **deriva** | se sigue borrando; el acto guarda sello y procedencia de su material |
| Qué promete | reconstruir la partición y los datos de cualquier intento, y **comparar rondas** | comprobar una reconstrucción, no hacerla |
| Costo | identidad por corrida (abajo); ~6 lecturas pasan a ser por token | nada |

**Por qué A, y no por elegancia:** comparar prompts y corridas **es la metodología** que la
memoria ya usa (acuerdo entre particiones, «el ejemplo manda», el banco de DATOS), y con B la
corrida anterior se pierde. Y las dos bases están en cero: es el momento más barato.

**Cambia la identidad, no la tabla:**

- `unidades`: unicidad por **`(corrida_UT, n)`** en vez de `(documento_id, n)`; el id pasa a
  `<token_UT>:U<n>`.
- `datos`: **el id lleva el token de DATOS** (`<token_DATOS>:D<j>`), además de la unidad. Sin
  esto, rehacer DATOS sobre la misma UT **repite los ids** y el acto se cae.
- **No hay columnas de vigencia ni índice parcial**: «vigente = la **última corrida exitosa**»
  se deriva del token (secuencia). La consulta la resuelve **una vez** y la registra, como
  `anclas` congela la hora.
- Efecto lateral que se gana: desaparece el `substr(unidad_id, …)` de `datos_de`.

---

## 3. El delta

### 3.1 Esquema

**`corridas` (corpus)** — lo que ya está no se toca: `modelo`, `esfuerzo`, tokens, `segundos`,
`turnos`, `llamadas`, `estado`, `motivo`, `documento_id`, `dominio`, `bateria`,
`pregunta_numero`, `pregunta_texto`, `hash_prompt`, `hash_r`.

| Nuevo | Qué es | Qué pregunta responde |
|---|---|---|
| `id` = **token** | `C000123`, del contador de su base | ¿qué corrida? |
| `reloj_radicado`, `reloj_sistema` | los dos relojes **como se inyectaron**, etiquetados por dónde van (radicado → `system`; sistema → `user`) | ¿qué hora entró al prompt? |
| `prompt_id`, `prompt_version` | reemplazan `prompt` (nombre de archivo) | ¿con qué plantilla, y cuál versión? |
| `corrida_origen` | la corrida de UT que usó DATOS | ¿de dónde salieron las unidades? |
| `iniciado` | con `terminado` (hoy `fecha`), los tiempos del **acto** | ¿cuánto duró el acto? |

**`prompts` (tabla nueva, en la base dueña del acto):** `id`, `version`, `texto`, `sello`,
`fecha`; PK `(id, version)`.

**`contador` (una fila por base)** y **`PRAGMA user_version`** con guardia: si la base no está
en la versión esperada → vacía, se recrea; con datos, **se detiene y reporta**. Está justificado
por algo que ya pasó: el `UNIQUE (sello)` que `CREATE TABLE IF NOT EXISTS` no pudo quitar.

**No se agregan** (y por qué): columnas de vigencia o índice parcial (la vigente se deriva);
`sello_material` (con A, todo material es reconstruible exacto: el texto por el sello del
documento, las unidades por su corrida, lo ofrecido por la corrida); `efecto` («qué cambió» es
un `COUNT` por token, y guardarlo reintroduce el bug de contar bajas que un `rollback` deshizo);
`codigo` y el diff (el instrumento que se compara es la plantilla versionada, no el commit).

**`almacen.volcados` (etapa I)** ya tiene su cédula con id propio. Suma, simétrico: `iniciado`,
los dos relojes, `prompt_id`/`prompt_version`, `sello_fuente` y la procedencia. **Sin cambios de
`paso` ni de `CHECK`**: al no haber espejo, el corpus no guarda corridas de volcado.

### 3.2 Las plantillas: registro perezoso

No hace falta un acto manual para meter un prompt. **El acto que lo usa lo registra**: antes de
llamar, hashea la plantilla y, **si ese sello no está, la guarda como versión nueva** (patrón de
contenido: idempotente, sin trabajo manual, y la base se llena sola con lo que corrió).

- El `.md` queda como **borrador y puerta**; la base es la fuente de lo que corrió.
- Editar la plantilla = sello nuevo = **versión nueva**; nunca un `UPDATE`.
- Cada plantilla vive con la base dueña de su acto (`prompt_volcado`, en el almacén; las otras
  tres, en el corpus).
- Mostrar antes de correr: se arma leyendo la base; si el borrador todavía no corrió, se muestra
  desde el archivo y queda registrado al primer uso.

### 3.3 La consulta (etapa III)

Se implementa en su ronda, pero se diseña ahora, porque es donde la traza se juega:

- `consultas` pasa a ser **append-only**, con el token por id: cada ejecución conserva **su**
  respuesta, **sus** casos y **sus** llamadas. Hoy se upsertea y se borran.
- Cada caso leído se registra con **la extracción que se leyó**: `(token_DATOS, unidad_id)`. No
  con el alias solo: tras rehacer DATOS sobre la misma UT, `doc:U1` puede nombrar otros datos, y
  [`obtener_datos_del_caso`](código/orq/obtener_datos_del_caso.py) hoy lee por unidad sin
  distinguir corrida. Con `(token_DATOS, unidad_id)` la respuesta se re-deriva exacta —las filas
  son conservadas e inmutables— y no hace falta guardar cada id de dato.
- `ofertado`: el token de UT del que salió el catálogo, los ids ofrecidos y las herramientas.

### 3.4 Qué se promete de un intento

Se registran **éxitos y fallos controlados** (la fila se escribe al cerrar el acto). Una muerte
abrupta antes de escribir **no deja constancia**, y no se promete. Si algún día importa, la
salida es una fila `en_curso` al abrir; eso trae un `UPDATE` y contradice «un acto, una fila»,
así que se hace cuando haya una pregunta que lo pida.

Del **código** no se promete reconstrucción: el commit no conserva el árbol sucio y una copia
del diff no se paga en cada acto. El día que haya que auditar una corrida con árbol sucio, se
guarda el diff **entonces**.

---

## 4. Las rondas

| # | Qué | Criterio de aceptación |
|---|---|---|
| **R0** | Cerrar las decisiones (§9). Sin código. | las respuestas escritas y el plan actualizado |
| **R1 · la fuente** | en el corpus: token, conservación con los ids nuevos, `prompts` con registro perezoso, `contador` y `user_version`; **se recrean las dos bases** | `leer_prompt(db,'UT')` devuelve el texto vivo; una UT simulada deja su corrida con los dos relojes, plantilla y versión, y un token; una segunda UT sobre el mismo documento **no borra** la primera |
| **R2 · los actos** | `acto.py` (`abrir()` → token e inicio; `cerrar()` → estado, motivo y fin); `paso1` y `paso2` lo usan; **`volcar.py` nace con todo** (plantilla de la base, token, procedencia, `sello_fuente`) | las etapas I y II corren con el modelo simulado, cada acto imprime su token, y DATOS queda encadenado a su corrida y a la de UT |
| **R3 · la consulta** | `consultas` append-only, casos y llamadas por token, `ofertado`, la extracción leída | rehacer **solo DATOS** y comprobar que la consulta anterior sigue mostrando **exactamente** los datos que leyó |
| **R4 · auditar** | las preguntas de §5; **solo si duele**, `traza.py` (~30 líneas, solo lectura) | §5 |

Los papeles se actualizan en el commit de cada ronda: `consulta-diseno.md` (D6, §4, §10, §11),
`almacen-diseno.md`, `AGENTS.md` y la memoria (#13, #14, #15a, #18).

**Hecho:** R1 completo, y los actos de UT, DATOS y el ORQ encima (R2 a medias: falta `volcar.py`).

---

## 5. La prueba de aceptación

Sobre una corrida **vieja**, después de rehacer DATOS (con la UT intacta) y de repetir la
consulta:

1. «¿Con qué plantilla y versión corrió?» — y el material se reconstruye exacto.
2. «¿Qué hora se inyectó en el prompt?»
3. «¿Qué datos leyó esa consulta?» — y siguen siendo **los mismos**, aunque DATOS se haya
   rehecho después.

Las tres se responden sobre la corrida vieja, no sobre la última. Cuarta pregunta —«¿qué código
la ensambló?»— **no se promete** (§3.4).

---

## 6. Anti-scope (lo que **no** se construye)

- Nada de **espejo del volcado** en el corpus, ni prefijos para evitar colisiones: cada base
  numera lo suyo y la vista unificada se hace cuando haga falta.
- Nada de **vigencia almacenada** (puntero o columna) ni índice parcial: se deriva.
- Nada de **sello del material**, **efecto** ni **versión del código** guardados.
- Nada de **event sourcing, outbox, CDC ni proyecciones**: el patrón es una tabla de actos y las
  filas producidas apuntando a su acto.
- Nada de **framework de migraciones**: `user_version` y la guardia.
- Nada de **guardar el prompt resuelto**: la plantilla y el material se reconstruyen.
- Nada de **uuid/ULID** ni dependencias nuevas: contador.
- Nada de **`traza.py` ni comandos nuevos** hasta que la consulta duela.

---

## 7. Lo que se quema, y lo que se gana

**Se quema** (todo sin datos dentro): la forma de `corridas`, el upsert y
`conservar_efectiva`, `borrar_corridas`, las tres copias de `fallar()`, los ids
determinísticos de corrida y el `UNIQUE (documento_id, n)`.

**Se gana en código, y no es poco:** conservar e insertar **elimina la parte más difícil de los
actos**. Hoy `--rehacer` borra sin commit y `fallar()` hace `rollback()` para que «lo anterior
vuelva»; de ahí salen las restauraciones y sus pruebas. Sin borrado no hay restauración: el acto
es «llamo; si falla, escribo la corrida fallida; si no, escribo corrida y productos en una
transacción». **Se cae maquinaria, no se agrega.**

---

## 8. Costo

Por acto: un `SELECT` y un `INSERT` de más, una fila, y un hash de la plantilla. **Cero llamadas
extra a modelos, cero dependencias, cero herramientas nuevas.** No toca el transporte ni los
prompts de trabajo, así que no altera ninguna medición en curso.

---

## 9. Lo que cerró R0 (12-10)

1. **Conservar los productos** (A) en vez de identificar sin conservar — recomendación: A.
2. **Token de 6 dígitos con prefijo de base** (`A`/`C`), por claridad al citarlo — recomendación:
   con prefijo.
3. **Plantillas con la base dueña del acto**, registro **perezoso** (sin acto manual de entrada)
   — recomendación: sí; alternativa: las cuatro en el corpus.
4. **`user_version`** con la guardia de §3.1 — recomendación: sí.
5. **R y la batería**: dejarlos como están (R ya viaja con su hash); la batería gana un hash si
   hace falta.
6. **Del código no se promete reconstrucción** (§3.4) — recomendación: declararlo así.

---

## 10. Referencias

- Event sourcing vs. tabla de actos: qué patrón es overkill y cuándo —
  <https://codenicelystudio.com/blog/businesses/saas/temporal-tables-vs-event-sourcing-audit-trail>
  y <https://stackoverflow.com/questions/1051449/ideas-on-database-design-for-capturing-audit-trails>
- `PRAGMA user_version` para versionar el esquema sin framework —
  <https://sqlite.org/pragma.html#pragma_user_version> y
  <https://levlaz.org/sqlite-db-migrations-with-pragma-user_version/>
- Almacenamiento por contenido (hash + «si ya está, no se escribe») para el registro perezoso —
  <https://limitsystems.ai/platform/storage>
- Atomicidad entre archivos con `ATTACH` (y por qué ninguna de las dos bases usa WAL) —
  <https://sqlite.org/lang_attach.html>
