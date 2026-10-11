#!/usr/bin/env python3
"""Los dos relojes que van en el `system` de **todo** prompt: el del sistema y el del radicado.

Formato, siempre el mismo: `[día-mes-año: hora]` — por ejemplo `[11-10-2026: 14:35]`.

- **El del sistema** es el «ahora» de la corrida. Se congela **una sola vez**, al empezar el acto:
  si cambiara entre turnos rompería el prefijo del caché y habría dos «ahora» distintos.
- **El del radicado** es cuándo entró el documento a Zettel: lo puso la base al radicar
  (`documentos.fecha_radicacion`). Es invariante por documento.

Van **juntos y etiquetados**, y la etiqueta no es adorno: el del radicado es el que resuelve un
deíctico **del documento** («ayer», «en dos días»); el del sistema, el de la corrida. Sin etiqueta,
el modelo puede resolver «ayer» contra el día equivocado.

Una llamada que no es de un documento —la consulta, que va sobre un dominio— lleva solo el del
sistema. Lo llena cada acto y va en el hueco `{{RELOJES}}`.
"""

from datetime import datetime

FORMATOS_BASE = ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M")  # como lo guarda SQLite


def formato(momento):
    """`[día-mes-año: hora]` — el formato de los relojes."""
    return (f"[{momento.day:02d}-{momento.month:02d}-{momento.year:04d}: "
            f"{momento.hour:02d}:{momento.minute:02d}]")


def _momento(valor):
    """Acepta un `datetime` o la fecha de radicación tal como la guarda la base."""
    if isinstance(valor, datetime):
        return valor
    texto = str(valor).strip()
    for patron in FORMATOS_BASE:
        try:
            return datetime.strptime(texto, patron)
        except ValueError:
            continue
    raise ValueError(f"no entiendo la fecha de radicado '{valor}': "
                     f"se espera AAAA-MM-DD HH:MM:SS")


def relojes(radicado=None, momento=None):
    """El texto que va en `{{RELOJES}}`: el del sistema y —si hay documento— el del radicado."""
    ahora = momento or datetime.now()
    lineas = [f"sistema: {formato(ahora)}"]
    if radicado:
        lineas.append(f"radicado: {formato(_momento(radicado))}")
    return "\n".join(lineas)


def de_marcas(marcas, radicado=None):
    """Lo mismo, a partir de las anclas ya congeladas de una consulta (`fecha` y `hora`)."""
    momento = datetime.strptime(f"{marcas['fecha']} {marcas['hora']}", "%Y-%m-%d %H:%M")
    return relojes(radicado=radicado, momento=momento)
