"""Corrida: misma escena, pregunta en instructions y criteria de una palabra, 3 replicas.

Body fijo (verbatim, no se toca). Crudos en
cache/modalidad-escena-4-r{1,2,3}.json. Idempotente: si el crudo de una
replica ya existe, no se vuelve a llamar.
"""
import json
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIKE_DIR = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")

REPS = (1, 2, 3)
UA = "spike-jev/1.0"
API_URL = "https://api.typesafe.ai/v1/systemone"

BODY = {
    "model": "jev-1.13.0",
    "state": "es un día caluroso; Juan llega a su casa y todas las ventanas están cerradas; su esposa está en la sala; Juan dice: hace frío, no?",
    "questions": {
        "q1": {
            "type": "choice",
            "instructions": "la frase de Juan: \"hace frío, no?\" es:",
            "criteria": {
                "b": "pregunta",
                "c": "afirmación",
                "d": "queja",
                "e": "ironía",
                "f": "ninguna de las anteriores",
            },
        }
    },
}


def jev_call(body):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode(),
        headers={
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        return json.loads(r.read().decode())


def cache_path(rep):
    return os.path.join(CACHE_DIR, f"modalidad-escena-4-r{rep}.json")


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    for rep in REPS:
        path = cache_path(rep)
        if os.path.exists(path):
            print(f"r{rep}: crudo ya existe, salto ({path})")
            continue
        resp = jev_call(BODY)
        with open(path, "w") as f:
            json.dump({"request": BODY, "response": resp}, f, ensure_ascii=False, indent=2)
        print(f"r{rep}: hecho -> {path}")


if __name__ == "__main__":
    run()
