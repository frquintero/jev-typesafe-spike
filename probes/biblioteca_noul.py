"""Spike: caso biblioteca — Noul con paths pelados en instructions."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": {
        "socio": {"id": "L-08", "prestamos_activos": 2},
        "solicitud": {"libro": "Cien años de soledad", "ejemplares disponibles": 0},
        "regla": "máx. 3 préstamos",
    },
    "questions": {
        "n01": {
            "type": "noul",
            "instructions": "¿puede `socio.id` llevarse `solicitud.libro`?",
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
with open("spike-jev/cache/biblioteca-noul.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
