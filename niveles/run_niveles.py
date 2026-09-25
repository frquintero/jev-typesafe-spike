"""niveles/: separar estructura argumentativa (llamada A), construir tesis (llamada B).

Uso: python3 niveles/run_niveles.py <doc> <modelo> <prompt_A> <prompt_B> <rN>
  p. ej. python3 niveles/run_niveles.py doc1 flash A_v1 B_v1 r1
         python3 niveles/run_niveles.py doc1 flash A_v2 B_v2 r1

El esquema (v1: datos/argumentos; v2: datos/garantias/conclusiones) se elige
por el sufijo de <prompt_A> (_v1 o _v2). v1 sigue funcionando igual que en la
ronda 1. No usa Jev. Modelos vía credencial de API inyectada por proxy (mismo
patron que TypeSafe/z.ai/DeepSeek en este entorno cloud): nunca se arma
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

# Confirmado contra la doc de cada proveedor (ver reportes de la sesión).
# Ronda 1 (v1): sin parametros extra. Ronda 2 (v2): parametros de la tabla
# del PLAN.md, excepcion autorizada a "sin parametros extra".
MODEL_PARAMS = {
    "v1": {
        "flash": {
            "id": "glm-5.3-flash",
            "url": "https://api.z.ai/api/paas/v4/chat/completions",
            "extra": {},
        },
        "deepseek": {
            "id": "deepseek-chat",
            "url": "https://api.deepseek.com/chat/completions",
            "extra": {},
        },
    },
    "v2": {
        "flash": {
            "id": "glm-5.3-flash",
            "url": "https://api.z.ai/api/paas/v4/chat/completions",
            "extra": {"reasoning_effort": "low"},
        },
        "deepseek": {
            "id": "deepseek-flash",
            "url": "https://api.deepseek.com/chat/completions",
            "extra": {"thinking": {"type": "enabled"}, "reasoning_effort": "low"},
        },
    },
}


def prompt_version(prompt_name):
    if prompt_name.endswith("_v2"):
        return "v2"
    if prompt_name.endswith("_v1"):
        return "v1"
    raise SystemExit(
        f"no puedo determinar el esquema de '{prompt_name}': debe terminar en _v1 o _v2"
    )


def call_model(version, alias, content):
    """Llama con stream=true (excepcion autorizada: stream es transporte, no
    cambia la salida) mas los parametros extra de MODEL_PARAMS[version][alias]
    (solo los de la tabla del PLAN, nunca temperature). Ensambla los deltas
    SSE. Devuelve (body_enviado, response_ensamblada) donde
    response_ensamblada imita la forma no-streaming (choices[0].message.
    content / .reasoning_content, model, usage) y ademas guarda los chunks
    crudos verbatim en "_stream_chunks_crudos". Cualquier rechazo del
    proveedor (parametro no soportado, autenticacion, lo que sea) detiene la
    ejecucion y reporta; no se reintenta ni se busca la clave por otros medios.
    """
    cfg = MODEL_PARAMS[version][alias]
    body = {
        "model": cfg["id"],
        "messages": [{"role": "user", "content": content}],
        "stream": True,
    }
    body.update(cfg["extra"])
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        cfg["url"],
        data=data,
        headers={
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": UA,
        },
        method="POST",
    )
    chunks_crudos = []
    content_parts = []
    reasoning_parts = []
    model_efectivo = None
    usage = None
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            for raw_line in r:
                line = raw_line.decode("utf-8").strip()
                if not line or not line.startswith("data:"):
                    continue
                payload = line[len("data:"):].strip()
                chunks_crudos.append(payload)
                if payload == "[DONE]":
                    break
                chunk = json.loads(payload)
                if chunk.get("model"):
                    model_efectivo = chunk["model"]
                if chunk.get("usage"):
                    usage = chunk["usage"]
                choices = chunk.get("choices") or []
                if choices:
                    delta = choices[0].get("delta", {})
                    if delta.get("content"):
                        content_parts.append(delta["content"])
                    if delta.get("reasoning_content"):
                        reasoning_parts.append(delta["reasoning_content"])
    except urllib.error.HTTPError as e:
        error_body = e.read().decode(errors="replace")[:500]
        raise SystemExit(
            f"error {e.code} llamando a '{alias}' ({version}): detenido, "
            f"no se reintenta ni se busca la clave por otros medios.\n{error_body}"
        )

    resp = {
        "model": model_efectivo,
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "".join(content_parts),
                    "reasoning_content": "".join(reasoning_parts),
                }
            }
        ],
        "usage": usage,
        "_stream_chunks_crudos": chunks_crudos,
    }
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


def _verificar_literalidad_cobertura(parsed, doc_text):
    """Comun a v1/v2: cada cita debe aparecer literal; cobertura del texto."""
    literalidad = {"ok": [], "fallidas": []}
    cobertura = {"ok": True, "sobrante": ""}

    if not parsed or "elementos" not in parsed:
        literalidad["fallidas"].append("(sin elementos: A no parseo o vino vacio)")
        cobertura["ok"] = False
        return literalidad, cobertura, {}

    elementos = parsed.get("elementos", [])
    elementos_by_id = {}
    for el in elementos:
        eid = el.get("id")
        cita = el.get("cita", "")
        elementos_by_id[eid] = el
        if cita and cita in doc_text:
            literalidad["ok"].append(eid)
        else:
            literalidad["fallidas"].append(eid)

    restante = doc_text
    for el in elementos:
        eid = el.get("id")
        cita = el.get("cita", "")
        if eid in literalidad["ok"] and cita:
            restante = restante.replace(cita, "", 1)
    sobrante_significativo = "".join(
        ch for ch in restante if not ch.isspace() and ch not in PUNCT
    )
    if sobrante_significativo:
        cobertura["ok"] = False
        cobertura["sobrante"] = restante

    return literalidad, cobertura, elementos_by_id


def verificar_a_v1(parsed, doc_text):
    literalidad, cobertura, elementos_by_id = _verificar_literalidad_cobertura(parsed, doc_text)
    ids = {"ok": True, "problemas": []}
    if not parsed:
        ids["ok"] = False
        return {"literalidad": literalidad, "cobertura": cobertura, "ids": ids}

    for sop in parsed.get("soporte", []):
        arg_id = sop.get("argumento")
        arg_el = elementos_by_id.get(arg_id)
        if arg_el is None:
            ids["problemas"].append(f"argumento {arg_id} no existe")
        elif arg_el.get("tipo") != "argumento":
            ids["problemas"].append(
                f"argumento {arg_id} no es tipo argumento (es {arg_el.get('tipo')})"
            )
        for did in sop.get("datos", []):
            dato_el = elementos_by_id.get(did)
            if dato_el is None:
                ids["problemas"].append(f"dato {did} no existe")
            elif dato_el.get("tipo") != "dato":
                ids["problemas"].append(
                    f"dato {did} no es tipo dato (es {dato_el.get('tipo')})"
                )
    if ids["problemas"]:
        ids["ok"] = False

    return {"literalidad": literalidad, "cobertura": cobertura, "ids": ids}


def verificar_a_v2(parsed, doc_text):
    literalidad, cobertura, elementos_by_id = _verificar_literalidad_cobertura(parsed, doc_text)
    ids = {"ok": True, "problemas": []}
    if not parsed:
        ids["ok"] = False
        return {"literalidad": literalidad, "cobertura": cobertura, "ids": ids}

    def check(eid, tipo_esperado, etiqueta):
        el = elementos_by_id.get(eid)
        if el is None:
            ids["problemas"].append(f"{etiqueta} {eid} no existe")
        elif el.get("tipo") != tipo_esperado:
            ids["problemas"].append(
                f"{etiqueta} {eid} no es tipo {tipo_esperado} (es {el.get('tipo')})"
            )

    for ap in parsed.get("apoyos", []):
        concl_id = ap.get("conclusion")
        check(concl_id, "conclusion", "conclusion")
        for did in ap.get("datos", []):
            check(did, "dato", "dato")
        for gid in ap.get("garantias", []):
            check(gid, "garantia", "garantia")
        for cid in ap.get("conclusiones", []):
            check(cid, "conclusion", "conclusion (apoyo)")

    if ids["problemas"]:
        ids["ok"] = False

    return {"literalidad": literalidad, "cobertura": cobertura, "ids": ids}


def construir_entrada_b_v1(parsed):
    """Renumera argumentos/datos (excluye 'otro'). Devuelve (secciones, correspondencia)."""
    if not parsed or "elementos" not in parsed:
        return {"ARGUMENTOS": "", "DATOS": ""}, {}

    elementos = parsed.get("elementos", [])
    correspondencia = {}
    args_orden = []
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
            correspondencia[eid] = None

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

    secciones = {
        "ARGUMENTOS": "\n".join(lineas_args),
        "DATOS": "\n".join(lineas_datos),
    }
    return secciones, correspondencia


def construir_entrada_b_v2(parsed):
    """Renumera conclusiones/garantias/datos (excluye 'otro'). Devuelve (secciones, correspondencia)."""
    if not parsed or "elementos" not in parsed:
        return {"CONCLUSIONES": "(ninguna)", "GARANTIAS": "(ninguna)", "DATOS": "(ninguna)"}, {}

    elementos = parsed.get("elementos", [])
    correspondencia = {}
    concl_orden = []
    garant_orden = []
    datos_orden = []

    for el in elementos:
        eid = el.get("id")
        tipo = el.get("tipo")
        if tipo == "conclusion":
            nuevo = f"C{len(concl_orden) + 1}"
            concl_orden.append((nuevo, el.get("cita", ""), eid))
            correspondencia[eid] = nuevo
        elif tipo == "garantia":
            nuevo = f"G{len(garant_orden) + 1}"
            garant_orden.append((nuevo, el.get("cita", ""), eid))
            correspondencia[eid] = nuevo
        elif tipo == "dato":
            nuevo = f"D{len(datos_orden) + 1}"
            datos_orden.append((nuevo, el.get("cita", ""), eid))
            correspondencia[eid] = nuevo
        else:
            correspondencia[eid] = None

    apoyos_por_concl_old = {}
    for ap in parsed.get("apoyos", []):
        apoyos_por_concl_old[ap.get("conclusion")] = ap

    lineas_concl = []
    for nuevo, cita, old_id in concl_orden:
        ap = apoyos_por_concl_old.get(old_id, {})
        datos_new = [correspondencia.get(d) for d in ap.get("datos", []) if correspondencia.get(d)]
        garant_new = [correspondencia.get(g) for g in ap.get("garantias", []) if correspondencia.get(g)]
        concl_new = [correspondencia.get(c) for c in ap.get("conclusiones", []) if correspondencia.get(c)]
        partes = []
        if datos_new:
            partes.append(f"datos {', '.join(datos_new)}")
        if garant_new:
            partes.append(f"garantías {', '.join(garant_new)}")
        if concl_new:
            partes.append(f"conclusiones {', '.join(concl_new)}")
        if partes:
            lineas_concl.append(f'{nuevo}: "{cita}" (apoyos: {"; ".join(partes)})')
        else:
            lineas_concl.append(f'{nuevo}: "{cita}" (sin apoyos)')

    lineas_garant = [f'{nuevo}: "{cita}"' for nuevo, cita, _old_id in garant_orden]
    lineas_datos = [f'{nuevo}: "{cita}"' for nuevo, cita, _old_id in datos_orden]

    secciones = {
        "CONCLUSIONES": "\n".join(lineas_concl) if lineas_concl else "(ninguna)",
        "GARANTIAS": "\n".join(lineas_garant) if lineas_garant else "(ninguna)",
        "DATOS": "\n".join(lineas_datos) if lineas_datos else "(ninguna)",
    }
    return secciones, correspondencia


def run(doc, modelo, prompt_a_name, prompt_b_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(
        CACHE_DIR, f"niveles-{doc}-{modelo}-{prompt_a_name}-{prompt_b_name}-{rep}.json"
    )
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return

    version = prompt_version(prompt_a_name)
    if modelo not in MODEL_PARAMS[version]:
        raise SystemExit(
            f"modelo desconocido para {version}: {modelo} "
            f"(conocidos: {list(MODEL_PARAMS[version])})"
        )

    doc_path = os.path.join(DOCS_DIR, f"{doc}.md")
    with open(doc_path, encoding="utf-8") as f:
        doc_text = f.read()

    prompt_a_path = os.path.join(PROMPTS_DIR, f"{prompt_a_name}.md")
    with open(prompt_a_path, encoding="utf-8") as f:
        prompt_a_tpl = f.read()
    contenido_a = prompt_a_tpl.replace("{{TEXTO}}", doc_text)

    body_a, resp_a = call_model(version, modelo, contenido_a)
    content_a = resp_a["choices"][0]["message"]["content"]
    parsed_a, wrapped_a, error_a = extract_json(content_a)

    if version == "v1":
        verificacion_a = verificar_a_v1(parsed_a, doc_text)
        secciones_b, correspondencia = construir_entrada_b_v1(parsed_a)
    else:
        verificacion_a = verificar_a_v2(parsed_a, doc_text)
        secciones_b, correspondencia = construir_entrada_b_v2(parsed_a)

    prompt_b_path = os.path.join(PROMPTS_DIR, f"{prompt_b_name}.md")
    with open(prompt_b_path, encoding="utf-8") as f:
        prompt_b_tpl = f.read()
    contenido_b = prompt_b_tpl
    for clave, valor in secciones_b.items():
        contenido_b = contenido_b.replace("{{" + clave + "}}", valor)

    body_b, resp_b = call_model(version, modelo, contenido_b)
    content_b = resp_b["choices"][0]["message"]["content"]
    parsed_b, wrapped_b, error_b = extract_json(content_b)

    crudo = {
        "doc": doc,
        "modelo": modelo,
        "esquema": version,
        "modelo_id": MODEL_PARAMS[version][modelo]["id"],
        "parametros_extra": MODEL_PARAMS[version][modelo]["extra"],
        "llamada_a": {
            "request": body_a,
            "response": resp_a,
            "parseo": {"ok": error_a is None, "venia_con_cerca": wrapped_a, "error": error_a},
            "verificacion": verificacion_a,
        },
        "correspondencia_ids": correspondencia,
        "entrada_b": secciones_b,
        "a_marcada_por_fallo": (
            error_a is not None
            or not verificacion_a["cobertura"]["ok"]
            or not verificacion_a["ids"]["ok"]
            or bool(verificacion_a["literalidad"]["fallidas"])
        ),
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
