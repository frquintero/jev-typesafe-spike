"""Común a FU1: unidades del paso 1 (crudo de DeepSeek) y texto de cada unidad.

Cada unidad conserva la numeración original del documento: «[5] … [9] …».
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
UNIDADES = REPO / "unidades"
sys.path.insert(0, str(REPO / "niveles"))
sys.path.insert(0, str(UNIDADES))
from extraer_unidades import numerar_oraciones  # noqa: E402

MARCADOR = "{{TEXTO_NUMERADO}}"


def cargar_unidades(doc, crudo_paso1):
    """Devuelve (unidades, registros_doc). unidades: [{id, subtema, oraciones, texto, registros}]."""
    texto = (UNIDADES / "docs" / f"{doc}.md").read_text(encoding="utf-8")
    _, registros = numerar_oraciones(texto)
    por_n = {r["n"]: r for r in registros}
    paso1 = json.loads(Path(crudo_paso1).read_text(encoding="utf-8"))
    if paso1.get("doc") != doc:
        raise SystemExit(f"el crudo del paso 1 es de {paso1.get('doc')}, no de {doc}")
    unidades = []
    for i, s in enumerate(paso1["parsed"]["subtemas"], 1):
        regs = [por_n[n] for n in s["oraciones"]]
        unidades.append({
            "id": f"U{i}", "subtema": s["subtema"], "oraciones": s["oraciones"],
            "texto": " ".join(f"[{r['n']}] {r['oracion']}" for r in regs),
            "registros": regs,
        })
    return unidades, registros
