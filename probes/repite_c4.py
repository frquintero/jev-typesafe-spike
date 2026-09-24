"""Repite el caso c4 de la Prueba 3c (Gagarin/Armstrong) con 3 réplicas nuevas (r4..r6).

Mismo request exacto que material_falso.py; crudos nuevos en
cache/falso-c4-{V|F}-r{4..6}.json (no toca r1..r3).

Uso: python3 probes/repite_c4.py
     (requiere credencial API "Typesafe" del entorno cloud hacia api.typesafe.ai)
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CASOS, CACHE_DIR, MODEL, jev_call

key, estr, tv, tf, iv, iff = CASOS["c4"]
res = {}
for ver, texto in (("V", tv), ("F", tf)):
    for rep in (4, 5, 6):
        path = os.path.join(CACHE_DIR, f"falso-c4-{ver}-r{rep}.json")
        if os.path.exists(path):
            d = json.load(open(path))
        else:
            body = {"model": MODEL, "state": {key: texto},
                    "questions": {"dice_verdad": {"type": "noul", "instructions": iv},
                                  "dice_falso": {"type": "noul", "instructions": iff}}}
            resp, lat = jev_call(body)
            if resp.get("model") != MODEL:
                raise SystemExit(f"modelo inesperado: {resp.get('model')}")
            d = {"request": body, "response": resp,
                 "meta": {"caso": "c4", "version": ver, "repeticion": True,
                          "latency_s": round(lat, 2), "date": datetime.date.today().isoformat()}}
            json.dump(d, open(path, "w"), ensure_ascii=False)
            time.sleep(0.5)
        a = d["response"]["answers"]
        res.setdefault(ver, []).append((a["dice_verdad"]["noul"], a["dice_falso"]["noul"]))

for ver in ("V", "F"):
    old = [json.load(open(os.path.join(CACHE_DIR, f"falso-c4-{ver}-r{r}.json")))["response"]["answers"] for r in (1, 2, 3)]
    print(f"c4 {ver}  r1-3 dice_verdad={[o['dice_verdad']['noul'] for o in old]}  dice_falso={[o['dice_falso']['noul'] for o in old]}")
    print(f"c4 {ver}  r4-6 dice_verdad={[x[0] for x in res[ver]]}  dice_falso={[x[1] for x in res[ver]]}")
