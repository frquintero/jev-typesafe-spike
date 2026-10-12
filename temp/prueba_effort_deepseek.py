#!/usr/bin/env python3
"""Prueba temporal: ¿se puede ajustar el esfuerzo de razonamiento de DeepSeek?

Usa `call_model` (el transporte del repo, el único que lee la clave) y solo cambia **en memoria**
el `extra` del alias `v2/deepseek` antes de cada llamada. No toca ningún archivo del repo ni
escribe crudos: solo imprime.

Cada nivel se prueba con el mismo pedido, para ver si cambia el razonamiento (tokens) o si la API
los convierte a todos en `high`, como dice la nota del 28-09.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "niveles"))

import run_niveles  # noqa: E402
from run_niveles import call_model  # noqa: E402

PROMPT = ("Una obra costó 1.200 millones y otra 2.000 millones. ¿Cuánto más costó la segunda "
          "y qué porcentaje representa sobre la primera? Contestá en una sola línea.")

CASOS = [
    ("low", {"thinking": {"type": "enabled"}, "reasoning_effort": "low"}),
    ("medium", {"thinking": {"type": "enabled"}, "reasoning_effort": "medium"}),
    ("high", {"thinking": {"type": "enabled"}, "reasoning_effort": "high"}),
    ("max", {"thinking": {"type": "enabled"}, "reasoning_effort": "max"}),
    ("xhigh (a ver)", {"thinking": {"type": "enabled"}, "reasoning_effort": "xhigh"}),
    ("sin pensamiento", {"thinking": {"type": "disabled"}}),
]

print(f"alias v2/deepseek · id {run_niveles.MODEL_PARAMS['v2']['deepseek']['id']}\n")
for nombre, extra in CASOS:
    run_niveles.MODEL_PARAMS["v2"]["deepseek"]["extra"] = extra
    try:
        t0 = time.time()
        _, resp = call_model("v2", "deepseek", PROMPT)
        segundos = round(time.time() - t0, 1)
        uso = resp.get("usage") or {}
        detalle = uso.get("completion_tokens_details") or {}
        mensaje = resp["choices"][0]["message"]
        print(f"  {nombre:16} {segundos:>5} s · in {uso.get('prompt_tokens')} · "
              f"out {uso.get('completion_tokens')} (razonamiento {detalle.get('reasoning_tokens')}) "
              f"· finish {resp['choices'][0].get('finish_reason')}")
        print(f"                   respuesta: {(mensaje.get('content') or '').strip()[:110]}")
        print(f"                   pensamiento: {len(mensaje.get('reasoning_content') or '')} car.")
    except Exception as error:  # la API rechaza con HTTPError, que trae el texto
        texto = getattr(error, "read", None)
        detalle = texto().decode("utf-8", "replace")[:200] if texto else str(error)[:200]
        print(f"  {nombre:16} -> RECHAZADO: {type(error).__name__}: {detalle}")
    print()
