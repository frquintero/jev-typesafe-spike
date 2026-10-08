#!/usr/bin/env python3
"""Arma la oferta de herramientas: R ∩ las que existen.

R **se aplica ofreciendo**: si una herramienta no está en R, no se le da al agente y no hay nada
que denegar. Las definiciones viven acá, en un solo lugar, y son las que viajan en el campo
`tools` de cada llamada.

Dos herramientas: la que trae los datos de un caso y la que le pregunta al usuario cuando la
pregunta admite dos o más respuestas plausibles. **No hay herramienta de entrega**: la respuesta
es el mensaje final del agente, y el ORQ la lee de ahí.
"""

OBTENER_DATOS_DEL_CASO = {
    "type": "function",
    "function": {
        "name": "obtener_datos_del_caso",
        "description": "Devuelve todos los datos de un caso del dominio. Se pide por su id.",
        "parameters": {
            "type": "object",
            "properties": {
                "unidad_id": {
                    "type": "string",
                    "description": "El id del caso, tal como figura en la lista de casos.",
                }
            },
            "required": ["unidad_id"],
            "additionalProperties": False,
        },
    },
}

# El ciclo termina cuando el agente la usa: el ORQ no responde la pregunta (D26).
PREGUNTAR_AL_USUARIO = {
    "type": "function",
    "function": {
        "name": "preguntar_al_usuario",
        "description": "Pregunta al usuario cuando la pregunta admite dos o más respuestas "
                       "plausibles. Poné la situación y las respuestas posibles.",
        "parameters": {
            "type": "object",
            "properties": {
                "pregunta": {
                    "type": "string",
                    "description": "La situación, clara, sucinta y autocontenida.",
                },
                "opciones": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Las dos o más respuestas plausibles.",
                },
            },
            "required": ["pregunta", "opciones"],
            "additionalProperties": False,
        },
    },
}

DEFINICIONES = {"obtener_datos_del_caso": OBTENER_DATOS_DEL_CASO,
                "preguntar_al_usuario": PREGUNTAR_AL_USUARIO}


def armar_herramientas(r):
    """Devuelve las definiciones que R ofrece. Se detiene si R pide una que no existe."""
    ofrecidas = []
    for nombre in r["herramientas"]:
        if nombre not in DEFINICIONES:
            raise SystemExit(f"R pide la herramienta '{nombre}', que no existe")
        ofrecidas.append(DEFINICIONES[nombre])
    if not ofrecidas:
        raise SystemExit("R no ofrece ninguna herramienta")
    return ofrecidas
