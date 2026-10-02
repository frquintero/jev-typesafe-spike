"""Descarga el archivo (artefacto tipo FILE, código 10) generado por la ejecución de código.

notebooklm-py 0.8.4 no trae descarga para FILE. La respuesta cruda del RPC gArtLc (lista de
artefactos) incluye un enlace contribution.usercontent.google.com/download; este script lo
extrae y lo baja con las cookies de la sesión. Solo lectura. Depende de un formato interno
de Google que puede cambiar.

Uso: python descargar_artefacto.py notebooklm-spike/cache/code-rN  (sin HTTPS_PROXY).
"""
import asyncio, os, re, json, sys, httpx
from pathlib import Path
from notebooklm import NotebookLMClient
from notebooklm.options import ClientConfig, RetryOptions, WebBackendConfig
os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"]="1"
NB="f113873f-7fdb-416a-bb83-d429c4a3ce1b"; ST=os.path.expanduser("~/.notebooklm/profiles/nblm-spike/storage_state.json")
out=Path(sys.argv[1])
bodies=[]; orig=httpx.AsyncClient
async def on_resp(r):
    await r.aread()
    if r.request.url.params.get("rpcids")=="gArtLc": bodies.append(r.text)
class C(orig):
    def __init__(s,*a,**k):
        k.setdefault("event_hooks",{}).setdefault("response",[]).append(on_resp); super().__init__(*a,**k)
httpx.AsyncClient=C
async def main():
    async with NotebookLMClient.from_storage(ST, allow_headless=False, config=ClientConfig(backend=WebBackendConfig(), retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0))) as c:
        await c.artifacts.list(NB)
    httpx.AsyncClient=orig
    t=bodies[0]
    urls=[u.encode().decode('unicode_escape') for u in re.findall(r'https://contribution\.usercontent\.google\.com/download[^"\\]*(?:\\\\u00[0-9a-f]{2}[^"\\]*)*', t)]
    urls=[u.replace('\\u003d','=').replace('\\u0026','&') for u in urls]
    print("download urls found:", len(urls), "| params:", sorted(set(k.split('=')[0] for k in re.split(r'[?&]', urls[0])[1:])) if urls else None)
    if not urls: return
    st=json.load(open(ST)); jar=httpx.Cookies()
    for ck in st["cookies"]: jar.set(ck["name"], ck["value"], domain=ck["domain"], path=ck.get("path","/"))
    async with orig(cookies=jar, follow_redirects=True, timeout=30) as h:
        r=await h.get(urls[0], headers={"User-Agent":"spike-jev/1.0"})
        print("status", r.status_code, "type", r.headers.get("content-type"), "bytes", len(r.content), "final host", r.url.host)
        if r.status_code==200 and "json" in (r.headers.get("content-type") or "") or r.content[:1] in (b"[",b"{"):
            (out/"oraciones-numeradas.json").write_bytes(r.content); print(r.content.decode()[:1500])
        else:
            print(r.text[:300])
asyncio.run(main())
