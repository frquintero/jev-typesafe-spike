"""Prueba 1: (a) urgencia ES vs EN (8 msgs x 3) + (b) fuerza ES (15 frases x 3).

69 llamadas. Textos verbatim del encargo. Uso:
    python3 score_prueba1.py run       # corre lo que falte
    python3 score_prueba1.py analyze   # tablas (a)+(b) a stdout
"""
import datetime
import json
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

Q_URG = {
    "horizonte": {
        "type": "score",
        "instructions": "¿Qué tan pronto espera el remitente de `mensaje` una acción, según lo que el mensaje dice o da a entender?",
        "criteria": [
            {"what": "Sin expectativa de tiempo: el mensaje dice o da a entender que puede atenderse cuando sea.",
             "examples": ["Para tus archivos, no hace falta nada.", "Tómate tu tiempo con esto."]},
            {"what": "Espera respuesta, sin plazo: el remitente pregunta cómo va algo o dice que alguien espera, pero no da una fecha límite ni señal de que se necesite hoy.",
             "examples": ["¿Hay noticias del borrador?", "Nuestro socio volvió a preguntarme por esto."]},
            {"what": "En los próximos días: el remitente espera una acción en los próximos días, por ejemplo esta semana.",
             "examples": ["¿Podrías revisarlo antes del viernes?", "En algún momento de esta semana estaría bien."]},
            {"what": "Hoy: se afirma o se da a entender claramente un plazo para el mismo día.",
             "examples": ["Necesito tus comentarios antes de que termine el día.", "¿Podemos cerrar esto hoy?"]},
            {"what": "De inmediato: el remitente necesita una acción ahora mismo.",
             "examples": ["Llámame en cuanto leas esto.", "Necesito esto en este mismo minuto."]},
        ]},
    "costo": {
        "type": "score",
        "instructions": "¿Qué consecuencia de la demora afirma o da a entender `mensaje`?",
        "criteria": [
            {"what": "La demora solo afecta al remitente: es él quien espera una respuesta.",
             "examples": ["¿Qué opinas de mi propuesta?", "Aquí está el archivo para tus registros."]},
            {"what": "La demora alcanza a alguien más allá del remitente: un cliente, un colega, un equipo o un proceso espera esto o está detenido por ello.",
             "examples": ["Mi gerente no deja de preguntarme por esto.", "Contabilidad no puede cerrar el mes sin tu firma."]},
            {"what": "Se afirma una pérdida concreta e inmediata.",
             "examples": ["Perdemos el contrato si esto no se firma ahora.", "A los clientes se les está cobrando dos veces."]},
        ]},
}

# id -> (mensaje ES, pred_horizonte, pred_costo)
MSGS_A = {
    "h1": ("Oye, ¿alguna novedad sobre el archivo del presupuesto?", 1, 0),
    "h2": ("Mi jefe me volvió a preguntar por el informe.", 1, 1),
    "h3": ("Jurídica no puede enviar el contrato hasta que apruebes el borrador.", 1, 1),
    "h4": ("Por favor, envíalo a más tardar el jueves.", 2, 0),
    "h5": ("El lanzamiento es el lunes y tu sección todavía no está.", 2, 1),
    "h6": ("Si no le pagamos hoy al proveedor, cancela el pedido.", 3, 2),
    "h7": ("Cuando puedas, sin presión.", 0, 0),
    "h8": ("El cliente está esperando la cotización.", 1, 1),
}

