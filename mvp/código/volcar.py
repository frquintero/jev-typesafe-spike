#!/usr/bin/env python3
"""El volcado: **una fuente → el markdown original, en el almacén**. Este acto **es la radicación**.

Uso:

    python3 mvp/código/volcar.py <fuente> [--id NOMBRE] [--coleccion E] [--modelo M] [--esfuerzo E]
    python3 mvp/código/volcar.py mvp/documentos/sol.md

Qué hace, y nada más:

1. **Lee la fuente** y su procedencia (nombre, ruta, mtime). Eso pasa a ser **traza**, no identidad.
2. **Toma la plantilla** de la base (`prompt_volcado`): el `.md` de `mvp/prompts/` es la puerta y se
   registra solo la primera vez, con su versión.
3. **Pide el índice** al modelo —los encabezados, con su `padre`— en una sola llamada.
4. **Verifica y arma el markdown**: ubica cada título y le inserta el marcador canónico. Nada del
   texto se reescribe, y quitar las marcas devuelve la fuente tal cual.
5. **Escribe, en una sola transacción**: el documento en el almacén, su **cédula** con su token y
   **el espejo** del corpus.

**Un documento radicado no se mueve**: si el id ya está, no se llama al modelo y se reporta. Volver a
volcar la misma fuente es **otro documento**, con otro id (los distingue la fecha). No hay `--rehacer`
y la fuente no es candado: es procedencia.

Un fallo controlado —la llamada, el corte, el JSON, la verificación— deja la **cédula fallida** con su
motivo y **no escribe documento**: es el único caso en que la cédula existe sola.

Nada queda en archivos: `mvp/temp/` no se toca.
"""

import pathlib
import sys
import time
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

from ajustes import resolver as resolver_ajuste  # noqa: E402
import almacen  # noqa: E402
from acto import abrir  # noqa: E402
from armar_volcado import armar  # noqa: E402
from base import conectar as conectar_corpus, hash_texto  # noqa: E402
from esquema import PREFIJO_ALMACEN  # noqa: E402
from mensajes import partir  # noqa: E402
from prompts import usar as usar_prompt  # noqa: E402
from proveedores import ErrorDeLlamada, llamar, resolver  # noqa: E402
from relojes import reloj_radicado, reloj_sistema  # noqa: E402
from respuesta import extract_json  # noqa: E402

PROMPTS = RAIZ / "mvp" / "prompts"
EXTRACTO = 100  # caracteres de la cabeza y de la cola que se guardan de una respuesta ilegible


def extracto(contenido):
    """Lo que se guarda de una respuesta ilegible: la cabeza y la cola, para diagnosticar."""
    limpio = (contenido or "").strip()
    if len(limpio) <= EXTRACTO * 2:
        return limpio
    return f"{limpio[:EXTRACTO]} … {limpio[-EXTRACTO:]}"


def procedencia_de(ruta):
    """La fuente como **traza**: de qué archivo salió, dónde estaba y cuándo se lo tocó."""
    return {"nombre": ruta.name, "ruta": str(ruta.resolve()),
            "fecha_modificacion": datetime.fromtimestamp(
                ruta.stat().st_mtime).strftime("%Y-%m-%d %H:%M:%S")}


