#!/usr/bin/env bash
# Envoltorio para delegar una tarea a DeepSeek Harness por terminal
# (dsh headless) y recibir un aviso cuando termina. Uso exclusivo de Claude y
# ChatGPT, con autorización expresa y previa de Frat (ver AGENTS.md,
# «DeepSeek Harness por terminal»).
#
# Uso (desde cualquier carpeta; trabaja siempre en la raíz del repo):
#   ./utiliarios/dsh_tarea.sh <etiqueta> <archivo_mensaje> [<session-id>|nueva]
#
#   etiqueta         nombre corto de la tarea (letras, números, - y _)
#   archivo_mensaje  el mensaje para DeepSeek (fuera del repo, p. ej. /tmp/…)
#   session-id       sesión a continuar; «nueva» crea una (por defecto: la de
#                    ~/.config/dsh_tarea/sesion, si existe; si no, nueva)
#
# Qué hace: corre dsh headless en segundo plano y devuelve el control al
# instante. Al terminar DeepSeek, escribe el resultado en
# ~/.cache/dsh_tareas/<etiqueta>.{out,err,json} y publica en ntfy.sh el aviso
#   "<etiqueta> exit=<código> <segundos>s"
# en el tema privado guardado en ~/.config/dsh_tarea/ntfy_topic (fuera del
# repo, que es público: el nombre del tema no se escribe en el repo).
# Con una sesión nueva, guarda su id en ~/.cache/dsh_tareas/<etiqueta>.json
# (campo session_id).
#
# Esfuerzo de razonamiento: variable ESFUERZO = off | low | high | max,
# OBLIGATORIA (sin valor por defecto: se elige en cada corrida según la
# tarea). Se aplica por llamada con --patch
# (~/.config/dsh_tarea/esfuerzo/<nivel>.yml), también al continuar una sesión.
# Política de uso: Claude-memoria/memoria/agentes-delegados.md, §8.

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CONF="$HOME/.config/dsh_tarea"
SALIDA="$HOME/.cache/dsh_tareas"
DSH="${DSH:-$HOME/.npm/_npx/1e7f6d9597241db0/node_modules/.bin/dsh}"

[ $# -ge 2 ] || { sed -n '2,25p' "$0"; exit 2; }
ETIQ="$1"; MSG="$2"; SES="${3:-}"
[[ "$ETIQ" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "etiqueta inválida: $ETIQ" >&2; exit 2; }
[ -f "$MSG" ] || { echo "no existe el mensaje: $MSG" >&2; exit 2; }
[ -x "$DSH" ] || { echo "no encuentro dsh en $DSH" >&2; exit 2; }
[ -f "$CONF/ntfy_topic" ] || { echo "falta $CONF/ntfy_topic" >&2; exit 2; }
TOPIC="$(tr -d '[:space:]' < "$CONF/ntfy_topic")"
if [ -z "$SES" ] && [ -f "$CONF/sesion" ]; then SES="$(tr -d '[:space:]' < "$CONF/sesion")"; fi
[ "$SES" = "nueva" ] && SES=""
ESF="${ESFUERZO:-}"
[ -n "$ESF" ] || { echo "falta ESFUERZO (off|low|high|max): elígelo según la tarea (agentes-delegados.md, §8)" >&2; exit 2; }
[[ "$ESF" =~ ^(off|low|high|max)$ ]] || { echo "ESFUERZO inválido: $ESF (off|low|high|max)" >&2; exit 2; }
PATCH="$CONF/esfuerzo/$ESF.yml"
[ -f "$PATCH" ] || { echo "falta $PATCH" >&2; exit 2; }
mkdir -p "$SALIDA"
for ext in out err json; do
  [ -e "$SALIDA/$ETIQ.$ext" ] && { echo "ya existe $SALIDA/$ETIQ.$ext: usa otra etiqueta" >&2; exit 2; }
done
cp "$MSG" "$SALIDA/$ETIQ.msg"

(
  cd "$REPO"
  inicio=$(date +%s)
  if [ -n "$SES" ]; then
    "$DSH" headless --patch "$PATCH" --session-id "$SES" - < "$SALIDA/$ETIQ.msg" > "$SALIDA/$ETIQ.out" 2> "$SALIDA/$ETIQ.err" && rc=0 || rc=$?
    sid="$SES"
  else
    "$DSH" headless --patch "$PATCH" --json - < "$SALIDA/$ETIQ.msg" > "$SALIDA/$ETIQ.jsonl" 2> "$SALIDA/$ETIQ.err" && rc=0 || rc=$?
    sid=$(grep -o '"sessionId":"session-[a-f0-9-]*"' "$SALIDA/$ETIQ.jsonl" | head -1 | cut -d'"' -f4 || true)
    python3 -c 'import json,sys
for l in open(sys.argv[1],encoding="utf-8"):
    e=json.loads(l)
    if e.get("type")=="final": print(e.get("text",""))' "$SALIDA/$ETIQ.jsonl" > "$SALIDA/$ETIQ.out" 2>/dev/null || true
  fi
  seg=$(( $(date +%s) - inicio ))
  printf '{"etiqueta":"%s","session_id":"%s","esfuerzo":"%s","exit":%s,"segundos":%s,"inicio":%s}\n' \
    "$ETIQ" "$sid" "$ESF" "$rc" "$seg" "$inicio" > "$SALIDA/$ETIQ.json"
  curl -s -m 15 -d "$ETIQ exit=$rc ${seg}s" "https://ntfy.sh/$TOPIC" > /dev/null || true
) > /dev/null 2>&1 &
disown
echo "lanzada: $ETIQ (sesión: ${SES:-nueva}, esfuerzo: $ESF); resultado en $SALIDA/$ETIQ.out"
