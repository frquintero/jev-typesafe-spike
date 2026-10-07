#!/usr/bin/env python3
"""Lee una pregunta del archivo del usuario, tal cual.

El archivo tiene una pregunta por línea, numeradas. Devuelve el texto sin el número: la pregunta
viaja al prompt sin tocarla. El archivo es del usuario, y no lleva condiciones ni pistas: las
condiciones van en R.
"""

import re


def leer_pregunta(ruta, cual):
    """Devuelve el texto de la pregunta `cual` (1..n) del archivo."""
    if not ruta.exists():
        raise SystemExit(f"no está el archivo de preguntas '{ruta}'")
    preguntas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        coincidencia = re.match(r"^\d+[.)]\s*(.+)$", linea)
        preguntas.append(coincidencia.group(1).strip() if coincidencia else linea)
    if not 1 <= cual <= len(preguntas):
        raise SystemExit(f"no hay pregunta {cual}: el archivo tiene {len(preguntas)}")
    return preguntas[cual - 1]
