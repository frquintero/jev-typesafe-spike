"""cutoff-spike Fase 2: analisis por capa (outcome vs scheduled).

Lee cache/cutoff-coarse.json + probes_coarse.json, une ground_truth +
fact_type + noul, e imprime a stdout sin intervencion manual:

  1. tabla trimestral por capa (solo ground_truth true): n, conoce, parcial, no
  2. falsos que rompen el umbral 0.3
  3. ventana candidata SOLO de outcomes
  4. anomalias de dominio (reglas, no hardcodeo de ids)

Umbrales del PLAN: conoce >= 0.8; parcial 0.5-0.8; no < 0.5;
falsos ok <= 0.3.

Decision documentada (ventana): la regla ">= 2/3" se agrega POR
TRIMESTRE (la rejilla del corpus), no por fecha suelta: con n=1 por
fecha la fraccion degenera a 0/100% y un solo probe ruidoso invierte
la ventana. T_lo = ultima event_date de outcomes-true del ultimo
trimestre con >= 2/3 conoce; T_hi = primera event_date del primer
trimestre con >= 2/3 no. Trimestres sin outcomes-true no cuentan.

Coarse v2: mismo analisis sobre probes_coarse_v2.json +
cache/cutoff-coarse-v2.json, mas delta v1->v2 emparejado por ref_v1
(medida de cuanto valio el sesgo de wording/IDs).

Uso: python3 analyze.py [v1|v2|delta|all]  (default v1)
Solo stdlib. No llama a Jev.
"""
import json
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # cutoff-spike/
SPIKE_DIR = os.path.dirname(BASE_DIR)  # spike-jev/
V1_CACHE = os.path.join(SPIKE_DIR, "cache", "cutoff-coarse.json")
V1_PROBES = os.path.join(BASE_DIR, "probes_coarse.json")
V2_CACHE = os.path.join(SPIKE_DIR, "cache", "cutoff-coarse-v2.json")
V2_PROBES = os.path.join(BASE_DIR, "probes_coarse_v2.json")


def status_true(noul):
    if noul >= 0.8:
        return "conoce"
    if noul >= 0.5:
        return "parcial"
    return "no"


def load_rows(cache_path, probes_path):
    with open(cache_path) as f:
        cache = json.load(f)
    with open(probes_path) as f:
        corpus = json.load(f)
    answers = cache["response"]["answers"]
    rows = []
    for p in corpus["probes"]:
        rows.append({
            "id": p["id"],
            "quarter": p["quarter"],
            "event_date": p["event_date"],
            "truth": p["ground_truth"],
            "fact_type": p["fact_type"],
            "noul": answers[p["id"]]["noul"],
        })
    return rows


