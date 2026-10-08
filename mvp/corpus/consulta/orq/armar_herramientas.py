#!/usr/bin/env python3
"""Arma la oferta de herramientas: R ∩ las que existen.

R **se aplica ofreciendo**: si una herramienta no está en R, no se le da al agente y no hay nada
que denegar. Las definiciones viven acá, en un solo lugar, y son las que viajan en el campo
`tools` de cada llamada.

Las dos herramientas, y nada más: la que trae los datos de un caso y la que entrega el JSON.
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

ENTREGAR = {
    "type": "function",
    "function": {
        "name": "entregar",
        "description": "Entrega la respuesta en el JSON de RESPUESTA_JSON.",
        "parameters": {
            "type": "object",
            "properties": {
                "desenlace": {
                    "type": "string",
                    "enum": ["respondida", "no_esta_en_el_corpus"],
                    "description": "'respondida' si hay respuesta; 'no_esta_en_el_corpus' si no.",
                },
                "respuesta": {
                    "type": "string",
                    "description": "La respuesta corta y autocontenida; vacía si no está en el corpus.",
                },
            },
            "required": ["desenlace", "respuesta"],
            "additionalProperties": False,
        },
    },
}

DEFINICIONES = {"obtener_datos_del_caso": OBTENER_DATOS_DEL_CASO, "entregar": ENTREGAR}


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
