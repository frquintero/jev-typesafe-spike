#!/usr/bin/env python3
"""El ORQUESTADOR: abre la consulta, corre el bucle y registra lo que pasó.

    python3 orquestador.py [n]

`n` es la pregunta del archivo (1..5). Si no se pasa, se usa `preguntas.cual` de `config.json`.

El orden, y nada más que el orden —cada paso vive en su archivo—:

    1. leer_config          la configuración y las rutas
    2. leer_pregunta        la pregunta, tal cual, del archivo del usuario
    3. leer_r               R: el JSON que aplica el orquestador (el agente no lo ve)
    4. abrir_db             la base del corpus, en solo lectura
    5. resolver_dominio     el dominio elegido → sus documentos (pertenencia, sin juicio)
    6. listar_casos         los casos del dominio: id, nombre y la tanda de DATOS ofrecida
    7. armar_herramientas   R ∩ las herramientas que existen
    8. anclas + armar_prompt  el system (radicado y lógica) y el user (casos, pregunta, ahora)
    9. bucle                llama, ejecuta y termina con la entrega (sin juzgarla)
   10. registrar_consulta   la corrida y la respuesta, en la base (al terminar)

La **plantilla** sale de la base —el `.md` es la puerta y se registra sola la primera vez—, y la
consulta **congela** los casos y su tanda de DATOS al abrir: lo que leyó queda en la traza.

Nada se escribe en archivos: `mvp/temp/` no se toca.
"""

import pathlib
import sys
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from abrir_db import abrir_db  # noqa: E402
from anclas import anclas  # noqa: E402
from armar_herramientas import armar_herramientas  # noqa: E402
from armar_prompt import armar_prompt  # noqa: E402
from base import conectar  # noqa: E402
from bucle import bucle  # noqa: E402
from leer_config import leer_config  # noqa: E402
from leer_pregunta import leer_pregunta  # noqa: E402
from leer_r import leer_r  # noqa: E402
from listar_casos import listar_casos  # noqa: E402
from prompts import usar as usar_prompt  # noqa: E402
from proveedores import ErrorDeLlamada  # noqa: E402
from registrar_consulta import registrar_consulta  # noqa: E402
from resolver_dominio import resolver_dominio  # noqa: E402


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

    db_prompt = conectar()  # la plantilla se registra sola, la primera vez que corre
    prompt = usar_prompt(db_prompt, "ORQ", config["rutas"]["prompt"])
    db_prompt.close()
    rotulo = f"{prompt['id']} v{prompt['version']}"
    mensajes = armar_prompt(prompt["texto"], rotulo, pregunta, casos, marcas, documentos)

    print(f"dominio {config['dominio']} · documentos {[d['id'] for d in documentos]} · "
          f"{len(casos)} casos · herramientas {[h['function']['name'] for h in herramientas]}")
    print(f"plantilla {rotulo} · pregunta {numero}: {pregunta}\n")

    estado = None
    corrida = {"anclas": marcas, "documentos": documentos, "pregunta": pregunta,
               "numero": numero, "casos": casos, "prompt": prompt,
               "iniciado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "herramientas": [h["function"]["name"] for h in herramientas],
               "r": r}
    try:
        estado = bucle(config, mensajes, herramientas, db, casos)
    except ErrorDeLlamada as error:
        # La llamada no se pudo completar: la corrida se registra fallida, con su motivo.
        db.close()
        token = registrar_consulta(config, corrida, error=str(error))
        print(f"la corrida se cortó: {error}")
        print(f"    -> la base: el acto {token} y su consulta (fallida)")
        raise SystemExit(1)
    db.close()

    corrida["estado"] = estado
    token = registrar_consulta(config, corrida)

    print(f"acto {token} · turnos {estado['turnos']} · llamadas {estado['llamadas']} · "
          f"corte {estado['corte'] or 'ninguno'} · "
          f"casos leídos {', '.join(estado['casos_leidos']) or 'ninguno'}")
    entrega = estado["entrega"]
    if isinstance(entrega, dict):
        print(f"desenlace: {entrega.get('desenlace')} ({estado['forma_entrega']})")
        print(f"respuesta: {entrega.get('respuesta') or '(sin respuesta)'}")
    elif estado.get("pregunta_usuario"):
        pregunta_usuario = estado["pregunta_usuario"]
        print(f"pregunta al usuario: {pregunta_usuario.get('pregunta')}")
        for opcion in pregunta_usuario.get("opciones") or []:
            print(f"  - {opcion}")
    elif estado.get("contenido_final"):
        print(f"respuesta (sin JSON): {estado['contenido_final']}")
    elif estado.get("corte"):
        print(f"sin entrega: la corrida se cortó por {estado['corte']}")
    else:
        print("sin respuesta: el agente no contestó")
    print(f"    -> la base: el acto {token} y su consulta")


if __name__ == "__main__":
    main()
