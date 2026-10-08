#!/usr/bin/env python3
"""Comparación de entradas del paso 2: (a) unidad sola, (b) unidad + referencias,
(c) unidad + documento completo. Usa el candidato `prompt_ficha_contexto.md` y la
partición congelada de v9, sin volver a correr el paso 1.

Uso:
  python3 mvp/temp/paso2/comparacion.py seco     <doc> <salida_v9> <unidad_n>
  python3 mvp/temp/paso2/comparacion.py correr   <doc> <salida_v9> <modelo> <rN> <entrada>
  python3 mvp/temp/paso2/comparacion.py resumen  <doc> <salida_v9> <modelo> <rN>
  python3 mvp/temp/paso2/comparacion.py comparar <doc> <salida_v9> <rN> [<unidad_n>]
  python3 mvp/temp/paso2/comparacion.py verificar <crudo.json> [...]
  python3 mvp/temp/paso2/comparacion.py verificar-todos [<patrón glob>]

  <doc>       documento sintético (p. ej. mvp/temp/pruebas/doc4.md)
  <salida_v9> salida cruda de v9 (p. ej. mvp/temp/pruebas/salida_prueba8-v9-doc4.md)
  <entrada>   a | b | c
  <unidad_n>  número de unidad (1..N) para el modo seco

El crudo guarda el prompt entero enviado, el contenido y el razonamiento de la
respuesta, el modelo efectivo, el `usage` y el informe de verificación, para poder
auditar cada cita. Los frames SSE no se guardan (son transporte): se guarda su
número. Idempotente: si el crudo existe no vuelve a llamar y nunca lo sobrescribe.

`verificar` y `verificar-todos` **no llaman a ningún modelo**: releen un crudo
guardado, reconstruyen la entrada a partir de `texto_enviado` y `contexto_enviado`,
vuelven a comprobar los literales contra ese material y comparan el informe con el
que se guardó. Sirven para auditar una salida de v9 ya procesada sin re-correr nada.
"""
import glob as globmod
import hashlib
import json
import pathlib
import re
import sys
import time

RAIZ = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(RAIZ / "unidades"))
sys.path.insert(0, str(RAIZ / "niveles"))

from extraer_unidades import numerar_oraciones  # noqa: E402
from run_niveles import call_model, extract_json  # noqa: E402
from ficha_doc import fragmentos, verificar  # noqa: E402

CACHE = pathlib.Path(__file__).resolve().parent / "cache"
CANDIDATO = pathlib.Path(__file__).resolve().parent / "prompt_ficha_contexto.md"
MARCADOR_TEXTO = "{{TEXTO_NUMERADO}}"
MARCADOR_CONTEXTO = "{{CONTEXTO}}"
ENTRADAS = ("a", "b", "c")


def cargar(doc_path, salida_path):
    """Unidades de v9 con su numeración original y sus referencias."""
    texto_numerado, registros = numerar_oraciones(doc_path.read_text(encoding="utf-8"))
    parsed, _, error = extract_json(salida_path.read_text(encoding="utf-8").strip())
    if not isinstance(parsed, dict) or "subtemas" not in parsed:
        raise SystemExit(f"la salida de v9 no trae subtemas: {error}")
    por_n = {r["n"]: r["oracion"] for r in registros}
    unidades = []
    for i, s in enumerate(parsed["subtemas"], 1):
        regs = [{"n": n, "oracion": por_n[n]} for n in s["oraciones"]]
        unidades.append({
            "id": f"U{i}",
            "subtema": s["subtema"],
            "oraciones": list(s["oraciones"]),
            "referencias": s.get("referencias") or [],
            "registros": regs,
            "texto": " ".join(f"[{r['n']}] {r['oracion']}" for r in regs),
        })
    return texto_numerado, registros, unidades


def bloque_contexto(entrada, unidad, texto_numerado):
    """Material de apoyo: vacío en (a), referencias en (b), documento en (c)."""
    if entrada == "a":
        return ""
    if entrada == "c":
        return ("DOCUMENTO COMPLETO NUMERADO (las oraciones de la unidad van "
                f"repetidas)\n{texto_numerado}")
    lineas = []
    for r in unidad["referencias"]:
        if r.get("referente"):
            destino = r["referente"]
        else:
            destino = "SIN RESOLVER" + (f" ({r['duda']})" if r.get("duda") else "")
        frags = " · ".join(f"[{f['oracion']}] «{f['texto']}»"
                           for f in r.get("respaldo", []))
        lineas.append(f"- oración {r['oracion']} de la unidad · «{r['expresion']}» "
                      f"→ {destino}\n  respaldo: {frags}")
    if not lineas:
        return ""
    return ("REFERENCIAS EXTERNAS DE LA UNIDAD (su respaldo son fragmentos "
            "literales del documento, con su número de oración)\n" + "\n".join(lineas))


