#!/usr/bin/env python3
"""El paso 2 con un modelo de la familia `responses` de OpenCode Go, **sin escribir en la base**.

Igual que `paso2_seco_v1.py` —misma base en solo lectura, mismas unidades en la forma
`caso:`/`satélites:`, mismo `temp/prompt_DATOS_v1.md`, misma verificación con `forma()`—, pero la
llamada va al endpoint `responses` (Responses API de OpenAI), que devuelve otra forma:
`output[].content[].text` y `usage.input_tokens`, no `choices[0].message`. Acá se traduce a la forma
interna de siempre y el resto del camino no cambia.

Clave: `OPENCODE_API_KEY` (del entorno; nunca se imprime ni se escribe en el crudo).

    bash -ic 'python3 temp/datos-test/paso2_seco_v1_luna.py <doc> <modelo> <esfuerzo> <rN>'
"""
import json
import os
import pathlib
import sqlite3
import sys
import time
import urllib.error
import urllib.request
import uuid

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from base import DB, exigir_sello, hash_texto  # noqa: E402
from extraer_unidades import numerar_oraciones  # noqa: E402
from mensajes import partir  # noqa: E402
from paso2_datos import forma, literales  # noqa: E402
from respuesta import extract_json  # noqa: E402

URL = "https://opencode.ai/zen/go/v1/responses"
# Precios de Go por 1M de tokens, tramo <=272K de contexto (página de Go, 10-10-2026).
PRECIO = {"entrada": 0.10, "salida": 0.50, "cache_lectura": 0.01}

doc, modelo, esfuerzo, rep = sys.argv[1:5]
destino = AQUI / f"{doc}-{modelo}-{esfuerzo}-v1-{rep}.json"
if destino.exists():
    raise SystemExit(f"{destino.name}: ya está, no se vuelve a llamar")

clave = os.environ.get("OPENCODE_API_KEY", "")
if not clave:
    raise SystemExit("falta OPENCODE_API_KEY en el entorno (correr con bash -ic)")

# --- la tanda, igual que en el acto real ---
db = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
db.row_factory = sqlite3.Row
fila = db.execute("SELECT * FROM documentos WHERE id = ?", (doc,)).fetchone()
if fila is None:
    raise SystemExit(f"'{doc}' no está radicado")
unidades = db.execute("SELECT * FROM unidades WHERE documento_id = ? ORDER BY n", (doc,)).fetchall()
texto = exigir_sello(fila)
_, registros = numerar_oraciones(texto)
por_numero = {r["n"]: r["oracion"] for r in registros}
lista = [{"caso": u["subtema"], "satelites": literales(u, por_numero)} for u in unidades]
bloques = ["caso: " + u["caso"] + "\nsatélites:\n"
           + "\n".join(f"[{k}] {o}" for k, o in enumerate(u["satelites"], 1)) for u in lista]
entrada = "\n\n".join(bloques)

ruta_prompt = RAIZ / "temp" / "prompt_DATOS_v1.md"
plantilla = ruta_prompt.read_text(encoding="utf-8")
mensajes = partir(plantilla, ruta_prompt.name, UNIDADES=entrada)
sistema = mensajes[0]["content"]
tarea = mensajes[1]["content"]

# --- la llamada: el `[SISTEMA]` va como `instructions` (invariante, cacheable) ---
cuerpo = {
    "model": modelo,
    "instructions": sistema,
    "input": tarea,
    "reasoning": {"effort": esfuerzo},
    "max_output_tokens": 16000,
}
peticion = urllib.request.Request(
    URL, data=json.dumps(cuerpo).encode(), method="POST",
    headers={"Authorization": "Bearer " + clave,
             "Content-Type": "application/json",
             "User-Agent": "spike-jev/1.0",
             "x-opencode-session": str(uuid.uuid4())})

t0 = time.time()
try:
    with urllib.request.urlopen(peticion, timeout=600) as r:
        respuesta = json.load(r)
except urllib.error.HTTPError as e:
    raise SystemExit(f"HTTP {e.code}: {e.read().decode()[:600]}")
segundos = round(time.time() - t0, 1)

# --- traducción a la forma interna ---
contenido = "".join(
    c.get("text") or ""
    for item in respuesta.get("output") or []
    if item.get("type") == "message"
    for c in item.get("content") or []
    if c.get("type") == "output_text")
razonamiento = "\n".join(
    json.dumps(item, ensure_ascii=False)
    for item in respuesta.get("output") or []
    if item.get("type") == "reasoning")

parsed, _, error = extract_json(contenido)
verificacion = forma(parsed, lista) if parsed is not None else None

uso = respuesta.get("usage") or {}
entrada_tok = uso.get("input_tokens") or 0
cacheados = (uso.get("input_tokens_details") or {}).get("cached_tokens") or 0
salida_tok = uso.get("output_tokens") or 0
costo = round((entrada_tok - cacheados) * PRECIO["entrada"] / 1e6
              + cacheados * PRECIO["cache_lectura"] / 1e6
              + salida_tok * PRECIO["salida"] / 1e6, 6)

destino.write_text(json.dumps({
    "doc": doc, "alias": "luna", "modelo": modelo, "esfuerzo": esfuerzo, "rN": rep,
    "ruta": "opencode-go/responses", "segundos": segundos,
    "prompt": "temp/prompt_DATOS_v1.md", "hash_prompt": hash_texto(plantilla),
    # El hash identifica pero no reconstruye: el texto va en el crudo para que la
    # corrida se interprete sin depender de que el archivo siga existiendo.
    "prompt_texto": plantilla,
    "status": respuesta.get("status"), "incomplete_details": respuesta.get("incomplete_details"),
    "usage": uso, "costo_estimado_usd": costo,
    "reasoning_devuelto": respuesta.get("reasoning"), "text_devuelto": respuesta.get("text"),
    "unidades_enviadas": entrada, "salida": parsed, "verificacion": verificacion,
    "error_parseo": error,
    "peticion": {k: v for k, v in cuerpo.items() if k not in ("instructions", "input")},
    "respuesta_cruda": contenido, "razonamiento": razonamiento,
}, ensure_ascii=False, indent=2), encoding="utf-8")

rt = (uso.get("output_tokens_details") or {}).get("reasoning_tokens")
print(f"{destino.name}: {segundos} s · status {respuesta.get('status')} · "
      f"in {entrada_tok} (cache {cacheados}) · out {salida_tok} (razonamiento {rt}) · "
      f"~US${costo} · verificación: {json.dumps(verificacion, ensure_ascii=False)}")
