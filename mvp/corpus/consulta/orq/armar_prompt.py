#!/usr/bin/env python3
"""Arma los mensajes de la consulta: un solo `system` con el prompt y la pregunta adentro.

El prompt vive en `prompt_agente.md` y se rellena con `str.replace` —nunca `str.format`: el texto
puede traer llaves—. Lo único dinámico son los casos, la pregunta y las anclas.

Todo lo que tiene que conservarse entre turnos va acá, en el system: el prompt, la lista de casos
y las anclas. R **no** va: R la aplica el orquestador, ofreciendo herramientas y admitiendo
fuentes.
"""


def armar_prompt(ruta_prompt, pregunta, casos, marcas):
    """Devuelve los mensajes: el system con el prompt y la pregunta embebida."""
    if not ruta_prompt.exists():
        raise SystemExit(f"no está el prompt del agente en '{ruta_prompt}'")
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    lista_casos = "\n".join(f"- {caso['unidad_id']} · {caso['caso']}" for caso in casos)
    texto = (plantilla
             .replace("{{CASOS}}", lista_casos)
             .replace("{{PREGUNTA}}", pregunta)
             .replace("{{ANCLAS}}", marcas["texto"]))
    return [{"role": "system", "content": texto.strip()}]
