# niveles/ — smoke test: separar datos y argumentos, construir la tesis

Sub-spike aparte (no usa Jev). Prueba si un LLM, con un prompt que viaja en
archivo, separa en un texto corto los **datos** (nivel 3) y los **argumentos**
(nivel 2), ambos literales, y luego construye la **tesis y el propósito**
(nivel 1) solo a partir de ellos. Esta primera ronda es un smoke test:
comprobar que la cadena funciona y ver qué sale. No se evalúa calidad.

Aplican las reglas de ejecución del `CLAUDE.md` raíz (el spike no concluye,
crudo siempre visible, solo documentos sintéticos, commit y push al final).

## Archivos (no editar sin aprobación de Frat)

- `docs/doc1.md` — documento sintético en Markdown.
- `prompts/A_v1.md` — llamada A: separa datos / argumentos / otro. Marcador `{{TEXTO}}`.
- `prompts/B_v1.md` — llamada B: tesis y propósito. Marcadores `{{ARGUMENTOS}}` y `{{DATOS}}`.

Los prompts se leen siempre de su archivo; nunca se copian dentro del código.
Los marcadores se sustituyen con `str.replace` (no `str.format`: los prompts
contienen llaves de JSON).

## Qué implementar: `niveles/run_niveles.py`

Uso: `python3 niveles/run_niveles.py <doc> <modelo> <prompt_A> <prompt_B> <rN>`
(p. ej. `doc1 flash A_v1 B_v1 r1`).

1. **Llamada A.** Leer el documento y `prompts/<prompt_A>.md`, sustituir
   `{{TEXTO}}` por el contenido completo del documento, enviar como único
   mensaje de usuario.
2. **Parseo.** Extraer el JSON de la respuesta. Si viene envuelto en una
   cerca ```json … ```, quitarla y reportar que venía así. Si no parsea,
   registrar el fallo y no reintentar.
3. **Verificación en código (no clasifica, solo verifica):**
   - *Literalidad:* cada `cita` debe aparecer tal cual (substring exacto) en
     el documento. Listar las que no.
   - *Cobertura:* quitar del documento, en orden, las citas encontradas;
     reportar lo que sobre que no sea espacio en blanco ni puntuación
     (incluido `#`).
   - *Ids:* que los ids de `soporte` existan y que `argumento` apunte a un
     elemento tipo argumento y `datos` a elementos tipo dato.
4. **Entrada de B.** Con los elementos de A (se excluye `otro`), renumerar:
   argumentos `A1, A2…` y datos `D1, D2…` en orden de aparición. Formato,
   una línea por elemento:
   - `A1: "<cita>" (sostenido por D1, D2)` — o `(sin datos)` si no tiene.
   - `D1: "<cita>"`
   Guardar la tabla de correspondencia `E<n> → A<n>/D<n>` en el crudo.
   Si A falló la verificación, correr B de todos modos y marcarlo.
5. **Llamada B.** Leer `prompts/<prompt_B>.md`, sustituir marcadores,
   enviar, parsear igual que en el paso 2.
6. **Crudo:** `niveles/cache/niveles-<doc>-<modelo>-<prompt_A>-<prompt_B>-<rN>.json`
   con, para cada llamada, el request completo (verbatim) y la respuesta
   completa, más el resultado de la verificación y la correspondencia de ids.
   Idempotente: si el crudo existe, no volver a llamar.

## Modelos y credenciales

- Dos modelos GLM que Frat indica al pasar la tarea (uno es GLM 5.3 Flash).
  Confirmar endpoint e id exacto de cada modelo en la documentación del
  proveedor; dejarlos en un dict al inicio del script con alias cortos
  (`flash`, y el alias del segundo).
- Frat configuró las credenciales en el entorno cloud. Si están como
  credencial de API inyectada por proxy, seguir el mismo patrón que Jev:
  nunca construir `Authorization` ni leer la clave. Si la llamada falla por
  autenticación, **detenerse y reportar**; no buscar la clave por otros medios.
