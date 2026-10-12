#!/usr/bin/env python3
"""Prueba temporal: ¿la API exige devolver el turno del asistente con su bloque de pensamiento?

Tres llamadas a Haiku 5.5 (effort max) con una herramienta trivial:
  1. el primer turno, para que el modelo pida la herramienta;
  2. el segundo turno devolviendo el asistente SIN el bloque de pensamiento;
  3. el segundo turno devolviéndolo TAL CUAL vino.

No escribe nada: solo imprime estados y textos cortos.
"""

import json
import os
import urllib.error
import urllib.request

URL = "https://api.anthropic.com/v1/messages"
CABECERAS = {"x-api-key": os.environ.get("ANTHROPIC_API_KEY", ""),
             "anthropic-version": "2023-06-01",
             "content-type": "application/json"}
TOOL = {"name": "eco",
        "description": "Devuelve el texto que recibe.",
        "input_schema": {"type": "object",
                         "properties": {"texto": {"type": "string"}},
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


estado, d = post({**BASE, "messages": [USUARIO]})
bloques = d.get("content", [])
print(f"1) primer turno: HTTP {estado} · stop_reason {d.get('stop_reason')}")
print(f"   bloques: {[b.get('type') for b in bloques]}")
usos = [b for b in bloques if b.get("type") == "tool_use"]
print(f"   tool_use: {[b.get('id') for b in usos]}")
resultado = {"role": "user", "content": [{"type": "tool_result",
                                          "tool_use_id": usos[0]["id"], "content": "hola"}]}

sin_pensamiento = [b for b in bloques if b.get("type") != "thinking"]
e2, d2 = post({**BASE, "messages": [USUARIO,
                                    {"role": "assistant", "content": sin_pensamiento},
                                    resultado]})
print(f"\n2) reenviando el asistente SIN el bloque de pensamiento: HTTP {e2}")
print(f"   {json.dumps(d2, ensure_ascii=False)[:300]}")

e3, d3 = post({**BASE, "messages": [USUARIO,
                                    {"role": "assistant", "content": bloques},
                                    resultado]})
print(f"\n3) reenviando el asistente TAL CUAL (con el bloque): HTTP {e3} · "
      f"stop_reason {d3.get('stop_reason')}")
print(f"   texto: {[b.get('text') for b in d3.get('content', []) if b.get('type') == 'text']}")
