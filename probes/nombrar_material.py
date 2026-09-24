"""Prueba 3a: como nombrar el material en la pregunta. 3 requests x 8 Nouls.

Uso: python3 nombrar_material.py run|analyze
"""
import datetime
import json
import math
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

QUESTIONS = {
    "campo_canberra": {"type": "noul", "instructions": "`folleto` afirma que la capital de Australia es Canberra."},
    "campo_sidney": {"type": "noul", "instructions": "`folleto` afirma que la capital de Australia es Sídney."},
    "elfolleto_canberra": {"type": "noul", "instructions": "El folleto afirma que la capital de Australia es Canberra."},
    "elfolleto_sidney": {"type": "noul", "instructions": "El folleto afirma que la capital de Australia es Sídney."},
    "eltexto_canberra": {"type": "noul", "instructions": "El texto afirma que la capital de Australia es Canberra."},
    "eltexto_sidney": {"type": "noul", "instructions": "El texto afirma que la capital de Australia es Sídney."},
    "eldocumento_canberra": {"type": "noul", "instructions": "El documento afirma que la capital de Australia es Canberra."},
    "eldocumento_sidney": {"type": "noul", "instructions": "El documento afirma que la capital de Australia es Sídney."},
}

FORMAS = [("`folleto`", "campo"), ("el folleto", "elfolleto"),
          ("el texto", "eltexto"), ("el documento", "eldocumento")]

PRED = {"canberra": ">0.8", "sidney": "<0.2"}


def jev_call(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "User-Agent": UA},
        method="POST")
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read()[:200]}")
    return resp, time.perf_counter() - t0


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    calls = skipped = 0
    for rep in REPS:
        path = os.path.join(CACHE_DIR, f"nombrar-r{rep}.json")
        if os.path.exists(path):
            skipped += 1
            continue
        body = {"model": MODEL, "state": {"folleto": FOLLETO}, "questions": QUESTIONS}
        resp, latency = jev_call(body)
        if resp.get("model") != MODEL:
            raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
        with open(path, "w") as f:
            json.dump({"request": body, "response": resp,
                       "meta": {"pred": PRED, "latency_s": round(latency, 2),
                                "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
        calls += 1
        time.sleep(0.5)
    print(f"llamadas: {calls}, omitidas: {skipped}")


def logit(p):
    p = min(0.99, max(0.01, p))
    return math.log(p / (1 - p))


def vals(q):
    out = []
    for r in REPS:
        with open(os.path.join(CACHE_DIR, f"nombrar-r{r}.json")) as f:
            out.append(json.load(f)["response"]["answers"][q]["noul"])
    return out


def analyze():
    print("== tabla por forma ==")
    print("forma        | Canberra media [min-max] | Sídney media [min-max] | sep dlogit | acierto")
    rows = []
    for label, prefix in FORMAS:
        c = vals(f"{prefix}_canberra")
        s = vals(f"{prefix}_sidney")
        mc, ms = sum(c) / 3, sum(s) / 3
        sep = logit(mc) - logit(ms)
        ok = mc > 0.5 and ms < 0.5
        rows.append((label, sep))
        print(f"{label:12s} | {mc:.2f} [{min(c):.2f}-{max(c):.2f}] | {ms:.2f} [{min(s):.2f}-{max(s):.2f}] | {sep:+.2f} | {'+' if ok else '-'}")
    print()
    print("== orden por separación ==")
    for label, sep in sorted(rows, key=lambda t: -t[1]):
        print(f"  {label}: {sep:+.2f}")
    print()
    print("== formas fuera de banda (Canberra<0.8 o Sídney>0.2) ==")
    found = False
    for label, prefix in FORMAS:
        mc = sum(vals(f"{prefix}_canberra")) / 3
        ms = sum(vals(f"{prefix}_sidney")) / 3
        if mc < 0.8 or ms > 0.2:
            print(f"  {label}: canberra={mc:.2f} sidney={ms:.2f}")
            found = True
    if not found:
        print("  ninguna")
    print()
    cs = vals("campo_sidney")
    print(f"== vs prueba 2 (Sídney `folleto` = 0.01): campo_sidney media {sum(cs) / 3:.2f} "
          f"[{min(cs):.2f}-{max(cs):.2f}]")
    print()
    print("== réplicas rango > 0.10 ==")
    found = False
    for q in QUESTIONS:
        v = vals(q)
        if max(v) - min(v) > 0.10:
            print(f"  {q}: {max(v) - min(v):.2f}")
            found = True
    if not found:
        print("  ninguna")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 nombrar_material.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