- No enviar parámetros extra (temperatura, modos de razonamiento, formato
  JSON forzado): usar los valores por defecto del proveedor y registrar en el
  crudo lo que la respuesta informe (modelo efectivo, tokens).
- Sin SDK: `urllib.request` + dicts planos, como el resto del repo.

## Smoke test (esta ronda)

Correr solo esto, una réplica por modelo:

```
python3 niveles/run_niveles.py doc1 flash A_v1 B_v1 r1
python3 niveles/run_niveles.py doc1 <segundo> A_v1 B_v1 r1
```

## Reporte (a Frat, en el chat)

Por modelo:
1. Salida de A y de B **verbatim** (el JSON tal como llegó).
2. Parseo: bien / fallo / venía con cerca.
3. Literalidad: n citas exactas de N; listar las que fallaron.
4. Cobertura: texto sobrante, citado.
5. Ids de `soporte`: bien / problemas.
6. Tokens y modelo efectivo.

Sin interpretación de calidad ni veredicto: eso lo hacen Frat y Cowork.
Al terminar, commit y push de `niveles/` (script y cache).

---

## Ronda 2: prompts v2 (`A_v2`, `B_v2`)

Lecciones del smoke test que entran en los prompts:
- El título se clasifica por función (en v1 la definición de OTRO lo impedía).
- El nivel 2 se divide en **conclusión** y **garantía** (principio general que
  conecta datos con conclusión). Una conclusión puede apoyarse en otras.
- Los conectores van pegados al fragmento que introducen.
- La tesis no incluye sus razones y tiene un máximo de 25 palabras.
- Los ejemplos de los prompts son de otro tema: nunca de un documento de prueba.

### Cambios en el script (v1 debe seguir funcionando igual)

El esquema depende del prompt A: `A_v1` usa el de la ronda 1; `A_v2` usa este.

**Salida de A_v2:**
```
{"elementos":[{"id","cita","tipo":"dato|conclusion|garantia|otro","duda","nota"}],
 "apoyos":[{"conclusion":"E3","datos":[...],"garantias":[...],"conclusiones":[...]}]}
```
Verificación: literalidad y cobertura igual que en v1. Ids de `apoyos`: que
`conclusion` y cada id de `conclusiones` apunten a elementos tipo conclusion,
`datos` a tipo dato y `garantias` a tipo garantia. Reportar cualquier
desajuste.

**Entrada de B_v2** (se excluye `otro`; renumerar en orden de aparición):
- `{{CONCLUSIONES}}`: una línea por conclusión:
  `C1: "<cita>" (apoyos: datos D1, D2; garantías G1; conclusiones C2)`.
  Omitir las partes vacías; `(sin apoyos)` si no tiene ninguno.
- `{{GARANTIAS}}`: `G1: "<cita>"`
- `{{DATOS}}`: `D1: "<cita>"`
- Si una sección queda vacía, poner `(ninguna)`.
Guardar la correspondencia `E<n> → C/G/D<n>` en el crudo.

### Modelos (ronda 2)

| alias | id | parámetros |
|---|---|---|
| `flash` | `glm-5.3-flash` | `stream: true`, `reasoning_effort: "low"` |
| `deepseek` | `deepseek-flash` (DeepSeek-V4.1-Flash) | `stream: true`, `thinking: {"type":"enabled"}`, `reasoning_effort: "low"` |

Nota (docs.api-docs.deepseek.com): el id a enviar sigue siendo `deepseek-flash`;
los nombres viejos `deepseek-v4-flash`/`deepseek-v4-flash-vision-exp` quedaron
retirados y hoy los sirve el mismo modelo, DeepSeek-V4.1-Flash, al precio Flash.
No hay que cambiar el id en el código por esto.

Excepción autorizada a "no enviar parámetros extra": solo los de esta tabla.
Nada de `temperature`. Si un proveedor rechaza un parámetro, detenerse y reportar.

### Corrida

