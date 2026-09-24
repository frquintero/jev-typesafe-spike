"""cutoff-spike Fase 0 (smoke) + Fase 1 (coarse).

Sonda de prior pura: state vacio + Nouls desconectadas (sin path, sin
backticks, sin referencia al state). Una sola call Jev por fase (fan-out).

Uso:
    python3 run_cutoff.py smoke|coarse|coarse2|all

coarse2: re-corrida sobre probes_coarse_v2.json (wording e IDs sin
pistas temporales). Mapeo: id -> clave de questions, statement ->
instructions. El id nunca se pega en instructions.

Runtime solo stdlib (urllib + dicts, regla 6 del repo): el SDK queda
como referencia de tipos, no se usa aca. Keys solo por entorno.
"""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"  # pineado, no alias (PLAN.md)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # cutoff-spike/
SPIKE_DIR = os.path.dirname(BASE_DIR)  # spike-jev/
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")
PROBES_PATH = os.path.join(BASE_DIR, "probes_coarse.json")
PROBES_V2_PATH = os.path.join(BASE_DIR, "probes_coarse_v2.json")

# Digitos de anio prohibidos en keys v2: anios de 4 cifras + fragmentos
# de 2 cifras de los anios del corpus (2019, 2023-2026). Runs como
# iphone17, cop30, win10, btc-first-100k, gpt5, f1, eclipse-3-* no son
# anios y pasan.
YEAR_FRAGMENTS = {"19", "23", "24", "25", "26"}


def has_year_digits(key):
    if re.search(r"(19|20)\d\d", key):
        return True
    return bool(set(re.findall(r"\d+", key)) & YEAR_FRAGMENTS)

SMOKE_TRUE = "Is Paris the capital of France?"
SMOKE_FALSE = "Is Berlin the capital of France?"
SMOKE_QUESTIONS = {
    "smoke_true": {"type": "noul", "instructions": SMOKE_TRUE},
    "smoke_false": {"type": "noul", "instructions": SMOKE_FALSE},
}

TIMEOUT_S = 120
MAX_ATTEMPTS = 4
BACKOFF_S = (2, 4, 8)  # entre intentos 1-2, 2-3, 3-4


def jev_call(state, questions):
    """Una call al cable. Devuelve (request_body, response)."""
    body = {"model": MODEL, "state": state, "questions": questions}
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
        return body, json.loads(r.read().decode())


def retryable(err):
    """Reintentar solo errores transitorios; un 400 es pedido malo, no reintentar."""
    if isinstance(err, urllib.error.HTTPError):
        return err.code == 429 or err.code >= 500
    return isinstance(err, urllib.error.URLError)


def jev_call_backoff(state, questions):
    """Reintenta la call COMPLETA con backoff; nunca probes sueltos."""
    last = None
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return jev_call(state, questions)
        except Exception as err:  # noqa: BLE001 - reportar y reintentar/abortar
            last = err
            if not retryable(err) or attempt == MAX_ATTEMPTS:
                raise
            wait = BACKOFF_S[attempt - 1] if attempt - 1 < len(BACKOFF_S) else BACKOFF_S[-1]
            print(f"  intento {attempt} fallo ({err}); reintento en {wait}s...", flush=True)
            time.sleep(wait)
    raise last


def save_cache(name, request_body, response):
    os.makedirs(CACHE_DIR, exist_ok=True)
    path = os.path.join(CACHE_DIR, name)
    with open(path, "w") as f:
        json.dump({"request": request_body, "response": response}, f, ensure_ascii=False)
    return path


def run_smoke():
    """Fase 0: 2 Nouls en un request. Devuelve (state_usado, ok)."""
    try:
        body, resp = jev_call("", SMOKE_QUESTIONS)
        state_used = ""
    except urllib.error.HTTPError as err:
        print(f'state "" rechazado ({err}); probando fallback "k"...')
        body, resp = jev_call("k", SMOKE_QUESTIONS)
        state_used = "k"
    path = save_cache("cutoff-smoke.json", body, resp)
    answers = resp.get("answers", {})
    t = answers.get("smoke_true", {}).get("noul")
    f = answers.get("smoke_false", {}).get("noul")
    print(f"smoke state_used={state_used!r} cache={path}")
    print(f"  smoke_true  noul={t} (umbral >= 0.8)")
    print(f"  smoke_false noul={f} (umbral <= 0.3)")
    ok = (
        t is not None
        and f is not None
        and t >= 0.8
        and f <= 0.3
    )
    print("  smoke: " + ("OK" if ok else "FALLA"))
    return state_used, ok


