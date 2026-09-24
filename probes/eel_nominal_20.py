"""Spike: 20 nominales con rol EEL conocido; un Choice de 5 subtipos por item.

Estructura sintética (título + N1 + N2 + numerales + negativos).
El state lleva el doc ordenado; cada pregunta apunta a su índice con
vecinas como contexto (el subtipo se lee en la posición, no en la forma).
"""
import json
import os
import urllib.request

# (rol, texto)
ITEMS = [
    ("titulo", "Sentencia T-012 de 2024"),
    ("numeral", "I."),
    ("capitulo", "ANTECEDENTES"),
    ("numeral", "1."),
    ("subtitulo", "Hechos relevantes"),
    ("otro_nominal", "Jorge Enrique Salas"),
    ("numeral", "2."),
    ("subtitulo", "Actuación procesal"),
    ("otro_nominal", "Bogotá, D. C."),
    ("numeral", "II."),
    ("capitulo", "CONSIDERACIONES"),
    ("numeral", "2.1."),
    ("subtitulo", "Problema jurídico"),
    ("otro_nominal", "Ley 1581 de 2012"),
    ("numeral", "2.2."),
    ("subtitulo", "Análisis de la Sala"),
    ("otro_nominal", "5 minutos"),
    ("numeral", "III."),
    ("capitulo", "RESUELVE"),
    ("otro_nominal", "34"),
]

CRITERIA = {
    "titulo": "Nombra el documento completo, va primero y no cuelga de nada",
    "capitulo": "Nombra una parte mayor del documento, en mayúsculas o numeración romana",
    "subtitulo": "Nombra una subsección que cuelga de un capítulo",
    "numeral": "Marcador de orden sin texto propio: números, letras o romanos con punto o paréntesis",
    "otro_nominal": "Nombra algo que no rotula ninguna parte: personas, lugares, normas citadas, medidas, números sueltos",
}

state = {"doc": [t for _, t in ITEMS]}
questions = {
    f"e{i:02d}": {
        "type": "choice",
        "instructions": (
            f"Clasifica el elemento {i} de `doc` según qué parte del "
            "documento rotula. Usa los elementos vecinos como contexto."
        ),
        "criteria": CRITERIA,
    }
    for i in range(len(ITEMS))
}
body = {"model": "jev-latest", "state": state, "questions": questions}

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
with open("spike-jev/cache/eel-nominal-20.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

ok = 0
print(f"{'id':4} {'esperado':13} {'jev':13} {'conf':6} resto")
for i, (gold, texto) in enumerate(ITEMS):
    a = resp["answers"][f"e{i:02d}"]
    got, conf = a["choice"], a["confidence"]
    mark = "✓" if got == gold else "✗"
    ok += got == gold
    rest = {k: v for k, v in a["probabilities"].items() if v > 0.01 and k != got}
    print(f"e{i:02d} {gold:13} {got:13} {conf:.2f} {mark} {texto[:38]!r} {rest}")
print(f"\nEXACTITUD: {ok}/{len(ITEMS)}")
print("USAGE:", json.dumps(resp.get("usage")))
