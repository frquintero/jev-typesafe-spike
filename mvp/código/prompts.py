#!/usr/bin/env python3
"""Las plantillas de los prompts: **en la base, con su versión**.

La plantilla es el texto del prompt **con sus huecos sin llenar**: las reglas, los ejemplos, las
marcas `[SISTEMA]`/`[TAREA]` y los `{{HUECOS}}`. El material —el documento, las unidades, los
casos, la pregunta, los relojes— sale de la base en cada acto, y el prompt resuelto no se
guarda: se re-arma.

**El acto la lee de la base.** La plantilla vigente es la **última versión inscrita** de su `id`: el
acto que corre no ve ningún archivo. Una plantilla nueva **se inscribe** con un acto aparte
—`python3 mvp/código/prompts.py inscribir <id> <archivo>`—, que lee el texto de un borrador que vive
donde se esté escribiendo (no en el repo) y deja la versión en `prompts`, con su fecha. **Una versión
inscrita no se toca**: editarla es inscribir otra. El texto de la versión es su identidad; por eso no
lleva sello.

Cada plantilla vive con la **base dueña de su acto**: `volcado`, en el almacén; `UT`, `DATOS` y
`ORQ`, en el corpus.
"""

import pathlib
import sys

DUEÑA = {"volcado": "almacen", "UT": "corpus", "DATOS": "corpus", "ORQ": "corpus"}


def usar(db, identificador):
    """La plantilla vigente —la última versión inscrita— para correr.

    Devuelve `{'id', 'version', 'texto'}`. Si no hay ninguna, se detiene y dice cómo inscribirla.
    """
    fila = db.execute("SELECT id, version, texto FROM prompts WHERE id = ? "
                      "ORDER BY version DESC LIMIT 1", (identificador,)).fetchone()
    if fila is None:
        raise SystemExit(f"no hay ninguna versión de '{identificador}' en la base: inscribila con "
                         f"python3 mvp/código/prompts.py inscribir {identificador} <archivo>")
    return {"id": fila["id"], "version": fila["version"], "texto": fila["texto"]}


def texto(db, identificador, version=None):
    """La fila de una versión, o la última. `None` si no está."""
    if version is None:
        return db.execute("SELECT * FROM prompts WHERE id = ? ORDER BY version DESC LIMIT 1",
                          (identificador,)).fetchone()
    return db.execute("SELECT * FROM prompts WHERE id = ? AND version = ?",
                      (identificador, version)).fetchone()


def inscribir(db, identificador, ruta):
    """Inscribe el texto de un archivo como **versión nueva** de la plantilla.

    Idempotente por texto: si es el texto de la última versión, no agrega nada y lo dice.
    """
    nuevo = pathlib.Path(ruta).read_text(encoding="utf-8")
    ultima = texto(db, identificador)
    if ultima is not None and ultima["texto"] == nuevo:
        return {"id": identificador, "version": ultima["version"], "texto": nuevo,
                "inscripta": False}
    version = db.execute("SELECT COALESCE(MAX(version), 0) + 1 FROM prompts WHERE id = ?",
                         (identificador,)).fetchone()[0]
    db.execute("INSERT INTO prompts (id, version, texto) VALUES (?,?,?)",
               (identificador, version, nuevo))
    db.commit()
    return {"id": identificador, "version": version, "texto": nuevo, "inscripta": True}


def conexion_duena(identificador):
    """La conexión de la base donde vive esa plantilla."""
    if DUEÑA.get(identificador) == "almacen":
        import almacen
        return almacen.conectar()
    import base
    return base.conectar()


def main(argumentos):
    if not argumentos or argumentos[0] not in ("inscribir", "mostrar"):
        raise SystemExit("uso: python3 mvp/código/prompts.py inscribir <id> <archivo>\n"
                         "     python3 mvp/código/prompts.py mostrar <id> [version]")
    orden, resto = argumentos[0], argumentos[1:]
    if not resto:
        raise SystemExit("falta el <id>: 'volcado', 'UT', 'DATOS' o 'ORQ'")
    identificador = resto[0]
    db = conexion_duena(identificador)
    try:
        if orden == "inscribir":
            if len(resto) != 2:
                raise SystemExit("uso: python3 mvp/código/prompts.py inscribir <id> <archivo>")
            resultado = inscribir(db, identificador, resto[1])
            if resultado["inscripta"]:
                print(f"  {identificador}: inscrita v{resultado['version']} "
                      f"({len(resultado['texto'])} car)")
            else:
                print(f"  {identificador}: es el texto de la v{resultado['version']}; "
                      f"no se inscribió nada")
        else:
            version = int(resto[1]) if len(resto) > 1 else None
            fila = texto(db, identificador, version)
            if fila is None:
                raise SystemExit(f"'{identificador}'"
                                 + (f" v{version}" if version else "") + " no está en la base")
            print(f"# {fila['id']} v{fila['version']} · {fila['fecha']}", file=sys.stderr)
            print(fila["texto"])
    finally:
        db.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
