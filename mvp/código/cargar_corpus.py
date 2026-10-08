#!/usr/bin/env python3
"""Inscribe documentos radicados en la base del corpus (SQLite).

**La base es el registro.** No es una vista derivada ni se regenera: acá se **inscribe**, y lo
inscrito no se vuelve a tocar.

    python3 mvp/código/cargar_corpus.py doc7                inscribe doc7: su fila y sus datos
    python3 mvp/código/cargar_corpus.py --reinscribir doc7  ACTO DE PRUEBAS: lo saca y lo inscribe de nuevo
    python3 mvp/código/cargar_corpus.py                     crea la base si no está y muestra el estado

Reglas:

- **No borra, no reescribe y no regenera nada.** Si el documento ya está inscrito, lo dice y no lo
  toca. Mover lo inscrito es **un acto explícito**: `--reinscribir <doc>` (en pruebas), que saca lo
  de ese documento y lo vuelve a inscribir, con la fecha y hora del acto nuevo.
- **La fecha y hora de radicación las pone la base**, en el momento de inscribir: ese es el acto.
- El **sello** se calcula: sha256 del documento tal como está en `documentos/`.
- Los **datos** salen de los crudos de la extracción: el paso 1 da las unidades, el paso 2 los
  datos de cada unidad (un archivo por unidad).

Qué hay en esta carpeta:

    documentos/       los documentos radicados — la única fuente de verdad de su texto
    extraccion/<doc>/ los crudos de la extracción: unidades (paso 1) y datos por unidad (paso 2)
    consulta/         el orquestador, las preguntas, los crudos y las salidas
    corpus.db         la base: documentos · datos

Qué guarda: las **referencias** al documento (dominio, fecha y hora de radicación, ubicación local
y en el repo, commit, sello) y **lo que produjo la extracción**. No guarda el texto del documento
ni los números de oración: el texto vive en el documento radicado, y los números son la vara con la
que evaluamos el paso 1. Cada fila de `datos` lleva su `caso` y su `unidad_id`, para leerse sola.

Si un documento no está donde dice su `ubicacion_local`, la inscripción se detiene y reporta: una
mudanza es un acto, con autorización.
"""

import hashlib
import json
import pathlib
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent  # la raíz del repo
AQUI = pathlib.Path(__file__).resolve().parent
DB = AQUI / "corpus.db"

# Los documentos **conocidos**, con sus referencias. Estar acá no es estar inscrito: la
# inscripción es el acto de correr este guion con el id. La fecha de radicación no se declara: la
# pone la base al inscribir. **Hoy está vacío**: los documentos que había (`doc4`, `doc6`) quedaron
# archivados en `mvp/temp/documentos/`, y el primero en entrar será el que se radique.
DOCUMENTOS = []

ESQUEMA = """
CREATE TABLE IF NOT EXISTS documentos (
  id                 TEXT PRIMARY KEY,
  dominio            TEXT NOT NULL,
  fecha_radicacion   TEXT NOT NULL DEFAULT (datetime('now','localtime')),  -- la pone la base
  ubicacion_local    TEXT NOT NULL,
  ubicacion_upstream TEXT NOT NULL,
  commit_publicacion TEXT,
  sello              TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS datos (
  id           TEXT PRIMARY KEY,
  unidad_id    TEXT NOT NULL,
  caso         TEXT NOT NULL,
  aspecto      TEXT NOT NULL,
  valor        TEXT NOT NULL,
  unidad_valor TEXT
);
CREATE INDEX IF NOT EXISTS idx_datos_unidad ON datos(unidad_id);
"""


def asegurar_base(db):
    """Crea las tablas si no están. Nunca borra ni vacía nada."""
    db.executescript(ESQUEMA)


