#!/usr/bin/env python3
"""Paso 2: las unidades de la base → los datos, en la base. Va **en tanda**.

Uso:

    python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--esfuerzo E] [--rehacer]
    python3 mvp/código/paso2_datos.py sol

Qué hace, y nada más:

1. **Lee la UT vigente de la base** (la escribió el paso 1) con **sus tramos**: la oración literal
   que el modelo devolvió en cada una, en orden; y comprueba el **sello** del documento en el almacén
   (`almacen.texto_de`), que es sobre cuyo texto se cuentan los tramos. El paso 2 **no corta ni
   numera nada**.
2. **Una sola llamada** —la tanda— con **todas** las unidades de esa UT y **los dos mensajes**: la
   **plantilla** (de la base, con su versión) como `system`, y las unidades como `user`. La
   respuesta se reparte por la **posición en la lista enviada**.
3. **Verifica la forma** de lo que volvió: que estén todas las posiciones y que cada dato traiga
   aspecto y valor. No juzga el contenido.
4. **Cierra el acto**: la corrida con su token y los datos, en una sola transacción. La corrida
   guarda **de qué UT** salieron las unidades (`corrida_origen`).

**Un acto, una fila.** Los datos cuelgan de su corrida y llevan su token en el id, así que una
tanda nueva **no pisa** la anterior: la vigente es la última exitosa **sobre la UT vigente**.

La fila se escribe al cerrar, con su `estado` y su `motivo`: un fallo controlado deja su corrida
fallida; una muerte abrupta antes de cerrar no deja constancia, y eso está declarado.

Nada queda en archivos: `mvp/temp/` no se toca.

Idempotente: si el documento ya tiene su tanda de DATOS sobre la UT vigente, no vuelve a llamar.
Para correr otra tanda: `--rehacer`.
"""

import json
import pathlib
import sys
import time
import unicodedata

AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from ajustes import resolver as resolver_ajuste  # noqa: E402
import almacen  # noqa: E402
from acto import abrir, cerrar  # noqa: E402
from base import (conectar, datos_vigente, exigir_documento,  # noqa: E402
                  unidades_vigentes, ut_vigente)
from mensajes import partir  # noqa: E402
from prompts import usar as usar_prompt  # noqa: E402
from proveedores import ErrorDeLlamada, llamar, resolver  # noqa: E402
from relojes import reloj_radicado, reloj_sistema  # noqa: E402
from respuesta import extract_json  # noqa: E402

EXTRACTO = 100  # caracteres de la cabeza y de la cola que se guardan de una respuesta ilegible


def extracto(contenido):
    """Lo que se guarda de una respuesta ilegible: la cabeza y la cola, para diagnosticar."""
    limpio = (contenido or "").strip()
    if len(limpio) <= EXTRACTO * 2:
        return limpio
    return f"{limpio[:EXTRACTO]} … {limpio[-EXTRACTO:]}"


def oraciones_de(db, unidad_id):
    """Las oraciones de una unidad, tal como las devolvió el modelo, en orden."""
    return [fila["texto"] for fila in db.execute(
        "SELECT texto FROM unidad_oraciones WHERE unidad_id = ? ORDER BY n", (unidad_id,))]


def _sin_tildes(texto):
    """El texto en minúsculas y sin tildes, para comparar sin que estorbe la ortografía."""
    return "".join(c for c in unicodedata.normalize("NFD", texto.lower())
                   if unicodedata.category(c) != "Mn")


