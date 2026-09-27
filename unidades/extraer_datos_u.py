"""unidades/extraer_datos_u.py: paso 2, datos de una unidad temática (PLAN.md, ronda DU1).

Uso: python3 unidades/extraer_datos_u.py <doc> <modelo> <prompt> <rN>
  p. ej. python3 unidades/extraer_datos_u.py ut1 grok datos_u1 r1

Solo orquesta: lee la unidad (docs/<doc>.md) y el prompt, sustituye {{TEXTO}},
llama al LLM con call_model de niveles/run_niveles.py y guarda el crudo con el
tiempo total. Idempotente: si el crudo existe, no vuelve a llamar.
"""
import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
from run_niveles import call_model, extract_json  # noqa: E402


def run(doc, modelo, prompt_name, rep):
    cache_dir = os.path.join(BASE_DIR, "cache")
    os.makedirs(cache_dir, exist_ok=True)
    cache_path = os.path.join(cache_dir, f"datos-{doc}-{modelo}-{prompt_name}-{rep}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return
    with open(os.path.join(BASE_DIR, "docs", f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(os.path.join(BASE_DIR, "prompts", f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()

    t0 = time.time()
    body, resp = call_model("toulmin", modelo, prompt.replace("{{TEXTO}}", texto))
    segundos = round(time.time() - t0, 1)
    parsed, venia_con_cerca, error = extract_json(resp["choices"][0]["message"]["content"])

    crudo = {
        "doc": doc, "modelo": modelo, "prompt": prompt_name, "segundos": segundos,
        "request": body, "response": resp,
        "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path} ({segundos} s)")


def main(argv):
    if len(argv) != 5:
        raise SystemExit("uso: python3 unidades/extraer_datos_u.py <doc> <modelo> <prompt> <rN>")
    run(*argv[1:])


if __name__ == "__main__":
    main(sys.argv)