def corpus_entrada(entrada, unidad, registros):
    """Registros contra los que se comprueba la literalidad, según la entrada.

    (a) las oraciones de la unidad; (b) esas más los fragmentos recibidos, cada uno
    con el número de la oración de donde viene; (c) el documento completo.
    """
    if entrada == "c":
        return list(registros)
    vistos = {r["n"]: [r["oracion"]] for r in unidad["registros"]}
    if entrada == "b":
        for ref in unidad["referencias"]:
            for f in ref.get("respaldo", []):
                vistos.setdefault(f["oracion"], []).append(f["texto"])
    return [{"n": n, "oracion": "\n".join(dict.fromkeys(textos))}
            for n, textos in sorted(vistos.items())]


def informe(parsed, unidad, registros, entrada):
    """Verificación de forma más los cortes que la evaluación necesita."""
    corpus = corpus_entrada(entrada, unidad, registros)
    inf = {"entrada": entrada, "oraciones_enviadas": [r["n"] for r in corpus]}
    if not isinstance(parsed, dict):
        return inf
    inf["verificacion"] = verificar(parsed, corpus)
    inf["respaldos_no_verificables"] = inf["verificacion"]["no_literales"]
    propias = set(unidad["oraciones"])
    recibidas = {r["n"] for r in corpus}
    fuera, no_recibidas = [], []
    for ruta, fr in fragmentos(parsed):
        o = fr.get("o")
        if o not in propias:
            (fuera if o in recibidas else no_recibidas).append(
                {"ruta": ruta, "o": o, "f": fr.get("f")})
    inf["citas_fuera_de_la_unidad"] = fuera
    inf["citas_de_oraciones_no_recibidas"] = no_recibidas
    return inf


def construir(doc_path, salida_path, entrada, unidad_n):
    texto_numerado, registros, unidades = cargar(doc_path, salida_path)
    plantilla = CANDIDATO.read_text(encoding="utf-8")
    if plantilla.count(MARCADOR_TEXTO) != 1 or plantilla.count(MARCADOR_CONTEXTO) != 1:
        raise SystemExit("el candidato debe tener un único {{TEXTO_NUMERADO}} y un único {{CONTEXTO}}")
    for u in unidades:
        if u["id"] != f"U{unidad_n}":
            continue
        contexto = bloque_contexto(entrada, u, texto_numerado)
        enviado = plantilla.replace(MARCADOR_TEXTO, u["texto"]).replace(MARCADOR_CONTEXTO, contexto)
        return {"doc": doc_path, "salida": salida_path, "unidad": u, "registros": registros,
                "texto_enviado": u["texto"], "contexto_enviado": contexto,
                "prompt_enviado": enviado, "entrada": entrada}
    raise SystemExit(f"no encuentro la unidad U{unidad_n} ({len(unidades)} unidades)")


def seco(doc_path, salida_path, unidad_n):
    for entrada in ENTRADAS:
        caso = construir(doc_path, salida_path, entrada, unidad_n)
        u = caso["unidad"]
        inf = informe(None, u, caso["registros"], entrada)
        print(f"=== entrada ({entrada}) · {u['id']} · oraciones {u['oraciones']} · "
              f"referencias {len(u['referencias'])} ===")
        print(f"unidad: {len(caso['texto_enviado'])} bytes | contexto: "
              f"{len(caso['contexto_enviado'])} bytes | prompt: {len(caso['prompt_enviado'])} bytes")
        print(f"corpus de verificación: {inf['oraciones_enviadas']}")
        print(caso["contexto_enviado"] or "(sin contexto)")
        print("(modo seco: no se llama al modelo)\n")


MARCA_ORACION = re.compile(r"\[(\d+)\]\s*")
CABECERA_DOCUMENTO = "DOCUMENTO COMPLETO NUMERADO"


def registros_desde_texto(texto):
    """Reconstruye [{"n","oracion"}] de un material numerado ya guardado."""
    partes = MARCA_ORACION.split(texto)
    if len(partes) % 2 != 1:
        raise SystemExit("material numerado mal formado")
    return [{"n": int(partes[i]), "oracion": partes[i + 1].strip()}
            for i in range(1, len(partes), 2)]


def unidad_desde_crudo(crudo):
    """La unidad tal como se envió, sin el documento ni la salida de v9 a mano."""
    return {"id": crudo.get("unidad", "?"), "oraciones": crudo["oraciones"],
            "referencias": crudo.get("referencias") or [],
            "registros": registros_desde_texto(crudo["texto_enviado"]),
            "texto": crudo["texto_enviado"]}


