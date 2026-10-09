#!/usr/bin/env python3
"""Registra la consulta en la base: la corrida del ORQ y la respuesta.

Es el último paso, y escribe **al terminar**, en una sola transacción:

- la fila de la **corrida**: modelo, esfuerzo, el prompt del agente y su hash, el hash de R, los
  tokens (la suma de los turnos), los segundos, los turnos y las llamadas, y el estado
  (`exitoso`/`fallido`) con su motivo;
- la fila de la **consulta**: el dominio, los documentos ofrecidos, la pregunta y su texto, el
  desenlace y la respuesta;
- los **casos leídos**, que es lo que permite la traza: de la respuesta a la unidad y al dato.

Los desenlaces son los de siempre: el JSON leído (`respondida`), la pregunta al usuario (el ciclo
termina ahí), el mensaje sin JSON, el corte por guardia y el silencio. **Un corte se registra como
fallido** —con su motivo— porque la corrida no llegó a responder; lo demás, como exitoso.

Con `error` —la llamada no se pudo completar y el bucle se cortó ahí— la corrida queda **fallida**
con ese motivo y la consulta sin desenlace ni respuesta: el expediente guarda que la pregunta se
intentó y no se pudo.

Nada se escribe en archivos: `mvp/temp/` no se toca.
"""

import pathlib

from base import conectar, hash_de, registrar_corrida
from proveedores import resolver


def documento_de_la_bateria(bateria):
    """El documento del que es la batería: `preguntas_doc8.md` → `doc8`."""
    nombre = pathlib.Path(bateria).stem
    return nombre[len("preguntas_"):] if nombre.startswith("preguntas_") else nombre


def registrar_consulta(config, corrida, error=None):
    """Escribe la corrida y su respuesta. Devuelve el id de las dos."""
    identificador = f"{documento_de_la_bateria(config['rutas']['preguntas'])}:q{corrida['numero']}"
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
    db = conectar()
    registrar_corrida(
        db, id=identificador, paso="ORQ",
        dominio=config["dominio"],
        bateria=pathlib.Path(config["rutas"]["preguntas"]).name,
        pregunta_numero=corrida["numero"], pregunta_texto=corrida["pregunta"],
        prompt=pathlib.Path(config["rutas"]["prompt"]).name,
        hash_prompt=hash_de(config["rutas"]["prompt"]), hash_r=hash_de(config["rutas"]["r"]),
        modelo=modelo["id"], esfuerzo=modelo.get("esfuerzo"),
        tokens_entrada=sum((uso.get("prompt_tokens") or 0) for uso in usos),
        tokens_salida=sum((uso.get("completion_tokens") or 0) for uso in usos),
        tokens_pensando=sum((uso.get("thinking_tokens") or 0) for uso in usos),
        cache_hit=sum((uso.get("prompt_cache_hit_tokens") or 0) for uso in usos),
        segundos=round(sum((respuesta_api.get("_segundos") or 0) for respuesta_api in respuestas), 1),
        turnos=(estado or {}).get("turnos"), llamadas=(estado or {}).get("llamadas"),
        estado=resultado, motivo=motivo)
    db.execute("INSERT INTO consultas (id, corrida_id, dominio, documentos, pregunta_texto, "
               "desenlace, respuesta) VALUES (?,?,?,?,?,?,?) "
               "ON CONFLICT(id) DO UPDATE SET corrida_id=excluded.corrida_id, "
               "dominio=excluded.dominio, documentos=excluded.documentos, "
               "pregunta_texto=excluded.pregunta_texto, desenlace=excluded.desenlace, "
               "respuesta=excluded.respuesta, fecha=datetime('now','localtime')",
               (identificador, identificador, config["dominio"],
                ",".join(documento["id"] for documento in corrida["documentos"]),
                corrida["pregunta"], desenlace, respuesta))
    db.execute("DELETE FROM consulta_casos WHERE consulta_id = ?", (identificador,))
    for unidad_id in ((estado or {}).get("casos_leidos") or []):
        db.execute("INSERT OR IGNORE INTO consulta_casos (consulta_id, unidad_id) VALUES (?,?)",
                   (identificador, unidad_id))
    db.commit()
    return identificador