def smoke_state_or_default():
    """State de la fase 0 (leido del cache smoke si existe)."""
    path = os.path.join(CACHE_DIR, "cutoff-smoke.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)["request"]["state"]
    return ""


def run_coarse(state):
    """Fase 1: los 33 probes en UN solo request."""
    with open(PROBES_PATH) as f:
        corpus = json.load(f)
    probes = corpus["probes"]
    print(f"coarse: {len(probes)} probes, state={state!r}, 1 call...")
    questions = {p["id"]: {"type": "noul", "instructions": p["statement"]} for p in probes}
    body, resp = jev_call_backoff(state, questions)
    answers = resp.get("answers", {})
    missing = [p["id"] for p in probes if p["id"] not in answers]
    if missing:
        raise SystemExit(f"coarse incompleto: faltan {missing} (no se reintentan sueltos; abortar)")
    path = save_cache("cutoff-coarse.json", body, resp)
    print(f"coarse cache={path}")
    print(f"{'id':28s} {'truth':5s} noul")
    for p in probes:
        noul = answers[p["id"]].get("noul")
        print(f"{p['id']:28s} {str(p['ground_truth']):5s} {noul}")


def run_coarse2():
    """Coarse v2: 33 Nouls sin sesgo en UN solo request, state ''."""
    with open(PROBES_V2_PATH) as f:
        corpus = json.load(f)
    probes = corpus["probes"]
    bad_ids = [p["id"] for p in probes if has_year_digits(p["id"])]
    if bad_ids:
        raise SystemExit(f"ids v2 con digitos de anio (abortar): {bad_ids}")
    print(f"coarse2: {len(probes)} probes, state='', 1 call...")
    questions = {p["id"]: {"type": "noul", "instructions": p["statement"]} for p in probes}
    body, resp = jev_call_backoff("", questions)
    answers = resp.get("answers", {})
    missing = [p["id"] for p in probes if p["id"] not in answers]
    if missing:
        raise SystemExit(f"coarse2 incompleto: faltan {missing} (no se reintentan sueltos; abortar)")
    path = save_cache("cutoff-coarse-v2.json", body, resp)
    # Validar contra el crudo guardado (no contra lo que creemos que mandamos).
    with open(path) as f:
        saved = json.load(f)
    stmt = {p["id"]: p["statement"] for p in probes}
    mism = [k for k, q in saved["request"]["questions"].items()
            if q.get("instructions") != stmt.get(k)]
    badkeys = [k for k in saved["request"]["questions"] if has_year_digits(k)]
    print(f"coarse2 cache={path}")
    print(f"validacion: instructions!=statement: {len(mism)} {mism or ''}")
    print(f"validacion: keys con digitos de anio: {len(badkeys)} {badkeys or ''}")
    print(f"{'id':26s} {'ref_v1':28s} {'truth':5s} noul")
    for p in probes:
        noul = answers[p["id"]].get("noul")
        print(f"{p['id']:26s} {p['ref_v1']:28s} {str(p['ground_truth']):5s} {noul}")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("smoke", "coarse", "coarse2", "all"):
        raise SystemExit("uso: python3 run_cutoff.py smoke|coarse|coarse2|all")
    mode = argv[1]
    if mode == "coarse2":
        run_coarse2()
        return
    if mode in ("smoke", "all"):
        state_used, ok = run_smoke()
        if not ok:
            raise SystemExit("smoke fuera de umbrales: abortar, no correr coarse")
        if mode == "smoke":
            return
    else:
        state_used = smoke_state_or_default()
    run_coarse(state_used)


if __name__ == "__main__":
    main(sys.argv)
