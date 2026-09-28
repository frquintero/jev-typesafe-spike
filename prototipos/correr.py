"""Curva de prototipos: corre la batería con cada configuración de ejemplos.

Uso: python3 prototipos/correr.py <modelo> <rN> [config ...]
Configs por defecto: k0 A AB ABC ABCD ABCDE (letras = ejemplos/<letra>.md).
Crudos: prototipos/cache/<config>-<id>-<modelo>-<rN>.json (idempotente:
si el crudo existe, no se vuelve a llamar; nunca se sobrescribe).
"""
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
from run_niveles import call_model, extract_json  # noqa: E402

CONFIGS = ["k0", "A", "AB", "ABC", "ABCD", "ABCDE"]


def leer(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def foco_de(texto):
    ns = [int(n) for n in re.findall(r"\[(\d+)\]", texto)]
    if len(ns) == 1:
        return f"oración {ns[0]}"
    return "oraciones " + ", ".join(str(n) for n in ns[:-1]) + f" y {ns[-1]}"


def armar_prompt(config, texto):
    base = leer(os.path.join(BASE_DIR, "base.md"))
    letras = "" if config == "k0" else config
    if letras:
        tarea = "Extrae los datos del `foco` según las definiciones, como en los ejemplos."
        bloques = []
        for i, letra in enumerate(letras, start=1):
            cuerpo = leer(os.path.join(BASE_DIR, "ejemplos", f"{letra}.md")).strip()
            bloques.append(f"EJEMPLO {i}\n{cuerpo}\n")
        ejemplos = "\n" + "\n".join(bloques)
    else:
        tarea = "Extrae los datos del `foco` según las definiciones."
        ejemplos = ""
    return (
        base.replace("{{TAREA}}", tarea)
        .replace("{{EJEMPLOS}}", ejemplos)
        .replace("{{DOCUMENTO_NUMERADO}}", texto)
        .replace("{{FOCO}}", foco_de(texto))
    )


def una(config, item, modelo, rep):
    path = os.path.join(CACHE_DIR, f"{config}-{item['id']}-{modelo}-{rep}.json")
    if os.path.exists(path):
        return f"ya existe, salto {path}"
    prompt = armar_prompt(config, item["texto"])
    t0 = time.time()
    request, response = call_model(
        "toulmin", modelo, prompt, conv_id=f"proto-{config}-{rep}"
    )
    segundos = round(time.time() - t0, 1)
    parsed, cerca, error = extract_json(response["choices"][0]["message"]["content"])
    usage = response.get("usage") or {}
    crudo = {
        "config": config, "id": item["id"], "modelo": modelo, "rep": rep,
        "segundos": segundos,
        "reasoning_tokens": (usage.get("completion_tokens_details") or {}).get("reasoning_tokens"),
        "prompt": prompt, "request": request, "response": response,
        "parsed": parsed, "venia_con_cerca": cerca, "error_parseo": error,
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    n = len(parsed.get("datos", [])) if isinstance(parsed, dict) else "null"
    return f"{config} {item['id']}: {n} datos, {segundos} s, rt={crudo['reasoning_tokens']}"


def main():
    modelo, rep = sys.argv[1], sys.argv[2]
    configs = sys.argv[3:] or CONFIGS
    os.makedirs(CACHE_DIR, exist_ok=True)
    bateria = json.loads(leer(os.path.join(BASE_DIR, "bateria.json")))
    for config in configs:
        with ThreadPoolExecutor(max_workers=5) as ex:
            for linea in ex.map(lambda it: una(config, it, modelo, rep), bateria):
                print(linea, flush=True)


if __name__ == "__main__":
    main()
