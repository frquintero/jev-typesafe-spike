#!/usr/bin/env python3
"""Una unidad × una entrada = una tarea de Muse, para la comparación del paso 2.

  python3 mvp/paso2/muse_unidad.py armar   <doc> <salida_v9> <unidad_n> <entrada> <etiqueta>
  python3 mvp/paso2/muse_unidad.py recoger <doc> <salida_v9> <unidad_n> <entrada> <etiqueta>

`armar` deja el mensaje en mvp/paso2/muse/mensaje_<etiqueta>.md y el meta de la
corrida en mvp/paso2/muse/corrida_<etiqueta>.json. `recoger` trae la salida de
~/.cache/muse_tareas/, la verifica con el corpus de la entrada y deja el crudo en
mvp/paso2/cache/comp-<doc>-<entrada>-u<n>-muse-<rN>.json. Nunca sobrescribe.
"""
import json
import pathlib
import sys

PASO2 = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(PASO2))
sys.path.insert(0, str(PASO2.parents[1] / "unidades"))

from comparacion import (CACHE, CANDIDATO, MARCADOR_CONTEXTO, MARCADOR_TEXTO,  # noqa: E402
                         bloque_contexto, cargar, informe)

MUSE_DIR = PASO2 / "muse"
SALIDA_MUSE = pathlib.Path.home() / ".cache" / "muse_tareas"

CABECERA = """TAREA
Ejecuta el prompt que va abajo. Es una llamada del paso 2 del repo
jev-typesafe-spike sobre una unidad temática de un documento sintético:
devuelve su salida y nada más.

NIVEL DE RAZONAMIENTO
high: hay que leer y decidir; no es mecánico.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `mvp/paso2/prompt_ficha_contexto.md`, con
`{{TEXTO_NUMERADO}}` y `{{CONTEXTO}}` ya sustituidos; esto es exactamente lo que
recibe el modelo)
---------------------------------------------------------------------

"""


def unidad_y_prompt(doc_path, salida_path, unidad_n):
    texto_numerado, registros, unidades = cargar(doc_path, salida_path)
    for u in unidades:
        if u["id"] == f"U{unidad_n}":
            return texto_numerado, registros, u
    raise SystemExit(f"no encuentro la unidad U{unidad_n}")


def armar(doc_path, salida_path, unidad_n, entrada, etiqueta):
    texto_numerado, registros, u = unidad_y_prompt(doc_path, salida_path, unidad_n)
    plantilla = CANDIDATO.read_text(encoding="utf-8")
    contexto = bloque_contexto(entrada, u, texto_numerado)
    enviado = plantilla.replace(MARCADOR_TEXTO, u["texto"]).replace(MARCADOR_CONTEXTO, contexto)
    mensaje = CABECERA + enviado
    MUSE_DIR.mkdir(exist_ok=True)
    (MUSE_DIR / f"mensaje_{etiqueta}.md").write_text(mensaje, encoding="utf-8")
    meta = {"etiqueta": etiqueta, "doc": str(doc_path), "salida_v9": str(salida_path),
            "unidad": u["id"], "entrada": entrada, "subtema": u["subtema"],
            "oraciones": u["oraciones"], "referencias": len(u["referencias"]),
            "bytes_mensaje": len(mensaje)}
    (MUSE_DIR / f"corrida_{etiqueta}.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"mensaje: mvp/paso2/muse/mensaje_{etiqueta}.md ({len(mensaje)} bytes) | "
          f"{u['id']} ({entrada})")


def _tokens_de_sesion(session_id):
    """Best effort: tokens de la sesión de Muse, si el diario los trae."""
    if not session_id:
        return None
    base = pathlib.Path.home() / ".local" / "share" / "muse" / "sessions"
    candidatos = list(base.glob(f"*/*/*/{session_id}/session.jsonl"))
    if not candidatos:
        return None
    vistos = {}
    for linea in candidatos[0].read_text(encoding="utf-8", errors="replace").splitlines():
        try:
            payload = json.loads(linea)
        except Exception:
            continue
        for k in ("input_tokens", "output_tokens", "reasoning_tokens", "total_tokens"):
            if isinstance(payload.get(k), int):
                vistos[k] = max(vistos.get(k, 0), payload[k])
            uso = payload.get("usage")
            if isinstance(uso, dict) and isinstance(uso.get(k), int):
                vistos[k] = max(vistos.get(k, 0), uso[k])
    return vistos or None


