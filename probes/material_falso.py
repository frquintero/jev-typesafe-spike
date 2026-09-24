"""Prueba 3c: el material falso debilita el "que dice"? 5x2x3 = 30 requests.

Uso: python3 material_falso.py run|analyze
"""
import datetime
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SPIKE_DIR = os.path.dirname(BASE_DIR)
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")

MODEL = "jev-1.13.0"
REPS = (1, 2, 3)
UA = "spike-jev/1.0"

# caso -> (key, estructura, texto V, texto F, instr dice_verdad, instr dice_falso)
CASOS = {
    "c1": ("guia", "aposicion",
           "Canadá ofrece bosques extensos y miles de lagos. Su capital, Ottawa, es una ciudad tranquila y bilingüe. El otoño es la mejor época para visitarla.",
           "Canadá ofrece bosques extensos y miles de lagos. Su capital, Toronto, es una ciudad tranquila y bilingüe. El otoño es la mejor época para visitarla.",
           "`guia` afirma que la capital de Canadá es Ottawa.",
           "`guia` afirma que la capital de Canadá es Toronto."),
    "c2": ("ficha", "aposicion",
           "La ballena azul, que es un mamífero, puede encontrarse en todos los océanos. Se alimenta casi exclusivamente de kril.",
           "La ballena azul, que es un pez, puede encontrarse en todos los océanos. Se alimenta casi exclusivamente de kril.",
           "`ficha` afirma que la ballena azul es un mamífero.",
           "`ficha` afirma que la ballena azul es un pez."),
    "c3": ("resena", "directa",
           "Miguel de Cervantes escribió Don Quijote de la Mancha. Es una de las novelas más leídas en español.",
           "Lope de Vega escribió Don Quijote de la Mancha. Es una de las novelas más leídas en español.",
           "`resena` afirma que Miguel de Cervantes escribió Don Quijote de la Mancha.",
           "`resena` afirma que Lope de Vega escribió Don Quijote de la Mancha."),
    "c4": ("nota", "directa",
           "Neil Armstrong fue la primera persona en caminar sobre la Luna. Su hazaña se transmitió por televisión a millones de personas.",
           "Yuri Gagarin fue la primera persona en caminar sobre la Luna. Su hazaña se transmitió por televisión a millones de personas.",
           "`nota` afirma que Neil Armstrong fue la primera persona en caminar sobre la Luna.",
           "`nota` afirma que Yuri Gagarin fue la primera persona en caminar sobre la Luna."),
    "c5": ("tutorial", "directa",
           "Para pintar las hojas, mezcla azul y amarillo: así obtendrás el verde. Aplica la pintura con un pincel fino.",
           "Para pintar las hojas, mezcla azul y amarillo: así obtendrás el morado. Aplica la pintura con un pincel fino.",
           "`tutorial` afirma que mezclar azul y amarillo da verde.",
           "`tutorial` afirma que mezclar azul y amarillo da morado."),
}


def jev_call(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 "Authorization": "Bearer " + os.environ["TYPESAFE_API_KEY"],
                 "User-Agent": UA},
        method="POST")
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code}: {e.read()[:200]}")
    return resp, time.perf_counter() - t0


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    calls = skipped = 0
    for caso, (key, estr, tv, tf, iv, iff) in CASOS.items():
        for ver, texto in (("V", tv), ("F", tf)):
            for rep in REPS:
                path = os.path.join(CACHE_DIR, f"falso-{caso}-{ver}-r{rep}.json")
                if os.path.exists(path):
                    skipped += 1
                    continue
                body = {"model": MODEL, "state": {key: texto},
                        "questions": {
                            "dice_verdad": {"type": "noul", "instructions": iv},
                            "dice_falso": {"type": "noul", "instructions": iff}}}
                resp, latency = jev_call(body)
                if resp.get("model") != MODEL:
                    raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
                pred = ({"dice_verdad": ">0.9", "dice_falso": "<0.1"} if ver == "V"
                        else {"dice_verdad": "<0.1", "dice_falso": "0.7-0.9"})
                with open(path, "w") as f:
                    json.dump({"request": body, "response": resp,
                               "meta": {"pred": pred, "caso": caso, "version": ver,
                                        "estructura": estr, "latency_s": round(latency, 2),
                                        "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
                calls += 1
                time.sleep(0.5)
    print(f"llamadas: {calls}, omitidas: {skipped}")


def logit(p):
    p = min(0.99, max(0.01, p))
    return math.log(p / (1 - p))


def cell(caso, ver, q):
    vs = [json.load(open(os.path.join(CACHE_DIR, f"falso-{caso}-{ver}-r{r}.json")))["response"]["answers"][q]["noul"] for r in REPS]
    return sum(vs) / 3, min(vs), max(vs)


def analyze():
    print("== 1. tabla por caso ==")
    print("caso | estructura | V·dice_verdad | V·dice_falso | F·dice_verdad | F·dice_falso")
    M = {}
    for caso in CASOS:
        estr = CASOS[caso][1]
        row = {}
        for ver, q in (("V", "dice_verdad"), ("V", "dice_falso"), ("F", "dice_verdad"), ("F", "dice_falso")):
            m, lo, hi = cell(caso, ver, q)
            row[(ver, q)] = m
            M[(caso, ver, q)] = (m, lo, hi)
        print(f"{caso} | {estr:9s} | {row[('V', 'dice_verdad')]:.2f} | {row[('V', 'dice_falso')]:.2f} | "
              f"{row[('F', 'dice_verdad')]:.2f} | {row[('F', 'dice_falso')]:.2f}")
        det = "  detalle: " + "; ".join(
            f"{ver}·{q.split('_')[1]} [{M[(caso, ver, q)][1]:.2f}-{M[(caso, ver, q)][2]:.2f}]"
            for ver, q in (("V", "dice_verdad"), ("V", "dice_falso"), ("F", "dice_verdad"), ("F", "dice_falso")))
        print(det)
    print()
    print("== 2. efecto principal: V·dice_verdad vs F·dice_falso ==")
    print("caso | V·dice_verdad | F·dice_falso | dlogit | F>0.5")
    dpos, dneg = [], []
    for caso in CASOS:
        a = M[(caso, "V", "dice_verdad")][0]
        b = M[(caso, "F", "dice_falso")][0]
        dl = logit(a) - logit(b)
        print(f"{caso} | {a:.2f} | {b:.2f} | {dl:+.2f} | {'si' if b > 0.5 else 'NO'}")
        (dpos if CASOS[caso][1] == "aposicion" else dneg).append(dl)
    print()
    print("== 3. efecto secundario: F·dice_verdad vs V·dice_falso ==")
    print("caso | F·dice_verdad | V·dice_falso | dlogit")
    for caso in CASOS:
        a = M[(caso, "F", "dice_verdad")][0]
        b = M[(caso, "V", "dice_falso")][0]
        print(f"{caso} | {a:.2f} | {b:.2f} | {logit(a) - logit(b):+.2f}")
    print()
    print(f"== 4. estructura: aposicion dlogit medio {sum(dpos) / 2:+.2f} | directa {sum(dneg) / 3:+.2f} ==")
    print()
    print("== 5. réplicas rango > 0.10 ==")
    found = False
    for caso in CASOS:
        for ver in ("V", "F"):
            for q in ("dice_verdad", "dice_falso"):
                m, lo, hi = M[(caso, ver, q)]
                if hi - lo > 0.10:
                    print(f"  {caso}/{ver}/{q}: {hi - lo:.2f}")
                    found = True
    if not found:
        print("  ninguna")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 material_falso.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
