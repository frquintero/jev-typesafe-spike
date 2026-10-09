#!/usr/bin/env python3
"""Lista los casos del dominio: el id de la unidad y su caso. Nada más.

Es lo único del corpus que viaja en el prompt antes de leer: **nombres para ubicar**, sin
aspectos y sin valores. Un caso por unidad, aunque dos unidades compartan el nombre.

Los casos salen de `unidades` —el nombre es el `subtema`—, no de `datos`: una unidad sin datos
sigue siendo un caso, y la pertenencia al dominio se resuelve por `documento_id`.
"""


def listar_casos(db, documentos):
    """Devuelve [{'unidad_id', 'caso'}] de los documentos admitidos, ordenado por id."""
    marcas = ",".join("?" * len(documentos))
    filas = db.execute(
        f"SELECT id AS unidad_id, subtema AS caso FROM unidades "
        f"WHERE documento_id IN ({marcas}) ORDER BY id",
        tuple(documento["id"] for documento in documentos),
    ).fetchall()
    return [{"unidad_id": fila["unidad_id"], "caso": fila["caso"]} for fila in filas]
