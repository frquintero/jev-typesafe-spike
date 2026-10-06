#!/usr/bin/env bash
# Comparación del paso 2 con Muse Code: una tarea por (documento, entrada, unidad).
# Secuencial: el envoltorio de Muse admite una sola tarea a la vez. Idempotente:
# salta los crudos que ya existen y nunca los sobrescribe.
# Uso: ./mvp/paso2/comparacion_muse.sh [esfuerzo] [rN]
set -uo pipefail
RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASO2="$RAIZ/mvp/paso2"
ESF="${1:-high}"
REP="${2:-r1}"
MSGS="$HOME/.cache/muse_tarea_msgs"
TAREAS="$HOME/.cache/muse_tareas"
mkdir -p "$MSGS"

DOCS=("doc4|mvp/pruebas/salida_prueba8-v9-doc4.md|6"
      "doc5|mvp/pruebas/salida_prueba9-v9-doc5.md|5")

for fila in "${DOCS[@]}"; do
  IFS='|' read -r doc salida nun <<< "$fila"
  for entrada in a b c; do
    for n in $(seq 1 "$nun"); do
      etiq="p2-$doc-$entrada-u$n-$REP"
      crudo="$PASO2/cache/comp-$doc-$entrada-u$n-muse-$REP.json"
      if [ -f "$crudo" ]; then echo "ya está: $etiq"; continue; fi
      echo "=== $etiq ($(date -Is)) ==="
      python3 "$PASO2/muse_unidad.py" armar "$RAIZ/mvp/pruebas/$doc.md" "$RAIZ/$salida" "$n" "$entrada" "$etiq" \
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
      for i in $(seq 1 300); do
        [ -f "$TAREAS/$etiq.json" ] && break
        sleep 5
      done
      if [ ! -f "$TAREAS/$etiq.json" ]; then echo "SIN META $etiq"; continue; fi
      python3 "$PASO2/muse_unidad.py" recoger "$RAIZ/mvp/pruebas/$doc.md" "$RAIZ/$salida" "$n" "$entrada" "$etiq" \
        || echo "FALLO recoger $etiq"
    done
  done
done
echo "fin: $(date -Is)"
