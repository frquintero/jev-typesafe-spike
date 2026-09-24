"""Spike: state vacío, Choice con conteo de letras en instructions."""
import json
import os
import urllib.request

CRITERIA = {
    "7": "La palabra tiene 7 letras",
    "8": "La palabra tiene 8 letras",
    "9": "La palabra tiene 9 letras",
    "10": "La palabra tiene 10 letras",
    "11": "La palabra tiene 11 letras",
    "12": "La palabra tiene 12 letras",
}

body = {
    "model": "jev-latest",
    "state": "",
    "questions": {
        "n01": {
            "type": "choice",
            "instructions": "¿Cuántas letras tiene la palabra 'strawberry'?",
            "criteria": CRITERIA,
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
with open("spike-jev/cache/strawberry.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

print("ENVIADO:")
print(json.dumps(body, ensure_ascii=False, indent=2))
print("\nRECIBIDO:")
print(json.dumps(resp, ensure_ascii=False, indent=2))
