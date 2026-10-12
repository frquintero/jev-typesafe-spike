#!/usr/bin/env python3
"""Las plantillas de los prompts: **en la base, con su versión**.

La plantilla es el texto del prompt **con sus huecos sin llenar**: las reglas, los ejemplos, las
marcas `[SISTEMA]`/`[TAREA]` y los `{{HUECOS}}`. El material —el documento, las unidades, los
casos, la pregunta, los relojes— sale de la base en cada acto, y el prompt resuelto no se
guarda: se re-arma.

**El acto que la usa la registra.** Antes de llamar, se hashea el **borrador** (el `.md` de
`mvp/prompts/`, que es la puerta) y, si ese sello no está, se guarda como **versión nueva**.
Editar una plantilla es **otra plantilla**: una versión inscrita no se toca nunca.

Es el patrón del contenido: idempotente, sin acto manual de entrada, y la base se llena sola con
lo que efectivamente corrió.
"""

from base import hash_texto


def usar(db, identificador, borrador):
    """La plantilla para correr, registrándola si es nueva.

    `identificador` es `'volcado'`, `'UT'`, `'DATOS'` o `'ORQ'`. `borrador` es la ruta del
    archivo que se está usando. Devuelve `{'id', 'version', 'texto', 'sello'}`.
    """
    texto = borrador.read_text(encoding="utf-8")
    sello = hash_texto(texto)
    fila = db.execute("SELECT id, version, texto FROM prompts WHERE id = ? AND sello = ?",
                      (identificador, sello)).fetchone()
    if fila is not None:
        return {"id": fila["id"], "version": fila["version"], "texto": fila["texto"],
                "sello": sello}
    version = db.execute("SELECT COALESCE(MAX(version), 0) + 1 FROM prompts WHERE id = ?",
                         (identificador,)).fetchone()[0]
    db.execute("INSERT INTO prompts (id, version, texto, sello) VALUES (?,?,?,?)",
               (identificador, version, texto, sello))
    db.commit()
    return {"id": identificador, "version": version, "texto": texto, "sello": sello}


def texto(db, identificador, version=None):
    """La fila de una versión, o la última. `None` si no está."""
    if version is None:
        return db.execute("SELECT * FROM prompts WHERE id = ? ORDER BY version DESC LIMIT 1",
                          (identificador,)).fetchone()
    return db.execute("SELECT * FROM prompts WHERE id = ? AND version = ?",
                      (identificador, version)).fetchone()
