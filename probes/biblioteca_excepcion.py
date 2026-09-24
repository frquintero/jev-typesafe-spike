"""Spike: caso biblioteca con excepción por nivel — Noul literal."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": {
        "socio": {"id": "L-08", "prestamos_activos": 4, "estudiante": "posgrado"},
        "solicitud": {"libro": "Cien años de soledad", "ejemplares disponibles": 0},
        "regla": "estudiante.pregrado 3; estudiante.posgrado 5",
    },
    "questions": {
        "n01": {
            "type": "noul",
            "instructions": "puede socio.id retirar solicitud.libro",
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
with open("spike-jev/cache/biblioteca-excepcion-0.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