Q_FUERZA = {
    "certeza": {
        "type": "score",
        "instructions": "¿Con qué fuerza presenta `texto` la afirmación de que el nortavel reduce la fiebre, venga de quien venga la afirmación?",
        "criteria": [
            {"what": "No afirma: el texto pregunta o menciona la idea sin tomar posición.",
             "examples": ["¿Soportará el puente la carga?", "Se discute si el puente soportará la carga."]},
            {"what": "Posible o dudosa: presenta la afirmación como una posibilidad o como algo incierto.",
             "examples": ["Tal vez el puente soporte la carga.", "Puede que el puente aguante."]},
            {"what": "Probable: presenta la afirmación como más cerca del sí que del no.",
             "examples": ["Seguramente el puente soportará la carga.", "Lo más esperable es que el puente aguante."]},
            {"what": "Firme: presenta la afirmación como un hecho, incluso si la atribuye a otra fuente.",
             "examples": ["El puente soporta la carga.", "Según la constructora, el puente soporta la carga."]},
            {"what": "Enfática: presenta la afirmación como un hecho y refuerza expresamente su certeza.",
             "examples": ["Es un hecho indiscutible que el puente soporta la carga.", "Queda plenamente confirmado que el puente aguanta."]},
        ]},
    "verificabilidad": {
        "type": "score",
        "instructions": "¿Qué tan verificable es el apoyo que `texto` ofrece para su afirmación?",
        "criteria": [
            {"what": "Sin apoyo: la afirmación aparece sola, sin fuente ni razón.",
             "examples": ["El puente aguanta.", "Tal vez el puente aguante."]},
            {"what": "Autoridad o experiencia: se invoca a especialistas, a la opinión general o a la experiencia propia, sin nada que otro pueda revisar.",
             "examples": ["Los ingenieros de la zona dicen que el puente aguanta.", "Llevo veinte años cruzándolo y nunca ha fallado."]},
            {"what": "Evidencia vaga: se alude a pruebas, informes o comprobaciones que existirían, pero sin decir cuáles.",
             "examples": ["Hay informes técnicos que lo confirman.", "Se ha comprobado que el puente aguanta."]},
            {"what": "Fuente localizable: se nombra una fuente concreta que otra persona podría encontrar y revisar.",
             "examples": ["El informe anual del Instituto Vial sobre este puente confirma que soporta la carga.", "La prueba de carga registrada como PC-14 lo confirma."]},
        ]},
}

# id -> (frase, pred_certeza, pred_verificab, borde_cer, borde_ver)
PHRASES_B = {
    "s01": ("Quizá el nortavel reduzca la fiebre.", 1, 0, False, False),
    "s02": ("Es probable que el nortavel reduzca la fiebre.", 2, 0, False, False),
    "s03": ("El nortavel reduce la fiebre.", 3, 0, False, False),
    "s04": ("Está demostrado que el nortavel reduce la fiebre.", 4, 2, True, True),
    "s05": ("Estoy completamente seguro de que el nortavel reduce la fiebre.", 4, 0, False, False),
    "s06": ("Según los ensayos NTV-201, NTV-202 y NTV-203, el nortavel podría reducir la fiebre.", 1, 3, False, False),
    "s07": ("Los ensayos NTV-201, NTV-202 y NTV-203 muestran que el nortavel reduce la fiebre.", 3, 3, False, False),
    "s08": ("Varios estudios muestran que el nortavel reduce la fiebre.", 3, 2, False, False),
    "s09": ("No es seguro que el nortavel reduzca la fiebre.", 1, 0, True, False),
    "s10": ("No cabe duda de que el nortavel reduce la fiebre.", 4, 0, False, False),
    "s11": ("¿Reduce el nortavel la fiebre?", 0, 0, False, False),
    "e02": ("Un ensayo con 480 pacientes (Ortega et al., 2023) muestra que el nortavel reduce la fiebre.", 3, 3, False, False),
    "e03": ("El registro público de la agencia sanitaria incluye un ensayo que muestra que el nortavel reduce la fiebre.", 3, 3, False, True),
    "e05": ("Los expertos coinciden en que el nortavel reduce la fiebre.", 3, 1, True, False),
    "e06": ("En mi consulta he visto que el nortavel reduce la fiebre.", 3, 1, False, False),
}
B_IDS = ["s01", "s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "s11",
         "e02", "e03", "e05", "e06"]


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


