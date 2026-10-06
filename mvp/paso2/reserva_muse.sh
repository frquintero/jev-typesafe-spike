#!/usr/bin/env bash
# Paso 1 (v9 congelado) sobre los documentos de la reserva, con Muse Code.
# Replica el procedimiento de mvp/pruebas/correr_muse.sh, pero deja todo en
# mvp/paso2/. El mensaje se arma desde mvp/pruebas/prompt_v9.md tal cual.
#
#   ./mvp/paso2/reserva_muse.sh armar   <doc> <etiqueta>
#   ./mvp/paso2/reserva_muse.sh lanzar  <etiqueta> [esfuerzo]
#   ./mvp/paso2/reserva_muse.sh recoger <etiqueta>
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PASO2="$RAIZ/mvp/paso2"
PROMPT="$RAIZ/mvp/pruebas/prompt_v9.md"
SALIDA_MUSE="$HOME/.cache/muse_tareas"
MSGS="$HOME/.cache/muse_tarea_msgs"
MODO="${1:?uso: reserva_muse.sh armar|lanzar|recoger ...}"

armar() {
  local doc="$1" etiq="$2"
  RAIZ="$RAIZ" PASO2="$PASO2" PROMPT="$PROMPT" DOC="$doc" ETIQUETA="$etiq" python3 - <<'PY'
import json, os, pathlib, sys
raiz, paso2 = pathlib.Path(os.environ["RAIZ"]), pathlib.Path(os.environ["PASO2"])
doc = pathlib.Path(os.environ["DOC"])
if not doc.exists():
    doc = paso2 / os.environ["DOC"]
if not doc.exists():
    doc = raiz / "unidades" / "docs" / f"{os.environ['DOC']}.md"
prompt = pathlib.Path(os.environ["PROMPT"])
if not doc.exists() or not prompt.exists():
    raise SystemExit(f"no encuentro doc o prompt: {doc} | {prompt}")
sys.path.insert(0, str(raiz / "unidades"))
import extraer_unidades as eu
documento = doc.read_text(encoding="utf-8")
plantilla = prompt.read_text(encoding="utf-8")
enviado, registros = eu.numerar_oraciones(documento)
cabecera = f"""TAREA
Ejecuta el prompt del repo que va abajo sobre el documento indicado y devuelve
su salida. Trabajas en el repo jev-typesafe-spike.

NIVEL DE RAZONAMIENTO
{os.environ.get('ESF', 'high')}: hay que leer el documento y decidir; no es mecánico.

QUÉ NO HACER
- No escribas ni modifiques archivos del repo. No hagas commit ni push.
- No corras scripts del repo ni llames a APIs de modelos.
- No inventes: la salida se apoya en el texto.

QUÉ DEVOLVER
Solo el JSON de la estructura pedida, sin comentarios ni explicación alrededor.

---------------------------------------------------------------------
PROMPT (verbatim de `{prompt.relative_to(raiz)}`, con `{{{{TEXTO_NUMERADO}}}}` ya
sustituido; esto es exactamente lo que recibe el modelo)
---------------------------------------------------------------------

"""
mensaje = cabecera + plantilla.replace("{{TEXTO_NUMERADO}}", enviado)
destino = paso2 / f"mensaje_{os.environ['ETIQUETA']}.md"
destino.write_text(mensaje, encoding="utf-8")
meta = {"etiqueta": os.environ["ETIQUETA"], "doc": str(doc), "prompt": str(prompt),
        "marcador": "{{TEXTO_NUMERADO}}", "oraciones": len(registros)}
(paso2 / f"corrida_{os.environ['ETIQUETA']}.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"mensaje: {destino.relative_to(raiz)} ({len(mensaje)} bytes) | oraciones: {len(registros)}")
PY
}

lanzar() {
  local etiq="$1" esf="${2:-high}"
  mkdir -p "$MSGS"
  cp "$PASO2/mensaje_$etiq.md" "$MSGS/$etiq.md"
  cd "$RAIZ"
  ESFUERZO="$esf" ./utiliarios/muse_tarea.sh "$etiq" "$MSGS/$etiq.md" nueva
  echo "cuando termine: ./mvp/paso2/reserva_muse.sh recoger $etiq"
}

recoger() {
  local etiq="$1"
  for ext in out json jsonl err; do
    [ -f "$SALIDA_MUSE/$etiq.$ext" ] || { echo "falta $SALIDA_MUSE/$etiq.$ext" >&2; exit 2; }
  done
  cp "$SALIDA_MUSE/$etiq.out"   "$PASO2/salida_$etiq.md"
  cp "$SALIDA_MUSE/$etiq.jsonl" "$PASO2/salida_$etiq.jsonl"
  cp "$SALIDA_MUSE/$etiq.err"   "$PASO2/salida_$etiq.err"
  cp "$SALIDA_MUSE/$etiq.json"  "$PASO2/salida_${etiq}_meta.json"
  [ -f "$MSGS/$etiq.md" ] && cp "$MSGS/$etiq.md" "$PASO2/mensaje_${etiq}_enviado.md"
  RAIZ="$RAIZ" PASO2="$PASO2" ETIQUETA="$etiq" python3 - <<'PY'
import json, os, pathlib, sys
raiz, paso2 = pathlib.Path(os.environ["RAIZ"]), pathlib.Path(os.environ["PASO2"])
etiq = os.environ["ETIQUETA"]
sys.path.insert(0, str(raiz / "unidades"))
import extraer_unidades as eu
salida = (paso2 / f"salida_{etiq}.md").read_text(encoding="utf-8").strip()
parsed, cerca, error = eu.extract_json(salida)
meta = json.loads((paso2 / f"corrida_{etiq}.json").read_text(encoding="utf-8"))
doc = pathlib.Path(meta["doc"])
informe = {"parseo": bool(parsed), "venia_con_cerca": cerca, "error_parseo": error,
           "doc": str(doc)}
if parsed:
    _, registros = eu.numerar_oraciones(doc.read_text(encoding="utf-8"))
    if eu.es_caso_subtemas(parsed):
        informe["verificacion"] = eu.verificar_subtemas(parsed, registros)
        informe["unidades_reconstruidas"] = eu.reconstruir_subtemas(parsed, registros)
    else:
        informe["verificacion"] = eu.verificar(parsed, doc.read_text(encoding="utf-8"))
print("parseo:", "ok" if parsed else "FALLO", "| error:", error)
print("verificacion:", json.dumps(informe.get("verificacion"), ensure_ascii=False))
(paso2 / f"verificacion_{etiq}.json").write_text(
    json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
PY
}

case "$MODO" in
  armar)   armar "${2:?falta <doc>}" "${3:?falta <etiqueta>}" ;;
  lanzar)  lanzar "${2:?falta <etiqueta>}" "${3:-high}" ;;
  recoger) recoger "${2:?falta <etiqueta>}" ;;
  *) echo "modo desconocido: $MODO (armar|lanzar|recoger)" >&2; exit 2 ;;
esac
