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