def one_call(path, body, meta_pred):
    if os.path.exists(path):
        return False
    resp, latency = jev_call(body)
    if resp.get("model") != MODEL:
        raise SystemExit(f"modelo inesperado en {path}: {resp.get('model')}")
    with open(path, "w") as f:
        json.dump({"request": body, "response": resp,
                   "meta": {"pred": meta_pred, "latency_s": round(latency, 2),
                            "date": datetime.date.today().isoformat()}}, f, ensure_ascii=False)
    time.sleep(0.5)
    return True


def run():
    os.makedirs(CACHE_DIR, exist_ok=True)
    calls = skipped = 0
    for hid, (msg, ph, pc) in MSGS_A.items():
        for rep in REPS:
            body = {"model": MODEL, "state": {"mensaje": msg}, "questions": Q_URG}
            if one_call(os.path.join(CACHE_DIR, f"score-urg-es-{hid}-r{rep}.json"),
                        body, {"horizonte": ph, "costo": pc}):
                calls += 1
            else:
                skipped += 1
    for pid, (frase, pc, pv, _, _) in PHRASES_B.items():
        for rep in REPS:
            body = {"model": MODEL, "state": {"texto": frase}, "questions": Q_FUERZA}
            if one_call(os.path.join(CACHE_DIR, f"score-fuerza-es-{pid}-r{rep}.json"),
                        body, {"certeza": pc, "verificabilidad": pv}):
                calls += 1
            else:
                skipped += 1
    print(f"llamadas: {calls}, omitidas: {skipped}")


def load_score(path, q):
    with open(path) as f:
        a = json.load(f)["response"]["answers"][q]
    return a["score"], a["confidence"], {int(k): v for k, v in a["probabilities"].items()}


def agg_score(paths, q):
    """Media score, media conf, probs medias, pico, rango scores."""
    ss, cc, pp = [], [], []
    for p in paths:
        s, c, pr = load_score(p, q)
        ss.append(s)
        cc.append(c)
        pp.append(pr)
    levels = sorted(pp[0])
    meanp = {lv: sum(pr[lv] for pr in pp) / len(pp) for lv in levels}
    peak = max(levels, key=lambda lv: meanp[lv])
    return (sum(ss) / len(ss), sum(cc) / len(cc), meanp, peak, max(ss) - min(ss))


