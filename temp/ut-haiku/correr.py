#!/usr/bin/env python3
"""Prueba de particiones (UT) fuera del registro: llama al modelo y guarda el JSON.

**No toca la base ni el código del repo.** Reusa lo mismo que el acto real:
`extraer_unidades` (la numeración y la verificación) y `proveedores.llamar` (el transporte), y lee
el documento radicado y el prompt tal como están. Lo único que escribe es su salida, acá al lado.

Uso:

    python3 temp/ut-haiku/correr.py <doc> <modelo> <esfuerzo> <rN> [--prompt <ruta>]
    python3 temp/ut-haiku/correr.py doc8 haiku high r1
    python3 temp/ut-haiku/correr.py doc8 haiku high tr1 --prompt temp/prompt_UT_test.md

`--prompt` apunta a otro archivo de prompt (por defecto, `mvp/prompts/prompt_UT.md`). Con el de
`temp/` el ejemplo es el propio documento, así que el texto viaja dos veces: una en el ejemplo y
otra como tarea.

Idempotente: si el JSON ya está, no vuelve a llamar.
"""

import hashlib
import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/ut-haiku → la raíz
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from proveedores import llamar, resolver  # noqa: E402
from respuesta import extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, verificar_subtemas  # noqa: E402

DOCUMENTOS = RAIZ / "mvp" / "documentos"
PROMPTS = RAIZ / "mvp" / "prompts"


def correr(doc, modelo, esfuerzo, rep, ruta_prompt=None):
    destino = AQUI / f"{doc}-{modelo}-{esfuerzo}-{rep}.json"
    if destino.exists():
        print(f"  {destino.name}: ya está, no se vuelve a llamar")
        return
    archivo_prompt = pathlib.Path(ruta_prompt) if ruta_prompt else PROMPTS / "prompt_UT.md"
    if not archivo_prompt.is_absolute():
        archivo_prompt = RAIZ / archivo_prompt
    plantilla = archivo_prompt.read_text(encoding="utf-8")

    # El acto real lee del registro (`mvp/documentos/`); el scratch también acepta los documentos
    # de prueba que viven en `temp/`.
    for candidata in (DOCUMENTOS / f"{doc}.md", RAIZ / "temp" / f"{doc}.md", AQUI / f"{doc}.md"):
        if candidata.is_file():
            ruta_documento = candidata
            break
    else:
        raise SystemExit(f"no encuentro el documento '{doc}.md' ni en mvp/documentos/ ni en temp/")
    texto = ruta_documento.read_text(encoding="utf-8")
    numerado, registros = numerar_oraciones(texto)
    prompt = plantilla.replace("{{TEXTO_NUMERADO}}", numerado)
    config = resolver(modelo, esfuerzo)

    t0 = time.time()
    cuerpo, respuesta = llamar(modelo, prompt=prompt, esfuerzo=esfuerzo)
    segundos = round(time.time() - t0, 1)
    mensaje = respuesta["choices"][0]["message"]
    contenido = mensaje.get("content") or ""
    parsed, cerca, error = extract_json(contenido)
    verificacion = verificar_subtemas(parsed, registros) if parsed else None

    salida = {
        "doc": doc, "documento": str(ruta_documento.relative_to(RAIZ)), "alias": modelo, "modelo": config["id"], "esfuerzo": config.get("esfuerzo"),
        "rN": rep, "segundos": segundos,
        "prompt": str(archivo_prompt.relative_to(RAIZ)),
        "hash_prompt": hashlib.sha256(plantilla.encode("utf-8")).hexdigest(),
        "finish_reason": respuesta["choices"][0].get("finish_reason"),
        "usage": respuesta.get("usage"),
        "subtemas": (parsed or {}).get("subtemas"),
        "verificacion": verificacion, "error_parseo": error,
        "peticion": {clave: valor for clave, valor in cuerpo.items() if clave != "messages"},
        "respuesta_cruda": contenido, "razonamiento": mensaje.get("reasoning_content"),
        "oraciones": registros,
    }
    destino.write_text(json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")

    subtemas = salida["subtemas"] or []
    print(f"  {destino.name}: {len(subtemas)} unidades · {segundos} s · "
          f"{salida['finish_reason']} · prompt {salida['prompt']}")
    print(f"    verificación: {json.dumps(verificacion, ensure_ascii=False)}"
          if verificacion else f"    no se pudo leer: {error}")
    for n, subtema in enumerate(subtemas, 1):
        print(f"    U{n}: {subtema.get('oraciones')} {subtema.get('subtema')}")


def main(argumentos):
    opciones = [a for a in argumentos if a.startswith("--")]
    resto = [a for a in argumentos if not a.startswith("--")]
    ruta_prompt = None
    if "--prompt" in opciones:
        indice = argumentos.index("--prompt")
        if indice + 1 >= len(argumentos):
            raise SystemExit("--prompt necesita una ruta")
        ruta_prompt = argumentos[indice + 1]
        resto = [a for a in resto if a != ruta_prompt]
    if len(resto) != 4:
        raise SystemExit("uso: python3 temp/ut-haiku/correr.py <doc> <modelo> <esfuerzo> <rN> "
                         "[--prompt <ruta>]")
    correr(*resto, ruta_prompt=ruta_prompt)


if __name__ == "__main__":
    main(sys.argv[1:])
