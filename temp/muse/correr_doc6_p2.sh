#!/usr/bin/env bash
# Paso 2 de doc6: una unidad por turno, de a una, esperando el aviso de ntfy de cada tarea.
# No sondea: por cada unidad conecta el oyente del aviso ANTES de lanzar, y espera ese aviso.
set -u
cd /home/fratquintero/Documentos/Claude/jev-typesafe-spike
T="$(tr -d '[:space:]' < "$HOME/.config/dsh_tarea/ntfy_topic")"

for i in $(seq 1 14); do
  ETQ="p2-doc6-u$i-r1"
  MSG="temp/muse/mensaje_p2-doc6-u$i-r1.md"
  [ -f "$MSG" ] || { echo "$ETQ: falta el mensaje"; continue; }
  ( curl -s --no-buffer "https://ntfy.sh/$T/raw" | grep -m1 -F "muse:$ETQ" >/dev/null ) &
  OYENTE=$!
  if ESFUERZO=high ./utiliarios/muse_tarea.sh "$ETQ" "$MSG" nueva >/dev/null 2>&1; then
    wait "$OYENTE"
    echo "$(date +%H:%M:%S) $ETQ listo"
  else
    echo "$(date +%H:%M:%S) $ETQ: no se pudo lanzar"
    kill "$OYENTE" 2>/dev/null
  fi
done
echo "PASO 2 doc6 terminado"
