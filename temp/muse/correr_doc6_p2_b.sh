#!/usr/bin/env bash
# Paso 2 de doc6, unidades 2 a 14: de a una, esperando el aviso de ntfy de cada tarea.
# Escucha con `since=15m` para no perder un aviso que haya salido antes de conectar.
set -u
cd /home/fratquintero/Documentos/Claude/jev-typesafe-spike
T="$(tr -d '[:space:]' < "$HOME/.config/dsh_tarea/ntfy_topic")"
CACHE="$HOME/.cache/muse_tareas"

for i in $(seq 3 14); do
  ETQ="p2-doc6-u$i-r1"
  MSG="temp/muse/mensaje_p2-doc6-u$i-r1.md"
  if [ -s "$CACHE/$ETQ.out" ]; then echo "$(date +%H:%M:%S) $ETQ: ya estaba listo"; continue; fi
  [ -f "$MSG" ] || { echo "$(date +%H:%M:%S) $ETQ: falta el mensaje"; continue; }
  ( curl -s --no-buffer "https://ntfy.sh/$T/raw?since=15m" | grep -m1 -F "muse:$ETQ" >/dev/null ) &
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
