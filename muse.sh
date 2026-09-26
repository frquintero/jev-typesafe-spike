#!/usr/bin/env bash
# Arranca el proxy local de claves (si no está corriendo) y luego Muse Code
# sin sandbox, en el directorio desde donde se llama (el proxy sí usa el
# proxy_local.py de este repo). Uso: muse [flags] (alias en ~/.bashrc);
# el binario sin proxy: command muse
#
# - Si este script arrancó el proxy, lo apaga al salir de Muse o al cerrarse
#   la terminal. Si ya había uno escuchando, lo usa y no lo toca.
#   Log: ~/.cache/proxy_local.log (fuera del repo).
# - Las claves se toman de las líneas export de ~/.bashrc (y ZAI de
#   ~/.config/zai/api_key.env) y solo las recibe el proxy; Muse no.
# - A Muse NO se le exporta HTTPS_PROXY: su propio tráfico (api.meta.ai) no
#   debe pasar por mitmproxy. Los scripts del repo lo exportan por comando.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$HOME/.cache/proxy_local.log"
PUERTO=8080
PID_PROXY=""

escuchando() { ss -ltn | grep -q "127.0.0.1:$PUERTO "; }

apagar_proxy() {
  if [ -n "$PID_PROXY" ] && kill -0 "$PID_PROXY" 2>/dev/null; then
    kill "$PID_PROXY" 2>/dev/null || true
    echo "proxy: apagado"
  fi
}
trap apagar_proxy EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM

if escuchando; then
  echo "proxy: ya hay algo escuchando en 127.0.0.1:$PUERTO; lo uso (no lo apago al salir)"
else
  mkdir -p "$(dirname "$LOG")"
  (
    eval "$(grep -E '^export (TYPESAFE|ZAI|DEEPSEEK|XAI)_API_KEY=' "$HOME/.bashrc")"
    # ZAI_API_KEY vive en un archivo aparte que ~/.bashrc carga con source
    [ -f "$HOME/.config/zai/api_key.env" ] && . "$HOME/.config/zai/api_key.env"
    cd "$REPO"
    # setsid: las señales de la terminal (Ctrl+C) no le llegan; lo apaga el trap
    exec setsid "$HOME/.venvs/mitmproxy/bin/mitmdump" -q --listen-host 127.0.0.1 \
      -p "$PUERTO" -s proxy_local.py >"$LOG" 2>&1
  ) &
  PID_PROXY=$!
  for _ in $(seq 20); do
    escuchando && break
    sleep 0.5
  done
  if escuchando; then
    echo "proxy: arrancado en 127.0.0.1:$PUERTO"
  else
    echo "proxy: no arrancó; revisa $LOG" >&2
    exit 1
  fi
fi

# Muse arranca en el directorio desde donde se llamó este script.
# Sin META_API_KEY: Muse usa la suscripción, no factura por API.
# --disable-sandbox: red completa (alcanza el proxy) y .git escribible;
# las aprobaciones siguen activas.
env -u META_API_KEY "$HOME/.local/bin/muse" --disable-sandbox "$@"
