#!/usr/bin/env python3
"""Arma la oferta de herramientas: R ∩ las que existen.

R **se aplica ofreciendo**: si una herramienta no está en R, no se le da al agente y no hay nada
que denegar. Las definiciones viven acá, en un solo lugar, y son las que viajan en el campo
`tools` de cada llamada.
"""

LEER_CASO = {
    "type": "function",
    "function": {
        "name": "leer_caso",
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
        "description": (
            "Entrega la respuesta y los datos que la sostienen. Si la respuesta no está en los "
            "datos del corpus, entregá desenlace 'no_esta_en_el_corpus' con el reporte."
        ),
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
                    "description": "La respuesta en una frase. Vacía si no está en el corpus.",
                },
                "datos": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Los ids de los datos que sostienen la respuesta.",
                },
                "reporte": {
                    "type": "string",
                    "description": "Qué casos leíste y qué encontraste en ellos.",
                },
            },
            "required": ["desenlace", "respuesta", "datos", "reporte"],
            "additionalProperties": False,
        },
    },
}

DEFINICIONES = {"leer_caso": LEER_CASO, "entregar": ENTREGAR}


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
