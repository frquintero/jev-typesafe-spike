#!/usr/bin/env python3
"""El ORQUESTADOR: abre la consulta, corre el bucle y entrega.

    python3 orquestador.py [n]

`n` es la pregunta del archivo (1..5). Si no se pasa, se usa `preguntas.cual` de `config.json`.

El orden, y nada más que el orden —cada paso vive en su archivo—:

    1. leer_config          la configuración y las rutas
    2. leer_pregunta        la pregunta, tal cual, del archivo del usuario
    3. leer_r               R: el JSON que aplica el orquestador (el agente no lo ve)
    4. abrir_db             la base del corpus, en solo lectura
    5. resolver_dominio     el dominio elegido → sus documentos (pertenencia, sin juicio)
    6. listar_casos         los casos del dominio: id y nombre, sin aspectos ni valores
    7. armar_herramientas   R ∩ las herramientas que existen
    8. anclas + armar_prompt  el system con el prompt y la pregunta
    9. bucle                llama, ejecuta y termina con la entrega (sin juzgarla)
   10. guardar_crudo · registrar_traza · escribir_salida
"""

import pathlib
import sys

from abrir_db import abrir_db
from anclas import anclas
from armar_herramientas import armar_herramientas
from armar_prompt import armar_prompt
from bucle import bucle
from escribir_salida import escribir_salida
from guardar_crudo import guardar_crudo
from leer_config import leer_config
from leer_pregunta import leer_pregunta
from leer_r import leer_r
from listar_casos import listar_casos
from registrar_traza import registrar_traza
from resolver_dominio import resolver_dominio

RAIZ = pathlib.Path(__file__).resolve().parents[4]


def main():
    config = leer_config()
    if not config["preguntas"]["desde_archivo"]:
        raise SystemExit("preguntas.desde_archivo está en false y no hay otra entrada todavía")
    numero = int(sys.argv[1]) if len(sys.argv) > 1 else config["preguntas"]["cual"]

    pregunta = leer_pregunta(config["rutas"]["preguntas"], numero)
    r = leer_r(config["rutas"]["r"])
    db = abrir_db(config["rutas"]["corpus"])
    documentos = resolver_dominio(db, config["dominio"])
    casos = listar_casos(db, documentos)
    herramientas = armar_herramientas(r)
    marcas = anclas()
    mensajes = armar_prompt(config["rutas"]["prompt"], pregunta, casos, marcas)

    print(f"dominio {config['dominio']} · documentos {[d['id'] for d in documentos]} · "
          f"{len(casos)} casos · herramientas {[h['function']['name'] for h in herramientas]}")
    print(f"pregunta {numero}: {pregunta}\n")

    estado = bucle(config, mensajes, herramientas, db, casos)
    corrida = {"anclas": marcas, "documentos": documentos, "pregunta": pregunta,
               "numero": numero, "casos": casos,
               "herramientas": [h["function"]["name"] for h in herramientas],
               "r": r, "estado": estado}
    ruta_crudo = guardar_crudo(config, corrida)
    ruta_salida = escribir_salida(config, corrida, ruta_crudo)
    ruta_traza = registrar_traza(config, corrida, ruta_crudo)

    print(f"turnos {estado['turnos']} · llamadas {estado['llamadas']} · "
          f"corte {estado['corte'] or 'ninguno'} · "
          f"casos leídos {', '.join(estado['casos_leidos']) or 'ninguno'}")
    if isinstance(estado["entrega"], dict):
        print(f"desenlace: {estado['entrega'].get('desenlace')} "
              f"({estado['forma_entrega']})")
        print(f"respuesta: {estado['entrega'].get('respuesta') or '(sin respuesta)'}")
    elif estado.get("pregunta_usuario"):
        pregunta = estado["pregunta_usuario"]
        print(f"pregunta al usuario: {pregunta.get('pregunta')}")
        for opcion in pregunta.get("opciones") or []:
            print(f"  - {opcion}")
    elif estado.get("contenido_final"):
        print(f"respuesta (sin JSON): {estado['contenido_final']}")
    elif estado.get("corte"):
        print(f"sin entrega: la corrida se cortó por {estado['corte']}")
    else:
        print("sin respuesta: el agente no contestó")
    for etiqueta, ruta in (("crudo", ruta_crudo), ("traza", ruta_traza), ("salida", ruta_salida)):
        print(f"{etiqueta}: {ruta.relative_to(RAIZ)}")


if __name__ == "__main__":
    main()
