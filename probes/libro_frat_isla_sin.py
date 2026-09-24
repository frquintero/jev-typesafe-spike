"""Frat e isla de los durmientes (hecho ficticio sin titular notorio): state como string (sin clave), juicio sin "El libro antiguo dice". 3 réplicas.
Crudos: cache/libro-frat-isla-sin-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

body = {"model": MODEL,
        "state": "Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que la verdad fue que Frat encontró la isla de los durmientes.",
        "questions": {
            "libro_dice": {"type": "noul", "instructions": "Frat encontró la isla de los durmientes."}}}
for rep in (1, 2, 3):
    path = os.path.join(CACHE_DIR, f"libro-frat-isla-sin-r{rep}.json")
    if not os.path.exists(path):
        resp, lat = jev_call(body)
        if resp.get("model") != MODEL:
            raise SystemExit(f"modelo inesperado: {resp.get('model')}")
        json.dump({"request": body, "response": resp,
                   "meta": {"latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}},
                  open(path, "w"), ensure_ascii=False)
        time.sleep(0.5)
print("ok")
