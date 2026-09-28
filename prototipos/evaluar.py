"""Evalúa la curva de prototipos contra bateria.json (sin API).

Uso: python3 prototipos/evaluar.py <modelo> <rN>
Criterio automático: un dato del modelo acierta si su valor coincide con el de
un dato correcto del mismo texto (normalizado) y su unidad es equivalente.
Las variables se revisan a mano.
"""
import glob
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EQUIV = {"horas": "hora", "año": "fecha", "m2": "metros cuadrados",
         "m²": "metros cuadrados", "l/min": "litros por minuto",
         "unidades": "unidad", "t": "toneladas", "m": "metros", "ha": "hectáreas"}


def norm(v):
    if v is None:
        return None
    v = str(v).strip().lower().rstrip(".")
    v = re.sub(r"\s+", " ", v)
    return EQUIV.get(v, v)


def main():
    modelo, rep = sys.argv[1], sys.argv[2]
    bateria = {b["id"]: b for b in json.load(open(os.path.join(BASE_DIR, "bateria.json"), encoding="utf-8"))}
    total_gold = sum(len(b["gold"]) for b in bateria.values())
    configs = ["k0", "A", "AB", "ABC", "ABCD", "ABCDE"]
    print(f"{'config':7} {'aciertos':>9} {'faltan':>7} {'sobran':>7} {'tokens':>7} {'seg':>6}")
    detalle = []
    for c in configs:
        ac = fa = so = tok = 0
        seg = 0.0
        porn = {}
        for i, b in bateria.items():
            p = os.path.join(BASE_DIR, "cache", f"{c}-{i}-{modelo}-{rep}.json")
            if not os.path.exists(p):
                continue
            cr = json.load(open(p, encoding="utf-8"))
            tok += cr.get("reasoning_tokens") or 0
            seg += cr.get("segundos") or 0
            datos = (cr.get("parsed") or {}).get("datos") or []
            gold = [(norm(v), norm(u)) for _, v, u in b["gold"]]
            usados = set()
            aciertos_t = 0
            for d in datos:
                par = (norm(d.get("valor")), norm(d.get("unidad_de_medida")))
                for k, g in enumerate(gold):
                    if k not in usados and g == par:
                        usados.add(k)
                        aciertos_t += 1
                        break
                else:
                    detalle.append((c, i, "SOBRA", d))
            for k, g in enumerate(b["gold"]):
                if k not in usados:
                    detalle.append((c, i, "FALTA", g))
            ac += aciertos_t
            fa += len(gold) - aciertos_t
            so += len(datos) - aciertos_t
            porn.setdefault(b["nodo"], [0, 0])
            porn[b["nodo"]][0] += aciertos_t
            porn[b["nodo"]][1] += len(gold) + (len(datos) - aciertos_t)
        print(f"{c:7} {ac:>4}/{total_gold:<4} {fa:>7} {so:>7} {tok:>7} {seg:>6.0f}  " +
              " ".join(f"{n}:{a}/{t}" for n, (a, t) in sorted(porn.items())))
    print()
    for c, i, tipo, d in detalle:
        print(c, i, tipo, d)


if __name__ == "__main__":
    main()
