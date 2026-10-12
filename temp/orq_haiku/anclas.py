#!/usr/bin/env python3
"""Congela el día y la hora del sistema al abrir la consulta.

Se toman **una sola vez**: si cambiaran entre turnos, romperían el prefijo del caché y la
consulta razonaría con dos «ahora» distintos. El ancla no es dato del documento: es el marco
temporal de esta consulta, y así lo dice el prompt.
"""

from datetime import datetime

MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]


def anclas(momento=None):
    """Devuelve las anclas de la consulta: fecha, hora y el texto que va al prompt."""
    ahora = momento or datetime.now()
    fecha = f"{ahora.year:04d}-{ahora.month:02d}-{ahora.day:02d}"
    hora = f"{ahora.hour:02d}:{ahora.minute:02d}"
    return {
        "fecha": fecha,
        "hora": hora,
        "texto": f"{ahora.day} de {MESES[ahora.month - 1]} de {ahora.year}, {hora}",
    }
