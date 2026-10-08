#!/usr/bin/env python3
"""Registra el recorrido de la consulta: una línea JSON por corrida, append-only.

La traza **no es corpus**: es el expediente. Deja constancia de qué se preguntó, con qué dominio
y qué documentos, qué casos se leyeron, qué rechazó el código, cómo terminó —el desenlace o el
corte por guardia—, cuánto costó y dónde quedó el crudo.
"""

import json


def registrar_traza(config, corrida, ruta_crudo):
    """Agrega una línea a la traza y devuelve su ruta."""
    estado = corrida["estado"]
    usos = [(respuesta.get("usage") or {}) for respuesta in estado["respuestas"]]
    entrega = estado["entrega"]
    linea = {
        "anclas": corrida["anclas"],
        "pregunta": {"numero": corrida["numero"], "texto": corrida["pregunta"]},
        "dominio": config["dominio"],
        "documentos": [documento["id"] for documento in corrida["documentos"]],
        "casos": len(corrida["casos"]),
        "casos_leidos": estado["casos_leidos"],
        "herramientas": corrida["herramientas"],
        "turnos": estado["turnos"],
        "llamadas": estado["llamadas"],
        "desenlace": entrega.get("desenlace") if isinstance(entrega, dict) else None,
        "cerrado": estado["cerrado"],
        "corte": estado.get("corte"),
        "forma_entrega": estado.get("forma_entrega"),
        "uso": [{"prompt": uso.get("prompt_tokens"),
                 "hit": uso.get("prompt_cache_hit_tokens"),
                 "miss": uso.get("prompt_cache_miss_tokens"),
                 "completion": uso.get("completion_tokens")} for uso in usos],
        "crudo": str(ruta_crudo),
    }
    ruta = config["rutas"]["traza"]
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("a", encoding="utf-8") as archivo:
        archivo.write(json.dumps(linea, ensure_ascii=False) + "\n")
    return ruta