def registros_documento(crudo):
    """El documento numerado de (c), tal como se envió en el contexto."""
    cabecera, _, cuerpo = (crudo.get("contexto_enviado") or "").partition("\n")
    if CABECERA_DOCUMENTO not in cabecera:
        raise SystemExit("la entrada (c) no trae el documento numerado en el contexto")
    return registros_desde_texto(cuerpo)


def revisar_crudo(ruta):
    """Re-verifica un crudo guardado sin llamar a ningún modelo."""
    ruta = pathlib.Path(ruta)
    crudo = json.loads(ruta.read_text(encoding="utf-8"))
    unidad = unidad_desde_crudo(crudo)
    entrada = crudo.get("entrada")
    registros = registros_documento(crudo) if entrada == "c" else unidad["registros"]
    problemas = []
    cuenta_texto = crudo["prompt_enviado"].count(crudo["texto_enviado"])
    if entrada in ("a", "b") and cuenta_texto != 1:
        problemas.append("el texto enviado no aparece exactamente una vez en el prompt")
    if entrada == "c":
        if cuenta_texto < 1:
            problemas.append("el texto enviado no aparece en el prompt")
        en_documento = {r["n"] for r in registros_documento(crudo)}
        faltan = [n for n in crudo["oraciones"] if n not in en_documento]
        if faltan:
            problemas.append(f"el documento del contexto no trae las oraciones {faltan}")
    if crudo.get("contexto_enviado") and crudo["prompt_enviado"].count(crudo["contexto_enviado"]) != 1:
        problemas.append("el contexto enviado no aparece exactamente una vez en el prompt")
    if [r["n"] for r in unidad["registros"]] != list(crudo["oraciones"]):
        problemas.append("las oraciones guardadas no coinciden con el texto enviado")
    guardado = crudo.get("informe") or {}
    nuevo = informe(crudo.get("parsed"), unidad, registros, entrada)
    return {
        "archivo": ruta.name, "entrada": entrada, "unidad": unidad["id"],
        "modelo": crudo.get("modelo"), "rep": crudo.get("rep"),
        "modelo_efectivo": crudo.get("modelo_efectivo"),
        "sha256_prompt": hashlib.sha256(crudo["prompt_enviado"].encode("utf-8")).hexdigest(),
        "problemas": problemas, "informe_igual": nuevo == guardado,
        "nuevo": nuevo, "guardado": guardado,
    }


def verificar_lista(rutas):
    malos = 0
    for ruta in rutas:
        v = revisar_crudo(ruta)
        inf = v["nuevo"]
        ok = not v["problemas"] and v["informe_igual"]
        if not ok:
            malos += 1
        print(f"{'ok' if ok else 'REVISAR'} {v['archivo']} | entrada ({v['entrada']}) "
              f"{v['unidad']} | modelo {v['modelo']} ({v['modelo_efectivo']}) | "
              f"prompt {v['sha256_prompt'][:12]} | "
              f"literales {len(inf.get('respaldos_no_verificables') or [])} | "
              f"fuera_unidad {len(inf.get('citas_fuera_de_la_unidad') or [])} | "
              f"informe {'igual' if v['informe_igual'] else 'DISTINTO'}")
        for problema in v["problemas"]:
            print("    - " + problema)
        if not v["informe_igual"]:
            for clave in sorted(set(inf) | set(v["guardado"])):
                if inf.get(clave) != v["guardado"].get(clave):
                    print(f"    - informe[{clave}]: guardado="
                          f"{str(v['guardado'].get(clave))[:120]} | nuevo="
                          f"{str(inf.get(clave))[:120]}")
    print(f"\n{len(rutas)} crudo(s) revisado(s); {malos} con diferencias o incoherencias.")
    return malos


