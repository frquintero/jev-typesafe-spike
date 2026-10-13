#!/usr/bin/env python3
"""El ORQUESTADOR: recibe la pregunta, corre el bucle y registra lo que pasó.

    python3 mvp/código/orq/orquestador.py --texto "…" --dominio E [--modelo M] [--esfuerzo E]
    python3 mvp/código/orq/orquestador.py <archivo> [--numero N] --dominio E

La pregunta **entra por el acto**: se carga de un archivo o del chat —el cargador es
`mvp/código/cargar_pregunta.py`— y **se radica al cerrar, solo si el modelo entregó su JSON**.
Mientras el ciclo corre, la base se abre **en solo lectura**: de esa pregunta no hay nada escrito.
Si el ciclo no entrega, queda la cédula del acto y **ninguna pregunta radicada**.

El orden, y nada más que el orden —cada paso vive en su archivo—:

    1. leer_config          la configuración y las rutas
    2. cargar la pregunta   del archivo o del chat (texto y fuente)
    3. leer_r               R: el JSON que aplica el orquestador (el agente no lo ve)
    4. abrir_db             la base del corpus, en solo lectura
    5. resolver_dominio     el dominio elegido → sus documentos (pertenencia, sin juicio)
    6. listar_casos         los casos del dominio: id, nombre y la tanda de DATOS ofrecida
    7. armar_herramientas   R ∩ las herramientas que existen
    8. anclas + armar_prompt  el system (radicado y lógica) y el user (casos, pregunta, ahora)
    9. bucle                llama, ejecuta y termina con la entrega (sin juzgarla)
   10. registrar_consulta   la corrida y —si hubo entrega— la pregunta y la respuesta

La **plantilla** sale de la base —su última versión inscrita—, y la
consulta **congela** los casos y su tanda de DATOS al abrir: lo que leyó queda en la traza.

Nada se escribe en archivos: `mvp/temp/` no se toca.
"""

import pathlib
import sys
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from abrir_db import abrir_db  # noqa: E402
from ajustes import resolver as resolver_ajuste  # noqa: E402

from anclas import anclas  # noqa: E402
from armar_herramientas import armar_herramientas  # noqa: E402
from armar_prompt import armar_prompt  # noqa: E402
from base import conectar  # noqa: E402
from bucle import bucle  # noqa: E402
from leer_config import leer_config  # noqa: E402
from leer_r import leer_r  # noqa: E402
from listar_casos import listar_casos  # noqa: E402
from prompts import usar as usar_prompt  # noqa: E402
from proveedores import ErrorDeLlamada  # noqa: E402
from cargar_pregunta import cargar, entero  # noqa: E402
from registrar_consulta import registrar_consulta  # noqa: E402
from resolver_dominio import resolver_dominio  # noqa: E402

USO = ("uso: python3 mvp/código/orq/orquestador.py (--texto \"…\" | <archivo> [--numero N]) "
       "--dominio E [--modelo M] [--esfuerzo E]")


def _entrada():
    """La pregunta (texto y fuente) y el dominio, del archivo o del chat."""
    archivo, texto, numero, dominio = None, None, None, None
    modelo, esfuerzo = None, None
    resto = sys.argv[1:]
    while resto:
        opcion = resto.pop(0)
        if opcion in ("--texto", "--dominio", "--numero", "--modelo", "--esfuerzo") and resto:
            valor = resto.pop(0)
            if opcion == "--texto":
                texto = valor
            elif opcion == "--dominio":
                dominio = valor
            elif opcion == "--numero":
                numero = entero(valor, "--numero")
            elif opcion == "--modelo":
                modelo = valor
            else:
                esfuerzo = valor
        elif archivo is None and not opcion.startswith("--"):
            archivo = opcion
        else:
            raise SystemExit(f"no entiendo '{opcion}'. {USO}")
    if dominio is None or not dominio.strip():
        raise SystemExit(f"falta --dominio: la pregunta vive en un dominio (la unidad semántica). {USO}")
    contenido, fuente = cargar(archivo=archivo, texto=texto, numero=numero)
    return contenido, fuente, dominio.strip(), modelo, esfuerzo


def main():
    config = leer_config()
    texto, fuente, dominio, modelo_pedido, esfuerzo_pedido = _entrada()

    r = leer_r(config["rutas"]["r"])
    db = abrir_db(config["rutas"]["corpus"])
    modelo, esfuerzo = resolver_ajuste(db, "ORQ", modelo_pedido, esfuerzo_pedido)
    config["modelo"] = {"alias": modelo, "esfuerzo": esfuerzo}
    documentos = resolver_dominio(db, dominio)
    casos = listar_casos(db, documentos)
    herramientas = armar_herramientas(r)
    marcas = anclas()

    db_prompt = conectar()  # la plantilla vigente se lee de la base
    prompt = usar_prompt(db_prompt, "ORQ")
    db_prompt.close()
    rotulo = f"{prompt['id']} v{prompt['version']}"
    mensajes = armar_prompt(prompt["texto"], rotulo, texto, casos, marcas, documentos)

    print(f"dominio {dominio} · documentos {[d['id'] for d in documentos]} · "
          f"{len(casos)} casos · herramientas {[h['function']['name'] for h in herramientas]}")
    print(f"plantilla {rotulo} · {modelo} ({esfuerzo}) · pregunta ({fuente}): {texto}\n")

    estado = None
    corrida = {"anclas": marcas, "documentos": documentos, "pregunta": texto, "fuente": fuente,
               "dominio": dominio, "casos": casos, "prompt": prompt,
               "iniciado": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
               "herramientas": [h["function"]["name"] for h in herramientas],
               "r": r}
    try:
        estado = bucle(config, mensajes, herramientas, db, casos)
    except ErrorDeLlamada as error:
        # La llamada no se pudo completar: el acto deja su cédula, y no se radica nada.
        db.close()
        token, _ = registrar_consulta(config, corrida, error=str(error))
        print(f"la corrida se cortó: {error}")
        print(f"    -> la base: el acto {token} (sin entrega: no se radicó ninguna pregunta)")
        raise SystemExit(1)
    db.close()

    corrida["estado"] = estado
    token, pregunta_id = registrar_consulta(config, corrida)

    print(f"acto {token} · turnos {estado['turnos']} · llamadas {estado['llamadas']} · "
          f"corte {estado['corte'] or 'ninguno'} · "
          f"casos leídos {', '.join(estado['casos_leidos']) or 'ninguno'}")
    entrega = estado["entrega"]
    if pregunta_id is not None and isinstance(entrega, dict):
        print(f"desenlace: {entrega.get('desenlace')} ({estado['forma_entrega']})")
        print(f"respuesta: {entrega.get('respuesta') or '(sin respuesta)'}")
        print(f"    -> la base: el acto {token} y su consulta q{pregunta_id}")
        return
    if estado.get("pregunta_usuario"):
        print(f"sin entrega: el agente preguntó al usuario — "
              f"{estado['pregunta_usuario'].get('pregunta')}")
    elif estado.get("contenido_final"):
        print(f"sin entrega (sin JSON): {estado['contenido_final']}")
    elif estado.get("corte"):
        print(f"sin entrega: la corrida se cortó por {estado['corte']}")
    else:
        print("sin entrega: el agente no contestó")
    print(f"    -> la base: el acto {token} (sin pregunta radicada)")


if __name__ == "__main__":
    main()
