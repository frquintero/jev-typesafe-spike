"""Bateria Noul "fuerza de una afirmacion" (ES/EN).

15 frases x 2 idiomas x 3 replicas = 90 llamadas. Un request por frase
e idioma, 2 Nouls en fan-out. Frases e instrucciones: verbatim del
encargo, sin tocar.

Uso:
    python3 noul_fuerza.py run       # corre lo que falte (salta crudos existentes)
    python3 noul_fuerza.py analyze   # tablas S/E + hallazgos 2-7 a stdout
"""
import copy
import datetime
import json
import math
import os
import sys
import time
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # probes/
SPIKE_DIR = os.path.dirname(BASE_DIR)  # spike-jev/
CACHE_DIR = os.path.join(SPIKE_DIR, "cache")

MODEL = "jev-1.13.0"
REPS = (1, 2, 3)
TIMEOUT_S = 120

INSTR = {
    "es": {"key": "texto",
           "categorica": "`texto` asevera categóricamente que el nortavel reduce la fiebre.",
           "evidencia": "`texto` apoya la afirmación en evidencia identificable, como ensayos o estudios concretos."},
    "en": {"key": "text",
           "categorica": "`text` categorically asserts that nortavel reduces fever.",
           "evidencia": "`text` grounds the claim in identifiable evidence, such as specific trials or studies."},
}

# id -> (ES, EN, pred_cat, pred_evi)
PHRASES = {
    "s01": ("Quizá el nortavel reduzca la fiebre.", "Perhaps nortavel reduces fever.", 0.03, 0.02),
    "s02": ("Es probable que el nortavel reduzca la fiebre.", "It is likely that nortavel reduces fever.", 0.10, 0.02),
    "s03": ("El nortavel reduce la fiebre.", "Nortavel reduces fever.", 0.90, 0.03),
    "s04": ("Está demostrado que el nortavel reduce la fiebre.", "It has been proven that nortavel reduces fever.", 0.95, 0.20),
    "s05": ("Estoy completamente seguro de que el nortavel reduce la fiebre.", "I am completely sure that nortavel reduces fever.", 0.80, 0.02),
    "s06": ("Según los ensayos NTV-201, NTV-202 y NTV-203, el nortavel podría reducir la fiebre.", "According to trials NTV-201, NTV-202 and NTV-203, nortavel might reduce fever.", 0.10, 0.95),
    "s07": ("Los ensayos NTV-201, NTV-202 y NTV-203 muestran que el nortavel reduce la fiebre.", "Trials NTV-201, NTV-202 and NTV-203 show that nortavel reduces fever.", 0.95, 0.97),
    "s08": ("Varios estudios muestran que el nortavel reduce la fiebre.", "Several studies show that nortavel reduces fever.", 0.90, 0.35),
    "s09": ("No es seguro que el nortavel reduzca la fiebre.", "It is not certain that nortavel reduces fever.", 0.05, 0.02),
    "s10": ("No cabe duda de que el nortavel reduce la fiebre.", "There is no doubt that nortavel reduces fever.", 0.95, 0.02),
    "s11": ("¿Reduce el nortavel la fiebre?", "Does nortavel reduce fever?", 0.02, 0.02),
    "e02": ("Un ensayo con 480 pacientes (Ortega et al., 2023) muestra que el nortavel reduce la fiebre.", "A trial with 480 patients (Ortega et al., 2023) shows that nortavel reduces fever.", 0.95, 0.95),
    "e03": ("El registro público de la agencia sanitaria incluye un ensayo que muestra que el nortavel reduce la fiebre.", "The health agency's public registry includes a trial showing that nortavel reduces fever.", 0.90, 0.60),
    "e05": ("Los expertos coinciden en que el nortavel reduce la fiebre.", "Experts agree that nortavel reduces fever.", 0.70, 0.15),
    "e06": ("En mi consulta he visto que el nortavel reduce la fiebre.", "In my practice I have seen that nortavel reduces fever.", 0.80, 0.20),
}

