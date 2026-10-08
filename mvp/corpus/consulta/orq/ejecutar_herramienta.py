#!/usr/bin/env python3
"""Ejecuta la herramienta que pide el agente y arma qué contestarle.

El único canal de vuelta es el mensaje `role: "tool"`: **lo que no viaje ahí, el agente no lo
sabe**. Los errores —un id que no está en la lista, argumentos que no son JSON— vuelven por el
mismo canal, para que el agente pueda corregirse en el turno siguiente.

Devuelve (texto, ok, objeto): `objeto` es el caso leído, cuando la herramienta es
`obtener_datos_del_caso`.
"""

import json

from obtener_datos_del_caso import obtener_datos_del_caso


def ejecutar_herramienta(nombre, argumentos_crudos, db, casos):
    """Ejecuta la llamada. Devuelve (texto para el agente, ok, objeto o None)."""
    try:
        argumentos = json.loads(argumentos_crudos or "{}")
    except json.JSONDecodeError as error:
        return json.dumps({"error": f"los argumentos no son JSON válido: {error}"},
                          ensure_ascii=False), False, None
    if not isinstance(argumentos, dict):
        return json.dumps({"error": "los argumentos tienen que ser un objeto"},
                          ensure_ascii=False), False, None

    if nombre == "obtener_datos_del_caso":
        unidad_id = argumentos.get("unidad_id")
        if not isinstance(unidad_id, str) or not unidad_id.strip():
            return json.dumps({"error": "falta 'unidad_id'"}, ensure_ascii=False), False, None
        caso, error = obtener_datos_del_caso(db, unidad_id.strip(), casos)
        if error:
            return json.dumps({"error": error}, ensure_ascii=False), False, None
        return json.dumps(caso, ensure_ascii=False), True, caso

    return json.dumps({"error": f"herramienta desconocida: {nombre}"},
                      ensure_ascii=False), False, None