```
python3 niveles/run_niveles.py doc1 flash A_v2 B_v2 r1
python3 niveles/run_niveles.py doc1 deepseek A_v2 B_v2 r1
```
Reporte igual que la ronda 1, más: tokens de razonamiento de cada llamada.

---

## Ronda 3: una sola llamada, modelo de Toulmin (`prompts/toulmin_v1.md`)

Cambio de diseño: **una sola llamada por modelo**, que clasifica y al final
formula la tesis. Ya no hay llamada B. Las rondas 1 y 2 (A/B) quedan como
están y deben seguir funcionando.

**Uso:** `python3 niveles/run_niveles.py <doc> <modelo> toulmin_v1 - <rN>`
(el `-` en lugar del prompt B indica llamada única).
**Crudo:** `niveles/cache/niveles-<doc>-<modelo>-toulmin_v1-<rN>.json`.

**Salida esperada:**
```
{"elementos":[{"id","cita","tipo":"dato|conclusion|garantia|respaldo|reserva|otro",
               "cualificador","sirve_a":[ids],"duda","nota"}],
 "tesis":{"texto","cercana_a","proposito","sostenida_por":[ids],"fuera":[ids],"sin_tesis","nota"}}
```

**Verificación en código (reportar, nunca corregir):**
1. Literalidad: cada `cita` es substring exacto del documento.
2. Cobertura: igual que en v1/v2.
3. Cualificador: si no está vacío, debe ser substring exacto de la `cita` de su
   elemento, y ese elemento debe ser tipo `conclusion`.
4. `sirve_a` según tipo:
   - `dato`, `garantia`, `conclusion` → ids de elementos tipo `conclusion`;
   - `respaldo` → ids tipo `garantia`;
   - `reserva` → ids tipo `conclusion`;
   - `otro` → vacía.
   Una conclusión no puede servirse a sí misma.
5. Tesis: `cercana_a` (si no es null), `sostenida_por` y `fuera` apuntan a
   elementos tipo `conclusion`.
6. Tesis: número de palabras de `tesis.texto` (el límite es 25) y si contiene
   "porque", "ya que" o "debido a". Solo se reporta; no se corrige.

**Modelos:** los mismos parámetros de la ronda 2 (`flash` con
`reasoning_effort: "low"`; `deepseek` = `deepseek-flash` con thinking enabled y
`reasoning_effort: "low"`; ambos con `stream: true`).

**Corrida:**
```
python3 niveles/run_niveles.py doc1 flash toulmin_v1 - r1
python3 niveles/run_niveles.py doc1 deepseek toulmin_v1 - r1
```

**Reporte:** por modelo, la salida verbatim, el parseo, las verificaciones 1 a 6,
los tokens (incluidos los de razonamiento) y el modelo efectivo. Sin veredicto.

---

## Ronda 4: doc2, mismo prompt (`toulmin_v1`), una corrida por modelo

Objetivo: ver hasta dónde el LLM separa de forma confiable cuando el documento
es más complejo. El prompt queda fijo; lo que cambia es el documento. No hay
cambios de código: el script ya soporta `toulmin_v1`.

```
python3 niveles/run_niveles.py doc2 flash toulmin_v1 - r1
python3 niveles/run_niveles.py doc2 deepseek toulmin_v1 - r1
```

**Reporte:** una tabla con una fila por fragmento y dos columnas de
clasificación (flash, deepseek); si los cortes difieren entre modelos, alinear
por texto y marcar la diferencia. Debajo de la tabla, las dos tesis. Después,
las verificaciones 1–6 y los tokens. Salidas verbatim en los crudos; en el
chat, solo tabla y tesis. Sin veredicto.

---

## Ronda 5: `toulmin_v2` (contraargumento y concesión) sobre doc2

Único cambio respecto de `toulmin_v1`: dos funciones nuevas.
- `contraargumento`: posición contraria que el texto presenta para rebatirla.
- `concesion`: algo en contra de la conclusión que el texto admite sin abandonarla.

