#!/usr/bin/env python3
"""Lee la configuración del orquestador y resuelve las rutas.

Las rutas de `config.json` son **relativas a la carpeta de este archivo** (`orq/`), así que la
configuración se puede mover con el código.

Qué hay en la configuración:

    rutas.*                  dónde está cada archivo, de entrada y de salida
    preguntas.desde_archivo  si la pregunta se lee del archivo (la otra vía, todavía no)
    preguntas.cual           qué pregunta del archivo, si no se pasa por consola
    dominio                  el dominio elegido para esta consulta (entrada, no se infiere)
    modelo.alias/.esfuerzo   qué proveedor del registro del MVP se usa, y con qué esfuerzo
    guardias.*               topes del bucle: no son R, son guardias del orquestador
    entrega.forma            cómo lee el ORQ la entrega; hoy, solo "json_en_mensaje_final"
    etiqueta                 nombre base del crudo de la corrida
"""

import json
import pathlib

AQUI = pathlib.Path(__file__).resolve().parent


def leer_config(ruta=None):
    """Devuelve la configuración, con las rutas resueltas a rutas absolutas."""
    ruta = pathlib.Path(ruta).resolve() if ruta else AQUI / "config.json"
    config = json.loads(ruta.read_text(encoding="utf-8"))
    config["rutas"] = {clave: (AQUI / valor).resolve()
                       for clave, valor in config["rutas"].items()}
    config["_config"] = str(ruta)
    forma = (config.get("entrega") or {}).get("forma")
    if forma != "json_en_mensaje_final":
        raise SystemExit(f"la forma de entrega '{forma}' no la sabe leer este orquestador: "
                         "solo 'json_en_mensaje_final'")
    return config
