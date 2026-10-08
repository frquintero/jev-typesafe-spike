#!/usr/bin/env python3
"""El bucle: llama, ejecuta las herramientas, apila; y termina con la respuesta del agente.

El estado es la lista de mensajes. En cada turno:

    1. se llama al modelo con los mensajes y las herramientas;
    2. si el mensaje trae llamadas, el mensaje del asistente vuelve **tal cual** —con sus
       `tool_calls` y su `reasoning_content`, que la API exige devolver cuando hay `tools`—,
       cada llamada se ejecuta y su resultado entra como un mensaje `role: "tool"` con su
       `tool_call_id`;
    3. si el mensaje **no** trae llamadas, el agente terminó: su contenido es la respuesta, y el
       ORQ la lee de ahí (el JSON de RESPUESTA_JSON). No la juzga: la registra tal como vino.

Se corta por `guardias.max_turnos` o `guardias.max_herramientas` (topes del orquestador, no de R).
"""

import copy
import json

from ejecutar_herramienta import ejecutar_herramienta
from llamar_modelo import llamar_modelo


def bucle(config, mensajes, herramientas, db, casos):
    """Corre el bucle y devuelve el estado de la corrida."""
    cuerpos, respuestas, casos_leidos = [], [], []
    entrega = None
    contenido_final = None
    cerrado = False
    turnos = 0
    llamadas = 0

    for turno in range(1, config["guardias"]["max_turnos"] + 1):
        turnos = turno
        cuerpo, respuesta = llamar_modelo(config, mensajes, herramientas)
        cuerpos.append(copy.deepcopy(cuerpo))  # copia: `messages` sigue creciendo
        respuestas.append(respuesta)
        mensaje = respuesta["choices"][0]["message"]
        pedidas = mensaje.get("tool_calls") or []

        if not pedidas:
            # El agente terminó: lo que trae el mensaje es su respuesta.
            contenido_final = (mensaje.get("content") or "").strip()
            try:
                entrega = json.loads(contenido_final) if contenido_final else None
            except json.JSONDecodeError:
                entrega = None  # no vino JSON: se registra el texto tal cual
            cerrado = True
            break

        asistente = {"role": "assistant", "content": mensaje["content"] or None,
                     "tool_calls": pedidas}
        if mensaje.get("reasoning_content"):
            asistente["reasoning_content"] = mensaje["reasoning_content"]
        mensajes.append(asistente)

        for llamada in pedidas:
            llamadas += 1
            nombre = llamada["function"]["name"]
            texto, ok, objeto = ejecutar_herramienta(nombre, llamada["function"]["arguments"],
                                                     db, casos)
            if nombre == "obtener_datos_del_caso" and ok:
                casos_leidos.append(objeto["unidad_id"])
            mensajes.append({"role": "tool", "tool_call_id": llamada["id"], "content": texto})
            if llamadas >= config["guardias"]["max_herramientas"]:
                break

    return {"entrega": entrega, "contenido_final": contenido_final, "cuerpos": cuerpos,
            "respuestas": respuestas, "casos_leidos": casos_leidos, "turnos": turnos,
            "llamadas": llamadas, "cerrado": cerrado, "mensajes": mensajes}
