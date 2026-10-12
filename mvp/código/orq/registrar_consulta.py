#!/usr/bin/env python3
"""Registra la consulta en la base: la corrida del acto y la respuesta.

Es el último paso, y escribe **al terminar**, en una sola transacción:

- la fila de la **corrida**, con su **token**: modelo, esfuerzo, la **plantilla y su versión**,
  el hash de R, los **relojes que entraron al prompt**, los tokens (la suma de los turnos), los
  segundos, los turnos y las llamadas, el `iniciado` y el `terminado`, y el estado
  (`exitoso`/`fallido`) con su motivo;
- la fila de la **consulta**: el dominio, los documentos ofrecidos, la pregunta y su texto, el
  desenlace y la respuesta;
- los **casos leídos**, que es lo que permite la traza: de la respuesta a la unidad y a sus datos.

Los desenlaces son los de siempre: el JSON leído (`respondida`), la pregunta al usuario (el ciclo
termina ahí), el mensaje sin JSON, el corte por guardia y el silencio. **Un corte se registra como
fallido** —con su motivo— porque la corrida no llegó a responder; lo demás, como exitoso.

Con `error` —la llamada no se pudo completar y el bucle se cortó ahí— la corrida queda **fallida**
con ese motivo y la consulta sin desenlace ni respuesta: el expediente guarda que la pregunta se
intentó y no se pudo.

Nada se escribe en archivos: `mvp/temp/` no se toca.
"""

import pathlib
import sys
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from base import conectar, hash_de, registrar_corrida  # noqa: E402
from esquema import PREFIJO_CORPUS, token_siguiente  # noqa: E402
from proveedores import resolver  # noqa: E402
from relojes import reloj_radicados, reloj_sistema_de  # noqa: E402


def registrar_consulta(config, corrida, error=None):
    """Escribe la corrida y su consulta. Devuelve el token de la corrida."""
    consulta_id = f"q{corrida['pregunta_id']}"
    estado = corrida.get("estado")
    respuestas = (estado or {}).get("respuestas") or []
    usos = [(respuesta.get("usage") or {}) for respuesta in respuestas]
    desenlace, respuesta, resultado, motivo = None, None, "exitoso", None

    if error is not None:
        resultado, motivo = "fallido", error
    else:
        entrega = estado["entrega"]
        if isinstance(entrega, dict):
            desenlace = entrega.get("desenlace")
            respuesta = (entrega.get("respuesta") or "").strip() or None
        elif estado.get("pregunta_usuario"):
            pregunta = estado["pregunta_usuario"]
            desenlace = "preguntó al usuario"
            opciones = "\n".join(f"- {opcion}" for opcion in pregunta.get("opciones") or [])
            respuesta = f"{pregunta.get('pregunta') or ''}\n{opciones}".strip() or None
        elif estado.get("contenido_final"):
            resultado, motivo = "fallido", "sin JSON"
            respuesta = estado["contenido_final"].strip()
        elif estado.get("corte"):
            resultado, motivo = "fallido", f"cortada por {estado['corte']}"
        else:
            resultado, motivo = "fallido", "el agente no contestó"

    modelo = resolver(config["modelo"]["alias"], config["modelo"].get("esfuerzo"))
    prompt = corrida["prompt"]
    db = conectar()
    token = token_siguiente(db, PREFIJO_CORPUS)
    registrar_corrida(
        db, id=token, paso="ORQ",
        dominio=corrida["dominio"],
        pregunta_id=corrida["pregunta_id"], pregunta_texto=corrida["pregunta"],
        prompt_id=prompt["id"], prompt_version=prompt["version"], hash_prompt=prompt["sello"],
        hash_r=hash_de(config["rutas"]["r"]),
        modelo=modelo["id"], esfuerzo=modelo.get("esfuerzo"),
        reloj_radicado=reloj_radicados(corrida["documentos"]),
        reloj_sistema=reloj_sistema_de(corrida["anclas"]),
        tokens_entrada=sum((uso.get("prompt_tokens") or 0) for uso in usos),
        tokens_salida=sum((uso.get("completion_tokens") or 0) for uso in usos),
        tokens_pensando=sum((uso.get("thinking_tokens") or 0) for uso in usos),
        cache_hit=sum((uso.get("prompt_cache_hit_tokens") or 0) for uso in usos),
        segundos=round(sum((respuesta_api.get("_segundos") or 0) for respuesta_api in respuestas), 1),
        turnos=(estado or {}).get("turnos"), llamadas=(estado or {}).get("llamadas"),
        estado=resultado, motivo=motivo,
        iniciado=corrida.get("iniciado"),
        terminado=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    db.execute("INSERT INTO consultas (id, corrida_id, dominio, documentos, pregunta_texto, "
               "desenlace, respuesta) VALUES (?,?,?,?,?,?,?) "
               "ON CONFLICT(id) DO UPDATE SET corrida_id=excluded.corrida_id, "
               "dominio=excluded.dominio, documentos=excluded.documentos, "
               "pregunta_texto=excluded.pregunta_texto, desenlace=excluded.desenlace, "
               "respuesta=excluded.respuesta, fecha=datetime('now','localtime')",
               (consulta_id, token, corrida["dominio"],
                ",".join(documento["id"] for documento in corrida["documentos"]),
                corrida["pregunta"], desenlace, respuesta))
    db.execute("DELETE FROM consulta_casos WHERE consulta_id = ?", (consulta_id,))
    for unidad_id in ((estado or {}).get("casos_leidos") or []):
        db.execute("INSERT OR IGNORE INTO consulta_casos (consulta_id, unidad_id) VALUES (?,?)",
                   (consulta_id, unidad_id))
    db.execute("DELETE FROM consulta_llamadas WHERE consulta_id = ?", (consulta_id,))
    for llamada in ((estado or {}).get("llamadas_detalle") or []):
        db.execute("INSERT INTO consulta_llamadas (consulta_id, turno, orden, herramienta, "
                   "argumentos, ok, error) VALUES (?,?,?,?,?,?,?)",
                   (consulta_id, llamada.get("turno"), llamada.get("orden"),
                    llamada.get("herramienta"), llamada.get("argumentos"),
                    llamada.get("ok"), llamada.get("error")))
    db.commit()
    return token
