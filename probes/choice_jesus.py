"""Libro Jesús como Choice: criteria = [juicio del libro, "No hay evidencia."]; instructions vacío.
Claves neutras (q1, a, b). 3 réplicas. Crudos: cache/choice-jesus-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

STATE = "Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que Jesús murió crucificado."
CRITERIA = {"a": "Un libro antiguo señalaba que Jesús murió crucificado.",
            "b": "No hay evidencia."}
for rep in (1, 2, 3):
    path = os.path.join(CACHE_DIR, f"choice-jesus-r{rep}.json")
    if os.path.exists(path):
        d = json.load(open(path))
    else:
        body = {"model": MODEL, "state": STATE,
                "questions": {"q1": {"type": "choice", "instructions": "", "criteria": CRITERIA}}}
        resp, lat = jev_call(body)
        if resp.get("model") != MODEL:
            raise SystemExit(f"modelo inesperado: {resp.get('model')}")
        d = {"request": body, "response": resp,
             "meta": {"latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}}
        json.dump(d, open(path, "w"), ensure_ascii=False)
        time.sleep(0.5)
    print(rep, json.dumps(d["response"]["answers"]["q1"], ensure_ascii=False))
