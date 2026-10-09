#!/usr/bin/env python3
"""Parte un prompt de trabajo en **los dos mensajes**: el `system` y el `user`.

Un prompt de trabajo trae dos marcas:

    [SISTEMA]   lo invariante: la tarea, las reglas, los casos, el formato de salida
    [TAREA]     el material de esta llamada: el texto numerado, las unidades, los casos del dominio

El `system` lleva el prompt —va con su hash en la fila de la corrida— y el `user` lleva el material
—que es lo que cambia de un documento a otro, y lo que va con el sello del documento radicado—.
Así el modelo lee la regla como instrucción y el texto como dato, y el prefijo invariante queda
estable entre llamadas.

Los huecos (`{{TEXTO_NUMERADO}}`, `{{UNIDADES}}`, `{{CASOS}}`, `{{PREGUNTA}}`, `{{ANCLAS}}`) se
rellenan con `str.replace` —nunca `str.format`: el texto puede traer llaves—.
"""

MARCA_SISTEMA = "[SISTEMA]"
MARCA_TAREA = "[TAREA]"


def partir(plantilla, ruta=None, **rellenos):
    """Devuelve los dos mensajes: `[{"role": "system", …}, {"role": "user", …}]`."""
    if MARCA_SISTEMA not in plantilla or MARCA_TAREA not in plantilla:
        raise SystemExit(f"el prompt '{ruta or '(sin nombre)'}' tiene que traer las marcas "
                         f"{MARCA_SISTEMA} y {MARCA_TAREA}")
    parte_sistema, parte_tarea = plantilla.split(MARCA_TAREA, 1)
    parte_sistema = parte_sistema.replace(MARCA_SISTEMA, "", 1)

    def rellenar(texto):
        for hueco, valor in rellenos.items():
            texto = texto.replace("{{" + hueco + "}}", valor)
        return texto.strip()

    return [{"role": "system", "content": rellenar(parte_sistema)},
            {"role": "user", "content": rellenar(parte_tarea)}]
