#!/usr/bin/env python3
"""Arma los mensajes de la consulta: el `system` (la regla) y el `user` (el material).

El prompt vigente es `mvp/prompts/prompt_ORQ.md` (lo apunta `config.json`), en dos partes marcadas
por `mensajes.partir`:

    [SISTEMA]   la LÓGICA DEL AGENTE ENCARGADO y la forma de la respuesta JSON
    [TAREA]     las anclas, los casos del dominio y la pregunta

Lo único dinámico son los casos, la pregunta y las anclas. R **no** va: R la aplica el orquestador,
ofreciendo herramientas y admitiendo fuentes.
"""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from mensajes import partir  # noqa: E402


def armar_prompt(ruta_prompt, pregunta, casos, marcas):
    """Devuelve los dos mensajes: el system con la regla y el user con la tarea."""
    if not ruta_prompt.exists():
        raise SystemExit(f"no está el prompt del agente en '{ruta_prompt}'")
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    lista_casos = "\n".join(f"- {caso['unidad_id']} · {caso['caso']}" for caso in casos)
    return partir(plantilla, ruta_prompt.name, CASOS=lista_casos, PREGUNTA=pregunta,
                  ANCLAS=marcas["texto"])
