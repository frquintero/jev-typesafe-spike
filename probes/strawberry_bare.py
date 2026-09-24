"""Spike: state vacío, Choice sin prosa: instructions 'letras en strawberry', criteria solo números."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": "",
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": "letras en 'strawberry'",
            "criteria": {k: k for k in ["7", "8", "9", "10", "11", "12"]},
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
with open("spike-jev/cache/strawberry-bare.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