**Cambios en la verificación 4 (`sirve_a`) solo para `toulmin_v2`:**
- `dato`, `garantia`, `conclusion` → ids tipo `conclusion` o `contraargumento`;
- `respaldo` → ids tipo `garantia`;
- `reserva`, `contraargumento`, `concesion` → ids tipo `conclusion`;
- `otro` → vacía.
Todo lo demás, igual que en `toulmin_v1`. Las rondas anteriores deben seguir
funcionando igual.

```
python3 niveles/run_niveles.py doc2 flash toulmin_v2 - r1
python3 niveles/run_niveles.py doc2 deepseek toulmin_v2 - r1
```

**Reporte:** el mismo formato de la ronda 4 (tabla fragmento × modelo, las dos
tesis debajo, verificaciones 1–6 y tokens), más una columna `sirve_a` por
modelo en la tabla. Sin veredicto.

---

## Ronda 6: `toulmin_v3` + Jev sopesa la clasificación del LLM (doc2)

### Paso 1: LLM con `toulmin_v3`

Cambios respecto de `toulmin_v2`:
- La unidad es la **oración completa**; nunca se corta.
- Cualificador y reserva que van dentro de una conclusión son **campos** de ese
  elemento (`cualificador`, `reserva`), copiados literalmente.
- Nuevo tipo `titulo`: el título es etiqueta.
- Se quitó la regla de conectores (ya no hay cortes).

**Verificaciones para `toulmin_v3`** (las rondas anteriores siguen igual):
1. Literalidad y 2. cobertura: igual.
3. `cualificador` y `reserva`: si no están vacíos, son substrings exactos de la
   `cita` de su elemento, y ese elemento es tipo `conclusion`.
4. `sirve_a`, igual que v2, más: `titulo` → vacía.
5 y 6. Tesis: igual.
7. **Oración completa:** cada `cita`, salvo la del título, termina en `.`, `?` o
   `!`; y el número de elementos es igual al número de oraciones del documento.
   Reportar las que no.

```
python3 niveles/run_niveles.py doc2 deepseek toulmin_v3 - r1
```

### Paso 2: `niveles/jev_sopesa.py` (nuevo)

Uso: `python3 niveles/jev_sopesa.py <crudo_llm.json>`

Lee la salida del LLM y **arma el build de Jev en tiempo de ejecución**: una
sola llamada con un juicio Noul por elemento.

- `state`: el texto completo del documento (`docs/<doc>.md`), tal cual.
- Se omiten los elementos tipo `titulo`.
- Por cada elemento restante, un Noul con clave neutra (`n01`, `n02`…):
  `En este texto, «{cita}» es {etiqueta}: {definición}.`
  | tipo | etiqueta | definición |
  |---|---|---|
  | dato | un dato | el hecho del que se parte; la evidencia |
  | conclusion | una conclusión | lo que el texto quiere establecer |
  | garantia | una garantía | la regla que autoriza a pasar del dato a la conclusión |
  | respaldo | un respaldo | lo que sostiene a la garantía: una norma, un estudio, la experiencia |
  | reserva | una reserva | una oración que establece las condiciones bajo las cuales una conclusión no vale |
  | contraargumento | un contraargumento | una posición o explicación contraria que el texto presenta para rebatirla |
  | concesion | una concesión | algo en contra de la propia conclusión que el texto admite como cierto, sin abandonar la conclusión |
  | otro | otra cosa | no cumple ninguna de las funciones de un argumento |
  (Las definiciones son las del prompt `toulmin_v3`; si el prompt cambia, esta tabla cambia con él.)
- **Un juicio de control**, al final, con la siguiente clave neutra: el primer
  elemento tipo `contraargumento` (si no hay, el primer `dato`) con la etiqueta
  **falsa** «una conclusión: lo que el texto quiere establecer». En el código se
  marca como control; la clave no lo delata.
- `model: "jev-1.13.0"`; mismo patrón de red que los probes (sin
  `Authorization`); avisar si `usage.model` no coincide.
- Crudo: `niveles/cache/jev-<nombre_del_crudo_llm>.json` con
  `{"request": ..., "response": ..., "mapa": {clave: id_elemento, ..., "control": clave}}`.
  Idempotente.

