"""La puerta a cada base: el esquema, su versión y el token del acto.

Dos bases —`mvp/código/corpus.db`, el centro, y `mvp/código/almacen.db`, el original—, y las dos
se abren igual:

- se comprueba la **versión del esquema** (`PRAGMA user_version`, que SQLite reserva para el
  usuario). Si no coincide y la base está **vacía**, se rehace con el esquema nuevo —lo barato
  mientras no hay datos—; si tiene datos, **se detiene y reporta**: migrar es un acto explícito,
  no algo que pase de largo;
- cada base lleva su **contador** y da sus **tokens**: `C000123` en el corpus, `A000123` en el
  almacén. El token es del acto, no de la etapa: lo da un contador de una fila, no se reinicia
  solo y no depende de uuid ni de azar.
"""

import sqlite3

PREFIJO_CORPUS = "C"
PREFIJO_ALMACEN = "A"


def abrir(ruta, esquema, version):
    """Abre la base con su esquema, o se detiene si hay que migrarla a mano."""
    db = sqlite3.connect(ruta)
    db.row_factory = sqlite3.Row
    db.execute("PRAGMA foreign_keys = ON")
    actual = db.execute("PRAGMA user_version").fetchone()[0]
    if actual == version:
        db.executescript(esquema)  # idempotente: crea lo que falte, no toca lo que está
        return db
    if _tiene_datos(db):
        raise SystemExit(
            f"la base '{ruta}' tiene el esquema {actual} y se espera {version}, y ya tiene "
            f"datos: migrarla es un acto explícito. Se guarda la base y se empieza de cero, o "
            f"se escribe la transformación a mano.")
    _rehacer(db, esquema, version)
    return db


def _tablas(db):
    return [fila[0] for fila in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name NOT LIKE 'sqlite_%'")]


def _tiene_datos(db):
    """¿Hay alguna fila en alguna tabla? Una base sin tablas no tiene datos."""
    for tabla in _tablas(db):
        if db.execute(f'SELECT 1 FROM "{tabla}" LIMIT 1').fetchone() is not None:
            return True
    return False


def _rehacer(db, esquema, version):
    """Deja la base con el esquema y la versión. Solo se llama con la base sin datos."""
    db.execute("PRAGMA foreign_keys = OFF")
    for tabla in _tablas(db):
        db.execute(f'DROP TABLE IF EXISTS "{tabla}"')
    db.executescript(esquema)
    db.execute(f"PRAGMA user_version = {int(version)}")
    db.commit()
    db.execute("PRAGMA foreign_keys = ON")


def token_siguiente(db, prefijo):
    """El token del acto —`C000123`—: avanza el contador de esta base."""
    db.execute("INSERT OR IGNORE INTO contador (id, ultimo) VALUES (1, 0)")
    db.execute("UPDATE contador SET ultimo = ultimo + 1 WHERE id = 1")
    ultimo = db.execute("SELECT ultimo FROM contador WHERE id = 1").fetchone()[0]
    db.commit()
    return f"{prefijo}{ultimo:06d}"
