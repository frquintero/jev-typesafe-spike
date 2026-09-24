"""Spike: caso vecinos — Noul literal, sin campo contexto en el state."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": {
        "mensaje": "Qué curioso que el pasillo del tercero siempre esté impecable menos los lunes, que es cuando pasa la señora del 3B con el perro."
    },
    "questions": {
        "n01": {
            "type": "noul",
            "instructions": "se insinúa que alguien ensucia",
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
with open("spike-jev/cache/vecinos-noul.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
