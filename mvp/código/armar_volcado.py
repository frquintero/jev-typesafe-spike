"""Del texto y el índice al **markdown**: ubicar los títulos, derivar la profundidad, marcar.

El modelo decide **qué líneas son encabezado y de qué cuelgan**; el código hace el resto: ubica
cada título en el texto, deriva la profundidad del bosque, **inserta el marcador canónico**
(`#`, `##`, …) al principio de esa línea y verifica que no inventó nada.

El markdown es **la fuente + las marcas**: nada del texto se reescribe. Un marcador que la fuente ya
traía —o que el modelo devolvió dentro del título— **se descarta** y se pone el canónico; por eso
volver a volcar un markdown ya marcado no lo cambia. La **ida y vuelta** se comprueba contra la
fuente **normalizada** (sin esos marcadores previos): quitar las marcas tiene que devolver el texto
tal cual, y lo único que el acto cambia son marcas.

Viene del prototipo probado en el scratch (`temp/estructura/probar_volcado.py`), sobre las cinco
formas de fuente: sin marcas, numerada, mixta, y con anexos pegados y separados.
"""

import re

from extraer_unidades import ubicar

MARCA = re.compile(r"#{1,6}\s+")


def profundidades(padres):
    """La profundidad de cada nodo en el bosque: 1 para las raíces."""
    profundidad = []
    for i, padre in enumerate(padres):
        profundidad.append(1 if not padre else profundidad[padre - 1] + 1)
    return profundidad


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
            for hijo in hijos[actual]:
                if hijo not in vistos:
                    vistos.add(hijo)
                    pila.append(hijo)
        dentro[i] = vistos
    return dentro


def contiguos(padres):
    """Los nodos cuyo subárbol no es un tramo contiguo del orden: markdown no sabe de cruces."""
    malos = []
    for i, dentro in subarboles(padres).items():
        if dentro and sorted(dentro) != list(range(min(dentro), max(dentro) + 1)):
            malos.append(i + 1)
    return malos


def sin_marcas(markdown, marcas):
    """Quita las marcas insertadas: tiene que devolver la fuente normalizada, tal cual."""
    for marca in sorted(marcas, key=lambda m: -m["desde"]):
        markdown = markdown[:marca["desde"]] + markdown[marca["desde"] + marca["largo"]:]
    return markdown


def armar_markdown(texto, filas, profundidad):
    """Inserta el marcador canónico delante de cada título.

    Devuelve `(markdown, marcas, normalizado, descartadas)`: la fuente **normalizada** es el texto
    con los marcadores previos quitados —lo que el markdown tiene que devolver—, y `descartadas`
    cuenta cuántos se descartaron (los que la fuente traía, o los que el modelo metió en el título).
    """
    marcas, piezas, normal = [], [], []
    anterior, descartadas = 0, 0
    for fila, nivel in zip(filas, profundidad):
        inicio = texto.rfind("\n", 0, fila["desde"]) + 1
        viejo = MARCA.match(texto, inicio, fila["desde"])             # un marcador en la línea…
        if not viejo:
            viejo = MARCA.match(texto, fila["desde"], fila["hasta"])  # …o dentro del título
        descartadas += 1 if viejo else 0
        corte = viejo.end() if viejo else None
        piezas.append(texto[anterior:inicio])                        # hasta el principio de la línea
        normal.append(texto[anterior:inicio])
        marca = "#" * nivel + " "
        marcas.append({"desde": sum(len(pieza) for pieza in piezas), "largo": len(marca)})
        piezas.append(marca)                                         # el marcador canónico
        anterior = corte if corte is not None else inicio
    piezas.append(texto[anterior:])
    normal.append(texto[anterior:])
    return "".join(piezas), marcas, "".join(normal), descartadas


def verificar(texto, parsed):
    """El índice contra el texto. Devuelve (filas, problemas): solo reporta, no corrige.

    - la **forma** del índice: una lista, `n` correlativos desde 1, `titulo` texto y `padre` 0 o
      un número anterior;
    - cada título, **literal**, **en orden** y sin repetir aparición;
    - y los **subárboles contiguos**: si no, el markdown no puede representar la jerarquía.
    """
    if not isinstance(parsed, dict) or not isinstance(parsed.get("indice"), list):
        return [], ["el JSON no trae una lista 'indice'"]
    nodos = parsed["indice"]
    problemas = [f"clave de más en la raíz: «{clave}»" for clave in parsed if clave != "indice"]
    titulos, padres = [], []
    for posicion, nodo in enumerate(nodos, 1):
        if not isinstance(nodo, dict):
            problemas.append(f"el nodo {posicion} no es un objeto")
            continue
        problemas += [f"n={nodo.get('n')}: clave de más «{clave}»"
                      for clave in nodo if clave not in ("n", "titulo", "padre")]
        if nodo.get("n") != posicion:
            problemas.append(f"el nodo {posicion} trae n={nodo.get('n')!r}; se esperaba {posicion}")
            continue
        if not isinstance(nodo.get("titulo"), str) or not nodo["titulo"].strip():
            problemas.append(f"n={posicion} sin 'titulo'")
            continue
        padre = nodo.get("padre")
        if not isinstance(padre, int) or isinstance(padre, bool) or not 0 <= padre < posicion:
            problemas.append(f"n={posicion}: 'padre' tiene que ser 0 o un n anterior, no {padre!r}")
            continue
        titulos.append(nodo["titulo"])
        padres.append(padre)
    if problemas:
        return [], problemas
    tramos, ausentes = ubicar(texto, titulos, [])
    if ausentes:
        return [], [f"títulos que no están en el texto: {ausentes}"]
    if not all(b[0] > a[0] for a, b in zip(tramos, tramos[1:])):
        return [], ["los títulos no están en orden en el texto"]
    cruzados = contiguos(padres)
    if cruzados:
        return [], [f"subárboles no contiguos en los títulos {cruzados}"]
    filas = [{"n": i, "titulo": titulo, "padre": padre, "desde": desde, "hasta": hasta}
             for i, (titulo, padre, (desde, hasta))
             in enumerate(zip(titulos, padres, tramos), 1)]
    return filas, []


def armar(texto, parsed):
    """El markdown y sus marcas, o los problemas.

    Devuelve `{'markdown', 'marcas', 'filas', 'descartadas', 'problemas'}`. Un **índice vacío es
    válido**: un documento sin encabezados sale igual a la fuente.
    """
    filas, problemas = verificar(texto, parsed)
    if problemas:
        return {"markdown": None, "marcas": [], "filas": filas, "descartadas": 0,
                "problemas": problemas}
    profundidad = profundidades([fila["padre"] for fila in filas])
    markdown, marcas, normalizado, descartadas = armar_markdown(texto, filas, profundidad)
    if sin_marcas(markdown, marcas) != normalizado:
        return {"markdown": None, "marcas": marcas, "filas": filas, "descartadas": descartadas,
                "problemas": ["quitar las marcas no devuelve la fuente: el armado está roto"]}
    return {"markdown": markdown, "marcas": marcas, "filas": filas, "descartadas": descartadas,
            "problemas": []}
