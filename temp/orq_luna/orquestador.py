#!/usr/bin/env python3
"""La etapa 3 (la consulta) en el **scratch**: corre con Luna `low` y no toca la base.

Reusa los módulos **vigentes** del ORQ del repo (`mvp/código/orq/`) para todo menos dos cosas:

- la llamada al modelo va por `adaptador_luna` (la familia `responses` con herramientas);
- lo que el ORQ del repo escribe en la base (`registrar_consulta`), acá se escribe en `out/`.

Todo lo que lee lo lee en solo lectura: la base, R, el prompt y la batería de preguntas.

    bash -ic 'python3 temp/orq_luna/orquestador.py [n] [ruta del prompt]'

`n` es la pregunta de la batería (1 por defecto) y el prompt es opcional: sin él usa el del repo
(`mvp/prompts/prompt_ORQ.md`); con él, una copia de trabajo —por ejemplo la temporal de acá al
lado—. El nombre de la salida lleva el del prompt, para que una corrida no pise la otra.
"""

import json
import pathlib
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]  # temp/orq_luna → la raíz
AQUI = pathlib.Path(__file__).resolve().parent

sys.path.insert(0, str(RAIZ / "mvp" / "código" / "orq"))
sys.path.insert(0, str(RAIZ / "mvp" / "código"))
sys.path.insert(0, str(AQUI))

import adaptador_luna  # noqa: E402
import bucle as bucle_repo  # noqa: E402
from abrir_db import abrir_db  # noqa: E402
from anclas import anclas  # noqa: E402
from armar_herramientas import armar_herramientas  # noqa: E402
from armar_prompt import armar_prompt  # noqa: E402
from leer_pregunta import leer_pregunta  # noqa: E402
from listar_casos import listar_casos  # noqa: E402
from resolver_dominio import resolver_dominio  # noqa: E402

# La única pieza que cambia respecto del ORQ del repo.
bucle_repo.llamar_modelo = adaptador_luna.llamar_modelo

BATERIA = RAIZ / "mvp" / "consulta" / "preguntas_sol.md"
PROMPT_POR_DEFECTO = RAIZ / "mvp" / "prompts" / "prompt_ORQ.md"
CORPUS = RAIZ / "mvp" / "código" / "corpus.db"
RUTA_R = RAIZ / "mvp" / "código" / "R.json"

CONFIG = {"dominio": "GENERAL",
          "modelo": {"alias": "luna", "esfuerzo": "low"},
          "guardias": {"max_turnos": 8, "max_herramientas": 20}}


def recorrido(mensajes):
    """La secuencia de lo que pasó, para leerla de un vistazo."""
    pasos = []
    for mensaje in mensajes:
        if mensaje.get("role") == "assistant" and mensaje.get("tool_calls"):
            pasos.append({"pidio": [{"herramienta": llamada["function"]["name"],
                                     "argumentos": llamada["function"]["arguments"]}
                                    for llamada in mensaje["tool_calls"]]})
        elif mensaje.get("role") == "tool":
            contenido = mensaje.get("content") or ""
            pasos.append({"volvio": contenido[:600] + ("…" if len(contenido) > 600 else "")})
    return pasos


