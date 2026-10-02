"""Determinaciones como tabla de datos de NotebookLM (ronda FN2).

Uso (desde la raíz, sin HTTPS_PROXY):
  python notebooklm-spike/tabla_nblm.py <doc> <instrucciones> <rN> --storage <storage_state.json>

Cuaderno nuevo; fuente = texto numerado con la numeración de unidades/ficha_doc.py;
generate_data_table(language="es", instructions=notebooklm-spike/prompts/<instrucciones>.md);
espera a que termine, baja el CSV y comprueba con código que cada «fragmento literal»
aparezca en la oración indicada. No juzga el contenido. Crudos únicos en
cache/tabla-<doc>-nblm-<instrucciones>-<rN>/ (la carpeta no puede existir).
"""
import argparse, asyncio, csv, dataclasses, datetime as dt, enum, io, json, os, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
UNIDADES = ROOT.parent / "unidades"
sys.path.insert(0, str(ROOT.parent / "niveles")); sys.path.insert(0, str(UNIDADES))
from extraer_unidades import numerar_oraciones  # noqa: E402
from notebooklm import NotebookLMClient  # noqa: E402
from notebooklm.options import ClientConfig, RetryOptions, WebBackendConfig  # noqa: E402
from notebooklm._web.transport.session_auth import WebSessionAuth  # noqa: E402

ACCOUNT = 0
COLUMNAS = ["caso de estudio", "aspecto", "valor", "unidad", "cambio", "condición",
            "quién lo sostiene", "inferido", "oración", "fragmento literal"]


async def stop_refresh(self, expected_epoch):
    raise RuntimeError("AUTH_STOP: automatic authentication recovery disabled")


def convert(v):
    if dataclasses.is_dataclass(v): return dataclasses.asdict(v)
    if isinstance(v, enum.Enum): return v.value
    return str(v)


def norm(s):
    return " ".join(s.strip().lower().split())


def verificar(filas, registros):
    por_n = {r["n"]: r["oracion"] for r in registros}
    malos = []
    for i, f in enumerate(filas):
        k = {norm(c): c for c in f}
        o, frag = f.get(k.get("oración", ""), ""), f.get(k.get("fragmento literal", ""), "")
        try:
            n = int(str(o).strip().strip("[]"))
        except ValueError:
            n = None
        if n not in por_n or not frag or frag.strip() not in por_n[n]:
            malos.append({"fila": i + 1, "oración": o, "fragmento": frag})
    return malos


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("doc"); ap.add_argument("instrucciones"); ap.add_argument("rep")
    ap.add_argument("--storage", type=Path, required=True)
    a = ap.parse_args()
    storage = a.storage.resolve()
    if storage.is_relative_to(ROOT.parent):
        ap.error("storage must be outside the repository")
    out = ROOT / "cache" / f"tabla-{a.doc}-nblm-{a.instrucciones}-{a.rep}"
    out.mkdir(parents=True, exist_ok=False)
    state = json.loads(storage.read_text())
    if state.get("notebooklm", {}).get("account", {}).get("authuser") != ACCOUNT:
        raise SystemExit(f"Expected account {ACCOUNT}")
    texto = (UNIDADES / "docs" / f"{a.doc}.md").read_text(encoding="utf-8")
    instrucciones = (ROOT / "prompts" / f"{a.instrucciones}.md").read_text(encoding="utf-8").strip()
    texto_numerado, registros = numerar_oraciones(texto)

    WebSessionAuth.refresh_base = stop_refresh
    os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"] = "1"
    os.environ["NOTEBOOKLM_HEADLESS_REAUTH"] = "0"
    os.environ.pop("NOTEBOOKLM_REFRESH_CMD", None)
    crudo = {"doc": a.doc, "instrucciones_archivo": a.instrucciones, "rep": a.rep,
             "cliente": "notebooklm-py==0.8.4", "herramienta": "generate_data_table",
             "inicio_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
             "texto_numerado": texto_numerado, "oraciones_numeradas": registros,
             "instrucciones_enviadas": instrucciones, "etapas": {}, "completed": False}

    async def run():
        cfg = ClientConfig(backend=WebBackendConfig(),
                           retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0))
        async with NotebookLMClient.from_storage(str(storage), allow_headless=False, config=cfg) as c:
            if c.get_account_authuser() != ACCOUNT:
                raise RuntimeError("Wrong account route")

            async def etapa(nombre, call):
                t = time.monotonic(); v = await call()
                crudo["etapas"][nombre] = round(time.monotonic() - t, 3)
                print(json.dumps({nombre: crudo["etapas"][nombre]}), flush=True)
                return v

            nb = await etapa("crear", lambda: c.notebooks.create(f"TABLA {a.doc} {a.instrucciones} {a.rep} {crudo['inicio_utc']}"))
            crudo["notebook_id"] = nb.id
            src = await etapa("cargar", lambda: c.sources.add_text(nb.id, a.doc, texto_numerado))
            crudo["source_id"] = src.id
            await etapa("lista", lambda: c.sources.wait_until_ready(nb.id, src.id, timeout=120))
            full = await etapa("texto", lambda: c.sources.get_fulltext(nb.id, src.id))
            crudo["fuente_recuperada"] = full.content
            crudo["fuente_igual_al_texto_numerado"] = full.content.strip() == texto_numerado.strip()
            st = await etapa("pedir_tabla", lambda: c.artifacts.generate_data_table(
                nb.id, source_ids=[src.id], language="es", instructions=instrucciones))
            crudo["generacion"] = st
            fin = await etapa("esperar_tabla", lambda: c.artifacts.wait_for_completion(nb.id, st.task_id, timeout=600))
            crudo["estado_final"] = fin
            ruta = str(out / "tabla.csv")
            await etapa("bajar_csv", lambda: c.artifacts.download_data_table(nb.id, ruta, artifact_id=st.task_id))

    t0 = time.monotonic()
    try:
        asyncio.run(run())
        crudo["completed"] = True
    except Exception as exc:
        crudo["error"] = {"type": type(exc).__name__, "message": str(exc)[:500]}
    crudo["segundos_total"] = round(time.monotonic() - t0, 3)
    csv_path = out / "tabla.csv"
    if csv_path.exists():
        texto_csv = csv_path.read_text(encoding="utf-8-sig")
        filas = list(csv.DictReader(io.StringIO(texto_csv)))
        cab = list(filas[0].keys()) if filas else next(csv.reader(io.StringIO(texto_csv)), [])
        crudo["columnas_recibidas"] = cab
        crudo["columnas_faltantes"] = [x for x in COLUMNAS if x not in [norm(h) for h in cab]]
        crudo["filas"] = len(filas)
        crudo["no_literales"] = verificar(filas, registros)
    with (out / "crudo.json").open("x", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2, default=convert)
    resumen = {k: crudo.get(k) for k in ("completed", "error", "segundos_total", "etapas",
               "fuente_igual_al_texto_numerado", "columnas_faltantes", "filas")}
    resumen["no_literales"] = len(crudo.get("no_literales", [])) if "no_literales" in crudo else None
    print(f"hecho -> {out}"); print(json.dumps(resumen, ensure_ascii=False, indent=2, default=convert))
    return 0 if crudo["completed"] else 1


if __name__ == "__main__":
    sys.exit(main())
