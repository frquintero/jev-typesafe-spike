#!/usr/bin/env bash
# Envoltorio para delegar una tarea a Muse Code sin terminal y recibir un
# aviso cuando termina (análogo a dsh_tarea.sh). Uso exclusivo de Claude y
# ChatGPT, con autorización expresa y previa de Frat (ver AGENTS.md).
#
# Uso (trabaja siempre en la raíz del repo):
#   ./muse_tarea.sh <etiqueta> <archivo_mensaje> [<uuid>|nueva]
#
#   etiqueta         nombre corto de la tarea (letras, números, - y _)
#   archivo_mensaje  el mensaje para Muse (fuera del repo, p. ej. /tmp/…)
#   uuid             sesión a continuar; «nueva» crea una con un uuid nuevo
#                    (por defecto: la de ~/.config/muse_tarea/sesion si
#                    existe; si no, nueva)
#
# Muse corre con la suscripción Everyday (nunca con META_API_KEY), sin
# sandbox y SIN aprobaciones (decisión de Frat, 04-10: sin terminal no hay
# quién apruebe), con tope de tiempo (MUSE_TAREA_TIMEOUT, 1800 s) y sin
# auto-actualizarse. Una sola tarea de Muse a la vez (candado).
# Al terminar deja en ~/.cache/muse_tareas/<etiqueta>.{jsonl,out,err,json,msg}
# y publica en ntfy.sh "muse:<etiqueta> exit=<código> <segundos>s" en el tema
# privado de ~/.config/dsh_tarea/ntfy_topic (el mismo de dsh_tarea.sh).

set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="$HOME/.config/muse_tarea"
SALIDA="$HOME/.cache/muse_tareas"
MUSE="${MUSE_BIN:-$HOME/.local/bin/muse}"
TOPE="${MUSE_TAREA_TIMEOUT:-1800}"

[ $# -ge 2 ] || { sed -n '2,23p' "$0"; exit 2; }
ETIQ="$1"; MSG="$2"; SES="${3:-}"
[[ "$ETIQ" =~ ^[A-Za-z0-9_-]+$ ]] || { echo "etiqueta inválida: $ETIQ" >&2; exit 2; }
[ -f "$MSG" ] || { echo "no existe el mensaje: $MSG" >&2; exit 2; }
[ -x "$MUSE" ] || { echo "no encuentro muse en $MUSE" >&2; exit 2; }
[ -f "$HOME/.config/dsh_tarea/ntfy_topic" ] || { echo "falta ~/.config/dsh_tarea/ntfy_topic" >&2; exit 2; }
TOPIC="$(tr -d '[:space:]' < "$HOME/.config/dsh_tarea/ntfy_topic")"
if [ -z "$SES" ] && [ -f "$CONF/sesion" ]; then SES="$(tr -d '[:space:]' < "$CONF/sesion")"; fi
if [ -z "$SES" ] || [ "$SES" = "nueva" ]; then SES="$(python3 -c 'import uuid;print(uuid.uuid4())')"; fi
mkdir -p "$SALIDA"
for ext in out err json jsonl; do
  [ -e "$SALIDA/$ETIQ.$ext" ] && { echo "ya existe $SALIDA/$ETIQ.$ext: usa otra etiqueta" >&2; exit 2; }
done
CANDADO="$SALIDA/.muse.lock"
exec 9>"$CANDADO"
flock -n 9 || { echo "ya hay una tarea de Muse corriendo; espera a que termine" >&2; exit 3; }
cp "$MSG" "$SALIDA/$ETIQ.msg"

(
  cd "$REPO"
  inicio=$(date +%s)
  env -u META_API_KEY MUSE_NO_AUTO_UPDATE=1 timeout "$TOPE" "$MUSE" exec \
      --disable-sandbox --disable-approval --json --session-id "$SES" \
      --prompt-file "$SALIDA/$ETIQ.msg" \
      > "$SALIDA/$ETIQ.jsonl" 2> "$SALIDA/$ETIQ.err" && rc=0 || rc=$?
  python3 - "$SALIDA/$ETIQ.jsonl" > "$SALIDA/$ETIQ.out" 2>/dev/null <<'PY' || true
import json, sys
ultimo = ""
for l in open(sys.argv[1], encoding="utf-8"):
    try:
        p = json.loads(l).get("payload") or {}
    except Exception:
        continue
    if p.get("kind") == "run_terminal" and isinstance(p.get("text"), str):
        ultimo = p["text"]
print(ultimo)
PY
  seg=$(( $(date +%s) - inicio ))
  printf '{"etiqueta":"%s","session_id":"%s","exit":%s,"segundos":%s,"inicio":%s}\n' \
    "$ETIQ" "$SES" "$rc" "$seg" "$inicio" > "$SALIDA/$ETIQ.json"
  curl -s -m 15 -d "muse:$ETIQ exit=$rc ${seg}s" "https://ntfy.sh/$TOPIC" > /dev/null || true
) > /dev/null 2>&1 &
disown
echo "lanzada: $ETIQ (sesión Muse: $SES); resultado en $SALIDA/$ETIQ.out"
