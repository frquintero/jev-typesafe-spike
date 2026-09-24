"""Spike: índice EEL puro en texto (20 líneas, todo rótulos, jerarquía
lógica coherente). Cada pregunta cita su entrada verbatim (sin ordinales)
y pide el nivel usando la posición entre vecinas.
"""
import json
import os
import urllib.request

# (nivel, entrada) — el subtítulo deriva lógicamente de su capítulo.
# Solo texto: sin numerales.
ITEMS = [
    ("titulo", "Sentencia T-012 de 2024"),
    ("capitulo", "ANTECEDENTES"),
    ("subtitulo", "Hechos relevantes"),
    ("subtitulo", "Actuación procesal"),
    ("capitulo", "CONSIDERACIONES"),
    ("subtitulo", "Problema jurídico"),
    ("subtitulo", "Análisis de la Sala"),
    ("capitulo", "RESUELVE"),
    ("subtitulo", "Órdenes impartidas"),
    ("subtitulo", "Alcance del amparo"),
    ("subtitulo", "Condena en costas"),
]

CRITERIA = {
    "titulo": "Nombra el documento completo, va primero y no cuelga de nada",
    "capitulo": "Nombra una parte mayor, deriva directamente del título",
    "subtitulo": "Nombra una subsección que deriva lógicamente del capítulo al que pertenece",
}

doc = "\n".join(t for _, t in ITEMS)
questions = {
    f"n{i:02d}": {
        "type": "choice",
        "instructions": (
            f"En el índice de `doc`, ¿qué nivel ocupa la entrada "
            f"'{texto}'? Usa su posición entre las entradas vecinas."
        ),
        "criteria": CRITERIA,
    }
    for i, (_, texto) in enumerate(ITEMS)
}
body = {"model": "jev-latest", "state": {"doc": doc}, "questions": questions}

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
with open("spike-jev/cache/eel-indice-20.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

ok = 0
print(f"{'id':4} {'esperado':10} {'jev':10} {'conf':6} resto")
for i, (gold, texto) in enumerate(ITEMS):
    a = resp["answers"][f"n{i:02d}"]
    got, conf = a["choice"], a["confidence"]
    mark = "✓" if got == gold else "✗"
    ok += got == gold
    rest = {k: v for k, v in a["probabilities"].items() if v > 0.01 and k != got}
    print(f"n{i:02d} {gold:10} {got:10} {conf:.2f} {mark} {texto[:34]!r} {rest}")
print(f"\nEXACTITUD: {ok}/{len(ITEMS)}")
print("USAGE:", json.dumps(resp.get("usage")))