**Lectura (umbral inicial, se ajustará):**
- noul > 0.75 → Jev sostiene la etiqueta del LLM;
- 0.30–0.75 → revisar;
- < 0.30 → Jev no la sostiene.
El control debería quedar < 0.30.

```
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc2-deepseek-toulmin_v3-r1.json
```

### Reporte
1. Tabla del paso 1: fragmento, tipo, cualificador, reserva; debajo, la tesis;
   luego verificaciones 1–7 y tokens.
2. Tabla del paso 2: fragmento, etiqueta del LLM, noul de Jev, lectura
   (sostiene / revisar / no sostiene), con el control en la última fila.
3. El request de Jev verbatim, completo.
Sin veredicto.

---

## Ronda 6b: build v2 de Jev (definición de dato corregida, sin control)

Hallazgo de la ronda 6: el dato «Pero la planta docente…» sacó 0.66. El LLM lo
clasificó bien; el problema es la definición de dato («el hecho **del que se
parte**; la evidencia»), que define al dato por su papel y no por lo que es. Un
dato es un dato tanto si sostiene como si rebate.

**Cambios en `jev_sopesa.py` (build v2):**
1. En la tabla `ETIQUETAS`, la definición de `dato` pasa a ser:
   `un hecho que el texto presenta como evidencia`
2. **Se elimina el juicio de control** (nada de etiquetas falsas). Se quitan
   `elegir_control` y la clave `control` del mapa.
3. La regla de construcción sigue usando solo `cita` y `tipo`; **no se usa
   `sirve_a`**.
4. Constante `BUILD = "v2"`; crudo nuevo:
   `niveles/cache/jev-v2-<nombre_del_crudo_llm>.json`. El crudo de la ronda 6
   (build v1) queda como está.

Nota: la misma definición de dato entra al prompt del LLM en su próxima
versión, para que LLM y Jev juzguen con la misma norma. Esta ronda no vuelve a
llamar al LLM: usa el crudo existente
`niveles/cache/niveles-doc2-deepseek-toulmin_v3-r1.json`.

```
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc2-deepseek-toulmin_v3-r1.json
```

**Reporte:** tabla fragmento, etiqueta del LLM, noul build v1 (ronda 6), noul
build v2, lectura con v2. Debajo, los juicios que cambiaron entre v1 y v2,
verbatim. Sin veredicto.

---

## Ronda 6c: build v3 de Jev (definición de conclusión corregida)

Hallazgo de la ronda 6b: la conclusión intermedia («Por eso, retrasar la
entrada… probablemente mejoraría…») sacó 0.67, mientras la final sacó 0.95. La
definición «lo que el texto quiere establecer» describe el punto de llegada
del texto (un papel), no lo que una conclusión es.

**Cambio (ya hecho en `jev_sopesa.py`, build v3):** la definición de
`conclusion` pasa a ser `una afirmación que el texto defiende apoyándose en
otras`. Todo lo demás igual que el build v2. Crudo nuevo:
`niveles/cache/jev-v3-<nombre_del_crudo_llm>.json`.

No se llama al LLM: se usa el crudo existente.

```
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc2-deepseek-toulmin_v3-r1.json
```

**Reporte:** tabla fragmento, etiqueta del LLM, noul build v2, noul build v3,
lectura con v3. Debajo, los juicios que cambiaron, verbatim. Sin veredicto.

---

## Ronda 7: `toulmin_v4` + build v4 de Jev, sobre doc3 (nuevo)

Lo que Jev enseñó en las rondas 6b y 6c pasa al prompt del LLM, y prompt y
build usan la misma norma:
- definiciones por lo que la cosa es: dato (un hecho **del caso**),
  conclusión (una afirmación que el texto defiende apoyándose en otras),
  garantía (una regla general que el texto aplica al caso), respaldo
  (evidencia general sobre una **clase de casos**);
- criterio **caso / clase de casos** para separar dato de respaldo;
- criterio **tipo de apoyo** para separar conclusión de garantía.