def analyze():
    print("== (a) urgencia ES vs EN ==")
    print("id | pico ES(H/C) | pico EN(H/C) | score ES | score EN | conf ES | conf EN | mismo pico | pred")
    match_h = match_c = 0
    for hid, (_, ph, pc) in MSGS_A.items():
        es_p = [os.path.join(CACHE_DIR, f"score-urg-es-{hid}-r{r}.json") for r in REPS]
        en_p = [os.path.join(CACHE_DIR, f"urg-holdout-{hid}-r{r}.json") for r in REPS]
        h_es = agg_score(es_p, "horizonte")
        c_es = agg_score(es_p, "costo")
        h_en = agg_score(en_p, "horizonte")
        c_en = agg_score(en_p, "costo")
        mh, mc = h_es[3] == h_en[3], c_es[3] == c_en[3]
        match_h += mh
        match_c += mc
        print(f"{hid} | {h_es[3]}/{c_es[3]} | {h_en[3]}/{c_en[3]} | "
              f"{h_es[0]:.2f}/{c_es[0]:.2f} | {h_en[0]:.2f}/{c_en[0]:.2f} | "
              f"{h_es[1]:.2f}/{c_es[1]:.2f} | {h_en[1]:.2f}/{c_en[1]:.2f} | "
              f"H:{'=' if mh else 'X'} C:{'=' if mc else 'X'} | {ph}/{pc}")
    print(f"mismo pico: horizonte {match_h}/8, costo {match_c}/8")
    print()
    print("== (b) fuerza ES ==")
    print("id  | probs medias | score | conf | pico | pred | acierto | borde")
    hit_c = tot_c = hit_v = tot_v = 0
    lowconf, bimodal, rangelist = [], [], []
    for pid in B_IDS:
        _, pc, pv, bc, bv = PHRASES_B[pid]
        paths = [os.path.join(CACHE_DIR, f"score-fuerza-es-{pid}-r{r}.json") for r in REPS]
        for q, pred, isb in (("certeza", pc, bc), ("verificabilidad", pv, bv)):
            s, c, mp, peak, rng = agg_score(paths, q)
            probs = " ".join(f"{lv}:{mp[lv]:.2f}" for lv in sorted(mp))
            acc = "borde" if isb else ("+" if peak == pred else "-")
            if not isb:
                if q == "certeza":
                    tot_c += 1
                    hit_c += peak == pred
                else:
                    tot_v += 1
                    hit_v += peak == pred
            bmark = "C" if (isb and q == "certeza") else ("V" if isb else "")
            if q == "certeza":
                brow = "C" if bc else ""
                brow += "V" if bv else ""
            else:
                brow = ""
            print(f"{pid}/{q[:4]} | {probs} | {s:.2f} | {c:.2f} | {peak} | {pred} | {acc} | {brow or bmark}")
            if c < 0.7:
                lowconf.append(f"{pid}/{q[:4]} ({c:.2f}){' borde' if isb else ''}")
            lvls = sorted(mp)
            for i, a in enumerate(lvls):
                for b in lvls[i + 2:]:
                    if mp[a] >= 0.2 and mp[b] >= 0.2:
                        bimodal.append(f"{pid}/{q[:4]} {a}/{b}")
            if rng > 0.3:
                rangelist.append(f"{pid}/{q[:4]} ({rng:.2f})")
    print(f"tasa acierto pico no-borde: certeza {hit_c}/{tot_c}, verificabilidad {hit_v}/{tot_v}")
    print(f"conf<0.7: " + (", ".join(lowconf) or "ninguna"))
    print(f"bimodales no-contiguas: " + (", ".join(bimodal) or "ninguna"))
    print(f"rango>0.3: " + (", ".join(rangelist) or "ninguna"))
    print()
    print("== (b5) Noul vs Score (medias ES) ==")
    print("id  | noul_cat | peak_cer | noul_evi | peak_ver | flag")
    for pid in B_IDS:
        ncat = sum(json.load(open(os.path.join(CACHE_DIR, f"noul-fuerza-es-{pid}-r{r}.json")))["response"]["answers"]["categorica"]["noul"] for r in REPS) / 3
        nevi = sum(json.load(open(os.path.join(CACHE_DIR, f"noul-fuerza-es-{pid}-r{r}.json")))["response"]["answers"]["evidencia"]["noul"] for r in REPS) / 3
        paths = [os.path.join(CACHE_DIR, f"score-fuerza-es-{pid}-r{r}.json") for r in REPS]
        _, _, _, pk_c, _ = agg_score(paths, "certeza")
        _, _, _, pk_v, _ = agg_score(paths, "verificabilidad")
        flags = []
        if (ncat > 0.8 and pk_c <= 1) or (ncat < 0.2 and pk_c >= 3):
            flags.append("cer!")
        if (nevi > 0.8 and pk_v <= 1) or (nevi < 0.2 and pk_v >= 2):
            flags.append("ver!")
        print(f"{pid} | {ncat:.2f} | {pk_c} | {nevi:.2f} | {pk_v} | {' '.join(flags)}")


def main(argv):
    if len(argv) != 2 or argv[1] not in ("run", "analyze"):
        raise SystemExit("uso: python3 score_prueba1.py run|analyze")
    {"run": run, "analyze": analyze}[argv[1]]()


if __name__ == "__main__":
    main(sys.argv)
