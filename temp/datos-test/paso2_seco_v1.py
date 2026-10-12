#!/usr/bin/env python3
"""El paso 2 tal como lo hace el acto real, **sin escribir en la base**.

Lee la base en solo lectura (el documento, su sello y sus unidades), arma la tanda y los dos
mensajes con `mvp/prompts/prompt_DATOS.md`, llama al modelo y verifica con `forma()` del acto. La
salida queda en un JSON acá al lado; la base no se toca.

    python3 temp/datos-test/paso2_seco.py <doc> <alias> <esfuerzo> <rN>

Variante: lee el prompt de `temp/prompt_DATOS_v1.md` y manda las unidades con la forma del ejemplo
de ese prompt —`caso:`, `satélites:` y cada oración numerada desde [1] en cada caso—.
"""
import json
import pathlib
import sqlite3
import sys
import time

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from base import DB, exigir_sello, hash_texto  # noqa: E402
from extraer_unidades import numerar_oraciones  # noqa: E402
from mensajes import partir  # noqa: E402
from paso2_datos import forma, literales  # noqa: E402
from proveedores import llamar, resolver  # noqa: E402
from respuesta import extract_json  # noqa: E402

doc, alias, esfuerzo, rep = sys.argv[1:5]
destino = AQUI / f"{doc}-{alias}-{esfuerzo}-v1-{rep}.json"
if destino.exists():
    raise SystemExit(f"{destino.name}: ya está, no se vuelve a llamar")

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
config = resolver(alias, esfuerzo)

t0 = time.time()
cuerpo, respuesta = llamar(alias, mensajes=mensajes, esfuerzo=esfuerzo)
segundos = round(time.time() - t0, 1)
mensaje = respuesta["choices"][0]["message"]
contenido = mensaje.get("content") or ""
parsed, _, error = extract_json(contenido)
verificacion = forma(parsed, lista) if parsed is not None else None

destino.write_text(json.dumps({
    "doc": doc, "alias": alias, "modelo": config["id"], "esfuerzo": config.get("esfuerzo"), "rN": rep,
    "segundos": segundos, "prompt": "temp/prompt_DATOS_v1.md", "hash_prompt": hash_texto(plantilla),
    # El hash identifica pero no reconstruye: el texto va en el crudo para que la
    # corrida se interprete sin depender de que el archivo siga existiendo.
    "prompt_texto": plantilla,
    "finish_reason": respuesta["choices"][0].get("finish_reason"), "usage": respuesta.get("usage"),
    "unidades_enviadas": entrada, "salida": parsed, "verificacion": verificacion, "error_parseo": error,
    "peticion": {k: v for k, v in cuerpo.items() if k not in ("messages", "system")},
    "respuesta_cruda": contenido, "razonamiento": mensaje.get("reasoning_content"),
}, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"{destino.name}: {segundos} s · {respuesta['choices'][0].get('finish_reason')} · "
      f"verificación: {json.dumps(verificacion, ensure_ascii=False)}")
