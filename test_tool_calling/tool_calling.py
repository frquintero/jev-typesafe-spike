#!/usr/bin/env python3
"""Prueba de configuración y operación de tools (DeepSeek v4.1, `deepseek-flash`).

Tres herramientas aritméticas —sumar, restar y multiplicar—, cada una con
cualquier cantidad de números. El system prompt vive en `system_prompt.md`; las
definiciones de las herramientas van en el campo `tools` de la petición (ahí las
recibe la API, no en el texto del system). El usuario dice por consola la
operación y los números.

El bucle lo lleva este guion: llama, ejecuta la herramienta, devuelve el
resultado con su `tool_call_id` y vuelve a llamar hasta que el modelo conteste
sin llamadas. En cada turno se reenvía todo el historial, porque la API de
DeepSeek es stateless; lo que abarata el reenvío es el caché de prefijo.

Las llamadas pasan por `call_model` (`niveles/run_niveles.py`), que lee la clave
del entorno; este guion no lee claves. El crudo de cada corrida queda en
`test_tool_calling/cache/` (cuerpos enviados y respuestas, sin cabeceras).

Uso (la clave vive en el `~/.bashrc` y los shells no interactivos no la cargan):

    bash -ic 'python3 test_tool_calling/tool_calling.py'
"""

import json
import pathlib
import sys
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "niveles"))
from run_niveles import call_model  # noqa: E402

AQUI = pathlib.Path(__file__).resolve().parent
CACHE = AQUI / "cache"
VERSION, ALIAS = "v2", "deepseek"  # v2/deepseek = deepseek-flash, con razonamiento
MAX_TURNOS = 6

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "sumar",
            "description": "Suma todos los números que recibe. Acepta cualquier cantidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numeros": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Los números a sumar, en el orden en que aparecen.",
                    }
                },
                "required": ["numeros"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "restar",
            "description": "Resta al primer número todos los demás, en orden. Acepta cualquier cantidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numeros": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "El minuendo primero y después los sustraendos, en orden.",
                    }
                },
                "required": ["numeros"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "multiplicar",
            "description": "Multiplica entre sí todos los números que recibe. Acepta cualquier cantidad.",
            "parameters": {
                "type": "object",
                "properties": {
                    "numeros": {
                        "type": "array",
                        "items": {"type": "number"},
                        "description": "Los factores, en el orden en que aparecen.",
                    }
                },
                "required": ["numeros"],
                "additionalProperties": False,
            },
        },
    },
]


def sumar(numeros):
    return sum(numeros)


def restar(numeros):
    total = numeros[0]
    for n in numeros[1:]:
        total -= n
    return total


def multiplicar(numeros):
    total = 1
    for n in numeros:
        total *= n
    return total


FUNCIONES = {"sumar": sumar, "restar": restar, "multiplicar": multiplicar}


def ejecutar(nombre, argumentos_crudos):
    """Ejecuta la herramienta pedida. Devuelve (texto para el modelo, ok)."""
    if nombre not in FUNCIONES:
        return json.dumps({"error": f"herramienta desconocida: {nombre}"}, ensure_ascii=False), False
    try:
        argumentos = json.loads(argumentos_crudos or "{}")
    except json.JSONDecodeError as error:
        return json.dumps({"error": f"los argumentos no son JSON válido: {error}"},
                          ensure_ascii=False), False
    numeros = argumentos.get("numeros")
    if not isinstance(numeros, list) or not numeros:
        return json.dumps({"error": "falta 'numeros': tiene que ser una lista no vacía"},
                          ensure_ascii=False), False
    try:
        resultado = FUNCIONES[nombre](numeros)
    except Exception as error:  # noqa: BLE001
        return json.dumps({"error": str(error)}, ensure_ascii=False), False
    return json.dumps({"resultado": resultado}, ensure_ascii=False), True


def leer_entrada():
    print("Operación (sumar | restar | multiplicar): ", end="")
    operacion = input().strip()
    print("Números (separados por espacio o coma): ", end="")
    crudo = input().strip()
    numeros = [t for t in crudo.replace(",", " ").split() if t]
    return operacion, numeros


def guardar_crudo(pregunta, cuerpos, respuestas):
    CACHE.mkdir(exist_ok=True)
    marca = datetime.now().strftime("%Y%m%d-%H%M%S")
    destino = CACHE / f"corrida-{marca}.json"
    while destino.exists():  # un crudo no se sobrescribe
        marca += "-r"
        destino = CACHE / f"corrida-{marca}.json"
    crudo = {
        "etiqueta": f"corrida-{marca}",
        "version": VERSION,
        "alias": ALIAS,
        "pregunta": pregunta,
        "tools": TOOLS,
        "requests": cuerpos,
        "responses": [
            {
                "model": r["model"],
                "finish_reason": r["choices"][0].get("finish_reason"),
                "message": r["choices"][0]["message"],
                "usage": r["usage"],
                "stream_chunks_crudos": r["_stream_chunks_crudos"],
            }
            for r in respuestas
        ],
    }
    destino.write_text(json.dumps(crudo, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\ncrudo: {destino.relative_to(RAIZ)}")


def main():
    system = (AQUI / "system_prompt.md").read_text(encoding="utf-8").strip()
    operacion, numeros = leer_entrada()
    if not operacion or not numeros:
        raise SystemExit("faltan la operación o los números")
    pregunta = f"Operación: {operacion}. Números: {', '.join(numeros)}."
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": pregunta},
    ]
    print(f"\nUsuario> {pregunta}")

    cuerpos, respuestas = [], []
    for turno in range(1, MAX_TURNOS + 1):
        body, resp = call_model(VERSION, ALIAS, None, messages=messages, tools=TOOLS)
        cuerpos.append(body)
        respuestas.append(resp)
        mensaje = resp["choices"][0]["message"]
        llamadas = mensaje.get("tool_calls") or []
        print(f"    (turno {turno}: {len(messages)} mensajes enviados, "
              f"{len(json.dumps(body))} bytes, finish_reason "
              f"{resp['choices'][0].get('finish_reason')})")
        if not llamadas:
            print(f"Modelo> {mensaje['content'].strip()}")
            break
        # El mensaje del asistente vuelve tal cual: con sus `tool_calls` y su
        # `reasoning_content`, que la API exige devolver cuando hay `tools`.
        assistant = {"role": "assistant", "content": mensaje["content"] or None,
                     "tool_calls": llamadas}
        if mensaje.get("reasoning_content"):
            assistant["reasoning_content"] = mensaje["reasoning_content"]
        messages.append(assistant)
        for llamada in llamadas:
            nombre = llamada["function"]["name"]
            argumentos = llamada["function"]["arguments"]
            texto, ok = ejecutar(nombre, argumentos)
            print(f"  tool> {nombre}({argumentos}) -> {texto}{'' if ok else '   [error]'}")
            messages.append({"role": "tool", "tool_call_id": llamada["id"], "content": texto})
    else:
        print(f"Modelo> (cortado: {MAX_TURNOS} turnos sin respuesta final)")

    guardar_crudo(pregunta, cuerpos, respuestas)


if __name__ == "__main__":
    main()
