# Paso 2 · inventario y costos (contra los crudos) · 06-10-2026

Todo lo de aquí sale de los archivos guardados en `mvp/paso2/` —`cache/`,
`muse/`, los `.json` de las tareas, los `.log` de las corridas y
`~/cache` ya copiado—, sin llamadas nuevas. **Resultados, tareas lanzadas e
intentos fallidos no son el mismo conteo**; se separan.

## 1. Resultados guardados

`cache/` tiene **69 crudos** `comp-*.json` (prompt enviado, respuesta,
`usage`, informe de verificación y ficha `parsed`):

| Conjunto | Modelo | Documentos | Entradas | Réplica | Crudos |
|---|---|---|---|---|---|
| Desarrollo | `deepseek-flash` | doc4 (6 unidades) y doc5 (5) | a, b, c | r1 | 33 |
| Desarrollo | Muse Code | doc4 (6 unidades) | a, b, c | r1 | 18 |
| Reserva | `deepseek-flash` | reserva_a (7) y reserva_b (5) | b | r1 | 12 |
| Reserva (sin uso) | Muse Code | reserva_a (U1–U6) | b | r1 | 6 |

- **En el análisis entran 63** (33 + 18 + 12). Los **6 de Muse de la reserva**
  se recolectaron, pero quedaron **fuera** por la corrida interrumpida.
- **Verificación mecánica de los 63:** 0 respaldos no verificables
  (`no_literales = 0` en las 63 fichas), 0 citas de oraciones no recibidas, y
  39 citas **fuera de la unidad** (legítimas: vienen del contexto de (b) o del
  documento de (c); están contadas en el `informe` de cada crudo).
- **Un fallo de parseo:** `comp-doc4-c-u3-muse-r1.json` (JSON inválido). Es un
  resultado guardado, pero sin ficha.
- Además hay dos salidas del paso 1 sobre la reserva (`salida_reservaA-v9.md`,
  `salida_reservaB-v9.md`), con su `.jsonl`, `.err` y `_meta.json`.

## 2. Tareas lanzadas

| Quién | Qué | Lanzadas | Con resultado | Sin resultado |
|---|---|---|---|---|
| `comparacion.py` (DeepSeek) | 33 de desarrollo + 12 de la reserva | **45** | 45 | 0 |
| `comparacion_muse.sh` | 18 de desarrollo (17 en la barrida `r1` + `doc4 a u3` suelta) | **18** | 18 | 0 |
| `muse_reserva.sh` | reserva (b): reserva_a U1–U7 | **7** | 6 | **1** (U7: lanzada 14:11:23 sin `.json` ni crudo) |
| `reserva_muse.sh` | paso 1 (v9) sobre reserva_a y reserva_b | **2** | 2 (72 s y 65 s) | 0 |
| `muse_reserva.sh` | reserva_b U1–U5 | 0 | 0 | **no se llegó a lanzar** |

No hay reintentos de lanzamiento en los `.log` (los envoltorios los tenían
previstos). **Intentos fallidos:** el fallo de parseo de Muse (`doc4 c u3`),
la U7 de la reserva lanzada sin resultado, y los **27 primeros crudos de
DeepSeek**, que el informe registra como corridos «por un error mío de
modelo» (primera pasada de 12:13 a 12:38: doc4 completo + doc5 a + doc5 b
U1–U4); se conservan íntegros y entran al análisis por decisión de Frat. La
naturaleza de ese error **no es reconstruible** con lo guardado (los 27 usan
`deepseek-flash` con `reasoning_effort: low`, igual que el resto).

## 3. Tiempo: tarea y modelo no son lo mismo

| Conjunto | Lo que mide `segundos` | Total | Rango por corrida |
|---|---|---|---|
| DeepSeek desarrollo (33) | **duración de la llamada** | 1 903,9 s | 29,0–84,2 s |
| DeepSeek reserva (12) | **duración de la llamada** | 646,2 s | 32,9–80,5 s |
| Muse desarrollo (18) | **tiempo del envoltorio** | 4 303 s | 65–2 646 s |
| Muse reserva (6, sin uso) | **tiempo del envoltorio** | 838 s | 88–209 s |

- **DeepSeek** guarda la latencia de la llamada, que es del modelo.
- **Muse** guarda el tiempo del envoltorio, que **no** es el del razonamiento:
  incluye el arranque, el reintento tras el fallo de transporte y la cola.
  Caso extremo, `p2-doc4-c-u6-r1` (sesión `9d818528-f000-43c6-ae4d-4fcd5b0a2bfb`):
  2 646 s de envoltorio, con **un timeout de transporte** (net-timeout:
  «180 KiB received, 47s», intento 1/10, reintento) y luego un stream
  completado. El `.jsonl` de la sesión tiene marcas de tiempo sintéticas, así
  que **la duración del modelo no se puede reconstruir de los archivos del
  repo**; el dato reportado (~76,7 s de la respuesta completada, 6 222 tokens
  de razonamiento) se registra como **reportado, no verificado aquí**, y **no
  se atribuye a toda la duración**.
- **Comparación limpia (solo DeepSeek, latencia de llamada):** en total, (b)
  usa 20,6 s menos que (a) y 34,4 s menos que (c) (≈3–5 %); es la más barata
  de las tres.

## 4. Consumo (DeepSeek, del `usage` de cada crudo)

`reasoning_tokens` viene **incluido** en `completion_tokens`; no se suma otra
vez.

| Conjunto | Llamadas | Entrada | Salida (`completion`) | De eso, razonamiento |
|---|---|---|---|---|
| Desarrollo | 33 | 95 749 | **441 768** | 402 145 (91,0 %) |
| Reserva | 12 | 34 088 | **149 021** | 136 065 (91,3 %) |
| **Total** | **45** | **129 837** | **590 789** | **538 210** |

Por entrada (desarrollo): (a) 11 llamadas, 147 967 de salida, 636,9 s;
(b) 11 llamadas, 145 171, 616,3 s; (c) 11 llamadas, 148 630, 650,7 s.
Reserva (b): 12 llamadas, 149 021, 646,2 s.

**No se calcula costo monetario:** la reserva de Muse es suscripción y para
DeepSeek no se aplicó tarifa. El consumo queda en tokens.

## 5. Reconciliación con la revisión de Astra

| Dato | Informe anterior | Verificado en los crudos | Estado |
|---|---|---|---|
| Llamadas DeepSeek de desarrollo | 51 (mezclaba el total del paso 2) | **33** | corregido |
| Tokens de salida de esas 33 | 316 000 | **441 768** | corregido |
| Llamadas DeepSeek de reserva | (no separado) | **12** | corregido |
| Tokens de salida de la reserva | (no separado) | **149 021** | corregido |
| Crudos del análisis | 51 | **63** (33 + 18 + 12) | corregido |
| «85–90 % del texto generado es razonamiento» | 85–90 % | **91,0 % / 91,3 %** | corregido |
| Ítems esperados en desarrollo | 57 | **42 expectativas registradas** | corregido (§ evaluación) |

Los números que Astra dio para DeepSeek (33/441 768 y 12/149 021) **se
confirman**. El «51» del informe anterior era el total del paso 2 mal
contado —y sin separar modelos— y los «316 000» una suma parcial de las 33.
