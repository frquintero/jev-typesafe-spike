"""Smoke de API oficial Cloud: OAuth ADC -> crear notebook -> cargar texto -> leer.

Credenciales externas al repo, sin sesión web ni transporte de navegador.
"""
import argparse
import datetime as dt
import importlib.metadata
import json
import os
import re
import sys
import time
from pathlib import Path

import google.auth
from google.auth.transport.requests import AuthorizedSession
import requests


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("replica", help="cloud-rN; carpeta nueva obligatoria")
    p.add_argument("--project-number", required=True)
    p.add_argument("--location", required=True, choices=["global", "us", "eu"])
    p.add_argument("--endpoint", choices=["default", "global", "us", "eu"], default="default")
    p.add_argument("--credentials-file", type=Path, help="ADC o credenciales fuera del repo")
    args = p.parse_args()
    if not re.fullmatch(r"cloud-r[1-9][0-9]*", args.replica):
        p.error("use cloud-rN")
    if not args.project_number.isdigit():
        p.error("provide the numeric Google Cloud project number")
    root = Path(__file__).resolve().parent
    explicit = args.credentials_file or os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    configured_adc = Path(os.environ.get("CLOUDSDK_CONFIG", Path.home() / ".config/gcloud")) / "application_default_credentials.json"
    credential_path = Path(explicit).expanduser().resolve() if explicit else configured_adc.resolve()
    if credential_path.is_relative_to(root.parent):
        p.error("credentials must remain outside the repo")
    run = root / "cache" / args.replica
    run.mkdir(parents=True, exist_ok=False)
    host = "discoveryengine.googleapis.com" if args.endpoint == "default" else f"{args.endpoint}-discoveryengine.googleapis.com"
    base = f"https://{host}/v1alpha"
    parent = f"projects/{args.project_number}/locations/{args.location}"
    result = {"base_url": base, "parent": parent, "replica": args.replica,
              "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "authentication": "Google Cloud OAuth via ADC and google-auth",
              "google-auth": importlib.metadata.version("google-auth"),
              "requests": importlib.metadata.version("requests"), "http_requests": 0}
    secrets = []

    def save(name, data, raw=False):
        value = data if raw else json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        for secret in secrets:
            if secret:
                value = value.replace(secret, "[REDACTED]")
        value = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", value)
        with (run / name).open("x", encoding="utf-8") as f:
            f.write(value)

    save("inputs.json", result)
    session = None
    auth_session = None
    started = time.monotonic()
    try:
        if not credential_path.is_file():
            raise RuntimeError("CLOUD_AUTH_MISSING: configure ADC outside the repo; no API request sent")
        credentials, _ = google.auth.load_credentials_from_file(
            str(credential_path), scopes=["https://www.googleapis.com/auth/cloud-platform"],
            quota_project_id=args.project_number)
        # Token acquisition and attachment belong to google-auth, not repo code.
        cert = os.environ.get("SSL_CERT_FILE", True)
        auth_session = requests.Session()
        auth_session.verify = cert
        auth_session.headers.update({"User-Agent": "spike-jev/1.0"})
        session = AuthorizedSession(credentials, auth_request=google.auth.transport.requests.Request(session=auth_session),
                                    max_refresh_attempts=0)
        session.verify = cert
        session.headers.update({"Content-Type": "application/json", "User-Agent": "spike-jev/1.0"})

        def call(label, method, resource, body=None):
            url = f"{base}/{resource}"
            save(f"{label}-request.json", {"method": method, "url": url, "body": body,
                                          "headers": {"Content-Type": "application/json", "User-Agent": "spike-jev/1.0"}})
            before = time.monotonic()
            response = session.request(method, url, json=body, timeout=30, allow_redirects=False)
            result["http_requests"] += 1
            secrets.append(credentials.token)
            save(f"{label}-response.txt", response.text, raw=True)
            save(f"{label}-status.json", {"http_status": response.status_code,
                                         "seconds": round(time.monotonic() - before, 3)})
            response.raise_for_status()
            if response.is_redirect:
                raise RuntimeError("Unexpected redirect; stopped")
            data = response.json()
            save(f"{label}-parsed.json", data)
            print(json.dumps({"step": label, "status": response.status_code}), flush=True)
            return data

        title = f"NBLM-CLOUD-SMOKE-001 · {args.replica}-{result['started_utc']}"
        notebook = call("01-create", "POST", f"{parent}/notebooks", {"title": title})
        name = notebook.get("name")
        if not name or not name.startswith(parent + "/notebooks/"):
            raise RuntimeError("Create response lacks matching notebook resource name")
        result["notebook_name"] = name
        call("02-get", "GET", name)
        text = (root / "docs/smoke-001.txt").read_text().strip()
        sources = call("03-add-text", "POST", name + "/sources:batchCreate",
                       {"userContents": [{"textContent": {"sourceName": "NBLM-SMOKE-001", "content": text}}]})
        created = sources.get("sources", [])
        if not created or not created[0].get("name"):
            raise RuntimeError("Batch create response lacks source resource name")
        source_name = created[0]["name"]
        deadline = time.monotonic() + 60
        index = 0
        while time.monotonic() < deadline:
            index += 1
            source = call(f"04-source-{index:02d}", "GET", source_name)
            # Support the wrapped form shown in the guide and the Source resource.
            item = source.get("sources", [source])[0]
            state = item.get("settings", {}).get("status")
            if state == "SOURCE_STATUS_COMPLETE":
                result["source_name"] = source_name
                result["source_status"] = state
                break
            if state == "SOURCE_STATUS_ERROR":
                raise RuntimeError("Source processing error")
            time.sleep(3)
        else:
            raise TimeoutError("Source did not become complete within polling budget")
        result["completed"] = True
        result["scope"] = "Official Cloud notebook creation, retrieval, source upload and processing; no chat API call"
        code = 0
    except Exception as error:
        # Do not log OAuth exception text or token responses.
        result.update(completed=False, error_type=type(error).__name__)
        if isinstance(error, RuntimeError):
            result["error"] = str(error)
        else:
            result["error"] = "Stopped; inspect recorded API response if available. No automatic authentication recovery."
        code = 1
    finally:
        if session:
            session.close()
        if auth_session:
            auth_session.close()
        result["seconds"] = round(time.monotonic() - started, 3)
        save("summary.json", result)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())
