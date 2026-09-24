"""Corrida: modalidad_escena_2 traducida al ingles, 3 replicas.

Body fijo (verbatim, no se toca). Crudos en
cache/modalidad-escena-2-en-r{1,2,3}.json. Idempotente: si el crudo de
una replica ya existe, no se vuelve a llamar.
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
    "state": "it is a hot day; Juan arrives home and all the windows are closed; his wife is in the living room; Juan says: it's cold, isn't it?",
    "questions": {
        "q1": {
            "type": "choice",
            "instructions": "",
            "criteria": {
                "a": "Juan asks his wife to open the windows",
                "b": "Juan asks his wife whether it is cold",
                "c": "Juan states that it is cold",
                "d": "Juan complains about the heat",
                "e": "Juan does something else",
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
    return os.path.join(CACHE_DIR, f"modalidad-escena-2-en-r{rep}.json")


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