def analyze(cache_path, probes_path, label):
    print(f"##### analisis {label} #####")
    rows = load_rows(cache_path, probes_path)

    # 1. tablas trimestrales por capa (solo verdaderos)
    for layer in ("outcome", "scheduled"):
        trues = [r for r in rows if r["fact_type"] == layer and r["truth"] is True]
        print(f"== capa {layer} (verdaderos: {len(trues)}) ==")
        print(f"{'trim':8s} {'n':>2s} {'conoce':>6s} {'parcial':>7s} {'no':>3s}")
        for q in sorted({r["quarter"] for r in trues}):
            qrows = [r for r in trues if r["quarter"] == q]
            st = [status_true(r["noul"]) for r in qrows]
            print(f"{q:8s} {len(qrows):>2d} {st.count('conoce'):>6d} "
                  f"{st.count('parcial'):>7d} {st.count('no'):>3d}")
        print()

    # 2. falsos: ok vs rompen 0.3
    falses = [r for r in rows if r["truth"] is False]
    print(f"== falsos ({len(falses)}) ==")
    breakers = []
    for r in sorted(falses, key=lambda r: r["event_date"]):
        mark = "ok" if r["noul"] <= 0.3 else "ROMPE"
        if r["noul"] > 0.3:
            breakers.append(r)
        print(f"  {r['id']:20s} {r['fact_type']:9s} noul={r['noul']:<5} {mark}")
    print("rompen 0.3:", ", ".join(f"{r['id']} ({r['noul']})" for r in breakers) or "ninguno")
    print()

    # 3. ventana candidata solo de outcomes-true, agregada por trimestre
    otrues = [r for r in rows if r["fact_type"] == "outcome" and r["truth"] is True]
    quarters = sorted({r["quarter"] for r in otrues})
    qstat = {}
    for q in quarters:
        qrows = [r for r in otrues if r["quarter"] == q]
        st = [status_true(r["noul"]) for r in qrows]
        qstat[q] = {"n": len(qrows), "conoce": st.count("conoce"), "no": st.count("no")}
    lo_q = next((q for q in reversed(quarters)
                 if qstat[q]["conoce"] / qstat[q]["n"] >= 2 / 3), None)
    hi_q = next((q for q in quarters
                 if qstat[q]["no"] / qstat[q]["n"] >= 2 / 3), None)
    t_lo = t_hi = None
    if lo_q is not None:
        t_lo = max(r["event_date"] for r in otrues if r["quarter"] == lo_q)
    if hi_q is not None:
        t_hi = min(r["event_date"] for r in otrues if r["quarter"] == hi_q)
    print("== ventana candidata (solo outcomes-true) ==")
    print(f"  ultimo trim >= 2/3 conoce: {lo_q} -> T_lo = {t_lo}")
    print(f"  primer trim >= 2/3 no:     {hi_q} -> T_hi = {t_hi}")
    print(f"  ventana: [{t_lo}, {t_hi}]")
    print()

    # 4. anomalias por regla (no atribuibles a lo temporal)
    print("== anomalias (reglas) ==")
    sched_weak = [r for r in rows if r["fact_type"] == "scheduled"
                  and r["truth"] is True and status_true(r["noul"]) != "conoce"]
    print("  scheduled-true sin conoce (la fecha no deberia importar):")
    for r in sorted(sched_weak, key=lambda r: r["event_date"]):
        print(f"    {r['id']:26s} {r['event_date']} noul={r['noul']}")
    if t_lo is not None:
        early_no = [r for r in rows if r["fact_type"] == "outcome"
                    and r["truth"] is True and r["event_date"] <= t_lo
                    and status_true(r["noul"]) == "no"]
        print("  outcome-true en 'no' ANTES de T_lo (no es el corte):")
        for r in sorted(early_no, key=lambda r: r["event_date"]):
            print(f"    {r['id']:26s} {r['event_date']} noul={r['noul']}")
        if not early_no:
            print("    ninguno")
    print()


def delta():
    print("##### delta v1 -> v2 (noul_v2 - noul_v1, emparejado por ref_v1) #####")
    v1 = {r["id"]: r for r in load_rows(V1_CACHE, V1_PROBES)}
    with open(V2_PROBES) as f:
        v2probes = json.load(f)["probes"]
    with open(V2_CACHE) as f:
        v2ans = json.load(f)["response"]["answers"]
    print(f"{'ref_v1':28s} {'truth':5s} {'capa':9s} {'v1':>5s} {'v2':>5s} {'delta':>6s}")
    big = []
    for p in v2probes:
        a = v1[p["ref_v1"]]["noul"]
        b = v2ans[p["id"]]["noul"]
        d = round(b - a, 2)
        if abs(d) >= 0.15:
            big.append((p["ref_v1"], a, b, d))
        print(f"{p['ref_v1']:28s} {str(p['ground_truth']):5s} {p['fact_type']:9s} "
              f"{a:>5} {b:>5} {d:>+6.2f}")
    print()
    print(f"|delta| >= 0.15: {len(big)} probes")
    for ref, a, b, d in sorted(big, key=lambda t: -abs(t[3])):
        print(f"  {ref:28s} {a:>5} -> {b:<5} ({d:>+6.2f})")


def main(argv):
    mode = argv[1] if len(argv) > 1 else "v1"
    if mode not in ("v1", "v2", "delta", "all"):
        raise SystemExit("uso: python3 analyze.py [v1|v2|delta|all]")
    if mode in ("v1", "all"):
        analyze(V1_CACHE, V1_PROBES, "coarse v1")
    if mode in ("v2", "all"):
        analyze(V2_CACHE, V2_PROBES, "coarse v2")
    if mode in ("delta", "all"):
        delta()


if __name__ == "__main__":
    main(sys.argv)
