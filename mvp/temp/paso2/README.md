# Paso 2 · extracción de datos por unidad

Extrae los datos de una unidad temática con el candidato
`prompt_ficha_contexto.md` (derivado de `ficha_v1`, que no se toca) y la
partición **congelada** de v9. **Base de trabajo provisional: la entrada (b)** —
las oraciones de la unidad y, como contexto que aclara y no amplía, las
referencias de v9 con sus respaldos.

Esta carpeta es de trabajo: el candidato **no** se mueve a `mvp/prompts/`
mientras no se adopte.

## Requisitos para procesar una salida de v9 (entrada b)

1. **Documento** sintético en Markdown, con párrafos (p. ej.
   `mvp/temp/paso2/reserva_b.md`). El código conserva la numeración original de las
   oraciones.
2. **Salida de v9** del mismo documento: el JSON con `subtemas` —`subtema`,
   `oraciones` y `referencias` (cada una con `oracion`, `expresion`,
   `referente` —o `null` si quedó sin resolver—, `respaldo` y `duda`)—, tal como
   lo produce el paso 1 con `unidades_v9`. Ejemplos guardados:
   `mvp/temp/paso2/salida_reservaA-v9.md` y `salida_reservaB-v9.md`.
3. **El candidato** `prompt_ficha_contexto.md`, con un único
   `{{TEXTO_NUMERADO}}` y un único `{{CONTEXTO}}` (se sustituyen con
   `str.replace`).
4. **Identificación nueva** para cada corrida: la réplica `rN`. Un crudo que ya
   existe **no se vuelve a llamar ni se sobrescribe**; para repetir hay que usar
   un `rN` nuevo.
5. **Clave del proveedor** en el entorno solo para `correr` (llega por
   `call_model`; los shells no interactivos la cargan con `bash -ic`). `seco` y
   `verificar` **no** llaman a ningún modelo ni necesitan clave. Ninguna clave
   se escribe en el repo.

## Comandos

Desde la raíz del repo:

```bash
# Armar las tres entradas y ver qué se enviaría (no llama a la API)
python3 mvp/temp/paso2/comparacion.py seco <doc.md> <salida_v9> <unidad_n>

# Procesar la salida de v9 con la entrada (b) y deepseek-flash
python3 mvp/temp/paso2/comparacion.py correr <doc.md> <salida_v9> deepseek r2 b

# Ver las tres entradas de cada unidad, una al lado de la otra
python3 mvp/temp/paso2/comparacion.py resumen <doc.md> <salida_v9> deepseek r2

# Re-verificar crudos guardados SIN llamar a ningún modelo
python3 mvp/temp/paso2/comparacion.py verificar mvp/temp/paso2/cache/comp-<...>.json
python3 mvp/temp/paso2/comparacion.py verificar-todos
```

Para Muse hay dos envoltorios: `comparacion_muse.sh` (una tarea por documento,
entrada y unidad; salta los crudos existentes) y `muse_reserva.sh` (la reserva
con la entrada b). Muse admite una sola tarea a la vez, y el aviso de fin va por
ntfy.

## Salidas

Cada corrida deja **un crudo** en
`mvp/temp/paso2/cache/comp-<doc>-<entrada>-<unidad>-<modelo>-<rN>.json` con:

- **Procedencia:** `doc`, `salida_v9`, `unidad`, `oraciones`, `subtema`.
- **Lo que se envió:** `texto_enviado`, `contexto_enviado` (referencias con su
  respaldo y, si vienen sin resolver, `SIN RESOLVER` con su duda) y
  `prompt_enviado` entero.
- **Referencias:** la lista de v9 tal cual, incluidas las irresueltas.
- **Lo que se recibió:** `response` (sin los frames SSE, que son transporte),
  `modelo_efectivo`, `tokens` (`entrada`, `salida`, `razonamiento`) y
  `error_parseo`.
- **Verificación:** `informe`, con los literales comprobados contra el material
  efectivamente enviado (unidad, unidad + fragmentos de las referencias, o
  documento completo según la entrada), más las citas fuera de la unidad y las
  de oraciones no recibidas.

Las salidas del paso 1 sobre la reserva (`salida_reservaA-v9.md`,
`salida_reservaB-v9.md`, `.jsonl`, `.err` y `_meta.json`) y los crudos de Muse
(`muse/`) se guardan en esta carpeta.

## Verificación offline (sin API)

`verificar` y `verificar-todos` releen un crudo, reconstruyen la unidad y el
documento a partir de `texto_enviado` y `contexto_enviado`, vuelven a comprobar
los literales y comparan el informe con el guardado. Comprueban además que el
texto y el contexto aparezcan una sola vez en el prompt (en (c) el documento del
contexto tiene que traer todas las oraciones de la unidad) y que las oraciones
guardadas coincidan con el texto enviado. **Estado al 06-10-2026: 69 crudos
revisados, 0 con diferencias o incoherencias.**

## Resultados y evaluación

- Informe de la ronda: `informe_paso2.md`.
- Inventario y costos verificados: `inventario_y_costos.md`.
- Evaluación por ítem: `evaluacion_items.md` (sustituye los totales agregados).
- Detalle por entrada: `evaluacion_desarrollo.md`, `evaluacion_reserva.md`.
- Lecciones: `hallazgos.md`; expectativas: `expectativas_desarrollo.md` y
  `expectativas_reserva.md`; especificación: `especificacion_comparacion.md`.
