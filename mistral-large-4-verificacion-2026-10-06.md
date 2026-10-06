# Mistral Large 4 — verificación independiente del informe de Claude (06-10-2026)

Ejecutor: DeepSeek Harness (`deepseek-flash`), sesión lanzada por Frat el 06-10-2026.
Alcance: revisar el informe «Mistral API: resumen para DeepSeek (6-oct-2026)», verificar
sus afirmaciones contra la API y las fuentes públicas, e investigar por cuenta propia lo
que falte. **Sin veredicto y sin decisión de diseño** (AGENTS.md: el ejecutor reporta;
Frat y Cowork planean; el spike no concluye).

- `[A]` = verificado por mí hoy contra `https://api.mistral.ai/v1` con la cuenta de Frat.
- `[D]` = verificado hoy en documentación pública (URL citada).
- `[?]` = no verificado o contradictorio.

---

## 1. Reglas de AGENTS.md que aplican (leído completo, 228 líneas)

| Regla (`AGENTS.md`) | Lo que implica aquí |
|---|---|
| l. 145–168, «Red y claves» | Las llamadas a modelos pasan por `call_model` (`niveles/run_niveles.py`); **«Ningún otro código lee claves»**. Las claves del taller son cuatro: TypeSafe, Z.ai, DeepSeek, xAI. **`MISTRAL_API_KEY` no está en esa lista ni en el protocolo del repo.** El proxy `proxy_local.py` está retirado desde el 04-10 (l. 122–123 y 147). |
| l. 170–176, «Agentes delegados» | **Autorización expresa y previa de Frat en cada uso**, **exclusivo de Claude y ChatGPT**. |
| l. 4–8, «Ejecutores» | El ejecutor no decide diseño, prompts, umbrales ni veredictos. |
| l. 216–221, «Reportes» | Prompts y campos enviados, verbatim; el crudo detrás de cada afirmación; sin veredicto. |
| l. 30–38, «Proyectos en curso» | Si esto llegara a ser un frente de trabajo, hay que actualizar en el mismo commit el `README.md`, el «Mapa del repo» de `AGENTS.md` y «Dónde quedamos» de la memoria. **No lo hice: no me consta que sea un frente, y los documentos vivos no se editan sin aprobación.** |
| *No está en AGENTS.md* | Nada dice que un agente delegado no pueda usar una API nueva… salvo que la clave no existía en el protocolo. Ver §7. |

**Desviación declarada (mía).** Las sondas de verificación fueron scripts de un solo uso
en `.verif-mistral/` (borrados al cerrar), fuera del repo, que leyeron `MISTRAL_API_KEY`
del entorno directamente con `urllib`. No pasaron por `call_model`. La clave no se
imprimió, no se guardó y no aparece en este documento. Para cualquier uso permanente la
vía es `call_model` (§7.1).

---

## 2. Qué corrí y cuánto costó

- `GET /v1/models` y `GET /v1/models/{id}` (gratis).
- 4 sondas de chat a `mistral-large-4` (forma de `content`, `reasoning_effort`, `temperature`).
- 14 sondas mínimas de disponibilidad por modelo (`max_tokens: 5`).
- 4 sondas de salida estructurada estricta y 8 de estabilidad (réplicas sobre el mismo texto).
- **Gasto total ≈ US$0,005** (1.001 tokens de entrada y 2.093 de salida en ML4 a
  $0,68/$2,09 por millón, más ~600 tokens en Ministral/Codestral). Las llamadas
  rechazadas (429/403/404/400) no se cobran.

---

## 3. Afirmaciones del informe, una por una

