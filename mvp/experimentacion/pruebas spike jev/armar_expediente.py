#!/usr/bin/env python3
"""Arma el expediente y las preguntas de la prueba de casos, leyendo la base.

El **catálogo** es el mismo que el ORQ tuvo delante: los casos (id y nombre) de la UT vigente de
cada documento del dominio, en el orden en que se ofrecen. Los **elegidos** salen de
`consulta_casos`: son los casos que el agente encargado pidió.

    python3 "mvp/experimentacion/pruebas spike jev/armar_expediente.py" [q1]

Solo lee: abre el corpus con `mode=ro`. Escribe dos archivos junto a este:
`expediente-<q>.json` (el `state`) y `preguntas-<q>.json` (el `questions`).
"""

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


def main(argv):
    identificador = argv[1] if len(argv) > 1 else "q1"
    db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
    db.row_factory = sqlite3.Row
    consulta = db.execute("SELECT * FROM consultas WHERE id = ?", (identificador,)).fetchone()
    if consulta is None:
        raise SystemExit(f"no está la consulta '{identificador}' en la base")
    casos = catalogo(db, consulta["dominio"])
    elegidos = []
    for fila in db.execute("SELECT unidad_id FROM consulta_casos WHERE consulta_id = ? "
                           "ORDER BY rowid", (identificador,)):
        u = db.execute("SELECT subtema FROM unidades WHERE id = ?", (fila["unidad_id"],)).fetchone()
        elegidos.append({"id": fila["unidad_id"], "caso": u["subtema"] if u else None})
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

    e = AQUI / f"expediente-{identificador}.json"
    p = AQUI / f"preguntas-{identificador}.json"
    e.write_text(json.dumps(estado, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    p.write_text(json.dumps(preguntas, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"  {identificador}: {len(casos)} casos en el catálogo · {len(elegidos)} elegidos "
          f"({', '.join(x['id'] for x in elegidos) or 'ninguno'})")
    print(f"  -> {e.relative_to(RAIZ)}")
    print(f"  -> {p.relative_to(RAIZ)}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
