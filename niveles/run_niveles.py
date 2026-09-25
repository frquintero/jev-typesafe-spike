"""niveles/: separar datos y argumentos (llamada A), construir tesis (llamada B).

Uso: python3 niveles/run_niveles.py <doc> <modelo> <prompt_A> <prompt_B> <rN>
  p. ej. python3 niveles/run_niveles.py doc1 flash A_v1 B_v1 r1

No usa Jev. Modelos vía credencial de API inyectada por proxy (mismo patrón
que TypeSafe/z.ai/DeepSeek en este entorno cloud): nunca se arma
Authorization ni se lee ninguna clave. Sin SDK: urllib + dicts planos.
"""
import json
import os
import string
import sys
import urllib.error
import urllib.request

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCS_DIR = os.path.join(BASE_DIR, "docs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

UA = "spike-jev/1.0"
PUNCT = set(string.punctuation)

# Confirmado contra la doc de cada proveedor (ver reporte de la sesión):
# - flash: GLM 5.3 Flash vía z.ai, API compatible OpenAI.
# - deepseek: DeepSeek, variante de chat estándar (no razonamiento).
MODELS = {
    "flash": {
        "id": "glm-5.3-flash",
        "url": "https://api.z.ai/api/paas/v4/chat/completions",
    },
    "deepseek": {
        "id": "deepseek-chat",
        "url": "https://api.deepseek.com/chat/completions",
    },
}


def call_model(alias, content):
    cfg = MODELS[alias]
    body = {"model": cfg["id"], "messages": [{"role": "user", "content": content}]}
    req = urllib.request.Request(
        cfg["url"],
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "User-Agent": UA},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            resp = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        if e.code in (401, 403):
            raise SystemExit(
                f"error de autenticación ({e.code}) llamando a '{alias}': "
                f"detenido, no se busca la clave por otros medios"
            )
        raise
    return body, resp


def extract_json(content):
    """Devuelve (parsed, wrapped, error) a partir del content de la respuesta."""
    text = content.strip()
    wrapped = False
    if text.startswith("```"):
        wrapped = True
        lines = text.split("\n")
        lines = lines[1:]  # quita la linea de apertura ``` o ```json
        if lines and lines[-1].strip().startswith("```"):
            lines = lines[:-1]
        text = "\n".join(lines).strip()
    try:
        return json.loads(text), wrapped, None
    except json.JSONDecodeError as e:
        return None, wrapped, str(e)


def verificar_a(parsed, doc_text):
    """Literalidad, cobertura, ids de soporte. Devuelve dict de resultados."""
    resultado = {
        "literalidad": {"ok": [], "fallidas": []},
        "cobertura": {"ok": True, "sobrante": ""},
        "ids": {"ok": True, "problemas": []},
    }
    if not parsed or "elementos" not in parsed:
        resultado["literalidad"]["fallidas"].append("(sin elementos: A no parseo o vino vacio)")
        resultado["cobertura"]["ok"] = False
        resultado["ids"]["ok"] = False
        return resultado

    elementos = parsed.get("elementos", [])
    elementos_by_id = {}
    for el in elementos:
        eid = el.get("id")
        cita = el.get("cita", "")
        elementos_by_id[eid] = el
        if cita and cita in doc_text:
            resultado["literalidad"]["ok"].append(eid)
        else:
            resultado["literalidad"]["fallidas"].append(eid)

    # Cobertura: quitar en orden las citas que si aparecieron literal.
    restante = doc_text
    for el in elementos:
        eid = el.get("id")
        cita = el.get("cita", "")
        if eid in resultado["literalidad"]["ok"] and cita:
            restante = restante.replace(cita, "", 1)
    sobrante_significativo = "".join(
        ch for ch in restante if not ch.isspace() and ch not in PUNCT
    )
    if sobrante_significativo:
        resultado["cobertura"]["ok"] = False
        resultado["cobertura"]["sobrante"] = restante

    # Ids de soporte.
    for sop in parsed.get("soporte", []):
        arg_id = sop.get("argumento")
        arg_el = elementos_by_id.get(arg_id)
        if arg_el is None:
            resultado["ids"]["problemas"].append(f"argumento {arg_id} no existe")
        elif arg_el.get("tipo") != "argumento":
            resultado["ids"]["problemas"].append(
                f"argumento {arg_id} no es tipo argumento (es {arg_el.get('tipo')})"
            )
        for did in sop.get("datos", []):
            dato_el = elementos_by_id.get(did)
            if dato_el is None:
                resultado["ids"]["problemas"].append(f"dato {did} no existe")
            elif dato_el.get("tipo") != "dato":
                resultado["ids"]["problemas"].append(
                    f"dato {did} no es tipo dato (es {dato_el.get('tipo')})"
                )
    if resultado["ids"]["problemas"]:
        resultado["ids"]["ok"] = False

    return resultado


def construir_entrada_b(parsed):
    """Renumera argumentos/datos (excluye 'otro'), arma texto B y la correspondencia."""
    if not parsed or "elementos" not in parsed:
        return "", "", {}

    elementos = parsed.get("elementos", [])
    correspondencia = {}
    args_orden = []  # (nuevo_id, cita, old_id)
    datos_orden = []

    for el in elementos:
        eid = el.get("id")
        tipo = el.get("tipo")
        if tipo == "argumento":
            nuevo = f"A{len(args_orden) + 1}"
            args_orden.append((nuevo, el.get("cita", ""), eid))
            correspondencia[eid] = nuevo
        elif tipo == "dato":
            nuevo = f"D{len(datos_orden) + 1}"
            datos_orden.append((nuevo, el.get("cita", ""), eid))
            correspondencia[eid] = nuevo
        else:
            correspondencia[eid] = None  # "otro": excluido

    # old_id -> lista de datos que lo sostienen (old ids), desde soporte.
    soporte_por_arg_old = {}
    for sop in parsed.get("soporte", []):
        soporte_por_arg_old[sop.get("argumento")] = sop.get("datos", [])

    lineas_args = []
    for nuevo, cita, old_id in args_orden:
        datos_old = soporte_por_arg_old.get(old_id, [])
        datos_new = [correspondencia.get(d) for d in datos_old if correspondencia.get(d)]
        if datos_new:
            lineas_args.append(f'{nuevo}: "{cita}" (sostenido por {", ".join(datos_new)})')
        else:
            lineas_args.append(f'{nuevo}: "{cita}" (sin datos)')

    lineas_datos = [f'{nuevo}: "{cita}"' for nuevo, cita, _old_id in datos_orden]

    return "\n".join(lineas_args), "\n".join(lineas_datos), correspondencia


def run(doc, modelo, prompt_a_name, prompt_b_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(
        CACHE_DIR, f"niveles-{doc}-{modelo}-{prompt_a_name}-{prompt_b_name}-{rep}.json"
    )
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return

    if modelo not in MODELS:
        raise SystemExit(f"modelo desconocido: {modelo} (conocidos: {list(MODELS)})")

    doc_path = os.path.join(DOCS_DIR, f"{doc}.md")
    with open(doc_path, encoding="utf-8") as f:
        doc_text = f.read()

    prompt_a_path = os.path.join(PROMPTS_DIR, f"{prompt_a_name}.md")
    with open(prompt_a_path, encoding="utf-8") as f:
        prompt_a_tpl = f.read()
    contenido_a = prompt_a_tpl.replace("{{TEXTO}}", doc_text)

    body_a, resp_a = call_model(modelo, contenido_a)
    content_a = resp_a["choices"][0]["message"]["content"]
    parsed_a, wrapped_a, error_a = extract_json(content_a)

    verificacion_a = verificar_a(parsed_a, doc_text)

    args_txt, datos_txt, correspondencia = construir_entrada_b(parsed_a)

    prompt_b_path = os.path.join(PROMPTS_DIR, f"{prompt_b_name}.md")
    with open(prompt_b_path, encoding="utf-8") as f:
        prompt_b_tpl = f.read()
    contenido_b = prompt_b_tpl.replace("{{ARGUMENTOS}}", args_txt).replace("{{DATOS}}", datos_txt)

    body_b, resp_b = call_model(modelo, contenido_b)
    content_b = resp_b["choices"][0]["message"]["content"]
    parsed_b, wrapped_b, error_b = extract_json(content_b)

    crudo = {
        "doc": doc,
        "modelo": modelo,
        "modelo_id": MODELS[modelo]["id"],
        "llamada_a": {
            "request": body_a,
            "response": resp_a,
            "parseo": {"ok": error_a is None, "venia_con_cerca": wrapped_a, "error": error_a},
            "verificacion": verificacion_a,
        },
        "correspondencia_ids": correspondencia,
        "entrada_b": {"argumentos": args_txt, "datos": datos_txt},
        "a_marcada_por_fallo": error_a is not None or not verificacion_a["cobertura"]["ok"]
        or not verificacion_a["ids"]["ok"]
        or bool(verificacion_a["literalidad"]["fallidas"]),
        "llamada_b": {
            "request": body_b,
            "response": resp_b,
            "parseo": {"ok": error_b is None, "venia_con_cerca": wrapped_b, "error": error_b},
        },
    }

    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path}")


def main(argv):
    if len(argv) != 6:
        raise SystemExit(
            "uso: python3 niveles/run_niveles.py <doc> <modelo> <prompt_A> <prompt_B> <rN>"
        )
    _, doc, modelo, prompt_a, prompt_b, rep = argv
    run(doc, modelo, prompt_a, prompt_b, rep)


if __name__ == "__main__":
    main(sys.argv)