def main():
    numero = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    prompt = (RAIZ / sys.argv[2]) if len(sys.argv) > 2 else PROMPT_POR_DEFECTO

    pregunta = leer_pregunta(BATERIA, numero)
    r = json.loads(RUTA_R.read_text(encoding="utf-8"))
    db = abrir_db(CORPUS)
    documentos = resolver_dominio(db, CONFIG["dominio"])
    casos = listar_casos(db, documentos)
    herramientas = armar_herramientas(r)
    marcas = anclas()
    mensajes = armar_prompt(prompt, pregunta, casos, marcas)

    print(f"dominio {CONFIG['dominio']} · documentos {[d['id'] for d in documentos]} · "
          f"{len(casos)} casos · herramientas {[h['function']['name'] for h in herramientas]}")
    print(f"modelo {CONFIG['modelo']['alias']} {CONFIG['modelo']['esfuerzo']} · "
          f"prompt {prompt.relative_to(RAIZ)}")
    print(f"pregunta {numero}: {pregunta}\n")

    estado = bucle_repo.bucle(CONFIG, mensajes, herramientas, db, casos)

    etiqueta = f"q{numero}-{prompt.stem}"
    (AQUI / "out").mkdir(exist_ok=True)
    crudo = AQUI / "out" / f"crudo-luna-{etiqueta}.json"
    salida = AQUI / "out" / f"salida-luna-{etiqueta}.md"

    crudo.write_text(json.dumps({
        "doc": "sol", "bateria": str(BATERIA.relative_to(RAIZ)), "numero": numero,
        "pregunta": pregunta, "dominio": CONFIG["dominio"],
        "prompt": str(prompt.relative_to(RAIZ)),
        "documentos": [d["id"] for d in documentos], "casos": casos,
        "herramientas": [h["function"]["name"] for h in herramientas],
        "anclas": marcas, "r": r, "modelo": CONFIG["modelo"],
        "guardias": CONFIG["guardias"],
        "entrega": estado["entrega"], "json_entrega": estado["json_entrega"],
        "forma_entrega": estado["forma_entrega"], "contenido_final": estado["contenido_final"],
        "pregunta_usuario": estado["pregunta_usuario"], "corte": estado["corte"],
        "cerrado": estado["cerrado"], "turnos": estado["turnos"], "llamadas": estado["llamadas"],
        "casos_leidos": estado["casos_leidos"],
        "cuerpos": estado["cuerpos"], "respuestas": estado["respuestas"],
        "mensajes_finales": estado["mensajes"], "recorrido": recorrido(estado["mensajes"]),
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    lineas = [f"# Consulta (scratch) · sol · pregunta {numero}", "",
              f"**Modelo:** {CONFIG['modelo']['alias']} `{CONFIG['modelo']['esfuerzo']}` · "
              f"turnos {estado['turnos']} · llamadas {estado['llamadas']} · "
              f"corte {estado['corte'] or 'ninguno'}", "",
              f"**Pregunta:** {pregunta}", "",
              f"**Casos leídos:** {', '.join(estado['casos_leidos']) or 'ninguno'}", ""]
    if isinstance(estado["entrega"], dict):
        lineas += [f"**Desenlace:** {estado['entrega'].get('desenlace')} "
                   f"({estado['forma_entrega']})", "",
                   "## Respuesta", "", estado["entrega"].get("respuesta") or "(vacía)", ""]
    elif estado.get("pregunta_usuario"):
        pregunta_usuario = estado["pregunta_usuario"]
        lineas += ["**Preguntó al usuario:**", "", pregunta_usuario.get("pregunta") or "", ""]
        lineas += [f"- {opcion}" for opcion in pregunta_usuario.get("opciones") or []]
    elif estado.get("contenido_final"):
        lineas += ["## Mensaje final (sin JSON)", "", estado["contenido_final"], ""]
    else:
        lineas += [f"**Sin entrega:** la corrida se cortó por {estado['corte']}", ""]
    lineas += ["## Recorrido", ""]
    for paso in recorrido(estado["mensajes"]):
        if "pidio" in paso:
            for llamada in paso["pidio"]:
                lineas.append(f"- pidió `{llamada['herramienta']}` {llamada['argumentos']}")
        else:
            lineas.append(f"- volvió: `{paso['volvio']}`")
    salida.write_text("\n".join(lineas) + "\n", encoding="utf-8")

    print(f"turnos {estado['turnos']} · llamadas {estado['llamadas']} · "
          f"corte {estado['corte'] or 'ninguno'} · "
          f"casos leídos {', '.join(estado['casos_leidos']) or 'ninguno'}")
    print("recorrido:")
    for paso in recorrido(estado["mensajes"]):
        if "pidio" in paso:
            for llamada in paso["pidio"]:
                print(f"  pidió {llamada['herramienta']} {llamada['argumentos']}")
        else:
            print(f"  volvió: {paso['volvio'][:200]}")
    print()
    if isinstance(estado["entrega"], dict):
        print(f"desenlace: {estado['entrega'].get('desenlace')} ({estado['forma_entrega']})")
        print(f"respuesta: {estado['entrega'].get('respuesta') or '(vacía)'}")
    elif estado.get("pregunta_usuario"):
        print(f"preguntó al usuario: {estado['pregunta_usuario'].get('pregunta')}")
    elif estado.get("contenido_final"):
        print(f"mensaje final (sin JSON): {estado['contenido_final']}")
    else:
        print(f"sin entrega: se cortó por {estado['corte']}")
    print(f"\ncrudo: {crudo.relative_to(RAIZ)}\nsalida: {salida.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
