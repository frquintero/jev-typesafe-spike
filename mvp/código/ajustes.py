#!/usr/bin/env python3
"""Los ajustes de cada acto: **qué modelo y qué esfuerzo**, en la base.

Una fila por acto (`volcado`, `UT`, `DATOS`, `ORQ`): la **política** del default. El **hecho** —con
qué modelo y esfuerzo corrió de verdad— lo guarda cada corrida, en su propia fila.

La precedencia es de tres escalones: **la línea de comandos > la base > el código**. Así el default
se cambia con un `UPDATE` (sin tocar código) y un acto puntual se puede pisar con `--modelo` o
`--esfuerzo`, sin dejar rastro en la base.

La base elige **entre los alias registrados** en `mvp/código/proveedores/`: ahí viven la URL, la
clave y el nombre real del modelo, que son código. Para estrenar un modelo que no está en el
registro, primero se declara ahí; después se elige desde acá.
"""

POR_DEFECTO = ("volcado", "UT", "DATOS", "ORQ")
MODELO_POR_DEFECTO = "luna"
ESFUERZO_POR_DEFECTO = "low"


def sembrar(db):
    """Deja el renglón de cada acto si falta. No pisa lo que ya está."""
    for paso in POR_DEFECTO:
        db.execute("INSERT OR IGNORE INTO ajustes (paso, modelo, esfuerzo) VALUES (?,?,?)",
                   (paso, MODELO_POR_DEFECTO, ESFUERZO_POR_DEFECTO))
    db.commit()


def de(db, paso):
    """El ajuste de un acto, o `None` si no está."""
    fila = db.execute("SELECT paso, modelo, esfuerzo FROM ajustes WHERE paso = ?",
                      (paso,)).fetchone()
    return dict(fila) if fila else None


def resolver(db, paso, modelo=None, esfuerzo=None):
    """El modelo y el esfuerzo del acto: la línea de comandos > la base > el código."""
    fila = de(db, paso) or {}
    return (modelo or fila.get("modelo") or MODELO_POR_DEFECTO,
            esfuerzo or fila.get("esfuerzo") or ESFUERZO_POR_DEFECTO)


def todos(db):
    """Los cuatro renglones, para leerlos o mostrarlos."""
    return [dict(fila) for fila in db.execute(
        "SELECT paso, modelo, esfuerzo FROM ajustes ORDER BY paso")]
