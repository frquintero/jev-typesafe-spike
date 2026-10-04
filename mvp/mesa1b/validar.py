#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validador de tablas de A(Q) — prueba de mesa 1b (MVP de Zettel).

Sin API de modelos; solo biblioteca estándar.

Uso:
    python3 validar.py tablas.json
    python3 validar.py --comparar a.json b.json

Esquema nuevo: cada tabla es {"filas": [...], "conflicto": [ids], "campo":
[ids]}. Cada fila es posicion · si · estado · ruta, con fila «resto».
`dependencias` = solo lo que aparece en alguna ruta; `datos` declara los ids
de `campo` que son mudos (id y valor). `desenlace` ∈ {cerrada, no establecido,
no cerrable}.

Qué revisa por pregunta:
  1. formato de tabla y campos; todo id de ruta, conflicto y campo existe
     (los de campo mudos, declarados en `datos`);
  2. diff en cuatro clases: cambian de estado (admisible→inadmisible y
     inadmisible→admisible, por separado); ganan o pierden sostén (fila
     admisible que cambia de ruta o cuyos ids entran en conflicto); cambia la
     razón de exclusión (fila inadmisible que cambia de ruta); aparecen
     distinciones (filas nuevas o cambio en `si`);
  3. coherencia del desenlace: «no establecido» ⇒ diff vacío; «cerrada» ⇒
     exactamente una fila admisible y resto inadmisible en tabla_final;
     «no cerrable» ⇒ resto admisible en tabla_final;
  4. condición 2 (R «solo el documento» ⇒ sin dependencias K de tipo dato) y
     condición 3 (si hay `conflicto`, avisar y exigir salida_esperada);
  5. cuenta y marca las filas admisibles sin ruta (no son error).
