#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validador de tablas de A(Q) — prueba de mesa 1 (MVP de Zettel).

Sin API de modelos; solo biblioteca estándar.

Uso:
    python3 validar.py tablas.json
    python3 validar.py --comparar a.json b.json

Qué revisa por pregunta:
  1. estados válidos (admisible / inadmisible);
  2. fila «resto» en cada tabla;
  3. ids de ruta existentes en dependencias, y cada dependencia con valor,
     procedencia y fecha;
  4. tabla inicial = solo «resto admisible, sin ruta»;
  5. diff inicial->final (y final->revisada) clasificado en los tres modos
     del marco: dejan de ser admisibles / ganan o pierden sostén / aparecen
     distinciones;
  6. condición de entrega 1 (diff != vacío) y 2 (si R = «solo el documento»,
     ninguna dependencia de tipo dato con procedencia K);
  7. cuenta y marca las filas admisibles sin ruta (no son error).
"""

import json
import sys

ESTADOS = ("admisible", "inadmisible")
TIPOS = ("dato", "regla")
TABLAS = ("tabla_inicial", "tabla_final", "tabla_revisada")
TABLAS_REQUERIDAS = ("tabla_inicial", "tabla_final")
COLS = ("si", "estado", "ruta")


# ---------------------------------------------------------------- utilidades

def cargar(ruta):
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    if isinstance(datos, dict):
        datos = [datos]
    if not isinstance(datos, list):
        raise SystemExit("se esperaba una lista de preguntas en %s" % ruta)
    return datos


def por_id(datos):
    return {q.get("id"): q for q in datos}


def filas(tabla):
    if not isinstance(tabla, list):
        return {}
    return {r.get("posicion"): r for r in tabla if isinstance(r, dict)}


def get_row(tabla, pos):
    """Fila de `pos`; si no está listada, la fila «resto» (decisión 3)."""
    fs = filas(tabla)
    if pos in fs:
        return fs[pos]
    return fs.get("resto")


def tabla_inicial_ok(tabla):
    if not isinstance(tabla, list) or len(tabla) != 1:
        return False
    r = tabla[0]
    return (r.get("posicion") == "resto" and r.get("si") is None
            and r.get("estado") == "admisible" and r.get("ruta") == [])


# --------------------------------------------------------------------- diff

def diff_tablas(vieja, nueva):
    """Clasifica el cambio entre dos tablas en los tres modos del marco."""
    v, n = filas(vieja), filas(nueva)
    dejan, sosten = [], []
    for pos in dict.fromkeys(list(n.keys()) + list(v.keys())):
        rv, rn = get_row(vieja, pos), get_row(nueva, pos)
        if rv is None or rn is None:
            continue
        if rv.get("estado") == "admisible" and rn.get("estado") == "inadmisible":
            dejan.append(pos)
        elif (rv.get("estado") == rn.get("estado")
              and (rv.get("ruta") != rn.get("ruta")
                   or rv.get("si") != rn.get("si"))):
            sosten.append(pos)
    explicitas = [r for r in (nueva or [])
                  if isinstance(r, dict) and r.get("posicion") != "resto"
                  and r.get("estado") == "admisible"]
    sis = {r.get("si") for r in explicitas if r.get("si") is not None}
    distinciones = []
    if len(explicitas) >= 2 or sis:
        viejas = set(v.keys())
        distinciones = [r.get("posicion") for r in explicitas
                        if r.get("posicion") not in viejas]
        if not distinciones:
            distinciones = [r.get("posicion") for r in explicitas]
    return {
        "dejan_de_ser_admisibles": dejan,
        "ganan_o_pierden_sosten": sosten,
        "aparecen_distinciones": distinciones,
    }


def hay_diff(d):
    return any(d[k] for k in d)


def resumen_diff(d):
    partes = []
    if d["dejan_de_ser_admisibles"]:
        partes.append("dejan de ser admisibles: "
                      + ", ".join(d["dejan_de_ser_admisibles"]))
    if d["ganan_o_pierden_sosten"]:
        partes.append("ganan o pierden sostén: "
                      + ", ".join(d["ganan_o_pierden_sosten"]))
    if d["aparecen_distinciones"]:
        partes.append("aparecen distinciones: "
                      + ", ".join(d["aparecen_distinciones"]))
    return "; ".join(partes) if partes else "(sin efecto)"


# --------------------------------------------------------- validar pregunta

def validar_pregunta(q):
    qid = q.get("id", "?")
    errores = []
    print("== %s ==" % qid)
    print("  pregunta: %s" % q.get("pregunta", "(falta)"))
    R = q.get("R") or {}
    fuentes = R.get("fuentes")
    print("  R: %s" % (fuentes if fuentes else "(falta)"))

    deps = q.get("dependencias") or []
    dep_ids = set()
    for d in deps:
        di = d.get("id")
        if di:
            dep_ids.add(di)
        else:
            errores.append("dependencia sin id")
        if d.get("tipo") not in TIPOS:
            errores.append("dependencia %s: tipo inválido %r"
                           % (di, d.get("tipo")))
        faltan = [c for c in ("valor", "procedencia", "fecha") if not d.get(c)]
        if faltan:
            errores.append("dependencia %s: sin %s" % (di, ", ".join(faltan)))

    presentes = []
    usadas = set()
    for nombre in TABLAS:
        if nombre not in q:
            continue
        t = q[nombre]
        if not isinstance(t, list):
            errores.append("%s no es una lista" % nombre)
            continue
        presentes.append(nombre)
        for r in t:
            if not isinstance(r, dict):
                errores.append("%s: fila que no es objeto" % nombre)
                continue
            if r.get("estado") not in ESTADOS:
                errores.append("%s: estado inválido %r"
                               % (nombre, r.get("estado")))
            if not r.get("posicion"):
                errores.append("%s: fila sin posición" % nombre)
            usadas.update(r.get("ruta") or [])
        if "resto" not in filas(t):
            errores.append("%s: falta la fila «resto»" % nombre)

    for nombre in TABLAS_REQUERIDAS:
        if nombre not in q:
            errores.append("falta %s" % nombre)
    if qid == "P4" and "tabla_revisada" not in q:
        errores.append("P4: falta tabla_revisada")

    huerfanas = sorted(usadas - dep_ids)
    if huerfanas:
        errores.append("ids de ruta sin dependencia: " + ", ".join(huerfanas))

    if "tabla_inicial" in q and not tabla_inicial_ok(q.get("tabla_inicial")):
        errores.append("tabla_inicial no es solo «resto admisible, sin ruta»")

    # 7. admisibles sin ruta (no es error)
    for nombre in presentes:
        sin_ruta = [r.get("posicion") for r in q[nombre]
                    if isinstance(r, dict) and r.get("estado") == "admisible"
                    and not (r.get("ruta") or [])]
        if sin_ruta:
            print("  [nota] %s: admisibles sin ruta (no es error): %s"
                  % (nombre, ", ".join(sin_ruta)))

    # 5. diff
    efectos = []
    if "tabla_inicial" in q and "tabla_final" in q:
        d1 = diff_tablas(q["tabla_inicial"], q["tabla_final"])
        print("  diff inicial->final: %s" % resumen_diff(d1))
        print("    %s" % json.dumps(d1, ensure_ascii=False))
        efectos.append(d1)
    if "tabla_final" in q and "tabla_revisada" in q:
        d2 = diff_tablas(q["tabla_final"], q["tabla_revisada"])
        print("  diff final->revisada: %s" % resumen_diff(d2))
        print("    %s" % json.dumps(d2, ensure_ascii=False))
        efectos.append(d2)

    # 6. condiciones de entrega
    con_efecto = any(hay_diff(d) for d in efectos)
    print("  condición 1 (diff != vacío): %s" % ("SÍ" if con_efecto else "NO"))
    if fuentes == "solo el documento":
        k_datos = [d.get("id") for d in deps
                   if d.get("tipo") == "dato"
                   and str(d.get("procedencia", "")).startswith("K")]
        print("  condición 2 (solo el documento, sin datos K): %s"
              % ("NO" if k_datos else "SÍ"))
        if k_datos:
            errores.append("R = «solo el documento» con datos K: "
                           + ", ".join(k_datos))
    else:
        print("  condición 2: no aplica (R = %s)" % (fuentes or "?"))

    print("  salida esperada (JSON): %s" % q.get("salida_esperada", "(falta)"))
    if errores:
        print("  [ERRORES]")
        for e in errores:
            print("    - %s" % e)
    print()
    return errores, con_efecto, len(dep_ids), len(presentes), len(usadas)


# ----------------------------------------------------------------- comparar

def comparar(na, nb, datos_a, datos_b):
    ia, ib = por_id(datos_a), por_id(datos_b)
    print("== comparar %s vs %s ==" % (na, nb))
    celdas = 0
    for qid in dict.fromkeys(list(ia.keys()) + list(ib.keys())):
        if qid not in ia:
            print("%s: solo en %s" % (qid, nb))
            celdas += 1
            continue
        if qid not in ib:
            print("%s: solo en %s" % (qid, na))
            celdas += 1
            continue
        qa, qb = ia[qid], ib[qid]
        lineas = []
        if (qa.get("R") or {}) != (qb.get("R") or {}):
            lineas.append("R.fuentes: %r -> %r"
                          % ((qa.get("R") or {}).get("fuentes"),
                             (qb.get("R") or {}).get("fuentes")))
        if (qa.get("encabezado") or {}) != (qb.get("encabezado") or {}):
            lineas.append("encabezado: %s -> %s"
                          % (json.dumps(qa.get("encabezado"),
                                        ensure_ascii=False),
                             json.dumps(qb.get("encabezado"),
                                        ensure_ascii=False)))
        for nombre in TABLAS:
            ta, tb = qa.get(nombre), qb.get(nombre)
            if ta is None and tb is None:
                continue
            fa, fb = filas(ta), filas(tb)
            for pos in dict.fromkeys(list(fa.keys()) + list(fb.keys())):
                ra, rb = fa.get(pos), fb.get(pos)
                if ra is None:
                    lineas.append("%s[%s]: solo en %s -> %s"
                                  % (nombre, pos, nb,
                                     json.dumps(rb, ensure_ascii=False)))
                elif rb is None:
                    lineas.append("%s[%s]: solo en %s -> %s"
                                  % (nombre, pos, na,
                                     json.dumps(ra, ensure_ascii=False)))
                else:
                    for col in COLS:
                        if ra.get(col) != rb.get(col):
                            lineas.append("%s[%s].%s: %s -> %s"
                                          % (nombre, pos, col,
                                             json.dumps(ra.get(col),
                                                        ensure_ascii=False),
                                             json.dumps(rb.get(col),
                                                        ensure_ascii=False)))
        if lineas:
            print("%s:" % qid)
            for l in lineas:
                print("  %s" % l)
            celdas += len(lineas)
    print("  celdas distintas: %d" % celdas)


# --------------------------------------------------------------------- main

def main(argv):
    if len(argv) == 4 and argv[1] == "--comparar":
        comparar(argv[2], argv[3], cargar(argv[2]), cargar(argv[3]))
        return 0
    if len(argv) != 2:
        print(__doc__)
        return 2
    datos = cargar(argv[1])
    todos = []
    con_efecto = 0
    for q in datos:
        es, ef, _, _, _ = validar_pregunta(q)
        todos.extend("%s: %s" % (q.get("id", "?"), e) for e in es)
        con_efecto += 1 if ef else 0
    print("== resumen ==")
    print("  preguntas: %d" % len(datos))
    print("  errores: %d" % len(todos))
    for e in todos:
        print("    [ERROR] %s" % e)
    print("  preguntas con efecto (condición 1): %d/%d"
          % (con_efecto, len(datos)))
    return 1 if todos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
