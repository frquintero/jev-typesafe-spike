"""Prueba 2: el objeto del juicio. 2 folletos x 3 replicas = 6 requests.

Uso: python3 objeto_juicio.py run|analyze
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

STATES = {
    "afirmaP": "Australia combina playas extensas y desiertos rojos. Su capital, Sídney, es una ciudad moderna y ordenada. La mejor época para visitarla va de septiembre a noviembre.",
    "afirmaQ": "Australia combina playas extensas y desiertos rojos. Su capital, Canberra, es una ciudad moderna y ordenada. La mejor época para visitarla va de septiembre a noviembre.",
}

QUESTIONS = {
    "dice_noul": {
        "type": "noul",
        "instructions": "`folleto` afirma que la capital de Australia es Sídney.",
    },
    "dice_choice": {
        "type": "choice",
        "instructions": "Según `folleto`, ¿cuál es la capital de Australia?",
        "criteria": {
            "Sídney": "`folleto` dice que la capital de Australia es Sídney.",
            "Canberra": "`folleto` dice que la capital de Australia es Canberra.",
            "otra": "`folleto` dice otra ciudad o no la indica.",
        },
    },
    "correcto_noul": {
        "type": "noul",
        "instructions": "El dato que da `folleto` sobre la capital de Australia es correcto.",
    },
    "correcto_choice": {
        "type": "choice",
        "instructions": "¿El dato que da `folleto` sobre la capital de Australia es correcto?",
        "criteria": {
            "correcto": "El dato de `folleto` sobre la capital de Australia es correcto.",
            "incorrecto": "El dato de `folleto` sobre la capital de Australia es incorrecto.",
            "no aplica": "`folleto` no da ningún dato sobre la capital de Australia.",
        },
    },
}

PRED = {
    "afirmaP": {"dice_noul": ">0.8", "dice_choice": "Sídney",
                "correcto_noul": "<0.2", "correcto_choice": "incorrecto"},
    "afirmaQ": {"dice_noul": "<0.2", "dice_choice": "Canberra",
                "correcto_noul": ">0.8", "correcto_choice": "correcto"},
}


def jev_call(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ["TYPESAFE_API_KEY"],
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
    for fid, folleto in STATES.items():
        for rep in REPS:
            path = os.path.join(CACHE_DIR, f"objeto-{fid}-r{rep}.json")
            if os.path.exists(path):
                skipped += 1
                continue
            body = {"model": MODEL, "state": {"folleto": folleto}, "questions": QUESTIONS}
            resp, latency = jev_call(body)
            if resp.get("model") != MODEL:
                raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
            with open(path, "w") as f:
                json.dump({"request": body, "response": resp,
                           "meta": {"pred": PRED[fid], "latency_s": round(latency, 2),
                                    "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
            calls += 1
            time.sleep(0.5)
    print(f"llamadas: {calls}, omitidas: {skipped}")


def logit(p):
    p = min(0.99, max(0.01, p))
    return math.log(p / (1 - p))


def load(fid):
    return [json.load(open(os.path.join(CACHE_DIR, f"objeto-{fid}-r{r}.json"))) for r in REPS]


def analyze():
    for fid in ("afirmaP", "afirmaQ"):
        print(f"== {fid} ==")
        ds = load(fid)
        for q in ("dice_noul", "correcto_noul"):
            vs = [d["response"]["answers"][q]["noul"] for d in ds]
            print(f"  {q}: {sum(vs) / 3:.2f} [{min(vs):.2f}-{max(vs):.2f}]")
        for q in ("dice_choice", "correcto_choice"):
            opts = list(QUESTIONS[q]["criteria"])
            mp = {o: sum(d["response"]["answers"][q]["probabilities"][o] for d in ds) / 3 for o in opts}
            ch = max(opts, key=lambda o: mp[o])
            print(f"  {q}: " + " ".join(f"{o}={mp[o]:.2f}" for o in opts) + f" -> {ch}")
    print()
    print("== tabla central: Noul vs Choice por objeto ==")
    print("folleto | objeto   | Noul | P(Choice equiv) | dlogit | mismo lado")
    for fid, obj, nq, cq, opt in (
            ("afirmaP", "dice", "dice_noul", "dice_choice", "Sídney"),
            ("afirmaP", "correcto", "correcto_noul", "correcto_choice", "correcto"),
            ("afirmaQ", "dice", "dice_noul", "dice_choice", "Sídney"),
            ("afirmaQ", "correcto", "correcto_noul", "correcto_choice", "correcto")):
        ds = load(fid)
        n = sum(d["response"]["answers"][nq]["noul"] for d in ds) / 3
        c = sum(d["response"]["answers"][cq]["probabilities"][opt] for d in ds) / 3
        dl = logit(n) - logit(c)
        print(f"{fid} | {obj:8s} | {n:.2f} | {c:.2f} | {dl:+.2f} | "
              + ("si" if (n > 0.5) == (c > 0.5) else "NO"))
    print()
    print("== cambio de objeto en afirmaP ==")
    ds = load("afirmaP")
    dn = sum(d["response"]["answers"]["dice_noul"]["noul"] for d in ds) / 3
    cn = sum(d["response"]["answers"]["correcto_noul"]["noul"] for d in ds) / 3
    dc = sum(d["response"]["answers"]["dice_choice"]["probabilities"]["Sídney"] for d in ds) / 3
    cc = sum(d["response"]["answers"]["correcto_choice"]["probabilities"]["correcto"] for d in ds) / 3
    print(f"  dice vs correcto — Noul: {dn:.2f} vs {cn:.2f} opuestos: {(dn > 0.5) != (cn > 0.5)}; "
          f"Choice(Sídney vs correcto): {dc:.2f} vs {cc:.2f}")
    print()
    print("== opciones de salida > 0.10 ==")
    found = False
    for fid in ("afirmaP", "afirmaQ"):
        ds = load(fid)
        for q, o in (("dice_choice", "otra"), ("correcto_choice", "no aplica")):
            m = sum(d["response"]["answers"][q]["probabilities"][o] for d in ds) / 3
            if m > 0.10:
                print(f"  {fid}/{q}/{o}: {m:.2f}")
                found = True
    if not found:
        print("  ninguna")
    print()
    print("== predicciones falladas ==")
    # afirmaP: dice_noul>0.8, dice_choice=Sídney, correcto_noul<0.2, correcto_choice=incorrecto
    # afirmaQ: dice_noul<0.2, dice_choice=Canberra, correcto_noul>0.8, correcto_choice=correcto
    checks = []
    for fid in ("afirmaP", "afirmaQ"):
        ds = load(fid)
        dn = sum(d["response"]["answers"]["dice_noul"]["noul"] for d in ds) / 3
        cn = sum(d["response"]["answers"]["correcto_noul"]["noul"] for d in ds) / 3
        dc = {o: sum(d["response"]["answers"]["dice_choice"]["probabilities"][o] for d in ds) / 3
              for o in QUESTIONS["dice_choice"]["criteria"]}
        cc = {o: sum(d["response"]["answers"]["correcto_choice"]["probabilities"][o] for d in ds) / 3
              for o in QUESTIONS["correcto_choice"]["criteria"]}
        exp = PRED[fid]
        if fid == "afirmaP":
            if not dn > 0.8:
                checks.append(f"{fid}/dice_noul: pred >0.8 vs {dn:.2f}")
            if max(dc, key=dc.get) != "Sídney":
                checks.append(f"{fid}/dice_choice: pred Sídney vs {max(dc, key=dc.get)}")
            if not cn < 0.2:
                checks.append(f"{fid}/correcto_noul: pred <0.2 vs {cn:.2f}")
            if max(cc, key=cc.get) != "incorrecto":
                checks.append(f"{fid}/correcto_choice: pred incorrecto vs {max(cc, key=cc.get)}")
        else:
            if not dn < 0.2:
                checks.append(f"{fid}/dice_noul: pred <0.2 vs {dn:.2f}")
            if max(dc, key=dc.get) != "Canberra":
                checks.append(f"{fid}/dice_choice: pred Canberra vs {max(dc, key=dc.get)}")
            if not cn > 0.8:
                checks.append(f"{fid}/correcto_noul: pred >0.8 vs {cn:.2f}")
            if max(cc, key=cc.get) != "correcto":
                checks.append(f"{fid}/correcto_choice: pred correcto vs {max(cc, key=cc.get)}")
    print("  " + ("\n  ".join(checks) if checks else "ninguna"))
    print()
    print("== réplicas rango > 0.10 ==")
    found = False
    for fid in ("afirmaP", "afirmaQ"):
        ds = load(fid)
        for q in ("dice_noul", "correcto_noul"):
            vs = [d["response"]["answers"][q]["noul"] for d in ds]
            if max(vs) - min(vs) > 0.10:
                print(f"  {fid}/{q}: {max(vs) - min(vs):.2f}")
                found = True
        for q in ("dice_choice", "correcto_choice"):
            for o in QUESTIONS[q]["criteria"]:
                vs = [d["response"]["answers"][q]["probabilities"][o] for d in ds]
                if max(vs) - min(vs) > 0.10:
                    print(f"  {fid}/{q}/{o}: {max(vs) - min(vs):.2f}")
                    found = True
    if not found:
        print("  ninguna")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 objeto_juicio.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