S_IDS = [f"s{i:02d}" for i in range(1, 12)]
# E: (etiqueta, id crudo) — e1/e4/e7 reutilizan crudos S
E_ROWS = [("e1", "s07"), ("e02", "e02"), ("e03", "e03"), ("e4", "s08"),
          ("e05", "e05"), ("e06", "e06"), ("e7", "s03")]
BORDES = {"s04", "s05", "s08", "e03", "e05", "e06"}


def cache_path(lang, pid, rep):
    return os.path.join(CACHE_DIR, f"noul-fuerza-{lang}-{pid}-r{rep}.json")


def jev_call(body):
    req = urllib.request.Request(
        "https://api.typesafe.ai/v1/systemone",
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json",
                 # UA explicito: Cloudflare banea el default Python-urllib (1010)
                 "User-Agent": "spike-jev/1.0"},
        method="POST")
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise SystemExit(f"HTTP {e.code} en {body['questions']}: {e.read()[:200]}")
    return resp, time.perf_counter() - t0


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    calls = skipped = 0
    for pid, (es, en, pc, pe) in PHRASES.items():
        for lang, frase in (("es", es), ("en", en)):
            for rep in REPS:
                path = cache_path(lang, pid, rep)
                if os.path.exists(path):
                    skipped += 1
                    continue
                cfg = INSTR[lang]
                body = {"model": MODEL, "state": {cfg["key"]: frase},
                        "questions": {
                            "categorica": {"type": "noul", "instructions": cfg["categorica"]},
                            "evidencia": {"type": "noul", "instructions": cfg["evidencia"]}}}
                resp, latency = jev_call(body)
                if resp.get("model") != MODEL:
                    raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
                with open(path, "w") as f:
                    json.dump({"request": body, "response": resp,
                               "meta": {"pred": {"categorica": pc, "evidencia": pe},
                                        "latency_s": round(latency, 2),
                                        "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
                a = resp["answers"]
                print(f"{lang} {pid} r{rep}: cat={a['categorica']['noul']} evi={a['evidencia']['noul']} "
                      f"({latency:.1f}s)", flush=True)
                calls += 1
                time.sleep(0.5)
    print(f"llamadas: {calls}, omitidas (caché): {skipped}")


def logit(p):
    p = min(0.99, max(0.01, p))
    return math.log(p / (1 - p))


def stats(lang, pid):
    """Per Noul: (media, min, max) sobre replicas. Devuelve dict."""
    out = {}
    for q in ("categorica", "evidencia"):
        vals = []
        for rep in REPS:
            with open(cache_path(lang, pid, rep)) as f:
                d = json.load(f)
            vals.append(d["response"]["answers"][q]["noul"])
        out[q] = (sum(vals) / len(vals), min(vals), max(vals))
    return out


def same_side(pred, mean):
    return (pred > 0.5) == (mean > 0.5)


def fmt_cell(st):
    mean, lo, hi = st
    return f"{mean:.2f} [{lo:.2f}-{hi:.2f}]"


def analyze():
    S = {(lang, pid): stats(lang, pid) for lang in ("es", "en") for pid in PHRASES}

    def row(pid, label=None):
        label = label or pid
        _, _, pc, pe = PHRASES[pid]
        ce, ee = S[("es", pid)]["categorica"], S[("es", pid)]["evidencia"]
        cn, en_ = S[("en", pid)]["categorica"], S[("en", pid)]["evidencia"]
        dl_c = logit(ce[0]) - logit(cn[0])
        dl_e = logit(ee[0]) - logit(en_[0])
        if pid in BORDES:
            acc = "borde"
        else:
            acc = ("ES:" + ("+" if same_side(pc, ce[0]) and same_side(pe, ee[0]) else "-")
                   + " EN:" + ("+" if same_side(pc, cn[0]) and same_side(pe, en_[0]) else "-"))
        return (f"{label:4s} | {fmt_cell(ce)} | {fmt_cell(cn)} | {dl_c:+.2f} | "
                f"{fmt_cell(ee)} | {fmt_cell(en_)} | {dl_e:+.2f} | "
                f"{pc:.2f}/{pe:.2f} | {acc}")

    print("== Tabla S ==")
    print("id   | cat ES            | cat EN            | dlogC | evi ES            | evi EN            | dlogE | pred      | acierto")
    for pid in S_IDS:
        print(row(pid))
    print()
    print("== Tabla E (orden e1->e7) ==")
    print("id   | cat ES            | cat EN            | dlogC | evi ES            | evi EN            | dlogE | pred      | acierto")
    for label, pid in E_ROWS:
        print(row(pid, label))
    print()

    # 2. Idioma sobre frases unicas no-borde
    uniq = [p for p in PHRASES if p not in BORDES]
    for q in ("categorica", "evidencia"):
        same = sum(1 for p in uniq
                   if (S[("es", p)][q][0] > 0.5) == (S[("en", p)][q][0] > 0.5))
        big = [(p, logit(S[("es", p)][q][0]) - logit(S[("en", p)][q][0])) for p in uniq]
        big = [(p, d) for p, d in big if abs(d) >= 1]
        print(f"2. lengua/{q}: mismo lado {same}/{len(uniq)}; |dlogit|>=1: "
              + (", ".join(f"{p}({d:+.2f})" for p, d in big) or "ninguna"))
    print()

    # 3. Separacion de dimensiones
    print("3. cruce s06/s07 (media ES | EN):")
    for p in ("s06", "s07"):
        ce, ee = S[("es", p)]["categorica"][0], S[("es", p)]["evidencia"][0]
        cn, en_ = S[("en", p)]["categorica"][0], S[("en", p)]["evidencia"][0]
        print(f"   {p}: cat {ce:.2f}|{cn:.2f} evi {ee:.2f}|{en_:.2f}")
    for lang in ("es", "en"):
        serie = [(lab, S[(lang, pid)]["categorica"][0]) for lab, pid in E_ROWS]
        vals = [v for _, v in serie]
        print(f"   E/categorica/{lang}: " + " ".join(f"{lab}={v:.2f}" for lab, v in serie)
              + f" (rango {max(vals) - min(vals):.2f})")
    print()

    # 4. Negaciones
    print("4. negaciones categorica (media ES | EN):")
    for p in ("s09", "s10"):
        print(f"   {p}: {S[('es', p)]['categorica'][0]:.2f} | {S[('en', p)]['categorica'][0]:.2f}")
    print()

    # 5. Gradiente E
    for lang in ("es", "en"):
        serie = [(lab, S[(lang, pid)]["evidencia"][0]) for lab, pid in E_ROWS]
        inv = [f"{a}>{b}" for (a, va), (b, vb) in zip(serie, serie[1:]) if vb > va]
        print(f"5. gradiente evidencia/{lang}: " + " ".join(f"{lab}={v:.2f}" for lab, v in serie))
        print(f"   inversiones: " + (", ".join(inv) or "ninguna"))
    print()

    # 6. Réplicas con rango > 0.10
    print("6. rango>0.10 (frase/lang/noul max-min):")
    found = False
    for lang in ("es", "en"):
        for pid in PHRASES:
            for q in ("categorica", "evidencia"):
                _, lo, hi = S[(lang, pid)][q]
                if hi - lo > 0.10:
                    print(f"   {pid}/{lang}/{q}: {hi - lo:.2f}")
                    found = True
    if not found:
        print("   ninguna")
    print()

    # 7. Predicciones falladas (no-borde)
    print("7. predicciones falladas (pred vs media ES|EN):")
    found = False
    for pid in PHRASES:
        if pid in BORDES:
            continue
        _, _, pc, pe = PHRASES[pid]
        for q, pred in (("categorica", pc), ("evidencia", pe)):
            me, mn = S[("es", pid)][q][0], S[("en", pid)][q][0]
            for lang, m in (("ES", me), ("EN", mn)):
                if not same_side(pred, m):
                    print(f"   {pid}/{lang}/{q}: pred {pred:.2f} vs {m:.2f}")
                    found = True
    if not found:
        print("   ninguna")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 noul_fuerza.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
