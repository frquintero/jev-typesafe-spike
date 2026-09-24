"""Revisión: Noul suelto (una pregunta por request) a 140 y 200, 3 reps — contra el fan-out."""
import json
import os
import urllib.request

TEXTO = (
    "The sample mean converges toward the expectation as the number of "
    "independent observations grows. That convergence, known as the law "
    "of large numbers, sustains much of the modern statistical inference "
    "and the analysis of experimental data."
)
assert sum(c.isalpha() for c in TEXTO) == 200


def llamar(x):
    body = {
        "model": "jev-latest",
        "state": TEXTO,
        "questions": {
            "q1": {"type": "noul", "instructions": f"has more than {x} letters"}
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
        return body, json.loads(r.read().decode())


os.makedirs("spike-jev/cache", exist_ok=True)
for x in (140, 200):
    vals = []
    for rep in range(1, 4):
        body, resp = llamar(x)
        with open(f"spike-jev/cache/tamano-200-noul-single-{x}-r{rep}.json", "w") as f:
            json.dump({"request": body, "response": resp}, f, ensure_ascii=False)
        vals.append(resp["answers"]["q1"]["noul"])
    print(f"single >{x} reps: {vals}  media={sum(vals)/len(vals):.3f}")

print("fan-out >140: [0.76, 0.70, 0.77] media=0.743")
print("fan-out >200: [0.43, 0.38, 0.40] media=0.403")
