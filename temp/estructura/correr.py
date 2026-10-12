#!/usr/bin/env python3
"""Corre un prompt de estructura (el índice) sobre un documento, en el scratch.

Acepta **los dos formatos** que fuimos probando:

- **por niveles**: `{"indice":[{"nivel":2,"titulo":"…"}]}` — la jerarquía en un entero;
- **por padres**: `{"indice":[{"n":2,"titulo":"…","padre":1}]}` — cada encabezado dice de cuál cuelga.

En los dos, el modelo devuelve **encabezados literales** y el código hace el resto:

- los **ubica** en el texto (`extraer_unidades.ubicar`, el mismo que ubica las oraciones);
- calcula **la sección que abre** cada uno (hasta el próximo encabezado que no cuelga de él);
- deriva la **numeración** del índice (`1`, `1.1`, `1.3.1` …): no se le pide al modelo;
- verifica lo mecánico: literales en el texto, orden, numeración de nodos, padres anteriores.

Los relojes se llenan **si el prompt los pide**: la regla dice que todo prompt los lleva, pero un
prompt de prueba puede no tenerlos, y el corredor no lo obliga.

    bash -ic 'python3 temp/estructura/correr.py <doc> <alias> <esfuerzo> <rN> [prompt.md]'
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

from extraer_unidades import ubicar  # noqa: E402
from mensajes import partir  # noqa: E402
from proveedores import llamar, resolver  # noqa: E402
from relojes import reloj_radicado, reloj_sistema  # noqa: E402
from respuesta import extract_json  # noqa: E402


def es_por_padres(nodos):
    return bool(nodos) and all("padre" in nodo for nodo in nodos)


def _subarbol(i, padres):
    """Los índices de los nodos que cuelgan de `i` (sin contarlo)."""
    dentro, pila = set(), [i]
    while pila:
        actual = pila.pop()
        for j, padre in enumerate(padres):
            if padre == actual + 1 and j not in dentro:
                dentro.add(j)
                pila.append(j)
    return dentro


def _numeracion_de_arbol(padres):
    """`1`, `1.1`, `1.2`, `1.3`, `1.3.1` … a partir de los padres."""
    etiquetas, contador_hijo, raiz = [], {}, 0
    for padre in padres:
        if not padre:
            raiz += 1
            etiquetas.append(str(raiz))
            continue
        etiqueta_padre = etiquetas[padre - 1]
        contador_hijo[etiqueta_padre] = contador_hijo.get(etiqueta_padre, 0) + 1
        etiquetas.append(f"{etiqueta_padre}.{contador_hijo[etiqueta_padre]}")
    return etiquetas


def _numeracion_por_niveles(niveles):
    contadores, etiquetas = {}, []
    for nivel in niveles:
        contadores[nivel] = contadores.get(nivel, 0) + 1
        for mas_profundo in [k for k in contadores if k > nivel]:
            del contadores[mas_profundo]
        etiquetas.append(".".join(str(contadores[k]) for k in sorted(contadores)))
    return etiquetas


def con_coordenadas(texto, nodos):
    """Ubica cada título y calcula la sección que abre. Devuelve las filas y los títulos ausentes."""
    titulos = [str(nodo.get("titulo") or "") for nodo in nodos]
    tramos, ausentes = ubicar(texto, titulos, [])
    filas = [{"n": n, "titulo": titulos[n - 1], "desde": tramo[0], "hasta": tramo[1]}
             for n, tramo in enumerate(tramos, 1)]
    for i, fila in enumerate(filas):
        fin = len(texto)
        if es_por_padres(nodos) and i < len(nodos):
            padres = [nodo.get("padre") for nodo in nodos]
            dentro = _subarbol(i, padres)
            for j in range(i + 1, len(filas)):
                if j not in dentro:
                    fin = filas[j]["desde"]
                    break
        else:
            for fila2 in filas[i + 1:]:
                if (fila2.get("nivel") or 0) <= (fila.get("nivel") or 0):
                    fin = fila2["desde"]
                    break
        fila["seccion_desde"], fila["seccion_hasta"] = fila["desde"], fin
    return filas, ausentes


def roturas(nodos, filas, ausentes):
    """Lo que hace inconsistente el índice con el texto (no es una lectura, es una rotura)."""
    rotas = []
    if ausentes:
        rotas.append(f"títulos que no están en el texto: {ausentes}")
    if not filas:
        return rotas or ["no hay ningún nodo"]
    if len(filas) != len(nodos):
        rotas.append(f"el índice trae {len(nodos)} nodos y se ubicaron {len(filas)}")
    desorden = [(a["titulo"], b["titulo"]) for a, b in zip(filas, filas[1:]) if b["desde"] < a["desde"]]
    if desorden:
        rotas.append(f"nodos fuera del orden del texto: {desorden}")
    vacios = [f["n"] for f in filas if not f["titulo"].strip()]
    if vacios:
        rotas.append(f"nodos sin título: {vacios}")
    if es_por_padres(nodos):
        padres = [nodo.get("padre") for nodo in nodos]
        if [nodo.get("n") for nodo in nodos] != list(range(1, len(nodos) + 1)):
            rotas.append(f"los `n` no son 1..{len(nodos)} en orden: "
                         f"{[nodo.get('n') for nodo in nodos]}")
        malos = [(i + 1, p) for i, p in enumerate(padres)
                 if not isinstance(p, int) or p < 0 or p >= i + 1]
        if malos:
            rotas.append(f"padres que no son 0 ni un número anterior: {malos}")
        for i, p in enumerate(padres):
            if isinstance(p, int) and 0 < p < i + 1 and i + 1 not in _subarbol(p - 1, padres):
                pass  # el subárbol se calcula al revés; el chequeo real es que el padre sea anterior
    else:
        niveles = [fila.get("nivel") for fila in filas]
        if any(not isinstance(n, int) or n < 1 for n in niveles):
            rotas.append(f"niveles que no son enteros ≥ 1: {niveles}")
        else:
            saltos = [(a, b) for a, b in zip(niveles, niveles[1:]) if b > a + 1]
            if saltos:
                rotas.append(f"niveles que saltan: {saltos}")
    return rotas


def main():
    if len(sys.argv) < 5:
        raise SystemExit(__doc__)
    doc, alias, esfuerzo, rep = sys.argv[1:5]
    prompt = (pathlib.Path(sys.argv[5]).resolve() if len(sys.argv) > 5
              else AQUI.parents[1] / "mvp" / "prompts" / "prompt_volcado.md")
    version = prompt.stem.replace("prompt_ESTRUCTURA_", "").replace("prompt_", "")
    destino = AQUI / "out" / f"{doc}-{alias}-{esfuerzo}-{version}-{rep}.json"
    if destino.exists():
        raise SystemExit(f"{destino.name}: ya está, no se vuelve a llamar")

    ruta = AQUI / f"{doc}.md"
    texto = ruta.read_text(encoding="utf-8").strip()
    plantilla = prompt.read_text(encoding="utf-8")
    if "{{TEXTO}}" not in plantilla:
        raise SystemExit(f"{prompt.name}: le falta el hueco {{{{TEXTO}}}}")
    rellenos = {"TEXTO": texto}
    if "{{RELOJ_RADICADO}}" in plantilla:
        rellenos["RELOJ_RADICADO"] = reloj_radicado(datetime.fromtimestamp(ruta.stat().st_mtime))
    if "{{RELOJ_SISTEMA}}" in plantilla:
        rellenos["RELOJ_SISTEMA"] = reloj_sistema()
    mensajes = partir(plantilla, prompt.name, **rellenos)
    config = resolver(alias, esfuerzo)

    t0 = time.time()
    enviado, respuesta = llamar(alias, mensajes=mensajes, esfuerzo=esfuerzo)
    segundos = round(time.time() - t0, 1)
    contenido = respuesta["choices"][0]["message"].get("content") or ""
    parsed, _, error = extract_json(contenido)
    nodos = (parsed or {}).get("indice") or []
    filas, ausentes = con_coordenadas(texto, nodos) if parsed else ([], [])
    por_padres = es_por_padres(nodos)
    etiquetas = (_numeracion_de_arbol([nodo.get("padre") for nodo in nodos]) if por_padres
                 else _numeracion_por_niveles([fila.get("nivel") or 1 for fila in filas]))
    rotas = roturas(nodos, filas, ausentes) if parsed else ["sin JSON"]
    uso = respuesta.get("usage") or {}

    destino.parent.mkdir(exist_ok=True)
    destino.write_text(json.dumps({
        "doc": doc, "texto_sha256": hashlib.sha256(texto.encode()).hexdigest(),
        "alias": alias, "modelo": config["id"], "esfuerzo": config.get("esfuerzo"), "rN": rep,
        "segundos": segundos, "prompt": str(prompt.relative_to(RAIZ)),
        "hash_prompt": hashlib.sha256(plantilla.encode()).hexdigest(), "prompt_texto": plantilla,
        "finish_reason": respuesta["choices"][0].get("finish_reason"), "usage": uso,
        "cuerpo_enviado": enviado, "respuesta_cruda": contenido,
        "formato": "padres" if por_padres else "niveles",
        "indice": nodos, "filas": filas, "numeracion": etiquetas, "roturas": rotas,
        "error_parseo": error,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"  {destino.name}: {len(nodos)} nodos · formato {'padres' if por_padres else 'niveles'} · "
          f"{segundos} s · {respuesta['choices'][0].get('finish_reason')}")
    print(f"    roturas: {rotas or 'ninguna'}")
    print(f"    {'índice':<8}{'n':<4}{'padre':<7}{'título':<40}{'encabezado':<14}{'sección'}")
    for etiqueta, fila, nodo in zip(etiquetas, filas, nodos):
        titulo = fila["titulo"] if len(fila["titulo"]) <= 38 else fila["titulo"][:37] + "…"
        padre = nodo.get("padre") if por_padres else ""
        print(f"    {etiqueta:<8}{fila['n']:<4}{str(padre):<7}«{titulo}»{' ' * max(0, 38 - len(titulo))}"
              f"{fila['desde']:>5}–{fila['hasta']:<8}{fila['seccion_desde']:>5}–{fila['seccion_hasta']}")


if __name__ == "__main__":
    main()
