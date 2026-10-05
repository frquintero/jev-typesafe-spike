"""Escalera de dificultad: donde se separa high de off, y si low lo alcanza.

Hipotesis:
- H1: off basta para lo simple y mecanico.
- H2: low reemplaza a high.
H2 solo tiene contenido donde high se separe de off; por eso la escalera busca
ese punto.

5 peldaños x 4 niveles (off/low/high/max):
  1 trivial   datos literales
  2 medio     2 pasos, numeros redondos
  3 duro      aritmetica no memorizable, 3-4 pasos
  4 juicio    cuantificadores vagos, trampa condicional, control positivo
  5 volumen   30 oraciones, formato estricto: que oraciones traen numero

Metrica (mecanica, sin jurado):
- acierto: el valor pedido, correcto.
- espurio: invento un valor donde el texto no lo tiene (main en peldaño 4).
- abstencion: devolvio null donde correspondia null.
- json_ok: respondio JSON parseable.

Uso: python3 probes/escalera.py [rN]
Crudos: cache/escalera-<rN>-*.json. No toca crudos previos.
"""
import copy
import json
import os
import re
import sys
import time
import urllib.request

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, "niveles"))
from run_niveles import MODEL_PARAMS, call_model  # noqa: E402

CACHE_DIR = os.path.join(BASE_DIR, "cache")
PRECIO = {"hit": (0.003, 0.006), "miss": (0.15, 0.30), "out": (0.60, 1.20)}
NIVELES = ["off", "low", "high", "max"]
TOPE_TOKENS = 8000

Request = urllib.request.Request


def request_con_tope(url, data=None, headers=None, **kw):
    if data and isinstance(data, (bytes, bytearray)):
        try:
            cuerpo = json.loads(data.decode("utf-8"))
            if isinstance(cuerpo, dict) and "messages" in cuerpo:
                cuerpo["max_tokens"] = TOPE_TOKENS
                data = json.dumps(cuerpo).encode("utf-8")
        except Exception:
            pass
    return Request(url, data=data, headers=headers, **kw)


def extra_de(nivel):
    if nivel == "off":
        return {"thinking": {"type": "disabled"}}
    return {"thinking": {"type": "enabled"}, "reasoning_effort": nivel}


def costo(usage):
    hit = usage.get("prompt_cache_hit_tokens", 0) or 0
    miss = usage.get("prompt_cache_miss_tokens", 0) or 0
    out = usage.get("completion_tokens", 0) or 0
    if not (hit or miss):
        miss = usage.get("prompt_tokens", 0) or 0
    off = hit / 1e6 * 0.003 + miss / 1e6 * 0.15 + out / 1e6 * 0.60
    pk = hit / 1e6 * 0.006 + miss / 1e6 * 0.30 + out / 1e6 * 1.20
    return off, pk


def num(v):
    if v is None or isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().lower().replace(" ", "").replace("$", "")
    for r in ("pesos", "kilometros", "kilómetros", "kilogramos", "kg", "litros", "unidad", "unidades", "°c"):
        s = s.replace(r, "")
    if s.endswith("l"):
        s = s[:-1]
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


