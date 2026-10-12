#!/usr/bin/env python3
"""Paso 1: el documento radicado → sus unidades temáticas, en la base.

Uso:

    python3 mvp/código/paso1_unidades.py <doc> [--modelo deepseek] [--prompt UT] [--rehacer]
    python3 mvp/código/paso1_unidades.py doc8

Qué hace, y nada más:

1. **Verifica el documento**: lee `mvp/documentos/<doc>.md` y comprueba su sello contra la base; si
   el archivo cambió, se detiene (eso es otro documento).
2. **Arma los dos mensajes**: la **plantilla** —que vive en la base, con su versión; el `.md` es la
   puerta y se registra sola la primera vez— va como `system`, y **el texto del documento, entero**
   (títulos incluidos), como `user`. Así la regla viaja como instrucción y el documento como dato, y
   el prefijo invariante queda estable entre documentos.
3. **Llama al modelo** por `proveedores.llamar`: una sola llamada de texto a JSON.
4. **Lee la respuesta** con `extract_json` y **ubica cada oración en el texto** para quedarse con su
   tramo, verificando el contrato —literalidad, cobertura del cuerpo, asignación exclusiva y
   orden—: solo reporta, no corrige.
5. **Cierra el acto**: la corrida con su token, y las **unidades** con sus tramos, en una sola
   transacción.

**Un acto, una fila.** La corrida lleva su **token** y los productos cuelgan de ella. Rehacer es
**correr otra vez**: la partición anterior queda en la base y la vigente es la última exitosa, así
que dos particiones del mismo documento se pueden comparar.

La fila **narra lo que está en la base**: se escribe al cerrar, con el `estado` y el `motivo` de lo
que pasó. Un fallo controlado —la llamada, el corte, el JSON, el contrato— deja su corrida fallida;
una muerte abrupta antes de cerrar no deja constancia, y eso está declarado.

Nada queda en archivos: `mvp/temp/` no se toca.

Idempotente: si el documento ya tiene una UT exitosa, no vuelve a llamar. Para correr otra
partición: `--rehacer`.
"""

import pathlib
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parent.parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))

import almacen  # noqa: E402
from acto import abrir, cerrar  # noqa: E402
from base import conectar, exigir_documento, unidades_de, ut_vigente  # noqa: E402
from extraer_unidades import roturas, verificar_particion  # noqa: E402
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


def escribir_unidades(doc, unidades, verificacion):
    """Lo que el acto produce: las unidades con sus tramos, colgando de la corrida."""
    def escribir(db, corrida_id):
        for posicion, unidad in enumerate(unidades, 1):
            identificador = f"{corrida_id}:U{posicion}"
            db.execute("INSERT INTO unidades (id, documento_id, n, subtema, corrida_id) "
                       "VALUES (?,?,?,?,?)",
                       (identificador, doc, posicion, unidad.get("subtema") or "", corrida_id))
            tramos = verificacion["por_unidad"][posicion - 1]["tramos"]
            for orden, (literal, (desde, hasta)) in enumerate(
                    zip(unidad.get("oraciones") or [], tramos), 1):
                db.execute("INSERT INTO unidad_oraciones (unidad_id, n, desde, hasta, texto) "
                           "VALUES (?,?,?,?,?)", (identificador, orden, desde, hasta, literal))
    return escribir


