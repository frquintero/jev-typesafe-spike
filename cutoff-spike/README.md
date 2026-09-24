# Cutoff de conocimiento de Jev — hallazgos Fase 1–2 (borrador)

Estimación del horizonte temporal de `jev-1.13.0` con sondas de prior
puras. Estado: coarse corrido y analizado; fine propuesto, **sin correr**.

## 1. Método

Sonda de prior pura: `state: ""` + pregunta Noul **desconectada**
(afirmación de mundo autocontenida, sin path, sin backticks, sin
referencia al state). Sin nada que juzgar en el state, Jev solo puede
responder desde entrenamiento.

Contraste con el 2+2=5 del diccionario: allá el state contenía
`"2+2=5"` pero la pregunta desconectada (`"Is 2+2=5?"`) dio 0.01 —
juzgó de entrenamiento aunque el texto coincidiera. Acá se usa esa
misma propiedad como instrumento: cada Noul mide si el hecho vive en
el prior del modelo.

Fase 0 (smoke, 1 call, 2 Nouls): Paris 0.99 / Berlín 0.01, `state: ""`
aceptado sin fallback. Fase 1 (coarse, 1 call, 33 Nouls en fan-out):
33/33 answers, modelo efectivo `jev-1.13.0`.

Umbrales de análisis (del PLAN, no de producción): verdaderos
conoce ≥ 0.8 / parcial 0.5–0.8 / no < 0.5; falsos ok ≤ 0.3.

## 2. Resultado por capa (nunca promediar)

El corpus mezcla dos clases de hechos (`fact_type` en cada probe):

- **outcome**: la respuesta solo existe después del hecho (quién ganó,
  qué se lanzó, qué ocurrió). Acá sí se estima un cutoff temporal.
- **scheduled**: sabible antes del hecho (sedes, EOL, calendarios,
  astronomía). Control: Jev puede saberla aunque el evento sea
  posterior a su corte.

### Capa outcome — la importante (17 verdaderos)

```text
trim      n conoce parcial  no
2024Q1    2      2       0   0
2024Q3    2      0       2   0
2024Q4    3      1       1   1
2025Q1    2      0       2   0
2025Q2    3      0       0   3
2025Q3    3      0       0   3
2025Q4    1      0       0   1
2026Q3    1      0       0   1
```

Ventana candidata: **[2024-02-11, 2025-04-13]** =
[última fecha del último trimestre outcome con ≥ 2/3 conoce,
primera fecha del primer trimestre con ≥ 2/3 no].
Lectura: conoce sólido hasta 2024Q1, zona parcial 2024Q3–2025Q1,
no-conoce desde 2025Q2. El fine densifica esta ventana.

Decisión documentada: la regla ≥ 2/3 se agrega **por trimestre**
(la rejilla del corpus), no por fecha suelta — con n=1 por fecha la
fracción degenera y un probe ruidoso invierte la ventana
(`trump-wins` conoce 2024-11-05 vs `btc-100k` no 2024-12-05).

### Capa scheduled — control (10 verdaderos)

```text
trim      n conoce parcial  no
2024Q1    1      1       0   0
2024Q2    3      2       1   0
2024Q3    1      1       0   0
2025Q1    1      0       1   0
2025Q4    2      0       2   0
2026Q1    1      0       1   0
2026Q2    1      0       1   0
```

Ningún trimestre scheduled llega a ≥ 2/3 "no" (piso ≈ 0.5–0.8 aun
en 2026: `cop30` 0.79, `milano-cortina` 0.66, `wc2026-opener` 0.56).
No hay ventana de corte para scheduled — es lo esperado si el
conocimiento es pre-anunciado, y confirma que mezclar capas
contamina la estimación.

## v2 sin sesgo de wording e IDs

