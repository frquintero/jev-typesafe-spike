#!/usr/bin/env python3
"""Registra el acto de la consulta: la corrida, y —si hubo entrega— la pregunta y su respuesta.

La regla es una sola: **nada se radica hasta que el modelo entrega su JSON**. El ciclo corre sin
tocar la base (la abre en solo lectura); al cerrar:

- **con entrega** —el JSON de `RESPUESTA_JSON`, un objeto con un `desenlace` de los dos estados—
  escribe, en una sola transacción, la fila de **`preguntas`** (su texto, su dominio y su fuente,
  con la fecha y la hora del cierre), la **corrida** y la **consulta**, con sus casos leídos y sus
  llamadas;
- **sin entrega** —prosa sin JSON, pregunta al usuario, corte por guardia o error de la API—
  escribe **solo la cédula**: la corrida `fallido`, con su `motivo`, el texto en `pregunta_texto` y
  `pregunta_id` **nulo** (el molde de `volcados.documento_id`). No hay pregunta radicada, ni
  consulta, ni casos, ni llamadas.

Un `{…}` sin `desenlace` **no es entrega**: el lector lo devuelve igual —«no se juzga: se registra»—
pero radicar es otra cosa, y no radica.

Nada se escribe en archivos: `mvp/temp/` no se toca.
"""

import pathlib
import sys
from datetime import datetime

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))

from base import conectar, hash_de, registrar_corrida  # noqa: E402
from esquema import PREFIJO_CORPUS, token_siguiente  # noqa: E402
from leer_entrega import ESTADOS  # noqa: E402
from proveedores import resolver  # noqa: E402
from relojes import reloj_radicados, reloj_sistema_de  # noqa: E402

EXTRACTO = 100  # caracteres de la cabeza y de la cola que se guardan de una respuesta ilegible


def extracto(contenido):
    """Lo que se guarda de una respuesta ilegible: la cabeza y la cola, para diagnosticar."""
    limpio = (contenido or "").strip()
    if len(limpio) <= EXTRACTO * 2:
        return limpio
    return f"{limpio[:EXTRACTO]} … {limpio[-EXTRACTO:]}"


def entrega_de(estado):
    """La entrega del ciclo: el JSON de `RESPUESTA_JSON`, o `None`.

    Es la entrega si es un objeto con un `desenlace` de los dos estados. Cualquier otro `{…}`
    —y la prosa, el silencio o el corte— no lo es.
    """
    entrega = (estado or {}).get("entrega")
    if not isinstance(entrega, dict) or entrega.get("desenlace") not in ESTADOS:
        return None
    return entrega


def _cierre(estado, error):
    """Cómo terminó el ciclo: `(estado, motivo, entrega)`."""
    entrega = None if error is not None else entrega_de(estado)
    if error is not None:
        return "fallido", error, None
    if entrega is not None:
        return "exitoso", None, entrega
    if estado.get("pregunta_usuario"):
        return "fallido", "sin JSON: el agente preguntó al usuario", None
    if estado.get("contenido_final"):
        return "fallido", f"sin JSON · respuesta: «{extracto(estado['contenido_final'])}»", None
    if estado.get("corte"):
        return "fallido", f"cortada por {estado['corte']}", None
    return "fallido", "el agente no contestó", None


def registrar_consulta(config, corrida, error=None):
    """Escribe el acto. Devuelve `(token, pregunta_id)`; `pregunta_id` es `None` sin entrega."""
    estado = corrida.get("estado") or {}
    resultado, motivo, entrega = _cierre(estado, error)
    respuestas = estado.get("respuestas") or []
    usos = [(respuesta.get("usage") or {}) for respuesta in respuestas]
    desenlace = respuesta = None
    if entrega is not None:
        desenlace = entrega.get("desenlace")
        respuesta = (entrega.get("respuesta") or "").strip() or None

    modelo = resolver(config["modelo"]["alias"], config["modelo"].get("esfuerzo"))
    prompt = corrida["prompt"]
    db = conectar()
    try:
        token = token_siguiente(db, PREFIJO_CORPUS)
        pregunta_id = None
        if resultado == "exitoso":
            # La radicación es el cierre: la pregunta existe porque hubo entrega.
            db.execute("INSERT INTO preguntas (dominio, texto, fuente) VALUES (?,?,?)",
                       (corrida["dominio"], corrida["pregunta"], corrida["fuente"]))
            pregunta_id = db.execute("SELECT last_insert_rowid()").fetchone()[0]
        registrar_corrida(
            db, id=token, paso="ORQ",
            dominio=corrida["dominio"],
            pregunta_id=pregunta_id, pregunta_texto=corrida["pregunta"],
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
            turnos=estado.get("turnos"), llamadas=estado.get("llamadas"),
            estado=resultado, motivo=motivo,
            iniciado=corrida.get("iniciado"),
            terminado=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        if pregunta_id is not None:
            consulta_id = f"q{pregunta_id}"
            db.execute("INSERT INTO consultas (id, corrida_id, dominio, documentos, pregunta_texto, "
                       "desenlace, respuesta) VALUES (?,?,?,?,?,?,?)",
                       (consulta_id, token, corrida["dominio"],
                        ",".join(documento["id"] for documento in corrida["documentos"]),
                        corrida["pregunta"], desenlace, respuesta))
            for unidad_id in estado.get("casos_leidos") or []:
                db.execute("INSERT OR IGNORE INTO consulta_casos (consulta_id, unidad_id) "
                           "VALUES (?,?)", (consulta_id, unidad_id))
            for llamada in estado.get("llamadas_detalle") or []:
                db.execute("INSERT INTO consulta_llamadas (consulta_id, turno, orden, herramienta, "
                           "argumentos, ok, error) VALUES (?,?,?,?,?,?,?)",
                           (consulta_id, llamada.get("turno"), llamada.get("orden"),
                            llamada.get("herramienta"), llamada.get("argumentos"),
                            llamada.get("ok"), llamada.get("error")))
        db.commit()
    finally:
        db.close()
    return token, pregunta_id
