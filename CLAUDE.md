# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Qué es este repo

Spike de investigación (separado del piloto EEL, que no se toca) que evalúa
si el modelo de decisiones **Jev** de TypeSafe (`api.typesafe.ai`) puede
reemplazar al pipeline GLM actual para tareas de detección de estructura.
Jev nunca genera texto: sopesa juicios angostos (`Noul`/`Choice`/`Score`) y
devuelve un grado de soporte 0–1; el código decide y renderiza. No hay
build system, package manager ni tests automatizados — son scripts Python
de un solo archivo, ejecutados a mano contra la API real.

**Estado actual:** el objetivo EEL está suspendido. El trabajo activo es
`niveles/` (extracción de datos con un LLM; Jev como auditor). Ver
«Estado actual» en el README y `memoria de trabajo y pendientes.md`.

**Antes de escribir o interpretar cualquier probe, lee `README.md`** (reglas
1–26, "Principios y reglas acordadas") y `diccionario.md`. Ahí está el
vocabulario correcto y los límites de lo que se le puede pedir a Jev — no
se opinan, se verifican contra `docs.typesafe.ai/api.md`.

## Rol y reglas de ejecución

**Frat y Cowork planean; el ejecutor corre** (Claude Code en la nube, o
Cowork en la máquina local con `proxy_local.py`). El rol va con la tarea,
no con el modelo: un mismo modelo puede planear, implementar, probar o ser
el LLM dentro del arnés (hoy DeepSeek, en `niveles/`). Quien ejecuta no
decide diseño de juicios, prompts, umbrales, ni si el spike adopta o descarta Jev —
corre lo que el plan indica, informa con números y deja la decisión a Frat.
Reglas del spike que aplican directamente a cómo correr y reportar:

- **Regla 15 — el spike no concluye.** No cerrar con un veredicto
  ("Jev sirve/no sirve"); juntar evidencia, informar con números, y que
  decida la auditoría con Frat.
- **Regla 22 — reportar antes de inventar.** Prompts y campos enviados se
  citan tal cual (verbatim), nunca resumidos ni parafraseados.
- **Regla 20 — solo documentos sintéticos.** Nunca meter texto real/privado
  en `state`, aunque TypeSafe no lo almacene.
- **Regla 16 — réplicas.** Las baterías corren 2–3 réplicas (`r1`/`r2`/`r3`)
  para medir estabilidad; los números "respiran" entre corridas (±0.01–0.02
  típico con juicios fijados) y eso no es un bug.
- **Regla 26 — caja negra.** No inventar mecanismos para explicar un grado
  concreto ("dio 0.56 porque..."); se documentan patrones y márgenes
  heurísticos, no causas internas del modelo.
- **Mostrar siempre el crudo junto al resultado**: cada afirmación sobre un
  grado va acompañada del JSON `{"request": ..., "response": ...}` que la
  respalda, no solo el número.
- **No cambiar juicios ni agregar campos/claves que no estén en el plan**
  sin decirlo explícitamente — si hace falta un ajuste de wording, se
  reporta como cambio, no se desliza en silencio.
- **Nombrado de crudos**: `cache/<probe>-r<N>.json` para réplicas
  (`cache/<probe>-r1.json`, `-r2.json`, `-r3.json`); un solo archivo
  `cache/<probe>.json` cuando no hay réplicas.
  En `niveles/`, el nombre lo fija cada script en `niveles/cache/`.
- **Al terminar una corrida**, hacer commit y push de los archivos nuevos/
  modificados en `cache/` (y del script si cambió) a la rama de trabajo,
  para que Frat los baje con `git pull` y se analicen juntos.

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

# niveles/: cada ronda se corre según su sección en niveles/PLAN.md
python3 niveles/extraer_datos.py <doc> <modelo> <prompt> <rN>
python3 niveles/run_niveles.py <doc> <modelo> <prompt_A|toulmin_vN> <prompt_B|-> <rN>
python3 niveles/jev_sopesa.py <crudo_llm.json>
```

No existe un runner único ni una suite de tests: cada archivo en `probes/`
es autocontenido y se corre solo.

## Credenciales y red

`TYPESAFE_API_KEY` **nunca** vive en el repo ni como variable de entorno
plana. En los entornos cloud de Claude Code se configura como **credencial
de API** (tipo Bearer, dominio permitido `api.typesafe.ai`) — el proxy de
red inyecta el header `Authorization: Bearer …` en cada request hacia ese
dominio; el código no debe construir ese header ni leer
`os.environ["TYPESAFE_API_KEY"]` (se quitó de todos los probes por eso
mismo — ver commit `6b1562f`). Si un script nuevo necesita llamar a la API,
sigue el mismo patrón: solo `Content-Type` y `User-Agent` en los headers,
nunca `Authorization`.

Lo mismo vale para Z.ai (`api.z.ai`) y DeepSeek (`api.deepseek.com`),
usados en `niveles/`. En local, `proxy_local.py` hace el papel del proxy de
la nube (instrucciones en el README).

## Arquitectura del protocolo Jev

Cada request a `POST https://api.typesafe.ai/v1/systemone` tiene esta forma
fija (campos del protocolo, no renombrables — regla 3 del README):

```python
body = {
    "model": "jev-1.13.0",   # fijo en corridas nuevas (ver nota de versión abajo)
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

**Versión del modelo — decisión vigente:** las corridas nuevas fijan
`"model": "jev-1.13.0"` (no `jev-latest`), para que los crudos queden
ligados a una versión conocida y no se mezclen sin aviso con los de una
versión futura. Algunos probes existentes todavía usan `jev-latest` (son
anteriores a esta decisión); no hace falta re-correrlos solo por eso. En
todo caso, comparar `usage.model` (el modelo efectivo que devuelve la
respuesta) contra lo esperado y **avisar explícitamente** si no coincide
— por ejemplo si TypeSafe retira `jev-1.13.0` y el pin ya no resuelve.

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

`cutoff-spike/PLAN.md` deja explícita esta convención para sus propios
documentos ("No editar `README.md` raíz, `diccionario.md` ni la guía sin
aprobación"); se extiende aquí a los documentos vivos del spike,
todos "nuestros" (de Frat):

- `README.md` (raíz): contexto, reglas acordadas, evidencia histórica.
  **No editar sin aprobación.**
- `diccionario.md`: vocabulario y ejemplos canónicos de Jev. **No editar
  sin aprobación.**
- `jev_typesafe_guia_pedagogica_v2.md`: guía pedagógica de referencia
  (bandas, límites de lectura literal, Anexos A–C) — es la versión
  vigente. **No editar sin aprobación.**
- `memoria de trabajo y pendientes.md`: fuente única del estado del
  trabajo (forma de trabajo, lecciones, pendientes).
- En `deleted/`: los snapshots `*.antes-v*.md` y el resumen retirado
  `jev_resumen_pedagogico.md` — no se editan ni se usan como fuente.
- Las secciones fechadas del README ("Evidencia reunida", "Plan de
  pruebas") son registro histórico: conservan el vocabulario de su
  momento («pregunta», «respuesta») aunque el marco vigente use otro
  («juicio», «grado de soporte»).
