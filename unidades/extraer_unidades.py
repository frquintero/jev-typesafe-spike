"""unidades/extraer_unidades.py: paso 1, unidades temáticas (PLAN.md, ronda U1).

Uso: python3 unidades/extraer_unidades.py <doc> <modelo> <prompt> <rN>
  p. ej. python3 unidades/extraer_unidades.py tec1 grok unidades_v1 r1

Lee el documento y el prompt, sustituye {{TEXTO}}, llama al LLM con call_model
de niveles/run_niveles.py (mismos modelos y parámetros) y guarda el crudo con el
tiempo total. Luego verifica literalidad y cobertura: solo reporta, nunca corrige.
Idempotente: si el crudo existe, no vuelve a llamar.
"""
import json
import os
import re
import sys
import time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(BASE_DIR), "niveles"))
from run_niveles import call_model, extract_json  # noqa: E402

DOCS_DIR = os.path.join(BASE_DIR, "docs")
PROMPTS_DIR = os.path.join(BASE_DIR, "prompts")
CACHE_DIR = os.path.join(BASE_DIR, "cache")


def oraciones(texto):
    """Definición del prompt: de un . ? ! al siguiente; el título (# ...) queda fuera."""
    cuerpo = "\n".join(l for l in texto.splitlines() if not l.startswith("#"))
    return [p.strip() for p in re.findall(r"[^.?!]+[.?!]?", cuerpo) if p.strip()]


def literales(parsed):
    # v1: nucleo/satelites son objetos con menciones; v2: son nombres (no literales)
    for u in parsed.get("unidades", []):
        yield from u.get("oraciones", [])
        nucleo = u.get("nucleo")
        if isinstance(nucleo, dict):
            yield from nucleo.get("menciones", [])
        for s in u.get("satelites", []):
            if isinstance(s, dict):
                yield from s.get("menciones", [])
    for a in parsed.get("anaforas", []):
        yield a.get("mencion", "")
        yield a.get("oracion", "")
    for p in parsed.get("procedencias", []):
        yield p.get("fuente", "")
        yield from p.get("oraciones", [])
    yield from parsed.get("oraciones_sin_unidad", [])


def verificar(parsed, texto):
    ors = oraciones(texto)
    asignadas = [o for u in parsed.get("unidades", []) for o in u.get("oraciones", [])]
    return {
        "oraciones_del_texto": len(ors),
        "no_literales": sorted({s for s in literales(parsed) if s and s not in texto}),
        "sin_asignar": [o for o in ors if o not in asignadas],
        "en_mas_de_una_unidad": sorted({o for o in asignadas if asignadas.count(o) > 1}),
        "asignadas_que_no_son_oracion": [o for o in asignadas if o not in ors],
    }


def numerar_oraciones(texto):
    """Return paragraph-preserving numbered text and its sentence records."""
    parrafos = []
    lineas_parrafo = []
    for linea in texto.splitlines():
        if linea.startswith("#"):
            continue
        if not linea.strip():
            if lineas_parrafo:
                parrafos.append("\n".join(lineas_parrafo))
                lineas_parrafo = []
        else:
            lineas_parrafo.append(linea)
    if lineas_parrafo:
        parrafos.append("\n".join(lineas_parrafo))

    registros = []
    parrafos_numerados = []
    for parrafo in parrafos:
        oraciones_parrafo = []
        for oracion in oraciones(parrafo):
            numero = len(registros) + 1
            registros.append({"n": numero, "oracion": oracion})
            oraciones_parrafo.append(f"[{numero}] {oracion}")
        if oraciones_parrafo:
            parrafos_numerados.append(" ".join(oraciones_parrafo))
    return "\n\n".join(parrafos_numerados), registros


def es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def reconstruir_unidades(parsed, oraciones_numeradas):
    por_numero = {item["n"]: item["oracion"] for item in oraciones_numeradas}
    reconstruidas = []
    for unidad in parsed.get("unidades", []):
        desde = unidad.get("desde")
        hasta = unidad.get("hasta")
        oraciones_unidad = []
        if es_entero(desde) and es_entero(hasta) and desde <= hasta:
            oraciones_unidad = [
                por_numero[n]
                for n in range(max(1, desde), min(len(por_numero), hasta) + 1)
                if n in por_numero
            ]
        reconstruidas.append(
            {
                "tema": unidad.get("tema"),
                "desde": desde,
                "hasta": hasta,
                "oraciones": oraciones_unidad,
            }
        )
    return reconstruidas


