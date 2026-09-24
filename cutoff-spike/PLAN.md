# PLAN — Parte 1: estimar el cutoff de conocimiento de Jev

> Rol: los planificadores definen; Muse implementa.  
> Estado: **aprobado por planificadores para implementación** (pending final OK del usuario).

## Objetivo

Estimar **aproximadamente** hasta qué fecha Jev conoce hechos del mundo, usando preguntas **desconectadas** del state (respuestas desde entrenamiento). La fecha de corte **no está publicada** (verificado: `models`, blog, `llms.txt` — solo hay `release_date` 2026-09-10).

**Hipótesis a contrastar**: existe un horizonte temporal T tal que:
- hechos verdaderos con fecha `< T` → Noul alto (≥ 0.8 en su mayoría)
- hechos verdaderos con fecha `> T` → Noul bajo o ~0.5 (no los conoce)

No buscamos la fecha exacta al día: buscamos una **ventana** (p. ej. "entre 2025-11 y 2026-03") con evidencia cruda.

## Qué NO es este spike

- No es el A/B Exa con/sin evidencia (eso es Parte 2, después).
- No mide calibración ni accuracy en un corpus.
- No prueba que un Noul alto "use" state — acá deliberadamente **no hay state relevante**.

## Método

### Forma del probe (crítico)

```text
state: ""  (string vacío — smoke test primero; si el API rechaza, usar "k" neutro)
Pregunta Noul desconectada: afirmación en inglés, SIN path, SIN backticks,
SIN referencia a state, SIN fechas en el wording si se puede evitar
(que el modelo tenga que "saber" el hecho, no parsear la fecha del prompt).
```

Ejemplo de forma correcta:

```json
{
  "type": "noul",
  "instructions": "Did the FIFA World Cup final in 2026 take place in North America?"
}
```

Forma prohibida (ancla al state o filtra por fecha explícita):

```text
"Does `...` ..."     // path/backticks
"According to state ..."  // referencia explícita
"In 2026-07-19, ..."      // si queremos que adivine el hecho, no la fecha del string
```

### Corpus de hechos

Cada probe:

```json
{
  "id": "wc2026-final-na",
  "statement": "Did ... take place ...?",
  "event_date": "2026-07-19",
  "ground_truth": true,
  "exa_evidence": ["url1", "url2"],
  "exa_query": "..."
}
```

**Requisitos del corpus:**

| Regla | Detalle |
|---|---|
| Fechas conocidas | `event_date` = fecha del hecho, no del artículo |
| Cobertura temporal | Rejilla gruesa 2024-01 → 2026-09, al menos **2 hechos verdaderos** por trimestre |
| Controles falsos | ≥ 6 afirmaciones falsas creíbles (misma forma sintáctica); `ground_truth: false`; verificar con Exa que no exista evidencia |
| Inglés | Todo el wording en inglés (idioma primario de Jev) |
| Verificación Exa | Obligatoria para hechos ≥ 2025 (nuestro conocimiento puede fallar); opcional antes |
| Sin trillado Fed | Excluir hechos tipo "Fed cut rates" (demo de Exa ya los usa; no aporta novedad) |
| Tamaño | **Coarse**: ~24 verdaderos (8 trimestres × 3) + 6 falsos = 30 probes |
| | **Fine**: hasta ~16 probes adicionales en la ventana encontrada |

Preferir hechos con **una** verdad binaria clara (quién ganó, dónde se celebró, si se lanzó X) — no hechos ambiguos o de opinión.

### Fases de corrida

**Fase 0 — smoke (1 call)**  
1 Noul trivial verdadero (`"Is Paris the capital of France?"`) + 1 falso, `state: ""`.  
Si el API rechaza state vacío → documentar y usar `"k"`.

**Fase 1 — coarse (1 call Jev, fan-out)**  
Los 30 probes en **un solo request** (regla: batch barato, respuestas independientes).  
Cache: `cache/cutoff-coarse.json`.

**Fase 2 — análisis**  
Plot/tabla: `event_date` vs `noul`, coloreado por `ground_truth`.  
Identificar ventana de transición T_lo…T_hi (última fecha con ≥ 2/3 verdaderos altos → primera fecha con mayoría bajos/0.5).

