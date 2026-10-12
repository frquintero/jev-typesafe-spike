#!/usr/bin/env python3
"""El acto: abrir, cerrar y dejar la fila.

Un **acto** es una ejecución de una etapa (el volcado, UT, DATOS, la consulta). Acá vive lo que
todos tienen igual:

- **`abrir()`** da el **token** —el del contador de su base— y el momento de arranque. No escribe
  nada: el acto todavía no pasó.
- **`cerrar()`** escribe la **fila del acto** y, si salió bien, **lo que produjo**, en una sola
  transacción: las dos cosas o ninguna. Un fallo controlado también deja su fila, con el motivo.

Una corrida **no se toca**: cada intento es su fila, y los productos apuntan a la corrida que
los hizo. Rehacer es correr otra vez, no borrar la anterior.

**Qué se promete:** los éxitos y los fallos controlados. Una muerte abrupta del proceso antes de
cerrar no deja constancia, y eso está declarado: cubrirlo pediría una fila `en_curso` al abrir y
cerrarla al final, que es un `UPDATE` que contradice «un acto, una fila».
"""

from datetime import datetime

from base import registrar_corrida
from esquema import PREFIJO_CORPUS, token_siguiente


def abrir(db, paso, prefijo=PREFIJO_CORPUS, **campos):
    """El acto empieza: devuelve la corrida con su token y su arranque. No escribe."""
    corrida = dict(campos)
    corrida["id"] = token_siguiente(db, prefijo)
    corrida["paso"] = paso
    corrida["iniciado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return corrida


def cerrar(db, corrida, estado, motivo=None, escribir=None):
    """Cierra el acto: la fila y —si salió bien— lo que produjo, en una transacción.

    `escribir` es una función `escribir(db, corrida_id)` que inserta los productos del acto. Si
    algo falla adentro, la transacción vuelve sola; y el intento **no se pierde**: se registra
    igual como fallido, con el error como motivo, y la excepción sigue su curso.
    """
    campos = dict(corrida)
    campos["estado"] = estado
    campos["motivo"] = motivo
    campos["terminado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with db:
            registrar_corrida(db, **campos)
            if estado == "exitoso" and escribir is not None:
                escribir(db, corrida["id"])
    except Exception as error:  # noqa: BLE001 (se re-lanza: solo se deja la constancia)
        try:
            registrar_corrida(db, **{**campos, "estado": "fallido",
                                     "motivo": f"error inesperado: {type(error).__name__}: "
                                               f"{error}"})
            db.commit()
        except Exception:  # noqa: BLE001 (si tampoco se puede dejar la cédula, se sigue)
            db.rollback()
        raise
    return corrida["id"]
