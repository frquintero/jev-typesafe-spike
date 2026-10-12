#!/usr/bin/env python3
"""Compara las particiones: la del registro contra las de la prueba, oración por oración.

Lee el registro **en solo lectura** —las unidades de un documento y su corrida— y los JSON que dejó
`correr.py` acá al lado. Imprime la comparación y la deja en `comparacion.md`.

Uso:

    python3 temp/ut-haiku/comparar.py doc8
"""

import json
import pathlib
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/ut-haiku → la raíz
AQUI = pathlib.Path(__file__).resolve().parent
DOCUMENTOS = RAIZ / "mvp" / "documentos"
DB = RAIZ / "mvp" / "código" / "corpus.db"


def total_oraciones(doc):
    """Cuántas oraciones tiene el documento (el mismo conteo que hace el corredor)."""
    sys.path.insert(0, str(RAIZ / "mvp" / "código"))
    from extraer_unidades import numerar_oraciones
    for candidata in (DOCUMENTOS / f"{doc}.md", RAIZ / "temp" / f"{doc}.md", AQUI / f"{doc}.md"):
        if candidata.is_file():
            return len(numerar_oraciones(candidata.read_text(encoding="utf-8"))[1])
    raise SystemExit(f"no encuentro '{doc}.md' ni en mvp/documentos/ ni en temp/")


def del_registro(doc):
    """La partición que está en el registro (solo lectura)."""
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    unidades = db.execute("SELECT n, subtema, oraciones FROM unidades WHERE documento_id = ? "
                          "ORDER BY n", (doc,)).fetchall()
    corrida = db.execute("SELECT modelo, esfuerzo, segundos, tokens_salida, tokens_pensando "
                         "FROM corridas WHERE id = ?", (f"{doc}:UT",)).fetchone()
    return {
        "nombre": "registro",
        "modelo": corrida["modelo"] if corrida else "—",
        "esfuerzo": corrida["esfuerzo"] if corrida else "—",
        "segundos": corrida["segundos"] if corrida else None,
        "tokens_salida": corrida["tokens_salida"] if corrida else None,
        "tokens_pensando": corrida["tokens_pensando"] if corrida else None,
        "verificacion": "—",
        "grupos": [(tuple(sorted(int(n) for n in (u["oraciones"] or "").split(",") if n.strip())),
                    u["subtema"]) for u in unidades],
    }


def del_archivo(ruta):
    """La partición de una corrida de la prueba."""
    datos = json.loads(ruta.read_text(encoding="utf-8"))
    uso = datos.get("usage") or {}
    grupos = []
    for subtema in datos.get("subtemas") or []:
        numeros = tuple(sorted(int(n) for n in (subtema.get("oraciones") or [])
                               if isinstance(n, int)))
        grupos.append((numeros, subtema.get("subtema")))
    return {
        "nombre": ruta.stem,
        "modelo": datos.get("modelo"),
        "esfuerzo": datos.get("esfuerzo"),
        "segundos": datos.get("segundos"),
        "tokens_salida": uso.get("completion_tokens"),
        "tokens_pensando": uso.get("thinking_tokens"),
        "verificacion": json.dumps(datos.get("verificacion"), ensure_ascii=False)
        if datos.get("verificacion") else f"no se pudo leer: {datos.get('error_parseo')}",
        "grupos": grupos,
    }


def comparar(doc):
    oraciones = total_oraciones(doc)
    corridas = [del_registro(doc)]
    corridas += [del_archivo(ruta) for ruta in sorted(AQUI.glob("*.json"))
                 if json.loads(ruta.read_text(encoding="utf-8")).get("doc") == doc]
    corridas = [c for c in corridas if c["grupos"]]

    lineas = [f"# Particiones de `{doc}` ({oraciones} oraciones)", ""]

    # 1) las corridas y su costo
    lineas += ["## Las corridas", "",
               "| corrida | modelo | esfuerzo | unidades | segundos | tokens salida (pensando) | verificación |",
               "|---|---|---|---|---|---|---|"]
    for c in corridas:
        lineas.append(f"| {c['nombre']} | {c['modelo']} | {c['esfuerzo']} | {len(c['grupos'])} | "
                      f"{c['segundos']} | {c['tokens_salida']} ({c['tokens_pensando']}) | "
                      f"{c['verificacion']} |")

    # 2) la partición de cada una
    lineas += ["", "## La partición de cada una", ""]
    for c in corridas:
        lineas.append(f"**{c['nombre']}** ({len(c['grupos'])} unidades)")
        lineas.append("")
        for numeros, nombre in c["grupos"]:
            lineas.append(f"- `[{','.join(str(n) for n in numeros)}]` {nombre}")
        lineas.append("")

    # 3) oración por oración: el grupo (los números que lo acompañan) en cada corrida
    por_corrida = [{n: numeros for numeros, _ in c["grupos"] for n in numeros} for c in corridas]
    lineas += [f"## Oración por oración (el grupo al que fue)", "",
               "| oración | " + " | ".join(c["nombre"] for c in corridas) + " |",
               "|---" * (len(corridas) + 1) + "|"]
    distintas = []
    for n in range(1, oraciones + 1):
        celdas = [",".join(str(x) for x in por_corrida[i].get(n, ())) for i in range(len(corridas))]
        lineas.append(f"| {n} | " + " | ".join(celdas) + " |")
        if len(set(celdas)) > 1:
            distintas.append(n)
    lineas.append("")

    # 4) qué coincide y qué no
    particiones = {frozenset(frozenset(g) for g, _ in c["grupos"]) for c in corridas}
    iguales = [c["nombre"] for c in corridas
               if frozenset(frozenset(g) for g, _ in c["grupos"])
               == frozenset(frozenset(g) for g, _ in corridas[0]["grupos"])]
    lineas += ["## Qué coincide y qué no", "",
               f"- Iguales a la del registro: {', '.join(iguales)}.",
               f"- Particiones distintas entre sí: {'sí' if len(particiones) > 1 else 'no'}.",
               f"- Oraciones donde no todas coinciden: "
               f"{', '.join(str(n) for n in distintas) if distintas else 'ninguna'}."]
    conteo = {}
    for c in corridas:
        for grupo, _ in c["grupos"]:
            conteo.setdefault(grupo, []).append(c["nombre"])
    solo_uno = [g for g, quienes in conteo.items() if len(set(quienes)) == 1]
    if solo_uno:
        lineas.append("- Grupos que aparecen en una sola corrida: "
                      + "; ".join(f"`[{','.join(str(n) for n in g)}]` ({conteo[g][0]})"
                                  for g in sorted(solo_uno, key=min)))
    lineas.append("")

    texto = "\n".join(lineas)
    (AQUI / f"comparacion-{doc}.md").write_text(texto, encoding="utf-8")
    print(texto)
    print(f"  -> {AQUI / f'comparacion-{doc}.md'}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("uso: python3 temp/ut-haiku/comparar.py <doc>")
    comparar(sys.argv[1])
