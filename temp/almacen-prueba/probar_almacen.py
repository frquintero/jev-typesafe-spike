#!/usr/bin/env python3
"""Prueba del almacén **sobre copias**: ni el almacén real ni el corpus real se tocan.

    python3 temp/almacen-prueba/probar_almacen.py
"""

import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
PRUEBA = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

import almacen  # noqa: E402

# --- sobre copias ---
shutil.copy(RAIZ / "mvp" / "código" / "corpus.db", PRUEBA / "corpus-copia.db")
almacen.DB = PRUEBA / "almacen-copia.db"
almacen.CORPUS = PRUEBA / "corpus-copia.db"
for ruta in (almacen.DB,):
    if ruta.exists():
        ruta.unlink()
db = almacen.conectar()

TEXTO = "# Un título\n\n## Una sección\n\nUna oración de desarrollo.\n"
PROCEDENCIA = {"nombre": "aviones.md", "ruta": "temp/estructura/aviones.md",
               "fecha_modificacion": "2026-10-11 12:00:00"}
VOLCADO = {"id": "aviones:volcado-1", "modelo": "gpt-6-luna", "esfuerzo": "low",
           "prompt": "prompt_volcado.md", "hash_prompt": "abc123", "tokens_entrada": 900,
           "tokens_salida": 200, "tokens_pensando": 60, "cache_hit": 0, "segundos": 3.1}

print("=== 1. escribir ===")
print(" ", almacen.escribir(db, "aviones", "GENERAL", TEXTO, PROCEDENCIA, VOLCADO))
print("=== 2. escribir otra vez lo mismo (idempotente) ===")
print(" ", almacen.escribir(db, "aviones", "GENERAL", TEXTO, PROCEDENCIA, VOLCADO))
print("=== 3. el mismo id con otro texto ===")
try:
    almacen.escribir(db, "aviones", "GENERAL", TEXTO + "otra cosa.", PROCEDENCIA, VOLCADO)
except SystemExit as error:
    print("  se detiene:", error)
print("=== 4. el mismo texto con otro id ===")
try:
    almacen.escribir(db, "aviones-2", "GENERAL", TEXTO, PROCEDENCIA, VOLCADO)
except SystemExit as error:
    print("  se detiene:", error)
print("=== 5. un volcado fallido (no deja documento) ===")
print(" ", almacen.registrar_fallo(db, {**VOLCADO, "id": "roto:volcado-1"}, "respuesta cortada"))
print("=== 6. texto_de, y el sello comprobado ===")
print("  el texto sale entero:", almacen.texto_de(db, "aviones") == TEXTO)
db.execute("UPDATE documentos SET texto = texto || 'x' WHERE id = 'aviones'")
try:
    almacen.texto_de(db, "aviones")
except SystemExit as error:
    print("  se detiene:", error)
db.rollback()

print("\n=== lo que quedó en el almacén ===")
for fila in db.execute("SELECT id, coleccion, sello, nombre_fuente, fecha_radicacion FROM documentos"):
    print(f"  documento {fila['id']} · {fila['coleccion']} · sello {fila['sello'][:12]}… · "
          f"fuente {fila['nombre_fuente']} · radicado {fila['fecha_radicacion']}")
for fila in db.execute("SELECT id, documento_id, estado, motivo, tokens_entrada FROM volcados ORDER BY id"):
    print(f"  volcado   {fila['id']} · documento {fila['documento_id']} · {fila['estado']} · "
          f"motivo {fila['motivo']} · entrada {fila['tokens_entrada']}")
db.close()

print("\n=== y el espejo en el corpus (copia) ===")
import sqlite3  # noqa: E402
con = sqlite3.connect(almacen.CORPUS)
con.row_factory = sqlite3.Row
for fila in con.execute("SELECT id, dominio, sello, ubicacion_upstream FROM documentos"):
    print(f"  {fila['id']} · dominio {fila['dominio']} · sello {fila['sello'][:12]}… · "
          f"ruta {fila['ubicacion_upstream']}")
print("  ¿el sello del espejo es el del almacén?",
      con.execute("SELECT sello FROM documentos WHERE id='aviones'").fetchone()[0]
      == sqlite3.connect(almacen.DB).execute("SELECT sello FROM documentos WHERE id='aviones'").fetchone()[0])
con.close()