# --- peldaño 5: documento largo, formato estricto ----------------------------
CON_NUMERO = [1, 2, 4, 6, 8, 10, 11, 13, 15, 17, 19, 20, 22, 24, 26, 28, 29]
ORACIONES = [
    "La planta de tratamiento Norte opera desde 1998.",
    "Su caudal de diseño es de 320 litros por segundo.",
    "El operario de turno revisa los filtros cada mañana.",
    "La última limpieza de los filtros fue hace 6 días.",
    "El registro de novedades se archiva en la oficina.",
    "El tanque de contacto tiene capacidad para 4.500 metros cúbicos.",
    "La alarma de cloro sonó dos veces.",
    "La concentración de cloro residual marcó 0,8 miligramos por litro.",
    "El laboratorio entrega los resultados los viernes.",
    "La muestra de las 6:30 pasó el control.",
    "El pH de esa muestra fue 7,1.",
    "El jefe de planta firma el reporte diario.",
    "La bomba centrífuga 3 consumió 87 kilovatios hora.",
    "El mantenimiento preventivo se hace cada trimestre.",
    "La tubería de entrada soporta 9 bares de presión.",
    "El personal rota cada semana.",
    "La empresa contratista llegó en la mañana.",
    "El sedimentador retiró 240 kilogramos de lodo.",
    "El análisis de turbiedad dio 3,4 unidades nefelométricas.",
    "El caudal de salida se midió en 298 litros por segundo.",
    "La válvula de alivio quedó cerrada.",
    "El consumo eléctrico de la semana fue 12.400 kilovatios hora.",
    "El reporte se envía a la autoridad ambiental.",
    "La eficiencia del proceso alcanzó 94 por ciento.",
    "La reunión de operarios duró una hora.",
    "El nivel del tanque bajó 1,2 metros.",
    "El operario dejó la novedad por escrito.",
    "La conductividad del agua fue 415 microsiemens por centímetro.",
    "El respaldo del generador cubre 8 horas.",
    "El acta de la visita quedó firmada.",
]
DOC5 = " ".join(f"[{i+1}] {o}" for i, o in enumerate(ORACIONES))
PREG5 = ("índice de cada oración del texto que contiene al menos un número, "
         "en el campo `oraciones_con_numero` (lista de enteros, sin repetir, en orden)")


