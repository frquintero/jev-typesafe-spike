#!/usr/bin/env python3
"""Radica una pregunta: **la única entrada de la consulta**.

La pregunta se lee **siempre de la base** (la tabla `preguntas`). Lo que cambia es de dónde se
**carga** para radicarla:

    python3 mvp/código/radicar_pregunta.py <archivo> --dominio E     # de un archivo: todas sus preguntas
    python3 mvp/código/radicar_pregunta.py --texto "…" --dominio E   # tecleada (el chat)

**Radicar** es anotar el texto, el **dominio** —el alcance, la unidad semántica donde vive la
pregunta, la misma etiqueta que llevan los documentos—, la **fuente** (de qué archivo se leyó, o
`tecleada`) y la **fecha y la hora**, que pone la base.

No llama al modelo y **no escribe una corrida**: la fila **es** la cédula del acto. Es idempotente
por texto y dominio: si esa pregunta ya está radicada, no la duplica y lo dice.
"""

import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from base import conectar  # noqa: E402

NUMERO = re.compile(r"^\d+[.)]\s*(.+)$")


def preguntas_de(ruta):
    """Las preguntas de un archivo: una por línea, con número o sin él."""
    preguntas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        coincidencia = NUMERO.match(linea)
        preguntas.append(coincidencia.group(1).strip() if coincidencia else linea)
    return preguntas


def radicar(db, texto, dominio, fuente):
    """Radica una pregunta. Devuelve `(id, estado)`: `radicada` o `ya_estaba`."""
    ya = db.execute("SELECT id FROM preguntas WHERE dominio = ? AND texto = ?",
                    (dominio, texto)).fetchone()
    if ya is not None:
        return ya["id"], "ya_estaba"
    db.execute("INSERT INTO preguntas (dominio, texto, fuente) VALUES (?,?,?)",
               (dominio, texto, fuente))
    db.commit()
    fila = db.execute("SELECT id FROM preguntas WHERE dominio = ? AND texto = ?",
                      (dominio, texto)).fetchone()
    return fila["id"], "radicada"


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/radicar_pregunta.py <archivo> --dominio E · "
                         "python3 mvp/código/radicar_pregunta.py --texto \"…\" --dominio E")
    origen, texto, dominio = None, None, None
    resto = list(argumentos)
    while resto:
        opcion = resto.pop(0)
        if opcion == "--texto" and resto:
            texto = resto.pop(0)
        elif opcion == "--dominio" and resto:
            dominio = resto.pop(0)
        elif origen is None and not opcion.startswith("--"):
            origen = opcion
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: radicar_pregunta.py <archivo> "
                             f"--dominio E · radicar_pregunta.py --texto \"…\" --dominio E")
    if dominio is None:
        raise SystemExit("falta --dominio: la pregunta vive en un dominio (la unidad semántica)")
    if not dominio.strip():
        raise SystemExit("el dominio está vacío: la pregunta vive en un dominio (la unidad semántica)")
    dominio = dominio.strip()
    if (origen is None) == (texto is None):
        raise SystemExit("hay que pasar un archivo **o** --texto, no los dos ni ninguno")

    if texto is not None:
        if not texto.strip():
            raise SystemExit("la pregunta está vacía: una pregunta sin texto no se radica")
        filas = [(texto.strip(), "tecleada")]
    else:
        ruta = pathlib.Path(origen)
        if not ruta.is_file():
            raise SystemExit(f"no está el archivo '{origen}'")
        filas = [(pregunta, str(ruta.resolve())) for pregunta in preguntas_de(ruta)]
    if not filas:
        raise SystemExit(f"'{origen}' no trae ninguna pregunta")

    db = conectar()
    for contenido, fuente in filas:
        identificador, estado = radicar(db, contenido, dominio, fuente)
        print(f"  {estado}: q{identificador} · {dominio} · {fuente}")
        print(f"    {contenido}")
    db.close()
    print(f"    -> la base: {len(filas)} pregunta(s) en `preguntas`")


if __name__ == "__main__":
    main(sys.argv[1:])
