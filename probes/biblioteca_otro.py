"""Spike: caso biblioteca — Choice con no-match explícito ('otro')."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": {
        "socio": {"id": "L-08", "prestamos_activos": 4, "grado_estudiante": "desconocido"},
        "regla": "estudiante pregrado max. 3 préstamos; estudiante posgrado max. 5 prestamos",
    },
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": "determinar socio.grado_estudiante",
            "criteria": {
                "pregrado": "pregrado",
                "posgrado": "posgrado",
                "otro": "el grado no se puede determinar con la regla y los hechos",
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
with open("spike-jev/cache/biblioteca-otro.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
