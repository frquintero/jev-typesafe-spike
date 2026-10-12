#!/usr/bin/env python3
"""Prueba temporal (no es del repo): las 6 unidades de doc7 en UNA sola llamada.

Lee `temp/prompt_DATOS_tanda.md`, arma la lista de unidades como la arma el paso 2 de a una
(mismo `caso` y mismo `contenido`), hace **una** llamada por `call_model` y mide. Deja el crudo
y la salida en `temp/tanda/`.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "niveles"))
sys.path.insert(0, str(RAIZ / "unidades"))

from run_niveles import call_model, extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, reconstruir_subtemas  # noqa: E402

DOC = "doc7"
PROMPT = RAIZ / "temp" / "prompt_DATOS_tanda.md"
UNIDADES = RAIZ / "mvp" / "corpus" / "extraccion" / DOC / "p1-doc7-v10-deepseek-r1.out"
TEXTO = RAIZ / "mvp" / "pruebas" / f"{DOC}.md"
SALIDA = RAIZ / "temp" / "tanda"


def forma(parsed, esperadas):
    """Verificación de forma: cuántas unidades y datos volvieron. No juzga el contenido."""
    if not isinstance(parsed, dict) or not isinstance(parsed.get("unidades"), list):
        return {"parseo": False, "unidades": 0, "datos": 0, "problemas": ["no hay lista 'unidades'"]}
    unidades = parsed["unidades"]
    problemas = []
    if len(unidades) != esperadas:
        problemas.append(f"devolvió {len(unidades)} y se esperaban {esperadas}")
    for u in unidades:
        if not isinstance(u, dict):
            problemas.append("una unidad no es un objeto")
            continue
        if not isinstance(u.get("n"), int):
            problemas.append("una unidad sin 'n'")
        if not isinstance(u.get("datos"), list):
            problemas.append(f"la unidad n={u.get('n')} no trae 'datos'")
    datos = sum(len(u.get("datos") or []) for u in unidades if isinstance(u, dict))
    return {"parseo": True, "unidades": len(unidades), "datos": datos, "problemas": problemas}


def main():
    unidades = json.loads(UNIDADES.read_text(encoding="utf-8"))["subtemas"]
    texto = TEXTO.read_text(encoding="utf-8")
    _, oraciones_numeradas = numerar_oraciones(texto)
    reconstruidas = reconstruir_subtemas({"subtemas": unidades}, oraciones_numeradas)
    lista = [{"caso": u["subtema"], "contenido": " ".join(u["oraciones"])} for u in reconstruidas]

    plantilla = PROMPT.read_text(encoding="utf-8")
    if "{{UNIDADES}}" not in plantilla:
        raise SystemExit("el prompt temporal no tiene {{UNIDADES}}")
    prompt = plantilla.replace("{{UNIDADES}}", json.dumps(lista, ensure_ascii=False))

    t0 = time.time()
    body, resp = call_model("v2", "deepseek", prompt)
    segundos = round(time.time() - t0, 1)
    contenido = resp["choices"][0]["message"]["content"] or ""
    parsed, venia_con_cerca, error = extract_json(contenido)
    uso = resp.get("usage") or {}
    v = forma(parsed, len(lista))

    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "salida.json").write_text(json.dumps(parsed, ensure_ascii=False, indent=2),
                                        encoding="utf-8")
    (SALIDA / "crudo.json").write_text(json.dumps({
        "doc": DOC, "segundos": segundos, "unidades_enviadas": lista,
        "request": body, "response": resp, "parsed": parsed,
        "venia_con_cerca": venia_con_cerca, "error_parseo": error, "forma": v,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"una sola llamada · {len(lista)} unidades · {segundos} s")
    print(f"tokens: prompt {uso.get('prompt_tokens')} "
          f"(hit {uso.get('prompt_cache_hit_tokens')}, miss {uso.get('prompt_cache_miss_tokens')}) "
          f"· completion {uso.get('completion_tokens')}")
    print("forma:", json.dumps(v, ensure_ascii=False))
    for u in (parsed or {}).get("unidades", []):
        print(f"  n={u.get('n')}: {len(u.get('datos') or [])} datos · {str(u.get('caso'))[:70]}")
    print(f"-> {SALIDA.relative_to(RAIZ)}/salida.json")


if __name__ == "__main__":
    main()
