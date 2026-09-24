"""Prueba 6: instructions vacio en Choice? 3 variantes x 3 replicas = 9 requests.

Orden: v3 una vez primero; si 4xx, guardar error en vacio-v3-error.json,
no reintentar v3, seguir con v1/v2. Uso: run|analyze.
"""
import datetime
import json
import os
import sys
import time
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIKE_DIR = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")

MODEL = "jev-1.13.0"
REPS = (1, 2, 3)
UA = "spike-jev/1.0"

FOLLETO = "Australia combina playas extensas y desiertos rojos. Su capital, Canberra, es una ciudad moderna y ordenada. La mejor época para visitarla va de septiembre a noviembre."

CRITERIA = {
    "Sídney": "`folleto` dice que la capital de Australia es Sídney.",
    "Canberra": "`folleto` dice que la capital de Australia es Canberra.",
    "otra": "`folleto` dice otra ciudad o no dice cuál es la capital.",
}

INSTR = {
    "v1": "¿Cuál es la capital de Australia según `folleto`?",
    "v2": "`folleto`",
    "v3": "",
}

PRED = "Canberra > 0.9, otra <= 0.05 en las tres variantes (si v3 aceptada)"


def jev_call(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": UA},
        method="POST")
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode()), time.perf_counter() - t0


def one_call(variant, rep):
    path = os.path.join(CACHE_DIR, f"vacio-{variant}-r{rep}.json")
    if os.path.exists(path):
        return "skipped"
    body = {"model": MODEL, "state": {"folleto": FOLLETO},
            "questions": {"capital": {"type": "choice",
                                      "instructions": INSTR[variant],
                                      "criteria": CRITERIA}}}
    try:
        resp, latency = jev_call(body)
    except urllib.error.HTTPError as e:
        return ("error", e.code, e.read()[:500])
    if resp.get("model") != MODEL:
        raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
    with open(path, "w") as f:
        json.dump({"request": body, "response": resp,
                   "meta": {"pred": PRED, "latency_s": round(latency, 2),
                            "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
    time.sleep(0.5)
    return "ok"


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    calls = skipped = 0
    # 1. v3 una sola vez primero
    r = one_call("v3", 1)
    if isinstance(r, tuple):
        _, code, body = r
        with open(os.path.join(CACHE_DIR, "vacio-v3-error.json"), "w") as f:
            json.dump({"code": code, "body": body.decode("utf-8", "replace")}, f)
        print(f"v3 rechazada: HTTP {code}: {body[:200]}")
        v3_ok = False
    else:
        calls += r == "ok"
        skipped += r == "skipped"
        v3_ok = True
    # 2. resto
    for variant, reps in (("v1", REPS), ("v2", REPS), ("v3", (2, 3) if v3_ok else ())):
        for rep in reps:
            r = one_call(variant, rep)
            if isinstance(r, tuple):
                _, code, body = r
                raise SystemExit(f"{variant} r{rep}: HTTP {code}: {body[:200]}")
            calls += r == "ok"
            skipped += r == "skipped"
    print(f"llamadas: {calls}, omitidas: {skipped}, v3_aceptada: {v3_ok}")


def analyze():
    print("variante | P(Sídney) | P(Canberra) | P(otra) | confidence (media [min-max])")
    for v in ("v1", "v2", "v3"):
        paths = [os.path.join(CACHE_DIR, f"vacio-{v}-r{r}.json") for r in REPS]
        if not all(os.path.exists(p) for p in paths):
            print(f"{v}: SIN CRUDOS (rechazada?)")
            continue
        ds = [json.load(open(p)) for p in paths]
        out = []
        for key in ("Sídney", "Canberra", "otra"):
            vs = [d["response"]["answers"]["capital"]["probabilities"][key] for d in ds]
            out.append(f"{sum(vs) / 3:.2f} [{min(vs):.2f}-{max(vs):.2f}]")
        cs = [d["response"]["answers"]["capital"]["confidence"] for d in ds]
        out.append(f"{sum(cs) / 3:.2f} [{min(cs):.2f}-{max(cs):.2f}]")
        print(f"{v} | " + " | ".join(out))


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 instructions_vacio.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
