#!/usr/bin/env python3
"""Prueba temporal del paquete `proveedores` del MVP. No escribe nada: solo imprime.

Una llamada por alias (sin herramientas) y una con herramienta para los dos proveedores que se
distinguen: el compatible con OpenAI y Anthropic (la traducción de `tool_use`/`tool_result`).
"""

import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path("mvp/código").resolve()))
from proveedores import ALIAS, llamar, resolver  # noqa: E402

ECO = {"type": "function",
       "function": {"name": "eco",
                    "description": "Devuelve el texto que recibe.",
                    "parameters": {"type": "object",
                                   "properties": {"texto": {"type": "string"}},
                                   "required": ["texto"]}}}

print("== el registro ==")
for alias in ALIAS:
    config = resolver(alias)
    print(f"  {alias:9} {config['proveedor']:18} {config['id']:22} esfuerzo {config['esfuerzo']}")
print(f"  con override: haiku → {resolver('haiku', 'max')['esfuerzo']}")

print("\n== una llamada por alias, sin herramientas ==")
for alias in ALIAS:
    try:
        cuerpo, respuesta = llamar(alias, prompt="Responde solo con la palabra ok.")
        mensaje = respuesta["choices"][0]["message"]
        uso = respuesta["usage"]
        sin_mensajes = {k: v for k, v in cuerpo.items() if k != "messages"}
        print(f"  {alias:9} {respuesta['_segundos']:>5} s · {respuesta.get('model')} · "
              f"finish {respuesta['choices'][0]['finish_reason']} · content {mensaje.get('content')!r}")
        print(f"            uso: in {uso.get('prompt_tokens')} / out {uso.get('completion_tokens')}"
              f" (pensando {uso.get('thinking_tokens')}) · pensamiento "
              f"{len(mensaje.get('reasoning_content') or '')} car.")
        print(f"            cuerpo: {json.dumps(sin_mensajes, ensure_ascii=False)}")
    except SystemExit as error:
        print(f"  {alias:9} -> {error}")

print("\n== con herramienta (la ida y la vuelta) ==")
for alias in ("deepseek", "haiku"):
    try:
        _, respuesta = llamar(alias,
                              mensajes=[{"role": "user",
                                         "content": "Usá la herramienta eco con el texto «hola»."}],
                              herramientas=[ECO])
        mensaje = respuesta["choices"][0]["message"]
        print(f"  {alias:9} finish {respuesta['choices'][0]['finish_reason']} · "
              f"tool_calls {json.dumps(mensaje.get('tool_calls'), ensure_ascii=False)}")
    except SystemExit as error:
        print(f"  {alias:9} -> {error}")
