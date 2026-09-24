"""Spike: tabla 30 filas x 3 cols como array; un Choice de modalidad por celda."""
import json
import os
import urllib.request

NOMBRES = [
    "María Fernanda Ríos", "Carlos Andrés Mesa", "Lucía Herrera Pardo",
    "Jorge Enrique Salas", "Ana Sofía Vélez", "Pedro Nel Ospina",
    "Catalina Muñoz Díez", "Andrés Felipe Cano", "Rosa Elvira Pineda",
    "Miguel Ángel Soto", "Laura Camila Rojas", "Diego Fernando Gil",
    "Sofía Isabel Vargas", "Juan Pablo Londoño", "Elena Márquez Ruiz",
    "Óscar Iván Torres", "Natalia Duque Marín", "Felipe Santiago Cruz",
    "Adriana Lucía Parra", "Raúl Ernesto Cifuentes", "Paula Andrea Ríos",
    "Héctor Fabio León", "Daniela Restrepo Gil", "Emilio José Navarro",
    "Carmen Elisa Duarte", "Iván Darío Salazar", "Mónica Liliana Vega",
    "Santiago Arias Bello", "Gloria Inés Montoya", "Tomás Emilio Vargas",
]
EDADES = [34, 27, 45, 52, 31, 29, 38, 41, 26, 33, 47, 55, 24, 36, 43,
          30, 28, 49, 51, 39, 25, 44, 37, 32, 48, 56, 23, 35, 42, 40]
SEXOS = ["F", "M", "F", "M", "F", "M", "F", "M", "F", "M",
         "F", "M", "F", "M", "F", "M", "F", "M", "F", "M",
         "F", "M", "F", "M", "F", "M", "F", "M", "F", "M"]

tabla = [{"nombre": n, "edad": str(e), "sexo": s}
         for n, e, s in zip(NOMBRES, EDADES, SEXOS)]

CRITERIA = {
    "enunciativa": "Expresa una afirmación o negación completa, con predicado: algo que puede ser verdadero o falso",
    "interrogativa": "Formula una pregunta",
    "exclamativa": "Expresa emoción o énfasis con exclamación",
    "imperativa": "Da una orden, instrucción o ruego directo",
    "desiderativa": "Expresa un deseo",
    "dubitativa": "Expresa duda o posibilidad",
    "frase_nominal": "Solo nombra, sin afirmar nada: etiquetas, nombres propios, números o códigos aislados, cantidades con unidad, letras sueltas; sin predicado",
}

questions = {}
for i, fila in enumerate(tabla):
    for campo in ("nombre", "edad", "sexo"):
        qid = f"c{i:02d}_{campo}"
        questions[qid] = {
            "type": "choice",
            "instructions": f"Clasifica el texto en `tabla[{i}].{campo}` según su modalidad.",
            "criteria": CRITERIA,
        }

body = {"model": "jev-latest", "state": {"tabla": tabla}, "questions": questions}

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
with open("spike-jev/cache/tabla-30.json", "w") as f:
    json.dump({"request": body, "response": resp}, f, ensure_ascii=False)

ok, total, tibias = 0, 0, []
for i, fila in enumerate(tabla):
    for campo in ("nombre", "edad", "sexo"):
        a = resp["answers"][f"c{i:02d}_{campo}"]
        total += 1
        ok += a["choice"] == "frase_nominal"
        if a["choice"] != "frase_nominal" or a["confidence"] < 0.99:
            tibias.append((f"c{i:02d}_{campo}", repr(fila[campo]),
                            a["choice"], round(a["confidence"], 2),
                            {k: v for k, v in a["probabilities"].items()
                             if v > 0.01}))
print(f"FRASE_NOMINAL: {ok}/{total}")
print("No unánimes o no nominales:")
for t in tibias:
    print(" ", t)
print("USAGE:", json.dumps(resp.get("usage")))
