#!/usr/bin/env python3
"""Las tres cosas: alinear el formato del acto, y que los crudos guarden el texto del prompt.

Idempotente: si ya está hecho, no hace nada.
"""
import pathlib

# ---------------------------------------------------------------- 1) el acto real
ACTO = pathlib.Path("mvp/código/paso2_datos.py")
t = ACTO.read_text(encoding="utf-8")

VIEJO = '''    lista = [{"caso": unidad["subtema"], "contenido": " ".join(oraciones)}
             for unidad, oraciones in armadas]
    mensajes = partir(plantilla, ruta_prompt.name, UNIDADES=json.dumps(lista, ensure_ascii=False))'''

NUEVO = '''    # El material va con la forma que el ejemplo del prompt enseña: un bloque por unidad, con su
    # `caso` y sus `satélites` numerados desde [1] en cada bloque. Oraciones separadas, no un
    # párrafo corrido: el corte entre oraciones es la pista de dónde hay predicados distintos, y es
    # la forma con la que se midió el banco de `temp/datos-test/`.
    lista = [{"caso": unidad["subtema"], "satelites": oraciones}
             for unidad, oraciones in armadas]
    bloques = ["caso: " + unidad["caso"] + "\\nsatélites:\\n"
               + "\\n".join(f"[{k}] {oracion}" for k, oracion in enumerate(unidad["satelites"], 1))
               for unidad in lista]
    mensajes = partir(plantilla, ruta_prompt.name, UNIDADES="\\n\\n".join(bloques))'''

if "satélites:" not in t:
    assert VIEJO in t, "no encontré el armado de la lista en paso2_datos.py"
    t = t.replace(VIEJO, NUEVO, 1)
    ACTO.write_text(t, encoding="utf-8")
    print("1) paso2_datos.py: alineado al formato caso/satélites")
else:
    print("1) paso2_datos.py: ya estaba alineado")

# ---------------------------------------------------- 3) el texto del prompt en los crudos
for nombre in ("paso2_seco_v1.py", "paso2_seco_v1_luna.py"):
    ruta = pathlib.Path("temp/datos-test") / nombre
    c = ruta.read_text(encoding="utf-8")
    if '"prompt_texto"' in c:
        print(f"3) {nombre}: ya guardaba el texto")
        continue
    viejo = '"hash_prompt": hash_texto(plantilla),'
    nuevo = ('"hash_prompt": hash_texto(plantilla),\n    '
             '# El hash identifica pero no reconstruye: el texto va en el crudo para que la\n    '
             '# corrida se interprete sin depender de que el archivo siga existiendo.\n    '
             '"prompt_texto": plantilla,')
    assert viejo in c, f"no encontré hash_prompt en {nombre}"
    ruta.write_text(c.replace(viejo, nuevo, 1), encoding="utf-8")
    print(f"3) {nombre}: guarda prompt_texto")
