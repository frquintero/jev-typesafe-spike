"""Parte un prompt de trabajo en **los dos mensajes**: el `system` y el `user`.

Un prompt de trabajo trae **dos marcas**: `[SISTEMA]` para lo invariante, y para el material de la
llamada `[TAREA]` **o** `[USUARIO]` (las dos valen). Las marcas **no llegan al modelo**: `partir` las
consume y devuelve el `system` y el `user` ya armados.

**La regla completa** —qué va en cada uno y por qué, los relojes y sus huecos— está en
`mvp/diseño-mvp.md` §4; las medidas de caché que la sostienen, en la memoria. Acá vive solo lo que la
implementa.
"""

MARCA_SISTEMA = "[SISTEMA]"
MARCA_TAREA = "[TAREA]"
MARCA_USUARIO = "[USUARIO]"  # el material de la llamada también puede venir marcado así


def partir(plantilla, ruta=None, **rellenos):
    """Devuelve los dos mensajes: `[{"role": "system", …}, {"role": "user", …}]`."""
    marcas_del_material = [marca for marca in (MARCA_TAREA, MARCA_USUARIO) if marca in plantilla]
    if MARCA_SISTEMA not in plantilla or not marcas_del_material:
        raise SystemExit(f"el prompt '{ruta or '(sin nombre)'}' tiene que traer la marca "
                         f"{MARCA_SISTEMA} y la del material ({MARCA_TAREA} o {MARCA_USUARIO})")
    parte_sistema, parte_tarea = plantilla.split(marcas_del_material[0], 1)
    parte_sistema = parte_sistema.replace(MARCA_SISTEMA, "", 1)

    def rellenar(texto):
        for hueco, valor in rellenos.items():
            texto = texto.replace("{{" + hueco + "}}", valor)
        return texto.strip()

    return [{"role": "system", "content": rellenar(parte_sistema)},
            {"role": "user", "content": rellenar(parte_tarea)}]
