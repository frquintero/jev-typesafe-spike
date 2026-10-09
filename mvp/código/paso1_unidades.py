#!/usr/bin/env python3
"""Paso 1: el documento radicado → sus unidades temáticas, en la base.

Uso:

    python3 mvp/código/paso1_unidades.py <doc> [--modelo deepseek] [--prompt UT] [--rehacer]
    python3 mvp/código/paso1_unidades.py doc8

Qué hace, y nada más:

1. **Verifica el documento**: lee `mvp/documentos/<doc>.md` y comprueba su sello contra la base; si
   el archivo cambió, se detiene (eso es otro documento).
2. **Numera las oraciones** y arma **los dos mensajes**: el prompt —reglas y ejemplo— va como
   `system`, y el texto numerado como `user`. Así la regla viaja como instrucción y el documento
   como dato, y el prefijo invariante queda estable entre documentos.
3. **Llama al modelo** por `proveedores.llamar`: una sola llamada de texto a JSON.
4. **Lee la respuesta** con `extract_json` (tolera la cerca de código) y **verifica la partición**
   —huecos, solapes, números fuera de rango—: solo reporta, no corrige.
5. **Escribe en la base**, en una sola transacción: la fila de la **corrida** (modelo, esfuerzo,
   prompt y su hash, tokens, segundos) y las **unidades** —el nombre del caso y los números de
   oración—. Las oraciones literales no se guardan: viven en el documento radicado.

**Todo o nada, y una sola transacción.** Si la llamada falla, si la respuesta se cortó o si el JSON
no se pudo leer, **no se escribe ninguna unidad**: la corrida queda `fallida` con su motivo —lo que
volvió, recortado a la cabeza y la cola, para poder diagnosticar— y, si el intento era un
`--rehacer`, **lo anterior vuelve**: lo que estaba en la base no se pierde por un intento fallido.
La fila de la corrida **narra lo que está en la base**: un reintento fallido no pisa la cita de la
extracción que sigue ahí.

Nada queda en archivos: `mvp/temp/` no se toca.

Idempotente: si el documento ya tiene unidades, no vuelve a llamar. Para rehacerlas: `--rehacer`.
"""

import json
import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from base import (borrar_corridas, borrar_unidades, conectar, exigir_documento,  # noqa: E402
                  exigir_sello, hash_texto, registrar_corrida, unidades_de)
from mensajes import partir  # noqa: E402
from proveedores import ErrorDeLlamada, llamar, resolver  # noqa: E402
from respuesta import extract_json  # noqa: E402
from extraer_unidades import numerar_oraciones, verificar_subtemas  # noqa: E402

PROMPTS = RAIZ / "mvp" / "prompts"
EXTRACTO = 100  # caracteres de la cabeza y de la cola que se guardan de una respuesta ilegible


def extracto(contenido):
    """Lo que se guarda de una respuesta ilegible: la cabeza y la cola, para diagnosticar."""
    limpio = (contenido or "").strip()
    if len(limpio) <= EXTRACTO * 2:
        return limpio
    return f"{limpio[:EXTRACTO]} … {limpio[-EXTRACTO:]}"


def fallar(db, corrida, motivo, conservar):
    """Deja la corrida fallida con su motivo, sin tocar la que ya narra lo que hay en la base."""
    db.rollback()  # vuelve lo que se hubiera borrado en un --rehacer
    registrar_corrida(db, conservar_efectiva=conservar, estado="fallido", motivo=motivo, **corrida)
    db.commit()


def roturas(verificacion):
    """Lo que hace inconsistente la partición con el documento.

    No es una lectura: es una partición rota. Si el texto tiene dieciocho oraciones, cada una tiene
    que quedar en una unidad y una sola, con números que existan y sean enteros. Que el Cámbrico
    vaya junto con la conquista de la tierra firme, en cambio, es una lectura: eso no es una rotura.
    """
    nombres = {"huecos": "oraciones sin unidad", "solapes": "oraciones en dos unidades",
               "fuera_de_rango": "números que no existen", "no_enteros": "números no enteros"}
    return [f"{nombres[clave]}: {verificacion[clave]}"
            for clave in ("huecos", "solapes", "fuera_de_rango", "no_enteros")
            if verificacion.get(clave)]