def recoger(doc_path, salida_path, unidad_n, entrada, etiqueta):
    meta_path = MUSE_DIR / f"corrida_{etiqueta}.json"
    if not meta_path.exists():
        raise SystemExit(f"falta {meta_path}: corre primero `armar`")
    for ext in ("out", "json", "jsonl", "err"):
        if not (SALIDA_MUSE / f"{etiqueta}.{ext}").exists():
            raise SystemExit(f"falta {SALIDA_MUSE / f'{etiqueta}.{ext}'}")
    _, registros, unidades = cargar(doc_path, salida_path)
    u = next((x for x in unidades if x["id"] == f"U{unidad_n}"), None)
    if u is None:
        raise SystemExit(f"no encuentro la unidad U{unidad_n}")
    salida = (SALIDA_MUSE / f"{etiqueta}.out").read_text(encoding="utf-8").strip()
    meta = json.loads((SALIDA_MUSE / f"{etiqueta}.json").read_text(encoding="utf-8"))
    sys.path.insert(0, str(PASO2.parents[1] / "unidades"))
    from run_niveles import extract_json  # noqa: E402
    parsed, cerca, error = extract_json(salida)
    inf = informe(parsed, u, registros, entrada)
    for ext in ("out", "jsonl", "err", "json"):
        origen = SALIDA_MUSE / f"{etiqueta}.{ext}"
        if origen.exists():
            (MUSE_DIR / f"{etiqueta}.{ext}").write_text(
                origen.read_text(encoding="utf-8", errors="replace"), encoding="utf-8")
    texto_numerado, _, _ = cargar(doc_path, salida_path)
    contexto = bloque_contexto(entrada, u, texto_numerado)
    plantilla = CANDIDATO.read_text(encoding="utf-8")
    enviado = plantilla.replace(MARCADOR_TEXTO, u["texto"]).replace(MARCADOR_CONTEXTO, contexto)
    modelo_muse = {"etiqueta": etiqueta, "session_id": meta.get("session_id"),
                   "esfuerzo": meta.get("esfuerzo"), "exit": meta.get("exit"),
                   "segundos": meta.get("segundos"), "inicio": meta.get("inicio")}
    rep = etiqueta.rsplit("-", 1)[-1]
    if not (rep.startswith("r") and rep[1:].isdigit()):
        rep = "r1"
    crude = {
        "doc": str(doc_path), "salida_v9": str(salida_path), "modelo": "muse",
        "rep": rep, "entrada": entrada,
        "segundos": meta.get("segundos"), "unidad": u["id"], "subtema": u["subtema"],
        "oraciones": u["oraciones"], "referencias": u["referencias"],
        "texto_enviado": u["texto"], "contexto_enviado": contexto,
        "prompt_enviado": enviado,
        "mensaje_enviado": (MUSE_DIR / f"mensaje_{etiqueta}.md").read_text(encoding="utf-8"),
        "salida_cruda": salida, "parsed": parsed, "venia_con_cerca": cerca,
        "error_parseo": error, "informe": inf, "meta_muse": modelo_muse,
        "tokens": _tokens_de_sesion(meta.get("session_id")),
        "modelo_efectivo": "muse-code",
    }
    CACHE.mkdir(exist_ok=True)
    destino = CACHE / f"comp-{doc_path.stem}-{entrada}-{u['id'].lower()}-muse-{crude['rep']}.json"
    if destino.exists():
        raise SystemExit(f"crudo ya existe, no lo sobrescribo ({destino})")
    destino.write_text(json.dumps(crude, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{u['id']} ({entrada}): {meta.get('segundos')} s | parseo "
          f"{'ok' if parsed else 'FALLO'} | exit {meta.get('exit')} | no verificables "
          f"{len(inf.get('respaldos_no_verificables', []))} | fuera de la unidad "
          f"{len(inf.get('citas_fuera_de_la_unidad', []))} | → {destino}")


def main(argv):
    if len(argv) != 7:
        raise SystemExit(__doc__)
    modo, doc, salida, unidad_n, entrada, etiqueta = argv[1:]
    doc_path, salida_path = pathlib.Path(doc), pathlib.Path(salida)
    if modo == "armar":
        armar(doc_path, salida_path, unidad_n, entrada, etiqueta)
    elif modo == "recoger":
        recoger(doc_path, salida_path, unidad_n, entrada, etiqueta)
    else:
        raise SystemExit(__doc__)


if __name__ == "__main__":
    main(sys.argv)
