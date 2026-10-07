#!/usr/bin/env python3
"""Lee un caso: **todos** sus datos. Es el cuerpo de la herramienta `leer_caso`.

Dos comprobaciones antes de devolver nada:

    - que el caso esté en la lista del dominio (el agente no inventa casos),
    - que exista en la base y tenga datos.

Devuelve el caso completo —id, caso y cada dato con su id— porque la lectura es por caso entero:
el agente no filtra por aspecto, decide con lo que hay.
"""


def leer_caso(db, unidad_id, casos):
    """Devuelve (caso, error). El caso es {'unidad_id', 'caso', 'datos': [...]}."""
    if unidad_id not in {caso["unidad_id"] for caso in casos}:
        return None, f"'{unidad_id}' no está en la lista de casos del dominio"
    filas = db.execute(
        "SELECT id, caso, aspecto, valor, unidad_valor FROM datos "
        "WHERE unidad_id = ? ORDER BY id", (unidad_id,)
    ).fetchall()
    if not filas:
        return None, f"'{unidad_id}' no tiene datos en la base"
    return {
        "unidad_id": unidad_id,
        "caso": filas[0]["caso"],
        "datos": [{"id": fila["id"], "aspecto": fila["aspecto"], "valor": fila["valor"],
                   "unidad_valor": fila["unidad_valor"]} for fila in filas],
    }, None
