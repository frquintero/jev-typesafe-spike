"""FU1, lado NotebookLM: ficha (mismo prompt) por unidad, por el chat.

Uso (desde la raíz, sin HTTPS_PROXY ni SSL_CERT_FILE):
  <venv>/bin/python nblm-grafo-semantico/ficha_unidad_nblm.py <doc> <prompt> <rN> <crudo_paso1>
      --storage <storage_state.json> --sonda-unidad Ux --sonda-pregunta "..."

Un cuaderno nuevo. Las reglas (el prompt, con su sección TEXTO remitida a la
fuente) van en chat.configure (goal CUSTOM, respuesta LONGER). Cada unidad es
una fuente aparte, con sus números de oración originales. Una pregunta corta
por unidad con source_ids=[esa unidad]; tras cada una se borra la conversación
para que la siguiente no herede historial. Al final, una sonda de aislamiento:
una pregunta cuya respuesta está en otra unidad, con source_ids=[sonda-unidad].
Comprueba por código que las citas apuntan solo a la fuente seleccionada y
aplica el verificador de unidades/ficha_doc.py. No juzga el contenido.
Crudo único: nblm-grafo-semantico/cache/fu-<doc>-nblm-<prompt>-<rN>.json
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

from unidades_comun import MARCADOR, ROOT, UNIDADES, cargar_unidades
from run_niveles import extract_json  # noqa: E402
from ficha_doc import verificar  # noqa: E402

from notebooklm import NotebookLMClient  # noqa: E402
from notebooklm._types.enums import ChatGoal, ChatResponseLength  # noqa: E402
from notebooklm.options import ClientConfig, FeatureOptions, RetryOptions, WebBackendConfig  # noqa: E402
from notebooklm._web.transport.session_auth import WebSessionAuth  # noqa: E402

ACCOUNT = 0
REMISION = "El texto con sus oraciones numeradas es la fuente seleccionada en cada pregunta."
PREGUNTA = ("Reconstruye la ficha JSON del texto de la fuente seleccionada, según tus "
            "instrucciones. Responde solo con el JSON.")
LIMITE_CUSTOM = 10000


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
    ap.add_argument("crudo_paso1")
    ap.add_argument("--storage", type=Path, required=True)
    ap.add_argument("--sonda-unidad", required=True)
    ap.add_argument("--sonda-pregunta", required=True)
    a = ap.parse_args()
    storage = a.storage.resolve()
    if storage.is_relative_to(ROOT.parent):
        ap.error("storage must be outside the repository")
    out = ROOT / "cache" / f"fu-{a.doc}-nblm-{a.prompt}-{a.rep}.json"
    if out.exists():
        raise SystemExit(f"crudo ya existe, me detengo ({out})")
    state = json.loads(storage.read_text())
    if state.get("notebooklm", {}).get("account", {}).get("authuser") != ACCOUNT:
        raise SystemExit(f"Expected account {ACCOUNT}")

    prompt = (UNIDADES / "prompts" / f"{a.prompt}.md").read_text(encoding="utf-8")
    if prompt.count(MARCADOR) != 1:
        raise SystemExit("el prompt debe tener un único {{TEXTO_NUMERADO}}")
    custom = prompt.replace(MARCADOR, REMISION)
    if len(custom) > LIMITE_CUSTOM:
        raise SystemExit(f"custom_prompt de {len(custom)} caracteres > {LIMITE_CUSTOM}")
    unidades, _ = cargar_unidades(a.doc, a.crudo_paso1)
    if a.sonda_unidad not in {u["id"] for u in unidades}:
        raise SystemExit(f"sonda-unidad {a.sonda_unidad} no existe")

    WebSessionAuth.refresh_base = stop_refresh
    os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"] = "1"
    os.environ["NOTEBOOKLM_HEADLESS_REAUTH"] = "0"
    os.environ.pop("NOTEBOOKLM_REFRESH_CMD", None)

    crudo = {"doc": a.doc, "modelo": "notebooklm (Gemini Notebook, modelo no expuesto)",
             "cliente": "notebooklm-py==0.8.4", "prompt": a.prompt, "rep": a.rep,
             "crudo_paso1": a.crudo_paso1,
             "inicio_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
             "custom_prompt_enviado": custom, "custom_prompt_caracteres": len(custom),
             "pregunta_enviada": PREGUNTA, "etapas": {}, "unidades": [], "completed": False}

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

            titulo = f"FU {a.doc} {a.prompt} {a.rep} {crudo['inicio_utc']}"
            nb = await etapa("crear", lambda: c.notebooks.create(titulo))
            crudo["notebook_id"] = nb.id
            await etapa("configurar", lambda: c.chat.configure(
                nb.id, goal=ChatGoal.CUSTOM, response_length=ChatResponseLength.LONGER,
                custom_prompt=custom))
            fuentes = {}
            for u in unidades:
                nombre = f"{a.doc} {u['id']} (oraciones {', '.join(map(str, u['oraciones']))})"
                src = await etapa(f"cargar_{u['id']}", lambda: c.sources.add_text(nb.id, nombre, u["texto"]))
                fuentes[u["id"]] = src.id
            for u in unidades:
                sid = fuentes[u["id"]]
                await etapa(f"lista_{u['id']}", lambda: c.sources.wait_until_ready(nb.id, sid, timeout=120))
                full = await etapa(f"texto_{u['id']}", lambda: c.sources.get_fulltext(nb.id, sid))
                u["fuente_igual_al_texto"] = full.content.strip() == u["texto"].strip()
            for u in unidades:
                sid = fuentes[u["id"]]
                r = await etapa(f"preguntar_{u['id']}", lambda: c.chat.ask(nb.id, PREGUNTA, source_ids=[sid]))
                refs = [getattr(x, "source_id", None) for x in (r.references or [])]
                fila = {**u, "source_id": sid, "segundos": crudo["etapas"][f"preguntar_{u['id']}"],
                        "respuesta": r.answer, "conversation_id": r.conversation_id,
                        "referencias": r.references, "raw_response": r.raw_response,
                        "citas_total": len(refs),
                        "citas_fuera_de_la_unidad": [s for s in refs if s != sid]}
                crudo["unidades"].append(fila)
                await etapa(f"borrar_conv_{u['id']}", lambda: c.chat.delete_conversation(nb.id, r.conversation_id))
            sid = fuentes[a.sonda_unidad]
            r = await etapa("sonda", lambda: c.chat.ask(nb.id, a.sonda_pregunta, source_ids=[sid]))
            crudo["sonda"] = {"unidad": a.sonda_unidad, "source_id": sid, "pregunta": a.sonda_pregunta,
                              "respuesta": r.answer, "referencias": r.references,
                              "citas_fuera_de_la_unidad": [getattr(x, "source_id", None)
                                                           for x in (r.references or [])
                                                           if getattr(x, "source_id", None) != sid]}

    t0 = time.monotonic()
    try:
        asyncio.run(run())
        crudo["completed"] = True
    except Exception as exc:
        crudo["error"] = {"type": type(exc).__name__, "message": str(exc)[:500]}
    crudo["segundos_total"] = round(time.monotonic() - t0, 3)
    for u in crudo["unidades"]:
        parsed, cerca, err = extract_json(u["respuesta"] or "")
        u.update(parsed=parsed, venia_con_cerca=cerca, error_parseo=err,
                 verificacion=verificar(parsed, u["registros"]) if isinstance(parsed, dict) else None)
    with out.open("x", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2, default=convert)
    resumen = {"completed": crudo["completed"], "error": crudo.get("error"),
               "segundos_total": crudo["segundos_total"], "unidades": [
                   {"id": u["id"], "segundos": u["segundos"], "fuente_igual": u.get("fuente_igual_al_texto"),
                    "citas": u["citas_total"], "citas_fuera": len(u["citas_fuera_de_la_unidad"]),
                    "error_parseo": u["error_parseo"],
                    "no_literales": len(u["verificacion"]["no_literales"]) if u["verificacion"] else None,
                    "conteo": u["verificacion"]["conteo"] if u["verificacion"] else None}
                   for u in crudo["unidades"]],
               "sonda": {k: crudo.get("sonda", {}).get(k) for k in ("respuesta", "citas_fuera_de_la_unidad")}}
    print(f"hecho -> {out}")
    print(json.dumps(resumen, ensure_ascii=False, indent=2, default=convert))
    return 0 if crudo["completed"] else 1


if __name__ == "__main__":
    sys.exit(main())