doc3 es nuevo (peatonalización de una calle; 12 oraciones). Incluye a propósito
una conclusión dicha en términos generales pero apoyada en datos del caso, una
garantía con respaldo, y un dato que viene de una fuente pero habla del caso.

**Cambios de código (ya hechos y revisados):** `run_niveles.py` trata
`toulmin_v4` igual que `toulmin_v3` (mismo esquema, verificaciones 1–7);
`jev_sopesa.py` pasa a build v4 con las definiciones de `toulmin_v4`.

```
python3 niveles/run_niveles.py doc3 deepseek toulmin_v4 - r1
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc3-deepseek-toulmin_v4-r1.json
```

**Reporte:**
1. Paso 1: tabla fragmento, tipo, cualificador, reserva, sirve_a; debajo, la
   tesis; luego verificaciones 1–7 y tokens.
2. Paso 2: tabla fragmento, etiqueta del LLM, noul de Jev, lectura
   (> 0.75 sostiene; 0.30–0.75 revisar; < 0.30 no sostiene).
Sin veredicto.

---

## Ronda 8: `toulmin_v5` + build v5 de Jev, sobre doc3 (el mismo de la ronda 7)

Cambios (prompt y build usan la misma norma):
- **Definiciones generales**, sin «caso» y sin «el texto»:
  dato (un hecho que se presenta como evidencia), conclusión (una afirmación
  que se defiende apoyándose en otras), garantía (una regla general que no se
  prueba con datos), respaldo (evidencia general: un estudio, una norma, la
  experiencia acumulada), reserva (una condición bajo la cual una conclusión no
  vale), contraargumento (una posición contraria que se presenta para
  rebatirla), concesión (algo en contra de la propia conclusión que se admite
  como cierto, sin abandonarla).
- Se quitan las secciones de criterios (caso/clase, tipo de apoyo): su
  contenido quedó dentro de las definiciones, que es lo único que ve Jev.
- **Sin tipo «otro»**: el universo de funciones queda cerrado. Si aparece una
  oración que no encaja, lo debe marcar Jev con nota baja.
- **`texto`**: el prompt nombra el material como `texto`; en Jev, `state` es
  `{"texto": ...}` y el juicio es `En `texto`, «{cita}» es {etiqueta}: {definición}.`
  (guía §4.1 y §4.3).

**Código (ya hecho y revisado):** `run_niveles.py` trata `toulmin_v5` como
v3/v4; `jev_sopesa.py` pasa a build v5. Si el LLM devolviera un tipo fuera de
la lista (por ejemplo «otro»), `jev_sopesa.py` se detiene con error: reportarlo
tal cual.

```
python3 niveles/run_niveles.py doc3 deepseek toulmin_v5 - r1
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc3-deepseek-toulmin_v5-r1.json
```

**Reporte:**
1. Paso 1: tabla fragmento, tipo (v4 → v5), cualificador, reserva; debajo,
   la tesis; luego verificaciones 1–7 y tokens.
2. Paso 2: tabla fragmento, etiqueta del LLM, noul build v4 (ronda 7), noul
   build v5, lectura con v5.
Sin veredicto.

---

## Ronda 8b: build v5b de Jev (garantía con «hechos particulares»)

Hallazgo de la ronda 8: la garantía de doc3 bajó de 0.69 a 0.59 con la
definición «una regla general que no se prueba con datos». El texto la
confirma con estudios, que también son datos en sentido amplio; al quitar
«caso» se perdió la separación entre los hechos particulares y la evidencia
general (respaldo).

**Único cambio (ya hecho en `jev_sopesa.py`, build v5b):** garantía = `una
regla general que no se prueba con hechos particulares`. Todo lo demás igual
que v5. No se llama al LLM: se usa el crudo existente.

```
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc3-deepseek-toulmin_v5-r1.json
```

**Reporte:** tabla fragmento, etiqueta del LLM, noul build v5, noul build v5b,
lectura con v5b. Debajo, el juicio que cambió, verbatim. Sin veredicto.

