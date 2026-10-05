"""Mide el bucle de agente real de DSH con esfuerzo low vs high. 2 corridas.

Por que: en llamada suelta low costo 4,45x menos que high. En un bucle con
herramientas el CoT se devuelve y se re-concatena como input en cada vuelta, y
la sesion guarda usage por turno: ahi el multiplicador real puede ser mucho
mayor.

Fuente de los numeros: DSH persiste usage por turno en
~/.dsh/sessions/<cwd-escapado>/<session-id>/session.v4.jsonl.zstd
campo `usage` de los eventos `assistant/message`:
  inputTokens     = tokens nuevos (cache miss)
  cacheReadTokens = tokens leidos de cache (cache hit)
  outputTokens    = salida; incluye el razonamiento
Precio oficial deepseek-flash off-peak: hit 0.003 / miss 0.15 / out 0.60 por 1M.

El script NO toca el repo: escribe evidencia y crudos en probes/evidencia/.

Uso: python3 probes/bucle_agente.py
"""
import glob
import json
import os
import shutil
import subprocess
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EVID = os.path.join(BASE_DIR, "probes", "evidencia")
MSG = os.path.join(BASE_DIR, "probes", "insumos", "tarea_medidas.txt")
TOTAL = os.path.join(BASE_DIR, "probes", "insumos", "total.txt")
DSH = shutil.which("dsh") or os.path.expanduser(
    "~/.npm/_npx/1e7f6d9597241db0/node_modules/.bin/dsh")
NIVELES = ["low", "high"]
PRECIO = {"hit": 0.003, "miss": 0.15, "out": 0.60}


def carpeta_sesiones():
    esc = BASE_DIR.replace("/", "-")
    return os.path.expanduser(f"~/.dsh/sessions/--{esc.lstrip('-')}--")


def sesiones_existentes():
    return set(os.listdir(carpeta_sesiones())) if os.path.isdir(carpeta_sesiones()) else set()


def leer_usage(sid):
    p = os.path.join(carpeta_sesiones(), sid, "session.v4.jsonl.zstd")
    if not os.path.exists(p):
        return None
    out = subprocess.run(["zstd", "-dc", p], capture_output=True)
    turnos = []
    for ln in out.stdout.decode("utf-8", "replace").splitlines():
        try:
            e = json.loads(ln)
        except Exception:
            continue
        if e.get("type") == "assistant/message":
            d = e.get("data", {})
            u = d.get("usage") or {}
            turnos.append({"turn": d.get("turn"), "step": d.get("step"),
                           "in": u.get("inputTokens", 0) or 0,
                           "hit": u.get("cacheReadTokens", 0) or 0,
                           "out": u.get("outputTokens", 0) or 0})
    return turnos


def corre(nivel):
    patch = f"/tmp/esf_{nivel}.yml"
    with open(patch, "w") as f:
        f.write("- id: agent-default-model\n"
                "  name: '@deepseek-ai/dsh-agent-default-model'\n"
                "  config:\n"
                "    provider: deepseek-official\n"
                "    model: deepseek-flash\n"
                f"    reasoningEffort: {nivel}\n")
    antes = sesiones_existentes()
    t0 = time.time()
    with open(MSG, "rb") as fin:
        r = subprocess.run([DSH, "headless", "--patch", patch, "-"],
                           cwd=BASE_DIR, stdin=fin, capture_output=True)
    seg = time.time() - t0
    nuevas = sesiones_existentes() - antes
    sid = sorted(nuevas)[0] if nuevas else None

    salida = r.stdout.decode("utf-8", "replace")
    err = r.stderr.decode("utf-8", "replace")
    total_txt = open(TOTAL, encoding="utf-8").read().strip() if os.path.exists(TOTAL) else "(no existe)"

    with open(os.path.join(EVID, f"bucle-{nivel}.json"), "w", encoding="utf-8") as f:
        json.dump({"nivel": nivel, "patch": open(patch).read(), "session_id": sid,
                   "exit": r.returncode, "segundos": round(seg, 1),
                   "stdout": salida, "stderr": err[-2000:],
                   "total_txt": total_txt}, f, ensure_ascii=False, indent=1)

    turnos = leer_usage(sid) if sid else None
    if turnos is None:
        print(f"{nivel}: NO pude leer la sesion (sid={sid}); stderr={err[-300:]}")
        return None
    return {"nivel": nivel, "sid": sid, "exit": r.returncode, "seg": seg,
            "total_txt": total_txt, "stdout": salida, "turnos": turnos}


