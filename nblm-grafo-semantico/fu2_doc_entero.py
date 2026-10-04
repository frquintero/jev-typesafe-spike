"""FU2 (exploratoria): ficha_v1 del documento entero con NotebookLM, una pregunta.

Uso: <venv>/bin/python nblm-grafo-semantico/fu2_doc_entero.py <doc> <prompt> <rN> --storage <state>
Un cuaderno, una fuente (el texto numerado completo), reglas en chat.configure
(goal CUSTOM, longitud por defecto), una pregunta. Cronometra la pregunta y cada
fragmento del flujo HTTP; guarda solo los hitos (razonamiento y herramientas con su hora).
"""
import argparse, asyncio, dataclasses, datetime as dt, enum, json, os, sys, time
from pathlib import Path
import httpx
from unidades_comun import MARCADOR, ROOT, UNIDADES
from extraer_unidades import numerar_oraciones
from run_niveles import extract_json
from ficha_doc import verificar
from hitos_flujo import hitos
from notebooklm import NotebookLMClient
from notebooklm._types.enums import ChatGoal
from notebooklm.options import ClientConfig, FeatureOptions, RetryOptions, WebBackendConfig
from notebooklm._web.transport.session_auth import WebSessionAuth

REMISION = "El texto con sus oraciones numeradas es la fuente de este cuaderno."
PREGUNTA = ("Reconstruye la ficha JSON del texto de la fuente, según tus "
            "instrucciones. Responde solo con el JSON.")
FLUJO = {"activo": False, "t0": None, "fragmentos": []}
_orig = httpx.Response.aiter_bytes


async def _aiter_cronometrado(self, *a, **k):
    async for ch in _orig(self, *a, **k):
        if FLUJO["activo"]:
            FLUJO["fragmentos"].append({"t": round(time.monotonic() - FLUJO["t0"], 3),
                                        "bytes": len(ch), "texto": ch.decode("utf-8", "replace")})
        yield ch

httpx.Response.aiter_bytes = _aiter_cronometrado


async def stop_refresh(self, expected_epoch):
    raise RuntimeError("AUTH_STOP")


def convert(v):
    if dataclasses.is_dataclass(v): return dataclasses.asdict(v)
    if isinstance(v, enum.Enum): return v.value
    return str(v)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("doc"); ap.add_argument("prompt"); ap.add_argument("rep")
    ap.add_argument("--storage", type=Path, required=True); a = ap.parse_args()
    out = ROOT / "cache" / f"fu2-{a.doc}-nblm-{a.prompt}-{a.rep}.json"
    if out.exists(): raise SystemExit(f"crudo ya existe ({out})")
    texto = (UNIDADES / "docs" / f"{a.doc}.md").read_text(encoding="utf-8")
    numerado, registros = numerar_oraciones(texto)
    custom = (UNIDADES / "prompts" / f"{a.prompt}.md").read_text(encoding="utf-8").replace(MARCADOR, REMISION)
    WebSessionAuth.refresh_base = stop_refresh
    os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"] = "1"; os.environ["NOTEBOOKLM_HEADLESS_REAUTH"] = "0"
    crudo = {"doc": a.doc, "prompt": a.prompt, "rep": a.rep, "inicio_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
             "custom_prompt_enviado": custom, "pregunta_enviada": PREGUNTA, "texto_numerado": numerado, "etapas": {}}

    async def run():
        cfg = ClientConfig(backend=WebBackendConfig(),
                           retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0),
                           features=FeatureOptions(chat_timeout=600))
        async with NotebookLMClient.from_storage(str(a.storage), allow_headless=False, config=cfg) as c:
            if c.get_account_authuser() != 0: raise RuntimeError("Wrong account")
            async def etapa(n, f):
                t = time.monotonic(); v = await f(); crudo["etapas"][n] = round(time.monotonic() - t, 3)
                print(json.dumps({n: crudo["etapas"][n]}), flush=True); return v
            nb = await etapa("crear", lambda: c.notebooks.create(f"FU2 {a.doc} {a.rep} {crudo['inicio_utc']}"))
            crudo["notebook_id"] = nb.id
            await etapa("configurar", lambda: c.chat.configure(nb.id, goal=ChatGoal.CUSTOM, custom_prompt=custom))
            src = await etapa("cargar", lambda: c.sources.add_text(nb.id, a.doc, numerado))
            await etapa("lista", lambda: c.sources.wait_until_ready(nb.id, src.id, timeout=120))
            FLUJO["t0"] = time.monotonic(); FLUJO["activo"] = True
            r = await etapa("preguntar", lambda: c.chat.ask(nb.id, PREGUNTA))
            FLUJO["activo"] = False
            crudo["respuesta"] = r.answer; crudo["referencias"] = r.references

    t0 = time.monotonic()
    try:
        asyncio.run(run()); crudo["completed"] = True
    except Exception as e:
        crudo["completed"] = False; crudo["error"] = f"{type(e).__name__}: {str(e)[:400]}"
    crudo["segundos_total"] = round(time.monotonic() - t0, 3)
    fr = FLUJO["fragmentos"]
    crudo["flujo_hitos"], crudo["flujo_resumen"] = hitos(fr)  # solo hitos, no el flujo entero
    if fr:
        crudo["primer_fragmento_s"] = fr[0]["t"]; crudo["ultimo_fragmento_s"] = fr[-1]["t"]
        crudo["fragmentos_n"] = len(fr); crudo["flujo_bytes"] = sum(x["bytes"] for x in fr)
    if crudo.get("respuesta"):
        p, cerca, err = extract_json(crudo["respuesta"])
        crudo.update(parsed=p, error_parseo=err, verificacion=verificar(p, registros) if isinstance(p, dict) else None)
    with out.open("x", encoding="utf-8") as f: json.dump(crudo, f, ensure_ascii=False, indent=2, default=convert)
    v = crudo.get("verificacion") or {}
    print(json.dumps({k: crudo.get(k) for k in ("completed", "error", "segundos_total", "etapas", "primer_fragmento_s",
          "ultimo_fragmento_s", "fragmentos_n", "flujo_bytes", "error_parseo")} |
          {"conteo": v.get("conteo"), "no_literales": len(v.get("no_literales", []))}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
