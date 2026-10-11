"""Parte un prompt de trabajo en **los dos mensajes**: el `system` y el `user`.

**La regla** —la misma para todos los prompts del MVP—:

1. Un prompt de trabajo trae **dos marcas**: `[SISTEMA]` para lo invariante, y para el material de
   la llamada `[TAREA]` **o** `[USUARIO]` (las dos valen). Las marcas **no llegan al modelo**:
   `partir` las consume.
2. El `system` lleva la tarea, las reglas, el formato de salida **y los ejemplos** —todo lo que no
   cambia de una llamada a otra—. El `user` lleva **el material de esta llamada** —el documento, las
   unidades, los casos, la pregunta— **y el pedido**.
3. El `system` es el **prefijo invariante**: es lo que aprovecha el caché (en la familia `responses`
   va como `instructions`). Por eso lo que cambia por llamada **no** va ahí.
4. **Todo prompt lleva los dos relojes**, y cada uno en su lugar (`mvp/código/relojes.py`, formato
   `[día-mes-año: hora]`): **el del radicado** —`{{RELOJ_RADICADO}}`, invariante por documento— va en
   el `[SISTEMA]`; **el del sistema** —`{{RELOJ_SISTEMA}}`, que cambia en cada corrida— va en el
   `[TAREA]`, **después del material**. El acto los llena con lo que aplica: un documento (UT y
   DATOS) o los documentos del dominio (la consulta).
5. Los huecos de cada prompt (`{{RELOJ_RADICADO}}`, `{{RELOJ_SISTEMA}}`, `{{TEXTO}}`,
   `{{UNIDADES}}`, `{{CASOS}}`, `{{PREGUNTA}}`) se rellenan con `str.replace` —**nunca**
   `str.format`: el texto puede traer llaves—.
6. El material va **delimitado** (por ejemplo `<texto> … </texto>`), y el pedido va al final del
   `user`.

El porqué del reparto y las medidas de caché que lo sostienen: `mvp/proveedores.md`, la sección de
la regla de los dos mensajes.
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