def forma(parsed, enviadas):
    """Verifica la forma de lo que devolvió la tanda.

    Devuelve dos cosas distintas, y la diferencia importa:

    - `problemas`: la **forma**. Si hay uno solo, el acto no escribe nada (todo o nada): el contrato
      está declarado en el prompt y una clave de más o un dato sin `aspecto` es una violación.
    - `avisos`: lo que es **contenido** —dónde va la unidad de medida— y no se juzga desde acá: se
      reporta y el dato entra igual.

    Lo que decide es la forma y la consistencia; lo que se juzga, se reporta.
    """
    if not isinstance(parsed, dict) or not isinstance(parsed.get("unidades"), list):
        return {"parseo": False, "unidades": 0, "datos": 0, "problemas": ["no hay lista 'unidades'"],
                "avisos": []}
    unidades = parsed["unidades"]
    problemas = [f"clave de más en la raíz: «{clave}»" for clave in parsed if clave != "unidades"]
    avisos = []
    if len(unidades) != len(enviadas):
        problemas.append(f"devolvió {len(unidades)} y se enviaron {len(enviadas)}")
    numeros = set()
    for u in unidades:
        if not isinstance(u, dict):
            problemas.append("una unidad no es un objeto")
            continue
        problemas += [f"unidad n={u.get('n')}: clave de más «{clave}»"
                      for clave in u if clave not in ("n", "caso", "datos")]
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
                problemas.append(f"n={u.get('n')} dato {i} no es un objeto")
                continue
            problemas += [f"n={u.get('n')} dato {i}: clave de más «{clave}»"
                          for clave in dato if clave not in ("aspecto", "valor", "unidad_valor")]
            if not isinstance(dato.get("aspecto"), str) or not dato["aspecto"].strip():
                problemas.append(f"n={u.get('n')} dato {i} sin 'aspecto'")
            if not isinstance(dato.get("valor"), (str, int, float)):
                problemas.append(f"n={u.get('n')} dato {i} sin 'valor'")
            if dato.get("unidad_valor") is not None and not isinstance(dato["unidad_valor"], str):
                problemas.append(f"n={u.get('n')} dato {i} 'unidad_valor' no es texto ni null")
            unidad_valor = dato.get("unidad_valor")
            if (isinstance(unidad_valor, str) and unidad_valor.strip()
                    and isinstance(dato.get("valor"), str)
                    and _sin_tildes(unidad_valor).strip() in _sin_tildes(dato["valor"])):
                avisos.append(f"n={u.get('n')} dato {i}: la unidad «{unidad_valor}» también está "
                              f"dentro del valor")
    faltan = [i for i in range(1, len(enviadas) + 1) if i not in numeros]
    if faltan:
        problemas.append(f"sin salida para las posiciones {faltan}")
    datos = sum(len(u.get("datos") or []) for u in unidades if isinstance(u, dict))
    return {"parseo": True, "unidades": len(unidades), "datos": datos, "problemas": problemas,
            "avisos": avisos}


def escribir_datos(armadas, por_posicion):
    """Lo que el acto produce: los datos, colgando de la corrida y de su unidad.

    El id lleva **la tanda, la unidad y el orden dentro de la unidad**: `C000002:U1:D1`. Sin la
    unidad, dos unidades de la misma tanda repetirían el id (el contador `j` empieza de nuevo en
    cada una) y la tanda entera se caería por la clave primaria.
    """
    def escribir(db, corrida_id):
        for posicion, (unidad, _) in enumerate(armadas, 1):
            item = por_posicion.get(posicion) or {}
            for j, dato in enumerate(item.get("datos") or [], 1):
                db.execute("INSERT INTO datos (id, unidad_id, caso, aspecto, valor, unidad_valor, "
                           "corrida_id) VALUES (?,?,?,?,?,?,?)",
                           (f"{corrida_id}:U{unidad['n']}:D{j}", unidad["id"],
                            unidad["subtema"] or item.get("caso") or "",
                            dato["aspecto"], str(dato["valor"]), dato.get("unidad_valor"),
                            corrida_id))
    return escribir