def correr(doc_path, salida_path, modelo, rep, entrada):
    if entrada not in ENTRADAS:
        raise SystemExit(f"entrada desconocida: {entrada} (a|b|c)")
    texto_numerado, registros, unidades = cargar(doc_path, salida_path)
    plantilla = CANDIDATO.read_text(encoding="utf-8")
    CACHE.mkdir(exist_ok=True)
    etiqueta = doc_path.stem
    for u in unidades:
        destino = CACHE / f"comp-{etiqueta}-{entrada}-{u['id'].lower()}-{modelo}-{rep}.json"
        if destino.exists():
            print(f"crudo ya existe, salto ({destino})")
            continue
        contexto = bloque_contexto(entrada, u, texto_numerado)
        enviado = plantilla.replace(MARCADOR_TEXTO, u["texto"]).replace(MARCADOR_CONTEXTO, contexto)
        t0 = time.time()
        body, resp = call_model("toulmin", modelo, enviado)
        segundos = round(time.time() - t0, 1)
        parsed, cerca, error = extract_json(resp["choices"][0]["message"]["content"])
        inf = informe(parsed, u, registros, entrada)
        usage = resp.get("usage") or {}
        detalles = usage.get("completion_tokens_details") or {}
        crudo = {
            "doc": str(doc_path), "salida_v9": str(salida_path), "modelo": modelo,
            "rep": rep, "entrada": entrada, "segundos": segundos,
            "unidad": u["id"], "subtema": u["subtema"], "oraciones": u["oraciones"],
            "referencias": u["referencias"], "texto_enviado": u["texto"],
            "contexto_enviado": contexto, "prompt_enviado": enviado,
            "request": body,
            "response": {k: v for k, v in resp.items() if k != "_stream_chunks_crudos"},
            "modelo_efectivo": resp.get("model"),
            "tokens": {"entrada": usage.get("prompt_tokens"),
                       "salida": usage.get("completion_tokens"),
                       "razonamiento": detalles.get("reasoning_tokens")},
            "frames_sse": len(resp.get("_stream_chunks_crudos", [])),
            "nota_frames": "los frames SSE no se guardan: son transporte",
            "parsed": parsed, "venia_con_cerca": cerca, "error_parseo": error,
            "informe": inf,
        }
        with destino.open("x", encoding="utf-8") as f:
            json.dump(crudo, f, ensure_ascii=False, indent=2)
        print(f"{u['id']} ({entrada}): {segundos} s | {crudo['modelo_efectivo']} | "
              f"tokens {crudo['tokens']} | no verificables "
              f"{len(inf.get('respaldos_no_verificables', []))} | fuera de la unidad "
              f"{len(inf.get('citas_fuera_de_la_unidad', []))} | → {destino}")


def _linea(items, formato):
    return " | ".join(formato(i) for i in items) if items else "—"


def digest(parsed):
    """Resumen compacto de la ficha, para evaluar sin volcar el JSON entero."""
    if not isinstance(parsed, dict):
        return ["(sin JSON)"]
    casos = {c.get("id"): c.get("nombre") for c in parsed.get("casos", [])}
    return [
        "casos: " + _linea(parsed.get("casos", []),
                           lambda c: f"{c.get('id')}={c.get('nombre')}"),
        "determ: " + _linea(parsed.get("determinaciones", []), lambda d: (
            f"{d.get('id')}[{casos.get(d.get('caso'), d.get('caso'))}·{d.get('aspecto')}="
            f"{d.get('valor')}"
            + (f" (cond {'; '.join(x.get('texto', '') for x in d['condiciones'])})"
               if d.get("condiciones") else "")
            + (f" dentro_de {d.get('dentro_de')}" if d.get("dentro_de") else "")
            + (f" cambio={d.get('cambio')}" if d.get("cambio") else "")
            + (" inferido" if d.get("inferido") else "") + "]")),
        "capas: " + _linea(parsed.get("capas", []),
                           lambda k: f"{k.get('id')}«{k.get('expresion')}» quien={k.get('quien')}"
                           + (f" dentro_de {k.get('dentro_de')}" if k.get("dentro_de") else "")),
        "acciones: " + _linea(parsed.get("acciones", []), lambda a: (
            f"{a.get('id')}[{a.get('agente')}·{a.get('accion')}·obj={a.get('objeto')}"
            + (f" cond {'; '.join(x.get('texto', '') for x in a['condiciones'])}"
               if a.get("condiciones") else "")
            + (f" dentro_de {a.get('dentro_de')}" if a.get("dentro_de") else "")
            + (" negada" if a.get("negada") else "") + "]")),
        "relaciones: " + _linea(parsed.get("relaciones", []), lambda r: (
            f"{r.get('id')}[{r.get('tipo')}: {r.get('de')}→{r.get('a')}"
            + (f" dentro_de {r.get('dentro_de')}" if r.get("dentro_de") else "")
            + (" inferido" if r.get("inferido") else "") + "]")),
        "marcas: " + _linea(parsed.get("marcas", []), lambda m: (
            f"«{m.get('marca')}»@{m.get('o')}=" + ",".join(
                f"{f.get('funcion')}→{f.get('refs')}" for f in m.get("funciones", [])))),
        "dudas: " + _linea(parsed.get("dudas", []), lambda q: f"{q.get('id')}«{q.get('texto')}»"),
    ]


