#!/usr/bin/env python3
"""Una pregunta suelta a GLM por el transporte del MVP; guarda el crudo al lado.

    python3 temp/glm_pregunta.py <esfuerzo> <rN> "<pregunta>"
"""
import json
import pathlib
import sys

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "mvp" / "código"))
from proveedores import llamar  # noqa: E402

esfuerzo, rep, pregunta = sys.argv[1], sys.argv[2], sys.argv[3]
destino = AQUI / f"glm_pregunta-{esfuerzo}-{rep}.json"
cuerpo, respuesta = llamar("glm", prompt=pregunta, esfuerzo=esfuerzo)
destino.write_text(json.dumps({"peticion": cuerpo, "respuesta": respuesta}, ensure_ascii=False, indent=2),
                   encoding="utf-8")
m = respuesta["choices"][0]["message"]
print("petición:", {k: v for k, v in cuerpo.items() if k != "messages"})
print("usage:", json.dumps(respuesta.get("usage"), ensure_ascii=False))
print("segundos:", respuesta.get("_segundos"))
print("reasoning_content:", len(m.get("reasoning_content") or ""), "caracteres")
print((m.get("reasoning_content") or "")[:600])
print("--- content:", (m.get("content") or "")[:300])