Re-corrida del mismo corpus con dos fugas cerradas: fechas libres
fuera del `statement` (salvo nombre propio de edición: `Euro 2024`,
`Super Bowl LVIII`) y fechas fuera de los IDs (claves del request).
Mapeo al cable: `id` → clave de `questions`, `statement` →
`instructions`; el id nunca se pega en instructions. 1 call, 33
answers, `state: ""`, modelo `jev-1.13.0`; validado 0 mismatches
instruction↔statement y 0 keys con dígitos de año.
Crudo: `spike-jev/cache/cutoff-coarse-v2.json`. Corpus:
`spike-jev/cutoff-spike/probes_coarse_v2.json` (`ref_v1` empareja).

*Corrección 2026-09-22*: según `api.md`, la clave de cada pregunta no
se envía al modelo ni participa en la inferencia. Quitar fechas de los
IDs no pudo cambiar nada; los Δ v1→v2 vienen solo del `statement` (y
de la variación entre corridas). Además, quitar la fecha convierte la
pregunta en otra: se evalúa desde el «ahora» implícito del modelo.

### Ventana v2 (solo outcomes-true)

```text
trim      n conoce parcial  no
2024Q1    2      2       0   0
2024Q3    2      1       1   0
2024Q4    3      0       1   2
2025Q1    2      0       2   0
2025Q2    3      0       2   1
2025Q3    3      0       0   3
2025Q4    1      0       0   1
2026Q3    1      0       0   1
```

Ventana: **[2024-02-11, 2024-10-13]** (v1: [2024-02-11, 2025-04-13]).
T_hi se adelanta dos trimestres: 2024Q4 pasa a 2/3 "no" porque
`trump-defeats-harris` cae a 0.49. T_lo no se mueve (2024Q1 2/2).

### Comparación v1 → v2

7/33 probes con |Δ| ≥ 0.15 (`analyze.py delta`):

```text
trump-wins-2024      0.86 -> 0.49  (-0.37)  outcome
win10-eol-2025       0.65 -> 0.33  (-0.32)  scheduled
masters-mcilroy-2025 0.31 -> 0.59  (+0.28)  outcome
iphone17-2025        0.45 -> 0.17  (-0.28)  outcome
who-pandemic-2025    0.42 -> 0.69  (+0.27)  outcome
btc-halving-2024     0.94 -> 0.73  (-0.21)  scheduled
eclipse-na-2024      0.53 -> 0.73  (+0.20)  scheduled
```

Los otros 26 mueven ≤ 0.14 (mediana de |Δ| sobre 33: 0.03). El wording con fecha
no sesgaba parejo: quitado, algunos hechos suben y otros bajan —
pesa más la identificación del hecho (nombres rivales, alcance)
que la fecha como hint. Scheduled sigue sin trimestre ≥ 2/3 "no".

Falsos v2: rompe solo `f-sinner-wimbledon` (0.45, peor que 0.39 en
v1); los otros 5 en ok. Ver FLAGS.

### FLAGS (wording que conserva fecha a propósito)

- `lunar-eclipse-total`: "…in March 2025" — no unívoca sin ancla
  temporal (hay varios eclipses totales).
- `f-vision-pro-year`, `f-eclipse-3-country-fake`, `f-gpt5-fake`:
  el año (2019/2023) ES la proposición falsa; quitarlo rompería el
  control.
- `f-sinner-wimbledon`: control flojo conocido (año vecino del
  verdadero); sube 0.39 → 0.45 sin la fecha en el ID.

## 3. Controles falsos

5/6 falsos en ok (≤ 0.3): `f-vision-pro-2019` 0.01, `f-gpt5-2023`
0.02, `f-tokyo-2024` 0.03, `f-sb-lviii-eagles` 0.16,
`f-eclipse-na-2023` 0.23.

