"""Ubica en el texto las oraciones que devuelve el modelo, y verifica la partición.

**El corte lo hace el modelo**: devuelve las oraciones **literales**. Acá se las **ubica** en el
texto del documento para quedarse con su tramo (`desde`, `hasta`), y se verifica el contrato:

- **literalidad**: la oración está en el texto tal cual, sin reformular ni completar;
- **cobertura del cuerpo**: no queda carácter no blanco del cuerpo fuera de un tramo. Los
  encabezados (`# …`) no cuentan: son estructura, no oraciones;
- **asignación exclusiva**: ninguna aparición se usa dos veces;
- **orden**: las oraciones de una unidad en orden textual, y las unidades por su primera oración.

**No hay números de oración.** El número no identifica nada: depende de la regla con la que se
cortó, y con otra regla dice otra cosa. La referencia es el tramo, y el tramo se cuenta sobre el
texto del documento, que está sellado.

Copia propia del MVP (sin dependencias fuera de la biblioteca estándar): `mvp/` no importa de
`unidades/`.
"""


def cuerpo(texto):
    """Lo que se reparte entre las unidades: el texto sin las líneas de encabezado."""
    return "\n".join(linea for linea in texto.splitlines() if not linea.startswith("#"))


def _mascara_del_cuerpo(texto):
    """Por carácter: 1 si es del cuerpo, 0 si es de un encabezado."""
    mascara = bytearray(b"\x01" * len(texto))
    punto = 0
    for linea in texto.splitlines(keepends=True):
        if linea.startswith("#"):
            mascara[punto:punto + len(linea)] = b"\x00" * len(linea)
        punto += len(linea)
    return mascara


def ubicar(texto, literales, usados):
    """La primera aparición **libre** de cada literal, en el orden dado.

    `usados` se comparte entre las unidades de la partición: así una misma aparición no puede ir a
    dos UT, y una oración repetida en el texto se ubica en otra aparición. Devuelve los tramos
    `(desde, hasta)` y los literales que no están en el texto.
    """
    tramos, ausentes = [], []
    for literal in literales:
        encontrado, desde = None, 0
        while True:
            posicion = texto.find(literal, desde)
            if posicion < 0:
                break
            if all(not (posicion < b and a < posicion + len(literal)) for a, b in usados):
                encontrado = posicion
                break
            desde = posicion + 1
        if encontrado is None:
            ausentes.append(literal)
        else:
            usados.append((encontrado, encontrado + len(literal)))
            tramos.append((encontrado, encontrado + len(literal)))
    return tramos, ausentes


def verificar_particion(texto, unidades):
    """El contrato medido contra el texto. Solo reporta: no corrige ni juzga el contenido."""
    usados, no_ubicadas, por_unidad = [], [], []
    for n, unidad in enumerate(unidades, 1):
        literales = [str(x) for x in (unidad.get("oraciones") or [])]
        tramos, ausentes = ubicar(texto, literales, usados)
        no_ubicadas += ausentes
        por_unidad.append({
            "n": n, "subtema": unidad.get("subtema"), "oraciones": len(literales),
            "tramos": tramos, "no_ubicadas": ausentes,
            "orden": all(b[0] > a[0] for a, b in zip(tramos, tramos[1:])),
            "primera": tramos[0][0] if tramos else None})

    del_cuerpo = _mascara_del_cuerpo(texto)
    cubierto = bytearray(len(texto))
    for desde, hasta in usados:
        cubierto[desde:hasta] = b"\x01" * (hasta - desde)
    huecos, i = [], 0
    while i < len(texto):
        if cubierto[i] or not del_cuerpo[i] or texto[i].isspace():
            i += 1
            continue
        j = i
        while j < len(texto) and not cubierto[j] and del_cuerpo[j] and not texto[j].isspace():
            j += 1
        huecos.append({"desde": i, "texto": texto[i:j][:100]})
        i = j
    no_blancos = sum(1 for k, c in enumerate(texto) if del_cuerpo[k] and not c.isspace())
    cubiertos = sum(1 for k, c in enumerate(texto)
                    if cubierto[k] and del_cuerpo[k] and not c.isspace())
    solapes = [(a, b) for (a, b), (c, d) in zip(sorted(usados), sorted(usados)[1:]) if b > c]
    primeras = [u["primera"] for u in por_unidad if u["primera"] is not None]
    return {
        "caracteres": len(texto), "caracteres_no_blancos": no_blancos,
        "cubiertos_no_blancos": cubiertos, "huecos": huecos,
        "unidades": len(unidades),
        "literales": sum(len(u.get("oraciones") or []) for u in unidades),
        "no_ubicadas": no_ubicadas, "solapes": solapes,
        "orden_en_unidades": all(u["orden"] for u in por_unidad),
        "orden_entre_unidades": all(b > a for a, b in zip(primeras, primeras[1:])),
        "por_unidad": por_unidad}


def roturas(informe):
    """Lo que hace inconsistente la partición con el texto.

    No es una lectura: es una partición rota. Que el Cámbrico vaya junto con la conquista de la
    tierra firme es una lectura —eso no es una rotura—; que una oración no esté en el texto, que
    quede un tramo del cuerpo sin cubrir o que se solapen, sí.
    """
    rotas = []
    if informe.get("no_ubicadas"):
        rotas.append(f"oraciones que no están en el texto: {informe['no_ubicadas']}")
    if informe.get("huecos"):
        rotas.append(f"tramos del cuerpo sin cubrir: {[h['texto'] for h in informe['huecos']]}")
    if informe.get("solapes"):
        rotas.append(f"tramos solapados: {informe['solapes']}")
    if not informe.get("orden_en_unidades"):
        rotas.append("oraciones fuera de orden dentro de una unidad")
    if not informe.get("orden_entre_unidades"):
        rotas.append("unidades fuera de orden")
    return rotas
