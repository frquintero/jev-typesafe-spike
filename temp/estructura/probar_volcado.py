#!/usr/bin/env python3
"""Prototipo del volcado: del texto fuente + el índice, al **markdown** que va al almacén.

El modelo decide qué líneas son encabezados y de qué cuelgan; el código hace el resto: ubica los
títulos, deriva la profundidad, **construye el markdown** y verifica que no inventó nada.

    python3 temp/estructura/probar_volcado.py <doc> [crudo.json]
"""

import json
import pathlib
import re
import sys

AQUI = pathlib.Path(__file__).resolve().parent


def profundidades(padres):
    """La profundidad de cada nodo en el bosque: 1 para las raíces."""
    prof = []
    for i, padre in enumerate(padres):
        prof.append(1 if not padre else prof[padre - 1] + 1)
    return prof


def subarboles(padres):
    """Para cada nodo, el conjunto de sus descendientes."""
    hijos = {i: [] for i in range(len(padres))}
    for i, padre in enumerate(padres):
        if padre:
            hijos[padre - 1].append(i)
    dentro = {}
    for i in range(len(padres)):
        vistos, pila = set(), [i]
        while pila:
            actual = pila.pop()
            for h in hijos[actual]:
                if h not in vistos:
                    vistos.add(h)
                    pila.append(h)
        dentro[i] = vistos
    return dentro


def contiguos(padres):
    """¿El subárbol de cada nodo es un tramo contiguo del orden? (markdown no sabe de cruces)."""
    malos = []
    for i, dentro in subarboles(padres).items():
        if dentro and sorted(dentro) != list(range(min(dentro), max(dentro) + 1)):
            malos.append((i + 1, sorted(dentro)))
    return malos


def armar_markdown(texto, filas, prof):
    """Inserta el marcador de encabezado delante de cada título. Devuelve el markdown y las marcas."""
    marcas, piezas = [], []
    anterior = 0
    for fila, nivel in zip(filas, prof):
        linea_inicio = texto.rfind("\n", 0, fila["desde"]) + 1
        prefijo = texto[linea_inicio:fila["desde"]]
        viejo = re.match(r"#{1,6}\s+", prefijo)          # un marcador que ya estaba
        corte = linea_inicio + (viejo.end() if viejo else 0)
        piezas.append(texto[anterior:linea_inicio])      # hasta el principio de la línea…
        marca = "#" * nivel + " "
        marcas.append({"desde": sum(len(p) for p in piezas), "largo": len(marca)})
        piezas.append(marca)                             # …y el marcador canónico
        anterior = corte                                 # el viejo queda atrás: se descarta
    piezas.append(texto[anterior:])
    return "".join(piezas), marcas


def sin_marcas(markdown, marcas):
    """Quita las marcas insertadas: tiene que devolver el texto fuente, tal cual."""
    for marca in sorted(marcas, key=lambda m: -m["desde"]):
        markdown = markdown[:marca["desde"]] + markdown[marca["desde"] + marca["largo"]:]
    return markdown


def main():
    doc = sys.argv[1] if len(sys.argv) > 1 else "aviones"
    crudo = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else \
        AQUI / "out" / f"{doc}-luna-low-v2-n1.json"
    texto = (AQUI / f"{doc}.md").read_text(encoding="utf-8").strip()
    datos = json.loads(crudo.read_text(encoding="utf-8"))

    sys.path.insert(0, str(AQUI.parents[1] / "mvp" / "código"))
    from extraer_unidades import ubicar
    nodos = datos["indice"]
    titulos = [n["titulo"] for n in nodos]
    tramos, ausentes = ubicar(texto, titulos, [])
    filas = [{"n": i, "titulo": t, "desde": a, "hasta": b}
             for i, (t, (a, b)) in enumerate(zip(titulos, tramos), 1)]
    padres = [n["padre"] for n in nodos]
    prof = profundidades(padres)

    print(f"texto fuente: {len(texto)} caracteres · encabezados: {len(filas)} · ausentes: {ausentes or 'ninguno'}")
    print(f"profundidades: {prof}  ·  subárboles contiguos: {'sí' if not contiguos(padres) else contiguos(padres)}")

    markdown, marcas = armar_markdown(texto, filas, prof)
    print(f"\nmarkdown: {len(markdown)} caracteres ({len(markdown) - len(texto)} más: los marcadores)")
    print(f"¿quitar las marcas devuelve el fuente exacto? {sin_marcas(markdown, marcas) == texto}")
    print(f"¿el markdown es idempotente? {armar_markdown(markdown, [{'desde': f['desde'] + sum(m['largo'] for m in marcas[:i]), **f} for i, f in enumerate(filas)], prof)[0] == markdown}")
    print("\n--- el markdown (primeras 16 líneas) ---")
    print("\n".join(markdown.splitlines()[:16]))


if __name__ == "__main__":
    main()
