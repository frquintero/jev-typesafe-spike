#!/usr/bin/env python3
"""¿Qué exactamente rechaza la API con los bloques de pensamiento?

Turno 1: pedir la herramienta. Turno 2, cuatro variantes del turno del asistente:
  a) sin el bloque de pensamiento        (ya visto: 200)
  b) con el bloque, pero con otra firma
  c) con el bloque, pero con el texto del pensamiento vaciado
  d) con el bloque tal cual vino

Solo imprime estados y el mensaje de error, recortado. No escribe archivos.
"""

import copy
import json
import os
import urllib.error
import urllib.request

URL = "https://api.anthropic.com/v1/messages"
CABECERAS = {"x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
             "anthropic-version": "2023-06-01", "content-type": "application/json"}
TOOL = {"name": "eco", "description": "Devuelve el texto que recibe.",
        "input_schema": {"type": "object", "properties": {"texto": {"type": "string"}},
                         "required": ["texto"]}}
BASE = {"model": "claude-haiku-5-5", "max_tokens": 2048,
        "output_config": {"effort": "max"}, "tools": [TOOL]}
USUARIO = {"role": "user", "content": "Usá la herramienta eco con el texto «hola»."}


def post(cuerpo):
    req = urllib.request.Request(URL, data=json.dumps(cuerpo).encode(),
                                 headers=CABECERAS, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read().decode("utf-8", "replace"))


_, d = post({**BASE, "messages": [USUARIO]})
bloques = d.get("content", [])
pensamiento = next((b for b in bloques if b.get("type") == "thinking"), None)
uso = next(b for b in bloques if b.get("type") == "tool_use")
resultado = {"role": "user", "content": [{"type": "tool_result",
                                          "tool_use_id": uso["id"], "content": "hola"}]}
print(f"bloque de pensamiento recibido: claves {sorted(pensamiento.keys())} · "
      f"firma {str(pensamiento.get('signature'))[:24]}… · "
      f"texto de {len(pensamiento.get('thinking') or '')} caracteres")

variantes = {}
a = cross = copy.deepcopy(pensamiento); cross["signature"] = "firmaInventadaAAA"
variantes["a) sin el bloque"] = [b for b in bloques if b.get("type") != "thinking"]
variantes["b) con firma cambiada"] = [cross] + [b for b in bloques if b.get("type") != "thinking"]
vaciado = copy.deepcopy(pensamiento); vaciado["thinking"] = ""
variantes["c) con el texto vaciado"] = [vaciado] + [b for b in bloques
                                                    if b.get("type") != "thinking"]
variantes["d) tal cual vino"] = bloques

for nombre, contenido in variantes.items():
    estado, respuesta = post({**BASE, "messages": [USUARIO,
                                                   {"role": "assistant", "content": contenido},
                                                   resultado]})
    detalle = ""
    if estado == 200:
        detalle = f"stop_reason {respuesta.get('stop_reason')}"
    else:
        err = respuesta.get("error") or {}
        detalle = f"{err.get('type')}: {str(err.get('message'))[:180]}"
    print(f"  {nombre:26} -> HTTP {estado} · {detalle}")
