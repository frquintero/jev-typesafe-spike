"""Spike: batería Noul — "has more than X letters" con X en N*0.3, N*0.7, N, N*1.3, N*2."""
import json
import os
import time
import urllib.request

PARRAFO = (
    "The sample mean converges toward the expectation as the number of "
    "independent observations grows. That convergence, known as the law "
    "of large numbers, sustains much of modern statistical inference and "
    "the analysis of experimental data."
)

N = sum(c.isalpha() for c in PARRAFO)
N_CARACTERES = len(PARRAFO)
print(f"conteo python: {N} letras (alfabéticas) | {N_CARACTERES} caracteres con espacios")

umbrales = [round(N * 0.3), round(N * 0.7), N, round(N * 1.3), round(N * 2)]

os.makedirs("spike-jev/cache", exist_ok=True)
filas = []
for i, t in enumerate(umbrales, 1):
    body = {
        "model": "jev-latest",
        "state": PARRAFO,
        "questions": {
            "n01": {
                "type": "noul",
                "instructions": f"has more than {t} letters",
            }
        },
    }
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "Authorization": "Bearer " + os.environ["TYPESAFE_API_KEY"],
        },
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    dt = time.perf_counter() - t0
    with open(f"spike-jev/cache/parrafo-noul-{t}.json", "w") as f:
        json.dump({"request": body, "response": resp}, f, ensure_ascii=False)
    noul = resp["answers"]["n01"]["noul"]
    verdad = N > t
    filas.append((i, t, t / N, verdad, noul, dt))

print(f"\n{'#':2} {'umbral':7} {'x N':6} {'verdad':7} {'noul':6} {'lat':5}")
for i, t, x, verdad, noul, dt in filas:
    print(f"{i:2} {t:7} {x:6.2f} {str(verdad):7} {noul:6.2f} {dt:4.1f}s")
