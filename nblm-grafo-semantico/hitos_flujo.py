"""Reduce un flujo de chat de NotebookLM (fragmentos acumulativos) a sus hitos.

Hito = primera aparición de un paso de razonamiento («**Título**») o una
llamada nueva a una herramienta (cuando sube su cuenta en el flujo
acumulado), con su hora relativa. Se usa en fu2_doc_entero.py y para
reducir crudos ya guardados: python3 hitos_flujo.py <crudo.json>
"""
import json
import re
import sys

TITULO = re.compile(r'\*\*([A-Z][^*\\]{3,80})\*\*')
HERRAMIENTA = re.compile(r'\\"([a-z]+(?:_[a-z]+)+|list_dir|semantic_search)\\",\[\[\[')


def hitos(fragmentos):
    vistos, cuentas, eventos = set(), {}, []
    for f in fragmentos:
        t, s = f["t"], f.get("texto", "")
        for m in TITULO.findall(s):
            if m not in vistos:
                vistos.add(m)
                eventos.append({"t": t, "tipo": "razonamiento", "texto": m})
        n = {}
        for h in HERRAMIENTA.findall(s):
            n[h] = n.get(h, 0) + 1
        for h, k in n.items():
            while cuentas.get(h, 0) < k:
                cuentas[h] = cuentas.get(h, 0) + 1
                eventos.append({"t": t, "tipo": "herramienta", "texto": h})
    eventos.sort(key=lambda e: e["t"])
    resumen = {"fragmentos_n": len(fragmentos),
               "flujo_bytes": sum(f["bytes"] for f in fragmentos),
               "fragmento_mayor_bytes": max((f["bytes"] for f in fragmentos), default=0),
               "primer_fragmento_s": fragmentos[0]["t"] if fragmentos else None,
               "ultimo_fragmento_s": fragmentos[-1]["t"] if fragmentos else None,
               "llamadas_por_herramienta": cuentas}
    return eventos, resumen


if __name__ == "__main__":
    ruta = sys.argv[1]
    c = json.load(open(ruta, encoding="utf-8"))
    ev, res = hitos(c.pop("flujo"))
    c["flujo_hitos"] = ev
    c["flujo_resumen"] = res
    c["nota_flujo"] = ("Flujo completo (~40 MB, acumulativo) reducido a hitos el 2026-10-03 "
                       "por decisión de Frat; el original queda en el historial de git (commit cebba25).")
    json.dump(c, open(ruta, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(len(ev), "hitos;", json.dumps(res["llamadas_por_herramienta"]))
