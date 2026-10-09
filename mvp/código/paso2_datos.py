#!/usr/bin/env python3
"""Paso 2: las unidades de la base → los datos, en la base. Va **en tanda**.

Uso:

    python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--rehacer]
    python3 mvp/código/paso2_datos.py doc8

Qué hace, y nada más:

1. **Lee las unidades de la base** (las escribió el paso 1) y el texto del documento radicado, para
   reponer las oraciones literales de cada unidad: del número a la oración. El sello es el guardián.
2. **Una sola llamada** —la tanda— con **todas** las unidades del documento, y la respuesta se
   reparte por la **posición en la lista enviada**.
3. **Verifica la forma** de lo que volvió: que estén todas las posiciones y que cada dato traiga
   aspecto y valor. No juzga el contenido.
4. **Escribe en la base**, en una sola transacción: la fila de la **corrida** y los **datos**.

**Todo o nada.** Si alguna unidad no se puede armar (sus oraciones no resuelven al texto), no se
llama al modelo: la corrida falla con ese motivo. Si la llamada falla, si la respuesta se cortó o si
lo que volvió no sirve, **no se escribe ningún dato**. En los dos casos la corrida queda `fallida`
con su motivo —lo que volvió, recortado a la cabeza y la cola— y, si el intento era un `--rehacer`,
**lo anterior vuelve**: lo que estaba en la base no se pierde por un intento fallido. La fila de la
corrida **narra lo que está en la base**.

Nada queda en archivos: `mvp/temp/` no se toca.

Idempotente: si el documento ya tiene datos, no vuelve a llamar. Para rehacerlos: `--rehacer`.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from base import (borrar_datos, conectar, datos_de, exigir_documento,  # noqa: E402
                  exigir_sello, hash_texto, registrar_corrida, unidades_de)
from proveedores import ErrorDeLlamada, llamar, resolver  # noqa: E402
from respuesta import extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones  # noqa: E402

PROMPTS = RAIZ / "mvp" / "prompts"
EXTRACTO = 100  # caracteres de la cabeza y de la cola que se guardan de una respuesta ilegible


def extracto(contenido):
    """Lo que se guarda de una respuesta ilegible: la cabeza y la cola, para diagnosticar."""
    limpio = (contenido or "").strip()
    if len(limpio) <= EXTRACTO * 2:
        return limpio
    return f"{limpio[:EXTRACTO]} … {limpio[-EXTRACTO:]}"


def literales(unidad, por_numero):
    """Las oraciones literales de una unidad, del número a la oración."""
    numeros = [n for n in (unidad["oraciones"] or "").split(",") if n.strip()]
    return [por_numero[int(n)] for n in numeros if n.strip().isdigit() and int(n) in por_numero]


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


def fallar(db, corrida, motivo, conservar):
    """Deja la corrida fallida con su motivo, sin tocar la que ya narra lo que hay en la base."""
    db.rollback()  # vuelve lo que se hubiera borrado en un --rehacer
    registrar_corrida(db, conservar_efectiva=conservar, estado="fallido", motivo=motivo, **corrida)
    db.commit()


def run(doc, modelo, rehacer):
    db = conectar()
    fila = exigir_documento(db, doc)
    unidades = unidades_de(db, doc)
    if not unidades:
        raise SystemExit(f"'{doc}' no tiene unidades: el paso 1 va primero "
                         f"(python3 mvp/código/paso1_unidades.py {doc})")

    ya = datos_de(db, doc)
    if ya and not rehacer:
        print(f"  {doc}: ya tiene {ya} datos cargados — no se llama al modelo. "
              f"(Para rehacerlos: --rehacer)")
        return
    if ya:
        print(f"  {doc}: ACTO explícito — se rehacen los datos de {len(unidades)} unidades")
        borrar_datos(db, doc)  # sin commit: si algo falla, lo anterior vuelve

    ruta_prompt = PROMPTS / "prompt_DATOS.md"
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    if "{{UNIDADES}}" not in plantilla:
        raise SystemExit(f"el prompt '{ruta_prompt.name}' no tiene {{{{UNIDADES}}}}")
    config = resolver(modelo)
    corrida = dict(id=f"{doc}:DATOS", paso="DATOS", documento_id=doc, prompt=ruta_prompt.name,
                   hash_prompt=hash_texto(plantilla), modelo=config["id"],
                   esfuerzo=config.get("esfuerzo"))

    # Todo o nada: si una unidad no se puede armar, no se llama al modelo.
    texto = exigir_sello(fila)
    _, registros = numerar_oraciones(texto)
    por_numero = {registro["n"]: registro["oracion"] for registro in registros}
    armadas = [(unidad, literales(unidad, por_numero)) for unidad in unidades]
    sin_armar = [unidad["id"] for unidad, oraciones in armadas if not oraciones]
    if sin_armar:
        motivo = f"no se pudieron armar sus oraciones: {', '.join(sin_armar)}"
        fallar(db, corrida, motivo, conservar=bool(ya))
        raise SystemExit(f"  {doc}: la corrida falló — {motivo}")

    lista = [{"caso": unidad["subtema"], "contenido": " ".join(oraciones)}
             for unidad, oraciones in armadas]
    prompt = plantilla.replace("{{UNIDADES}}", json.dumps(lista, ensure_ascii=False))

    print(f"  {doc}: una llamada con {len(lista)} unidades "
          f"({[unidad['id'] for unidad, _ in armadas]}) · {config['id']}")
    t0 = time.time()
    try:
        _, respuesta = llamar(modelo, prompt=prompt)
    except ErrorDeLlamada as error:
        fallar(db, corrida, str(error), conservar=bool(ya))
        raise SystemExit(f"  {doc}: la corrida falló — {error}")

    segundos = round(time.time() - t0, 1)
    uso = respuesta.get("usage") or {}
    corrida.update(
        tokens_entrada=uso.get("prompt_tokens"), tokens_salida=uso.get("completion_tokens"),
        tokens_pensando=uso.get("thinking_tokens"), cache_hit=uso.get("prompt_cache_hit_tokens"),
        segundos=segundos)
    terminó = respuesta["choices"][0].get("finish_reason")
    contenido = respuesta["choices"][0]["message"]["content"] or ""
    if terminó != "stop":
        fallar(db, corrida, f"la respuesta se cortó ({terminó})", conservar=bool(ya))
        raise SystemExit(f"  {doc}: la corrida falló — la respuesta se cortó ({terminó})")

    parsed, venia_con_cerca, error = extract_json(contenido)
    verificacion = forma(parsed, lista)
    if parsed is None or verificacion["problemas"]:
        motivo = (f"sin JSON: {error} · respuesta: «{extracto(contenido)}»" if parsed is None
                  else "; ".join(verificacion["problemas"]))
        fallar(db, corrida, motivo, conservar=bool(ya))
        print(f"  {doc}: la corrida falló — {motivo}")
        print("    queda registrada como fallida; no se escribió ningún dato")
        return

    por_posicion = {item["n"]: item for item in parsed["unidades"]
                    if isinstance(item.get("n"), int)}
    registrar_corrida(db, estado="exitoso", **corrida)
    cargados = 0
    for posicion, (unidad, _) in enumerate(armadas, 1):
        item = por_posicion.get(posicion) or {}
        for j, dato in enumerate(item.get("datos") or [], 1):
            db.execute("INSERT INTO datos (id, unidad_id, caso, aspecto, valor, unidad_valor, "
                       "corrida_id) VALUES (?,?,?,?,?,?,?)",
                       (f"{unidad['id']}:D{j}", unidad["id"],
                        dato.get("caso") or unidad["subtema"] or item.get("caso") or "",
                        dato["aspecto"], str(dato["valor"]), dato.get("unidad_valor"),
                        f"{doc}:DATOS"))
            cargados += 1
    db.commit()

    print(f"  {doc}: {len(armadas)} unidades · {cargados} datos · {segundos} s · "
          f"{config['id']} (esfuerzo {config.get('esfuerzo')})")
    print(f"    verificación: {json.dumps(verificacion, ensure_ascii=False)}")
    print(f"    -> la base: la corrida {doc}:DATOS y {cargados} datos")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--rehacer]")
    doc = argumentos[0]
    modelo, rehacer = "deepseek", False
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion == "--rehacer":
            rehacer = True
        elif opcion == "--modelo" and resto:
            modelo = resto.pop(0)
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: paso2_datos.py <doc> "
                             f"[--modelo M] [--rehacer]")
    run(doc, modelo, rehacer)


if __name__ == "__main__":
    main(sys.argv[1:])