def run(doc, modelo, prompt_name, rehacer):
    db = conectar()
    fila = exigir_documento(db, doc)
    ya = unidades_de(db, doc)
    if ya and not rehacer:
        print(f"  {doc}: ya tiene {len(ya)} unidades cargadas — no se llama al modelo. "
              f"(Para rehacerlas: --rehacer)")
        return
    if ya:
        print(f"  {doc}: ACTO explícito — se rehacen sus {len(ya)} unidades "
              f"(y los datos que cuelgan de ellas)")
        borrar_unidades(db, doc)
        borrar_corridas(db, doc)  # sin commit: si algo falla, lo anterior vuelve

    texto = exigir_sello(fila)
    ruta_prompt = PROMPTS / f"prompt_{prompt_name}.md"
    plantilla = ruta_prompt.read_text(encoding="utf-8")
    if "{{TEXTO_NUMERADO}}" not in plantilla:
        raise SystemExit(f"el prompt '{ruta_prompt.name}' no tiene {{{{TEXTO_NUMERADO}}}}")

    texto_numerado, registros = numerar_oraciones(texto)
    mensajes = partir(plantilla, ruta_prompt.name, TEXTO_NUMERADO=texto_numerado)
    config = resolver(modelo)
    corrida = dict(id=f"{doc}:UT", paso="UT", documento_id=doc, prompt=ruta_prompt.name,
                   hash_prompt=hash_texto(plantilla), modelo=config["id"],
                   esfuerzo=config.get("esfuerzo"))

    t0 = time.time()
    try:
        _, respuesta = llamar(modelo, mensajes=mensajes)
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
    if parsed is None:
        motivo = f"sin JSON: {error} · respuesta: «{extracto(contenido)}»"
        fallar(db, corrida, motivo, conservar=bool(ya))
        print(f"  {doc}: la corrida falló — el JSON no se pudo leer ({error})")
        print(f"    queda registrada como fallida; no se escribió ninguna unidad")
        return

    verificacion = verificar_subtemas(parsed, registros)
    rotas = roturas(verificacion)
    if rotas:
        motivo = "la partición no cierra — " + " · ".join(rotas)
        fallar(db, corrida, motivo, conservar=bool(ya))
        raise SystemExit(f"  {doc}: la corrida falló — {motivo}")
    subtemas = parsed.get("subtemas") or []
    registrar_corrida(db, estado="exitoso", **corrida)
    for n, subtema in enumerate(subtemas, 1):
        numeros = [str(x) for x in (subtema.get("oraciones") or [])]
        db.execute("INSERT INTO unidades (id, documento_id, n, subtema, oraciones, corrida_id) "
                   "VALUES (?,?,?,?,?,?)",
                   (f"{doc}:U{n}", doc, n, subtema.get("subtema") or "", ",".join(numeros),
                    f"{doc}:UT"))
    db.commit()

    print(f"  {doc}: {len(registros)} oraciones · {len(subtemas)} unidades · {segundos} s · "
          f"{config['id']} (esfuerzo {config.get('esfuerzo')})")
    print(f"    verificación: {json.dumps(verificacion, ensure_ascii=False)}")
    for n, subtema in enumerate(subtemas, 1):
        print(f"    U{n}: [{', '.join(str(x) for x in (subtema.get('oraciones') or []))}] "
              f"{subtema.get('subtema')}")
    print(f"    -> la base: la corrida {doc}:UT y {len(subtemas)} unidades")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/paso1_unidades.py <doc> "
                         "[--modelo M] [--prompt UT] [--rehacer]")
    doc = argumentos[0]
    modelo, prompt_name, rehacer = "deepseek", "UT", False
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion == "--rehacer":
            rehacer = True
        elif opcion in ("--modelo", "--prompt") and resto:
            valor = resto.pop(0)
            if opcion == "--modelo":
                modelo = valor
            else:
                prompt_name = valor
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: paso1_unidades.py <doc> "
                             f"[--modelo M] [--prompt UT] [--rehacer]")
    run(doc, modelo, prompt_name, rehacer)


if __name__ == "__main__":
    main(sys.argv[1:])
