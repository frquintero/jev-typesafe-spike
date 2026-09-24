"""Caso similar a c4 (Prueba 3c): Amundsen/Scott, Polo Sur. 2 versiones x 3 réplicas.
Crudos: cache/falso-c6-{V|F}-r{1..3}.json
"""
import datetime, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from material_falso import CACHE_DIR, MODEL, jev_call

KEY = "nota"
V = "Roald Amundsen fue la primera persona en llegar al Polo Sur. Su expedición avanzó con trineos tirados por perros."
F = "Robert Scott fue la primera persona en llegar al Polo Sur. Su expedición avanzó con trineos tirados por perros."
IV = "`nota` afirma que Roald Amundsen fue la primera persona en llegar al Polo Sur."
IF = "`nota` afirma que Robert Scott fue la primera persona en llegar al Polo Sur."

for ver, texto in (("V", V), ("F", F)):
    out = []
    for rep in (1, 2, 3):
        path = os.path.join(CACHE_DIR, f"falso-c6-{ver}-r{rep}.json")
        if os.path.exists(path):
            d = json.load(open(path))
        else:
            body = {"model": MODEL, "state": {KEY: texto},
                    "questions": {"dice_verdad": {"type": "noul", "instructions": IV},
                                  "dice_falso": {"type": "noul", "instructions": IF}}}
            resp, lat = jev_call(body)
            if resp.get("model") != MODEL:
                raise SystemExit(f"modelo inesperado: {resp.get('model')}")
            d = {"request": body, "response": resp,
                 "meta": {"caso": "c6", "version": ver, "latency_s": round(lat, 2),
                          "date": datetime.date.today().isoformat()}}
            json.dump(d, open(path, "w"), ensure_ascii=False)
            time.sleep(0.5)
        a = d["response"]["answers"]
        out.append((a["dice_verdad"]["noul"], a["dice_falso"]["noul"]))
    print(f"c6 {ver}  dice_verdad={[x[0] for x in out]}  dice_falso={[x[1] for x in out]}")