def verificar_rangos(parsed, oraciones_numeradas):
    total = len(oraciones_numeradas)
    asignaciones = [0] * (total + 1)
    fuera_de_rango = []
    desordenadas = []
    desde_anterior = None

    for unidad_n, unidad in enumerate(parsed.get("unidades", []), start=1):
        desde = unidad.get("desde")
        hasta = unidad.get("hasta")
        if not es_entero(desde) or not es_entero(hasta):
            fuera_de_rango.append(unidad_n)
            continue

        if desde < 1 or desde > total or hasta < 1 or hasta > total:
            fuera_de_rango.append(unidad_n)
        if desde > hasta or (
            desde_anterior is not None and desde <= desde_anterior
        ):
            desordenadas.append(unidad_n)
        desde_anterior = desde

        if desde <= hasta:
            primero = max(1, desde)
            ultimo = min(total, hasta)
            for numero in range(primero, ultimo + 1):
                asignaciones[numero] += 1

    return {
        "oraciones_del_texto": total,
        "huecos": [n for n in range(1, total + 1) if asignaciones[n] == 0],
        "solapes": [n for n in range(1, total + 1) if asignaciones[n] > 1],
        "fuera_de_rango": fuera_de_rango,
        "desordenadas": desordenadas,
    }


def run(doc, modelo, prompt_name, rep):
    os.makedirs(CACHE_DIR, exist_ok=True)
    cache_path = os.path.join(CACHE_DIR, f"unidades-{doc}-{modelo}-{prompt_name}-{rep}.json")
    if os.path.exists(cache_path):
        print(f"crudo ya existe, salto ({cache_path})")
        return
    with open(os.path.join(DOCS_DIR, f"{doc}.md"), encoding="utf-8") as f:
        texto = f.read()
    with open(os.path.join(PROMPTS_DIR, f"{prompt_name}.md"), encoding="utf-8") as f:
        prompt = f.read()

    numerado = "{{TEXTO_NUMERADO}}" in prompt
    oraciones_numeradas = None
    if numerado:
        texto_enviado, oraciones_numeradas = numerar_oraciones(texto)
        prompt_enviado = prompt.replace("{{TEXTO_NUMERADO}}", texto_enviado)
    else:
        prompt_enviado = prompt.replace("{{TEXTO}}", texto)

    t0 = time.time()
    body, resp = call_model("toulmin", modelo, prompt_enviado)
    segundos = round(time.time() - t0, 1)
    parsed, venia_con_cerca, error = extract_json(resp["choices"][0]["message"]["content"])

    if numerado:
        verificacion = (
            verificar_rangos(parsed, oraciones_numeradas)
            if parsed is not None
            else None
        )
    else:
        verificacion = verificar(parsed, texto) if parsed else None

    crudo = {
        "doc": doc, "modelo": modelo, "prompt": prompt_name,
        "segundos": segundos,
        "request": body, "response": resp,
        "parsed": parsed, "venia_con_cerca": venia_con_cerca, "error_parseo": error,
        "verificacion": verificacion,
    }
    if numerado:
        crudo["texto_numerado"] = texto_enviado
        crudo["oraciones_numeradas"] = oraciones_numeradas
        unidades = parsed.get("unidades", []) if isinstance(parsed, dict) else []
        if unidades and all(
            isinstance(unidad, dict)
            and "desde" in unidad
            and "hasta" in unidad
            for unidad in unidades
        ):
            crudo["unidades_reconstruidas"] = reconstruir_unidades(
                parsed, oraciones_numeradas
            )
    with open(cache_path, "w", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {cache_path} ({segundos} s)")
    print(json.dumps(crudo["verificacion"], ensure_ascii=False, indent=2))


def main(argv):
    if len(argv) != 5:
        raise SystemExit("uso: python3 unidades/extraer_unidades.py <doc> <modelo> <prompt> <rN>")
    run(*argv[1:])


if __name__ == "__main__":
    main(sys.argv)
