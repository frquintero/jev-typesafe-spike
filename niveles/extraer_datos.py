"""niveles/extraer_datos.py: smoke test del objeto «dato».

Uso: python3 niveles/extraer_datos.py <doc> <modelo> <prompt> <rN>
  p. ej. python3 niveles/extraer_datos.py doc2 deepseek datos_v1 r1

Orquestador, sin verificaciones (PLAN.md, Ronda D1): lee el documento y el
prompt, sustituye {{TEXTO}}, llama al LLM con los mismos parametros de modelo
de las rondas Toulmin y guarda el crudo completo. Idempotente.
"""
import json
import os
import sys

from run_niveles import call_model, extract_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def run(doc, modelo, prompt_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"datos-{doc}-{modelo}-{prompt_name}-{rep}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return

    with open(os.path.join(DOCS_DIR, f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(os.path.join(PROMPTS_DIR, f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()
    contenido = prompt.replace("{{TEXTO}}", texto)

    body, resp = call_model("toulmin", modelo, contenido)
    content = resp["choices"][0]["message"]["content"]
    parsed, venia_con_cerca, error = extract_json(content)

    crudo = {
        "doc": doc,
        "modelo": modelo,
        "prompt": prompt_name,
        "request": body,
        "response": resp,
        "parsed": parsed,
        "venia_con_cerca": venia_con_cerca,
        "error_parseo": error,
    }
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path}")


def main(argv):
    if len(argv) != 5:
        raise SystemExit("uso: python3 niveles/extraer_datos.py <doc> <modelo> <prompt> <rN>")
    _, doc, modelo, prompt_name, rep = argv
    run(doc, modelo, prompt_name, rep)


if __name__ == "__main__":
    main(sys.argv)
