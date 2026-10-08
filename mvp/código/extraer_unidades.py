"""Los ayudantes del paso 1 que usa el MVP: numerar oraciones y verificar la partición.

Copia **propia del MVP** (sin dependencias fuera de la biblioteca estándar) de la parte de
`unidades/extraer_unidades.py` que el MVP usa: `mvp/` no importa de la línea `unidades/`. El
original, que además trae el runner de aquella línea y su llamada al modelo, sigue ahí para lo
suyo; acá el `re` es lo único que se importa.

Lo que hace:

- `numerar_oraciones`: numera las oraciones conservando los párrafos. El título (`# …`) queda
  fuera. Devuelve el texto numerado y los registros `{"n", "oracion"}`.
- `verificar_subtemas`: **solo reporta** huecos, solapes, números fuera de rango y no enteros.
  No corrige ni juzga el contenido.
- `reconstruir_subtemas`: repone las oraciones literales de cada subtema a partir de sus números.
"""

import re


def oraciones(texto):
    """Definición del prompt: de un . ? ! al siguiente; el título (# ...) queda fuera."""
    cuerpo = "\n".join(l for l in texto.splitlines() if not l.startswith("#"))
    return [p.strip() for p in re.findall(r"[^.?!]+[.?!]?", cuerpo) if p.strip()]


def numerar_oraciones(texto):
    """Devuelve el texto numerado conservando párrafos y los registros de cada oración."""
    parrafos = []
    lineas_parrafo = []
    for linea in texto.splitlines():
        if linea.startswith("#"):
            continue
        if not linea.strip():
            if lineas_parrafo:
                parrafos.append("\n".join(lineas_parrafo))
                lineas_parrafo = []
        else:
            lineas_parrafo.append(linea)
    if lineas_parrafo:
        parrafos.append("\n".join(lineas_parrafo))

    registros = []
    parrafos_numerados = []
    for parrafo in parrafos:
        oraciones_parrafo = []
        for oracion in oraciones(parrafo):
            numero = len(registros) + 1
            registros.append({"n": numero, "oracion": oracion})
            oraciones_parrafo.append(f"[{numero}] {oracion}")
        if oraciones_parrafo:
            parrafos_numerados.append(" ".join(oraciones_parrafo))
    return "\n\n".join(parrafos_numerados), registros


def es_entero(valor):
    return isinstance(valor, int) and not isinstance(valor, bool)


def reconstruir_subtemas(parsed, oraciones_numeradas):
    por_numero = {item["n"]: item["oracion"] for item in oraciones_numeradas}
    reconstruidas = []
    for subtema in parsed.get("subtemas", []):
        numeros = list(subtema.get("oraciones", []))
        reconstruidas.append(
            {
                "subtema": subtema.get("subtema"),
                "oraciones_n": numeros,
                "oraciones": [
                    por_numero[n]
                    for n in numeros
                    if es_entero(n) and n in por_numero
                ],
            }
        )
    return reconstruidas


def verificar_subtemas(parsed, oraciones_numeradas):
    total = len(oraciones_numeradas)
    asignaciones = [0] * (total + 1)
    fuera_de_rango = []
    no_enteros = []
    for subtema in parsed.get("subtemas", []):
        for numero in subtema.get("oraciones", []):
            if not es_entero(numero):
                if not any(numero == visto for visto in no_enteros):
                    no_enteros.append(numero)
            elif numero < 1 or numero > total:
                if numero not in fuera_de_rango:
                    fuera_de_rango.append(numero)
            else:
                asignaciones[numero] += 1
    return {
        "oraciones_del_texto": total,
        "huecos": [n for n in range(1, total + 1) if asignaciones[n] == 0],
        "solapes": [n for n in range(1, total + 1) if asignaciones[n] > 1],
        "fuera_de_rango": sorted(fuera_de_rango),
        "no_enteros": no_enteros,
    }
