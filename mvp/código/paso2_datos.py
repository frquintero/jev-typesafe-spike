#!/usr/bin/env python3
"""Paso 2 del corpus: los datos de las unidades temáticas, en UNA llamada por documento.

Uso:
    python3 mvp/código/paso2_datos.py <doc> <unidades> <modelo> <rN>
    python3 mvp/código/paso2_datos.py doc7 p1-doc7-v10-deepseek-r1.out deepseek r1

`<unidades>` es el archivo de paso 1 que se usa: una ruta, o el nombre suelto del archivo
dentro de `mvp/temp/extraccion/<doc>/` (`p1-doc7-v10-deepseek-r1.out`). `<rN>` es la réplica
con su `r` (`r1`, `r2`…), igual que en el paso 1.

El paso 2 va **en tanda**: las unidades del documento se mandan en **una sola llamada**. Medido
el 08-10 sobre las seis unidades de `doc7`: **24,4 s y 8.759 tokens** en una llamada, contra
**52,2 s y 18.481 tokens** en seis llamadas, con los mismos datos salvo granularidad (una vez
juntó en un valor lo que de a una salieron dos). Antes el corredor iba de a una unidad.

1. arma la lista de unidades —`caso` = el `subtema` que devolvió el paso 1, `contenido` = sus
   oraciones unidas en un párrafo y sin numeración—, **solo con las que todavía no tienen su
   salida**;
2. sustituye `{{UNIDADES}}` en `mvp/prompts/prompt_DATOS.md`;
3. llama al modelo por `proveedores.llamar`, **una vez**;
4. lee la respuesta con `extract_json` y verifica la **forma** (no el contenido);
5. **reparte** la respuesta: escribe un `.out` por unidad, que es lo que lee el cargador.

Escribe, en `mvp/temp/extraccion/<doc>/`:

    p2-<doc>-u<n>-<rN>.out     los datos de esa unidad (uno por unidad: lo que lee el cargador)
    p2-<doc>-tanda-<rN>.json   el crudo de la llamada: unidades enviadas, petición, respuesta,
                               segundos y forma

Idempotente **por unidad**: las que ya tienen su `.out` no se mandan, así una corrida cortada se
retoma sin repetir —ni volver a pagar— lo hecho.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))  # todo lo que el MVP necesita vive acá

from proveedores import llamar  # noqa: E402
from respuesta import extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, reconstruir_subtemas  # noqa: E402

PRUEBAS = RAIZ / "mvp" / "temp" / "pruebas"
PROMPTS = RAIZ / "mvp" / "prompts"
EXTRACCION = RAIZ / "mvp" / "temp" / "extraccion"


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


def forma(parsed, enviadas):
    """Verifica la forma de lo que devolvió la tanda. No juzga el contenido."""
    if not isinstance(parsed, dict) or not isinstance(parsed.get("unidades"), list):
        return {"parseo": False, "unidades": 0, "datos": 0, "problemas": ["no hay lista 'unidades'"]}
    unidades = parsed["unidades"]
    problemas = []
    if len(unidades) != len(enviadas):
        problemas.append(f"devolvió {len(unidades)} y se enviaron {len(enviadas)}")
    numeros = set()
    for u in unidades:
        if not isinstance(u, dict):
            problemas.append("una unidad no es un objeto")
            continue
        if not isinstance(u.get("n"), int):
            problemas.append("una unidad sin 'n'")
        else:
            numeros.add(u["n"])
        if not isinstance(u.get("caso"), str) or not u["caso"].strip():
            problemas.append(f"la unidad n={u.get('n')} sin 'caso'")
        if not isinstance(u.get("datos"), list):
            problemas.append(f"la unidad n={u.get('n')} no trae 'datos'")
            continue
        for i, dato in enumerate(u["datos"], 1):
            if not isinstance(dato, dict):
                problemas.append(f"n={u.get('n')} datos[{i}] no es un objeto")
                continue
            if not isinstance(dato.get("aspecto"), str) or not dato["aspecto"].strip():
                problemas.append(f"n={u.get('n')} datos[{i}] sin 'aspecto'")
            if not isinstance(dato.get("valor"), (str, int, float)):
                problemas.append(f"n={u.get('n')} datos[{i}] sin 'valor'")
            if dato.get("unidad_valor") is not None and not isinstance(dato["unidad_valor"], str):
                problemas.append(f"n={u.get('n')} datos[{i}] 'unidad_valor' no es texto ni null")
    faltan = [i for i in range(1, len(enviadas) + 1) if i not in numeros]
    if faltan:
        problemas.append(f"sin salida para las posiciones {faltan}")
    datos = sum(len(u.get("datos") or []) for u in unidades if isinstance(u, dict))
    return {"parseo": True, "unidades": len(unidades), "datos": datos, "problemas": problemas}


def run(doc, unidades_arg, modelo, rep):
    carpeta = EXTRACCION / doc
    ruta_unidades = resolver_unidades(doc, unidades_arg)
    unidades = json.loads(ruta_unidades.read_text(encoding="utf-8"))["subtemas"]
    texto = (PRUEBAS / f"{doc}.md").read_text(encoding="utf-8")
    _, oraciones_numeradas = numerar_oraciones(texto)
    reconstruidas = reconstruir_subtemas({"subtemas": unidades}, oraciones_numeradas)

    print(f"{doc}: {len(unidades)} unidades desde {ruta_unidades.name} · modelo {modelo}")
    faltantes = []
    for n, unidad in enumerate(reconstruidas, 1):
        if not unidad["oraciones"]:
            print(f"  U{n}: sin oraciones reconstruidas, salto")
            continue
        if (carpeta / f"p2-{doc}-u{n}-{rep}.out").exists():
            print(f"  U{n}: crudo ya existe, salto")
            continue
        faltantes.append((n, unidad))
    if not faltantes:
        print("  no falta ninguna unidad: no se llama al modelo")
        return

    lista = [{"caso": u["subtema"], "contenido": " ".join(u["oraciones"])} for _, u in faltantes]
    ruta_prompt = PROMPTS / "prompt_DATOS.md"
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    if "{{UNIDADES}}" not in plantilla:
        raise SystemExit(f"el prompt '{ruta_prompt.name}' no tiene {{{{UNIDADES}}}}")
    prompt = plantilla.replace("{{UNIDADES}}", json.dumps(lista, ensure_ascii=False))

    print(f"  una llamada con {len(lista)} unidades: {[n for n, _ in faltantes]}")
    t0 = time.time()
    body, resp = llamar(modelo, prompt=prompt)
    segundos = round(time.time() - t0, 1)
    contenido = resp["choices"][0]["message"]["content"] or ""
    parsed, venia_con_cerca, error = extract_json(contenido)
    v = forma(parsed, lista)
    uso = resp.get("usage") or {}

    # Reparto: la posición en la lista enviada es el número real de la unidad.
    por_posicion = {}
    if isinstance(parsed, dict) and isinstance(parsed.get("unidades"), list):
        for item in parsed["unidades"]:
            if isinstance(item, dict) and isinstance(item.get("n"), int):
                por_posicion[item["n"]] = item
    carpeta.mkdir(parents=True, exist_ok=True)
    (carpeta / f"p2-{doc}-tanda-{rep}.json").write_text(json.dumps({
        "doc": doc, "prompt": "prompt_DATOS", "modelo": modelo, "rN": rep,
        "segundos": segundos, "unidades_enviadas": lista,
        "request": body, "response": resp, "parsed": parsed,
        "venia_con_cerca": venia_con_cerca, "error_parseo": error, "forma": v,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    escritas = 0
    for posicion, (n, unidad) in enumerate(faltantes, 1):
        item = por_posicion.get(posicion)
        if item is None:  # sin `n` utilizable: se busca por el caso
            for candidato in (parsed or {}).get("unidades", []):
                if (isinstance(candidato, dict)
                        and str(candidato.get("caso", "")).strip() == unidad["subtema"].strip()):
                    item = candidato
                    break
        if item is None:
            print(f"  U{n}: la tanda no trajo su salida")
            continue
        salida = {"caso": item.get("caso") or unidad["subtema"], "datos": item.get("datos") or []}
        (carpeta / f"p2-{doc}-u{n}-{rep}.out").write_text(
            json.dumps(salida, ensure_ascii=False, indent=2), encoding="utf-8")
        escritas += 1
        print(f"  U{n}: {len(salida['datos'])} datos")

    print(f"  {escritas} de {len(faltantes)} unidades escritas · {segundos} s · "
          f"tokens prompt {uso.get('prompt_tokens')} · completion {uso.get('completion_tokens')}")
    if v["problemas"]:
        print(f"  problemas de forma: {v['problemas']}")
    print(f"  -> {carpeta.relative_to(RAIZ)}/p2-{doc}-tanda-{rep}.json")


if __name__ == "__main__":
    if len(sys.argv) != 5:
        raise SystemExit("uso: python3 mvp/código/paso2_datos.py <doc> <unidades> <modelo> <rN>")
    run(*sys.argv[1:])
