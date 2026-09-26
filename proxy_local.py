"""Proxy local para correr las pruebas en la máquina de Frat.

Hace lo mismo que el proxy de la nube: agrega la clave de API a cada petición.
Los scripts no se tocan y nunca ven las claves.

Instalar (una vez):
    pip install --user mitmproxy

Terminal 1, arrancar el proxy (las claves solo viven en esta terminal):
    export TYPESAFE_API_KEY=...  ZAI_API_KEY=...  DEEPSEEK_API_KEY=...
    mitmdump -q --listen-host 127.0.0.1 -p 8080 -s proxy_local.py

Terminal 2, correr cualquier script:
    export HTTPS_PROXY=http://127.0.0.1:8080 SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem
    python3 niveles/extraer_datos.py doc5 deepseek datos_v8 r1

El certificado lo crea mitmdump la primera vez que arranca. Solo lo usan los
procesos que exportan SSL_CERT_FILE; no se instala en el sistema.
"""
import os

CLAVES = {
    "api.typesafe.ai": "TYPESAFE_API_KEY",
    "api.z.ai": "ZAI_API_KEY",
    "api.deepseek.com": "DEEPSEEK_API_KEY",
}


def request(flow):
    var = CLAVES.get(flow.request.pretty_host)
    if var and os.environ.get(var):
        flow.request.headers["Authorization"] = "Bearer " + os.environ[var]


def responseheaders(flow):
    flow.response.stream = True  # deja pasar el streaming sin esperar al final