def resumen(doc_path, salida_path, modelo, rep):
    """Los tres brazos de cada unidad, uno al lado del otro, para evaluar."""
    _, _, unidades = cargar(doc_path, salida_path)
    etiqueta = doc_path.stem
    for u in unidades:
        print(f"\n{'=' * 78}\n{u['id']} oraciones {u['oraciones']} · {u['subtema']}\n{'=' * 78}")
        for entrada in ENTRADAS:
            ruta = CACHE / f"comp-{etiqueta}-{entrada}-{u['id'].lower()}-{modelo}-{rep}.json"
            print(f"--- ({entrada}) ---")
            if not ruta.exists():
                print(f"   falta {ruta.name}")
                continue
            c = json.loads(ruta.read_text(encoding="utf-8"))
            inf = c["informe"]
            print(f"   {c['segundos']} s | {c['modelo_efectivo']} | tokens {c['tokens']} | "
                  f"no verificables {len(inf.get('respaldos_no_verificables', []))} | "
                  f"fuera de la unidad {len(inf.get('citas_fuera_de_la_unidad', []))} | "
                  f"no recibidas {len(inf.get('citas_de_oraciones_no_recibidas', []))}")
            for linea in digest(c.get("parsed")):
                print("   " + linea)


def comparar(doc_path, salida_path, rep, unidad_n=None):
    """Los tres brazos de cada unidad, en los dos modelos que corrieron."""
    _, _, unidades = cargar(doc_path, salida_path)
    etiqueta = doc_path.stem
    for u in unidades:
        if unidad_n and u["id"] != f"U{unidad_n}":
            continue
        print(f"\n{'=' * 78}\n{u['id']} oraciones {u['oraciones']} · {u['subtema']}\n{'=' * 78}")
        if u["referencias"]:
            print("referencias de v9: " + _linea(
                u["referencias"], lambda r: f"[{r['oracion']}]«{r['expresion']}»→"
                f"{r['referente'] if r.get('referente') else 'SIN RESOLVER'}"))
        for modelo in ("muse", "deepseek"):
            for entrada in ENTRADAS:
                ruta = CACHE / f"comp-{etiqueta}-{entrada}-{u['id'].lower()}-{modelo}-{rep}.json"
                print(f"--- {modelo} ({entrada}) ---")
                if not ruta.exists():
                    print(f"   falta {ruta.name}")
                    continue
                c = json.loads(ruta.read_text(encoding="utf-8"))
                inf = c["informe"]
                print(f"   {c.get('segundos')} s | {c.get('modelo_efectivo')} | tokens "
                      f"{c.get('tokens')} | no verificables "
                      f"{len(inf.get('respaldos_no_verificables', []))} | fuera de la unidad "
                      f"{len(inf.get('citas_fuera_de_la_unidad', []))}")
                for linea in digest(c.get("parsed")):
                    print("   " + linea)


def main(argv):
    if len(argv) < 2:
        raise SystemExit(__doc__)
    modo = argv[1]
    if modo in ("verificar", "verificar-todos"):
        if modo == "verificar":
            if len(argv) < 3:
                raise SystemExit("uso: verificar <crudo.json> [...]")
            rutas = argv[2:]
        else:
            patron = argv[2] if len(argv) > 2 else str(CACHE / "comp-*.json")
            rutas = sorted(globmod.glob(patron))
            if not rutas:
                raise SystemExit(f"sin crudos para {patron}")
        if verificar_lista(rutas):
            raise SystemExit("hay crudos con diferencias o incoherencias")
        return
    if len(argv) < 5:
        raise SystemExit(__doc__)
    doc_path, salida_path = pathlib.Path(argv[2]), pathlib.Path(argv[3])
    for p in (doc_path, salida_path):
        if not p.exists():
            raise SystemExit(f"no existe: {p}")
    if modo == "seco":
        seco(doc_path, salida_path, argv[4])
    elif modo == "correr":
        if len(argv) != 7:
            raise SystemExit("uso: correr <doc> <salida_v9> <modelo> <rN> <entrada>")
        correr(doc_path, salida_path, argv[4], argv[5], argv[6])
    elif modo == "resumen":
        if len(argv) != 6:
            raise SystemExit("uso: resumen <doc> <salida_v9> <modelo> <rN>")
        resumen(doc_path, salida_path, argv[4], argv[5])
    elif modo == "comparar":
        if len(argv) not in (5, 6):
            raise SystemExit("uso: comparar <doc> <salida_v9> <rN> [<unidad_n>]")
        comparar(doc_path, salida_path, argv[4], argv[5] if len(argv) == 6 else None)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