def main():
    rep = sys.argv[1] if len(sys.argv) > 1 else "r1"
    with open(os.path.join(BASE_DIR, "probes", "prompt_escalera.md"), encoding="utf-8") as f:
        plantilla = f.read()
    with open(os.path.join(BASE_DIR, "probes", "escalera_casos.json"), encoding="utf-8") as f:
        casos = json.load(f)
    casos.append({"id": "v1", "peldaño": 5, "tipo": "volumen",
                  "texto": DOC5, "pregunta": PREG5, "esperado": CON_NUMERO, "unidad": None})

    os.makedirs(CACHE_DIR, exist_ok=True)
    print(f"escalera {rep}: {len(casos)} casos x {len(NIVELES)} niveles "
          f"= {len(casos)*len(NIVELES)} llamadas, tope {TOPE_TOKENS} tokens")
    urllib.request.Request = request_con_tope

    filas = []
    for c in casos:
        contenido = plantilla.replace("{{TEXTO}}", c["texto"]).replace("{{PREGUNTA}}", c["pregunta"])
        for nivel in NIVELES:
            orig = MODEL_PARAMS["v2"]["deepseek"]
            cfg = copy.deepcopy(orig)
            cfg["extra"] = extra_de(nivel)
            MODEL_PARAMS["v2"]["deepseek"] = cfg
            t0 = time.time()
            try:
                body, resp = call_model("v2", "deepseek", contenido)
            finally:
                MODEL_PARAMS["v2"]["deepseek"] = orig
            seg = time.time() - t0

            usage = resp.get("usage") or {}
            off_usd, pk_usd = costo(usage)
            content = resp["choices"][0]["message"]["content"]
            limpio = content.strip()
            if limpio.startswith("```"):
                limpio = "\n".join(limpio.split("\n")[1:-1])
            parsed, json_ok = None, False
            try:
                parsed = json.loads(limpio)
                json_ok = True
            except Exception:
                m = re.search(r"\{.*\}", limpio, flags=re.S)
                if m:
                    try:
                        parsed = json.loads(m.group(0))
                        json_ok = True
                    except Exception:
                        pass

            if c["tipo"] == "volumen":
                lista = (parsed or {}).get("oraciones_con_numero")
                lista = [x for x in lista if isinstance(x, int)] if isinstance(lista, list) else None
                if lista is None:
                    veredicto, detalle = "FALLO", "sin lista"
                else:
                    fp = sorted(set(lista) - set(CON_NUMERO))
                    fn = sorted(set(CON_NUMERO) - set(lista))
                    veredicto = "ACIERTO" if not fp and not fn else "FALLO"
                    detalle = f"fp={fp} fn={fn}"
                valor, espurio, abstencion = None, False, False
            else:
                valor = (parsed or {}).get("dato", {}).get("valor") if isinstance(parsed, dict) else None
                if c["esperado"] is None:
                    abstencion = valor is None
                    espurio = (valor is not None) and (num(valor) is not None or str(valor).strip() != "")
                    veredicto = "ABSTENCION" if abstencion else "ESPURIO"
                    detalle = f"valor={valor!r}"
                else:
                    n = num(valor)
                    ok = n is not None and abs(n - float(c["esperado"])) < 1e-6
                    veredicto = "ACIERTO" if ok else "FALLO"
                    espurio = abstencion = False
                    detalle = f"esperado={c['esperado']} valor={valor!r}"

            raw = {"caso": c["id"], "peldaño": c["peldaño"], "tipo": c["tipo"],
                   "tag": c.get("tag"), "nivel": nivel, "rep": rep,
                   "pregunta": c["pregunta"], "esperado": c["esperado"],
                   "veredicto": veredicto, "detalle": detalle, "json_ok": json_ok,
                   "segundos": round(seg, 2), "modelo_efectivo": resp.get("model"),
                   "parametros_extra": cfg["extra"], "usage": usage,
                   "costo_usd_offpeak": round(off_usd, 6), "costo_usd_peak": round(pk_usd, 6),
                   "body_enviado": body, "content": content, "dato_parseado": parsed,
                   "chunks_crudos": resp.get("_stream_chunks_crudos")}
            with open(os.path.join(CACHE_DIR, f"escalera-{rep}-{c['id']}-{nivel}.json"),
                      "w", encoding="utf-8") as f:
                json.dump(raw, f, ensure_ascii=False, indent=1)

            filas.append({"id": c["id"], "peldaño": c["peldaño"], "tipo": c["tipo"],
                          "nivel": nivel, "veredicto": veredicto, "json_ok": json_ok,
                          "espurio": espurio, "abstencion": abstencion,
                          "out": usage.get("completion_tokens", 0) or 0,
                          "seg": round(seg, 1), "usd": off_usd})
            print(f"  {c['id']:4} P{c['peldaño']} {c['tipo'][:7]:7} {nivel:4} {veredicto:10} "
                  f"{detalle[:46]:46} out={filas[-1]['out']:5} seg={seg:5.1f} {off_usd:.6f}")
            sys.stdout.flush()

    print("\n=== resumen por nivel ===")
    print(f"{'nivel':5} {'aciertos':>9} {'espurios':>9} {'abstenc.':>9} {'json_ok':>8} "
          f"{'out':>7} {'seg':>7} {'usd_off':>10} {'usd_peak':>10}")
    for nivel in NIVELES:
        fs = [f for f in filas if f["nivel"] == nivel]
        ac = sum(1 for f in fs if f["veredicto"] == "ACIERTO")
        esp = sum(1 for f in fs if f["espurio"])
        ab = sum(1 for f in fs if f["abstencion"])
        jk = sum(1 for f in fs if f["json_ok"])
        print(f"{nivel:5} {ac:>9} {esp:>9} {ab:>9} {jk:>8}/{len(fs)} "
              f"{sum(f['out'] for f in fs):>7} {sum(f['seg'] for f in fs):>7.1f} "
              f"{sum(f['usd'] for f in fs):>10.6f} "
              f"{sum(f['usd']*2 for f in fs):>10.6f}")
    print("\n=== desglose de los casos de juicio (peldaño 4) ===")
    for nivel in NIVELES:
        fs = [f for f in filas if f["nivel"] == nivel and f["peldaño"] == 4]
        print(f"  {nivel:4} " + "  ".join(f"{f['id']}={f['veredicto']}" for f in fs))
    print("\n=== peldaño por peldaño (aciertos / casos con valor esperado) ===")
    for p in [1, 2, 3]:
        for nivel in NIVELES:
            fs = [f for f in filas if f["nivel"] == nivel and f["peldaño"] == p]
            print(f"  P{p} {nivel:4} {sum(1 for f in fs if f['veredicto']=='ACIERTO')}/{len(fs)}", end="")
        print()
    for nivel in NIVELES:
        fs = [f for f in filas if f["nivel"] == nivel and f["peldaño"] == 5]
        print(f"  P5 {nivel:4} {'ACIERTO' if fs and fs[0]['veredicto']=='ACIERTO' else 'FALLO'}")
    print(f"\ncrudos en cache/escalera-{rep}-*.json")


if __name__ == "__main__":
    main()
