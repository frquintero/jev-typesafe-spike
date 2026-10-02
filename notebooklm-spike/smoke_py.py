"""Smoke S0–S3 con notebooklm-py 0.8.4; secretos externos y crudos únicos."""
import argparse
import asyncio
import dataclasses
import datetime as dt
import enum
import importlib.metadata
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from http.cookies import SimpleCookie
from urllib.parse import parse_qs

import httpx
from notebooklm import NotebookLMClient, resolve_chat_reference_passage
from notebooklm.options import ClientConfig, FeatureOptions, RetryOptions, WebBackendConfig
from notebooklm._web.transport.session_auth import WebSessionAuth


ACCOUNT = 0  # authuser of the nblm-spike profile (Frat's main account)


async def stop_refresh(self, expected_epoch):
    raise RuntimeError("AUTH_STOP: automatic authentication recovery disabled")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replica")
    parser.add_argument("--storage", type=Path, required=True)
    parser.add_argument("--reconnect", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"py-r[1-9][0-9]*", args.replica):
        parser.error("replica must be py-rN")
    if importlib.metadata.version("notebooklm-py") != "0.8.4":
        parser.error("requires notebooklm-py==0.8.4")
    root = Path(__file__).resolve().parent
    storage = args.storage.resolve()
    if storage.is_relative_to(root.parent):
        parser.error("storage must be outside the repository")
    run = root / "cache" / args.replica
    # Session written by `notebooklm -p <profile> login`; read only, never rewritten here.
    state = json.loads(storage.read_text())
    if state.get("notebooklm", {}).get("account", {}).get("authuser") != ACCOUNT:
        raise RuntimeError(f"Expected account {ACCOUNT}")
    if not args.reconnect:
        run.mkdir(parents=True, exist_ok=False)
    original = {}
    secrets = {c["value"] for c in state["cookies"] if len(c["value"]) >= 6}
    secrets.update(original[k] for k in ("csrf_token", "session_id") if original.get(k))
    prefix = "reconnect-" if args.reconnect else ""
    current = "S3-open" if args.reconnect else "S0-open"
    requests = []
    stages = []
    began = time.monotonic()

    def clean(value):
        for secret in sorted(secrets, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", value)

    def convert(value):
        if dataclasses.is_dataclass(value):
            return dataclasses.asdict(value)
        if isinstance(value, enum.Enum):
            return value.value
        return str(value)

    def save(name, value, raw=False):
        text = value if raw else json.dumps(value, default=convert, ensure_ascii=False, indent=2)
        with (run / (prefix + name)).open("x", encoding="utf-8") as f:
            f.write(clean(text) + "\n")

    async def on_request(request):
        if request.url.host not in {"notebook.google.com", "notebooklm.google.com"}:
            raise RuntimeError("AUTH_STOP: unexpected host or login redirect")
        cookie = SimpleCookie()
        cookie.load(request.headers.get("cookie", ""))
        secrets.update(v.value for v in cookie.values() if len(v.value) >= 6)
        body = await request.aread()
        form = parse_qs(body.decode()) if body else {}
        secrets.update(v for k in ("at", "f.sid") for v in form.get(k, []))
        secrets.update(v for k,v in request.url.params.multi_items() if k in {"at", "f.sid"})
        request.headers["User-Agent"] = "spike-jev/1.0"
        index = len(requests) + 1
        request.extensions.update(smoke_index=index, smoke_start=time.monotonic())
        record = {"index": index, "step": current, "method": request.method,
                  "host": request.url.host, "path": request.url.path,
                  "query": {k:v for k,v in request.url.params.multi_items()
                            if k not in {"at", "f.sid"}},
                  "f.req": form.get("f.req", [None])[0],
                  "user_agent": "spike-jev/1.0", "auth_fields_omitted": True}
        requests.append(record)
        save(f"http-{index:02d}-request.json", record)

    async def on_response(response):
        await response.aread()
        for header in response.headers.get_list("set-cookie"):
            cookie = SimpleCookie(); cookie.load(header)
            secrets.update(v.value for v in cookie.values() if len(v.value) >= 6)
        for key in ("SNlM0e", "FdrFJe"):
            match = re.search(r'"' + key + r'"\s*:\s*"([^"\\]+)"', response.text)
            if match:
                secrets.add(match.group(1))
        index = response.request.extensions["smoke_index"]
        is_rpc = "/_/" in response.request.url.path
        save(f"http-{index:02d}-response.json", {
            "status": response.status_code, "bytes": len(response.content),
            "seconds": round(time.monotonic()-response.request.extensions["smoke_start"], 3),
            "body_saved": is_rpc,
            "omission": None if is_rpc else "auth bootstrap HTML contains account/session data"})
        if is_rpc:
            save(f"http-{index:02d}-response.txt", response.text, raw=True)
        if response.status_code in (401,403) or "accounts.google.com" in response.headers.get("location", ""):
            raise RuntimeError(f"AUTH_STOP: HTTP {response.status_code}")

    original_client = httpx.AsyncClient

    class RecordedClient(original_client):
        def __init__(self, *a, **kw):
            hooks = kw.setdefault("event_hooks", {})
            hooks.setdefault("request", []).append(on_request)
            hooks.setdefault("response", []).append(on_response)
            super().__init__(*a, **kw)

    httpx.AsyncClient = RecordedClient
    # Pinned diagnostic seam: prevent the SDK's auth coordinator retrying auth.
    WebSessionAuth.refresh_base = stop_refresh
    os.environ["NOTEBOOKLM_DISABLE_KEEPALIVE_POKE"] = "1"
    os.environ["NOTEBOOKLM_HEADLESS_REAUTH"] = "0"
    os.environ.pop("NOTEBOOKLM_REFRESH_CMD", None)

    async def step(name, call):
        nonlocal current
        current = name
        begin = time.monotonic()
        value = await call()
        save(name + ".json", value)
        stages.append({"step": name, "seconds": round(time.monotonic()-begin,3)})
        print(json.dumps(stages[-1]), flush=True)
        return value

    summary = {"replica": args.replica, "client": "notebooklm-py==0.8.4",
               "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "account": ACCOUNT, "completed": False, "stages": stages}
    if not args.reconnect:
        text = (root / "docs/smoke-001.txt").read_text().strip()
        prompt = (root / "prompts/smoke-001.txt").read_text().strip()
        summary.update(text=text, prompt=prompt)
        save("inputs.json", {"text": text, "prompt": prompt,
                             "expected": "17 fichas violetas, cita y pasaje recuperable"})

    async def execute():
        nonlocal current
        async with NotebookLMClient.from_storage(
            str(storage), allow_headless=False,
            config=ClientConfig(backend=WebBackendConfig(),
                                retry=RetryOptions(rate_limit_max_retries=0, server_error_max_retries=0),
                                features=FeatureOptions(chat_timeout=60)),
        ) as client:
            if client.get_account_authuser() != ACCOUNT:
                raise RuntimeError("Wrong account route")
            if args.reconnect:
                previous = json.loads((run / "summary.json").read_text())
                nb_id, src_id = previous["notebook_id"], previous["source_id"]
                nb = await step("S3-notebook", lambda: client.notebooks.get(nb_id))
                fulltext3 = await step("S3-fulltext", lambda: client.sources.get_fulltext(nb_id, src_id))
                history = await step("S3-history", lambda: client.chat.get_history(nb_id))
                checks = {"notebook_id_matches": nb.id == nb_id,
                          "source_content_matches": fulltext3.content.strip() == previous["text"],
                          "history_recovers_question_answer": any(q == previous["prompt"] and a.strip() == previous["answer"].strip() for q,a in history)}
                summary["checks"] = checks
                if not all(checks.values()):
                    raise RuntimeError("S3 semantic check failed")
                return
            await step("S0-notebook", lambda: client.notebooks.get("f113873f-7fdb-416a-bb83-d429c4a3ce1b"))
            await step("S0-limits", client.settings.get_account_limits)
            title = f"NBLM-SMOKE-001 {args.replica} {summary['started_utc']}"
            nb = await step("S1-create", lambda: client.notebooks.create(title))
            summary["notebook_id"] = nb.id
            source = await step("S1-add-text", lambda: client.sources.add_text(nb.id,title,text))
            summary["source_id"] = source.id
            await step("S1-ready", lambda: client.sources.wait_until_ready(nb.id,source.id,timeout=60))
            full = await step("S1-fulltext", lambda: client.sources.get_fulltext(nb.id,source.id))
            if full.content.strip() != text:
                raise RuntimeError("S1 indexed content differs from input")
            result = await step("S2-ask", lambda: client.chat.ask(nb.id,prompt,source_ids=[source.id]))
            summary["answer"] = result.answer
            cited = [r for r in result.references if r.source_id == source.id]
            passages = []
            for i,ref in enumerate(cited):
                passages.append(await step(f"S2-passage-{i+1}",lambda ref=ref: resolve_chat_reference_passage(client,nb.id,ref)))
            checks = {"fulltext_matches": full.content.strip()==text,
                      "answer_contains_17": bool(re.search(r"\b17\b",result.answer)),
                      "answer_contains_violetas": "violetas" in result.answer.lower(),
                      "citation_matches_uploaded_source": bool(cited),
                      "retrieved_passage_supports_answer": any("17" in p and "violetas" in p.lower() and "Luma" in p for p in passages)}
            summary["checks"] = checks
            if not all(checks.values()):
                raise RuntimeError("S2 content/citation check failed")

    code = 0
    try:
        asyncio.run(execute())
        summary["completed"] = True
    except Exception as exc:
        summary["error"] = {"type": type(exc).__name__, "step": current, "message": clean(str(exc))}
        code = 1
    summary.update(http_requests=len(requests), total_seconds=round(time.monotonic()-began,3))
    save("summary.json",summary)
    print(json.dumps({"completed":summary["completed"],"step":current,"seconds":summary["total_seconds"],"error":summary.get("error")}),flush=True)
    if not args.reconnect and code == 0:
        child = subprocess.run([sys.executable,str(Path(__file__).resolve()),args.replica,"--storage",str(storage),"--reconnect"],check=False)
        code = child.returncode
    return code


if __name__ == "__main__":
    sys.exit(main())
