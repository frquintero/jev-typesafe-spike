"""unidades/extraer_unidades.py: paso 1, unidades temáticas (PLAN.md, ronda U1).

Uso: python3 unidades/extraer_unidades.py <doc> <modelo> <prompt> <rN>
  p. ej. python3 unidades/extraer_unidades.py tec1 grok unidades_v1 r1

Lee el documento y el prompt, sustituye {{TEXTO}}, llama al LLM con call_model
de niveles/run_niveles.py (mismos modelos y parámetros) y guarda el crudo con el
tiempo total. Luego verifica literalidad y cobertura: solo reporta, nunca corrige.
Idempotente: si el crudo existe, no vuelve a llamar.
"""
import json
import os
import re
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
from run_niveles import call_model, extract_json  # noqa: E402

DOCS_DIR = os.path.join(BASE_DIR, "docs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def oraciones(texto):
    """Definición del prompt: de un . ? ! al siguiente; el título (# ...) queda fuera."""
    cuerpo = "\n".join(l for l in texto.splitlines() if not l.startswith("#"))
    return [p.strip() for p in re.findall(r"[^.?!]+[.?!]?", cuerpo) if p.strip()]


def literales(parsed):
    for u in parsed.get("unidades", []):
        yield from u.get("oraciones", [])
        yield from u.get("nucleo", {}).get("menciones", [])
        for s in u.get("satelites", []):
            yield from s.get("menciones", [])
    for a in parsed.get("anaforas", []):
        yield a.get("mencion", "")
        yield a.get("oracion", "")
    for p in parsed.get("procedencias", []):
        yield p.get("fuente", "")
        yield from p.get("oraciones", [])
    yield from parsed.get("oraciones_sin_unidad", [])


def verificar(parsed, texto):
    ors = oraciones(texto)
    asignadas = [o for u in parsed.get("unidades", []) for o in u.get("oraciones", [])]
    return {
        "oraciones_del_texto": len(ors),
        "no_literales": sorted({s for s in literales(parsed) if s and s not in texto}),
        "sin_asignar": [o for o in ors if o not in asignadas],
        "en_mas_de_una_unidad": sorted({o for o in asignadas if asignadas.count(o) > 1}),
        "asignadas_que_no_son_oracion": [o for o in asignadas if o not in ors],
    }


def run(doc, modelo, prompt_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"unidades-{doc}-{modelo}-{prompt_name}-{rep}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return
    with open(os.path.join(DOCS_DIR, f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(os.path.join(PROMPTS_DIR, f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()

    t0 = time.time()
    body, resp = call_model("toulmin", modelo, prompt.replace("{{TEXTO}}", texto))
    segundos = round(time.time() - t0, 1)
    parsed, venia_con_cerca, error = extract_json(resp["choices"][0]["message"]["content"])

    crudo = {
        "doc": doc, "modelo": modelo, "prompt": prompt_name,
        "segundos": segundos,
        "request": body, "response": resp,
        "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
        "verificacion": verificar(parsed, texto) if parsed else None,
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path} ({segundos} s)")
    print(json.dumps(crudo["verificacion"], ensure_ascii=False, indent=2))


def main(argv):
    if len(argv) != 5:
        raise SystemExit("uso: python3 unidades/extraer_unidades.py <doc> <modelo> <prompt> <rN>")
    run(*argv[1:])


if __name__ == "__main__":
    main(sys.argv)
