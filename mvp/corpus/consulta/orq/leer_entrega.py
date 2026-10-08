#!/usr/bin/env python3
"""Lee la entrega: el JSON de RESPUESTA_JSON, donde el prompt del agente lo ponga.

El prompt del agente (`mvp/prompts/prompt_ORQ.md`, congelado) pide, **en el mismo mensaje
final**: la respuesta corta de la tarea 5 y, en la tarea 6, «diligencia el JSON en
RESPUESTA_JSON». Así, el JSON puede venir de cuatro formas, todas legítimas:

    - solo, como todo el mensaje;
    - dentro de una cerca de código (```json … ```);
    - detrás de la etiqueta `RESPUESTA_JSON:`;
    - después de la prosa, al final del mensaje.

Este módulo lo ubica. **No juzga**: devuelve el objeto tal como vino, o nada. La lectura es
mecánica: escanea los tramos `{…}` balanceados —respetando las llaves dentro de las
cadenas— y se queda con el que sigue a la etiqueta; si no hay etiqueta, con el último que
traiga un `desenlace` de los dos estados de prompt 3; y si ninguno lo trae, con el último que
sea un objeto JSON.
"""

import json

ETIQUETA = "RESPUESTA_JSON"
# El valor viejo (`no_esta_en_el_corpus`) se sigue aceptando: los crudos de prompt 3 lo traen.
ESTADOS = ("respondida", "no_esta_en_los_datos", "no_esta_en_el_corpus")


def _tramos(texto):
    """Devuelve los tramos `{…}` balanceados del texto, de izquierda a derecha."""
    tramos = []
    profundidad = 0
    inicio = None
    en_cadena = False
    escape = False
    for posicion, caracter in enumerate(texto):
        if en_cadena:
            if escape:
                escape = False
            elif caracter == "\\":
                escape = True
            elif caracter == '"':
                en_cadena = False
            continue
        if caracter == '"':
            en_cadena = True
        elif caracter == "{":
            if profundidad == 0:
                inicio = posicion
            profundidad += 1
        elif caracter == "}":
            if profundidad:
                profundidad -= 1
                if profundidad == 0 and inicio is not None:
                    tramos.append(texto[inicio:posicion + 1])
                    inicio = None
    return tramos


def _objeto(tramo):
    """Devuelve el objeto si el tramo es JSON y es un objeto; si no, None."""
    try:
        objeto = json.loads(tramo)
    except json.JSONDecodeError:
        return None
    return objeto if isinstance(objeto, dict) else None


def extraer_entrega(contenido):
    """Devuelve (entrega, json_crudo, forma); (None, None, None) si no hay JSON.

    `forma` dice de dónde salió: `todo_el_mensaje` o `dentro_del_mensaje`.
    """
    texto = (contenido or "").strip()
    if not texto:
        return None, None, None

    # 1. El mensaje entero es el JSON (el caso limpio).
    objeto = _objeto(texto)
    if objeto is not None:
        return objeto, texto, "todo_el_mensaje"

    # 2. Detrás de la etiqueta RESPUESTA_JSON: el primer objeto que siga.
    etiqueta = texto.rfind(ETIQUETA)
    if etiqueta != -1:
        for tramo in _tramos(texto[etiqueta:]):
            objeto = _objeto(tramo)
            if objeto is not None:
                return objeto, tramo, "dentro_del_mensaje"

    # 3. El último objeto con un desenlace de prompt 3.
    for tramo in reversed(_tramos(texto)):
        objeto = _objeto(tramo)
        if objeto is not None and objeto.get("desenlace") in ESTADOS:
            return objeto, tramo, "dentro_del_mensaje"

    # 4. El último objeto, aunque no traiga desenlace conocido. No se juzga: se registra.
    for tramo in reversed(_tramos(texto)):
        objeto = _objeto(tramo)
        if objeto is not None:
            return objeto, tramo, "dentro_del_mensaje"

    return None, None, None
