#!/usr/bin/env python3
"""Arma los mensajes de la consulta: el `system` (de archivo) y la pregunta.

El prompt vive en `prompt_agente.md` y se rellena con `str.replace` —nunca `str.format`: el texto
puede traer llaves—. Lo único dinámico es el dominio, los documentos, los casos y las anclas.

R **no** va en el prompt: R la aplica el orquestador, ofreciendo herramientas y admitiendo
fuentes. Las condiciones que no se pueden hacer cumplir por código van en el prompt, como reglas.
"""


def armar_prompt(ruta_prompt, pregunta, casos, documentos, dominio, marcas):
    """Devuelve la lista de mensajes: el system con los bloques y la pregunta del usuario."""
    if not ruta_prompt.exists():
        raise SystemExit(f"no está el prompt del agente en '{ruta_prompt}'")
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    lista_documentos = "\n".join(
        f"- {documento['id']} · {documento['ubicacion_local']} "
        f"(radicado {documento['fecha_radicacion']}, sello {documento['sello'][:12]}…)"
        for documento in documentos
    )
    lista_casos = "\n".join(f"- {caso['unidad_id']} · {caso['caso']}" for caso in casos)
    texto = (plantilla
             .replace("{{DOMINIO}}", dominio)
             .replace("{{DOCUMENTOS}}", lista_documentos)
             .replace("{{CASOS}}", lista_casos)
             .replace("{{ANCLAS}}", marcas["texto"]))
    return [{"role": "system", "content": texto.strip()},
            {"role": "user", "content": pregunta}]
