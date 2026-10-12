#!/usr/bin/env python3
"""Obtiene los datos de un caso: **todos**. Es el cuerpo de la herramienta
`obtener_datos_del_caso`.

Dos comprobaciones mecánicas antes de devolver nada —no son juicio: sin esto no hay nada que
devolver—:

    - que el caso esté en la lista del dominio (el agente no puede pedir un caso que no exista),
    - que exista en la base y tenga datos **en la tanda que el catálogo fijó**.

Los datos se leen de `(unidad, tanda)`, no de «los datos de la unidad»: con dos tandas de DATOS
sobre la misma UT, esa lectura mezclaría las dos, y la consulta tiene que poder mostrar después
**exactamente** los datos que leyó.

Devuelve el caso completo —id, caso y cada dato con su id—: la lectura es por caso entero, sin
filtrar por aspecto.
"""


def obtener_datos_del_caso(db, unidad_id, casos):
    """Devuelve (caso, error). El caso es {'unidad_id', 'caso', 'datos': [...]}."""
    ofrecidos = {caso["unidad_id"]: caso for caso in casos}
    if unidad_id not in ofrecidos:
        return None, f"'{unidad_id}' no está en la lista de casos del dominio"
    unidad = db.execute("SELECT subtema FROM unidades WHERE id = ?", (unidad_id,)).fetchone()
    if unidad is None:
        return None, f"'{unidad_id}' no está en la base"
    tanda = ofrecidos[unidad_id].get("datos_token")
    if tanda is None:
        return None, f"'{unidad_id}' no tiene datos en la base"
    filas = db.execute(
        "SELECT id, aspecto, valor, unidad_valor FROM datos "
        "WHERE unidad_id = ? AND corrida_id = ? ORDER BY id", (unidad_id, tanda)
    ).fetchall()
    if not filas:
        return None, f"'{unidad_id}' no tiene datos en la base"
    return {
        "unidad_id": unidad_id,
        "caso": unidad["subtema"],
        "datos": [{"id": fila["id"], "aspecto": fila["aspecto"], "valor": fila["valor"],
                   "unidad_valor": fila["unidad_valor"]} for fila in filas],
    }, None
