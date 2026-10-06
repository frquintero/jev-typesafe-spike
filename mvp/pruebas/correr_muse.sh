#!/usr/bin/env bash
# Paso 1 con Muse Code: arma el mensaje desde un documento y un prompt del repo,
# lo deja fuera del repo y lanza la tarea. Todo en un solo proceso: no depende
# de /tmp (que en el sandbox del Harness no persiste entre llamadas).
#
#   ./mvp/pruebas/correr_muse.sh correr  <doc> <prompt> <etiqueta> [esfuerzo]
#   ./mvp/pruebas/correr_muse.sh seco    <doc> <prompt> <etiqueta>
#   ./mvp/pruebas/correr_muse.sh recoger <etiqueta> [<doc>]
#
#   <doc>     ruta al documento, o nombre suelto de unidades/docs (p. ej. tec1)
#   <prompt>  nombre de unidades/prompts sin .md (p. ej. unidades_v5)
#   <etiqueta> identificador corto y nuevo para la corrida
#   [esfuerzo] off | low | high | max   (por defecto: high)
#
# El mensaje queda en mvp/pruebas/mensaje_<etiqueta>.md (registro) y en
# ~/.cache/muse_tarea_msgs/<etiqueta>.md (lo que lee el envoltorio).
# Al terminar Muse: ./mvp/pruebas/correr_muse.sh recoger <etiqueta> trae la
# salida a la carpeta y la verifica con el verificador del repo.
set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PRUEBAS="$RAIZ/mvp/pruebas"
SALIDA_MUSE="$HOME/.cache/muse_tareas"
MSGS="$HOME/.cache/muse_tarea_msgs"
MODO="${1:?uso: correr_muse.sh correr|seco|recoger ...}"

