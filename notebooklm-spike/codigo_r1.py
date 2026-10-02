"""code-r1: una consulta que pide a NotebookLM ejecutar código y entregar un archivo JSON.

Uso: python codigo_r1.py notebooklm-spike/cache/code-rN  (sin HTTPS_PROXY; sesión del perfil nblm-spike).
Guarda pregunta, respuesta, referencias, raw_response y artefactos antes/después en result.json.
"""
import asyncio, json, time, dataclasses, enum, os, sys
from pathlib import Path
from notebooklm import NotebookLMClient
from notebooklm.options import ClientConfig, FeatureOptions, RetryOptions, WebBackendConfig
os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"]="1"
NB="f113873f-7fdb-416a-bb83-d429c4a3ce1b"
Q="Usa código para dividir la fuente en oraciones numeradas y entrégame un archivo JSON con ellas."
out=Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=False)
def conv(v):
    if dataclasses.is_dataclass(v): return dataclasses.asdict(v)
    if isinstance(v, enum.Enum): return v.value
    return str(v)
async def main():
    st=os.path.expanduser("~/.notebooklm/profiles/nblm-spike/storage_state.json")
    async with NotebookLMClient.from_storage(st, allow_headless=False, config=ClientConfig(backend=WebBackendConfig(),
        retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0), features=FeatureOptions(chat_timeout=180))) as c:
        before=await c.artifacts.list(NB)
        t=time.monotonic(); r=await c.chat.ask(NB,Q); secs=round(time.monotonic()-t,3)
        after=await c.artifacts.list(NB)
        res={"notebook":NB,"question":Q,"seconds":secs,"answer":r.answer,"conversation_id":r.conversation_id,
             "references":r.references,"raw_response":r.raw_response,
             "artifacts_before":len(before),"artifacts_after":after}
        (out/"result.json").write_text(json.dumps(res,default=conv,ensure_ascii=False,indent=2))
        print("SECONDS",secs); print("ANSWER\n"+r.answer); print("ARTIFACTS before/after",len(before),len(after))
        print("RAW\n"+(r.raw_response or "")[:1000])
asyncio.run(main())
