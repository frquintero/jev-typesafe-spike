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
