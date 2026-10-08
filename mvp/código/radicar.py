#!/usr/bin/env python3
"""Radica un documento: lo graba en `mvp/documentos/` y la base anota su nombre, fecha y hora.

El acto es uno y es simple: el texto queda en la carpeta de los documentos radicados, y la base le
pone su fila con **la fecha y la hora del momento** (las pone ella). Nada más. La extracción, la
carga de los datos y la consulta son actos **posteriores y separados**, y ninguno se dispara solo.

Uso:

    python3 mvp/código/radicar.py doc8                     radica el texto que ya está en mvp/documentos/doc8.md
    python3 mvp/código/radicar.py doc8 --desde <ruta>      lo graba antes, desde otro archivo
    python3 mvp/código/radicar.py doc8 --dominio MONTAÑA
    python3 mvp/código/radicar.py --estado                 qué hay radicado (solo lee)
    python3 mvp/código/radicar.py --rehacer doc8           ACTO DE PRUEBAS: saca su fila y sus datos

Qué guarda la fila: el nombre; el dominio (GENERAL por defecto); la fecha y la hora, que pone la
base; dónde vive el documento, en esta máquina y en el repo; y su **sello** (sha256 del texto: es la
identidad de lo radicado, y si el archivo cambia después la carga de los datos se detiene y lo
reporta). De la vida del repo —commits incluidos— **no va nada**: el sello alcanza.

**Un documento radicado no se mueve**: si su texto cambia, eso es otro documento.
"""

import hashlib
import pathlib
import sys

from base import DOCUMENTOS, RAIZ, conectar, datos_de, borrar_datos


def radicar(identificador, dominio, origen):
    """El acto: el texto en `mvp/documentos/<doc>.md` y la fila con nombre, fecha y hora."""
    destino = DOCUMENTOS / f"{identificador}.md"
    db = conectar()
    if db.execute("SELECT 1 FROM documentos WHERE id = ?", (identificador,)).fetchone():
        raise SystemExit(f"'{identificador}' ya está radicado: un documento radicado no se mueve. "
                         f"(En pruebas, para rehacerlo: --rehacer {identificador})")
    if origen is not None:
        entrada = pathlib.Path(origen)
        if not entrada.is_file():
            raise SystemExit(f"no está el archivo de origen '{origen}'")
        if destino.exists():
            raise SystemExit(f"ya hay un documento en '{destino.relative_to(RAIZ)}': "
                             f"no se sobrescribe")
        DOCUMENTOS.mkdir(parents=True, exist_ok=True)
        destino.write_bytes(entrada.read_bytes())
    if not destino.is_file():
        raise SystemExit(f"el texto no está en '{destino.relative_to(RAIZ)}': se graba ahí, "
                         f"o se pasa --desde <ruta>")

    sello = hashlib.sha256(destino.read_bytes()).hexdigest()
    db.execute("INSERT INTO documentos (id, dominio, ubicacion_local, ubicacion_upstream, "
               "sello) VALUES (?,?,?,?,?)",
               (identificador, dominio, str(destino), str(destino.relative_to(RAIZ)), sello))
    db.commit()
    fecha = db.execute("SELECT fecha_radicacion FROM documentos WHERE id = ?",
                       (identificador,)).fetchone()[0]
    print(f"  {identificador}: radicado {fecha} · {destino.relative_to(RAIZ)}")
    print(f"    dominio {dominio} · sello {sello[:12]}…")
    print("    Sigue, en actos aparte: extraer (paso 1 y paso 2) y cargar los datos.")


def rehacer(identificador):
    """ACTO DE PRUEBAS: saca la fila del documento y sus datos, para poder radicarlo de nuevo."""
    db = conectar()
    if not db.execute("SELECT 1 FROM documentos WHERE id = ?", (identificador,)).fetchone():
        raise SystemExit(f"'{identificador}' no está radicado: no hay nada que rehacer")
    datos = datos_de(db, identificador)
    print(f"  {identificador}: ACTO DE PRUEBAS — se saca su fila y sus {datos} datos")
    borrar_datos(db, identificador)
    db.execute("DELETE FROM documentos WHERE id = ?", (identificador,))
    db.commit()
    print("    (el texto en mvp/documentos/ queda: se puede radicar de nuevo)")


def estado():
    """Lo que hay radicado. Solo lee."""
    db = conectar()
    filas = db.execute("SELECT id, dominio, fecha_radicacion, ubicacion_upstream, sello "
                       "FROM documentos ORDER BY fecha_radicacion").fetchall()
    if not filas:
        print("  (no hay documentos radicados)")
        return
    for identificador, dominio, fecha, ubicacion, sello in filas:
        print(f"  {identificador}: radicado {fecha} · {dominio} · {datos_de(db, identificador)} datos"
              f" · {ubicacion} · sello {sello[:12]}…")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/radicar.py <doc> [--dominio D] [--desde ruta] "
                         "· --estado · --rehacer <doc>")
    if argumentos[0] == "--estado":
        estado()
        return
    if argumentos[0] == "--rehacer":
        if len(argumentos) != 2:
            raise SystemExit("uso: radicar.py --rehacer <doc>")
        rehacer(argumentos[1])
        return
    identificador = argumentos[0]
    dominio, origen = "GENERAL", None
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion in ("--dominio", "--desde") and resto:
            valor = resto.pop(0)
            if opcion == "--dominio":
                dominio = valor
            else:
                origen = valor
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: radicar.py <doc> "
                             f"[--dominio D] [--desde ruta] · --estado · --rehacer <doc>")
    radicar(identificador, dominio, origen)


if __name__ == "__main__":
    main(sys.argv[1:])
