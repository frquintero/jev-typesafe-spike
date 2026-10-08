#!/usr/bin/env python3
"""Paso 1 del corpus: texto → unidades temáticas, con el prompt de trabajo.

Uso:
    python3 mvp/corpus/paso1_unidades.py <doc> <prompt> <modelo> <rN>
    python3 mvp/corpus/paso1_unidades.py doc7 v10 deepseek r1

Hace lo que para `doc4` y `doc6` se hizo a mano delegando a Muse (pegar el prompt con el
texto numerado en un mensaje): lee el documento de `mvp/pruebas/<doc>.md` y el prompt de
`mvp/pruebas/prompt_<prompt>.md`, numera las oraciones y sustituye `{{TEXTO_NUMERADO}}`,
llama al modelo por `call_model` y verifica cobertura y solapes. La numeración y la
verificación son las de `unidades/extraer_unidades.py`: un solo lugar para las dos.

Escribe, en `mvp/corpus/extraccion/<doc>/`:

    p1-<doc>-<prompt>-<modelo>-<rN>.out    el JSON de unidades (lo que lee el cargador)
    p1-<doc>-<prompt>-<modelo>-<rN>.json   el crudo: petición, respuesta, segundos y verificación

Idempotente: si el `.out` existe, no vuelve a llamar.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "niveles"))
sys.path.insert(0, str(RAIZ / "unidades"))

from run_niveles import call_model, extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, verificar_subtemas  # noqa: E402

PRUEBAS = RAIZ / "mvp" / "pruebas"
EXTRACCION = RAIZ / "mvp" / "corpus" / "extraccion"
VERSION = "v2"  # el mismo esquema de parámetros que usa el ORQ


def run(doc, prompt_name, modelo, rep):
    carpeta = EXTRACCION / doc
    salida = carpeta / f"p1-{doc}-{prompt_name}-{modelo}-{rep}.out"
    if salida.exists():
        print(f"crudo ya existe, salto ({salida.relative_to(RAIZ)})")
        return

    ruta_prompt = PRUEBAS / f"prompt_{prompt_name}.md"
    texto = (PRUEBAS / f"{doc}.md").read_text(encoding="utf-8")
    prompt = ruta_prompt.read_text(encoding="utf-8")
    if "{{TEXTO_NUMERADO}}" not in prompt:
        raise SystemExit(f"el prompt '{ruta_prompt.name}' no tiene {{{{TEXTO_NUMERADO}}}}")

    texto_numerado, oraciones_numeradas = numerar_oraciones(texto)
    prompt_enviado = prompt.replace("{{TEXTO_NUMERADO}}", texto_numerado)

    t0 = time.time()
    body, resp = call_model(VERSION, modelo, prompt_enviado)
    segundos = round(time.time() - t0, 1)
    contenido = resp["choices"][0]["message"]["content"] or ""
    parsed, venia_con_cerca, error = extract_json(contenido)
    verificacion = verificar_subtemas(parsed, oraciones_numeradas) if parsed else None

    carpeta.mkdir(parents=True, exist_ok=True)
    if parsed is not None:
        salida.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
    crudo = {
        "doc": doc, "prompt": prompt_name, "modelo": modelo, "version": VERSION, "rN": rep,
        "segundos": segundos,
        "texto_numerado": texto_numerado, "oraciones_numeradas": oraciones_numeradas,
        "request": body, "response": resp,
        "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
        "verificacion": verificacion,
    }
    (carpeta / f"p1-{doc}-{prompt_name}-{modelo}-{rep}.json").write_text(
        json.dumps(crudo, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"{doc}: {len(oraciones_numeradas)} oraciones · "
          f"{len(parsed.get('subtemas', [])) if parsed else 0} unidades · {segundos} s")
    print(f"  verificación: {json.dumps(verificacion, ensure_ascii=False)}")
    if parsed is None:
        print(f"  NO se pudo parsear el JSON (error: {error}); el .out no se escribió")
        return
    print(f"  -> {salida.relative_to(RAIZ)}")
    for i, subtema in enumerate(parsed.get("subtemas", []), 1):
        print(f"  U{i}: [{', '.join(str(n) for n in subtema.get('oraciones', []))}] "
              f"{subtema.get('subtema')}")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("uso: python3 mvp/corpus/paso1_unidades.py <doc> <prompt> <modelo> <rN>")
    run(*sys.argv[1:])
