#!/usr/bin/env python3
"""Escribe lo que lee el usuario: la respuesta que entregó el agente.

Es el único artefacto que no es para nosotros. Va la pregunta, la respuesta —tal como vino en el
JSON, sin juzgarla— y los casos que se leyeron. Se **agrega** al archivo, una sección por
pregunta, así una corrida no borra la anterior.
"""


def escribir_salida(config, corrida):
    """Agrega la sección de esta pregunta a `salida.md` y devuelve su ruta."""
    estado = corrida["estado"]
    entrega = estado["entrega"]
    lineas = [f"## Pregunta {corrida['numero']}", "", corrida["pregunta"], ""]

    if not isinstance(entrega, dict):
        lineas += ["**Sin entrega.** El agente no entregó el JSON.", ""]
    elif entrega.get("desenlace") == "no_esta_en_el_corpus":
        lineas += ["**No está en los datos del corpus.**", ""]
        if entrega.get("respuesta"):
            lineas += [f"**Respuesta:** {entrega['respuesta']}", ""]
    else:
        lineas += [f"**Respuesta:** {entrega.get('respuesta') or ''}", ""]

    leidos = ", ".join(estado["casos_leidos"]) or "ninguno"
    lineas += [f"**Casos leídos:** {leidos} (de {len(corrida['casos'])})", ""]

    ruta = config["rutas"]["salida"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return ruta
