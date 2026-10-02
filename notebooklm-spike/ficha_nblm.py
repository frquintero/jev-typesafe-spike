"""Ficha con NotebookLM: el mismo prompt y texto que unidades/ficha_doc.py, otro extractor.

Uso (desde la raíz, sin HTTPS_PROXY):
  python notebooklm-spike/ficha_nblm.py <doc> <prompt> <rN> --storage <storage_state.json>

Crea un cuaderno nuevo, carga el texto numerado (misma numeración que ficha_doc) como
fuente, hace una sola pregunta con el prompt (la sección TEXTO remite a la fuente),
saca el JSON de la respuesta y aplica el mismo verificador de ficha_doc. No juzga el
contenido. Crudo único: cache/ficha-<doc>-nblm-<prompt>-<rN>.json (no se sobrescribe).
"""
import argparse
import asyncio
import dataclasses
import datetime as dt
import enum
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNIDADES = ROOT.parent / "unidades"
sys.path.insert(0, str(ROOT.parent / "niveles"))
sys.path.insert(0, str(UNIDADES))
from extraer_unidades import numerar_oraciones  # noqa: E402
from run_niveles import extract_json  # noqa: E402
from ficha_doc import verificar  # noqa: E402

from notebooklm import NotebookLMClient  # noqa: E402
from notebooklm.options import ClientConfig, FeatureOptions, RetryOptions, WebBackendConfig  # noqa: E402
from notebooklm._web.transport.session_auth import WebSessionAuth  # noqa: E402

ACCOUNT = 0
MARCADOR = "{{TEXTO_NUMERADO}}"
REMISION = "El texto con sus oraciones numeradas es la fuente de este cuaderno."


async def stop_refresh(self, expected_epoch):
    raise RuntimeError("AUTH_STOP: automatic authentication recovery disabled")


def convert(value):
    if dataclasses.is_dataclass(value):
        return dataclasses.asdict(value)
    if isinstance(value, enum.Enum):
        return value.value
    return str(value)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc"); ap.add_argument("prompt"); ap.add_argument("rep")
    ap.add_argument("--storage", type=Path, required=True)
    a = ap.parse_args()
    storage = a.storage.resolve()
    if storage.is_relative_to(ROOT.parent):
        ap.error("storage must be outside the repository")
    out = ROOT / "cache" / f"ficha-{a.doc}-nblm-{a.prompt}-{a.rep}.json"
    if out.exists():
        raise SystemExit(f"crudo ya existe, me detengo ({out})")
    state = json.loads(storage.read_text())
    if state.get("notebooklm", {}).get("account", {}).get("authuser") != ACCOUNT:
        raise SystemExit(f"Expected account {ACCOUNT}")

    texto = (UNIDADES / "docs" / f"{a.doc}.md").read_text(encoding="utf-8")
    prompt = (UNIDADES / "prompts" / f"{a.prompt}.md").read_text(encoding="utf-8")
    if prompt.count(MARCADOR) != 1:
        raise SystemExit("el prompt debe tener un único {{TEXTO_NUMERADO}}")
    texto_numerado, registros = numerar_oraciones(texto)
    pregunta = prompt.replace(MARCADOR, REMISION)

    WebSessionAuth.refresh_base = stop_refresh
    os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"] = "1"
    os.environ["NOTEBOOKLM_HEADLESS_REAUTH"] = "0"
    os.environ.pop("NOTEBOOKLM_REFRESH_CMD", None)

    crudo = {"doc": a.doc, "modelo": "notebooklm (Gemini Notebook, modelo no expuesto)",
             "cliente": "notebooklm-py==0.8.4", "prompt": a.prompt, "rep": a.rep,
             "inicio_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
             "texto_numerado": texto_numerado, "oraciones_numeradas": registros,
             "pregunta_enviada": pregunta, "etapas": {}, "completed": False}

    async def run():
        cfg = ClientConfig(backend=WebBackendConfig(),
                           retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0),
                           features=FeatureOptions(chat_timeout=600))
        async with NotebookLMClient.from_storage(str(storage), allow_headless=False, config=cfg) as c:
            if c.get_account_authuser() != ACCOUNT:
                raise RuntimeError("Wrong account route")

            async def etapa(nombre, call):
                t = time.monotonic(); v = await call()
                crudo["etapas"][nombre] = round(time.monotonic() - t, 3)
                print(json.dumps({nombre: crudo["etapas"][nombre]}), flush=True)
                return v

            titulo = f"FICHA {a.doc} {a.prompt} {a.rep} {crudo['inicio_utc']}"
            nb = await etapa("crear", lambda: c.notebooks.create(titulo))
            crudo["notebook_id"] = nb.id
            src = await etapa("cargar", lambda: c.sources.add_text(nb.id, a.doc, texto_numerado))
            crudo["source_id"] = src.id
            await etapa("lista", lambda: c.sources.wait_until_ready(nb.id, src.id, timeout=120))
            full = await etapa("texto", lambda: c.sources.get_fulltext(nb.id, src.id))
            crudo["fuente_igual_al_texto_numerado"] = full.content.strip() == texto_numerado.strip()
            r = await etapa("preguntar", lambda: c.chat.ask(nb.id, pregunta, source_ids=[src.id]))
            crudo["respuesta"] = r.answer
            crudo["conversation_id"] = r.conversation_id
            crudo["referencias"] = r.references
            crudo["raw_response"] = r.raw_response

    t0 = time.monotonic()
    try:
        asyncio.run(run())
        crudo["completed"] = True
    except Exception as exc:
        crudo["error"] = {"type": type(exc).__name__, "message": str(exc)[:500]}
    crudo["segundos_total"] = round(time.monotonic() - t0, 3)
    if "respuesta" in crudo:
        parsed, cerca, err = extract_json(crudo["respuesta"])
        crudo.update(parsed=parsed, venia_con_cerca=cerca, error_parseo=err,
                     verificacion=verificar(parsed, registros) if isinstance(parsed, dict) else None)
    with out.open("x", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2, default=convert)
    resumen = {k: crudo.get(k) for k in ("completed", "error", "segundos_total", "etapas",
                                          "fuente_igual_al_texto_numerado", "venia_con_cerca", "error_parseo")}
    v = crudo.get("verificacion")
    if v:
        resumen.update(fragmentos=v["fragmentos"], no_literales=len(v["no_literales"]),
                       listas_faltantes=v["listas_faltantes"], conteo=v["conteo"])
    print(f"hecho -> {out}")
    print(json.dumps(resumen, ensure_ascii=False, indent=2))
    return 0 if crudo["completed"] else 1


if __name__ == "__main__":
    sys.exit(main())
