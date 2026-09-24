"""2+2=5 con verbos de reporte vs aseveración. 3 réplicas.
Crudos: cache/diag-2mas2-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

body = {"model": MODEL, "state": {"texto": "2+2=5"},
        "questions": {
            "afirma": {"type": "noul", "instructions": "`texto` afirma que 2+2=5."},
            "dice": {"type": "noul", "instructions": "`texto` dice que 2+2=5."}}}
res = {"afirma": [], "dice": []}
for rep in (1, 2, 3):
    path = os.path.join(CACHE_DIR, f"diag-2mas2-r{rep}.json")
    if os.path.exists(path):
        d = json.load(open(path))
    else:
        resp, lat = jev_call(body)
        if resp.get("model") != MODEL:
            raise SystemExit(f"modelo inesperado: {resp.get('model')}")
        d = {"request": body, "response": resp,
             "meta": {"latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}}
        json.dump(d, open(path, "w"), ensure_ascii=False)
        time.sleep(0.5)
    for k in res:
        res[k].append(d["response"]["answers"][k]["noul"])
for k, v in res.items():
    print(k, v)
