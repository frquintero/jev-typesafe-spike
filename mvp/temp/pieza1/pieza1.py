#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Pieza 1 de la MVP de Zettel: verificador de forma y comparador de tablas de A(Q).

Esquema candidato: mvp/temp/pieza1/esquema2.md (sello "2-candidato").
Sin API de modelos; solo biblioteca estándar.

Uso:
    python3 pieza1.py verificar <tablas.json>
    python3 pieza1.py comparar <a.json> <b.json>
    python3 pieza1.py guardar <tablas.json> <corpus.jsonl>
    python3 pieza1.py mantener <corpus.jsonl> <id_dependencia> "<valor nuevo>"

Las tablas pueden venir como {"preguntas": [...]} o como lista.
El verificador de forma (formato, sintaxis, cálculos y consistencia; no
juzga si una ruta sostiene) solo informa errores (no hay avisos). El comparador lista cada
diferencia en una línea, sin clasificarla.
"""

import copy
import datetime
import json
import re
import sys

SELLO = "2-candidato"

# esquema2.md §3: lista cerrada de R.
R_LISTA = (
    "solo el documento",
    "sin externas, con el mundo del orquestador",
    "libre",
)

# Qué categorías (por origen/mundo, nunca por la letra del id) admite cada R.
# Claves: "D" = origen documento; "M-orquestador", "M-fuente", "M-codigo".
R_ADMITE = {
    "solo el documento": {"D": True, "M-orquestador": False,
                           "M-fuente": False, "M-codigo": True},
    "sin externas, con el mundo del orquestador":
        {"D": True, "M-orquestador": True,
         "M-fuente": False, "M-codigo": True},
    "libre": {"D": True, "M-orquestador": True,
              "M-fuente": True, "M-codigo": True},
}

DESENLACES = ("cerrada", "en conflicto", "no establecido", "no cerrable")
ESTADOS = ("admisible", "inadmisible")
TABLAS_ORDEN = ("tabla_inicial", "tabla_final", "tabla_revisada")

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    "ene": 1, "feb": 2, "mar": 3, "abr": 4, "may": 5, "jun": 6,
    "jul": 7, "ago": 8, "sep": 9, "sept": 9, "set": 9, "oct": 10,
    "nov": 11, "dic": 12,
}

RE_NUM = re.compile(r"(\d{1,2})\s*-\s*(\d{1,2})\s*-\s*(\d{4})")
RE_LARGA = re.compile(r"(\d{1,2})\s+de\s+([a-z\xe1\xe9\xed\xf3\xfa\xfc\xf1]+)"
                      r"\s+de\s+(\d{4})", re.IGNORECASE)
RE_COND_REF = re.compile(r"^(.*)\s+\(([^()]+)\)\s*$")
RE_CIERRE = re.compile(r"del\s+(\d{1,2})\s+al\s+(\d{1,2})\s+de\s+"
                       r"([a-z\xe1\xe9\xed\xf3\xfa\xfc\xf1]+)",
                       re.IGNORECASE)


# ------------------------------------------------------------- carga y base

def cargar_preguntas(ruta):
    """Devuelve (sello superior o None, lista de preguntas)."""
    with open(ruta, encoding="utf-8") as f:
        datos = json.load(f)
    if isinstance(datos, dict) and isinstance(datos.get("preguntas"), list):
        return datos.get("esquema"), datos["preguntas"]
    if isinstance(datos, list):
        return None, datos
    if isinstance(datos, dict) and "pregunta" in datos:
        return datos.get("esquema"), [datos]
    raise SystemExit("en %s: se esperaba {\"preguntas\": [...]} o una lista"
                     % ruta)


def qid(q):
    return q.get("pregunta", q.get("id", "?"))


def norm_r(q):
    r = q.get("R")
    if isinstance(r, dict):
        r = r.get("fuentes", r.get("R"))
    return r


def categoria_dep(d):
    """Categoría por origen/mundo (§2): D, M-orquestador, M-fuente, M-codigo.

    Devuelve (categoria, etiqueta) o (None, motivo) si origen/mundo inválidos.
    """
    origen = (d.get("origen") or "").strip().lower()
    mundo = (d.get("mundo") or "").strip().lower()
    if origen == "documento":
        return "D", "documento"
    if origen == "mundo":
        mundo = mundo.replace("código", "codigo")
        if mundo == "orquestador":
            return "M-orquestador", "mundo/orquestador"
        if mundo == "fuente":
            return "M-fuente", "mundo/fuente"
        if mundo == "codigo":
            return "M-codigo", "mundo/código"
        return None, "mundo %r no admitido (§2: orquestador|código|fuente)" % (
            d.get("mundo"),)
    if not origen:
        return None, "sin origen (§2: documento|mundo)"
    return None, "origen %r no admitido (§2: documento|mundo)" % (
        d.get("origen"),)


def norm_condiciones(conds):
    """Conjunto normalizado de (texto, ref) para comparar condiciones."""
    out = set()
    for c in (conds or []):
        if isinstance(c, dict):
            out.add(((c.get("texto") or "").strip().lower(),
                     (c.get("ref") or "").strip().lower()))
        else:
            s = str(c).strip()
            m = RE_COND_REF.match(s)
            if m:
                out.add((m.group(1).strip().lower(),
                         m.group(2).strip().lower()))
            else:
                out.add((s.lower(), ""))
    return out


def norm_fecha(s):
    """Fecha a d-m-aaaa («1-10-2026», «20 de septiembre de 2026») o None."""
    if not isinstance(s, str):
        return None
    m = RE_NUM.search(s)
    if m:
        return "%d-%d-%s" % (int(m.group(1)), int(m.group(2)), m.group(3))
    m = RE_LARGA.search(s)
    if m and m.group(2).lower() in MESES:
        return "%d-%d-%s" % (int(m.group(1)), MESES[m.group(2).lower()],
                             m.group(3))
    return None


def canon_fechas(s):
    """Normaliza las fechas contenidas en un texto para poder comparar."""
    if not isinstance(s, str):
        return s

    def num(m):
        return "%d-%d-%s" % (int(m.group(1)), int(m.group(2)), m.group(3))

    def larga(m):
        mes = m.group(2).lower()
        if mes not in MESES:
            return m.group(0)
        return "%d-%d-%s" % (int(m.group(1)), MESES[mes], m.group(3))

    return RE_LARGA.sub(larga, RE_NUM.sub(num, s))


def fecha_efectiva(dep, cual):
    """radicacion/consulta efectivas; «fecha» vieja vale como alias.

    radicacion: la lleva lo radicado (origen documento); consulta: lo traído
    de una fuente (mundo/fuente). Normalizada a d-m-aaaa.
    """
    val = dep.get(cual)
    if not val and cual == "radicacion" and \
            (dep.get("origen") or "") == "documento":
        val = dep.get("fecha")
    if not val and cual == "consulta":
        mundo = (dep.get("mundo") or "").replace("código", "codigo")
        if mundo == "fuente":
            val = dep.get("fecha")
    if not val:
        return None
    return norm_fecha(val) or str(val).strip()


def filas_por_pos(tabla):
    fs = (tabla or {}).get("filas")
    if not isinstance(fs, list):
        return {}
    return {r.get("posicion"): r for r in fs if isinstance(r, dict)}


def tablas_presentes(q):
    return [t for t in TABLAS_ORDEN if isinstance(q.get(t), dict)] + sorted(
        k for k in q if k.startswith("tabla_") and k not in TABLAS_ORDEN
        and isinstance(q.get(k), dict))


def nombre_corto(tabla):
    return tabla[len("tabla_"):] if tabla.startswith("tabla_") else tabla


def norm_esperada(e):
    if e in TABLAS_ORDEN:
        return e
    if ("tabla_" + str(e)) in TABLAS_ORDEN:
        return "tabla_" + str(e)
    return e

# -------------------------------------------------------------- verificar

def verificar_pregunta(q, sello_sup):
    nombre = qid(q)
    errores = []
    print("== %s ==" % nombre)

    # Sello (suyo o heredado del archivo).
    sello = q.get("esquema", sello_sup)
    if sello != SELLO:
        errores.append("sello %r (se esperaba %r)" % (sello, SELLO))
    print("  sello: %s" % sello)

    # R contra la lista cerrada de §3.
    r = norm_r(q)
    print("  R: %s" % (r if r else "(falta)"))
    r_ok = r in R_LISTA
    if not r_ok:
        errores.append("R %r fuera de la lista cerrada de §3 %s"
                       % (r, list(R_LISTA)))

    # Dependencias: categoría por origen/mundo y admisión por R.
    deps = q.get("dependencias") or []
    dep_ids = set()
    dep_por_id = {}
    for d in deps:
        di = (d or {}).get("id")
        if not di:
            errores.append("dependencia sin id")
            continue
        dep_ids.add(di)
        dep_por_id[di] = d
        cat, etiqueta = categoria_dep(d)
        if cat is None:
            errores.append("dependencia %s: %s" % (di, etiqueta))
        elif r_ok and not R_ADMITE[r].get(cat, False):
            errores.append("dependencia %s (%s) no admitida por R %r (§3)"
                           % (di, etiqueta, r))

    # Tablas esperadas y presentes.
    esperadas = q.get("tablas_esperadas")
    if not isinstance(esperadas, list) or not esperadas:
        errores.append("sin tablas_esperadas (§4)")
        esperadas = []
    esperadas_n = [norm_esperada(e) for e in esperadas]
    presentes = tablas_presentes(q)
    print("  tablas esperadas: %s; presentes: %s"
          % (esperadas_n, presentes))
    for t in esperadas_n:
        if not isinstance(q.get(t), dict):
            errores.append("falta %s (según tablas_esperadas)" % t)

    # Filas, desenlaces, ids de ruta / conflicto / campo.
    usadas = set()
    for t in presentes:
        tb = q.get(t)
        print("  %s: desenlace=%s filas=%s conflicto=%s campo=%s"
              % (t, tb.get("desenlace"),
                 [r.get("posicion") for r in (tb.get("filas") or [])
                  if isinstance(r, dict)],
                 tb.get("conflicto"), tb.get("campo")))
        if not isinstance(tb.get("filas"), list):
            errores.append("%s: 'filas' no es lista" % t)
            continue
        for key in ("conflicto", "campo"):
            if not isinstance(tb.get(key, []), list):
                errores.append("%s: '%s' no es lista" % (t, key))
        des = tb.get("desenlace")
        if des not in DESENLACES:
            errores.append("%s: desenlace %r fuera de %s"
                           % (t, des, list(DESENLACES)))
        for r_ in tb["filas"]:
            if not isinstance(r_, dict):
                errores.append("%s: fila que no es objeto" % t)
                continue
            if not r_.get("posicion"):
                errores.append("%s: fila sin posición" % t)
            if r_.get("estado") not in ESTADOS:
                errores.append("%s: estado %r fuera de %s en %r"
                               % (t, r_.get("estado"), list(ESTADOS),
                                  r_.get("posicion")))
            if not isinstance(r_.get("ruta", []), list):
                errores.append("%s: ruta no es lista en %r"
                               % (t, r_.get("posicion")))
            else:
                usadas.update(r_.get("ruta") or [])

    # Rutas <-> dependencias (§4: dependencias = lo que aparece en rutas).
    huerfanas = sorted(usadas - dep_ids)
    if huerfanas:
        errores.append("ids de ruta sin dependencia: "
                       + ", ".join(huerfanas))
    sin_ruta = sorted(dep_ids - usadas)
    if sin_ruta:
        errores.append("dependencias que no aparecen en ninguna ruta: "
                       + ", ".join(sin_ruta))

    # Conflicto: ids con condiciones distintas (§4, §7).
    for t in presentes:
        tb = q.get(t)
        conf = tb.get("conflicto") or []
        if not isinstance(conf, list):
            continue
        for cid in conf:
            if cid not in dep_por_id:
                errores.append("%s: conflicto %s sin dependencia"
                               % (t, cid))
        vistos = {}
        for cid in conf:
            if cid in dep_por_id:
                vistos[cid] = sorted(
                    "%s|%s" % c for c in
                    norm_condiciones(dep_por_id[cid].get("condiciones")))
        if len(set(tuple(v) for v in vistos.values())) > 1:
            errores.append(
                "%s: conflicto %s con condiciones distintas: %s"
                % (t, sorted(vistos),
                   json.dumps(vistos, ensure_ascii=False)))

    # Campo: solo datos (§4); M de fuente con consulta; M de código con
    # versión (§2, §4). «fecha» vieja vale como radicacion/consulta.
    for t in presentes:
        for cid in ((q.get(t) or {}).get("campo") or []):
            if cid not in dep_por_id:
                errores.append("%s: campo %s sin dependencia" % (t, cid))
            elif dep_por_id[cid].get("tipo") == "regla":
                errores.append("%s: campo %s es regla (solo datos)" % (t, cid))
    for di, d in dep_por_id.items():
        cat, _ = categoria_dep(d)
        if cat == "M-fuente" and not fecha_efectiva(d, "consulta"):
            errores.append("dependencia %s: M de fuente sin consulta" % di)
        if cat == "M-codigo" and not d.get("version"):
            errores.append("dependencia %s: M de código sin version" % di)

    if errores:
        print("  [ERRORES]")
        for e in errores:
            print("    - %s" % e)
    print()
    return ["%s: %s" % (nombre, e) for e in errores]


def cmd_verificar(ruta):
    sello_sup, preguntas = cargar_preguntas(ruta)
    print("verificar %s (preguntas: %d)" % (ruta, len(preguntas)))
    todos = []
    for q in preguntas:
        todos.extend(verificar_pregunta(q, sello_sup))
    print("== resumen ==")
    print("  preguntas: %d" % len(preguntas))
    print("  errores: %d" % len(todos))
    for e in todos:
        print("    [ERROR] %s" % e)
    return 1 if todos else 0

# ------------------------------------------------------------- comparar

def linea(s):
    return " ".join(str(s).split())


def cmp_dep(a, b):
    """Diferencias entre dos dependencias con el mismo id (lista de líneas)."""
    difs = []
    if (a.get("origen") or "") != (b.get("origen") or ""):
        difs.append("origen: %s vs %s"
                    % (json.dumps(a.get("origen"), ensure_ascii=False),
                       json.dumps(b.get("origen"), ensure_ascii=False)))
    if (a.get("mundo") or "") != (b.get("mundo") or ""):
        difs.append("mundo: %s vs %s"
                    % (json.dumps(a.get("mundo"), ensure_ascii=False),
                       json.dumps(b.get("mundo"), ensure_ascii=False)))
    if a.get("tipo") != b.get("tipo"):
        difs.append("tipo: %s vs %s"
                    % (json.dumps(a.get("tipo"), ensure_ascii=False),
                       json.dumps(b.get("tipo"), ensure_ascii=False)))
    if canon_fechas(a.get("valor")) != canon_fechas(b.get("valor")):
        difs.append("valor: %s vs %s"
                    % (json.dumps(a.get("valor"), ensure_ascii=False),
                       json.dumps(b.get("valor"), ensure_ascii=False)))
    ca, cb = norm_condiciones(a.get("condiciones")), norm_condiciones(
        b.get("condiciones"))
    if ca != cb:
        difs.append("condiciones: %s vs %s"
                    % (json.dumps(a.get("condiciones"), ensure_ascii=False),
                       json.dumps(b.get("condiciones"), ensure_ascii=False)))
    if (a.get("procedencia") or "") != (b.get("procedencia") or ""):
        difs.append("procedencia: %s vs %s"
                    % (json.dumps(a.get("procedencia"), ensure_ascii=False),
                       json.dumps(b.get("procedencia"), ensure_ascii=False)))
    for cual in ("radicacion", "consulta"):
        fa, fb = fecha_efectiva(a, cual), fecha_efectiva(b, cual)
        if fa != fb:
            difs.append("%s: %s vs %s"
                        % (cual, json.dumps(fa, ensure_ascii=False),
                           json.dumps(fb, ensure_ascii=False)))
    if (a.get("version") or "") != (b.get("version") or ""):
        difs.append("version: %s vs %s"
                    % (json.dumps(a.get("version"), ensure_ascii=False),
                       json.dumps(b.get("version"), ensure_ascii=False)))
    return difs


def cmp_pregunta(nombre, a, b, na, nb):
    difs = []
    ra, rb = norm_r(a), norm_r(b)
    if ra != rb:
        difs.append("%s R: %s vs %s"
                    % (nombre, json.dumps(ra, ensure_ascii=False),
                       json.dumps(rb, ensure_ascii=False)))
    ea, eb = a.get("encabezado") or {}, b.get("encabezado") or {}
    if (ea.get("caso") or "") != (eb.get("caso") or ""):
        difs.append("%s encabezado.caso: %s vs %s"
                    % (nombre, json.dumps(ea.get("caso"), ensure_ascii=False),
                       json.dumps(eb.get("caso"), ensure_ascii=False)))
    if (ea.get("aspecto") or "") != (eb.get("aspecto") or ""):
        difs.append("%s encabezado.aspecto: %s vs %s"
                    % (nombre,
                       json.dumps(ea.get("aspecto"), ensure_ascii=False),
                       json.dumps(eb.get("aspecto"), ensure_ascii=False)))
    if norm_condiciones(ea.get("condiciones")) != norm_condiciones(
            eb.get("condiciones")):
        difs.append("%s encabezado.condiciones: %s vs %s"
                    % (nombre,
                       json.dumps(ea.get("condiciones"), ensure_ascii=False),
                       json.dumps(eb.get("condiciones"), ensure_ascii=False)))
    da, db = a.get("dominio") or {}, b.get("dominio") or {}
    for campo in ("escala", "regla"):
        if (da.get(campo) or "") != (db.get(campo) or ""):
            difs.append("%s dominio.%s: %s vs %s"
                        % (nombre, campo,
                           json.dumps(da.get(campo), ensure_ascii=False),
                           json.dumps(db.get(campo), ensure_ascii=False)))
    if set(a.get("tablas_esperadas") or []) != set(
            b.get("tablas_esperadas") or []):
        difs.append("%s tablas_esperadas: %s vs %s"
                    % (nombre,
                       json.dumps(a.get("tablas_esperadas"),
                                  ensure_ascii=False),
                       json.dumps(b.get("tablas_esperadas"),
                                  ensure_ascii=False)))

    for t in TABLAS_ORDEN + tuple(sorted(
            set([k for k in list(a) + list(b) if str(k).startswith("tabla_")])
            - set(TABLAS_ORDEN))):
        ta, tb = a.get(t), b.get(t)
        if ta is None and tb is None:
            continue
        if ta is None or tb is None:
            difs.append("%s [%s]: solo en %s"
                        % (nombre, t, nb if ta is None else na))
            continue
        if (ta.get("desenlace") or "") != (tb.get("desenlace") or ""):
            difs.append("%s [%s] desenlace: %s vs %s"
                        % (nombre, t,
                           json.dumps(ta.get("desenlace"), ensure_ascii=False),
                           json.dumps(tb.get("desenlace"), ensure_ascii=False)))
        if set(ta.get("conflicto") or []) != set(tb.get("conflicto") or []):
            difs.append("%s [%s] conflicto: %s vs %s"
                        % (nombre, t,
                           json.dumps(sorted(ta.get("conflicto") or []),
                                      ensure_ascii=False),
                           json.dumps(sorted(tb.get("conflicto") or []),
                                      ensure_ascii=False)))
        if set(ta.get("campo") or []) != set(tb.get("campo") or []):
            difs.append("%s [%s] campo: %s vs %s"
                        % (nombre, t,
                           json.dumps(sorted(ta.get("campo") or []),
                                      ensure_ascii=False),
                           json.dumps(sorted(tb.get("campo") or []),
                                      ensure_ascii=False)))
        fa, fb = filas_por_pos(ta), filas_por_pos(tb)
        ka = {canon_fechas(p): p for p in fa}
        kb = {canon_fechas(p): p for p in fb}
        for k in sorted(set(ka) - set(kb), key=str):
            difs.append("%s [%s] posicion %s: solo en %s"
                        % (nombre, t, json.dumps(ka[k], ensure_ascii=False),
                           na))
        for k in sorted(set(kb) - set(ka), key=str):
            difs.append("%s [%s] posicion %s: solo en %s"
                        % (nombre, t, json.dumps(kb[k], ensure_ascii=False),
                           nb))
        for k in sorted(set(ka) & set(kb), key=str):
            ra_, rb_ = fa[ka[k]], fb[kb[k]]
            pos = ka[k]
            if ra_.get("si") != rb_.get("si"):
                difs.append("%s [%s] %s si: %s vs %s"
                            % (nombre, t,
                               json.dumps(pos, ensure_ascii=False),
                               json.dumps(ra_.get("si"), ensure_ascii=False),
                               json.dumps(rb_.get("si"), ensure_ascii=False)))
            if ra_.get("estado") != rb_.get("estado"):
                difs.append("%s [%s] %s estado: %s vs %s"
                            % (nombre, t,
                               json.dumps(pos, ensure_ascii=False),
                               json.dumps(ra_.get("estado"),
                                          ensure_ascii=False),
                               json.dumps(rb_.get("estado"),
                                          ensure_ascii=False)))
            if set(ra_.get("ruta") or []) != set(rb_.get("ruta") or []):
                difs.append("%s [%s] %s ruta: %s vs %s"
                            % (nombre, t,
                               json.dumps(pos, ensure_ascii=False),
                               json.dumps(sorted(ra_.get("ruta") or []),
                                          ensure_ascii=False),
                               json.dumps(sorted(rb_.get("ruta") or []),
                                          ensure_ascii=False)))

    ma = {d.get("id"): d for d in (a.get("dependencias") or [])
          if isinstance(d, dict)}
    mb = {d.get("id"): d for d in (b.get("dependencias") or [])
          if isinstance(d, dict)}
    for did in sorted(set(ma) | set(mb)):
        if did not in ma:
            difs.append("%s dependencia %s: solo en %s" % (nombre, did, nb))
        elif did not in mb:
            difs.append("%s dependencia %s: solo en %s" % (nombre, did, na))
        else:
            for d in cmp_dep(ma[did], mb[did]):
                difs.append("%s dependencia %s.%s" % (nombre, did, d))
    return [linea(d) for d in difs]


def cmd_comparar(pa, pb):
    _, la = cargar_preguntas(pa)
    _, lb = cargar_preguntas(pb)
    ia = {qid(q): q for q in la}
    ib = {qid(q): q for q in lb}
    print("comparar %s vs %s" % (pa, pb))
    n = 0
    for nombre in sorted(set(ia) | set(ib)):
        if nombre not in ia:
            print("%s: solo en %s" % (nombre, pb))
            n += 1
        elif nombre not in ib:
            print("%s: solo en %s" % (nombre, pa))
            n += 1
        else:
            for d in cmp_pregunta(nombre, ia[nombre], ib[nombre], pa, pb):
                print(d)
                n += 1
    print("diferencias: %d" % n)
    return 0

# -------------------------------------------------------------- guardar

def hoy_d_m_aaaa():
    d = datetime.date.today()
    return "%d-%d-%d" % (d.day, d.month, d.year)


def cmd_guardar(ptablas, pcorpus):
    _, preguntas = cargar_preguntas(ptablas)
    hoy = hoy_d_m_aaaa()
    escritos = []
    for q in preguntas:
        dd = q.get("dato_derivado")
        if not isinstance(dd, dict):
            continue
        linea_dd = copy.deepcopy(dd)
        der = linea_dd.setdefault("derivacion", {})
        der["radicacion"] = hoy
        ref = {d.get("id"): d for d in (q.get("dependencias") or [])
               if isinstance(d, dict)}
        completas = []
        for dep in (der.get("dependencias") or []):
            if isinstance(dep, str) and dep in ref:
                completas.append(copy.deepcopy(ref[dep]))
            elif isinstance(dep, dict) and set(dep) <= {"id"} \
                    and dep.get("id") in ref:
                completas.append(copy.deepcopy(ref[dep["id"]]))
            else:
                completas.append(dep)
        der["dependencias"] = completas
        escritos.append(linea_dd)
        print("guardar: %s (%s) valor %s -> %s (radicacion %s, "
              "dependencias: %d objetos)"
              % (linea_dd.get("id"), qid(q), linea_dd.get("valor"),
                 pcorpus, hoy, len(completas)))
    if not escritos:
        print("guardar: sin datos derivados en %s; nada que guardar"
              % ptablas)
        return 0
    with open(pcorpus, "a", encoding="utf-8") as f:
        for e in escritos:
            f.write(json.dumps(e, ensure_ascii=False) + "\n")
    with open(pcorpus, encoding="utf-8") as f:
        lineas = [l for l in f.read().split("\n") if l.strip()]
    leidos = [json.loads(l) for l in lineas[-len(escritos):]]
    ok = leidos == escritos
    print("verificación: %d línea(s) leída(s) de vuelta de %s, "
          "iguales a lo escrito: %s" % (len(leidos), pcorpus,
                                        "SÍ" if ok else "NO"))
    return 0 if ok else 1


# ------------------------------------------------------------- mantener

def segmento_valor(valor):
    if not isinstance(valor, str):
        return ""
    if "·" in valor:
        return valor.split("·")[-1]
    return valor


def parse_fecha_texto(valor):
    seg = segmento_valor(valor)
    m = RE_NUM.search(seg) or RE_NUM.search(valor or "")
    if m:
        return datetime.date(int(m.group(3)), int(m.group(2)),
                             int(m.group(1)))
    for texto in (seg, valor or ""):
        m = RE_LARGA.search(texto)
        if m and m.group(2).lower() in MESES:
            return datetime.date(int(m.group(3)), MESES[m.group(2).lower()],
                                 int(m.group(1)))
    return None


def parse_cierre(valor):
    for texto in (segmento_valor(valor), valor or ""):
        m = RE_CIERRE.search(texto)
        if m and m.group(3).lower() in MESES:
            return int(m.group(1)), int(m.group(2)), MESES[m.group(3).lower()]
    return None


def fmt_fecha(d):
    return "%d-%d-%d" % (d.day, d.month, d.year)


def reapertura(ref_fecha, cierre):
    """M3 (mes sin año = próxima ocurrencia desde la fecha del texto) +
    M1 (el día Y sigue cerrado; se reabre Y+1) + M4 (datetime)."""
    _, dia_fin, mes = cierre
    anio = ref_fecha.year if mes >= ref_fecha.month else ref_fecha.year + 1
    fin = datetime.date(anio, mes, dia_fin)  # M4: calendario
    return fin + datetime.timedelta(days=1)  # M1: Y+1; M4: aritmética


def cmd_mantener(pcorpus, id_dep, valor_nuevo):
    with open(pcorpus, encoding="utf-8") as f:
        datos = [json.loads(l) for l in f.read().split("\n") if l.strip()]
    ver_m4 = "Python %s (datetime)" % sys.version.split()[0]
    afectados = []
    for dato in datos:
        ids = [(d.get("id") if isinstance(d, dict) else d)
               for d in ((dato.get("derivacion") or {}).get("dependencias")
                         or [])]
        if id_dep in ids:
            afectados.append(dato)
    if not afectados:
        print("mantener: ninguna línea de %s usa la dependencia %s"
              % (pcorpus, id_dep))
        return 1
    rc = 0
    for dato in afectados:
        nombre = "%s (%s)" % (dato.get("id"),
                              (dato.get("derivacion") or {}).get("pregunta"))
        deps = {d.get("id"): d for d in
                ((dato.get("derivacion") or {}).get("dependencias") or [])
                if isinstance(d, dict)}
        if id_dep not in deps:
            print("%s: %s sin objeto completo; no se puede recalcular"
                  % (nombre, id_dep))
            rc = 1
            continue
        d_dep = deps[id_dep]
        d1 = deps.get("D1")
        if d1 is None:
            cand = [d for d in deps.values()
                    if (d.get("origen") or "") == "documento"
                    and parse_fecha_texto(d.get("valor")) is not None]
            d1 = cand[0] if cand else None
        if d1 is None:
            print("%s: sin fecha del texto (D1); no se puede recalcular"
                  % nombre)
            rc = 1
            continue
        ref = parse_fecha_texto(d1.get("valor"))
        cierre_reg = parse_cierre(d_dep.get("valor"))
        cierre_nuevo = parse_cierre(valor_nuevo)
        if ref is None or cierre_reg is None or cierre_nuevo is None:
            print("%s: no se pudo interpretar D1=%r, %s=%r o valor nuevo=%r"
                  % (nombre, d1.get("valor"), id_dep, d_dep.get("valor"),
                     valor_nuevo))
            rc = 1
            continue
        registrada = norm_fecha(dato.get("valor")) or dato.get("valor")
        recalc = fmt_fecha(reapertura(ref, cierre_reg))
        nueva = fmt_fecha(reapertura(ref, cierre_nuevo))
        print("dato %s, dependencia %s" % (nombre, id_dep))
        print("  posición registrada: %s" % registrada)
        print("  recalculada con valores registrados "
              "[fecha del texto %s (%s), cierre %s]: %s — coincide: %s "
              "(chequeo aritmético M1+M3+M4)"
              % (fmt_fecha(ref), d1.get("id"), d_dep.get("valor"), recalc,
                 "SÍ" if recalc == registrada else "NO"))
        print("  M4 (código): aritmética con datetime — version: %s"
              % ver_m4)
        if recalc != registrada:
            rc = 1
        print("  con %s = %r: nueva posición: %s"
              % (id_dep, valor_nuevo, nueva))
        if nueva == registrada:
            print("  sin cambio: %s conserva el sostén" % registrada)
        else:
            print("  pierde sostén: %s; gana sostén: %s"
                  % (registrada, nueva))
    return rc


# ------------------------------------------------------------------ main

def main(argv):
    if len(argv) == 3 and argv[1] == "verificar":
        return cmd_verificar(argv[2])
    if len(argv) == 4 and argv[1] == "comparar":
        return cmd_comparar(argv[2], argv[3])
    if len(argv) == 4 and argv[1] == "guardar":
        return cmd_guardar(argv[2], argv[3])
    if len(argv) == 5 and argv[1] == "mantener":
        return cmd_mantener(argv[2], argv[3], argv[4])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
