"""Gagarin como estado de las cosas (sin segundo detalle) + juicio "Decimos que...".
Control: "`nota` afirma que..." sobre el mismo expediente. 3 réplicas.
Crudos: cache/decimos-gagarin-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

body = {"model": MODEL,
        "state": {"nota": "Yuri Gagarin fue la primera persona en caminar sobre la Luna."},
        "questions": {
            "decimos": {"type": "noul", "instructions": "Decimos que Yuri Gagarin fue la primera persona en caminar sobre la Luna."},
            "nota_afirma": {"type": "noul", "instructions": "`nota` afirma que Yuri Gagarin fue la primera persona en caminar sobre la Luna."}}}
res = {"decimos": [], "nota_afirma": []}
for rep in (1, 2, 3):
    path = os.path.join(CACHE_DIR, f"decimos-gagarin-r{rep}.json")
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