def run(doc, modelo, prompt_name, rehacer, esfuerzo=None):
    db = conectar()
    fila = exigir_documento(db, doc)
    vigente = ut_vigente(db, doc)
    if vigente and not rehacer:
        unidades = unidades_de(db, vigente)
        print(f"  {doc}: ya tiene una UT vigente ({vigente}, {len(unidades)} unidades) — no se "
              f"llama al modelo. (Para correr otra partición: --rehacer)")
        return
    if vigente:
        print(f"  {doc}: ACTO explícito — se corre otra UT; la vigente ({vigente}) queda")

    prompt = usar_prompt(db, prompt_name, PROMPTS / f"prompt_{prompt_name}.md")
    plantilla = prompt["texto"]
    for hueco in ("{{TEXTO}}", "{{RELOJ_RADICADO}}", "{{RELOJ_SISTEMA}}"):
        if hueco not in plantilla:
            raise SystemExit(f"la plantilla '{prompt['id']}' v{prompt['version']} no tiene {hueco}")

    db_almacen = almacen.conectar()
    texto = almacen.texto_de(db_almacen, doc)  # el original: el markdown del volcado
    db_almacen.close()
    relojes = {"reloj_radicado": reloj_radicado(fila["fecha_radicacion"]),
               "reloj_sistema": reloj_sistema()}
    rotulo = f"{prompt['id']} v{prompt['version']}"
    mensajes = partir(plantilla, rotulo, TEXTO=texto,
                      RELOJ_RADICADO=relojes["reloj_radicado"],
                      RELOJ_SISTEMA=relojes["reloj_sistema"])
    config = resolver(modelo, esfuerzo)
    corrida = abrir(db, "UT", documento_id=doc, prompt_id=prompt["id"],
                    prompt_version=prompt["version"], hash_prompt=prompt["sello"],
                    modelo=config["id"], esfuerzo=config.get("esfuerzo"), **relojes)

    def fallar(motivo):
        """Cierra el acto como fallido y se detiene: el fallo controlado deja su fila."""
        cerrar(db, corrida, "fallido", motivo)
        raise SystemExit(f"  {doc}: el acto falló — {motivo}")

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
    if parsed is None:
        fallar(f"sin JSON: {error} · respuesta: «{extracto(contenido)}»")
    if not isinstance(parsed, dict) or not isinstance(parsed.get("unidades"), list):
        fallar(f"el JSON no trae una lista 'unidades' · respuesta: «{extracto(contenido)}»")

    unidades = parsed["unidades"] or []
    for posicion, unidad in enumerate(unidades, 1):
        if not isinstance(unidad, dict):
            fallar(f"la unidad {posicion} no es un objeto · respuesta: «{extracto(contenido)}»")
        oraciones = unidad.get("oraciones")
        if oraciones is not None and (not isinstance(oraciones, list)
                                      or not all(isinstance(x, str) for x in oraciones)):
            fallar(f"las oraciones de la unidad {posicion} no son una lista de textos")

    verificacion = verificar_particion(texto, unidades)
    rotas = roturas(verificacion)
    if rotas:
        fallar("la partición no cierra — " + " · ".join(rotas))

    token = cerrar(db, corrida, "exitoso", escribir=escribir_unidades(doc, unidades,
                                                                     verificacion))

    print(f"  {doc}: acto {token} · {verificacion['literales']} oraciones · {len(unidades)} "
          f"unidades · {segundos} s · {config['id']} (esfuerzo {config.get('esfuerzo')}) · "
          f"plantilla {rotulo}")
    print(f"    contrato: sin ubicar {len(verificacion['no_ubicadas'])} · "
          f"sin cubrir {len(verificacion['huecos'])} · solapes {len(verificacion['solapes'])} · "
          f"cuerpo cubierto {verificacion['cubiertos_no_blancos']}/"
          f"{verificacion['caracteres_no_blancos']}")
    for posicion, unidad in enumerate(unidades, 1):
        print(f"    U{posicion} · «{unidad.get('subtema')}»")
        for literal, (desde, hasta) in zip(unidad.get("oraciones") or [],
                                           verificacion["por_unidad"][posicion - 1]["tramos"]):
            print(f"      {desde:>7}–{hasta:>3}   {literal}")
    print(f"    -> la base: la corrida {token}, {len(unidades)} unidades y sus tramos")


def main(argumentos):
    if not argumentos:
        raise SystemExit("uso: python3 mvp/código/paso1_unidades.py <doc> "
                         "[--modelo M] [--esfuerzo E] [--prompt UT] [--rehacer]")
    doc = argumentos[0]
    modelo, prompt_name, rehacer, esfuerzo = "deepseek", "UT", False, None
    resto = argumentos[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion == "--rehacer":
            rehacer = True
        elif opcion in ("--modelo", "--esfuerzo", "--prompt") and resto:
            valor = resto.pop(0)
            if opcion == "--modelo":
                modelo = valor
            elif opcion == "--esfuerzo":
                esfuerzo = valor
            else:
                prompt_name = valor
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: paso1_unidades.py <doc> "
                             f"[--modelo M] [--esfuerzo E] [--prompt UT] [--rehacer]")
    run(doc, modelo, prompt_name, rehacer, esfuerzo)


if __name__ == "__main__":
    main(sys.argv[1:])