"""

import json
import sys

ESTADOS = ("admisible", "inadmisible")
TIPOS = ("dato", "regla")
TABLAS = ("tabla_inicial", "tabla_final", "tabla_revisada")
TABLAS_REQUERIDAS = ("tabla_inicial", "tabla_final")
DESENLACES = ("cerrada", "no establecido", "no cerrable")
COLS = ("si", "estado", "ruta")
CAMPOS_DEP = ("tipo", "valor", "procedencia", "fecha")


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
    if not isinstance(tabla, dict):
        return {}
    fs = tabla.get("filas")
    if not isinstance(fs, list):
        return {}
    return {r.get("posicion"): r for r in fs if isinstance(r, dict)}


def get_row(tabla, pos):
    """Fila de `pos`; si no está listada, la fila «resto»."""
    fs = filas(tabla)
    if pos in fs:
        return fs[pos]
    return fs.get("resto")


def conflicto(tabla):
    if not isinstance(tabla, dict):
        return []
    c = tabla.get("conflicto")
    return list(c) if isinstance(c, list) else []


def campo(tabla):
    if not isinstance(tabla, dict):
        return []
    c = tabla.get("campo")
    return list(c) if isinstance(c, list) else []


def tabla_inicial_ok(tabla):
    if not isinstance(tabla, dict):
        return False
    fs = tabla.get("filas")
    if not isinstance(fs, list) or len(fs) != 1:
        return False
    r = fs[0]
    return (r.get("posicion") == "resto" and r.get("si") is None
            and r.get("estado") == "admisible" and r.get("ruta") == []
            and conflicto(tabla) == [] and campo(tabla) == [])


# --------------------------------------------------------------------- diff

def diff_tablas(vieja, nueva):
    """Clasifica el cambio entre dos tablas en las cuatro clases del marco."""
    v, n = filas(vieja), filas(nueva)
    adm_a_inadm, inadm_a_adm = [], []
    gana_pierde, razon = [], []
    conf_v, conf_n = set(conflicto(vieja)), set(conflicto(nueva))
    for pos in dict.fromkeys(list(n.keys()) + list(v.keys())):
        rv, rn = get_row(vieja, pos), get_row(nueva, pos)
        if rv is None or rn is None:
            continue
        ev, en = rv.get("estado"), rn.get("estado")
        if ev == "admisible" and en == "inadmisible":
            adm_a_inadm.append(pos)
        elif ev == "inadmisible" and en == "admisible":
            inadm_a_adm.append(pos)
        if ev == "admisible" and en == "admisible":
            cambio_ruta = rv.get("ruta") != rn.get("ruta")
            toca_conflicto = bool((conf_v ^ conf_n) & set(rn.get("ruta") or []))
            if cambio_ruta or toca_conflicto:
                gana_pierde.append(pos)
        if (ev == "inadmisible" and en == "inadmisible"
                and rv.get("ruta") != rn.get("ruta")):
            razon.append(pos)
    distinciones = []
    for pos, rn in n.items():
        if pos not in v:
            distinciones.append(pos)
        elif v[pos].get("si") != rn.get("si"):
            distinciones.append(pos)
    return {
        "cambian_de_estado": {
            "admisible_a_inadmisible": adm_a_inadm,
            "inadmisible_a_admisible": inadm_a_adm,
        },
        "ganan_o_pierden_sosten": gana_pierde,
        "cambia_la_razon_de_exclusion": razon,
        "aparecen_distinciones": distinciones,
    }


def hay_diff(d):
    ce = d["cambian_de_estado"]
    return bool(ce["admisible_a_inadmisible"] or ce["inadmisible_a_admisible"]
                or d["ganan_o_pierden_sosten"]
                or d["cambia_la_razon_de_exclusion"]
                or d["aparecen_distinciones"])


def resumen_diff(d):
    partes = []
    ce = d["cambian_de_estado"]
    if ce["admisible_a_inadmisible"]:
        partes.append("admisible→inadmisible: "
                      + ", ".join(ce["admisible_a_inadmisible"]))
    if ce["inadmisible_a_admisible"]:
        partes.append("inadmisible→admisible: "
                      + ", ".join(ce["inadmisible_a_admisible"]))
    if d["ganan_o_pierden_sosten"]:
        partes.append("ganan o pierden sostén: "
                      + ", ".join(d["ganan_o_pierden_sosten"]))
    if d["cambia_la_razon_de_exclusion"]:
        partes.append("cambia la razón de exclusión: "
                      + ", ".join(d["cambia_la_razon_de_exclusion"]))
    if d["aparecen_distinciones"]:
        partes.append("aparecen distinciones: "
                      + ", ".join(d["aparecen_distinciones"]))
    return "; ".join(partes) if partes else "(sin efecto)"


# --------------------------------------------------------- validar pregunta

def validar_pregunta(q):
    qid = q.get("id", "?")
    errores = []
    avisos = []
    print("== %s ==" % qid)
    print("  pregunta: %s" % q.get("pregunta", "(falta)"))
    R = q.get("R") or {}
    fuentes = R.get("fuentes")
    print("  R: %s" % (fuentes if fuentes else "(falta)"))
    des = q.get("desenlace")
    print("  desenlace: %s" % (des if des else "(falta)"))

    enc = q.get("encabezado") or {}
    caso = enc.get("caso")
    if isinstance(caso, dict):
        if not caso.get("nombre") or not caso.get("id"):
            errores.append("encabezado.caso: falta nombre o id")
    elif not caso:
        errores.append("encabezado: falta caso")
    if not enc.get("aspecto"):
        errores.append("encabezado: falta aspecto")

    # dependencias (solo lo que aparece en alguna ruta)
    deps = q.get("dependencias") or []
    dep_ids = set()
    dep_tipos = {}
    for d in deps:
        di = d.get("id")
        if di:
            dep_ids.add(di)
        else:
            errores.append("dependencia sin id")
        dep_tipos[di] = d.get("tipo")
        if d.get("tipo") not in TIPOS:
            errores.append("dependencia %s: tipo inválido %r"
                           % (di, d.get("tipo")))
        faltan = [c for c in ("valor", "procedencia", "fecha") if not d.get(c)]
        if faltan:
            errores.append("dependencia %s: sin %s" % (di, ", ".join(faltan)))

    # datos mudos declarados
    datos = q.get("datos") or []
    datos_ids = set()
    for d in datos:
        di = d.get("id")
        if not di:
            errores.append("dato sin id")
        if not d.get("valor"):
            errores.append("dato %s: sin valor" % di)
        datos_ids.add(di)

    # tablas
    presentes = []
    usadas = set()
    conflictos = set()
    campos = set()
    for nombre in TABLAS:
        if nombre not in q:
            continue
        t = q[nombre]
        if not isinstance(t, dict):
            errores.append("%s: no es un objeto {filas, conflicto, campo}"
                           % nombre)
            continue
        if not isinstance(t.get("filas"), list):
            errores.append("%s: 'filas' no es lista" % nombre)
            continue
        for key in ("conflicto", "campo"):
            if not isinstance(t.get(key, []), list):
                errores.append("%s: '%s' no es lista" % (nombre, key))
        presentes.append(nombre)
        for r in t["filas"]:
            if not isinstance(r, dict):
                errores.append("%s: fila que no es objeto" % nombre)
                continue
            if r.get("estado") not in ESTADOS:
                errores.append("%s: estado inválido %r en %r"
                               % (nombre, r.get("estado"), r.get("posicion")))
            if not r.get("posicion"):
                errores.append("%s: fila sin posición" % nombre)
            usadas.update(r.get("ruta") or [])
        if "resto" not in filas(t):
            errores.append("%s: falta la fila «resto»" % nombre)
        conflictos.update(conflicto(t))
        campos.update(campo(t))

    for nombre in TABLAS_REQUERIDAS:
        if nombre not in q:
            errores.append("falta %s" % nombre)
    for qrev in ("Q5", "Q6"):
        if qid == qrev and "tabla_revisada" not in q:
            errores.append("%s: falta tabla_revisada" % qid)

    # 1. ids
    huerfanas = sorted(usadas - dep_ids)
    if huerfanas:
        errores.append("ids de ruta sin dependencia: " + ", ".join(huerfanas))
    dep_sin_ruta = sorted(dep_ids - usadas)
    if dep_sin_ruta:
        errores.append("dependencias que no aparecen en ninguna ruta: "
                       + ", ".join(dep_sin_ruta))
    conf_huerfanos = sorted(conflictos - dep_ids)
    if conf_huerfanos:
        errores.append("ids de conflicto sin dependencia: "
                       + ", ".join(conf_huerfanos))
    campo_huerfanos = sorted(campos - (dep_ids | datos_ids))
    if campo_huerfanos:
        errores.append("ids de campo sin dependencia ni dato declarado: "
                       + ", ".join(campo_huerfanos))
    mudos = sorted(campos - usadas)
    if mudos:
        print("  [nota] campo mudo (considerado y sin ruta): %s"
              % ", ".join(mudos))
        for m in mudos:
            if m not in datos_ids:
                errores.append("campo mudo %s no declarado en 'datos'" % m)

    # aviso: una regla genérica no excluye
    for nombre in presentes:
        for r in q[nombre].get("filas", []):
            if not isinstance(r, dict) or r.get("estado") != "inadmisible":
                continue
            for rid in (r.get("ruta") or []):
                if dep_tipos.get(rid) == "regla":
                    avisos.append("%s/%s: la regla %s aparece en la ruta de "
                                  "exclusión de «%s»; revisar si es genérica "
                                  "(un genérico solo sostiene)"
                                  % (qid, nombre, rid, r.get("posicion")))

    if "tabla_inicial" in q and not tabla_inicial_ok(q.get("tabla_inicial")):
        errores.append("tabla_inicial no es solo «resto admisible, sin ruta, "
                       "sin conflicto ni campo»")

    # 5. admisibles sin ruta (no es error)
    for nombre in presentes:
        sin_ruta = [r.get("posicion") for r in q[nombre].get("filas", [])
                    if isinstance(r, dict)
                    and r.get("estado") == "admisible"
                    and not (r.get("ruta") or [])]
        if sin_ruta:
            print("  [nota] %s: admisibles sin ruta (no es error): %s"
                  % (nombre, ", ".join(sin_ruta)))

    # 2. diff
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
    con_efecto = any(hay_diff(d) for d in efectos)
    print("  efecto: %s" % ("SÍ" if con_efecto else "NO"))

    # 3. coherencia del desenlace
    if des not in DESENLACES:
        errores.append("desenlace inválido %r" % des)
    else:
        if des == "no establecido" and con_efecto:
            errores.append("desenlace «no establecido» pero el diff no es vacío")
        if des == "cerrada":
            fs = filas(q.get("tabla_final"))
            adm = [p for p, r in fs.items()
                   if p != "resto" and r.get("estado") == "admisible"]
            resto = fs.get("resto")
            if len(adm) != 1 or resto is None or resto.get("estado") != "inadmisible":
                errores.append("desenlace «cerrada» exige una sola fila "
                               "admisible y resto inadmisible en tabla_final "
                               "(hay %d admisibles)" % len(adm))
        if des == "no cerrable":
            resto = filas(q.get("tabla_final")).get("resto")
            if resto is None or resto.get("estado") != "admisible":
                errores.append("desenlace «no cerrable» exige resto admisible "
                               "en tabla_final")

    # 4. condiciones 2 y 3
    if fuentes == "solo el documento":
        k_datos = [d.get("id") for d in deps
                   if d.get("tipo") == "dato"
                   and str(d.get("procedencia", "")).startswith("K")]
        print("  condición 2 (solo el documento, sin datos K): %s"
              % ("NO" if k_datos else "SÍ"))
        if k_datos:
            errores.append("R = «solo el documento» con datos K: "
                           + ", ".join(k_datos))
        k_mudos = [d.get("id") for d in datos
                   if str(d.get("id", "")).startswith("K")]
        if k_mudos:
            avisos.append("R = «solo el documento» y datos mudos con id K: "
                          + ", ".join(k_mudos))
    else:
        print("  condición 2: no aplica (R = %s)" % (fuentes or "?"))

    if conflictos:
        sal = q.get("salida_esperada") or ""
        print("  condición 3 (conflicto ⇒ salida): conflicto=%s; "
              "salida_esperada %s"
              % (sorted(conflictos), "presente" if sal else "VACÍA"))
        if not sal:
            errores.append("hay conflicto %s pero salida_esperada vacía"
                           % sorted(conflictos))
        else:
            avisos.append("conflicto %s declarado; salida_esperada presente"
                          % sorted(conflictos))

    print("  salida esperada (JSON): %s" % q.get("salida_esperada", "(falta)"))
    if avisos:
        print("  [avisos]")
        for a in avisos:
            print("    - %s" % a)
    if errores:
        print("  [ERRORES]")
        for e in errores:
            print("    - %s" % e)
    print()
    return errores, avisos, con_efecto


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
        if qa.get("desenlace") != qb.get("desenlace"):
            lineas.append("desenlace: %r -> %r"
                          % (qa.get("desenlace"), qb.get("desenlace")))
        # dependencias
        da = {d.get("id"): d for d in (qa.get("dependencias") or [])}
        db = {d.get("id"): d for d in (qb.get("dependencias") or [])}
        for did in dict.fromkeys(list(da.keys()) + list(db.keys())):
            if did not in da:
                lineas.append("dependencias[%s]: solo en %s" % (did, nb))
            elif did not in db:
                lineas.append("dependencias[%s]: solo en %s" % (did, na))
            else:
                for col in CAMPOS_DEP:
                    if da[did].get(col) != db[did].get(col):
                        lineas.append("dependencias[%s].%s: %s -> %s"
                                      % (did, col,
                                         json.dumps(da[did].get(col),
                                                    ensure_ascii=False),
                                         json.dumps(db[did].get(col),
                                                    ensure_ascii=False)))
        # datos
        ma = {d.get("id"): d for d in (qa.get("datos") or [])}
        mb = {d.get("id"): d for d in (qb.get("datos") or [])}
        for did in dict.fromkeys(list(ma.keys()) + list(mb.keys())):
            if did not in ma:
                lineas.append("datos[%s]: solo en %s" % (did, nb))
            elif did not in mb:
                lineas.append("datos[%s]: solo en %s" % (did, na))
            elif ma[did].get("valor") != mb[did].get("valor"):
                lineas.append("datos[%s].valor: %s -> %s"
                              % (did,
                                 json.dumps(ma[did].get("valor"),
                                            ensure_ascii=False),
                                 json.dumps(mb[did].get("valor"),
                                            ensure_ascii=False)))
        # tablas
        for nombre in TABLAS:
            ta, tb = qa.get(nombre), qb.get(nombre)
            if ta is None and tb is None:
                continue
            if ta is None or tb is None:
                lineas.append("%s: solo en %s" % (nombre, nb if ta is None else na))
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
            if sorted(conflicto(ta)) != sorted(conflicto(tb)):
                lineas.append("%s.conflicto: %s -> %s"
                              % (nombre,
                                 json.dumps(conflicto(ta), ensure_ascii=False),
                                 json.dumps(conflicto(tb), ensure_ascii=False)))
            if sorted(campo(ta)) != sorted(campo(tb)):
                lineas.append("%s.campo: %s -> %s"
                              % (nombre,
                                 json.dumps(campo(ta), ensure_ascii=False),
                                 json.dumps(campo(tb), ensure_ascii=False)))
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
    todos, avisos_todos = [], []
    con_efecto = 0
    for q in datos:
        es, av, ef = validar_pregunta(q)
        todos.extend("%s: %s" % (q.get("id", "?"), e) for e in es)
        avisos_todos.extend("%s: %s" % (q.get("id", "?"), a) for a in av)
        con_efecto += 1 if ef else 0
    print("== resumen ==")
    print("  preguntas: %d" % len(datos))
    print("  errores: %d" % len(todos))
    for e in todos:
        print("    [ERROR] %s" % e)
    print("  avisos: %d" % len(avisos_todos))
    for a in avisos_todos:
        print("    [AVISO] %s" % a)
    print("  preguntas con efecto: %d/%d" % (con_efecto, len(datos)))
    return 1 if todos else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
