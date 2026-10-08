#!/usr/bin/env python3
"""Escribe lo que lee el usuario: la respuesta que dio el agente.

Es el único artefacto que no es para nosotros. Va la pregunta, la respuesta —tal como vino, sin
juzgarla— y los casos que se leyeron. Se **agrega** al archivo, una sección por pregunta, así una
corrida no borra la anterior.

Si el agente no contestó con el JSON de RESPUESTA_JSON, se escribe lo que contestó: el ORQ no
corrige ni completa.
"""


def escribir_salida(config, corrida):
    """Agrega la sección de esta pregunta a `salida.md` y devuelve su ruta."""
    estado = corrida["estado"]
    entrega = estado["entrega"]
    lineas = [f"## Pregunta {corrida['numero']}", "", corrida["pregunta"], ""]

    if isinstance(entrega, dict) and entrega.get("desenlace") == "no_esta_en_el_corpus":
        lineas += ["**No está en los datos del corpus.**", ""]
        if entrega.get("respuesta"):
            lineas += [f"**Respuesta:** {entrega['respuesta']}", ""]
    elif isinstance(entrega, dict):
        lineas += [f"**Respuesta:** {entrega.get('respuesta') or ''}", ""]
    elif estado.get("contenido_final"):
        lineas += ["**Respuesta del agente (sin JSON):**", "", estado["contenido_final"], ""]
    else:
        lineas += ["**Sin respuesta.** El agente no contestó.", ""]

    leidos = ", ".join(estado["casos_leidos"]) or "ninguno"
    lineas += [f"**Casos leídos:** {leidos} (de {len(corrida['casos'])})", ""]

    ruta = config["rutas"]["salida"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return ruta
