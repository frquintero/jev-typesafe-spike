#!/usr/bin/env python3
"""Anota en la memoria el prompt radicado, la alineación del acto y lo que queda. Idempotente."""
import pathlib

RUTA = pathlib.Path("mvp/memoria de trabajo y pendientes.md")
t = RUTA.read_text(encoding="utf-8")

NOTA = """**`prompt_DATOS` radicado y el acto alineado (10-10).** El prompt con el que corrió todo el banco
de DATOS vivía sin versionar en `temp/prompt_DATOS_v1.md`: quita el párrafo de reglas explícitas y lo
reemplaza por un ejemplo de dos casos relacionados —el faro de la isla y el rescate de los
pescadores— con el formato `caso:` / `satélites:` y cada oración numerada desde [1] en cada caso. Ya
es `mvp/prompts/prompt_DATOS.md` (hash `5b456379…`). **De las 43 corridas de DATOS sobre
`preparacion_cafe`, 38 comparten ese hash** —DeepSeek, GLM en tres niveles, Haiku `high` y `max`,
Sonnet, GPT 6 Luna y MiMo—: ese es el banco comparable. Las otras cinco son de cuando se armaba `v1`
y **ya son irrecuperables**: sus hashes (`1e986db3`, `2d3c8584`, `7fdc4bc3`) apuntan a textos que el
archivo actual sobrescribió y que nunca se versionaron; la sexta, `haiku-high-s1` sin `-v1-`, corrió
con el `prompt_DATOS` viejo. El sufijo `s1`…`s4` de los nombres no era de réplica: era **de versión
del prompt**, y `s4` es la que se estabilizó.

Con el prompt radicado se vio que **el acto mandaba el material con otra forma que el banco**:
`paso2_datos.py` lo enviaba como JSON con `caso` y `contenido` —las oraciones unidas en un párrafo
corrido—, mientras el ejemplo del prompt enseña bloques con satélites numerados. El hueco
`{{UNIDADES}}` es el mismo, así que el acto no habría fallado: habría corrido en silencio con una
entrada que ninguna corrida midió. **Ya está alineado**, y se verificó carácter por carácter contra
el `unidades_enviadas` de un crudo: idénticos. Y los corredores de prueba guardan ahora
`prompt_texto` además del hash, porque **el hash identifica pero no reconstruye** —fue justo lo que
dejó irrecuperables a esas cinco corridas—.

**Lo que queda de eso:** la tabla `corridas` de la base guarda `prompt` y `hash_prompt`, **no el
texto**, así que una corrida de producción tiene la misma fragilidad que tenían los crudos. La base
está vacía hoy, así que es cambiar el esquema, no migrar (como el pendiente 15). Sin decidir.

"""

ANCLA = "## 3. Pendientes vigentes"
if "prompt_DATOS` radicado y el acto alineado" not in t:
    assert ANCLA in t, "no encontré el ancla de pendientes"
    t = t.replace(ANCLA, NOTA + ANCLA, 1)

RUTA.write_text(t, encoding="utf-8")
print("listo")
