"""¿Llegan las claves de pregunta al modelo? Mismo request de libro_jesus, solo cambia la clave.
Una clave por request, 3 réplicas. Crudos: cache/claves-jesus-{clave}-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

STATE = "Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que Jesús murió crucificado."
INSTR = "Un libro antiguo señalaba que Jesús murió crucificado."
for key in ("q1", "libro_senalaba", "falso"):
    vals = []
    for rep in (1, 2, 3):
        path = os.path.join(CACHE_DIR, f"claves-jesus-{key}-r{rep}.json")
        if os.path.exists(path):
            d = json.load(open(path))
        else:
            body = {"model": MODEL, "state": STATE,
                    "questions": {key: {"type": "noul", "instructions": INSTR}}}
            resp, lat = jev_call(body)
            if resp.get("model") != MODEL:
                raise SystemExit(f"modelo inesperado: {resp.get('model')}")
            d = {"request": body, "response": resp,
                 "meta": {"latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}}
            json.dump(d, open(path, "w"), ensure_ascii=False)
            time.sleep(0.5)
        vals.append(d["response"]["answers"][key]["noul"])
    print(key, vals)
