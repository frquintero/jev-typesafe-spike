#!/usr/bin/env python3
"""Los dos relojes, y **dónde va cada uno**.

Formato, siempre el mismo: `[día-mes-año: hora]` — por ejemplo `[11-10-2026: 14:35]`.

- **El del radicado** es cuándo entró el documento a Zettel: lo puso la base al radicar
  (`documentos.fecha_radicacion`). Es **invariante por documento**, así que va en el **`system`**,
  junto a las reglas: el prefijo que cachea no cambia de una corrida a otra del mismo documento.
- **El del sistema** es el «ahora» de la corrida: **cambia en cada corrida**, así que va en el
  **`user`**, con el material y **al final**, después del texto —para no romper el prefijo por
  delante—.

Van **etiquetados**, y la etiqueta no es adorno: el del radicado es el que resuelve un deíctico
**del documento** («ayer», «en dos días»); el del sistema, el de la corrida. Sin etiqueta, el modelo
puede resolver «ayer» contra el día equivocado.

Una llamada que no es de un documento —la consulta— lleva **los radicados de los documentos del
dominio**: una línea por documento.
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


def reloj_sistema(momento=None):
    """El «ahora» de la corrida. Va en el `user`, al final, después del material."""
    return f"sistema: {formato(momento or datetime.now())}"


def reloj_sistema_de(marcas):
    """Lo mismo, a partir de las anclas ya congeladas de una consulta (`fecha` y `hora`)."""
    momento = datetime.strptime(f"{marcas['fecha']} {marcas['hora']}", "%Y-%m-%d %H:%M")
    return reloj_sistema(momento)


def reloj_radicado(radicado, etiqueta=None):
    """La fecha de radicación de un documento. Va en el `system`."""
    nombre = f" {etiqueta}" if etiqueta else ""
    return f"radicado{nombre}: {formato(_momento(radicado))}"


def reloj_radicados(documentos):
    """Una línea por documento del dominio: la consulta no va sobre uno solo."""
    return "\n".join(reloj_radicado(fila["fecha_radicacion"], fila["id"]) for fila in documentos)
