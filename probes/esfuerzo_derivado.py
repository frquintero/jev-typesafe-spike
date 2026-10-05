"""Sonda discriminante: calidad low vs high vs max en datos DERIVADOS.

Hipotesis a probar: si en los casos donde el valor pedido NO esta escrito en el
texto (hay que calcularlo), low y high empatan, entonces low es un sweet spot de
calidad/costo. Si low pierde exactitud, el tramo 50->75 es donde esta la calidad
y low no es el punto.

Diseno:
- 5 casos 'derivado' (el valor se calcula: 55% de 420, resta, conversion de
  unidades, caudal x tiempo, sillas libres) + 5 'control_literal' sobre el MISMO
  texto (el valor esta impreso). El control aisla el efecto de la tarea: mide si
  un nivel degrada incluso lo que no exige razonar.
- 3 niveles: low (b=50), high (b=75), max (b=100). Se omite 'off' aqui: en la
  corrida anterior no razona, y estos casos exigen aritmetica; se reporta a ojo.
- Mismo prompt y mismo texto en los tres niveles; el esfuerzo va en el parametro
  extra de la llamada.

Uso: python3 probes/esfuerzo_derivado.py [rN]

Costos con la tabla oficial de deepseek-flash (V4.1-Flash):
off-peak hit 0.003 / miss 0.15 / out 0.60 por 1M; peak es el doble.
Los crudos van a cache/esfuerzo_derivado-<rN>-*.json. No toca crudos previos.

Sin veredicto unico: imprime acierto/fallo por caso y el valor verbatim.
"""
import copy
import json
import os
import sys
import time
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "niveles"))
import run_niveles  # noqa: E402
from run_niveles import MODEL_PARAMS, call_model  # noqa: E402

CACHE_DIR = os.path.join(BASE_DIR, "cache")
PRECIO = {"hit": (0.003, 0.006), "miss": (0.15, 0.30), "out": (0.60, 1.20)}
NIVELES = ["off", "low", "high", "max"]
TOPE_TOKENS = 8000  # tope duro por llamada: evita deliberaciones de 20k tokens

# --- inyeccion de max_tokens sin duplicar call_model -------------------------
_Request = urllib.request.Request


def _request_con_tope(url, data=None, headers=None, **kw):
    if data and isinstance(data, (bytes, bytearray)):
        try:
            cuerpo = json.loads(data.decode("utf-8"))
            if isinstance(cuerpo, dict) and "messages" in cuerpo:
                cuerpo["max_tokens"] = TOPE_TOKENS
                data = json.dumps(cuerpo).encode("utf-8")
        except Exception:
            pass
    return _Request(url, data=data, headers=headers, **kw)


def extra_de(nivel):
    """off NO es un nivel de esfuerzo: la API lo rechaza (422). Es apagar
    thinking, que en DSH se manda como {"thinking": {"type": "disabled"}} sin
    output_config.effort. Verificado contra la API el 05-10-2026."""
    if nivel == "off":
        return {"thinking": {"type": "disabled"}}
    return {"thinking": {"type": "enabled"}, "reasoning_effort": nivel}


def costo(usage):
    hit = usage.get("prompt_cache_hit_tokens", 0) or 0
    miss = usage.get("prompt_cache_miss_tokens", 0) or 0
    out = usage.get("completion_tokens", 0) or 0
    if not (hit or miss):
        miss = usage.get("prompt_tokens", 0) or 0
    off = hit / 1e6 * PRECIO["hit"][0] + miss / 1e6 * PRECIO["miss"][0] + out / 1e6 * PRECIO["out"][0]
    pk = hit / 1e6 * PRECIO["hit"][1] + miss / 1e6 * PRECIO["miss"][1] + out / 1e6 * PRECIO["out"][1]
    return off, pk


