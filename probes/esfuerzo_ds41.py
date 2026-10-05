"""Sonda: costo y calidad de DeepSeek-V4.1-Flash segun reasoning_effort.

Idea chica, no estudio. Corre el MISMO prompt y el MISMO texto con los cuatro
niveles de esfuerzo del selector de DSH (off | low | high | max) y reporta, por
llamada: tokens de entrada con y sin cache, tokens de salida, tokens de
razonamiento, segundos, costo en dolares y el JSON extraido.

Uso: python3 probes/esfuerzo_ds41.py [rN]

- Reutiliza call_model de niveles/run_niveles.py (mismo camino de red y de
  cabecera de clave). No reinventa transporte ni lee claves.
- No toca ningun crudo existente: escribe en cache/esfuerzo_ds41-<rN>-*.json.
- El esfuerzo se inyecta en el parametro extra de la llamada:
  off   -> {"thinking": {"type": "disabled"}}                (sin razonamiento)
  low   -> {"thinking": {"type": "enabled"}, "reasoning_effort": "low"}   (b=50)
  high  -> idem con "high"                                   (b=75)
  max   -> idem con "max"                                    (b=100)
  Verificado: DSH (dsh-llm-deepseek) mapea off a thinking disabled y no manda
  output_config.effort; los otros tres son niveles reales de la API.

Costos: tabla oficial de https://api-docs.deepseek.com/quick_start/pricing/,
deepseek-flash (DeepSeek-V4.1-Flash). Off-peak: hit 0.003 / miss 0.15 / out 0.60
por 1M. Peak es el doble, 01:00-04:00 y 06:00-10:00 UTC L-V. El script reporta
los dos totales y no adivina la hora de facturacion.

Sin veredicto: imprime el crudo y lo guarda. La calidad se lee a ojo y con el
conteo de valores citados; no hay puntaje unico.
"""
import copy
import json
import os
import re
import sys
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "niveles"))
from run_niveles import MODEL_PARAMS, call_model  # noqa: E402

CACHE_DIR = os.path.join(BASE_DIR, "cache")

# Precio oficial deepseek-flash, USD por 1M tokens (off-peak / peak).
PRECIO = {
    "hit": (0.003, 0.006),
    "miss": (0.15, 0.30),
    "out": (0.60, 1.20),
}

NIVELES = ["off", "low", "high", "max"]


def extra_de(nivel):
    if nivel == "off":
        return {"thinking": {"type": "disabled"}}
    return {"thinking": {"type": "enabled"}, "reasoning_effort": nivel}


def costo(usage):
    """Devuelve (off_peak, peak) en USD a partir del usage de la respuesta."""
    hit = usage.get("prompt_cache_hit_tokens", 0) or 0
    miss = usage.get("prompt_cache_miss_tokens", 0) or 0
    out = usage.get("completion_tokens", 0) or 0
    if not (hit or miss):  # sin desglose: todo miss
        miss = usage.get("prompt_tokens", 0) or 0
    off = hit / 1e6 * PRECIO["hit"][0] + miss / 1e6 * PRECIO["miss"][0] + out / 1e6 * PRECIO["out"][0]
    pk = hit / 1e6 * PRECIO["hit"][1] + miss / 1e6 * PRECIO["miss"][1] + out / 1e6 * PRECIO["out"][1]
    return off, pk


def valores_citados(content):
    """Valores no nulos del JSON de datos, normalizados para comparar."""
    try:
        parsed = json.loads(re.sub(r"^```(?:json)?|```$", "", content.strip(), flags=re.M).strip())
    except Exception:
        return None
    vals = []
    for u in parsed.get("unidades", []) or []:
        for v in u.get("variables", []) or []:
            for x in v.get("valores", []) or []:
                val = x.get("valor")
                if val not in (None, ""):
                    vals.append(re.sub(r"\s+", " ", str(val)).strip().lower())
    return vals