def run(doc, modelo, rehacer, esfuerzo=None):
    db = conectar()
    fila = exigir_documento(db, doc)
    modelo, esfuerzo = resolver_ajuste(db, "DATOS", modelo, esfuerzo)
    ut = ut_vigente(db, doc)
    if ut is None:
        raise SystemExit(f"'{doc}' no tiene unidades: el paso 1 va primero "
                         f"(python3 mvp/código/paso1_unidades.py {doc})")
    unidades = unidades_vigentes(db, doc)
    if not unidades:
        raise SystemExit(f"la UT vigente de '{doc}' ({ut}) no tiene unidades: se rehace el paso 1")

    tanda = datos_vigente(db, doc)
    if tanda and not rehacer:
        cuantos = db.execute("SELECT COUNT(*) FROM datos WHERE corrida_id = ?",
                             (tanda,)).fetchone()[0]
        print(f"  {doc}: ya tiene su tanda de DATOS sobre la UT vigente ({tanda}, {cuantos} "
              f"datos) — no se llama al modelo. (Para correr otra tanda: --rehacer)")
        return
    if tanda:
        print(f"  {doc}: ACTO explícito — se corre otra tanda sobre la UT {ut}; "
              f"la vigente ({tanda}) queda")

    prompt = usar_prompt(db, "DATOS")
    plantilla = prompt["texto"]
    for hueco in ("{{UNIDADES}}", "{{RELOJ_RADICADO}}", "{{RELOJ_SISTEMA}}"):
        if hueco not in plantilla:
            raise SystemExit(f"la plantilla '{prompt['id']}' v{prompt['version']} no tiene {hueco}")

    relojes = {"reloj_radicado": reloj_radicado(fila["fecha_radicacion"]),
               "reloj_sistema": reloj_sistema()}
    config = resolver(modelo, esfuerzo)
    corrida = abrir(db, "DATOS", documento_id=doc, prompt_id=prompt["id"],
                    prompt_version=prompt["version"],
                    modelo=config["id"], esfuerzo=config.get("esfuerzo"),
                    corrida_origen=ut, **relojes)

    def fallar(motivo):
        """Cierra el acto como fallido y se detiene: el fallo controlado deja su fila."""
        cerrar(db, corrida, "fallido", motivo)
        raise SystemExit(f"  {doc}: el acto falló — {motivo}")

    # Todo o nada: si una unidad no se puede armar, no se llama al modelo.
    db_almacen = almacen.conectar()
    almacen.texto_de(db_almacen, doc)  # el texto no cambió: los tramos se cuentan sobre él
    db_almacen.close()
    armadas = [(unidad, oraciones_de(db, unidad["id"])) for unidad in unidades]
    sin_armar = [unidad["id"] for unidad, oraciones in armadas if not oraciones]
    if sin_armar:
        fallar(f"no se pudieron armar sus oraciones: {', '.join(sin_armar)}")

    # El material va con la forma que el ejemplo del prompt enseña: un bloque por unidad, con su
    # `caso` y sus `satélites` numerados desde [1] en cada bloque.
    lista = [{"caso": unidad["subtema"], "satelites": oraciones}
             for unidad, oraciones in armadas]
    bloques = ["caso: " + unidad["caso"] + "\nsatélites:\n"
               + "\n".join(f"[{k}] {oracion}" for k, oracion in enumerate(unidad["satelites"], 1))
               for unidad in lista]
    rotulo = f"{prompt['id']} v{prompt['version']}"
    mensajes = partir(plantilla, rotulo, UNIDADES="\n\n".join(bloques),
                      RELOJ_RADICADO=relojes["reloj_radicado"],
                      RELOJ_SISTEMA=relojes["reloj_sistema"])

    print(f"  {doc}: una llamada con {len(lista)} unidades de la UT {ut} "
          f"({[unidad['id'] for unidad, _ in armadas]}) · {config['id']} · plantilla {rotulo}")
    t0 = time.time()
    try:
        _, respuesta = llamar(modelo, mensajes=mensajes, esfuerzo=esfuerzo)
    except ErrorDeLlamada as error:
        fallar(str(error))

    segundos = round(time.time() - t0, 1)
    uso = respuesta.get("usage") or {}
    corrida.update(
        tokens_entrada=uso.get("prompt_tokens"), tokens_salida=uso.get("completion_tokens"),
        tokens_pensando=uso.get("thinking_tokens"), cache_hit=uso.get("prompt_cache_hit_tokens"),
        segundos=segundos)
    terminó = respuesta["choices"][0].get("finish_reason")
    contenido = respuesta["choices"][0]["message"]["content"] or ""
    if terminó != "stop":
        fallar(f"la respuesta se cortó ({terminó})")

    parsed, venia_con_cerca, error = extract_json(contenido)
    verificacion = forma(parsed, lista)
    if parsed is None or verificacion["problemas"]:
        motivo = (f"sin JSON: {error} · respuesta: «{extracto(contenido)}»" if parsed is None
                  else "; ".join(verificacion["problemas"]))
        fallar(motivo)

    por_posicion = {item["n"]: item for item in parsed["unidades"]
                    if isinstance(item.get("n"), int)}
    token = cerrar(db, corrida, "exitoso", escribir=escribir_datos(armadas, por_posicion))
    cargados = sum(len((por_posicion.get(posicion) or {}).get("datos") or [])
                   for posicion in range(1, len(armadas) + 1))

    print(f"  {doc}: acto {token} · {len(armadas)} unidades de la UT {ut} · {cargados} datos · "
          f"{segundos} s · {config['id']} (esfuerzo {config.get('esfuerzo')}) · plantilla {rotulo}")
    print(f"    verificación: {json.dumps(verificacion, ensure_ascii=False)}")
    for aviso in verificacion["avisos"]:
        print(f"    aviso: {aviso}")
    print(f"    -> la base: la corrida {token} y {cargados} datos")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/paso2_datos.py <doc> [--modelo M] [--esfuerzo E] [--rehacer]")
    doc = argumentos[0]
    modelo, rehacer, esfuerzo = None, False, None
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion == "--rehacer":
            rehacer = True
        elif opcion == "--modelo" and resto:
            modelo = resto.pop(0)
        elif opcion == "--esfuerzo" and resto:
            esfuerzo = resto.pop(0)
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: paso2_datos.py <doc> "
                             f"[--modelo M] [--esfuerzo E] [--rehacer]")
    run(doc, modelo, rehacer, esfuerzo)


if __name__ == "__main__":
    main(sys.argv[1:])