def inscribir(db, doc):
    """Inscribe un documento: su fila y sus datos. Si ya está, no lo toca. Devuelve True si inscribió."""
    if db.execute("SELECT 1 FROM documentos WHERE id = ?", (doc["id"],)).fetchone():
        print(f"  {doc['id']}: ya está inscrito — no se toca. "
              f"(En pruebas, para rehacerlo: --reinscribir {doc['id']})")
        return False
    ruta = RAIZ / doc["ubicacion_local"]
    if not ruta.exists():
        raise SystemExit(
            f"el documento no está en '{doc['ubicacion_local']}': una mudanza es un acto, "
            f"con autorización — no se sigue a ciegas"
        )
    db.execute(
        "INSERT INTO documentos (id, dominio, ubicacion_local, ubicacion_upstream, "
        "commit_publicacion, sello) VALUES (?,?,?,?,?,?)",
        (doc["id"], doc["dominio"], doc["ubicacion_local"], doc["ubicacion_upstream"],
         doc["commit"], hashlib.sha256(ruta.read_bytes()).hexdigest()),
    )
    radicado = db.execute("SELECT fecha_radicacion FROM documentos WHERE id = ?",
                          (doc["id"],)).fetchone()[0]

    unidades = json.loads((RAIZ / doc["unidades"]).read_text(encoding="utf-8"))["subtemas"]
    datos_inscritos = 0
    for n, unidad in enumerate(unidades, 1):
        uid = f"{doc['id']}:U{n}"
        datos = json.loads((RAIZ / doc["datos"].format(n=n)).read_text(encoding="utf-8"))
        for j, dato in enumerate(datos.get("datos") or [], 1):
            db.execute("INSERT INTO datos VALUES (?,?,?,?,?,?)",
                       (f"{uid}:D{j}", uid, dato.get("caso") or unidad["subtema"],
                        dato["aspecto"], dato["valor"], dato.get("unidad_valor")))
            datos_inscritos += 1
    db.commit()
    print(f"  {doc['id']}: inscrito · radicado {radicado} · "
          f"{len(unidades)} unidades · {datos_inscritos} datos")
    return True


def reinscribir(db, doc):
    """Acto de pruebas: saca lo inscrito de ese documento y lo vuelve a inscribir."""
    if not db.execute("SELECT 1 FROM documentos WHERE id = ?", (doc["id"],)).fetchone():
        print(f"  {doc['id']}: no estaba inscrito — se inscribe")
        return inscribir(db, doc)
    print(f"  {doc['id']}: ACTO DE PRUEBAS — se reinscribe (lo inscrito se saca y vuelve a entrar)")
    db.execute("DELETE FROM datos WHERE unidad_id LIKE ?", (f"{doc['id']}:%",))
    db.execute("DELETE FROM documentos WHERE id = ?", (doc["id"],))
    db.commit()
    return inscribir(db, doc)


def mostrar_estado(db):
    filas = db.execute("SELECT id, dominio, fecha_radicacion, ubicacion_local, sello "
                       "FROM documentos ORDER BY id").fetchall()
    datos = db.execute("SELECT count(*) FROM datos").fetchone()[0]
    casos = db.execute("SELECT count(DISTINCT unidad_id) FROM datos").fetchone()[0]
    print(f"base: {DB.relative_to(RAIZ)}")
    if not filas:
        print("  sin documentos inscritos: el registro está vacío")
        return
    for fila in filas:
        print(f"  inscrito: {fila[0]} · {fila[1]} · radicado {fila[2]} · "
              f"{fila[3]} · sello {fila[4][:12]}…")
    print(f"  datos: {datos} · casos: {casos}")


def main():
    argumentos = sys.argv[1:]
    reinscribir_lo_pedido = "--reinscribir" in argumentos
    ids = [a for a in argumentos if a != "--reinscribir"]
    db = sqlite3.connect(DB)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    asegurar_base(db)

    if not ids:
        mostrar_estado(db)
        print("  (inscribir: python3 mvp/código/cargar_corpus.py <doc> · "
              "en pruebas, rehacer: --reinscribir <doc>)")
        db.close()
        return

    catalogo = {d["id"]: d for d in DOCUMENTOS}
    for identificador in ids:
        if identificador not in catalogo:
            raise SystemExit(f"'{identificador}' no está en el catálogo de documentos conocidos")
        if reinscribir_lo_pedido:
            reinscribir(db, catalogo[identificador])
        else:
            inscribir(db, catalogo[identificador])
    mostrar_estado(db)
    db.close()


if __name__ == "__main__":
    main()
