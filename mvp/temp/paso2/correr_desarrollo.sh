#!/usr/bin/env bash
# Una pasada de las tres entradas (a, b, c) sobre las 11 unidades congeladas de v9
# en doc4 y doc5. Idempotente: si el crudo existe, `comparacion.py` no vuelve a
# llamar. Uso: ./mvp/temp/paso2/correr_desarrollo.sh [modelo] [rN]
set -euo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$RAIZ"
MODELO="${1:-deepseek}"
REP="${2:-r1}"
for par in "doc4 mvp/temp/pruebas/salida_prueba8-v9-doc4.md" "doc5 mvp/temp/pruebas/salida_prueba9-v9-doc5.md"; do
  set -- $par
  for entrada in a b c; do
    echo "=== $1 · entrada ($entrada) · $REP ==="
    python3 mvp/temp/paso2/comparacion.py correr "mvp/temp/pruebas/$1.md" "$2" "$MODELO" "$REP" "$entrada"
  done
done
echo "fin: $(date -Is)"
