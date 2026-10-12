#!/usr/bin/env python3
"""Lista los casos del dominio: el id de la unidad y su caso. Nada más.

Es lo único del corpus que viaja en el prompt antes de leer: **nombres para ubicar**, sin
aspectos y sin valores. Un caso por unidad, aunque dos unidades compartan el nombre.

Los casos salen de la **UT vigente** de cada documento —el nombre es el `subtema`—, no de `datos`:
una unidad sin datos sigue siendo un caso. Y cada caso viaja con **la tanda de DATOS que se le
ofreció** (`datos_token`): con dos tandas sobre la misma UT, el catálogo tiene que decir cuál se
leyó.

La vigencia se resuelve **una sola vez, acá**, al abrir la consulta: es donde se congela, como la
hora en `anclas`.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from base import datos_vigente, unidades_vigentes  # noqa: E402


def listar_casos(db, documentos):
    """Devuelve [{'unidad_id', 'caso', 'datos_token'}] de los documentos admitidos."""
    casos = []
    for documento in documentos:
        tanda = datos_vigente(db, documento["id"])
        for unidad in unidades_vigentes(db, documento["id"]):
            casos.append({"unidad_id": unidad["id"], "caso": unidad["subtema"],
                          "datos_token": tanda})
    return casos