def norm_num(v):
    """Normaliza a float para comparar. None si no es numerico."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower().replace(" ", "")
    for ruido in ("$", "kg", "kilogramos", "litros", "unidad", "unidades"):
        s = s.replace(ruido, "")
    if s.endswith("l"):
        s = s[:-1]
    # separador de miles y decimal: 1.800 o 1,800 -> 1800 ; 1.8 -> 1.8
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".")
    elif s.count(".") == 1 and len(s.split(".")[-1]) == 3 and len(s.split(".")[0]) <= 3:
        s = s.replace(".", "")
    else:
        s = s.replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def main():
    rep = sys.argv[1] if len(sys.argv) > 1 else "r1"
    with open(os.path.join(BASE_DIR, "probes", "prompt_calculo.md"), encoding="utf-8") as f:
        plantilla = f.read()
    with open(os.path.join(BASE_DIR, "probes", "esfuerzo_casos.json"), encoding="utf-8") as f:
        casos = json.load(f)

    os.makedirs(CACHE_DIR, exist_ok=True)
    print(f"esfuerzo_derivado {rep}: {len(casos)} casos x {len(NIVELES)} niveles "
          f"= {len(casos) * len(NIVELES)} llamadas, tope {TOPE_TOKENS} tokens")
    urllib.request.Request = _request_con_tope

    filas = []
    for c in casos:
        contenido = plantilla.replace("{{TEXTO}}", c["texto"]).replace("{{PREGUNTA}}", c["pregunta"])
        for nivel in NIVELES:
            cfg_orig = MODEL_PARAMS["v2"]["deepseek"]
            cfg = copy.deepcopy(cfg_orig)
            cfg["extra"] = extra_de(nivel)
            MODEL_PARAMS["v2"]["deepseek"] = cfg
            t0 = time.time()
            try:
                body, resp = call_model("v2", "deepseek", contenido)
            finally:
                MODEL_PARAMS["v2"]["deepseek"] = cfg_orig
            seg = time.time() - t0

            usage = resp.get("usage") or {}
            off, pk = costo(usage)
            content = resp["choices"][0]["message"]["content"]
            razon = resp["choices"][0]["message"].get("reasoning_content") or ""
            try:
                limpio = content.strip()
                if limpio.startswith("```"):
                    limpio = "\n".join(limpio.split("\n")[1:-1])
                dato = json.loads(limpio)["dato"]
            except Exception:
                dato = None
            valor = dato.get("valor") if isinstance(dato, dict) else None
            num = norm_num(valor)
            acierto = num is not None and abs(num - float(c["esperado"])) < 1e-6

            raw = {
                "caso": c["id"], "tipo": c["tipo"], "nivel": nivel, "rep": rep,
                "pregunta": c["pregunta"], "esperado": c["esperado"],
                "texto": c["texto"], "parametros_extra": cfg["extra"],
                "segundos": round(seg, 2), "modelo_efectivo": resp.get("model"),
                "body_enviado": body, "usage": usage,
                "costo_usd_offpeak": round(off, 6), "costo_usd_peak": round(pk, 6),
                "content": content, "reasoning_chars": len(razon),
                "dato_extraido": dato, "acierto": acierto,
                "chunks_crudos": resp.get("_stream_crudos") or resp.get("_stream_chunks_crudos"),
            }
            with open(os.path.join(CACHE_DIR, f"esfuerzo_derivado-{rep}-{c['id']}-{nivel}.json"),
                      "w", encoding="utf-8") as f:
                json.dump(raw, f, ensure_ascii=False, indent=1)

            filas.append({"id": c["id"], "tipo": c["tipo"], "nivel": nivel,
                          "acierto": acierto, "valor": valor,
                          "unidad": (dato or {}).get("unidad_de_medida"),
                          "esperado": c["esperado"],
                          "hit": usage.get("prompt_cache_hit_tokens", 0) or 0,
                          "miss": usage.get("prompt_cache_miss_tokens", 0) or 0,
                          "out": usage.get("completion_tokens", 0) or 0,
                          "seg": round(seg, 1), "usd": off})
            print(f"  {c['id']:4} {c['tipo'][:15]:15} {nivel:4} "
                  f"{'ACIERTO' if acierto else 'fallo  '} esperado={c['esperado']:>7} "
                  f"valor={str(valor)[:22]:22} out={filas[-1]['out']:5} "
                  f"seg={seg:5.1f} usd={off:.6f}")
            sys.stdout.flush()

    print("\nresumen por nivel:")
    for nivel in NIVELES:
        fs = [f for f in filas if f["nivel"] == nivel]
        for tipo in ["derivado", "control_literal"]:
            sub = [f for f in fs if f["tipo"] == tipo]
            ok = sum(1 for f in sub if f["acierto"])
            print(f"  {nivel:4} {tipo:15} {ok}/{len(sub)} aciertos  "
                  f"out={sum(f['out'] for f in sub):6} "
                  f"seg={sum(f['seg'] for f in sub):6.1f} "
                  f"usd={sum(f['usd'] for f in sub):.6f}")
    print("\ncrudos en cache/esfuerzo_derivado-%s-*.json" % rep)


if __name__ == "__main__":
    main()
