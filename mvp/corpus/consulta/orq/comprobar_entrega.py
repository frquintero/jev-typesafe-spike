#!/usr/bin/env python3
"""Comprueba la entrega: forma, alcance y cobertura. Es lo que el código no delega.

Reglas de esta versión (el sobre mínimo):

    - `desenlace` tiene que ser uno de los dos estados, y el `reporte` tiene que estar;
    - con «respondida»: hay respuesta, se cita al menos un dato, y cada dato citado existe, es
      del dominio y es de un caso que el agente **leyó**;
    - con «no_esta_en_el_corpus»: el agente tiene que haber leído **todos** los casos de la
      lista. Es la diferencia entre «agoté» y «me cansé».

Devuelve (ok, motivo). El motivo, cuando falla, vuelve al agente por el canal `tool`.
"""

ESTADOS = ("respondida", "no_esta_en_el_corpus")


def comprobar_entrega(entrega, casos, casos_leidos, documentos, db):
    """Devuelve (True, "aceptada") o (False, motivo)."""
    if not isinstance(entrega, dict):
        return False, "la entrega no es un objeto"

    desenlace = entrega.get("desenlace")
    if desenlace not in ESTADOS:
        return False, f"'desenlace' tiene que ser uno de: {', '.join(ESTADOS)}"

    reporte = entrega.get("reporte")
    if not isinstance(reporte, str) or not reporte.strip():
        return False, "falta el 'reporte': qué casos leíste y qué encontraste"

    datos = entrega.get("datos")
    if not isinstance(datos, list):
        return False, "'datos' tiene que ser una lista de ids"

    marcas = ",".join("?" * len(documentos))
    del_dominio = {fila[0] for fila in db.execute(
        f"SELECT id FROM datos "
        f"WHERE substr(unidad_id, 1, instr(unidad_id, ':') - 1) IN ({marcas})",
        tuple(documento["id"] for documento in documentos))}

    for dato in datos:
        if dato not in del_dominio:
            return False, f"el dato '{dato}' no existe o no es del dominio"
        if dato.rsplit(":", 1)[0] not in casos_leidos:
            return False, f"el dato '{dato}' es de un caso que no leíste"

    if desenlace == "respondida":
        if not isinstance(entrega.get("respuesta"), str) or not entrega["respuesta"].strip():
            return False, "con 'respondida' falta la respuesta"
        if not datos:
            return False, "con 'respondida' hay que citar al menos un dato que la sostenga"
        return True, "aceptada"

    pendientes = [caso["unidad_id"] for caso in casos if caso["unidad_id"] not in casos_leidos]
    if pendientes:
        return False, ("decís que no está en el corpus, pero no leíste todos los casos: "
                       f"faltan {', '.join(pendientes)}")
    return True, "aceptada"
