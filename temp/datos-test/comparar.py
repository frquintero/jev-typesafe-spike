#!/usr/bin/env python3
"""Compara dos extracciones de DATOS sobre las mismas unidades: dos prompts, un modelo.

Lee los JSON que dejó `correr.py` (acá al lado), los empareja por parecido de aspecto y escribe
`comparacion-<doc>.md` por cada documento. No toca la base.

Uso:

    python3 temp/datos-test/comparar.py doc9 doc9-haiku-high-d1 doc9-haiku-high-d2
"""

import json
import pathlib
import sys
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
CORTAS = {"de", "del", "la", "el", "los", "las", "que", "en", "con", "por", "al", "un", "una",
          "y", "o", "a", "su", "sus", "se", "lo", "es", "son", "cada", "para", "sobre"}


def llano(texto):
    return "".join(c for c in unicodedata.normalize("NFD", str(texto).lower())
                   if unicodedata.category(c) != "Mn")


def palabras(texto):
    return {p for p in llano(texto).replace(",", " ").replace(".", " ").split()
            if p not in CORTAS and len(p) > 2}


def parecido(a, b):
    unidos = palabras(a) | palabras(b)
    return len(palabras(a) & palabras(b)) / len(unidos) if unidos else 0.0


def unidad_json(ruta):
    d = json.loads(pathlib.Path(ruta).read_text(encoding="utf-8"))
    uso = d.get("usage") or {}
    datos = [dato for u in d.get("salida") or [] for dato in (u.get("datos") or [])]
    return {
        "archivo": pathlib.Path(ruta).stem, "prompt": d.get("prompt"),
        "modelo": d.get("modelo"), "esfuerzo": d.get("esfuerzo"), "segundos": d.get("segundos"),
        "entrada": uso.get("prompt_tokens"), "salida": uso.get("completion_tokens"),
        "pensando": uso.get("thinking_tokens"), "unidades": d.get("salida") or [],
        "datos": len(datos), "con_unidad": sum(1 for x in datos if x.get("unidad_valor")),
        "verificacion": d.get("verificacion"),
    }


def celdas(unidad):
    return [{"aspecto": x.get("aspecto"), "valor": x.get("valor"),
             "unidad_valor": x.get("unidad_valor")} for x in (unidad.get("datos") or [])]


def comparar(doc, *archivos):
    corridas = [unidad_json(AQUI / f"{a}.json") for a in archivos]
    a, b = corridas[0], corridas[1]
    lineas = [f"# Extracción de datos de `{doc}`: dos prompts, un modelo", "",
              "| | " + " | ".join(f"`{c['archivo']}`" for c in corridas) + " |",
              "|---|---|---|"]
    filas = [
        ("prompt", [c["prompt"] for c in corridas]),
        ("segundos", [c["segundos"] for c in corridas]),
        ("tokens de entrada", [c["entrada"] for c in corridas]),
        ("salida (pensando)", [f"{c['salida']} ({c['pensando']})" for c in corridas]),
        ("datos", [c["datos"] for c in corridas]),
        ("con `unidad_valor`", [c["con_unidad"] for c in corridas]),
        ("verificación", ["sin problemas" if not (c["verificacion"] or {}).get("problemas")
                          else "con problemas" for c in corridas]),
    ]
    for etiqueta, fila in filas:
        lineas.append(f"| {etiqueta} | " + " | ".join(str(x) for x in fila) + " |")
    lineas.append("")

    # la proporción de unidad_valor, que es el eje del examen
    lineas += ["## El campo `unidad_valor`", ""]
    for c in corridas:
        lineas.append(f"- **{c['archivo']}**: {c['con_unidad']} de {c['datos']} datos "
                      f"({round(100 * c['con_unidad'] / c['datos']) if c['datos'] else 0} %) con unidad")
    usadas = {c["archivo"]: sorted({x["unidad_valor"] for u in c["unidades"]
                                    for x in (u.get("datos") or []) if x.get("unidad_valor")})
              for c in corridas}
    for nombre, lista in usadas.items():
        lineas.append(f"- unidades de `{nombre}`: {', '.join(f'«{u}»' for u in lista)}")
    lineas.append("")

    # unidad por unidad, emparejando por parecido de aspecto
    lineas += ["## Unidad por unidad", "",
               "Emparejado aproximado por parecido de aspecto (Jaccard sobre las palabras). "
               "`=` par, `+` solo en el primero, `-` solo en el segundo.", ""]
    solo_a = solo_b = pares = 0
    for i, (ua, ub) in enumerate(zip(a["unidades"], b["unidades"]), 1):
        da, db = celdas(ua), celdas(ub)
        usados_b = set()
        filas = []
        for x in da:
            mejor, puntaje = None, 0.0
            for j, y in enumerate(db):
                if j in usados_b:
                    continue
                p = parecido(x["aspecto"], y["aspecto"])
                if p > puntaje:
                    mejor, puntaje = j, p
            if mejor is not None and puntaje >= 0.3:
                usados_b.add(mejor)
                pares += 1
                filas.append(("=", x, db[mejor]))
            else:
                solo_a += 1
                filas.append(("+", x, None))
        for j, y in enumerate(db):
            if j not in usados_b:
                solo_b += 1
                filas.append(("-", None, y))
        lineas.append(f"### n={i} · {ua.get('caso')}")
        lineas.append("")
        lineas.append(f"| | {a['archivo']} | {b['archivo']} |")
        lineas.append("|---|---|---|")
        for marca, x, y in filas:
            def fmt(d):
                if not d:
                    return ""
                u = f" **[{d['unidad_valor']}]**" if d.get("unidad_valor") else ""
                return f"{d['aspecto']} = {d['valor']}{u}"
            lineas.append(f"| {marca} | {fmt(x)} | {fmt(y)} |")
        lineas.append("")
    lineas += [f"**Pares: {pares} · solo en `{a['archivo']}`: {solo_a} · "
               f"solo en `{b['archivo']}`: {solo_b}.**", ""]

    destino = AQUI / f"comparacion-{doc}.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print("\n".join(lineas))
    print(f"  -> {destino}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        raise SystemExit("uso: python3 temp/datos-test/comparar.py <doc> <a> <b>")
    comparar(*sys.argv[1:])
