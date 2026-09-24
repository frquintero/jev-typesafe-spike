"""Spike: párrafo EN, instructions con 'letes in' (tal cual) en lugar de 'letras en'."""
import json
import os
import urllib.request

PARRAFO = (
    "The sample mean converges toward the expectation as the number of "
    "independent observations grows. That convergence, known as the law "
    "of large numbers, sustains much of modern statistical inference and "
    "the analysis of experimental data."
)

N_LETRAS = sum(c.isalpha() for c in PARRAFO)
N_CARACTERES = len(PARRAFO)
print(f"conteo python: {N_LETRAS} letras (alfabéticas) | {N_CARACTERES} caracteres con espacios")

body = {
    "model": "jev-latest",
    "state": "",
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": f"letes in '{PARRAFO}'",
            "criteria": {
                "opción 1": str(N_LETRAS - 40),
                "opción 2": str(N_LETRAS - 10),
                "opción 3": str(N_LETRAS),
                "opción 4": str(N_LETRAS + 20),
            },
        }
    },
}

req = urllib.request.Request(
    "https://api.typesafe.ai/v1/systemone",
    data=json.dumps(body).encode(),
    headers={
        "Content-Type": "application/json",
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as r:
    resp = json.loads(r.read().decode())

os.makedirs("spike-jev/cache", exist_ok=True)
with open("spike-jev/cache/parrafo-estadistica-en-letes.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
