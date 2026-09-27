"""Run the thematic-unit and per-unit data extraction steps over one document.

Usage: python3 unidades/extraer_datos_doc.py <doc> <modelo>
       <prompt_unidades> <prompt_datos> <rN>
"""
import json
import os
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")

sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
sys.path.insert(0, BASE_DIR)
from extraer_unidades import run as run_unidades  # noqa: E402
from run_niveles import call_model, extract_json  # noqa: E402


def ordenar_oraciones(oraciones, texto):
    """Order literal sentences by document position; missing ones stay last."""
    indexed = list(enumerate(oraciones))

    def key(item):
        original_index, oracion = item
        position = texto.find(oracion)
        if position < 0:
            return (1, original_index)
        return (0, position)

    indexed.sort(key=key)
    return [oracion for _, oracion in indexed]


def leer_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def escribir_json(path, value):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(value, f, ensure_ascii=False, indent=2)


def run(doc, modelo, prompt_unidades, prompt_datos, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)

    unidades_path = os.path.join(
        CACHE_DIR, f"unidades-{doc}-{modelo}-{prompt_unidades}-{rep}.json"
    )
    datos_doc_path = os.path.join(
        CACHE_DIR,
        f"doc-{doc}-{modelo}-{prompt_unidades}-{prompt_datos}-{rep}.json",
    )

    run_unidades(doc, modelo, prompt_unidades, rep)
    unidades_crudo = leer_json(unidades_path)
    parsed_unidades = unidades_crudo.get("parsed")
    if parsed_unidades is None:
        raise SystemExit(f"paso 1 sin parsed; detenido ({unidades_path})")
    usa_unidades_reconstruidas = "unidades_reconstruidas" in unidades_crudo
    if usa_unidades_reconstruidas:
        unidades = unidades_crudo["unidades_reconstruidas"]
    else:
        unidades = parsed_unidades.get("unidades", [])

    with open(os.path.join(BASE_DIR, "docs", f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(
        os.path.join(PROMPTS_DIR, f"{prompt_datos}.md"), encoding="utf-8"
    ) as f:
        plantilla_datos = f.read()

    unidades_con_datos = []
    for unidad_n, unidad in enumerate(unidades, start=1):
        if usa_unidades_reconstruidas:
            texto_unidad = " ".join(unidad.get("oraciones", []))
            campos_unidad = {
                "tema": unidad.get("tema"),
                "desde": unidad.get("desde"),
                "hasta": unidad.get("hasta"),
            }
        else:
            texto_unidad = " ".join(ordenar_oraciones(unidad.get("oraciones", []), texto))
            campos_unidad = {
                "nucleo": unidad.get("nucleo"),
                "satelites": unidad.get("satelites"),
            }

        if prompt_unidades == "unidades_v2":
            nombre_crudo = (
                f"datos-{doc}-u{unidad_n}-{modelo}-{prompt_datos}-{rep}.json"
            )
        else:
            nombre_crudo = (
                f"datos-{doc}-{prompt_unidades}-u{unidad_n}-"
                f"{modelo}-{prompt_datos}-{rep}.json"
            )
        datos_path = os.path.join(
            CACHE_DIR, nombre_crudo
        )

        if os.path.exists(datos_path):
            print(f"crudo ya existe, salto ({datos_path})")
        else:
            prompt = plantilla_datos.replace("{{TEXTO}}", texto_unidad)
            t0 = time.time()
            request, response = call_model("toulmin", modelo, prompt)
            segundos = round(time.time() - t0, 1)
            parsed_datos, venia_con_cerca, error_parseo = extract_json(
                response["choices"][0]["message"]["content"]
            )
            crudo_datos = {
                "doc": doc,
                "modelo": modelo,
                "prompt": prompt_datos,
                "segundos": segundos,
                "request": request,
                "response": response,
                "parsed": parsed_datos,
                "venia_con_cerca": venia_con_cerca,
                "error_parseo": error_parseo,
                "unidad_n": unidad_n,
                **campos_unidad,
                "texto_unidad": texto_unidad,
            }
            escribir_json(datos_path, crudo_datos)
            print(f"hecho -> {datos_path} ({segundos} s)")

        crudo_datos = leer_json(datos_path)
        parsed_datos = crudo_datos.get("parsed")
        datos = (
            parsed_datos.get("datos")
            if isinstance(parsed_datos, dict)
            else None
        )
        consolidado_unidad = {"unidad_n": unidad_n}
        consolidado_unidad.update(campos_unidad)
        consolidado_unidad.update(
            {
                "texto_unidad": texto_unidad,
                "datos": datos,
                "error_parseo": crudo_datos.get("error_parseo"),
            }
        )
        unidades_con_datos.append(consolidado_unidad)
        cantidad_datos = len(datos) if isinstance(datos, list) else "null"
        print(f"unidad {unidad_n}: {cantidad_datos} datos, {crudo_datos.get('segundos')} s")

    consolidado = {
        "doc": doc,
        "modelo": modelo,
        "prompt_unidades": prompt_unidades,
        "prompt_datos": prompt_datos,
        "rep": rep,
        "unidades": unidades_con_datos,
    }
    escribir_json(datos_doc_path, consolidado)
    print(f"consolidado -> {datos_doc_path}")


def main(argv):
    if len(argv) != 6:
        raise SystemExit(
            "uso: python3 unidades/extraer_datos_doc.py "
            "<doc> <modelo> <prompt_unidades> <prompt_datos> <rN>"
        )
    run(*argv[1:])


if __name__ == "__main__":
    main(sys.argv)
