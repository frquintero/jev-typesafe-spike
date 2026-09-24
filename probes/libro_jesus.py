"""Libro antiguo: 'Jesús murió crucificado' (hecho con fuerte presencia notoria). 3 réplicas.
Crudos: cache/libro-jesus-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

body = {"model": MODEL,
        "state": "Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que Jesús murió crucificado.",
        "questions": {
            "libro_senalaba": {"type": "noul", "instructions": "Un libro antiguo señalaba que Jesús murió crucificado."}}}
for rep in (1, 2, 3):
    path = os.path.join(CACHE_DIR, f"libro-jesus-r{rep}.json")
    if not os.path.exists(path):
        resp, lat = jev_call(body)
        if resp.get("model") != MODEL:
            raise SystemExit(f"modelo inesperado: {resp.get('model')}")
        json.dump({"request": body, "response": resp,
                   "meta": {"latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}},
                  open(path, "w"), ensure_ascii=False)
        time.sleep(0.5)
print("ok")