def run(fuente, identificador, coleccion, modelo, esfuerzo=None):
    ruta = pathlib.Path(fuente)
    if not ruta.is_file():
        raise SystemExit(f"no está la fuente '{fuente}'")
    texto = ruta.read_text(encoding="utf-8")
    if not texto.strip():
        raise SystemExit(f"la fuente '{fuente}' está vacía: no hay nada que volcar")
    procedencia = procedencia_de(ruta)

    db = almacen.conectar()
    ya = almacen.documento(db, identificador)
    if ya is not None:
        raise SystemExit(f"'{identificador}' ya está radicado (sello {ya['sello'][:12]}…, "
                         f"radicado {ya['fecha_radicacion']}): un documento radicado no se mueve. "
                         f"Volcá la fuente con otro --id.")

    db_corpus = conectar_corpus()  # la política —modelo y esfuerzo— vive en el centro
    modelo, esfuerzo = resolver_ajuste(db_corpus, "volcado", modelo, esfuerzo)
    db_corpus.close()

    prompt = usar_prompt(db, "volcado", PROMPTS / "prompt_volcado.md")
    plantilla = prompt["texto"]
    for hueco in ("{{TEXTO}}", "{{RELOJ_RADICADO}}", "{{RELOJ_SISTEMA}}"):
        if hueco not in plantilla:
            raise SystemExit(f"la plantilla '{prompt['id']}' v{prompt['version']} no tiene {hueco}")

    # En el volcado todavía no hay documento: el reloj del radicado **es** el del acto.
    momento = datetime.now()
    relojes = {"reloj_radicado": reloj_radicado(momento), "reloj_sistema": reloj_sistema(momento)}
    rotulo = f"{prompt['id']} v{prompt['version']}"
    mensajes = partir(plantilla, rotulo, TEXTO=texto,
                      RELOJ_RADICADO=relojes["reloj_radicado"],
                      RELOJ_SISTEMA=relojes["reloj_sistema"])

    config = resolver(modelo, esfuerzo)
    volcado = abrir(db, "volcado", prefijo=PREFIJO_ALMACEN, modelo=config["id"],
                    esfuerzo=config.get("esfuerzo"), prompt_id=prompt["id"],
                    prompt_version=prompt["version"], hash_prompt=prompt["sello"],
                    sello_fuente=hash_texto(texto), **relojes)

    def fallar(motivo):
        """Deja la cédula fallida con su motivo y se detiene: no se escribe documento."""
        volcado["terminado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        almacen.registrar_fallo(db, volcado, motivo)
        raise SystemExit(f"  {identificador}: el volcado falló — {motivo}")

    print(f"  {identificador}: {len(texto)} caracteres de «{procedencia['nombre']}» · "
          f"plantilla {rotulo} · {config['id']} (esfuerzo {config.get('esfuerzo')})")
    t0 = time.time()
    try:
        _, respuesta = llamar(modelo, mensajes=mensajes, esfuerzo=esfuerzo)
    except ErrorDeLlamada as error:
        fallar(str(error))

    segundos = round(time.time() - t0, 1)
    uso = respuesta.get("usage") or {}
    volcado.update(tokens_entrada=uso.get("prompt_tokens"),
                   tokens_salida=uso.get("completion_tokens"),
                   tokens_pensando=uso.get("thinking_tokens"),
                   cache_hit=uso.get("prompt_cache_hit_tokens"), segundos=segundos)
    terminó = respuesta["choices"][0].get("finish_reason")
    contenido = respuesta["choices"][0]["message"]["content"] or ""
    if terminó != "stop":
        fallar(f"la respuesta se cortó ({terminó})")

    parsed, venia_con_cerca, error = extract_json(contenido)
    if parsed is None:
        fallar(f"sin JSON: {error} · respuesta: «{extracto(contenido)}»")

    armado = armar(texto, parsed)
    if armado["problemas"]:
        fallar("el índice no cierra — " + " · ".join(armado["problemas"]))

    volcado["terminado"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    resultado = almacen.escribir(db, identificador, coleccion, armado["markdown"], procedencia,
                                 volcado)
    db.close()

    print(f"  {identificador}: acto {volcado['id']} · {len(armado['filas'])} encabezados · "
          f"{len(armado['markdown']) - len(texto)} caracteres de marca · "
          f"{armado['descartadas']} marcador(es) previo(s) descartado(s) · {segundos} s")
    print(f"    ida y vuelta: quitar las marcas devuelve la fuente, tal cual")
    print(f"    -> el almacén: el documento (sello {resultado['sello'][:12]}…) y su cédula "
          f"{volcado['id']}")
    print(f"    -> el corpus: su fila en documentos, con el mismo sello")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/volcar.py <fuente> [--id NOMBRE] "
                         "[--coleccion E] [--modelo M] [--esfuerzo E]")
    fuente = argumentos[0]
    identificador = pathlib.Path(fuente).stem
    coleccion, modelo, esfuerzo = "GENERAL", None, None
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion in ("--id", "--coleccion", "--modelo", "--esfuerzo") and resto:
            valor = resto.pop(0)
            if opcion == "--id":
                identificador = valor
            elif opcion == "--coleccion":
                coleccion = valor
            elif opcion == "--modelo":
                modelo = valor
            else:
                esfuerzo = valor
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: volcar.py <fuente> [--id NOMBRE] "
                             f"[--coleccion E] [--modelo M] [--esfuerzo E]")
    run(fuente, identificador, coleccion, modelo, esfuerzo)


if __name__ == "__main__":
    main(sys.argv[1:])
