"""Choice Gagarin, "libro antiguo" -> "libro". Dos variantes: fue / no_fue. instructions vacío, clave q1.
3 réplicas. Crudos: cache/choice-gagarin-libro-{variante}-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

for var, verbo in (("fue", "fue"), ("no_fue", "no fue")):
    STATE = f"Un hombre encontró un libro que señalaba, entre otras cosas, que Yuri Gagarin {verbo} la primera persona en caminar sobre la Luna."
    CRITERIA = {"a": f"Un libro señalaba que Yuri Gagarin {verbo} la primera persona en caminar sobre la Luna.",
                "b": f"No hay evidencia de que un libro señalara que Yuri Gagarin {verbo} la primera persona en caminar sobre la Luna."}
    for rep in (1, 2, 3):
        path = os.path.join(CACHE_DIR, f"choice-gagarin-libro-{var}-r{rep}.json")
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
        print(var, rep, json.dumps(d["response"]["answers"]["q1"], ensure_ascii=False))
