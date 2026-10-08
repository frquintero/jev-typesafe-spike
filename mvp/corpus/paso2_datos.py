#!/usr/bin/env python3
"""Paso 2 del corpus: los datos de cada unidad temática, por la API (`call_model`).

Uso:
    python3 mvp/corpus/paso2_datos.py <doc> <unidades> <modelo> <rN>
    python3 mvp/corpus/paso2_datos.py doc7 p1-doc7-v10-deepseek-r1.out deepseek r1

`<unidades>` es el archivo de paso 1 que se usa: una ruta, o el nombre suelto del archivo
dentro de `mvp/corpus/extraccion/<doc>/` (`p1-doc7-v10-deepseek-r1.out`). `<rN>` es la réplica
con su `r` (`r1`, `r2`…), igual que en el paso 1.

Hace, por cada unidad, lo que para `doc4` y `doc6` se hizo a mano delegando a Muse:

1. arma la unidad que recibe el paso 2 —`caso` = el `subtema` que devolvió el paso 1,
   `contenido` = sus oraciones unidas en un párrafo y sin numeración—;
2. sustituye `{{UNIDAD}}` en `mvp/prompts/prompt_DATOS.md`;
3. llama al modelo por `call_model` (`niveles/run_niveles.py`): **una llamada por unidad, sin
   agente de por medio**;
4. lee la respuesta con `extract_json` y verifica la **forma** (no el contenido);
5. escribe la salida y el crudo.

Escribe, en `mvp/corpus/extraccion/<doc>/`:

    p2-<doc>-u<n>-<rN>.out    el JSON de datos de esa unidad (lo que lee el cargador)
    p2-<doc>-u<n>-<rN>.json   el crudo: unidad enviada, petición, respuesta, segundos y forma

Idempotente **por unidad**: si el `.out` de esa unidad ya existe, no vuelve a llamar; así una
corrida cortada se retoma sin repetir lo hecho.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(RAIZ / "niveles"))
sys.path.insert(0, str(RAIZ / "unidades"))

from run_niveles import call_model, extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, reconstruir_subtemas  # noqa: E402

PRUEBAS = RAIZ / "mvp" / "pruebas"
PROMPTS = RAIZ / "mvp" / "prompts"
EXTRACCION = RAIZ / "mvp" / "corpus" / "extraccion"
VERSION = "v2"  # el mismo esquema de parámetros que usa el ORQ


def resolver_unidades(doc, argumento):
    """El archivo de paso 1: la ruta tal cual, o el nombre dentro de la carpeta del doc."""
    candidato = pathlib.Path(argumento)
    if not candidato.is_absolute():
        candidato = RAIZ / candidato
    if candidato.exists():
        return candidato
    dentro = EXTRACCION / doc / argumento
    if dentro.exists():
        return dentro
    raise SystemExit(f"no encuentro el archivo de unidades '{argumento}' para {doc}")


def forma(parsed):
    """Verifica la forma de la salida del paso 2. No juzga el contenido."""
    if not isinstance(parsed, dict):
        return {"parseo": False, "datos": 0, "problemas": ["no hay objeto JSON"]}
    problemas = []
    if not isinstance(parsed.get("caso"), str) or not parsed["caso"].strip():
        problemas.append("falta 'caso'")
    datos = parsed.get("datos")
    if not isinstance(datos, list):
        problemas.append("'datos' no es una lista")
        datos = []
    for i, dato in enumerate(datos, 1):
        if not isinstance(dato, dict):
            problemas.append(f"datos[{i}] no es un objeto")
            continue
        if not isinstance(dato.get("aspecto"), str) or not dato["aspecto"].strip():
            problemas.append(f"datos[{i}] sin 'aspecto'")
        if not isinstance(dato.get("valor"), (str, int, float)):
            problemas.append(f"datos[{i}] sin 'valor'")
        if dato.get("unidad_valor") is not None and not isinstance(dato["unidad_valor"], str):
            problemas.append(f"datos[{i}] 'unidad_valor' no es texto ni null")
    return {"parseo": True, "datos": len(datos), "problemas": problemas}


def run(doc, unidades_arg, modelo, rep):
    carpeta = EXTRACCION / doc
    ruta_unidades = resolver_unidades(doc, unidades_arg)
    unidades = json.loads(ruta_unidades.read_text(encoding="utf-8"))["subtemas"]
    texto = (PRUEBAS / f"{doc}.md").read_text(encoding="utf-8")
    _, oraciones_numeradas = numerar_oraciones(texto)
    reconstruidas = reconstruir_subtemas({"subtemas": unidades}, oraciones_numeradas)

    ruta_prompt = PROMPTS / "prompt_DATOS.md"
    prompt = ruta_prompt.read_text(encoding="utf-8")
    if "{{UNIDAD}}" not in prompt:
        raise SystemExit(f"el prompt '{ruta_prompt.name}' no tiene {{{{UNIDAD}}}}")

    print(f"{doc}: {len(unidades)} unidades desde {ruta_unidades.name} · modelo {modelo}")
    total = 0.0
    llamadas = 0
    for n, unidad in enumerate(reconstruidas, 1):
        if not unidad["oraciones"]:
            print(f"  U{n}: sin oraciones reconstruidas, salto")
            continue
        salida = carpeta / f"p2-{doc}-u{n}-{rep}.out"
        if salida.exists():
            print(f"  U{n}: crudo ya existe, salto")
            continue

        entrada = {"caso": unidad["subtema"], "contenido": " ".join(unidad["oraciones"])}
        prompt_enviado = prompt.replace("{{UNIDAD}}", json.dumps(entrada, ensure_ascii=False))

        t0 = time.time()
        body, resp = call_model(VERSION, modelo, prompt_enviado)
        segundos = round(time.time() - t0, 1)
        total += segundos
        llamadas += 1
        parsed, venia_con_cerca, error = extract_json(resp["choices"][0]["message"]["content"])

        carpeta.mkdir(parents=True, exist_ok=True)
        if parsed is not None:
            salida.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        (carpeta / f"p2-{doc}-u{n}-{rep}.json").write_text(json.dumps({
            "doc": doc, "unidad_n": n, "prompt": "prompt_DATOS", "modelo": modelo,
            "version": VERSION, "rN": rep, "segundos": segundos,
            "unidad_enviada": entrada, "request": body, "response": resp,
            "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
            "forma": forma(parsed),
        }, ensure_ascii=False, indent=2), encoding="utf-8")

        if parsed is None:
            print(f"  U{n}: NO se pudo parsear ({error}) · {segundos} s")
            continue
        v = forma(parsed)
        aviso = f" · problemas: {v['problemas']}" if v["problemas"] else ""
        print(f"  U{n}: {v['datos']} datos · {segundos} s{aviso}")

    if llamadas:
        print(f"  total: {total:.1f} s en {llamadas} llamadas · media {total / llamadas:.1f} s")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("uso: python3 mvp/corpus/paso2_datos.py <doc> <unidades> <modelo> <rN>")
    run(*sys.argv[1:])
