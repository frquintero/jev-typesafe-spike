#!/usr/bin/env python3
"""Mide el ruido: dos prompts × dos réplicas sobre las mismas unidades.

Empareja los datos de cada par de corridas con la misma vara que `comparar.py` —parecido de aspecto,
Jaccard sobre las palabras— y separa los pares **dentro del mismo prompt** de los pares **entre
prompts**. Si lo de adentro mide tanto como lo de afuera, la diferencia entre prompts no está medida.

Uso:

    python3 temp/datos-test/ruido.py doc9 d1 d2 d1r2 d2r2      (nombres de archivo, sin .json)
"""

import itertools
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from comparar import celdas, parecido, unidad_json  # noqa: E402


def emparejar(a, b, umbral=0.3):
    """Cuántos datos de cada corrida se corresponden, y cuántos quedan sueltos."""
    da = [x for u in a["unidades"] for x in celdas(u)]
    db = [x for u in b["unidades"] for x in celdas(u)]
    usados = set()
    pares = 0
    for x in da:
        mejor, puntaje = None, 0.0
        for j, y in enumerate(db):
            if j in usados:
                continue
            p = parecido(x["aspecto"], y["aspecto"])
            if p > puntaje:
                mejor, puntaje = j, p
        if mejor is not None and puntaje >= umbral:
            usados.add(mejor)
            pares += 1
    solo_a = len(da) - pares
    solo_b = len(db) - len(usados)
    acuerdo = pares / max(len(da), len(db)) if max(len(da), len(db)) else 0.0
    return pares, solo_a, solo_b, acuerdo


def resolver(nombre):
    """Acepta el nombre del archivo o solo el final (`d1` → `doc9-haiku-high-d1.json`)."""
    exacto = AQUI / f"{nombre}.json"
    if exacto.is_file():
        return exacto
    candidatos = sorted(AQUI.glob(f"*{nombre}.json"))
    if len(candidatos) != 1:
        raise SystemExit(f"'{nombre}' no identifica un solo archivo: {candidatos}")
    return candidatos[0]


def ruido(doc, *archivos):
    corridas = {a: unidad_json(resolver(a)) for a in archivos}
    grupos = {}
    for nombre, c in corridas.items():
        grupos.setdefault(c["prompt"], []).append(nombre)

    lineas = [f"# Ruido de la extracción de `{doc}` (mismo modelo, mismas unidades)", "",
              "| corrida | prompt | datos | con `unidad_valor` | segundos | entrada | salida (pensando) |",
              "|---|---|---|---|---|---|---|"]
    for nombre, c in corridas.items():
        lineas.append(f"| `{nombre}` | `{c['prompt']}` | {c['datos']} | {c['con_unidad']} | "
                      f"{c['segundos']} | {c['entrada']} | {c['salida']} ({c['pensando']}) |")
    lineas.append("")

    lineas += ["## Par por par", "",
               "`pares` = datos que se corresponden · `sueltos` = los que quedan sin par · "
               "`acuerdo` = pares / el mayor de los dos.", "",
               "| par | tipo | pares | sueltos | acuerdo |", "|---|---|---|---|---|"]
    dentro, entre, cruces = [], [], []
    for x, y in itertools.combinations(archivos, 2):
        pares, solo_a, solo_b, acuerdo = emparejar(corridas[x], corridas[y])
        mismo_prompt = corridas[x]["prompt"] == corridas[y]["prompt"]
        mismo_modelo = corridas[x]["modelo"] == corridas[y]["modelo"]
        if not mismo_modelo:
            tipo, cubeta = "otro modelo", cruces
        elif mismo_prompt:
            tipo, cubeta = "dentro del prompt", dentro
        else:
            tipo, cubeta = "entre prompts", entre
        cubeta.append((pares, solo_a + solo_b, acuerdo))
        lineas.append(f"| `{x}` vs `{y}` | {tipo} | {pares} | {solo_a} + {solo_b} | "
                      f"{round(100 * acuerdo)} % |")
    lineas.append("")

    def promedio(lista):
        return (sum(p for p, _, _ in lista) / len(lista),
                sum(s for _, s, _ in lista) / len(lista),
                sum(a for _, _, a in lista) / len(lista)) if lista else (0, 0, 0)

    pd, sd, ad = promedio(dentro)
    pe, se, ae = promedio(entre)
    lineas += ["## La cuenta", "",
               f"- **Dentro del mismo prompt** ({len(dentro)} pares): {pd:.0f} datos en pareja, "
               f"{sd:.0f} sueltos, acuerdo {round(100 * ad)} %.",
               f"- **Entre prompts** ({len(entre)} pares): {pe:.0f} datos en pareja, "
               f"{se:.0f} sueltos, acuerdo {round(100 * ae)} %.",
               "",
               f"**El ruido de adentro mide {round(100 * ad)} % y la diferencia entre prompts "
               f"{round(100 * ae)} %** — " +
               ("el prompt nuevo no se distingue del temblor." if abs(ad - ae) < 0.10
                else "hay separación entre los dos."),
               "",
               "Los datos de cada corrida: " +
               ", ".join(f"`{n}` {c['datos']}" for n, c in corridas.items()) + "."]

    destino = AQUI / f"ruido-{doc}.md"
    destino.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    print(f"\n  -> {destino}")


if __name__ == "__main__":
    if len(sys.argv) < 4:
        raise SystemExit("uso: python3 temp/datos-test/ruido.py <doc> <corrida> <corrida> [...]")
    ruido(*sys.argv[1:])