| # | Afirma | Resultado | Evidencia |
|---|---|---|---|
| 1 | `mistral-large-4` y `mistral-large-4-0` existen | **Cierto** `[A]` | Ambos en `GET /v1/models`, cada uno con el otro como `aliases` |
| 2 | `mistral-large-latest` no aparece y no hay que asumir que apunta a ML4 | **Cierto, y se explica** `[A][D]` | No está en el listado; además la política de ciclo de vida dice que los alias `-latest` solo los tienen modelos GA y ML4 es Public Preview. La doc de Vibe lista `mistral-large-latest` = **Mistral Large 3** |
| 3 | Contexto de **1M** | **Contradictorio** `[?]` | La ficha del modelo en docs dice «Context 1M»; el metadato de la API devuelve `"max_context_length": 524288` (512K) `[A]`. No lo resolví: una prueba empírica de ~600K tokens cuesta ≈ US$0,41 solo de entrada |
| 4 | Precios: entrada $0,68 (tachado $1,36), salida $2,09 ($4,18), cacheada $0,07 | **Cierto** `[A][D]` | La [página de precios](https://docs.mistral.ai/inference/pricing) ya lista ML4 en «Flagship» con $0,68/$0,07/$2,09 → el «la tabla general aún no lo incluye» del informe ya no se sostiene |
| 5 | «No está claro si la rebaja es temporal» | **Hay evidencia de que es de lanzamiento** `[A]` | `"billing_model_name": "mistral-large-4-0-launch-discount"` en ambos ids |
| 6 | Large 3 $0,5/$1,5; Medium 3.5 $1,5/$7,5; Small 4 $0,15/$0,6; Ministral 3 $0,1/$0,15/$0,2; Codestral $0,3/$0,9; OCR $4/1000 páginas | **Cierto** `[D]` | Tabla de precios, sección por sección |
| 7 | Small 4: 119B MoE, **6B** activos, Apache 2.0 | **Cierto salvo un decimal** `[D]` | La ficha dice «119B parameters with **6.5B** active»; contexto 256k (el informe no lo menciona) |
| 8 | **No existe una línea «Flash»** | **Cierto** `[A]` | Ningún id del listado contiene «flash» (48/48 revisados) |
| 9 | «Magistral, Devstral y Pixtral están deprecados» | **Parcialmente falso** `[A][D]` | `devstral-medium-latest` → HTTP 404 `Model ... is deprecated`. `pixtral-large-latest` → 404 `was not found`. Pero `magistral-medium-latest` y `magistral-small-latest` **responden y siguen en el listado con `deprecation: null`**; la doc sí los da por deprecados. Doc contra API, sin resolver |
| 10 | Clave en `~/.config/mistral.env` (600) cargada por `~/.bashrc`; los shells no interactivos no la cargan | **Cierto** `[A]` | Archivo presente con permisos `-rw-------`, línea 152 del `~/.bashrc`, y `MISTRAL_API_KEY: SET` con `bash -ic` |
| 11 | `GET /v1/models` → HTTP 200 con **48 modelos** | **Cierto** `[A]` | 48 exactos, todos `type: "base"` |
| 12 | `proxy_local.py` inyecta claves por host y «faltaría una línea» | **Desactualizado** `[A]`/AGENTS.md | El proxy está retirado desde el 04-10. El sitio donde va Mistral es `CLAVE_POR_HOST` en `niveles/run_niveles.py:30-35` (más `MODEL_PARAMS`) |
| 13 | `reasoning_effort`: `"high"` o `"none"`; con `high`, `content` pasa a lista de bloques; sin el parámetro es string; `usage` no trae `reasoning_tokens` | **Cierto, con más detalle** `[A][D]` | Ver §4.1 |
| 14 | Solo probó `"high"`; `"none"` sin probar | **Probado** `[A]` | `"none"` → HTTP 200, `content` string, 2 tokens de salida, 0,98 s |
| 15 | Prueba: respuesta «7», 1013 tokens de salida | **Reproducida** `[A]` | Con `high`: «7», 1.794 tokens de salida, 23,83 s |
| 16 | Salidas estructuradas con `json_schema` estricto | **Cierto y probado en esta cuenta** `[A]` | Ver §4.2 |
| 17 | `web_search`/`web_search_premium` solo en Conversations y Agents | **Cierto, con matiz** `[D]` | El aviso añade `code_interpreter`; `image_generation` **sí** funciona en chat completions |
| 18 | Vibe CLI programático: `--prompt`, `--max-turns`, `--max-price`, `--max-tokens`, `--output`, `--enabled-tools`; aprueba todo por defecto | **Cierto en lo esencial** `[D]` | Confirmados `--prompt`, `--max-turns`, `--enabled-tools`, `--output` y que el modo programático corre con `auto-approve`. `--max-price`/`--max-tokens` no los vi hoy `[?]` |
| 19 | Servidor MCP de Mistral: administra el workspace (Skills), **no expone los modelos** | **Cierto** `[D]` | El servidor expone el workspace como herramientas MCP; la primera capacidad son Skills |
| 20 | Avisos MAI-2026-002 (SDK) y MAI-2026-003 (Vibe) | **Cierto, y son más graves de lo que sugieren los títulos** `[D]` | Ver §4.4 |
| 21 | Batch: 50 % de descuento; máximo 100.000 solicitudes o 512 MB | **50 % cierto; topes no vistos** `[D]` | El descuento está en la doc y en la columna «Batch» de precios; los topes no los encontré en la parte leída `[?]` |

---

## 4. Hallazgos que no están en el informe

### 4.1 Forma exacta de la respuesta con razonamiento `[A]`

```
reasoning_effort=high  →  content = [
    {"type": "thinking", "thinking": [{"type": "text", "text": "..."}], "closed": false},
    {"type": "text", "text": "7"}
]
```
- El bloque de pensamiento lleva una clave **`closed`** que el informe no menciona.
- `usage` = `{"prompt_tokens":35, "total_tokens":1829, "completion_tokens":1794,
  "prompt_tokens_details":{"cached_tokens":0}, "service_tier":"standard"}`:
  **no hay `reasoning_tokens`** (confirmado) y aparecen `prompt_tokens_details.cached_tokens`
  y `service_tier` (útiles para la tarifa cacheada y para Priority Tier).
- Latencia de la misma pregunta: **1,19 s** sin razonamiento, **23,83 s** con `high`.
- `[D]` `reasoning_effort` lo soportan `mistral-small-latest`, `mistral-medium-3-5`,
  `mistral-large-4-0` y `zai-glm-5-3` (este último con `low|high|max`, **sin `none`**, y
  siempre devuelve bloques). En Agents/Conversations el parámetro va en `completion_args`.

### 4.2 Salida estructurada estricta: funciona en ML4 `[A]`

`response_format` con `json_schema` `strict: true` y `additionalProperties: false` →
HTTP 200 en 1,48 s, `content` string con JSON válido y exactamente las claves del esquema.
También funciona en `ministral-14b-latest`, `ministral-8b-latest`, `ministral-3b-latest`
y `codestral-latest` (§4.3).

### 4.3 Restricción no documentada en el informe: `temperature: 0` + `reasoning_effort: "high"` → 400 `[A]`

```
HTTP 400  top_p must be 1 when using greedy sampling.
```
Si alguien quiere razonamiento con muestreo determinista, tiene que mandar `top_p: 1`.

### 4.4 Los dos avisos de seguridad, leídos `[D]`

- **MAI-2026-002** (12-05-2026, *High*, cerrado): ataque de cadena de suministro
  «Mini Shai-Hulud» vía TanStack. La versión PyPI **`mistralai` 2.4.6 ejecuta un script
  malicioso al importar** que descarga y lanza un proceso en segundo plano para cosechar
  credenciales (solo Linux). Afectados también `@mistralai/mistralai` 2.2.2–2.2.4.
  → El «por ahora se usa `curl`, sin SDK» del informe no es una preferencia estética:
  tiene una razón concreta y fechada.
- **MAI-2026-003** (14-09-2026, *High*): seis CVE (2026-87983 … 2026-87988) en las
  comprobaciones de permisos de shell de Vibe, corregidas en **2.25.4**. En versiones
  afectadas, contenido malicioso procesado por el agente podía ejecutar comandos **sin el
  aviso de aprobación**, con capacidad de leer credenciales y escribir fuera del
  workspace. Y la doc de Vibe dice que el **modo programático corre con `auto-approve`**;
  el propio aviso pide «mantener las comprobaciones activas cuando se exigen aprobaciones».
  → Choca de frente con la regla dura de AGENTS.md (l. 175): autorización previa de Frat
  en cada uso.

### 4.5 Vibe CLI se puede invocar **como modelo de chat** `[A]`

`GET /v1/models` de la cuenta lista `mistral-vibe-cli-latest`, `mistral-vibe-cli-fast` y
`mistral-vibe-cli-with-tools`, con capacidades `completion_chat` + `function_calling` +
`reasoning` y `billing_model_name: mistral-medium-3-5`. Es decir: hay una vía por API para
lanzar un agente con herramientas. No la llamé (AGENTS.md: ningún agente delegado lanza a
otro; y esta sesión es un agente delegado). En esta cuenta responde 429 con cuota 0 (§5).

### 4.6 El listado de modelos **no** es un oráculo de disponibilidad `[A]`

`zai-glm-5-3` no aparece en `GET /v1/models`, pero `GET /v1/models/zai-glm-5-3` responde
200 y el chat devuelve **403 `tier_not_allowed`**. La [página de precios](https://docs.mistral.ai/inference/pricing)
lo anuncia como «third-party hosted» a $1,4/$4,4 y la doc de Vibe lo lista como modelo
utilizable. Lo mismo con `shieldstral-1-0`: 404 en esta cuenta aunque esté documentado.
Conclusión operativa: «no está en el listado» ≠ «no existe» (lo que sí se sostiene es el
caso de `mistral-large-latest`, explicado por la política de alias en §3.2).

### 4.7 Estado real de **esta** cuenta, modelo por modelo `[A]`

| Resultado | Modelos | Nota |
|---|---|---|
| **200 y usable** | `mistral-large-4` (50 req/min), `ministral-14b-latest` (30), `ministral-8b-latest` (188), `ministral-3b-latest` (750), `codestral-latest` (125) | ML4 además con `x-ratelimit-limit-tokens-minute: 20000` |
| **429 con cuota 0** (`x-ratelimit-limit-req-minute: 0`, persiste en intentos repetidos) | `mistral-medium-latest`, `mistral-medium-3-5`, `mistral-small-latest`, `mistral-small-2603`, `magistral-medium-latest`, `magistral-small-latest`, `mistral-vibe-cli-latest` | **Incluye Small 4 y Medium 3.5**, los candidatos del informe |
| **403 `tier_not_allowed`** | `mistral-large-latest` (Large 3), `zai-glm-5-3` | |
| **403 `labs_not_enabled`** | `labs-leanstral-1-5` | Un admin debe habilitar Labs en la organización; la doc lo marca como gratuito |
| **404** | `devstral-medium-latest` («is deprecated»), `pixtral-large-latest` («not found»), `shieldstral-1-0`, `mistral-small-4-0-26-03` | El último es el **slug de la doc**, no el id de la API (el real es `mistral-small-2603`) |

Esto último importa para el informe: su candidato nº 1 («Small 4 con `json_schema` estricto
y batch a mitad de precio, junto a Grok 4.7 y DeepSeek») **no corre en esta cuenta hoy**:
Small 4 devuelve 429 de cuota 0 en tres intentos seguidos y también con y sin esquema.
Lo barato que sí corre en esta cuenta es la familia **Ministral 3** (3B/8B/14B) y Codestral.

### 4.7 bis Plan real de la cuenta (captura de Frat, `admin.mistral.ai/subscription`, 06-10) `[A][D]`

La captura muestra: plan **Free**, «Included API usage» **$0,01 / $10** (reinicia en 25 días),
«Included Vibe Code usage» **$0 / $10**, y «API pay-as-you-go» **apagado** (botón «Enable»).

- Un solo plan y **una sola bolsa mensual compartida** entre Studio, API y Vibe Code; la
  página la desglosa por producto `[D]`.
- Los $0,01 cuadran con el gasto medido en §2 (≈US$0,005 en mis sondas más las dos llamadas
  previas del informe de Claude).
- Consecuencia para §4.7: los 429/403 **no son agotamiento de la bolsa** (queda casi entera),
  sino límites por modelo o de tier (`x-ratelimit-limit-req-minute: 0`, `tier_not_allowed`).
  El sitio para verlos es **Admin › Limits**.
- Con pay-as-you-go apagado, al agotarse la bolsa el uso **se detiene** hasta el reinicio
  mensual (o hasta que un admin lo active) `[D]`.
- Orden de magnitud con la bolsa entera (estimación, no medición): ML4 a $0,68/$2,09 por
  millón → una ficha del tamaño de las de DeepSeek (~20K tokens de salida, más razonamiento)
  ronda **US$0,04–0,05**, o sea ~200–250 fichas por mes con los $10 completos.
- En esta máquina Vibe Code **no se ha usado nunca**: no existe `~/.vibe/` y la clave vive
  solo en `~/.config/mistral.env`. La huella corta del valor es
  `sha256[:16]=005446e681f85e92` (no se imprime la clave); con eso se puede comprobar más
  adelante si la clave cambia sin volver a exponerla.

### 4.8 Réplicas y estabilidad (sonda, no medición) `[A]`

Mismo texto de dos oraciones, mismo esquema estricto, mismas instrucciones:

| Modelo / ajuste | Réplicas | Salidas distintas |
|---|---|---|
| `mistral-large-4`, temperatura por defecto (1.0) | 3 | 2 (r1 = r2 normalizado; r3 literal) |
| `mistral-large-4`, `temperature: 0` | 3 | **3** (no es determinista ni con temperatura 0) |
| `ministral-14b-latest`, `temperature: 0` | 2 | 1 |
| `ministral-8b-latest`, `temperature: 0` | 2 | 2 («18 C» / «18 °C») |
| `ministral-3b-latest`, `temperature: 0` | 2 | 2 (una parafrasea, otra recorta) |

Latencia: 0,77–1,49 s por llamada en todos los casos sin razonamiento. Esto es una sonda de
forma, **no** una medición del extractor: no hay esperado escrito antes ni reserva
independiente, así que no dice nada sobre el ≈90 % de contenido correcto. Lo que sí dice:
la disciplina de réplicas del repo sigue haciendo falta, y `temperature: 0` no la sustituye.

### 4.9 Ciclo de vida: Public Preview no es gratis en reproducibilidad `[D]`

- Public Preview: **permite actualizaciones silenciosas**, no tiene camino garantizado a GA
  y puede retirarse antes de llegar.
- Los alias `-latest`/`-major` son **solo de modelos GA**; por eso ML4 no tiene `-latest`.
- Aviso: usar alias expone a cambios silenciosos de comportamiento y de precio; para
  control fino hay que fijar `mayor.menor`.
- Fijar `mistral-large-4-0` hoy **no congela el comportamiento**: sigue siendo Preview.
  Es exactamente el problema que el repo ya resuelve anotando el modelo efectivo por crudo.
- Pesos abiertos: la [página de HF](https://huggingface.co/mistralai/Mistral-Large-4.0-1T05-A52B)
  da **31-10-2026** como fecha esperada (275 interesados); la prensa habla del 27-10.
  Licencia: no publicada todavía `[?]`.

---

## 5. Lo que el informe acierta

1. La ficha del modelo (MoE 1,05T/49B, visión 1,6B, multimodal, preview pública, pesos a
   fin de mes).
2. Los dos ids y la ausencia de `mistral-large-latest`, con la advertencia de no asumirlo.
3. Los precios vigentes y tachados, incluida la cacheada.
4. Que no hay línea «Flash».
5. Cómo se carga la clave y que los shells no interactivos no la cargan.
6. La forma de `content` con `high` (lista de bloques `thinking` + `text`) y que `usage` no
   separa `reasoning_tokens`.
7. Que `web_search`/`web_search_premium` no están en chat completions.
8. Que el servidor MCP no expone los modelos.
9. Que la decisión sensata con el SDK es no usarlo (ahora con la razón de MAI-2026-002).
10. La separación Agents/Conversations frente a chat completions para no esconder la ruta
    de procedencia: es coherente con el faro del repo (todo dato con su ruta) y con
    «recuperar no es responder».

---

## 6. Preguntas abiertas (no me toca decidirlas)

1. **Contradicción 512K/1M** en ML4: la API, Vals, AA y Vercel apuntan a 512K (§9.3); solo la
   ficha de Mistral dice 1M. ¿Basta eso, o se pide a Mistral que corrija la ficha?
2. **La cuenta está en plan Free y no da cuota a Small 4 ni a Medium 3.5** (§4.7, §4.7 bis).
   ¿Se pide habilitación/pago a Mistral antes de seguir, o se prueba con lo que sí corre
   (ML4 50 req/min, Ministral 3)? Conviene mirar **Admin › Limits** para distinguir «tier»
   de «límite por modelo».
3. **`MISTRAL_API_KEY` no está en el protocolo del repo.** ¿Se autoriza y se añade a
   `AGENTS.md` (l. 153–156) y a `call_model`, o se mantiene fuera?
4. **¿Esto es un frente de trabajo?** Si sí, falta el mismo commit en los tres sitios
   (README, Mapa del repo, Dónde quedamos) y decidir dónde vive este documento.
5. **Magistral: doc contra API** (§3.9). No lo resolví.
6. **Topes del batch** (100.000 / 512 MB): no los verifiqué.

---

## 7. Consecuencias operativas si Frat autoriza usarlo (hechos, sin veredicto)

1. **Dónde va la clave.** `niveles/run_niveles.py:30-35` (`CLAVE_POR_HOST`) es el único
   sitio previsto; añadir `"api.mistral.ai": "MISTRAL_API_KEY"` deja las llamadas dentro
   de la regla «ningún otro código lee claves». `proxy_local.py` está retirado.
2. **Autorización.** Cualquier uso de Vibe CLI cae en «Agentes delegados»: autorización
   expresa y previa de Frat en cada uso, y ningún agente delegado lanza a otro. El modo
   programático con `auto-approve` contradice el espíritu de esa regla, y MAI-2026-003
   documenta que `auto-approve` salta justamente los controles que estaban rotos.
3. **Procedencia.** La forma natural para lo que el repo ya hace (crudo por corrida,
   modelo efectivo anotado, herramienta ejecutada por el código) es chat completions.
   Agents/Conversations y las herramientas integradas ejecutan en servidor y guardan la
   conversación fuera del repo: la ruta deja de estar en el código.
4. **Reproducibilidad.** ML4 es Public Preview con actualizaciones silenciosas; el
   `billing_model_name` dice «launch-discount». Un crudo de hoy no es comparable con uno
   de la semana que viene sin anotar id exacto, fecha y precio.
5. **Costo del taller.** El costo dominante en el repo es la deliberación del ejecutor, no
   la API. Aquí la API de verificación completa costó ≈ US$0,005; ML4 sin razonamiento
   responde en ~1,4 s y con `high` en ~24 s, frente a los 76–127 s por ficha de DeepSeek.

---

## 8. Crudos (verbatim)

```json
GET /v1/models  → 200, 48 modelos. Ficha de mistral-large-4:
{"id":"mistral-large-4","object":"model","created":1791303487,"owned_by":"mistralai",
 "capabilities":{"completion_chat":true,"function_calling":true,"reasoning":true,
 "completion_fim":false,"fine_tuning":false,"vision":true,"ocr":false,"classification":false,
 "moderation":false,"audio":false,"audio_transcription":false,"audio_transcription_realtime":false,
 "audio_speech":false,"unified_resources":true},
 "name":"mistral-large-4","description":"Official mistral-large-4 Mistral AI model",
 "max_context_length":524288,"aliases":["mistral-large-4-0"],"deprecation":null,
 "deprecation_replacement_model":null,"default_model_temperature":1.0,
 "billing_model_name":"mistral-large-4-0-launch-discount","type":"base"}
```

```json
Cuerpo enviado (sonda B, la única con razonamiento):
{"model":"mistral-large-4","max_tokens":4000,"reasoning_effort":"high",
 "messages":[{"role":"user","content":"Cuantos numeros primos hay entre 90 y 130? Responde solo con el numero."}]}

Respuesta: HTTP 200 en 23,83 s
  model: mistral-large-4
  usage: {"prompt_tokens":35,"total_tokens":1829,"completion_tokens":1794,
          "prompt_tokens_details":{"cached_tokens":0},"service_tier":"standard"}
  content (tipo list): [{"type":"thinking","thinking":[{"type":"text","text":"The user is asking: ..."}],"closed":false},
                        {"type":"text","text":"7"}]
```

```json
Cuerpo con esquema estricto (sonda 3 de verif5):
{"model":"mistral-large-4","max_tokens":400,"temperature":0,
 "response_format":{"type":"json_schema","json_schema":{"name":"unidad","strict":true,
   "schema":{"type":"object","properties":{"oracion":{"type":"integer"},"afirmacion":{"type":"string"}},
             "required":["oracion","afirmacion"],"additionalProperties":false}}},
 "messages":[{"role":"system","content":"Extrae la afirmacion de cada oracion numerada. Responde en JSON."},
             {"role":"user","content":"(1) En la superficie, el agua del estanque norte de la finca El Roble esta a 18 C. (2) Ademas tiene un color verdoso."}]}

Respuesta: HTTP 200 en 1,48 s
  usage: {"prompt_tokens":124,"total_tokens":165,"completion_tokens":41,
          "prompt_tokens_details":{"cached_tokens":0},"service_tier":"standard"}
  content (tipo str):
{
  "oracion": 1,
  "afirmacion": "El agua del estanque norte de la finca El Roble está a 18 °C en la superficie."
}
Nota: el esquema pedía un objeto, no una lista; el modelo devolvió una sola oración.
Es una sonda de forma, no de calidad de extracción.
```

```json
Cabeceras de una llamada aceptada a ML4:
x-ratelimit-limit-tokens-minute: 20000 | x-ratelimit-remaining-tokens-minute: 19259
x-ratelimit-limit-req-minute: 50       | x-ratelimit-remaining-req-minute: 49

Cabeceras de las rechazadas por cuota (Medium 3.5, Small 4, Magistral, Vibe CLI):
x-ratelimit-limit-req-minute: 0        | x-ratelimit-remaining-req-minute: 0
{"object":"error","message":"Rate limit exceeded","type":"rate_limited","code":"1300","raw_status_code":429}
```

```json
GET /v1/models/magistral-medium-latest → 200, deprecation=null, context=262144
GET /v1/models/devstral-medium-latest  → 404 {"message":"Model devstral-medium-latest is deprecated."}
GET /v1/models/pixtral-large-latest    → 404 {"message":"Model pixtral-large-latest was not found."}
GET /v1/models/zai-glm-5-3             → 200 (context=1048576) pero el chat → 403 tier_not_allowed
GET /v1/models/labs-leanstral-1-5      → 200 pero el chat → 403 labs_not_enabled
POST con {"model":"mistral-large-4","temperature":0,"reasoning_effort":"high", ...}
                                       → 400 "top_p must be 1 when using greedy sampling."
```

---

## 9. Los benchmarks de la noticia y la tarjeta «Deep Financial Research» (06-10)

Frat mostró la tarjeta del demo **Deep Financial Research** («Quickest path from Q to A»):
ML4 16 turnos / 67 fuentes, DeepSeek 4 38/121, GLM-5.3 28/77, con un mapa semántico y un
botón «Replay». Es lo que se puede leer de la imagen.

### 9.1 Qué es esa tarjeta (y qué no)

- La propia noticia la llama **demo**, no benchmark: «In this demo, ML4 compared to other
  top OSS models take on the same multistep corporate finance challenge, searching through
  public company filings…». La versión anterior de la página (12:00:27 UTC) decía «ML4 and
  Mistral Medium 3.5»; la actual (13:25:50 UTC) dice «other top OSS models». La página se
  editó en vivo en menos de hora y media `[?]`.
- Mide **esfuerzo de la trayectoria**: turnos y fuentes. No hay columna de acierto, ni
  juez, ni esperado, ni barras de error, ni réplicas. Es **una sola pregunta** («the same
  financial question», en singular) `[A sobre la imagen]`.
- Su propio marco es de eficiencia: «Quickest path from Q to A». Leer eso como calidad
  exige cuatro supuestos que la tarjeta no muestra: (i) los tres acertaron, (ii) mismo
  arnés, mismas herramientas y mismo tope de pasos, (iii) una corrida basta, (iv) menos
  fuentes es mejor.
- La lectura contraria es igual de compatible con los números: 121 fuentes pueden ser más
  evidencia y 67 puede ser haber parado antes. La propia animación dice que cada trazo
  refleja «the evidence gathered, the results of calculations, and the questions that
  remain unresolved»: hay preguntas sin resolver en el mapa, y no se ven en la tabla.
- Contra el estándar del taller: el repo exige esperado escrito antes, réplica y reserva
  independiente (`memoria`, §4), y su faro dice que **recuperar no es responder**. Contar
  turnos y fuentes cuenta el camino, no el cambio en A(Q). No es comparable con F5/F6
  (llamadas sueltas, 76–127 s, ~74 % de los tokens en razonamiento, sin gold).

### 9.2 Las cifras de la noticia, contra quien las midió después

| Afirmación de la noticia | Quién la midió | Estado hoy |
|---|---|---|
| Índice de Inteligencia de Artificial Analysis **38** | **AA** (independiente) | Publicado: **#64/225**, mediana 26 → por encima de la media, no frontera. La frase «modelo más inteligente fuera de EE. UU. y China» es **geográfica**, no absoluta |
| **Cyber Index 50**; 82 % en reproducir-y-parchear; 93 % en Cybench | AA (índice) / Mistral (82 % y 93 %) | AA: 50, igual que GLM-5.3-Flash y por debajo de MiMo-V2.6-Pro (56). El «casi cero» de los modelos cerrados es en parte **rechazo** de la tarea y la metodología de AA puntúa los rechazos con cero: la cifra mezcla capacidad y política. Además, TNW: Mistral «has not shared figures to back» su ventaja en ciber, y hay una versión **menos restringida** para socios de ciberseguridad: no es el modelo del API público |
| Harvey Legal **15 %** | **Vals** (independiente) | **15,83 % ±2,96, puesto 6/75** → el dato que mejor resiste el cruce, como resultado de **especialista**. La tabla de Harvey tiene arriba a Muse Spark 1.2 con 25,42 % |
| Finance: FinWorkBench/Finch **67 %** | Mistral (su gráfica) | Empata con DeepSeek V4 Pro (67 %) y GLM-5.3 (65 %): es un empate, no una ventaja. En la medición independiente (Vals Finance Agent v2): ML4 **54,68 %**, por detrás de Gemini 4 Argon (65,40 %), Claude Opus 5.5 (58,59 %) y GLM 5.3 (55,84 %) |
| Coding: DeepSWE v1.1 **61,7 %** y «Coding Agent Index **49,8 %**» | AA, citado por Mistral | 49,8 % es la **media aritmética** de 61,7 / 59,4 / **28,3** (comprobado: 149,4/3 = 49,8) → el compuesto esconde el componente flojo. En el tablero vivo de DeepSWE, eligiendo la mejor configuración publicada, GLM-5.3 y Kimi K3 rondan 69 % y los cerrados 74 %; ML4 **no está** en el tablero. En Terminal-Bench 4 medido aparte por **Vals**: ML4 **22,73 % ±0,88** frente a GLM 5.3 38,89 % |
| Vals Index (índice amplio) | **Vals** | **48,05 % ±1,11, puesto 32/44**; coste **$13,78 por test** y latencia **105 min 50 s**. Por debajo de GPT-6.1 Sol (61,15 %), GLM 5.3 (53,51 %), Kimi K3 (50,30 %) y DeepSeek V4.1 Flash (51,32 % a $0,33/test) |
| Visión: Dense200 **42 %** vs Astra 41 %; DIOR-RSVG 73 % | Mistral (su gráfica) | Un punto de diferencia en un test, sin incertidumbre. VentureBeat no encontró las cifras de los competidores en fuentes públicas |

Notas de método de terceros `[D]`: VentureBeat verifica que las cifras de los rivales son
rastreables a fuentes públicas, pero **no reproduce las de ML4**; el tablero vivo de DeepSWE
y el índice público de AA no tenían a ML4 al momento de la nota; la propia noticia dice que
el *reinforcement learning* del preview sigue en marcha y que publicará más resultados antes
de los pesos. Y el preview admite **actualizaciones silenciosas** (§4.9): cualquier número
de hoy describe un modelo que puede cambiar mañana.

### 9.3 Lo que esto resuelve de mis preguntas abiertas

1. **Contexto (fila 3 de §3, pregunta 1 de §6):** mi lectura de la API (524.288) coincide con Vals (512k), AA
   (524k) y Vercel (524k / salida 262k). Solo la ficha de Mistral dice 1M. La evidencia
   pesa del lado de **512K**; la ficha parece desactualizada o referida a otra ruta.
2. **Descuento (fila 5 de §3):** AA lo fecha: «**50 % off for the first two weeks**»; el
   `billing_model_name` dice `launch-discount`. Las dos señales apuntan a que **termina
   hacia el 20-10** y que los independientes midieron con la tarifa sin descuento
   ($1,36/$4,18): por eso Vals y AA listan esas tarifas.
3. **Verbosity (nuevo):** AA mide **200 M tokens de salida** en su índice frente a una
   mediana de 81 M → «very verbose». En bucles de agente eso se paga: el costo por test de
   Vals ($13,78) es 4× el de GPT-6.1 Sol ($3,24) pese a tener tarifas de token más bajas.
4. **Pesos:** HF da **31-10-2026**; TNW dice **27-10**; licencia aún no publicada `[?]`.

### 9.4 Lo que no se puede concluir

No reproduje ningún benchmark: no hay arnés, ni gold escrito antes, ni reserva, ni
autorización de gasto para eso. Lo verificado por mí hoy sigue siendo la forma del API
(§4), no la calidad del modelo. La afirmación del repo —«el spike no concluye»— aplica
entera: estas cifras entran como **afirmaciones de terceros y de la casa**, no como
mediciones nuestras. Cualquier comprobación seria exigiría gold previo y reserva
independiente, y eso lo deciden Frat y Cowork.

## 10. Nota de estado del árbol

Al abrir la sesión, `git status --short` mostraba `?? mvp/paso2/` (sin seguimiento, de las
06:25 de hoy) con `comparacion.py`, `especificacion_comparacion.md`, `prompt_ficha_contexto.md`
y `__pycache__/`. No es mío y no lo toqué: si alguien commitea, que no lo barra por descuido.
HEAD: `6bf6e9d`, rama `main`.
