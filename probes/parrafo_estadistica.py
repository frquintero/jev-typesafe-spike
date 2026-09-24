"""Spike: state vacío, párrafo de estadística en instructions, Choice [N-40, N-10, N, N+20]."""
import json
import os
import urllib.request

PARRAFO = (
    "La media muestral converge hacia la esperanza cuando crece el número "
    "de observaciones independientes. Esa convergencia, la ley de los "
    "grandes números, sostiene buena parte de la inferencia estadística "
    "moderna y del análisis de datos experimentales."
)

N_LETRAS = sum(c.isalpha() for c in PARRAFO)
N_CARACTERES = len(PARRAFO)
assert N_CARACTERES <= 300
print(f"conteo python: {N_LETRAS} letras (alfabéticas) | {N_CARACTERES} caracteres con espacios")

body = {
    "model": "jev-latest",
    "state": "",
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": f"letras en '{PARRAFO}'",
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
        "Authorization": "Bearer " + os.environ["TYPESAFE_API_KEY"],
    },
    method="POST",
)
with urllib.request.urlopen(req, timeout=120) as r:
    resp = json.loads(r.read().decode())

os.makedirs("spike-jev/cache", exist_ok=True)
with open("spike-jev/cache/parrafo-estadistica.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
