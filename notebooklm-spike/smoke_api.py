"""Smoke HTTP con sesión externa; conserva cada réplica y detiene errores de auth.

Ejecutar con el Python del entorno notebooklm-mcp-cli==0.15.0.
No usa control de navegador durante la corrida ni modifica el cliente instalado.
"""
import argparse
import dataclasses
import datetime as dt
import importlib.metadata
import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import parse_qs

import httpx
from notebooklm_tools.core.client import NotebookLMClient


class SmokeClient(NotebookLMClient):
    def _cdp_rpc_transport_enabled(self):
        return False

    def _call_rpc(self, *args, **kwargs):
        kwargs.update(_retry=True, _deep_retry=True, retry_server_errors=False)
        return super()._call_rpc(*args, **kwargs)

    def _refresh_auth_tokens(self):
        raise RuntimeError("AUTH_STOP: no automatic session refresh in this smoke")

    def _try_reload_or_headless_auth(self):
        return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("replica", help="Nueva réplica: api-r1, api-r2, ...")
    parser.add_argument("--session-file", type=Path, required=True)
    parser.add_argument("--probe-notebook", required=True,
                        help="Notebook sintético ya existente para lectura inicial")
    args = parser.parse_args()
    if not re.fullmatch(r"api-r[1-9][0-9]*", args.replica):
        parser.error("replica must be api-rN")
    root = Path(__file__).resolve().parent
    session_path = args.session_file.resolve()
    if session_path.is_relative_to(root.parent):
        parser.error("session file must be outside the repository")
    version = importlib.metadata.version("notebooklm-mcp-cli")
    if version != "0.15.0":
        parser.error("requires notebooklm-mcp-cli==0.15.0")
    run = root / "cache" / args.replica
    run.mkdir(parents=True, exist_ok=False)
    auth = json.loads(session_path.read_text())
    required = ("cookies", "csrf_token", "session_id", "build_label", "authuser")
    if not all(auth.get(k) for k in required):
        raise RuntimeError("Incomplete external session")
    secrets = [auth["csrf_token"], auth["session_id"]]
    secrets += [c["value"] for c in auth["cookies"] if len(c["value"]) >= 8]

    def clean(value):
        for secret in sorted(secrets, key=len, reverse=True):
            value = value.replace(secret, "[REDACTED]")
        return re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", value)

    def save(name, value, raw=False):
        if dataclasses.is_dataclass(value):
            value = dataclasses.asdict(value)
        text = value if raw else json.dumps(value, ensure_ascii=False, indent=2)
        with (run / name).open("x", encoding="utf-8") as output:
            output.write(clean(text) + ("" if raw else "\n"))

    started = time.monotonic()
    current_step = "setup"
    requests = []
    stages = []

    def on_request(request):
        request.url = request.url.copy_merge_params({"authuser": auth["authuser"]})
        request.headers["User-Agent"] = "spike-jev/1.0"
        index = len(requests) + 1
        request.extensions["smoke_index"] = index
        request.extensions["smoke_start"] = time.monotonic()
        form = parse_qs(request.content.decode())
        record = {
            "index": index, "step": current_step, "method": request.method,
            "host": request.url.host, "path": request.url.path,
            "query": {k: v for k, v in request.url.params.multi_items()
                      if k not in {"f.sid", "at"}},
            "content_type": request.headers.get("Content-Type"),
            "user_agent": request.headers["User-Agent"],
            "f.req": form.get("f.req", [None])[0],
            "auth_fields_omitted": ["cookies", "at", "f.sid", "csrf headers"],
        }
        requests.append(record)
        save(f"http-{index:02d}-request.json", record)

    def on_response(response):
        index = response.request.extensions["smoke_index"]
        response.read()
        save(f"http-{index:02d}-response.txt", response.text, raw=True)
        record = {
            "index": index, "step": current_step, "status": response.status_code,
            "seconds": round(time.monotonic() - response.request.extensions["smoke_start"], 3),
            "bytes": len(response.content),
            "content_type": response.headers.get("Content-Type"),
        }
        save(f"http-{index:02d}-response.json", record)
        if response.status_code in (401, 403) or (
            300 <= response.status_code < 400
            and "accounts.google.com" in response.headers.get("location", "")
        ):
            raise RuntimeError(f"AUTH_STOP: HTTP {response.status_code}")

    # query() creates its own httpx.Client; instrument both it and RPC clients.
    original_httpx_client = httpx.Client

    class RecordedHTTPClient(original_httpx_client):
        def __init__(self, *args, **kwargs):
            hooks = kwargs.setdefault("event_hooks", {})
            hooks.setdefault("request", []).append(on_request)
            hooks.setdefault("response", []).append(on_response)
            super().__init__(*args, **kwargs)

    httpx.Client = RecordedHTTPClient

    def step(name, operation):
        nonlocal current_step
        current_step = name
        begin = time.monotonic()
        result = operation()
        save(f"{name}-parsed.json", result)
        elapsed = round(time.monotonic() - begin, 3)
        stages.append({"step": name, "seconds": elapsed})
        print(json.dumps({"step": name, "seconds": elapsed, "completed": True}), flush=True)
        return result

    text = (root / "docs/smoke-001.txt").read_text().strip()
    prompt = (root / "prompts/smoke-001.txt").read_text().strip()
    title = f"NBLM-SMOKE-001 · {args.replica}-{dt.datetime.now(dt.timezone.utc).isoformat()}"
    summary = {
        "replica": args.replica, "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "transport": "Python httpx HTTPS (no browser transport)",
        "client": {"notebooklm-mcp-cli": version, "httpx": importlib.metadata.version("httpx")},
        "auth": "external Google browser session; cookies + at + f.sid; authuser=" + auth["authuser"],
        "text": text, "prompt": prompt, "title": title,
        "expected": "17 fichas violetas; cita vinculada a la fuente y pasaje recuperable",
    }
    save("inputs.json", summary)
    client = None
    exit_code = 0
    try:
        client = SmokeClient(cookies=auth["cookies"], csrf_token=auth["csrf_token"],
                             session_id=auth["session_id"], build_label=auth["build_label"],
                             base_host=auth.get("base_host", "notebook.google.com"))
        probe = step("01-auth-read", lambda: client.get_notebook(args.probe_notebook))
        if not probe:
            raise RuntimeError("Authenticated synthetic notebook read returned no data")
        notebook = step("02-create", lambda: client.create_notebook(title))
        if not notebook:
            raise RuntimeError("Notebook creation returned no identifier")
        summary["notebook_id"] = notebook.id
        summary["url"] = f"https://notebook.google.com/notebook/{notebook.id}?authuser={auth['authuser']}"
        source = step("03-add-text", lambda: client.add_text_source(notebook.id, text, title="NBLM-SMOKE-001"))
        if not source or not source.get("id"):
            raise RuntimeError("Source upload returned no identifier; no replay attempted")
        summary["source_id"] = source["id"]
        step("04-processing", lambda: client.wait_for_source_ready(notebook.id, source["id"], timeout=60))
        answer = step("05-query", lambda: client.query(notebook.id, prompt,
                      source_ids=[source["id"]], new_conversation=True, timeout=120))
        fulltext = step("06-source-fulltext", lambda: client.get_source_fulltext(source["id"]))
        observations = {
            "answer": answer.get("answer") if answer else None,
            "contains_17": bool(answer and "17" in answer.get("answer", "")),
            "contains_violetas": bool(answer and "violetas" in answer.get("answer", "").lower()),
            "citations_link_uploaded_source": bool(answer and source["id"] in answer.get("citations", {}).values()),
            "references": answer.get("references", []) if answer else [],
            "full_source_matches_input": bool(fulltext and fulltext.get("content", "").strip() == text),
        }
        summary["observations"] = observations
        if not all(observations[k] for k in ("contains_17", "contains_violetas", "citations_link_uploaded_source", "full_source_matches_input")):
            raise RuntimeError("One or more prewritten observations were not obtained; inspect raws")
        summary["completed"] = True
    except Exception as exc:
        exit_code = 1
        summary["completed"] = False
        summary["failed_step"] = current_step
        summary["error_type"] = type(exc).__name__
        summary["error"] = clean(str(exc))
    finally:
        if client:
            client.close()
        httpx.Client = original_httpx_client
        summary["stages"] = stages
        summary["http_requests"] = len(requests)
        summary["total_seconds"] = round(time.monotonic() - started, 3)
        save("summary.json", summary)
        print(clean(json.dumps(summary, ensure_ascii=False, indent=2)), flush=True)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
