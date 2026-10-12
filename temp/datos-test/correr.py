#!/usr/bin/env python3
"""Prueba de DATOS fuera de la base: llama al modelo y guarda su JSON.

**No toca la base.** Toma las unidades de un JSON de la prueba de UT (las que produjo `correr.py`
del scratch), arma el `{{UNIDADES}}` con el mismo criterio que el acto real —`caso` = el subtema,
`contenido` = sus oraciones unidas y sin numerar—, y verifica la forma con la **misma función** que
usa `mvp/código/paso2_datos.py`. Lo único que escribe es su salida, acá al lado.

Uso:

    python3 temp/datos-test/correr.py <doc> <unidades.json> <modelo> <esfuerzo> <rN> [--prompt <ruta>]
    python3 temp/datos-test/correr.py doc9 temp/ut-haiku/doc9-haiku-high-tr1.json haiku high d1 \
        --prompt temp/prompt_DATOS_test.md

Idempotente: si el JSON ya está, no vuelve a llamar.
"""

import hashlib
import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/datos-test → la raíz
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from proveedores import llamar, resolver  # noqa: E402
from respuesta import extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones  # noqa: E402
from paso2_datos import forma  # noqa: E402  (la misma verificación del acto real)


def documento(doc):
    for candidata in (RAIZ / "mvp" / "documentos" / f"{doc}.md", RAIZ / "temp" / f"{doc}.md",
                      AQUI / f"{doc}.md"):
        if candidata.is_file():
            return candidata
    raise SystemExit(f"no encuentro '{doc}.md' ni en mvp/documentos/ ni en temp/")


def unidades_de(ruta_json, doc):
    """Las unidades que produjo la prueba de UT, armadas como las recibe el paso 2."""
    datos = json.loads(pathlib.Path(ruta_json).read_text(encoding="utf-8"))
    if datos.get("doc") != doc:
        raise SystemExit(f"{ruta_json} es de '{datos.get('doc')}', no de '{doc}'")
    _, registros = numerar_oraciones(documento(doc).read_text(encoding="utf-8"))
    por_numero = {r["n"]: r["oracion"] for r in registros}
    lista = []
    for subtema in datos.get("subtemas") or []:
        numeros = [n for n in (subtema.get("oraciones") or []) if n in por_numero]
        lista.append({"caso": subtema.get("subtema") or "",
                      "contenido": " ".join(por_numero[n] for n in numeros)})
    return lista


def correr(doc, ruta_unidades, modelo, esfuerzo, rep, ruta_prompt=None):
    destino = AQUI / f"{doc}-{modelo}-{esfuerzo}-{rep}.json"
    if destino.exists():
        print(f"  {destino.name}: ya está, no se vuelve a llamar")
        return
    archivo_prompt = pathlib.Path(ruta_prompt) if ruta_prompt else RAIZ / "temp" / "prompt_DATOS_test.md"
    if not archivo_prompt.is_absolute():
        archivo_prompt = RAIZ / archivo_prompt
    plantilla = archivo_prompt.read_text(encoding="utf-8")
    if "{{UNIDADES}}" not in plantilla:
        raise SystemExit(f"el prompt '{archivo_prompt.name}' no tiene {{{{UNIDADES}}}}")

    lista = unidades_de(ruta_unidades, doc)
    prompt = plantilla.replace("{{UNIDADES}}", json.dumps(lista, ensure_ascii=False))
    config = resolver(modelo, esfuerzo)

    print(f"  {doc}: una llamada con {len(lista)} unidades · prompt {archivo_prompt.name} · "
          f"{config['id']} (esfuerzo {config.get('esfuerzo')})")
    t0 = time.time()
    cuerpo, respuesta = llamar(modelo, prompt=prompt, esfuerzo=esfuerzo)
    segundos = round(time.time() - t0, 1)
    mensaje = respuesta["choices"][0]["message"]
    contenido = mensaje.get("content") or ""
    parsed, cerca, error = extract_json(contenido)
    verificacion = forma(parsed, lista) if parsed else None

    salida = {
        "doc": doc, "documento": str(documento(doc).relative_to(RAIZ)), "alias": modelo,
        "modelo": config["id"], "esfuerzo": config.get("esfuerzo"), "rN": rep,
        "unidades_origen": str(pathlib.Path(ruta_unidades)), "unidades": lista,
        "segundos": segundos, "prompt": str(archivo_prompt.relative_to(RAIZ)),
        "hash_prompt": hashlib.sha256(plantilla.encode("utf-8")).hexdigest(),
        "finish_reason": respuesta["choices"][0].get("finish_reason"),
        "usage": respuesta.get("usage"), "salida": (parsed or {}).get("unidades"),
        "verificacion": verificacion, "error_parseo": error,
        "peticion": {clave: valor for clave, valor in cuerpo.items() if clave != "messages"},
        "respuesta_cruda": contenido, "razonamiento": mensaje.get("reasoning_content"),
    }
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  {destino.name}: {segundos} s · {salida['finish_reason']} · "
          f"{json.dumps(verificacion, ensure_ascii=False) if verificacion else error}")
    for unidad in salida["salida"] or []:
        print(f"    n={unidad.get('n')} · {len(unidad.get('datos') or [])} datos · "
              f"{unidad.get('caso')}")
        for dato in unidad.get("datos") or []:
            unidad_valor = dato.get("unidad_valor")
            sufijo = f" [{unidad_valor}]" if unidad_valor else ""
            print(f"      · {dato.get('aspecto')} = {dato.get('valor')}{sufijo}")


def main(argumentos):
    ruta_prompt = None
    if "--prompt" in argumentos:
        indice = argumentos.index("--prompt")
        if indice + 1 >= len(argumentos):
            raise SystemExit("--prompt necesita una ruta")
        ruta_prompt = argumentos[indice + 1]
    resto = [a for a in argumentos if not a.startswith("--") and a != ruta_prompt]
    if len(resto) != 5:
        raise SystemExit("uso: python3 temp/datos-test/correr.py <doc> <unidades.json> <modelo> "
                         "<esfuerzo> <rN> [--prompt <ruta>]")
    correr(*resto, ruta_prompt=ruta_prompt)


if __name__ == "__main__":
    main(sys.argv[1:])
