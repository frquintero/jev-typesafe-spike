"""Revisión: ¿por qué dos corridas idénticas dieron bit a bit lo mismo?

Envía dos réplicas: el cuerpo n01 (ya enviado 2 veces, bit-idéntico) y el
cuerpo n02 (enviado 1 vez, dio distribución distinta). Mide latencia para
oler cache del lado servidor.
"""
import json
import os
import time
import urllib.request

CRITERIA = {"opción 1": "4", "opción 2": "6", "opción 3": "8", "opción 4": "9"}


def body(qid):
    return {
        "model": "jev-latest",
        "state": "",
        "questions": {
            qid: {
                "type": "choice",
                "instructions": "letras en 'terminal'",
                "criteria": CRITERIA,
            }
        },
    }


def call(b):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(b).encode(),
        headers={
            "Content-Type": "application/json",
        },
        method="POST",
    )
    t0 = time.perf_counter()
    with urllib.request.urlopen(req, timeout=120) as r:
        resp = json.loads(r.read().decode())
    return resp, time.perf_counter() - t0


os.makedirs("spike-jev/cache", exist_ok=True)
for qid, name in [("n01", "terminal-palabra-n01-r3.json"), ("n02", "terminal-palabra-n02-r2.json")]:
    b = body(qid)
    resp, dt = call(b)
    with open("spike-jev/cache/" + name, "w") as f:
        json.dump({"request": b, "response": resp}, f, ensure_ascii=False)
    a = resp["answers"][qid]
    print(f"[{qid}] {dt:.2f}s choice={a['choice']} conf={a['confidence']} probs={a['probabilities']} usage={resp['usage']}")
