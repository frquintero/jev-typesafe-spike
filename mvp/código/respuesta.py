"""Lee lo que el modelo contestó: el JSON, con o sin cerca de código.

Copia propia del MVP (la de `niveles/run_niveles.py`, que el MVP usaba prestada). Devuelve
`(parsed, venia_con_cerca, error)`: `parsed` es `None` si no era JSON, y el error explica por qué.
No juzga el contenido.
"""

import json


def extract_json(content):
    """Devuelve (parsed, wrapped, error) a partir del content de la respuesta."""
    text = content.strip()
    wrapped = False
    if text.startswith("```"):
        wrapped = True
        lines = text.split("\n")
        lines = lines[1:]  # quita la linea de apertura ``` o ```json
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text), wrapped, None
    except json.JSONDecodeError as e:
        return None, wrapped, str(e)
