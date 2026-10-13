#!/usr/bin/env bash
# Pide la clave de API de xAI (Grok) y la deja en ~/.config/xai/api_key.env (modo 600), que es
# donde el ~/.bashrc la busca —igual que las demás claves (ZAI, Anthropic, Gemini…)—.
# La clave no se muestra al escribirla ni queda en el historial.
#
# Uso:  bash utiliarios/configurar_clave_xai.sh
# Después: source ~/.bashrc

set -euo pipefail

read -rsp "Clave de API de xAI (no se verá al escribir): " clave
echo
if [ -z "$clave" ]; then
  echo "No se escribió ninguna clave; no se cambió nada." >&2
  exit 1
fi

destino="$HOME/.config/xai/api_key.env"
mkdir -p "$(dirname "$destino")"
umask 077
printf "export XAI_API_KEY='%s'\n" "$clave" > "$destino"
chmod 600 "$destino"

# Si quedó la línea vieja dentro del ~/.bashrc (de antes del 13-10-2026), se retira: la clave
# vive en un solo lugar.
if grep -q '^export XAI_API_KEY=' "$HOME/.bashrc" 2>/dev/null; then
  tmp="$(mktemp)"
  grep -v '^export XAI_API_KEY=' "$HOME/.bashrc" > "$tmp" || true
  cat "$tmp" > "$HOME/.bashrc"
  rm -f "$tmp"
  echo "Se retiró la línea vieja de ~/.bashrc."
fi

unset clave
echo "Listo: XAI_API_KEY quedó en $destino (600)."
echo "Ahora: source ~/.bashrc"
