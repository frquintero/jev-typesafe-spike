"""FU1, lado DeepSeek: ficha (mismo prompt) una llamada por unidad del paso 1.

Uso (desde la raíz, con HTTPS_PROXY y SSL_CERT_FILE exportados):
  python3 nblm-grafo-semantico/ficha_unidad_deepseek.py <doc> <modelo> <prompt> <rN> <crudo_paso1>

El prompt recibe en {{TEXTO_NUMERADO}} solo las oraciones de la unidad, con sus
números originales. Verificador de unidades/ficha_doc.py sobre las oraciones de
la unidad. No juzga el contenido. Crudo único (no se sobrescribe):
nblm-grafo-semantico/cache/fu-<doc>-<modelo>-<prompt>-<rN>.json
"""
import json
import sys
import time

from unidades_comun import MARCADOR, ROOT, UNIDADES, cargar_unidades
from run_niveles import call_model, extract_json  # noqa: E402
from ficha_doc import verificar  # noqa: E402


def main(doc, modelo, prompt_name, rep, crudo_paso1):
    out = ROOT / "cache" / f"fu-{doc}-{modelo}-{prompt_name}-{rep}.json"
    if out.exists():
        raise SystemExit(f"crudo ya existe, me detengo ({out})")
    prompt = (UNIDADES / "prompts" / f"{prompt_name}.md").read_text(encoding="utf-8")
    if prompt.count(MARCADOR) != 1:
        raise SystemExit("el prompt debe tener un único {{TEXTO_NUMERADO}}")
    unidades, _ = cargar_unidades(doc, crudo_paso1)
    crudo = {"doc": doc, "modelo": modelo, "prompt": prompt_name, "rep": rep,
             "crudo_paso1": str(crudo_paso1), "unidades": []}
    t0 = time.time()
    for u in unidades:
        enviado = prompt.replace(MARCADOR, u["texto"])
        t = time.time()
        body, resp = call_model("toulmin", modelo, enviado)
        seg = round(time.time() - t, 1)
        parsed, cerca, err = extract_json(resp["choices"][0]["message"]["content"])
        ver = verificar(parsed, u["registros"]) if isinstance(parsed, dict) else None
        crudo["unidades"].append({**u, "segundos": seg, "request": body, "response": resp,
                                  "parsed": parsed, "venia_con_cerca": cerca,
                                  "error_parseo": err, "verificacion": ver})
        print(json.dumps({u["id"]: seg, "oraciones": u["oraciones"],
                          "modelo_efectivo": resp.get("model"),
                          "no_literales": len(ver["no_literales"]) if ver else None}), flush=True)
    crudo["segundos_total"] = round(time.time() - t0, 1)
    with out.open("x", encoding="utf-8") as f:
        json.dump(crudo, f, ensure_ascii=False, indent=2)
    print(f"hecho -> {out} ({crudo['segundos_total']} s)")


if __name__ == "__main__":
    if len(sys.argv) != 6:
        raise SystemExit(__doc__)
    main(*sys.argv[1:])
