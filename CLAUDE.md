# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repo

Spike de investigación (rama `spike-jev`, no se toca el piloto EEL) que evalúa
si el modelo de decisiones **Jev** de TypeSafe (`api.typesafe.ai`) puede
reemplazar al pipeline GLM actual para tareas de detección de estructura.
Jev nunca genera texto: sopesa juicios angostos (`Noul`/`Choice`/`Score`) y
devuelve un grado de soporte 0–1; el código decide y renderiza. No hay
build system, package manager ni tests automatizados — son scripts Python
de un solo archivo, ejecutados a mano contra la API real.

**Antes de escribir o interpretar cualquier probe, lee `README.md`** (reglas
1–26, "Principios y reglas acordadas") y `diccionario.md`. Ahí está el
vocabulario correcto y los límites de lo que se le puede pedir a Jev — no
se opinan, se verifican contra `docs.typesafe.ai/api.md`.

## Comandos

No hay lint/build/test config (no `package.json`, `pyproject.toml`,
`Makefile`). Los "comandos" son invocar cada script directamente:

```bash
# Probe de una sola corrida (la mayoría de probes/*.py)
python3 probes/strawberry.py

# Probes con subcomandos run/analyze (baterías grandes, cachean y son idempotentes)
python3 probes/noul_fuerza.py run        # corre lo que falte, salta crudos existentes
python3 probes/noul_fuerza.py analyze    # tablas y hallazgos a stdout, sin llamar a la API
python3 probes/score_prueba1.py run
python3 probes/score_prueba1.py analyze

# Sub-spike cutoff-spike/ (subcomandos por fase)
python3 cutoff-spike/run_cutoff.py smoke|coarse|coarse2|all
python3 cutoff-spike/analyze.py v1|v2|delta|all

# Verificar sintaxis tras editar varios probes a la vez
python3 -m py_compile probes/*.py
```

No existe un runner único ni una suite de tests: cada archivo en `probes/`
es autocontenido y se corre solo.

## Credenciales y red (entorno cloud)

`TYPESAFE_API_KEY` **nunca** vive en el repo ni como variable de entorno
plana. En los entornos cloud de Claude Code se configura como **credencial
de API** (tipo Bearer, dominio permitido `api.typesafe.ai`) — el proxy de
red inyecta el header `Authorization: Bearer …` en cada request hacia ese
dominio; el código no debe construir ese header ni leer
`os.environ["TYPESAFE_API_KEY"]` (se quitó de todos los probes por eso
mismo — ver commit `6b1562f`). Si un script nuevo necesita llamar a la API,
sigue el mismo patrón: solo `Content-Type` y `User-Agent` en los headers,
nunca `Authorization`.

## Arquitectura del protocolo Jev

Cada request a `POST https://api.typesafe.ai/v1/systemone` tiene esta forma
fija (campos del protocolo, no renombrables — regla 3 del README):

```python
body = {
    "model": "jev-latest",   # o versión fija p.ej. "jev-1.13.0" para reproducibilidad
    "state": ...,            # el "expediente": lo que se somete a juicio (string, dict o array)
    "questions": {
        "id_neutro": {
            "type": "noul" | "choice" | "score",
            "instructions": "...",   # el juicio (Noul), o el marco que agrupa criteria (Choice/Score)
            "criteria": {...} | [...],  # solo Choice/Score: juicios alternativos (sin orden) o niveles (ordenados)
        },
    },
}
```

- **Noul**: un solo juicio en `instructions` → un grado 0–1, leído por
  bandas (>0.85 muy seguramente cierto … <0.20 muy seguramente falso; la
  franja 0.30–0.65 es señal de diseño, no incertidumbre de Jev).
- **Choice**: juicios alternativos sin orden en `criteria` → Jev reparte
  soporte; siempre debe incluir una opción de salida explícita.
- **Score**: juicios como niveles ordenados en `criteria` → el `score` es
  la posición media del soporte repartido.
- Varias preguntas en un mismo `questions` se resuelven en **fan-out**
  paralelo dentro de una sola llamada (no cambia el resultado vs. llamadas
  separadas, solo la latencia — regla 25).
- Los IDs de `questions` viajan pero el modelo no los ve ni los usa para
  inferir — son solo para casar resultados en código; aun así se usan
  claves neutras (`q1`, `n01`) para no filtrar pistas.
- Sin SDK en runtime: todo con `urllib.request` + dicts planos (el SDK
  0.7.0 instalado queda solo como referencia de tipos — regla 6).
- Sin `temperature`: la estabilidad se mide re-corriendo, no fijando un
  parámetro.

## Convención de cada script en `probes/`

Casi todos siguen el mismo esqueleto: build del `body`, `urllib.request.Request`
al endpoint, escritura de `{"request": body, "response": resp}` a
`cache/<nombre-descriptivo>.json`, y print a stdout de lo enviado/recibido.
Los que hacen baterías grandes (`noul_fuerza.py`, `score_prueba1.py`,
`objeto_juicio.py`, `material_falso.py`, `nombrar_material.py`,
`instructions_vacio.py`) exponen `run` (idempotente: si el crudo ya existe
en `cache/`, no vuelve a llamar) y `analyze` (solo lee `cache/`, nunca
llama a la API) vía `main(argv)`.

`cache/` está commiteado (no gitignored): es el registro de evidencia del
spike, no un artefacto descartable — un re-run no debe volver a pagar/llamar
si el crudo ya existe.

## `cutoff-spike/`

Sub-spike aparte, con su propio `PLAN.md`/`README.md`: estima por
comportamiento (no está publicada) la ventana de corte de conocimiento de
`jev-1.13.0`, con sondas de prior puro (`state: ""` + pregunta Noul
desconectada del state). `run_cutoff.py` corre las fases contra la API;
`analyze.py` solo lee los crudos cacheados y nunca llama a la API. No
editar `probes_coarse*.json`/`probes_fine.json` sin releer el método del
`PLAN.md` (reglas de wording: sin fechas evitables, sin pistas en los IDs).

## Documentación viva — cuál manda

- `README.md` (raíz): contexto, reglas acordadas, evidencia histórica.
  **No editar sin aprobación** (regla del propio spike).
- `diccionario.md`: vocabulario y ejemplos canónicos de Jev. **No editar
  sin aprobación.**
- `jev_typesafe_guia_pedagogica_v2.md`: guía pedagógica de referencia
  (bandas, límites de lectura literal, Anexos A–C) — es la versión vigente;
  los archivos `*.antes-v*.md` junto a cada uno de estos tres documentos
  son snapshots históricos de antes de cada revisión, no se editan ni se
  usan como fuente.
- Las secciones fechadas del README ("Evidencia reunida", "Plan de
  pruebas") son registro histórico: conservan el vocabulario de su
  momento («pregunta», «respuesta») aunque el marco vigente use otro
  («juicio», «grado de soporte»).
