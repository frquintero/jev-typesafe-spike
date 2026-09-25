"""niveles/jev_sopesa.py: Jev sopesa (Noul) la clasificacion Toulmin de un LLM.

Uso: python3 niveles/jev_sopesa.py <crudo_llm.json>
  p. ej. python3 niveles/jev_sopesa.py niveles/cache/niveles-doc2-deepseek-toulmin_v3-r1.json

Arma el build de Jev en tiempo de ejecucion a partir de la salida ya
clasificada por el LLM (una llamada unica de run_niveles.py, formato
toulmin_v3): un Noul por elemento (se omiten los tipo 'titulo') mas un Noul
de control, todo en una sola llamada (fan-out). No corrige nada de lo que
clasifico el LLM; solo reporta el grado de soporte que Jev le da a cada
etiqueta. Credencial via proxy del entorno cloud (mismo patron que
probes/): nunca se arma Authorization ni se lee ninguna clave. Sin SDK:
urllib + dicts planos.
"""
import json
import os
import sys
import urllib.error
import urllib.request

from run_niveles import extract_json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

API_URL = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"
UA = "spike-jev/1.0"

# Etiqueta y definicion por tipo, verbatim del prompt toulmin_v3 (PLAN.md,
# Ronda 6). Si el prompt cambia, esta tabla cambia con el.
ETIQUETAS = {
    "dato": ("un dato", "el hecho del que se parte; la evidencia"),
    "conclusion": ("una conclusión", "lo que el texto quiere establecer"),
    "garantia": ("una garantía", "la regla que autoriza a pasar del dato a la conclusión"),
    "respaldo": ("un respaldo", "lo que sostiene a la garantía: una norma, un estudio, la experiencia"),
    "reserva": ("una reserva", "una oración que establece las condiciones bajo las cuales una conclusión no vale"),
    "contraargumento": ("un contraargumento", "una posición o explicación contraria que el texto presenta para rebatirla"),
    "concesion": ("una concesión", "algo en contra de la propia conclusión que el texto admite como cierto, sin abandonar la conclusión"),
    "otro": ("otra cosa", "no cumple ninguna de las funciones de un argumento"),
}
CONTROL_ETIQUETA, CONTROL_DEFINICION = ETIQUETAS["conclusion"]


def cargar_elementos(crudo_llm_path):
    with open(crudo_llm_path, encoding="utf-8") as f:
        crudo = json.load(f)
    content = crudo["llamada_unica"]["response"]["choices"][0]["message"]["content"]
    parsed, _wrapped, error = extract_json(content)
    if error:
        raise SystemExit(f"el crudo LLM no parsea como JSON: {error}")
    return crudo["doc"], parsed.get("elementos", [])


def elegir_control(elementos):
    """El primer contraargumento; si no hay, el primer dato (PLAN.md, Ronda 6)."""
    for el in elementos:
        if el.get("tipo") == "contraargumento":
            return el
    for el in elementos:
        if el.get("tipo") == "dato":
            return el
    raise SystemExit("no hay elemento tipo 'contraargumento' ni 'dato' para el control")


def construir_body(doc, elementos):
    doc_path = os.path.join(DOCS_DIR, f"{doc}.md")
    with open(doc_path, encoding="utf-8") as f:
        state = f.read()

    utiles = [el for el in elementos if el.get("tipo") != "titulo"]
    questions = {}
    mapa = {}
    for i, el in enumerate(utiles, start=1):
        clave = f"n{i:02d}"
        etiqueta, definicion = ETIQUETAS[el["tipo"]]
        questions[clave] = {
            "type": "noul",
            "instructions": f"En este texto, «{el['cita']}» es {etiqueta}: {definicion}.",
        }
        mapa[clave] = el["id"]

    control_el = elegir_control(utiles)
    clave_control = f"n{len(utiles) + 1:02d}"
    questions[clave_control] = {
        "type": "noul",
        "instructions": (
            f"En este texto, «{control_el['cita']}» es {CONTROL_ETIQUETA}: "
            f"{CONTROL_DEFINICION}."
        ),
    }
    # El control reutiliza un elemento ya preguntado con su etiqueta correcta;
    # aqui se le pregunta ademas con la etiqueta falsa "conclusion". La clave
    # es neutra igual que las demas; "control" solo existe en el mapa, nunca
    # en el body que ve Jev.
    mapa[clave_control] = control_el["id"]
    mapa["control"] = clave_control

    body = {"model": MODEL, "state": state, "questions": questions}
    return body, mapa


def llamar_jev(body):
    req = urllib.request.Request(
        API_URL,
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        error_body = e.read().decode(errors="replace")[:500]
        raise SystemExit(
            f"error {e.code} llamando a Jev: detenido, no se reintenta ni se "
            f"busca la clave por otros medios.\n{error_body}"
        )


def run(crudo_llm_path):
    os.makedirs(CACHE_DIR, exist_ok=True)
    nombre = os.path.splitext(os.path.basename(crudo_llm_path))[0]
    cache_path = os.path.join(CACHE_DIR, f"jev-{nombre}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return

    doc, elementos = cargar_elementos(crudo_llm_path)
    body, mapa = construir_body(doc, elementos)
    resp = llamar_jev(body)

    if resp.get("model") != MODEL:
        print(
            f"AVISO: modelo efectivo '{resp.get('model')}' no coincide con "
            f"el pineado '{MODEL}'"
        )

    crudo = {"request": body, "response": resp, "mapa": mapa}
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path}")


def main(argv):
    if len(argv) != 2:
        raise SystemExit("uso: python3 niveles/jev_sopesa.py <crudo_llm.json>")
    run(argv[1])


if __name__ == "__main__":
    main(sys.argv)
