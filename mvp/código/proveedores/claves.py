"""Las claves: el único lugar que lee el entorno, y **nunca se imprimen**.

Se leen por host (`CLAVE_POR_HOST`) y van en la cabecera que cada proveedor usa: `Authorization:
Bearer` en los compatibles con OpenAI, `x-api-key` + `anthropic-version` en Anthropic. El cuerpo
que se devuelve **no lleva cabeceras**: la clave no entra en ningún archivo ni en la base.

Acá vive también `ErrorDeLlamada`: lo que impidió completar una llamada —una clave que falta o una
respuesta de la API—. Los corredores lo atrapan, dejan la corrida marcada como fallida con su motivo
y se detienen: un fallo no se pierde.
"""

import os

CLAVE_POR_HOST = {
    "api.deepseek.com": "DEEPSEEK_API_KEY",
    "api.z.ai": "ZAI_API_KEY",
    "api.x.ai": "XAI_API_KEY",
    "api.anthropic.com": "ANTHROPIC_API_KEY",
}

UA = "spike-jev/1.0"


class ErrorDeLlamada(Exception):
    """La llamada no se pudo completar: falta la clave, o la API contestó con un error."""


def variable(url):
    """El nombre de la variable de entorno del host de esa URL, o None si no está mapeado."""
    return CLAVE_POR_HOST.get(url.split("/")[2])


def clave(url):
    """La clave del host, o cadena vacía si la variable no está en el entorno."""
    return os.environ.get(variable(url) or "", "")


def exigir(url):
    """Se detiene si falta la clave: no se sigue a ciegas ni se busca por otros medios."""
    if not clave(url):
        raise ErrorDeLlamada(f"falta {variable(url) or 'la clave'} en el entorno "
                             f"(los shells no interactivos no la cargan: correr con bash -ic)")


def cabeceras(proveedor, url, conv_id=None):
    """Las cabeceras de la petición, según el proveedor."""
    cabeceras = {"content-type": "application/json", "user-agent": UA}
    valor = clave(url)
    if proveedor == "anthropic":
        cabeceras["anthropic-version"] = "2023-06-01"
        if valor:
            cabeceras["x-api-key"] = valor
    else:
        if valor:
            cabeceras["Authorization"] = f"Bearer {valor}"
        # xAI enruta el caché por conversación; sin esto no hay caché entre turnos (D10g).
        if conv_id and url.split("/")[2] == "api.x.ai":
            cabeceras["x-grok-conv-id"] = conv_id
    return cabeceras
