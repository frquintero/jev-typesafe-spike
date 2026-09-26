# MUSE.md — anotaciones operativas para Muse Code

Soy Muse Code (powered by Meta Muse Spark). Frat y Cowork planean; yo ejecuto:
corro lo que el plan indica, informo con números y crudos, no decido diseño,
umbrales ni veredictos. El spike no concluye. (`cutoff-spike/PLAN.md` ya me
asigna ese rol: «los planificadores definen; Muse implementa».)

## Arranque de cada sesión (en este orden)

1. `git status --short` + `git log --oneline -5` + `git branch --show-current`
   (rama de trabajo: `main`; el piloto EEL no se toca).
2. Leer `README.md` → sección «Estado actual» (puede cambiar: el objetivo EEL
   está **suspendido**, lo activo es `niveles/`).
3. Leer `memoria de trabajo y pendientes.md` → §8 pendientes y estado D1–D10.
   Es la fuente única del estado: no duplicarlo en ningún otro archivo.
4. Leer la sección de la ronda indicada en `niveles/PLAN.md` (o
   `cutoff-spike/PLAN.md` si toca ese sub-spike).
5. `diccionario.md` + `jev_typesafe_guia_pedagogica_v2.md` son el vocabulario
   vigente (juicio/expediente/grado, bandas, fan-out). Ya leídos una vez; solo
   releer si la ronda cita una sección concreta.

## Mapa del repo

- `probes/` + `cache/`: spike Jev original (scripts autocontenidos, casi todos
  con `run` idempotente / `analyze` sin API). `cache/` está commiteado.
- `niveles/`: hilo activo. `run_niveles.py` (`call_model`, streaming),
  `extraer_datos.py` (solo orquesta, sin verificaciones),
  `jev_sopesa.py` (builds Jev v1–v6 más v5b, etapa Toulmin, sin uso actual),
  `docs/doc1–5.md` (sintéticos), `prompts/` (se leen de archivo, `str.replace`
  para `{{TEXTO}}`, nunca `str.format`), `cache/` (crudos
  `datos-<doc>-<modelo>-<prompt>-<rN>.json` y `niveles-...`).
- `cutoff-spike/`: `run_cutoff.py smoke|coarse|coarse2|all`,
  `analyze.py v1|v2|delta|all`. No editar sus JSON de sondas sin releer su PLAN.
- `proxy_local.py`: inyecta `Authorization` según host (solo local).
- `deleted/`: snapshots históricos `*.antes-v*` del README, el diccionario y
  la guía, más el resumen retirado (`jev_resumen_pedagogico.md`). No es
  material de trabajo ni fuente vigente.
- Documentos vivos (no editar sin aprobación): `README.md`, `diccionario.md`,
  `jev_typesafe_guia_pedagogica_v2.md`.

## Red y claves (regla dura)

- El código del repo **nunca** arma `Authorization` ni lee `*_API_KEY`.
  Solo `Content-Type` + `User-Agent: spike-jev/1.0`.
- Claves: `TYPESAFE_API_KEY` (api.typesafe.ai), `ZAI_API_KEY` (api.z.ai),
  `DEEPSEEK_API_KEY` (api.deepseek.com). Viven en `~/.bashrc` (local) o las
  inyecta el proxy (nube).
- Verificar presencia sin imprimir valores:
  `bash -ic 'for v in TYPESAFE_API_KEY ZAI_API_KEY DEEPSEEK_API_KEY; do
  [ -n "${!v}" ] && echo "$v: SET" || echo "$v: MISSING"; done'`
- Local (máquina de Frat), dos terminales:
  `~/.venvs/mitmproxy/bin/mitmdump -q --listen-host 127.0.0.1 -p 8080
  -s proxy_local.py` (con `bash -ic` si el shell no carga `~/.bashrc`);
  `export HTTPS_PROXY=http://127.0.0.1:8080
  SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem`.
- **Medido 2026-09-26**: el proxy del sandbox NO inyecta (sin Auth: 403
  TypeSafe, 401 Z.ai/DeepSeek). Si una llamada falla por autenticación,
  **detenerse y reportar** (`niveles/PLAN.md`); no buscar la clave por otros
  medios.
- Modelos: Jev pin `jev-1.13.0` y avisar si `usage.model` difiere;
  `deepseek` = `deepseek-flash` (+thinking, reasoning_effort low);
  `flash` = `glm-5.3-flash`. Medido: DeepSeek sirvió `deepseek-flash`
  cuando se pidió `deepseek-chat`; Z.ai tarda ~50 s aun en llamadas mínimas.

## Comandos

- `python3 probes/<x>.py` · `python3 probes/<bateria>.py run|analyze`
- `python3 niveles/extraer_datos.py <doc> <modelo> <prompt> <rN>`
- `python3 niveles/run_niveles.py <doc> <modelo> <prompt_A> <prompt_B> <rN>`
  (`-` en prompt_B = llamada única Toulmin)
- `python3 -m py_compile` tras tocar código (no hay tests/lint).
- Nombrado crudos réplica: `cache/<probe>-r<N>.json`.
- Al terminar una corrida, commit y push de `cache/` (y del script si cambió)
  a la rama de trabajo: lo pide el mensaje de cada ronda y coincide con
  `CLAUDE.md` (que no se tocó).

## Reportes

- Prompts y campos enviados, verbatim (regla 22). Cada grado con su JSON
  `{request, response}` al lado. Réplicas r1/r2/r3 respiran ±0.01–0.02: normal.
- Sin mecanismos inventados para grados concretos (regla 26); sin veredicto
  (regla 15); solo documentos sintéticos en `state` (regla 20).

## Lecciones de latencia (sesión 2026-09-26, 5:28 medidos)

- El costo dominante soy yo (pasos secuenciales con deliberación larga),
  no la API — salvo GLM/DeepSeek con razonamiento (minutos por llamada).
- Pasos grandes y en paralelo; no re-verificar lo que la salida ya mostró;
  no probar Z.ai salvo que la ronda lo pida.
- `pgrep -af` vuelca el entorno del sandbox (KB de basura): usar `pgrep -x`
  o sondas de puerto. Cada `bash` con red puede pagar ~5–9 s de revisión
  automática; `read_file`/`write_file` no.
- Desde el sandbox no se ven procesos ni puertos del host (namespaces
  propios); el puerto del broker cambia por comando.

## Estado

Ver `memoria de trabajo y pendientes.md` (§6–§8) y `git log`. A propósito no
hay foto fija aquí: duplicarla es como desactualizarse.
