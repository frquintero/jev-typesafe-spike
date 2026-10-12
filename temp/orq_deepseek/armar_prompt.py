#!/usr/bin/env python3
"""Arma los mensajes de la consulta: el `system` (lo que siempre va) y el `user` (la tarea).

El prompt vigente es `mvp/prompts/prompt_ORQ.md` (lo apunta `config.json`), en dos partes
marcadas:

    [SISTEMA]   lo que se conserva entre turnos: las anclas
    [TAREA]     los casos del dominio, la tarea y el formato de salida

Se rellena con `str.replace` —nunca `str.format`: el texto puede traer llaves—. Lo único dinámico
son los casos, la pregunta y las anclas. R **no** va: R la aplica el orquestador, ofreciendo
herramientas y admitiendo fuentes.
"""

MARCA_SISTEMA = "[SISTEMA]"
MARCA_TAREA = "[TAREA]"


def armar_prompt(ruta_prompt, pregunta, casos, marcas):
    """Devuelve los dos mensajes: el system con lo fijo y el user con la tarea."""
    if not ruta_prompt.exists():
        raise SystemExit(f"no está el prompt del agente en '{ruta_prompt}'")
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    if MARCA_SISTEMA not in plantilla or MARCA_TAREA not in plantilla:
        raise SystemExit(
            f"el prompt '{ruta_prompt}' tiene que traer las marcas {MARCA_SISTEMA} y {MARCA_TAREA}"
        )
    parte_sistema, parte_tarea = plantilla.split(MARCA_TAREA, 1)
    parte_sistema = parte_sistema.replace(MARCA_SISTEMA, "", 1)
    lista_casos = "\n".join(f"- {caso['unidad_id']} · {caso['caso']}" for caso in casos)

    def rellenar(texto):
        return (texto.replace("{{CASOS}}", lista_casos)
                     .replace("{{PREGUNTA}}", pregunta)
                     .replace("{{ANCLAS}}", marcas["texto"])
                     .strip())

    return [{"role": "system", "content": rellenar(parte_sistema)},
            {"role": "user", "content": rellenar(parte_tarea)}]
