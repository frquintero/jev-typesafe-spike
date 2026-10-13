#!/usr/bin/env python3
"""Carga una pregunta para la consulta: **de un archivo o del chat**.

**Cargar no es radicar.** La pregunta se radica **cuando el ciclo la entrega**: el acto de la
consulta la recibe, corre, y **al cerrar con el JSON de `RESPUESTA_JSON`** escribe la fila de
`preguntas` —su texto, su dominio, su fuente y la fecha y la hora del cierre— junto con su corrida
y su respuesta. Si el ciclo no entrega, no hay pregunta radicada: queda la cédula del acto.

    python3 mvp/código/cargar_pregunta.py <archivo> [--numero N]   # una del archivo (1-based)
    python3 mvp/código/cargar_pregunta.py --texto "…"              # tecleada

Este guion solo **muestra** lo que se cargaría: no toca la base. El acto lo usa como módulo
(`cargar`), y el dominio —la unidad semántica donde vive la pregunta— lo pone el acto.
"""

import pathlib
import re
import sys

NUMERO = re.compile(r"^\d+[.)]\s*(.+)$")


def entero(valor, opcion):
    """El número pedido, o se detiene: un `--numero` que no es número no se adivina."""
    try:
        return int(valor)
    except ValueError:
        raise SystemExit(f"`{opcion} {valor}` no es un número")


def preguntas_de(ruta):
    """Las preguntas de un archivo: una por línea, con número o sin él."""
    preguntas = []
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea:
            continue
        coincidencia = NUMERO.match(linea)
        preguntas.append(coincidencia.group(1).strip() if coincidencia else linea)
    return preguntas


def cargar(archivo=None, texto=None, numero=None):
    """La pregunta a consultar: `(texto, fuente)`.

    `fuente` es `'tecleada'` o la ruta del archivo del que se leyó. De un archivo se carga **una**
    pregunta: si trae varias, hay que decir cuál con `numero` (1-based).
    """
    if (archivo is None) == (texto is None):
        raise SystemExit("hay que pasar un archivo **o** `--texto`, no los dos ni ninguno")
    if texto is not None:
        if not texto.strip():
            raise SystemExit("la pregunta está vacía: una pregunta sin texto no se carga")
        return texto.strip(), "tecleada"
    ruta = pathlib.Path(archivo)
    if not ruta.is_file():
        raise SystemExit(f"no está el archivo '{archivo}'")
    preguntas = preguntas_de(ruta)
    if not preguntas:
        raise SystemExit(f"'{archivo}' no trae ninguna pregunta")
    if numero is None:
        if len(preguntas) > 1:
            raise SystemExit(f"'{archivo}' trae {len(preguntas)} preguntas: decí cuál con "
                             f"`--numero N` (1 a {len(preguntas)})")
        numero = 1
    if not 1 <= numero <= len(preguntas):
        raise SystemExit(f"`--numero {numero}` está fuera del archivo (trae {len(preguntas)})")
    return preguntas[numero - 1], str(ruta.resolve())


def main(argumentos):
    if not argumentos:
        raise SystemExit('uso: python3 mvp/código/cargar_pregunta.py <archivo> [--numero N] · '
                         'python3 mvp/código/cargar_pregunta.py --texto "…"')
    archivo, texto, numero = None, None, None
    resto = list(argumentos)
    while resto:
        opcion = resto.pop(0)
        if opcion == "--texto" and resto:
            texto = resto.pop(0)
        elif opcion == "--numero" and resto:
            numero = entero(resto.pop(0), "--numero")
        elif archivo is None and not opcion.startswith("--"):
            archivo = opcion
        else:
            raise SystemExit(f"no entiendo '{opcion}'. Uso: cargar_pregunta.py <archivo> "
                             f"[--numero N] · cargar_pregunta.py --texto \"…\"")

    contenido, fuente = cargar(archivo=archivo, texto=texto, numero=numero)
    print(f"  cargada ({fuente}):")
    print(f"    {contenido}")
    print("    -> la pregunta se radica cuando el ciclo la entregue "
          "(python3 mvp/código/orq/orquestador.py … --dominio E)")


if __name__ == "__main__":
    main(sys.argv[1:])
