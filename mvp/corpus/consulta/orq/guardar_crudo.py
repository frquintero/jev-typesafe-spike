#!/usr/bin/env python3
"""Guarda el crudo de la corrida: los cuerpos enviados y las respuestas, sin cabeceras.

No se sobrescribe: si la etiqueta ya existe, agrega un `rN` nuevo —la misma regla que los crudos
del resto del repo—. Los cuerpos vienen copiados desde el bucle, porque `messages` es una lista
que sigue creciendo: sin copia, todos los turnos mostrarían el historial final.
"""

import json


def guardar_crudo(config, corrida):
    """Escribe el crudo y devuelve su ruta."""
    carpeta = config["rutas"]["crudos"]
    carpeta.mkdir(parents=True, exist_ok=True)
    # La etiqueta es una plantilla con el número de pregunta: cada pregunta tiene su crudo.
    etiqueta = config["etiqueta"].format(numero=corrida["numero"])
    numero = 1
    destino = carpeta / f"{etiqueta}-r{numero}.json"
    while destino.exists():
        numero += 1
        destino = carpeta / f"{etiqueta}-r{numero}.json"

    estado = corrida["estado"]
    crudo = {
        "etiqueta": destino.stem,
        "anclas": corrida["anclas"],
        "dominio": config["dominio"],
        "modelo": config["modelo"],
        "guardias": config["guardias"],
        "config": config["_config"],
        "r": corrida["r"],
        "documentos": corrida["documentos"],
        "pregunta": {"numero": corrida["numero"], "texto": corrida["pregunta"]},
        "casos": corrida["casos"],
        "herramientas": corrida["herramientas"],
        "requests": estado["cuerpos"],
        "responses": [
            {"model": respuesta.get("model"),
             "finish_reason": respuesta["choices"][0].get("finish_reason"),
             "message": respuesta["choices"][0]["message"],
             "usage": respuesta.get("usage"),
             "stream_chunks_crudos": respuesta.get("_stream_chunks_crudos")}
            for respuesta in estado["respuestas"]
        ],
        "casos_leidos": estado["casos_leidos"],
        "turnos": estado["turnos"],
        "llamadas": estado["llamadas"],
        "cerrado": estado["cerrado"],
        "entrega": estado["entrega"],
    }
    destino.write_text(json.dumps(crudo, ensure_ascii=False, indent=1), encoding="utf-8")
    return destino
