#!/usr/bin/env python3
"""Carga los datos de un documento radicado: de los crudos de la extracción a la base.

Es un acto **posterior y aparte** de la radicación: no toca la fila del documento —su nombre, su
fecha y su hora no se mueven— y escribe solo las filas de datos de ese documento. Si los datos ya
están cargados, no hace nada; para reemplazarlos por los de otra extracción hay que pedirlo con
`--recargar` (otro acto, explícito).

Uso:

    python3 mvp/código/cargar_datos.py doc8 p1-doc8-UT-deepseek-r1.out r1
    python3 mvp/código/cargar_datos.py doc8 p1-doc8-UT-deepseek-r1.out r1 --recargar

Lee, de `mvp/temp/extraccion/<doc>/`: el `.out` de las unidades (que se pasa como argumento) y, por
cada unidad, `p2-<doc>-u<n>-<rN>.out`; el `caso` del dato es el que traiga el paso 2, y si no lo
trae, el nombre del subtema. Antes de escribir nada, compara el sello del documento con el que
guardó la base: si el texto cambió, se detiene y lo reporta.
"""

import hashlib
import json
import pathlib
import sys

from base import RAIZ, borrar_datos, conectar, datos_de


def cargar(identificador, p1, rep, recargar):
    db = conectar()
    fila = db.execute("SELECT ubicacion_upstream, sello FROM documentos WHERE id = ?",
                      (identificador,)).fetchone()
    if fila is None:
        raise SystemExit(f"'{identificador}' no está radicado: la radicación es el acto que va "
                         f"primero (python3 mvp/código/radicar.py {identificador})")

    documento = RAIZ / fila[0]
    if hashlib.sha256(documento.read_bytes()).hexdigest() != fila[1]:
        raise SystemExit(f"el texto de '{identificador}' cambió desde que se radicó: eso es otro "
                         f"documento. Se radica de nuevo con otro nombre (o, en pruebas, --rehacer).")

    ya = datos_de(db, identificador)
    if ya and not recargar:
        print(f"  {identificador}: ya tiene {ya} datos cargados — no se toca. "
              f"(Para reemplazarlos por los de esta extracción: --recargar)")
        return

    carpeta = RAIZ / "mvp" / "temp" / "extraccion" / identificador
    ruta_unidades = carpeta / p1
    if not ruta_unidades.is_file():
        raise SystemExit(f"no está '{ruta_unidades.relative_to(RAIZ)}': "
                         f"el paso 1 no dejó ahí las unidades de '{identificador}'")
    unidades = json.loads(ruta_unidades.read_text(encoding="utf-8"))["subtemas"]

    # Primero se lee todo; recién después se escribe: si falta una unidad, no queda media carga.
    por_unidad = []
    for n, unidad in enumerate(unidades, 1):
        ruta = carpeta / f"p2-{identificador}-u{n}-{rep}.out"
        if not ruta.is_file():
            raise SystemExit(f"no está '{ruta.relative_to(RAIZ)}': el paso 2 no dejó los datos de "
                             f"la unidad {n} de '{identificador}' (réplica {rep})")
        por_unidad.append((n, unidad, json.loads(ruta.read_text(encoding="utf-8"))))

    if ya:
        print(f"  {identificador}: ACTO explícito — se reemplazan sus {ya} datos por los de {p1}/{rep}")
        borrar_datos(db, identificador)
    cargados = 0
    for n, unidad, datos in por_unidad:
        uid = f"{identificador}:U{n}"
        for j, dato in enumerate(datos.get("datos") or [], 1):
            db.execute("INSERT INTO datos VALUES (?,?,?,?,?,?)",
                       (f"{uid}:D{j}", uid, dato.get("caso") or unidad["subtema"],
                        dato["aspecto"], dato["valor"], dato.get("unidad_valor")))
            cargados += 1
    db.commit()
    fecha = db.execute("SELECT fecha_radicacion FROM documentos WHERE id = ?",
                       (identificador,)).fetchone()[0]
    print(f"  {identificador}: {len(por_unidad)} unidades · {cargados} datos cargados "
          f"(la radicación no se movió: sigue {fecha})")


def main(argumentos):
    if len(argumentos) < 3 or len(argumentos) > 4:
        raise SystemExit("uso: python3 mvp/código/cargar_datos.py <doc> <p1.out> <rN> [--recargar]")
    identificador, p1, rep = argumentos[0], argumentos[1], argumentos[2]
    recargar = "--recargar" in argumentos[3:]
    cargar(identificador, p1, rep, recargar)


if __name__ == "__main__":
    main(sys.argv[1:])
