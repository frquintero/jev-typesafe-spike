"""Crea el proyecto autorizado y lee facturación/estado API. No vincula cobros."""
import datetime as dt
import json
import os
import re
import sys
import time
from pathlib import Path

import google.auth
from google.auth.transport.requests import AuthorizedSession, Request
import requests


def main():
    run = Path(__file__).resolve().parent / "cache/cloud-setup-r1"
    run.mkdir(parents=True, exist_ok=False)
    credentials, _ = google.auth.default(scopes=["https://www.googleapis.com/auth/cloud-platform"])
    cert = os.environ.get("SSL_CERT_FILE", True)
    auth_http = requests.Session()
    auth_http.verify = cert
    auth_http.headers["User-Agent"] = "spike-jev/1.0"
    http = AuthorizedSession(credentials, auth_request=Request(session=auth_http), max_refresh_attempts=0)
    http.verify = cert
    http.headers.update({"User-Agent": "spike-jev/1.0", "Content-Type": "application/json"})
    result = {"projectId": "notebooklm-spike-20261002", "displayName": "NotebookLM Spike",
              "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
              "authorized_by": "Frat selected creation of NotebookLM Spike",
              "billing_linked_by_script": False, "licenses_purchased": False}
    secrets = []

    def save(name, data, raw=False):
        text = data if raw else json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        for secret in secrets:
            if secret:
                text = text.replace(secret, "[REDACTED]")
        text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[REDACTED_EMAIL]", text)
        with (run / name).open("x", encoding="utf-8") as output:
            output.write(text)

    def call(label, method, url, body=None):
        save(label + "-request.json", {"method": method, "url": url, "body": body})
        start = time.monotonic()
        response = http.request(method, url, json=body, timeout=30, allow_redirects=False)
        secrets.append(credentials.token)
        save(label + "-response.txt", response.text, raw=True)
        save(label + "-status.json", {"http_status": response.status_code, "seconds": round(time.monotonic() - start, 3)})
        response.raise_for_status()
        if response.is_redirect:
            raise RuntimeError("Unexpected redirect")
        data = response.json()
        print(json.dumps({"step": label, "status": response.status_code}), flush=True)
        return data

    code = 1
    try:
        operation = call("01-create", "POST", "https://cloudresourcemanager.googleapis.com/v3/projects",
                         {"projectId": result["projectId"], "displayName": result["displayName"]})
        result["creation_operation"] = operation.get("name")
        deadline = time.monotonic() + 90
        poll = 0
        while not operation.get("done"):
            if time.monotonic() > deadline:
                raise TimeoutError("Project creation still pending; preserve operation and do not replay POST")
            time.sleep(2)
            poll += 1
            operation = call(f"02-poll-{poll:02d}", "GET", "https://cloudresourcemanager.googleapis.com/v3/" + operation["name"])
        if operation.get("error"):
            result["operation_error"] = operation["error"]
            raise RuntimeError("Project creation operation reported an error")
        project = operation.get("response", {})
        if not project.get("name"):
            raise RuntimeError("Project operation response missing resource name")
        result["projectNumber"] = project["name"].removeprefix("projects/")
        result["project_created"] = True
        result["state"] = project.get("state")
        billing = call("03-billing", "GET", f"https://cloudbilling.googleapis.com/v1/projects/{result['projectId']}/billingInfo")
        result["billing_enabled"] = billing.get("billingEnabled", False)
        service = call("04-api-state", "GET", f"https://serviceusage.googleapis.com/v1/projects/{result['projectNumber']}/services/discoveryengine.googleapis.com")
        result["discoveryengine_state"] = service.get("state")
        code = 0
    except Exception as error:
        result["error_type"] = type(error).__name__
        result["error"] = str(error) if isinstance(error, (RuntimeError, TimeoutError)) else "Stopped; inspect recorded response. No automatic auth retry."
    finally:
        save("summary.json", result)
        print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
        http.close()
        auth_http.close()
    return code


if __name__ == "__main__":
    sys.exit(main())
