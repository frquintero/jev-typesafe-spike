#!/usr/bin/env bash
# Pide la clave de API de xAI (Grok) y la deja como variable global en ~/.bashrc
# (export XAI_API_KEY=...), igual que TYPESAFE_API_KEY, ZAI_API_KEY y DEEPSEEK_API_KEY.
# La clave no se muestra al escribirla ni queda en el historial.
#
# Uso:  bash utiliarios/configurar_clave_xai.sh
# Después: source ~/.bashrc  y reiniciar el proxy local (lee las claves al arrancar).

set -euo pipefail

read -rsp "Clave de API de xAI (no se verá al escribir): " clave
echo
if [ -z "$clave" ]; then
  echo "No se escribió ninguna clave; no se cambió nada." >&2
  exit 1
fi

bashrc="$HOME/.bashrc"
touch "$bashrc"
tmp="$(mktemp)"
grep -v '^export XAI_API_KEY=' "$bashrc" > "$tmp" || true
printf "export XAI_API_KEY='%s'\n" "$clave" >> "$tmp"
cat "$tmp" > "$bashrc"
rm -f "$tmp"
unset clave

echo "Listo: XAI_API_KEY quedó en $bashrc."
echo "Ahora: source ~/.bashrc  y reinicia el proxy local."
