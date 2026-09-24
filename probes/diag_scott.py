"""Diagnóstico del caso Scott (c6-F): ¿falla la redacción o es rasgo de Jev?
Una pregunta por request, 3 réplicas por variante.
Crudos: cache/diag-scott-{a|b|c|d}-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

ES = {"nota": "Robert Scott fue la primera persona en llegar al Polo Sur. Su expedición avanzó con trineos tirados por perros."}
EN = {"note": "Robert Scott was the first person to reach the South Pole. His expedition advanced with dog-pulled sledges."}
VAR = {
    "a": (ES, "`nota` afirma que Robert Scott fue la primera persona en llegar al Polo Sur."),
    "b": (ES, "`nota` dice que Robert Scott fue la primera persona en llegar al Polo Sur."),
    "c": (ES, "Según `nota`, Robert Scott fue la primera persona en llegar al Polo Sur."),
    "d": (EN, "`note` states that Robert Scott was the first person to reach the South Pole."),
}
for v, (state, instr) in VAR.items():
    vals = []
    for rep in (1, 2, 3):
        path = os.path.join(CACHE_DIR, f"diag-scott-{v}-r{rep}.json")
        if os.path.exists(path):
            d = json.load(open(path))
        else:
            body = {"model": MODEL, "state": state,
                    "questions": {"q": {"type": "noul", "instructions": instr}}}
            resp, lat = jev_call(body)
            if resp.get("model") != MODEL:
                raise SystemExit(f"modelo inesperado: {resp.get('model')}")
            d = {"request": body, "response": resp,
                 "meta": {"variante": v, "latency_s": round(lat, 2),
                          "date": datetime.date.today().isoformat()}}
            json.dump(d, open(path, "w"), ensure_ascii=False)
            time.sleep(0.5)
        vals.append(d["response"]["answers"]["q"]["noul"])
    print(f"{v}: {vals}  | {instr}")
