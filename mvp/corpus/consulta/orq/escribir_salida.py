#!/usr/bin/env python3
"""Escribe lo que lee el usuario: la respuesta que dio el agente.

Es el único artefacto que no es para nosotros. Va la pregunta, la respuesta —tal como vino, sin
juzgarla—, lo que el agente escribió además del JSON y los casos que se leyeron. Se **agrega** al
archivo, una sección por pregunta, así una corrida no borra la anterior.

Tres desenlaces posibles:

    - el JSON de `RESPUESTA_JSON` se leyó: van el desenlace y la respuesta;
    - no se leyó: se escribe el mensaje final tal cual, diciendo que no hubo JSON;
    - no hubo mensaje final: se dice si lo cortó una guardia o si el agente no contestó.

El ORQ no corrige ni completa: registra.
"""


def escribir_salida(config, corrida, ruta_crudo):
    """Agrega la sección de esta pregunta a `salida.md` y devuelve su ruta."""
    estado = corrida["estado"]
    entrega = estado["entrega"]
    documentos = ", ".join(documento["id"] for documento in corrida["documentos"])
    # La etiqueta del crudo identifica la corrida: las dos baterías numeran 1..5.
    lineas = [f"## Pregunta {corrida['numero']} · {documentos} ({ruta_crudo.stem})", "",
              corrida["pregunta"], ""]

    if isinstance(entrega, dict):
        if entrega.get("desenlace") == "no_esta_en_el_corpus":
            lineas += ["**No está en los datos del corpus.**", ""]
        respuesta = (entrega.get("respuesta") or "").strip()
        lineas += [f"**Respuesta:** {respuesta or '(vacía)'}", ""]
        if estado.get("forma_entrega") == "dentro_del_mensaje" and estado.get("contenido_final"):
            lineas += ["**Mensaje del agente:**", "", estado["contenido_final"], ""]
    elif estado.get("contenido_final"):
        lineas += ["**Sin entrega:** el agente no escribió el JSON de RESPUESTA_JSON. "
                   "Su mensaje final decía:", "", estado["contenido_final"], ""]
    elif estado.get("corte"):
        lineas += [f"**Sin entrega:** la corrida se cortó por `{estado['corte']}` antes de que "
                   "el agente cerrara la respuesta.", ""]
    else:
        lineas += ["**Sin respuesta.** El agente no contestó.", ""]

    leidos = ", ".join(estado["casos_leidos"]) or "ninguno"
    lineas += [f"**Casos leídos:** {leidos} (de {len(corrida['casos'])})", ""]

    ruta = config["rutas"]["salida"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return ruta