def corre(etq, prompt_name, doc_name, rep):
    with open(os.path.join(BASE_DIR, "unidades", "prompts", f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()
    with open(os.path.join(BASE_DIR, "unidades", "docs", f"{doc_name}.md"), encoding="utf-8") as f:
        texto = f.read().strip()
    contenido = prompt.replace("{{TEXTO}}", texto)
    gold = GOLD.get(doc_name)

    filas = []
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
        vals = valores_citados(content)

        raw = {
            "etiqueta": etq, "doc": doc_name, "prompt": prompt_name, "rep": rep,
            "nivel": nivel, "parametros_extra": cfg["extra"], "segundos": round(seg, 2),
            "modelo_efectivo": resp.get("model"), "body_enviado": body,
            "usage": usage, "costo_usd_offpeak": round(off, 6), "costo_usd_peak": round(pk, 6),
            "content": content, "reasoning_chars": len(razon),
            "valores_citados": vals, "gold": gold,
            "chunks_crudos": resp.get("_stream_chunks_crudos"),
        }
        ruta = os.path.join(CACHE_DIR, f"esfuerzo_ds41-{rep}-{etq}-{nivel}.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump(raw, f, ensure_ascii=False, indent=1)

        hit = usage.get("prompt_cache_hit_tokens", 0) or 0
        miss = usage.get("prompt_cache_miss_tokens", 0) or 0
        out = usage.get("completion_tokens", 0) or 0
        filas.append({
            "nivel": nivel, "hit": hit, "miss": miss, "out": out,
            "seg": round(seg, 1),
            "usd_off": round(off, 6), "usd_peak": round(pk, 6),
            "vals": len(vals) if vals is not None else None,
        })
        print(f"  {nivel:5} hit={hit:5} miss={miss:5} out={out:5} "
              f"seg={seg:6.1f} usd_off={off:.6f} usd_peak={pk:.6f} "
              f"json={'ok' if vals is not None else 'FALLO'} vals={len(vals) if vals is not None else '-'}")
        sys.stdout.flush()
    return filas


# gold minimo y explicito para los micro-documentos de verificacion.
GOLD = {
    "ut1": [("temperatura del termostato del circuito de retorno", "55 °C")],
    "ut2": [("capacidad del tanque de agua potable", "30000 litros")],
    "ut3": [("presion de las llantas delanteras", "32 psi"),
            ("presion de las llantas traseras", "35 psi")],
}


def main():
    rep = sys.argv[1] if len(sys.argv) > 1 else "r1"
    os.makedirs(CACHE_DIR, exist_ok=True)
    casos = [
        ("micro-ut1", "datos_u1", "ut1"),
        ("micro-ut2", "datos_u1", "ut2"),
        ("micro-ut3", "datos_u1", "ut3"),
    ]
    print(f"esfuerzo_ds41 {rep}: {len(casos)} caso(s) x {len(NIVELES)} niveles "
          f"= {len(casos) * len(NIVELES)} llamadas")
    print(f"{'caso':11} {'nivel':5} {'hit':>5} {'miss':>5} {'out':>5} {'seg':>6} "
          f"{'usd_off':>10} {'usd_peak':>10} json")
    totales = {}
    for etq, prompt_name, doc_name in casos:
        print(f"{etq}:")
        for f in corre(etq, prompt_name, doc_name, rep):
            totales.setdefault(f["nivel"], []).append(f)
    print("\nresumen por nivel (off-peak / peak):")
    for nivel in NIVELES:
        fs = totales.get(nivel, [])
        if not fs:
            continue
        print(f"  {nivel:5} out_total={sum(x['out'] for x in fs):5} "
              f"seg_total={sum(x['seg'] for x in fs):6.1f} "
              f"usd_off={sum(x['usd_off'] for x in fs):.6f} "
              f"usd_peak={sum(x['usd_peak'] for x in fs):.6f} "
              f"vals={[x['vals'] for x in fs]}")


if __name__ == "__main__":
    main()
