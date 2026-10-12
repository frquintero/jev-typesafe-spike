#!/usr/bin/env python3
"""Corre un prompt de UT sobre un documento (scratch) y verifica **contra el texto**.

El contrato: el modelo devuelve oraciones **literales**; el código las **ubica** en el texto, y de
ahí salen las coordenadas. La verificación es la del repo (`extraer_unidades.verificar_particion`):
literalidad, cobertura del cuerpo, asignación exclusiva y orden.

**No hay números de oración en ningún lado**: acá no se corta ni se numera — solo se ubica lo que el
modelo devolvió.

    bash -ic 'python3 temp/ut-sin-marcas/correr.py <doc> <alias> <esfuerzo> <rN> [prompt.md]'
"""

import hashlib
import json
import pathlib
import sys
import time
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parents[2]
AQUI = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ / "mvp" / "código"))

from extraer_unidades import roturas, verificar_particion  # noqa: E402
from mensajes import partir  # noqa: E402
from proveedores import llamar, resolver  # noqa: E402
from relojes import reloj_radicado, reloj_sistema  # noqa: E402
from respuesta import extract_json  # noqa: E402


def cuerpo(doc):
    """El texto del documento **entero**: los encabezados entran (son contexto), no se borran."""
    return (RAIZ / "mvp" / "documentos" / f"{doc}.md").read_text(encoding="utf-8").strip()


def main():
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    doc, alias, esfuerzo, rep = sys.argv[1:5]
    prompt = (pathlib.Path(sys.argv[5]).resolve() if len(sys.argv) > 5
              else RAIZ / "mvp" / "prompts" / "prompt_UT.md")
    version = "mvp" if prompt.stem == "prompt_UT" else prompt.stem.replace("prompt_UT_", "")
    destino = AQUI / "out" / f"{doc}-{alias}-{esfuerzo}-{version}-{rep}.json"
    if destino.exists():
        raise SystemExit(f"{destino.name}: ya está, no se vuelve a llamar")

    texto = cuerpo(doc)
    plantilla = prompt.read_text(encoding="utf-8")
    if "{{TEXTO}}" not in plantilla:
        raise SystemExit(f"{prompt.name}: le falta el hueco {{{{TEXTO}}}} — no se llama al modelo")
    # Los relojes van en el prompt del acto (el del radicado sale de `documentos.fecha_radicacion`).
    # Acá, en pruebas, el radicado se toma de la fecha del archivo: el documento no está radicado.
    rellenos = {"TEXTO": texto}
    if "{{RELOJ_RADICADO}}" in plantilla:
        rellenos["RELOJ_RADICADO"] = reloj_radicado(
            datetime.fromtimestamp((RAIZ / "mvp" / "documentos" / f"{doc}.md").stat().st_mtime))
    if "{{RELOJ_SISTEMA}}" in plantilla:
        rellenos["RELOJ_SISTEMA"] = reloj_sistema()
    # El material puede venir marcado como [TAREA] (convención del repo) o como [USUARIO]. La marca
    # no llega al modelo: `partir` la consume al partir.
    mensajes = partir(plantilla.replace("[USUARIO]", "[TAREA]"), prompt.name, **rellenos)
    config = resolver(alias, esfuerzo)

    t0 = time.time()
    enviado, respuesta = llamar(alias, mensajes=mensajes, esfuerzo=esfuerzo)
    segundos = round(time.time() - t0, 1)
    contenido = respuesta["choices"][0]["message"].get("content") or ""
    parsed, _, error = extract_json(contenido)
    unidades = (parsed or {}).get("unidades") or []
    informe = verificar_particion(texto, unidades) if parsed else None
    uso = respuesta.get("usage") or {}

    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps({
        "doc": doc, "cuerpo_sha256": hashlib.sha256(texto.encode()).hexdigest(),
        "alias": alias, "modelo": config["id"], "esfuerzo": config.get("esfuerzo"), "rN": rep,
        "segundos": segundos, "prompt": str(prompt.relative_to(RAIZ)),
        "hash_prompt": hashlib.sha256(plantilla.encode()).hexdigest(), "prompt_texto": plantilla,
        "finish_reason": respuesta["choices"][0].get("finish_reason"),
        "usage": uso, "cuerpo_enviado": enviado, "respuesta_cruda": contenido,
        "unidades": unidades, "informe": informe, "error_parseo": error,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  {destino.name}: {len(unidades)} UT · {segundos} s · "
          f"{respuesta['choices'][0].get('finish_reason')}")
    if informe:
        print(f"    contrato: literales {informe['literales']} · sin ubicar {len(informe['no_ubicadas'])} · "
              f"sin cubrir {len(informe['huecos'])} · solapes {len(informe['solapes'])} · "
              f"orden en UT {'✓' if informe['orden_en_unidades'] else '✗'} · "
              f"orden entre UT {'✓' if informe['orden_entre_unidades'] else '✗'}")
        if roturas(informe):
            print("    ROTO: " + " · ".join(roturas(informe)))
    for u in unidades:
        print(f"    · {u.get('subtema')}  [{len(u.get('oraciones') or [])} oraciones]")


if __name__ == "__main__":
    main()
