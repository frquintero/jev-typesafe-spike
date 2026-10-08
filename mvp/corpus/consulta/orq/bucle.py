#!/usr/bin/env python3
"""El bucle: llama, ejecuta las herramientas, apila; y termina con la respuesta del agente.

El estado es la lista de mensajes. En cada turno:

    1. se llama al modelo con los mensajes y las herramientas;
    2. si el mensaje trae llamadas, el mensaje del asistente vuelve **tal cual** —con sus
       `tool_calls` y su `reasoning_content`, que la API exige devolver cuando hay `tools`—,
       cada llamada se ejecuta y su resultado entra como un mensaje `role: "tool"` con su
       `tool_call_id`;
    3. si el mensaje **no** trae llamadas, el agente terminó: su contenido es la respuesta, y
       de ahí sale la entrega —el JSON de `RESPUESTA_JSON`, donde el prompt lo ponga
       (`leer_entrega.extraer_entrega`)—. El ORQ no la juzga: la registra tal como vino.

Se corta por `guardias.max_turnos` o `guardias.max_herramientas` (topes del orquestador, no
de R), y la causa queda en `corte`: `None` si el agente cerró; `"max_turnos"` o
`"max_herramientas"` si lo cortó una guardia.
"""

import copy

from ejecutar_herramienta import ejecutar_herramienta
from leer_entrega import extraer_entrega
from llamar_modelo import llamar_modelo


def bucle(config, mensajes, herramientas, db, casos):
    """Corre el bucle y devuelve el estado de la corrida."""
    cuerpos, respuestas, casos_leidos = [], [], []
    entrega = None
    json_entrega = None
    forma_entrega = None
    contenido_final = None
    cerrado = False
    corte = None
    turnos = 0
    llamadas = 0
    tope_herramientas = config["guardias"]["max_herramientas"]

    for turno in range(1, config["guardias"]["max_turnos"] + 1):
        turnos = turno
        cuerpo, respuesta = llamar_modelo(config, mensajes, herramientas)
        cuerpos.append(copy.deepcopy(cuerpo))  # copia: `messages` sigue creciendo
        respuestas.append(respuesta)
        mensaje = respuesta["choices"][0]["message"]
        pedidas = mensaje.get("tool_calls") or []

        if not pedidas:
            # El agente terminó: su mensaje trae la respuesta y, dentro, la entrega.
            contenido_final = (mensaje.get("content") or "").strip()
            entrega, json_entrega, forma_entrega = extraer_entrega(contenido_final)
            cerrado = True
            break

        asistente = {"role": "assistant", "content": mensaje["content"] or None,
                     "tool_calls": pedidas}
        if mensaje.get("reasoning_content"):
            asistente["reasoning_content"] = mensaje["reasoning_content"]
        mensajes.append(asistente)

        for llamada in pedidas:
            # El tope se mira **antes** de ejecutar: no se pasa del número ofrecido.
            if llamadas >= tope_herramientas:
                corte = "max_herramientas"
                break
            llamadas += 1
            nombre = llamada["function"]["name"]
            texto, ok, objeto = ejecutar_herramienta(nombre, llamada["function"]["arguments"],
                                                     db, casos)
            if nombre == "obtener_datos_del_caso" and ok:
                casos_leidos.append(objeto["unidad_id"])
            mensajes.append({"role": "tool", "tool_call_id": llamada["id"], "content": texto})
        if corte:
            break
    else:
        corte = "max_turnos"

    return {"entrega": entrega, "json_entrega": json_entrega, "forma_entrega": forma_entrega,
            "contenido_final": contenido_final, "cuerpos": cuerpos,
            "respuestas": respuestas, "casos_leidos": casos_leidos, "turnos": turnos,
            "llamadas": llamadas, "cerrado": cerrado, "corte": corte, "mensajes": mensajes}
