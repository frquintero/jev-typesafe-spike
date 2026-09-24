"""Corrida: modalidad de oracion con Choice, state vacio, 8 oraciones x 3 replicas.

Cada replica manda las 8 preguntas juntas en un solo request (fan-out).
Crudos en cache/modalidad-choice-8-r{1,2,3}.json. Idempotente: si el
crudo de una replica ya existe, no se vuelve a llamar.
"""
import json
import os
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIKE_DIR = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")

MODEL = "jev-1.13.0"
REPS = (1, 2, 3)
UA = "spike-jev/1.0"
API_URL = "https://api.typesafe.ai/v1/systemone"

# (id, oracion) -- lo esperado vive solo aqui, en codigo, NO se envia a Jev.
ORACIONES = [
    ("q1", "La puerta está abierta.", "a"),
    ("q2", "Juan llegó ayer.", "a"),
    ("q3", "¿Vienes mañana?", "b"),
    ("q4", "¿Dónde está la llave?", "b"),
    ("q5", "Cierra la ventana.", "c"),
    ("q6", "Siéntate aquí.", "c"),
    ("q7", "¡Qué frío hace!", "d"),
    ("q8", "Ojalá llueva mañana.", "d"),
]


def criteria_for(s):
    return {
        "a": f"«{s}» es enunciativa",
        "b": f"«{s}» es interrogativa",
        "c": f"«{s}» es imperativa",
        "d": f"«{s}» es exclamativa, desiderativa o dubitativa",
        "e": f"«{s}» es otra cosa",
    }


def build_questions():
    questions = {}
    for qid, s, _esperado in ORACIONES:
        questions[qid] = {
            "type": "choice",
            "instructions": "",
            "criteria": criteria_for(s),
        }
    return questions


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
    return os.path.join(CACHE_DIR, f"modalidad-choice-8-r{rep}.json")


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    body = {"model": MODEL, "state": "", "questions": build_questions()}
    for rep in REPS:
        path = cache_path(rep)
        if os.path.exists(path):
            print(f"r{rep}: crudo ya existe, salto ({path})")
            continue
        resp = jev_call(body)
        with open(path, "w") as f:
            json.dump({"request": body, "response": resp}, f, ensure_ascii=False, indent=2)
        print(f"r{rep}: hecho -> {path}")


if __name__ == "__main__":
    run()
