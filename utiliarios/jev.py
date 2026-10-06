#!/usr/bin/env python3
"""Protocolo Jev (SystemOne de TypeSafe): arma la petición y la envía.

  python3 utiliarios/jev.py seco   <expediente> <preguntas> [<salida.json>]
  python3 utiliarios/jev.py correr <expediente> <preguntas> [<salida.json>]

  <expediente>  el estado: un .json (string, dict o array) o un texto suelto
  <preguntas>   un .json con el objeto `questions`
  <salida.json> opcional: guarda {request, response}; nunca la cabecera

El modelo es fijo: `jev-1.13.0`. Si la respuesta trae otro `model`, se avisa.

Forma de cada pregunta (las claves son neutras: el modelo no las usa):
  "q1": {"type": "noul",   "instructions": "el juicio"}
  "q1": {"type": "choice", "instructions": "el marco", "criteria": [...]}
  "q1": {"type": "score",  "instructions": "el marco", "criteria": [...]}

Lectura: **Noul** devuelve un grado 0–1, que se lee por bandas (la franja
0,30–0,65 es señal de diseño); **Choice**, alternativas sin orden y siempre con
opción de salida; **Score**, niveles ordenados, con `score` = posición media.
Varias preguntas en una llamada se resuelven en paralelo (fan-out): cambia la
latencia, no el resultado. No hay `temperature`: la estabilidad se mide con
réplicas (r1/r2/r3).

La clave la pone `cabecera_clave` de `niveles/run_niveles.py` desde el entorno:
aquí no se lee ni se imprime ninguna clave.
"""
import json
import pathlib
import sys
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "niveles"))

from run_niveles import cabecera_clave  # noqa: E402

URL = "https://api.typesafe.ai/v1/systemone"
MODELO = "jev-1.13.0"
TIPOS = ("noul", "choice", "score")


def leer(ruta):
    p = pathlib.Path(ruta)
    if not p.exists():
        raise SystemExit(f"no existe: {p}")
    texto = p.read_text(encoding="utf-8")
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return texto  # el expediente puede ser texto suelto


def cuerpo(estado, preguntas):
    if not isinstance(preguntas, dict) or not preguntas:
        raise SystemExit("las preguntas deben ser un objeto JSON no vacío")
    for clave, q in preguntas.items():
        if not isinstance(q, dict) or q.get("type") not in TIPOS:
            raise SystemExit(f"pregunta inválida «{clave}»: type debe ser noul|choice|score")
        if q["type"] in ("choice", "score") and "criteria" not in q:
            raise SystemExit(f"pregunta «{clave}»: {q['type']} necesita criteria")
    return {"model": MODELO, "state": estado, "questions": preguntas}


def main(argv):
    if len(argv) not in (4, 5) or argv[1] not in ("seco", "correr"):
        raise SystemExit(__doc__)
    modo = argv[1]
    enviado = cuerpo(leer(argv[2]), leer(argv[3]))
    if modo == "seco":
        print(json.dumps(enviado, ensure_ascii=False, indent=2))
        print("(modo seco: no se llama a la API)")
        return
    req = urllib.request.Request(
        URL,
        data=json.dumps(enviado).encode("utf-8"),
        headers={"Content-Type": "application/json", **cabecera_clave(URL)},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=600) as r:
        respuesta = json.loads(r.read().decode("utf-8"))
    modelo = respuesta.get("model") or (respuesta.get("usage") or {}).get("model")
    if modelo and modelo != MODELO:
        print(f"AVISO: el modelo efectivo es {modelo}, no {MODELO}", file=sys.stderr)
    print(json.dumps(respuesta, ensure_ascii=False, indent=2))
    if len(argv) == 5:
        pathlib.Path(argv[4]).write_text(
            json.dumps({"request": enviado, "response": respuesta}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"guardado: {argv[4]}")


if __name__ == "__main__":
    main(sys.argv)