---

## Ronda 9: `toulmin_v6` + build v6 de Jev, sobre doc3

Cambios respecto de `toulmin_v5` / build v5 (prompt y build usan la misma norma):
- la garantía se define por su papel, con la pregunta de Toulmin: `una regla
  general que autoriza pasar de un dato a una conclusión`;
- **sin ejemplos en ninguna parte** (decisión de Frat): se quitan del prompt
  las frases de ejemplo de cada función y las listas ilustrativas (palabras de
  cualificador y reserva, propósitos, palabras prohibidas en la tesis); el
  respaldo pasa a `evidencia de alcance general que sostiene una regla general`.

**Código (ya hecho y revisado):** `run_niveles.py` trata `toulmin_v6` como
v3–v5; `jev_sopesa.py` pasa a build v6.

```
python3 niveles/run_niveles.py doc3 deepseek toulmin_v6 - r1
python3 niveles/jev_sopesa.py niveles/cache/niveles-doc3-deepseek-toulmin_v6-r1.json
```

**Reporte:**
1. Paso 1: tabla fragmento, tipo v5 → v6; debajo, la tesis; verificaciones
   1–7 y tokens.
2. Paso 2: tabla fragmento, etiqueta del LLM, noul build v5 (ronda 8), noul
   build v5b (ronda 8b), noul build v6, lectura con v6.
Sin veredicto.

---

## Ronda D1: smoke test del objeto «dato» (solo LLM)

Comprueba si DeepSeek entiende el objeto dato con definición y plantilla, sin
ejemplos. Sin Jev. El código solo orquesta (no verifica nada).

- Prompt: `niveles/prompts/datos_v1.md`.
- Script: `niveles/extraer_datos.py` (ya hecho y revisado; no modificarlo).

```
python3 niveles/extraer_datos.py doc2 deepseek datos_v1 r1
```

**Reporte:** los objetos `datos` tal como llegaron (JSON verbatim), si venía
con cerca o hubo error de parseo, y tokens (incluidos los de razonamiento).
Sin veredicto.

---

## Ronda D2: datos y afirmaciones (solo LLM), doc4 (nuevo)

Dos objetos en una sola llamada:
- **dato** (con los ajustes de D1: caso concreto, no una clase; registra lo que
  es o lo que será, no lo que debería ser);
- **afirmación**: un enunciado mediante el cual se asegura o sostiene algo
  (campos `oracion`, `afirmacion`).
El título es etiqueta: no da datos ni afirmaciones. Sin ejemplos. Sin Jev.

doc4 (árboles de una avenida; 10 oraciones contando el título) trae: datos con
y sin escala, un dato comparativo, una predicción, un dato con fuente, una
oración con varios datos, una concesión, una regla general, una posición de
otros («los comerciantes dicen…»), una valoración y una recomendación.

Se reutiliza `niveles/extraer_datos.py` sin cambios (solo orquesta):

```
python3 niveles/extraer_datos.py doc4 deepseek clasif_v1 r1
```

**Reporte:** los objetos `datos` y `afirmaciones` tal como llegaron (JSON
verbatim), si venía con cerca o hubo error de parseo, y tokens (incluidos los
de razonamiento). Sin veredicto.

---

## Ronda D3: smoke test de datos con jerarquía oración → casos → datos (doc4)

Solo datos, sin afirmaciones ni Jev. Estructura: cada oración con datos es un
objeto; de una oración salen uno o varios casos, y de cada caso uno o varios
datos (`dato`, `variable`, `valor`, `escala`). Definición de dato con los
ajustes de D1 (caso concreto; lo que es o será, no lo que debería ser).

Se reutiliza `niveles/extraer_datos.py` sin cambios (solo orquesta):

