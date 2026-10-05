"""Repuntua el peldaño 5 (volumen) desde los crudos guardados. Sin API.

Dos bugs del runner original, ambos de puntuacion, no del modelo:
1. escalera.py buscaba la lista de oraciones en la raiz del JSON
   (oraciones_con_numero), pero la plantilla pedia un escalar y el modelo la
   puso correctamente en dato.valor.
2. El oro estaba escrito a mano en una lista y NO coincidia con el documento
   que el script genero (17 indices en orden equivocado). Aqui el oro se
   DERIVA del body_enviado de los crudos: se leen las oraciones numeradas y se
   marca cual contiene un digito. Asi el oro no puede desincronizarse.

Se puntua con dos criterios, porque la diferencia entre ellos es informativa:
- cifras: oraciones con al menos un digito (determinista).
- numerales: ademas las que traen un numeral escrito con letra (dos, una).

Uso: python3 probes/escalera_p5_revisar.py [rN]
"""
import json
import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(BASE_DIR, "cache")
NIVELES = ["off", "low", "high", "max"]


def oraciones_de(body):
    """Lee las oraciones numeradas del texto realmente enviado."""
    msg = body["messages"][0]["content"]
    doc = msg.split("<<<")[1]
    pares = re.findall(r"\[(\d+)\]\s*(.*?)(?=\s*\[\d+\]|\s*>>>|$)", doc, flags=re.S)
    return [(int(n), t.strip()) for n, t in pares]


LETRAS_NUM = re.compile(r"\b(una|un|uno|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez)\b", re.I)


def main():
    rep = sys.argv[1] if len(sys.argv) > 1 else "r1"
    off_raw = json.load(open(os.path.join(CACHE, f"escalera-{rep}-v1-off.json"), encoding="utf-8"))
    oras = oraciones_de(off_raw["body_enviado"])
    cifras = [n for n, t in oras if re.search(r"\d", t)]
    numerales = [n for n, t in oras if re.search(r"\d", t) or LETRAS_NUM.search(t)]

    print(f"documento leido del crudo: {len(oras)} oraciones "
          f"(mismo texto en los 4 niveles: {all(oraciones_de(json.load(open(os.path.join(CACHE, f'escalera-{rep}-v1-{x}.json'), encoding='utf-8'))['body_enviado']) == oras for x in NIVELES)})")
    print(f"\noro_cifras    ({len(cifras)}): {cifras}")
    print(f"oro_numerales ({len(numerales)}): {numerales}")
    print("\noraciones discutidas (numeral con letra, sin digito):")
    for n, t in oras:
        if n not in cifras:
            print(f"  [{n:>2}] {'NUMERAL' if LETRAS_NUM.search(t) else '       '} {t[:66]}")

    for nombre, oro in (("oro_cifras", cifras), ("oro_numerales", numerales)):
        print(f"\n=== contra {nombre} ===")
        print(f"{'nivel':5} {'n':>3} {'fp':>20} {'fn':>20}  exacto")
        for nivel in NIVELES:
            d = json.load(open(os.path.join(CACHE, f"escalera-{rep}-v1-{nivel}.json"), encoding="utf-8"))
            valor = (d.get("dato_parseado") or {}).get("dato", {}).get("valor")
            if not isinstance(valor, list):
                print(f"{nivel:5} {'-':>3} {'sin lista':>20} {'sin lista':>20}  no")
                continue
            s = {x for x in valor if isinstance(x, int)}
            fp = sorted(s - set(oro))
            fn = sorted(set(oro) - s)
            ok = not fp and not fn
            print(f"{nivel:5} {len(s):>3} {str(fp):>20} {str(fn):>20}  {'SI' if ok else 'no'}")

    print("\n=== respuesta verbatim de cada nivel ===")
    for nivel in NIVELES:
        d = json.load(open(os.path.join(CACHE, f"escalera-{rep}-v1-{nivel}.json"), encoding="utf-8"))
        val = (d.get("dato_parseado") or {}).get("dato", {})
        print(f"  {nivel:4} out={d['usage'].get('completion_tokens'):>5} {val.get('valor')}")


if __name__ == "__main__":
    main()