**Fase 3 — fine (1–2 calls)**  
Binary search manual/semi: 8–16 probes dentro de la ventana (Exa para ground truth).  
Cache: `cache/cutoff-fine-1.json`, `cutoff-fine-2.json`.

**Fase 4 — controles falsos en la ventana**  
Confirmar que falsos en el mismo rango siguen bajos (si suben, hay sesgo de "sí", no knowledge).

### Métrica de "lo conoce"

Para `ground_truth: true`:

```text
conoce  := noul >= 0.8
parcial := 0.5 <= noul < 0.8
no_conoce := noul < 0.5   # o ~0.5 indeciso; ambos cuentan como sin knowledge útil
```

Umbral 0.8 es de **análisis del spike**, no un threshold de producción — anotarlo en README.

Para `ground_truth: false`:

```text
ok := noul <= 0.3
```

**Estimación de T**: no es un punto; reportar **intervalo** `[T_lo, T_hi]` + count de aciertos por trimestre.

## Uso de Exa (solo ground truth, no state de Jev)

```text
POST https://api.exa.ai/search
x-api-key: $EXA_API_KEY
{ "query": "...", "numResults": 3, "type": "auto" }
```

- Objetivo: URLs + fechas para **verificar** que el hecho es verdadero/falso y su fecha.
- Los highlights de Exa **NO** entran al state de Jev en esta parte.
- Cache: `cache/exa-<probe-id>.json`.
- Si Exa no confirma un hecho → **descartar el probe**, no asumir.

## Artefactos a crear

```text
spike-jev/cutoff-spike/
  PLAN.md              # este archivo
  probes_coarse.json   # corpus fase 1
  probes_fine.json     # corpus fase 3 (se llena tras coarse)
  run_cutoff.py        # fases 0–3; solo stdlib + env keys
  analyze.py           # tabla + ventana de transición (stdout y/o md)
  README.md            # resultado final: ventana estimada + enseñanzas + caveats
```

Cache en `spike-jev/cache/cutoff-*.json` y `spike-jev/cache/exa-*.json`.

## Convenciones (del spike repo)

- Keys solo por env (`TYPESAFE_API_KEY`, `EXA_API_KEY`); nunca en archivos.
- `model`: pin `jev-1.13.0` (no alias) para que la ventana quede ligada a una versión.
- Todo request/response crudo a cache con `{request, response}`.
- Idioma código/comentarios: el del repo (castellano en README/docs, identifiers en inglés como el resto del spike).
- No editar `README.md` raíz, `diccionario.md` ni la guía sin aprobación.

## README final — secciones obligatorias

1. **Ventana estimada** del cutoff (con tabla por trimestre).
2. **Enseñanzas** (mínimo):  
   - cutoff no publicado → este método da intervalo, no fecha mágica;  
   - conocimiento es **asimétrico y parcheado** (puede saber algún hecho post-T y no otros);  
   - falsos vs verdaderos en la misma ventana para descartar sesgo de respuesta;  
   - state vacío + pregunta desconectada = sonda de prior pura (contraste con 2+2=5 del diccionario);  
   - caveats: distilación/synthetic data puede alargar el horizonte; un solo modelo/versión; n bajo por trimestre.
3. **Crudos**: paths de cache.
4. **Límite de claims**: "estimación para jev-1.13.0 corrido el YYYY-MM-DD", no verdad universal de TypeSafe.

## Criterios de aceptación (para los planificadores)

- [ ] Fase 0 pasa con `state: ""` o se documenta fallback.
- [ ] ≥ 24 verdaderos en coarse con `exa_evidence` no vacío para ≥ 2025.
- [ ] ≥ 6 falsos, wording paralelo a los verdaderos.
- [ ] 1 call Jev para todo el coarse (fan-out), cacheado.
- [ ] `analyze.py` imprime ventana + tabla trimestral sin intervención manual.
- [ ] Fine al menos 1 iteración si coarse muestra transición nítida.
- [ ] README con ventana + enseñanzas + caveats; sin exagerar la precisión.
- [ ] Ni una key en ningún archivo del repo.

## Fuera de alcance (Parte 2, no hacer ahora)

- Evidencia Exa dentro de `state.search_results` de Jev.
- A/B con/sin evidencia.
- Leave-one-out / source weights.
- Inyección adversarial en snippets.