# --- arma el mensaje ---------------------------------------------------------
construir() {
  local doc="$1" prompt="$2" etiqueta="$3"
  RAIZ="$RAIZ" DOC="$doc" PROMPT="$prompt" ETIQUETA="$etiqueta" PRUEBAS="$PRUEBAS" python3 - <<'PY'
import json, os, pathlib, sys
raiz, pruebas = pathlib.Path(os.environ["RAIZ"]), pathlib.Path(os.environ["PRUEBAS"])
doc_arg, prompt_arg, etiq = os.environ["DOC"], os.environ["PROMPT"], os.environ["ETIQUETA"]
sys.path.insert(0, str(raiz / "unidades"))
import extraer_unidades as eu

doc = pathlib.Path(doc_arg)
if not doc.exists():
    doc = pruebas / doc_arg
if not doc.exists():
    doc = raiz / "unidades" / "docs" / (doc_arg if doc_arg.endswith(".md") else f"{doc_arg}.md")
if not doc.exists():
    raise SystemExit(f"no encuentro el documento: {doc_arg}")
p = pathlib.Path(prompt_arg)
if not p.suffix:
    p = raiz / "unidades" / "prompts" / f"{prompt_arg}.md"
if not p.exists():
    raise SystemExit(f"no encuentro el prompt: {prompt_arg}")
doc, p = doc.resolve(), p.resolve()

texto = doc.read_text(encoding="utf-8")
plantilla = p.read_text(encoding="utf-8")
if "{{TEXTO_NUMERADO}}" in plantilla:
    enviado, registros = eu.numerar_oraciones(texto)
    marcador = "{{TEXTO_NUMERADO}}"
else:
    enviado, registros = texto, None
    marcador = "{{TEXTO}}"

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
PROMPT (verbatim de `{p.relative_to(raiz)}`, con `{marcador}` ya sustituido;
esto es exactamente lo que recibe el modelo cuando corre
`python3 unidades/extraer_unidades.py`)
---------------------------------------------------------------------

"""
mensaje = cabecera + plantilla.replace(marcador, enviado)
destino = pruebas / f"mensaje_{etiq}.md"
destino.write_text(mensaje, encoding="utf-8")
n_oraciones = len(registros) if registros else len(eu.oraciones(texto))
meta = {"etiqueta": etiq, "doc": str(doc), "prompt": str(p),
        "marcador": marcador, "oraciones": n_oraciones}
(pruebas / f"corrida_{etiq}.json").write_text(
    json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"mensaje: {destino.relative_to(raiz)} ({len(mensaje)} bytes)")
print(f"meta: mvp/pruebas/corrida_{etiq}.json")
print(f"oraciones: {n_oraciones}")
print(f"texto enviado:\n{enviado}")
PY
}

# --- trae la salida y verifica ----------------------------------------------
recoger() {
  local etiq="$1" doc_arg="${2:-}"
  local base="$SALIDA_MUSE/$etiq"
  for ext in out json jsonl err; do
    [ -f "$base.$ext" ] || { echo "falta $base.$ext" >&2; exit 2; }
  done
  cp "$base.out"  "$PRUEBAS/salida_$etiq.md"
  cp "$base.jsonl" "$PRUEBAS/salida_$etiq.jsonl"
  cp "$base.err"  "$PRUEBAS/salida_$etiq.err"
  cp "$base.json" "$PRUEBAS/salida_${etiq}_meta.json"
  [ -f "$MSGS/$etiq.md" ] && cp "$MSGS/$etiq.md" "$PRUEBAS/mensaje_${etiq}_enviado.md"
  RAIZ="$RAIZ" PRUEBAS="$PRUEBAS" ETIQUETA="$etiq" DOC="$doc_arg" python3 - <<'PY'
import json, os, pathlib, sys
raiz, pruebas = pathlib.Path(os.environ["RAIZ"]), pathlib.Path(os.environ["PRUEBAS"])
etiq = os.environ["ETIQUETA"]
sys.path.insert(0, str(raiz / "unidades"))
import extraer_unidades as eu

salida = (pruebas / f"salida_{etiq}.md").read_text(encoding="utf-8").strip()
parsed, cerca, error = eu.extract_json(salida)
print(f"parseo: {'ok' if parsed else 'FALLO'} | venia_con_cerca: {cerca} | error: {error}")
informe = {"parseo": bool(parsed), "venia_con_cerca": cerca, "error_parseo": error}
if parsed:
    doc_arg = os.environ.get("DOC") or ""
    meta_path = pruebas / f"corrida_{etiq}.json"
    if doc_arg:
        doc_path = pathlib.Path(doc_arg)
        if not doc_path.exists():
            doc_path = pruebas / doc_arg
    elif meta_path.exists():
        doc_path = pathlib.Path(json.loads(meta_path.read_text(encoding="utf-8"))["doc"])
    else:
        raise SystemExit(
            f"falta mvp/pruebas/corrida_{etiq}.json: pasa el documento "
            f"(recoger {etiq} <doc>)")
    if not doc_path.exists():
        raise SystemExit(f"no encuentro el documento de la corrida: {doc_path}")
    doc = doc_path.read_text(encoding="utf-8")
    informe["doc"] = str(doc_path)
    _, registros = eu.numerar_oraciones(doc)
    if eu.es_caso_subtemas(parsed):
        informe["verificacion"] = eu.verificar_subtemas(parsed, registros)
        informe["unidades_reconstruidas"] = eu.reconstruir_subtemas(parsed, registros)
    else:
        unidades = parsed.get("unidades", [])
        if unidades and all("desde" in u and "hasta" in u for u in unidades):
            informe["verificacion"] = eu.verificar_rangos(parsed, registros)
            informe["unidades_reconstruidas"] = eu.reconstruir_unidades(parsed, registros)
        else:
            informe["verificacion"] = eu.verificar(parsed, doc)
    print("verificacion:", json.dumps(informe["verificacion"], ensure_ascii=False))
(pruebas / f"verificacion_{etiq}.json").write_text(json.dumps(informe, ensure_ascii=False, indent=2), encoding="utf-8")
print(f"verificacion: mvp/pruebas/verificacion_{etiq}.json")
PY
}

case "$MODO" in
  seco)
    construir "${2:?falta <doc>}" "${3:?falta <prompt>}" "${4:?falta <etiqueta>}"
    echo "(modo seco: no se lanza nada)"
    ;;
  correr)
    ETIQUETA="${4:?uso: correr <doc> <prompt> <etiqueta> [esfuerzo]}"
    ESF="${5:-high}"
    export ESF
    construir "$2" "$3" "$ETIQUETA"
    mkdir -p "$MSGS"
    cp "$PRUEBAS/mensaje_$ETIQUETA.md" "$MSGS/$ETIQUETA.md"
    cd "$RAIZ"
    ESFUERZO="$ESF" ./utiliarios/muse_tarea.sh "$ETIQUETA" "$MSGS/$ETIQUETA.md" nueva
    echo "cuando termine: ./mvp/pruebas/correr_muse.sh recoger $ETIQUETA"
    ;;
  recoger)
    recoger "${2:?falta <etiqueta>}" "${3:-}"
    ;;
  *)
    echo "modo desconocido: $MODO (correr|seco|recoger)" >&2
    exit 2
    ;;
esac
