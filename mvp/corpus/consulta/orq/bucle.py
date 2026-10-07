#!/usr/bin/env python3
"""El bucle: llama, ejecuta las herramientas, apila; y el código acepta o rechaza la entrega.

El estado es la lista de mensajes. En cada turno:

    1. se llama al modelo con los mensajes y las herramientas;
    2. el mensaje del asistente vuelve **tal cual** —con sus `tool_calls` y su
       `reasoning_content`, que la API exige devolver cuando hay `tools`—;
    3. cada llamada se ejecuta y su resultado entra como un mensaje `role: "tool"` con su
       `tool_call_id`;
    4. si la llamada es `entregar`, el código la comprueba: si pasa, la corrida termina; si no,
       el motivo vuelve al agente por el mismo canal.

Se corta por `guardias.max_turnos` o `guardias.max_herramientas` (topes del orquestador, no de R).
"""

import copy
import json

from comprobar_entrega import comprobar_entrega
from ejecutar_herramienta import ejecutar_herramienta
from llamar_modelo import llamar_modelo


def bucle(config, mensajes, herramientas, db, casos, documentos):
    """Corre el bucle y devuelve el estado de la corrida."""
    cuerpos, respuestas, casos_leidos, rechazos = [], [], [], []
    entrega = None
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
            break  # contestó sin herramientas: no hay entrega formal

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
            if nombre == "leer_caso" and ok:
                casos_leidos.append(objeto["unidad_id"])
            if nombre == "entregar":
                valido, motivo = comprobar_entrega(objeto, casos, casos_leidos, documentos, db)
                rechazos.append({"desenlace": objeto.get("desenlace"), "motivo": motivo})
                if valido:
                    entrega = objeto
                    return {"entrega": entrega, "cuerpos": cuerpos, "respuestas": respuestas,
                            "casos_leidos": casos_leidos, "rechazos": rechazos,
                            "turnos": turnos, "llamadas": llamadas, "cerrado": True,
                            "mensajes": mensajes}
                texto = json.dumps({"rechazada": motivo}, ensure_ascii=False)
            mensajes.append({"role": "tool", "tool_call_id": llamada["id"], "content": texto})
            if llamadas >= config["guardias"]["max_herramientas"]:
                break

    return {"entrega": entrega, "cuerpos": cuerpos, "respuestas": respuestas,
            "casos_leidos": casos_leidos, "rechazos": rechazos, "turnos": turnos,
            "llamadas": llamadas, "cerrado": False, "mensajes": mensajes}