```
python3 niveles/extraer_datos.py doc4 deepseek datos_v2 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.

---

## Ronda D4: casos primero, unificados; luego datos (doc4)

Solo datos, sin afirmaciones ni Jev. Cambios respecto de `datos_v2`:
- definiciones propias de **caso** (lo que queda fijado; una misma unidad en
  todo `texto`, aunque se nombre de varias maneras o con pronombres) y de
  **variable** (el aspecto bajo el cual se determina el caso);
- el LLM **identifica y unifica primero los casos** de todo el texto, con sus
  menciones literales (incluidos pronombres), y después registra los datos por
  oración, colgados de un caso ya unificado;
- el **valor va sin la escala**.

Se reutiliza `niveles/extraer_datos.py` sin cambios (solo orquesta):

```
python3 niveles/extraer_datos.py doc4 deepseek datos_v3 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.

---

## Ronda D5: JSON organizado por caso (doc4)

Solo datos, sin afirmaciones ni Jev. Cambios respecto de `datos_v3`:
- el prompt se ordena en TAREA, DEFINICIONES PARA CUMPLIR LA TAREA y
  ESTRUCTURA DEL JSON DE RESPUESTA;
- el JSON se organiza por **caso**: caso → oraciones donde aparece → datos de
  cada oración; sale `menciones`;
- la variable dice: si algo es un aspecto de un caso, es variable de ese caso,
  no un caso propio;
- la escala dice «no el valor mismo».

Se reutiliza `niveles/extraer_datos.py` sin cambios (solo orquesta):

```
python3 niveles/extraer_datos.py doc4 deepseek datos_v4 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.

## Ronda D6: dato según el ensayo; escala obligatoria (doc4)

Solo datos, sin afirmaciones ni Jev. Cambios respecto de `datos_v4`:
- TAREA: identificar los **datos** registrados en `texto` (no los casos);
- definiciones alineadas con el ensayo «¿Qué es un dato?»: valor = posición o
  elemento de una escala; escala = sistema al que pertenece todo valor;
  vuelven las condiciones constitutivas;
- sección REGLAS: método casos → variables → datos; prueba de la pregunta
  `<variable>(<caso>, <condiciones constitutivas>) = ?`; sin caso, variable,
  valor o escala no hay dato; cada determinación una sola vez; un caso sin
  datos no va en el JSON; plan o intención es determinación de quien lo tiene;
- JSON: valor tal como lo expresa `texto`; escala obligatoria; nuevo campo
  `condiciones_constitutivas`.

Conjetura: exigir la escala elimina los valores que son enunciados
(«registro», «declaración», «plan» de D5).

Se reutiliza `niveles/extraer_datos.py` sin cambios (solo orquesta):

```
python3 niveles/extraer_datos.py doc4 deepseek datos_v5 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.

## Ronda D7: condiciones constitutivas con el criterio del ensayo (doc4)

Un solo cambio respecto de `datos_v5`: la definición de condiciones
constitutivas usa el criterio del ensayo (si cambiara, la pregunta sería otra)
y excluye la procedencia («No es de dónde proviene el valor»).

Conjetura: «según la oficina de tránsito» y «medición municipal» salen de las
condiciones; «verano pasado» se queda.

```
python3 niveles/extraer_datos.py doc4 deepseek datos_v6 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.

## Ronda D8: `datos_v6` sobre un documento nuevo (doc5)

Mismo prompt que D7 (`datos_v6`), sin cambios. Documento nuevo:
`niveles/docs/doc5.md` (sintético, pozo de Los Robles, ~190 palabras).

Qué pone a prueba respecto de doc4: una misma variable con valores distintos
bajo condiciones constitutivas distintas; valores no numéricos (escala nominal
y ordinal); procedencia en dos formas; un caso nombrado de varias maneras y la
frontera entre dos casos cercanos; oraciones que no deberían dar datos (clase,
normativa, título); material abierto para la decisión sobre planes y dichos
(atribución de causa, dicho con dato adentro, cifra fijada por una norma,
hecho futuro).

```
python3 niveles/extraer_datos.py doc5 deepseek datos_v6 r1
```

**Reporte:** el JSON tal como llegó (verbatim), si venía con cerca o hubo
error de parseo, y tokens (incluidos los de razonamiento). Sin veredicto.