El que rompe: **`f-sinner-wim-2024` = 0.39** ("Did Jannik Sinner win
Wimbledon in 2024?" — ganó Alcaraz). Es un **mal control**: mismo
deportista + año vecino del hecho verdadero (Sinner sí ganó
Wimbledon 2025). El 0.39 mide confusión de año, no sesgo de "sí".
Los falsos del fine evitan este estilo: actor incorrecto en evento
conocido (`f-damascus-israel`, `f-euro-england`) o evento
inexistente con forma idéntica (`f-blueghost-crew`), más veredicto
invertido (`f-trump-acquitted`).

Corrección anotada: el reporte de Fase 1 dijo "todos los falsos
≤ 0.3" de una mirada; el dato era 0.39. Desde ahora los resúmenes
se calculan de los datos (`analyze.py` lista rompedores).

## 4. Caveats

- Cutoff **no publicado** por TypeSafe: esto estima un intervalo por
  comportamiento, no una fecha oficial.
- Conocimiento **parcheado y asimétrico**: dentro de la ventana hay
  parciales dispersos (0.5–0.8), no un escalón nítido.
- **Anomalías de dominio**: los 2 eclipses scheduled puntúan flojo
  (`eclipse-na-2024` 0.53, `lunar-eclipse-2025-03` 0.50) aunque la
  fecha no debería importar; `btc-100k-2024` (outcome, 2024-12-05)
  da 0.43 rodeado de conocimiento — posible efecto número/wording
  (Jev no calcula; guía §6), no temporal.
- **Fechas en el wording del coarse** ("in April 2024", "in 2019"):
  permiten adivinar por fecha en vez de saber el hecho. El fine lo
  corrige (sin año/fecha salvo nombre del evento).
- **n bajo por trimestre** (1–3 outcomes): la ventana es gruesa; el
  fine la angosta.
- Distilación/synthetic data puede alargar el horizonte más allá del
  corte nominal de entrenamiento.
- Un solo modelo (`jev-1.13.0`), una sola corrida por probe (los
  números respiran entre corridas; regla 16).

Clasificaciones `fact_type` en el borde (revisables): `vision-pro`
y `paris-olympics-open` → scheduled (fecha/formato anunciados antes
de event_date); `btc-halving` → scheduled (bloque conocido, fecha
proyectada); `iphone17` y `who-pandemic` → outcome (nombre/voto
solo existen después).

## 5. Crudos y artefactos

- `spike-jev/cache/cutoff-smoke.json` — Fase 0 (request+response).
- `spike-jev/cache/cutoff-coarse.json` — Fase 1, 33 answers
  (request+response, 1044 in / 803 out tokens).
- `spike-jev/cache/exa-<id>.json` — 16 crudos Exa del fine
  (request+response). Tres se re-queraron con query más afilada y el
  crudo guarda el query final: `la-fires-2025`, `tariffs-liberation`,
  `f-blueghost-crew`. Además `la-fires-2025` se re-redactó al claim
  confirmado ("Palisades and Eaton … major damage", sin cuantificar
  viviendas).
- `spike-jev/cutoff-spike/probes_coarse.json` — 33 probes + fact_type.
- `spike-jev/cutoff-spike/probes_fine.json` — propuesta (12+4),
  **no corrida**.
- `spike-jev/cutoff-spike/run_cutoff.py` — Fases 0–1 (sin tocar
  desde su corrida).
- `spike-jev/cutoff-spike/analyze.py` — este análisis, stdout.

Cero calls Jev nuevas en Fase 2. Cero keys en el repo.

## 6. Límite de claims

Estimación gruesa para **jev-1.13.0 corrido el 2026-09-22**: ventana
outcome [2024-02-11, 2025-04-13], scheduled sin corte (control).
No es una verdad universal de TypeSafe ni aplica a otras versiones.

*Corrección 2026-09-22*: la ventana citada arriba es la de v1; la de v2
es [2024-02-11, 2024-10-13]. Más importante: ninguna de las dos estima
un cutoff. Un Noul bajo significa «probablemente no», no «no sé»: puede
venir de desconocimiento, de conocimiento antiguo (el PSG «nunca había
ganado»), de la tasa base del desenlace o de la semántica temporal de
la pregunta. Una v2 debe usar pares verdadero/contrafáctico del mismo
evento, Choice con opción «no ha ocurrido / no sé», clases separadas,
controles y réplicas. Ver guía §6.
