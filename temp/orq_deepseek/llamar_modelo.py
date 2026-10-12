#!/usr/bin/env python3
"""COPIA TEMPORAL del ORQ para **medir** la corrida de DeepSeek. NO es el del repo.

Igual que el del repo (`call_model` de `niveles/run_niveles.py`, el único que lee la clave), con
dos cosas agregadas:

- mide los **segundos** de cada llamada y los deja en la respuesta, para que el crudo los guarde
  (el ORQ del repo no los mide: esa es la comparación que falta);
- imprime una línea por llamada, para ver el avance.

Todo lo que escribe cae en `temp/orq_deepseek/out/`.
"""

import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/orq_deepseek → la raíz del repo
sys.path.insert(0, str(RAIZ / "niveles"))
from run_niveles import call_model  # noqa: E402


def llamar_modelo(config, mensajes, herramientas):
    """Devuelve (cuerpo enviado, respuesta ensamblada), con los segundos de la llamada."""
    modelo = config["modelo"]
    t0 = time.time()
    cuerpo, respuesta = call_model(modelo["version"], modelo["alias"], None,
                                   messages=mensajes, tools=herramientas)
    segundos = round(time.time() - t0, 1)
    respuesta["_segundos"] = segundos
    uso = respuesta.get("usage") or {}
    print(f"    [{modelo['alias']}] {segundos} s · {uso.get('prompt_tokens')} in "
          f"({uso.get('prompt_cache_hit_tokens')} caché) / {uso.get('completion_tokens')} out · "
          f"{respuesta['choices'][0].get('finish_reason')}")
    return cuerpo, respuesta
