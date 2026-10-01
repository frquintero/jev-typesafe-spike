"""Ficha v0: una llamada por documento (texto entero, sin subtemas).

Uso: python3 unidades/ficha_doc.py <doc> <modelo> <prompt> <rN>
El código solo numera las oraciones y verifica que cada respaldo/mención
{o, f} esté literal en la oración o. No juzga el contenido.
"""
import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
sys.path.insert(0, BASE_DIR)
from extraer_unidades import numerar_oraciones  # noqa: E402
from run_niveles import call_model, extract_json  # noqa: E402

DOCS_DIR = os.path.join(BASE_DIR, "docs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def fragmentos(nodo, ruta=""):
    """Recorre la ficha y devuelve todos los objetos {o, f} con su ruta."""
    if isinstance(nodo, dict):
        if "o" in nodo and "f" in nodo:
            yield ruta, nodo
        for k, v in nodo.items():
            yield from fragmentos(v, f"{ruta}.{k}")
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from fragmentos(v, f"{ruta}[{i}]")


def verificar(parsed, registros):
    por_n = {r["n"]: r["oracion"] for r in registros}
    total, malos = 0, []
    for ruta, fr in fragmentos(parsed):
        total += 1
        oracion = por_n.get(fr.get("o"))
        f = fr.get("f")
        if oracion is None or not isinstance(f, str) or f not in oracion:
            malos.append({"ruta": ruta, "o": fr.get("o"), "f": f})
    for i, m in enumerate(parsed.get("marcas", []) if isinstance(parsed.get("marcas"), list) else []):
        total += 1
        oracion = por_n.get(m.get("o")) if isinstance(m, dict) else None
        marca = m.get("marca") if isinstance(m, dict) else None
        if oracion is None or not isinstance(marca, str) or marca not in oracion:
            malos.append({"ruta": f".marcas[{i}]", "o": m.get("o") if isinstance(m, dict) else None, "f": marca})
    listas = ["casos", "relaciones", "capas", "determinaciones", "acciones", "marcas", "dudas"]
    return {
        "fragmentos": total,
        "no_literales": malos,
        "listas_faltantes": [l for l in listas if l not in parsed],
        "conteo": {l: len(parsed.get(l, [])) for l in listas if isinstance(parsed.get(l), list)},
    }


def run(doc, modelo, prompt_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"ficha-{doc}-{modelo}-{prompt_name}-{rep}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return
    with open(os.path.join(DOCS_DIR, f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(os.path.join(PROMPTS_DIR, f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()
    texto_numerado, registros = numerar_oraciones(texto)
    prompt_enviado = prompt.replace("{{TEXTO_NUMERADO}}", texto_numerado)

    t0 = time.time()
    body, resp = call_model("toulmin", modelo, prompt_enviado)
    segundos = round(time.time() - t0, 1)
    parsed, venia_con_cerca, error = extract_json(resp["choices"][0]["message"]["content"])
    verificacion = verificar(parsed, registros) if isinstance(parsed, dict) else None

    crudo = {
        "doc": doc, "modelo": modelo, "prompt": prompt_name, "segundos": segundos,
        "texto_numerado": texto_numerado, "oraciones_numeradas": registros,
        "request": body, "response": resp,
        "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
        "verificacion": verificacion,
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path} ({segundos} s)")
    print(json.dumps(verificacion, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("uso: python3 unidades/ficha_doc.py <doc> <modelo> <prompt> <rN>")
    run(*sys.argv[1:])
