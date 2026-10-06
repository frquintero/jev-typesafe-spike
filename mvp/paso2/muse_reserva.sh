#!/usr/bin/env bash
# Reserva con Muse y la entrada seleccionada (b): una tarea por unidad.
# Uso: ./mvp/paso2/muse_reserva.sh [esfuerzo] [rN]
set -uo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASO2="$RAIZ/mvp/paso2"
ESF="${1:-high}"
REP="${2:-r1}"
MSGS="$HOME/.cache/muse_tarea_msgs"
TAREAS="$HOME/.cache/muse_tareas"
mkdir -p "$MSGS"

DOCS=("reserva_a|mvp/paso2/salida_reservaA-v9.md|7"
      "reserva_b|mvp/paso2/salida_reservaB-v9.md|5")

for fila in "${DOCS[@]}"; do
  IFS='|' read -r doc salida nun <<< "$fila"
  for n in $(seq 1 "$nun"); do
    etiq="p2r-$doc-b-u$n-$REP"
    crudo="$PASO2/cache/comp-$doc-b-u$n-muse-$REP.json"
    if [ -f "$crudo" ]; then echo "ya está: $etiq"; continue; fi
    echo "=== $etiq ($(date -Is)) ==="
    python3 "$PASO2/muse_unidad.py" armar "$PASO2/$doc.md" "$RAIZ/$salida" "$n" b "$etiq" \
      || { echo "FALLO armar $etiq"; continue; }
    cp "$PASO2/muse/mensaje_$etiq.md" "$MSGS/"
    lanzada=0
    for intento in 1 2 3 4 5; do
      if ESFUERZO="$ESF" "$RAIZ/muse_tarea.sh" "$etiq" "$MSGS/mensaje_$etiq.md" nueva; then
        lanzada=1; break
      fi
      echo "reintento de lanzamiento $intento ($etiq)"; sleep 20
    done
    [ "$lanzada" = 1 ] || { echo "NO LANZADA $etiq"; continue; }
    for i in $(seq 1 500); do
      [ -f "$TAREAS/$etiq.json" ] && break
      sleep 5
    done
    [ -f "$TAREAS/$etiq.json" ] || { echo "SIN META $etiq"; continue; }
    python3 "$PASO2/muse_unidad.py" recoger "$PASO2/$doc.md" "$RAIZ/$salida" "$n" b "$etiq" \
      || echo "FALLO recoger $etiq"
  done
done
echo "fin: $(date -Is)"
