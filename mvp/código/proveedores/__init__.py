"""La puerta del MVP a los modelos: **un alias → un proveedor**, y una sola forma de respuesta.

El contrato interno es **la forma de OpenAI** —`choices[0].message` con `content`,
`reasoning_content` y `tool_calls`, más `finish_reason` y `usage`—, que es la que ya consumen el
bucle del ORQ y los corredores. Cada proveedor traduce a/desde su API; el resto del MVP no sabe
con quién está hablando.

Sin streaming: un POST y la respuesta entera. Los **segundos** de cada llamada quedan en
`respuesta["_segundos"]`, y el cuerpo enviado —que es donde se ve el esfuerzo pedido— se devuelve
para el crudo.

El **esfuerzo** tiene un valor por defecto (`low`) y se puede cambiar por alias o por llamada; el
proveedor lo traduce a su nombre (`reasoning_effort` o `output_config.effort`).

Uso:

    from proveedores import llamar
    cuerpo, respuesta = llamar("deepseek", prompt=texto)
    cuerpo, respuesta = llamar("haiku", mensajes=mensajes, herramientas=tools, esfuerzo="max")
"""

from . import anthropic, openai_compatible
from .claves import ErrorDeLlamada  # se exporta: los corredores atrapan el fallo y lo registran

ESFUERZO_POR_DEFECTO = "low"

# Un alias por modelo que usamos. `proveedor` elige el módulo; `id` es el modelo en su API;
# `esfuerzo` se puede pisar en la llamada; `extra` es lo propio del host que va tal cual al cuerpo.
ALIAS = {
    "deepseek": {
        "proveedor": "openai_compatible",
        "id": "deepseek-flash",
        "url": "https://api.deepseek.com/chat/completions",
        "esfuerzo": "low",
        "extra": {"thinking": {"type": "enabled"}},
    },
    # GLM-5.3-Flash (z.ai). La documentación de z.ai dice que el razonamiento no se puede apagar
    # (`thinking.type` solo admite `enabled`, que es el valor por defecto), que «GLM-5.3 y
    # GLM-5.3-FLASH siempre piensan cuando está habilitado» y que `reasoning_effort` admite
    # `low` / `high` / `max` (por defecto y recomendado: `max`).
    # Lo observado NO coincide con eso:
    # - 09-10-2026: sobre doc10 (prompt DATOS v7), `low` razonó 516 y 877 tokens; `high`, 4.921 y
    #   6.401.
    # - 10-10-2026: `low` devolvió `reasoning_tokens: 0` y sin `reasoning_content` en todas las
    #   pruebas —el café con DATOS v1 (system + user, un solo mensaje, y con `thinking: enabled`
    #   explícito), doc10 repetido con v7, y «qué es una variable en python», también por `curl`
    #   directo con `max_tokens` 256 y 8.000—; `high` dio 0 en la pregunta y 5 tokens en el café
    #   («Extract data per UT.»); solo `max` razonó (298 a 472 tokens en la pregunta, 3.088 en el
    #   café). La API aceptó los tres niveles (HTTP 200).
    # El transporte no es la causa: el `curl` directo da lo mismo. Si se quiere razonamiento de
    # GLM, hay que pedir `max` explícito; con el `low` de este alias, hoy no razona.
    "glm": {
        "proveedor": "openai_compatible",
        "id": "glm-5.3-flash",
        "url": "https://api.z.ai/api/paas/v4/chat/completions",
        "esfuerzo": "low",
    },
    "haiku": {
        "proveedor": "anthropic",
        "id": "claude-haiku-5-5",
        "url": "https://api.anthropic.com/v1/messages",
        "esfuerzo": "low",
        # El techo tiene que cubrir el pensamiento *y* la respuesta: con 16384, un `high` sobre un
        # documento de cuatro párrafos se lo comió pensando y volvió vacío (`finish_reason: length`).
        "max_tokens": 64000,
    },
    # Sin créditos en xAI: se declara para cuando se recargue (ver la memoria).
    "grok": {
        "proveedor": "openai_compatible",
        "id": "grok-4.7",
        "url": "https://api.x.ai/v1/chat/completions",
        "esfuerzo": "low",
    },
}

_PROVEEDORES = {"openai_compatible": openai_compatible, "anthropic": anthropic}


def resolver(alias, esfuerzo=None):
    """El alias resuelto, con el esfuerzo pedido encima del de defecto. No toca el registro."""
    if alias not in ALIAS:
        raise SystemExit(f"'{alias}' no está en el registro de proveedores: {sorted(ALIAS)}")
    config = dict(ALIAS[alias])
    config["esfuerzo"] = esfuerzo or config.get("esfuerzo") or ESFUERZO_POR_DEFECTO
    return config


def llamar(alias, prompt=None, mensajes=None, herramientas=None, conv_id=None, esfuerzo=None):
    """Llama al modelo del alias. Devuelve (cuerpo enviado, respuesta en la forma de siempre)."""
    config = resolver(alias, esfuerzo)
    if mensajes is None:
        if prompt is None:
            raise SystemExit("hay que pasar `prompt` o `mensajes`")
        mensajes = [{"role": "user", "content": prompt}]
    return _PROVEEDORES[config["proveedor"]].llamar(config, mensajes, herramientas, conv_id)
