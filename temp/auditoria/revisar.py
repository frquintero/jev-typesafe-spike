#!/usr/bin/env python3
"""Revisión de coherencia del MVP, para la auditoría.

Comprueba, sin escribir nada:

1. **Las bases**: tablas y filas (deben estar limpias).
2. **El diseño contra la base**: los `CREATE TABLE` de `mvp/diseño-mvp.md`
   contra el esquema real —tablas y columnas.
3. **Los prompts contra los actos**: qué huecos tiene cada prompt y quién los llena.
4. **Los relojes**: cada prompt, con qué reloj y en qué mensaje.
5. **Rastros de lo jubilado** dentro del MVP (fuera del MVP hay otras líneas, y no se tocan).

    python3 temp/auditoria/revisar.py
"""

import pathlib
import re
import sqlite3
import sys

RAIZ = pathlib.Path(__file__).resolve().parents[2]
MVP = RAIZ / "mvp"
RESTRICCIONES = ("CHECK", "UNIQUE", "PRIMARY", "FOREIGN", "CONSTRAINT", "OR", "AND")


def columnas_del_diseno(texto, tabla):
    """Las columnas que el diseño declara para una tabla.

    Una línea puede traer varias columnas; y las líneas de restricción (`CHECK`, `UNIQUE`, el `OR`
    de un CHECK partido en dos) no son columnas.
    """
    bloque = re.search(rf"CREATE TABLE (?:IF NOT EXISTS )?{tabla} \((.*?)\n\);", texto, re.S)
    if not bloque:
        return None
    columnas = []
    for linea in bloque.group(1).splitlines():
        limpia = linea.split("--")[0].strip().rstrip(",")
        if not limpia:
            continue
        for parte in re.split(r",(?![^(]*\))", limpia):
            palabra = parte.strip().split(" ")[0] if parte.strip() else ""
            if palabra and palabra.upper() not in RESTRICCIONES:
                columnas.append(palabra)
    return columnas


def esquema_real(ruta):
    db = sqlite3.connect(ruta)
    tablas = {}
    for (nombre,) in db.execute("SELECT name FROM sqlite_master WHERE type='table' "
                                "AND name NOT LIKE 'sqlite_%' ORDER BY name"):
        tablas[nombre] = [fila[1] for fila in db.execute(f"PRAGMA table_info({nombre})")]
    db.close()
    return tablas


def main():
    print("=" * 92)
    print("1. LAS BASES")
    for nombre in ("corpus", "almacen"):
        ruta = MVP / "código" / f"{nombre}.db"
        tablas = esquema_real(ruta)
        db = sqlite3.connect(ruta)
        filas = sum(db.execute(f"SELECT count(*) FROM {t}").fetchone()[0] for t in tablas)
        db.close()
        estado = "LIMPIA" if filas == 0 else f"CON {filas} FILAS"
        print(f"   {nombre}.db: {len(tablas)} tablas · {estado} · {', '.join(tablas)}")

    print("=" * 92)
    print("2. EL DISEÑO CONTRA LA BASE")
    texto = (MVP / "diseño-mvp.md").read_text(encoding="utf-8")
    reales = {base: esquema_real(MVP / "código" / f"{base}.db") for base in ("corpus", "almacen")}
    # el diseño trae las dos bases en un solo archivo: el corpus primero, el almacén al final
    corte = texto.rindex("**El almacén**")
    textos = {"corpus": texto[:corte], "almacen": texto[corte:]}
    for base, real in reales.items():
        print(f"   --- diseño-mvp.md vs {base}.db")
        for tabla, columnas in real.items():
            declaradas = columnas_del_diseno(textos[base], tabla)
            if declaradas is None:
                print(f"      {tabla}: está en la base y NO en el diseño")
                continue
            faltan = [c for c in columnas if c not in declaradas]
            sobran = [c for c in declaradas if c not in columnas]
            aviso = "ok" if not faltan and not sobran else f"faltan {faltan} · sobran {sobran}"
            print(f"      {tabla}: {len(columnas)} columnas · {aviso}")
    en_las_bases = set().union(*(set(real) for real in reales.values()))
    for tabla in set(re.findall(r"CREATE TABLE (?:IF NOT EXISTS )?(\w+)", texto)) - en_las_bases:
        print(f"      {tabla}: está en el diseño y NO en la base")

    print("=" * 92)
    print("3. LOS PROMPTS: HUECOS Y QUIÉN LOS LLENA")
    actos = {
        "prompt_volcado.md": "mvp/código/volcar.py (todavía no existe)",
        "prompt_UT.md": "mvp/código/paso1_unidades.py",
        "prompt_DATOS.md": "mvp/código/paso2_datos.py",
        "prompt_ORQ.md": "mvp/código/orq/armar_prompt.py",
    }
    for prompt, acto in actos.items():
        texto = (MVP / "prompts" / prompt).read_text(encoding="utf-8")
        huecos = sorted(set(re.findall(r"\{\{(\w+)\}\}", texto)))
        sistema = texto.split("[TAREA]")[0] if "[TAREA]" in texto else texto
        print(f"   {prompt:<22} huecos: {', '.join(huecos) or 'ninguno'}")
        print(f"   {'':<22} radicado en el system: {'{{RELOJ_RADICADO}}' in sistema} · "
              f"sistema en el user: {{RELOJ_SISTEMA}} en el user: "
              f"{'{{RELOJ_SISTEMA}}' in texto.split('[TAREA]')[1] if '[TAREA]' in texto else False}")
        print(f"   {'':<22} lo llena: {acto}")

    print("=" * 92)
    print("4. RASTROS DE LO JUBILADO, DENTRO DEL MVP")
    patrones = ("numerar_oraciones", "verificar_subtemas", "TEXTO_NUMERADO", "{{RELOJES}}",
                "{{ANCLAS}}", "version_volcado", "seis tablas", "siete tablas")
    encontrados = 0
    for ruta in sorted((MVP).rglob("*")):
        if not ruta.is_file() or ruta.suffix not in (".py", ".md", ".json"):
            continue
        if "temp/" in str(ruta) or "/temp" in str(ruta):
            continue
        texto = ruta.read_text(encoding="utf-8", errors="ignore")
        for patron in patrones:
            if patron in texto:
                encontrados += 1
                print(f"   {ruta.relative_to(RAIZ)}: {patron}")
    if not encontrados:
        print("   ninguno")
    return 0


if __name__ == "__main__":
    sys.exit(main())
