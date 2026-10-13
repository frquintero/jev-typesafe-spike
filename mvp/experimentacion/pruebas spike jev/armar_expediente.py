#!/usr/bin/env python3
"""Arma el expediente y las preguntas de la prueba de casos, leyendo la base.

El **catálogo** es el mismo que el ORQ tuvo delante: los casos (id y nombre) de la UT vigente de
cada documento del dominio, en el orden en que se ofrecen. Los **elegidos** salen de
`consulta_casos`: son los casos que el agente encargado pidió.

    python3 "mvp/experimentacion/pruebas spike jev/armar_expediente.py" q4 \
        --nombre q4-inyectados --elegidos-extra C000002:U4,C000002:U8,C000002:U10

`--elegidos-extra` agrega ids a los elegidos (el control: casos que no tienen que ver con la
pregunta, para ver si el juicio se mueve), y `--nombre` cambia el nombre de los dos archivos para no
pisar los de la corrida limpia.

Solo lee: abre el corpus con `mode=ro`. Escribe dos archivos junto a este:
`expediente-<nombre>.json` (el `state`) y `preguntas-<nombre>.json` (el `questions`).
"""

import argparse
import json
import pathlib
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[3]
DB = RAIZ / "mvp" / "código" / "corpus.db"
AQUI = pathlib.Path(__file__).resolve().parent

ELECCION = {
    "type": "choice",
    "instructions": "Comparando `elegidos` con todos los de `casos`, ¿cómo es la elección que "
                    "se hizo para responder `pregunta`?",
    "criteria": {
        "correcta": "`elegidos` alcanza y no sobra ninguno",
        "sobran": "`elegidos` alcanza, pero hay alguno que no hacía falta",
        "faltan": "a `elegidos` le falta algún caso de `casos`",
        "no_sirve": "ninguno de `elegidos` responde `pregunta`",
    },
}


def catalogo(db, dominio):
    """Los casos de la UT vigente de cada documento del dominio, en el orden del ORQ."""
    casos = []
    for d in db.execute("SELECT id FROM documentos WHERE dominio = ? ORDER BY id", (dominio,)):
        ut = db.execute("SELECT id FROM corridas WHERE documento_id = ? AND paso = 'UT' "
                        "AND estado = 'exitoso' ORDER BY id DESC LIMIT 1",
                        (d["id"],)).fetchone()
        if ut is None:
            continue
        for u in db.execute("SELECT id, subtema FROM unidades WHERE corrida_id = ? ORDER BY n",
                            (ut["id"],)):
            casos.append({"id": u["id"], "caso": u["subtema"]})
    return casos


def nombre_de(db, unidad_id):
    """El nombre del caso, o se detiene si esa unidad no está."""
    u = db.execute("SELECT subtema FROM unidades WHERE id = ?", (unidad_id,)).fetchone()
    if u is None:
        raise SystemExit(f"la unidad '{unidad_id}' no está en la base")
    return u["subtema"]


def main(argv):
    ap = argparse.ArgumentParser(description="Arma el expediente de la prueba de casos.")
    ap.add_argument("consulta", nargs="?", default="q1", help="el id de la consulta (q1…)")
    ap.add_argument("--nombre", help="etiqueta de los archivos (por defecto, el id de la consulta)")
    ap.add_argument("--elegidos-extra", default="",
                    help="ids de unidades que se agregan a los elegidos, separados por coma")
    args = ap.parse_args(argv[1:])

    identificador = args.consulta
    etiqueta = args.nombre or identificador
    extras = [x.strip() for x in args.elegidos_extra.split(",") if x.strip()]

    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    consulta = db.execute("SELECT * FROM consultas WHERE id = ?", (identificador,)).fetchone()
    if consulta is None:
        raise SystemExit(f"no está la consulta '{identificador}' en la base")
    casos = catalogo(db, consulta["dominio"])
    elegidos = []
    for fila in db.execute("SELECT unidad_id FROM consulta_casos WHERE consulta_id = ? "
                           "ORDER BY rowid", (identificador,)):
        elegidos.append({"id": fila["unidad_id"], "caso": nombre_de(db, fila["unidad_id"])})
    for extra in extras:
        elegidos.append({"id": extra, "caso": nombre_de(db, extra)})
    db.close()

    estado = {"pregunta": consulta["pregunta_texto"], "casos": casos, "elegidos": elegidos}
    preguntas = {}
    for i in range(len(elegidos)):
        preguntas[f"elegido_{i + 1}"] = {
            "type": "noul",
            "instructions": f"`elegidos[{i}]` es un caso que permite responder `pregunta`",
            "criteria": {
                "true": "sus oraciones tratan lo que la pregunta pide",
                "false": "sus oraciones no tratan lo que la pregunta pide",
            },
        }
    preguntas["eleccion"] = ELECCION

    e = AQUI / f"expediente-{etiqueta}.json"
    p = AQUI / f"preguntas-{etiqueta}.json"
    e.write_text(json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {identificador} ({etiqueta}): {len(casos)} casos en el catálogo · "
          f"{len(elegidos)} elegidos " + (f"({len(extras)} inyectados)" if extras else ""))
    for x in elegidos:
        print(f"      {x['id']:<14} {x['caso']}")
    print(f"  -> {e.relative_to(RAIZ)}")
    print(f"  -> {p.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
