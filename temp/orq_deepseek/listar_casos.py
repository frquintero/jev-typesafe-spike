#!/usr/bin/env python3
"""Lista los casos del dominio: el id de la unidad y su caso. Nada más.

Es lo único del corpus que viaja en el prompt antes de leer: **nombres para ubicar**, sin
aspectos y sin valores. Un caso por unidad, aunque dos unidades compartan el nombre.

El filtro por documento se hace por el prefijo del id (`doc4:U1` → `doc4`), porque `datos` no
lleva `documento_id`: la pertenencia se resuelve contra los documentos ya admitidos.
"""


def listar_casos(db, documentos):
    """Devuelve [{'unidad_id', 'caso'}] de los documentos admitidos, ordenado por id."""
    marcas = ",".join("?" * len(documentos))
    filas = db.execute(
        f"SELECT unidad_id, min(caso) AS caso FROM datos "
        f"WHERE substr(unidad_id, 1, instr(unidad_id, ':') - 1) IN ({marcas}) "
        f"GROUP BY unidad_id ORDER BY unidad_id",
        tuple(documento["id"] for documento in documentos),
    ).fetchall()
    return [{"unidad_id": fila["unidad_id"], "caso": fila["caso"]} for fila in filas]
