"""Spike: gradiente por tamaño — 10/40/100/200/500 letras, 3 reps.

Cada request (fan-out): 5 Noul "has more than X letters" (X = 0.3N, 0.7N, N,
1.3N, 2N) + 1 Choice "letters in '<texto>'" con opciones [0.8N, 0.95N, N, 1.1N].
"""
import json
import os
import statistics
import time
import urllib.request

TEXTOS = {
    10: "statistics",
    40: "Random samples vary around the population mean.",
    100: (
        "The sample mean converges toward the expectation as the number of "
        "independent observations grows. More data helps a lot."
    ),
    200: (
        "The sample mean converges toward the expectation as the number of "
        "independent observations grows. That convergence, known as the law "
        "of large numbers, sustains much of the modern statistical inference "
        "and the analysis of experimental data."
    ),
    500: (
        "The sample mean converges toward the expectation as the number of "
        "independent observations grows. That convergence, known as the law "
        "of large numbers, sustains much of the modern statistical inference "
        "and the analysis of experimental data. "
        "Estimators are compared by their bias and variance. "
        "Hypothesis tests control the probability of false discoveries. "
        "Regression models describe how variables change together. "
        "Random sampling reduces the risk of systematic distortions. "
        "Sample sizes matter very much. "
        "Outliers distort the mean more than the median. "
        "Good designs reduce bias and variance at once."
    ),
}

N_LETRAS = {k: sum(c.isalpha() for c in v) for k, v in TEXTOS.items()}
for k, v in N_LETRAS.items():
    assert v == k, (k, v)
print("conteo python (letras):", N_LETRAS)

REPS = 3


def umbrales(n):
    return [round(n * 0.3), round(n * 0.7), n, round(n * 1.3), n * 2]


def opciones(n):
    return [int(n * 0.8), int(n * 0.95), n, int(n * 1.1)]


def pregunta_noul(x):
    return {"type": "noul", "instructions": f"has more than {x} letters"}


def pregunta_choice(n, texto):
    opts = opciones(n)
    return {
        "type": "choice",
        "instructions": f"letters in '{texto}'",
        "criteria": {f"opción {i}": str(o) for i, o in enumerate(opts, 1)},
    }


def llamar(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    return resp, time.perf_counter() - t0


def cruce(xs, ps):
    for i in range(len(xs) - 1):
        if ps[i] >= 0.5 > ps[i + 1]:
            return xs[i] + (ps[i] - 0.5) / (ps[i] - ps[i + 1]) * (xs[i + 1] - xs[i])
    return None


os.makedirs("spike-jev/cache", exist_ok=True)
resumen = {}
for n, texto in TEXTOS.items():
    xs = umbrales(n)
    opts = opciones(n)
    filas = []
    for rep in range(1, REPS + 1):
        preguntas = {f"q{i}": pregunta_noul(x) for i, x in enumerate(xs, 1)}
        preguntas["c1"] = pregunta_choice(n, texto)
        body = {"model": "jev-latest", "state": texto, "questions": preguntas}
        resp, dt = llamar(body)
        with open(f"spike-jev/cache/tamano-{n}-r{rep}.json", "w") as f:
            json.dump({"request": body, "response": resp}, f, ensure_ascii=False)
        ns = [resp["answers"][f"q{i}"]["noul"] for i in range(1, 6)]
        ca = resp["answers"]["c1"]
        elegido = int(ca["choice"].split()[-1])
        filas.append({
            "rep": rep, "ns": ns, "dt": dt,
            "choice": elegido, "conf": ca["confidence"], "probs": ca["probabilities"],
            "cruce": cruce(xs, ns),
        })
    resumen[n] = {"xs": xs, "opts": opts, "filas": filas}

print(f"\n{'N':4} {'rep':4} {'noul por umbral (0.3N 0.7N N 1.3N 2N)':38} choice  cruce")
for n, r in resumen.items():
    for f in r["filas"]:
        ns = " ".join(f"{v:.2f} " for v in f["ns"])
        c = f"{f['choice']}{'✓' if f['choice'] == n else '✗'}"
        cr = f"{f['cruce']:.0f}" if f["cruce"] else "—"
        print(f"{n:4} r{f['rep']:<3} {ns} {c:7} {cr}")

print(f"\n{'N':4} {'umbrales Noul':30} {'choice (reps)':16} {'cruce mediano':13} {'sesgo %':8} {'caída 0.7→1.3':13}")
for n, r in resumen.items():
    picks = [f["choice"] for f in r["filas"]]
    cruces = [f["cruce"] for f in r["filas"] if f["cruce"]]
    med = statistics.median(cruces) if cruces else None
    sesgo = (med - n) / n * 100 if med else None
    caida = statistics.mean(f["ns"][1] - f["ns"][3] for f in r["filas"])
    print(f"{n:4} {str(r['xs']):30} {str(picks):16} {(f'{med:.0f}' if med else '—'):13} "
          f"{(f'{sesgo:+.1f}' if sesgo is not None else '—'):8} {caida:13.2f}")
