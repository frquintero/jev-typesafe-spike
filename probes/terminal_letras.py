"""Spike: terminal con letras sueltas en instructions (contraste con la palabra completa)."""
import json
import os
import urllib.request

body = {
    "model": "jev-latest",
    "state": "",
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": "letras en 't', 'e', 'r', 'm', 'i', 'n', 'a', 'l'",
            "criteria": {
                "opción 1": "4",
                "opción 2": "6",
                "opción 3": "8",
                "opción 4": "9",
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
with open("spike-jev/cache/terminal-letras.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
