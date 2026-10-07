#!/usr/bin/env python3
"""Escribe lo que lee el usuario: la respuesta con los datos que la sostienen.

Es el único artefacto que no es para nosotros. Va la pregunta, la respuesta, los datos citados
—con su aspecto y su valor, para que se pueda ver la fuente— y el recorrido. Se **agrega** al
archivo, una sección por pregunta, así una corrida no borra la anterior.
"""


def escribir_salida(config, corrida, db):
    """Agrega la sección de esta pregunta a `salida.md` y devuelve su ruta."""
    estado = corrida["estado"]
    entrega = estado["entrega"]
    lineas = [f"## Pregunta {corrida['numero']}", "", corrida["pregunta"], ""]

    if entrega is None:
        lineas += ["**Sin entrega.** El agente no entregó un objeto válido.", ""]
    elif entrega["desenlace"] == "respondida":
        lineas += [f"**Respuesta:** {entrega['respuesta']}", "", "**Datos que la sostienen:**", ""]
        for identificador in entrega["datos"]:
            fila = db.execute("SELECT aspecto, valor, unidad_valor FROM datos WHERE id = ?",
                              (identificador,)).fetchone()
            valor = fila["valor"] + (f" {fila['unidad_valor']}" if fila["unidad_valor"] else "")
            lineas.append(f"- `{identificador}` · {fila['aspecto']}: {valor}")
        lineas.append("")
    else:
        lineas += ["**No está en los datos del corpus.**", ""]

    if entrega is not None:
        leidos = ", ".join(estado["casos_leidos"]) or "ninguno"
        lineas += [f"**Recorrido:** {entrega['reporte']}", "",
                   f"**Casos leídos:** {leidos} (de {len(corrida['casos'])})", ""]

    ruta = config["rutas"]["salida"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write("\n".join(lineas) + "\n")
    return ruta
