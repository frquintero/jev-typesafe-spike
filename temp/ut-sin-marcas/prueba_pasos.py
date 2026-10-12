#!/usr/bin/env python3
"""Prueba de punta a punta de los pasos 1 y 2 **contra una copia de la base**.

La base real no se toca: `base.DB` se apunta a `temp/…/corpus-prueba.db`. El documento no se copia:
la fila apunta al archivo real (`mvp/documentos/sol.md`) y su sello es el del archivo, así que el
acto lo lee de ahí y escribe sus unidades —con sus tramos— en la copia.

    bash -ic 'python3 temp/ut-sin-marcas/prueba_pasos.py'
"""

import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

import base  # noqa: E402

base.DB = RAIZ / "temp" / "ut-sin-marcas" / "out" / "corpus-prueba.db"
if base.DB.exists():
    base.DB.unlink()

db = base.conectar()
db.execute("INSERT INTO documentos (id, dominio, ubicacion_upstream, sello) VALUES (?,?,?,?)",
           ("sol-prueba", "GENERAL", "mvp/documentos/sol.md",
            base.hash_de(RAIZ / "mvp" / "documentos" / "sol.md")))
db.commit()
db.close()
print(f"copia de la base: {base.DB.relative_to(RAIZ)}")
print("sol-prueba: radicado apuntando al archivo real, sin copiarlo\n")

import paso1_unidades  # noqa: E402
import paso2_datos  # noqa: E402

paso1_unidades.run("sol-prueba", "luna", "UT", False, "low")
print()
paso2_datos.run("sol-prueba", "deepseek", False, None)

db = base.conectar()
texto = (RAIZ / "mvp" / "documentos" / "sol.md").read_text(encoding="utf-8").strip()
filas = db.execute("SELECT unidad_id, n, desde, hasta, texto FROM unidad_oraciones "
                   "ORDER BY unidad_id, n").fetchall()
malas = [dict(f) for f in filas if texto[f["desde"]:f["hasta"]] != f["texto"]]
print()
print(f"unidad_oraciones: {len(filas)} filas · tramos que no devuelven su oración: {len(malas)}")
for f in filas:
    print(f'  {f["unidad_id"]} · {f["n"]} · {f["desde"]:>4}–{f["hasta"]:<4} {f["texto"][:64]}…')
print(f'unidades: {db.execute("SELECT count(*) FROM unidades").fetchone()[0]} · '
      f'datos: {db.execute("SELECT count(*) FROM datos").fetchone()[0]}')
db.close()
