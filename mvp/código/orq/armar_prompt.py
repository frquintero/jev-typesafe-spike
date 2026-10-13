#!/usr/bin/env python3
"""Arma los mensajes de la consulta: el `system` (la regla) y el `user` (el material).

La **plantilla** llega de la base (con su versión), que es donde vive: el acto lee de ahí la última
versión inscrita. Viene en dos partes marcadas por `mensajes.partir`:

    [SISTEMA]   la fecha de radicación de los documentos del dominio (invariante) y la LÓGICA DEL
                AGENTE ENCARGADO con la forma de la respuesta JSON
    [TAREA]     los casos del dominio, la pregunta y —al final, porque cambia en cada consulta— el
                «ahora»

Lo único dinámico son los casos, la pregunta y el reloj del sistema. R **no** va: R la aplica el
orquestador, ofreciendo herramientas y admitiendo fuentes.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from mensajes import partir  # noqa: E402
from relojes import reloj_radicados, reloj_sistema_de  # noqa: E402


def armar_prompt(plantilla, rotulo, pregunta, casos, marcas, documentos=()):
    """Devuelve los dos mensajes: el system con la regla y el radicado, y el user con la tarea."""
    for hueco in ("{{RELOJ_RADICADO}}", "{{CASOS}}", "{{PREGUNTA}}", "{{RELOJ_SISTEMA}}"):
        if hueco not in plantilla:
            raise SystemExit(f"la plantilla '{rotulo}' no tiene {hueco}")
    lista_casos = "\n".join(f"- {caso['unidad_id']} · {caso['caso']}" for caso in casos)
    return partir(plantilla, rotulo, CASOS=lista_casos, PREGUNTA=pregunta,
                  RELOJ_RADICADO=reloj_radicados(documentos),
                  RELOJ_SISTEMA=reloj_sistema_de(marcas))