def main():
    os.makedirs(EVID, exist_ok=True)
    # Cada corrida necesita un total.txt propio: se borra el anterior.
    if os.path.exists(TOTAL):
        os.remove(TOTAL)
    print(f"tarea: {os.path.relpath(MSG, BASE_DIR)}   total esperado: 288,5")
    print(f"dsh: {DSH}\n")

    res = []
    for nivel in NIVELES:
        print(f"--- corriendo {nivel} ...")
        sys.stdout.flush()
        r = corre(nivel)
        if r:
            res.append(r)
            u = r["turnos"]
            print(f"    sid={r['sid']} exit={r['exit']} seg={r['seg']:.0f} "
                  f"turnos={len(u)} total.txt={r['total_txt']!r}")

    print("\n=== por turno ===")
    for r in res:
        print(f"\n{r['nivel']} (session {r['sid']}, exit {r['exit']}, {r['seg']:.0f}s)")
        print(f"  {'step':>4} {'in(miss)':>9} {'hit':>8} {'out':>7} {'usd':>9}")
        for t in r["turnos"]:
            usd = t["hit"]/1e6*PRECIO["hit"] + t["in"]/1e6*PRECIO["miss"] + t["out"]/1e6*PRECIO["out"]
            print(f"  {t['step']:>4} {t['in']:>9} {t['hit']:>8} {t['out']:>7} {usd:>9.6f}")

    print("\n=== totales ===")
    print(f"{'nivel':5} {'steps':>5} {'miss':>8} {'hit':>10} {'out':>7} {'seg':>6} {'usd_off':>10} {'usd_peak':>10}")
    resumen = {}
    for r in res:
        u = r["turnos"]
        miss = sum(t["in"] for t in u)
        hit = sum(t["hit"] for t in u)
        out = sum(t["out"] for t in u)
        usd = hit/1e6*0.003 + miss/1e6*0.15 + out/1e6*0.60
        resumen[r["nivel"]] = {"steps": len(u), "miss": miss, "hit": hit, "out": out,
                              "seg": r["seg"], "usd": usd,
                              "ok": r["total_txt"].strip() == "TOTAL: 288,5"}
        print(f"{r['nivel']:5} {len(u):>5} {miss:>8} {hit:>10} {out:>7} {r['seg']:>6.0f} "
              f"{usd:>10.6f} {usd*2:>10.6f}")

    if "low" in resumen and "high" in resumen:
        lo, hi = resumen["low"], resumen["high"]
        print(f"\n=== low vs high ===")
        for campo in ["steps", "miss", "hit", "out", "seg", "usd"]:
            a, b = lo[campo], hi[campo]
            razon = (b / a) if a else float("inf")
            print(f"  {campo:6} low={a:>10.2f}  high={b:>10.2f}  high/low={razon:.2f}x")
        print(f"\n  tarea correcta: low={lo['ok']}  high={hi['ok']} (total.txt == 'TOTAL: 288,5')")
        print(f"  COSTO POR TAREA CORRECTA: low={lo['usd'] if lo['ok'] else float('nan'):.6f} USD  "
              f"high={hi['usd'] if hi['ok'] else float('nan'):.6f} USD")
    print(f"\nevidencia y crudos en probes/evidencia/")


if __name__ == "__main__":
    main()
