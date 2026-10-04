# reporte_ds.md — prueba de mesa 1b, tablas a mano (DeepSeek)

**Qué es.** Las tablas de A(Q) de `tablas_ds.json`, escritas a mano para las
seis preguntas de `preguntas.md` sobre `documento.md` (refugio de Peña Alta,
radicación 4-10-2026), en el esquema nuevo `{filas, conflicto, campo}` por
tabla. Sin API de modelos.

**Comando:** `python3 validar.py tablas_ds.json`

## Dónde dudé al llenar el esquema (2–3 líneas)

1. **Q5, el `desenlace`.** La `tabla_final` (solo documento) cierra la
   pregunta, así que puse `cerrada`, pero con K entra un conflicto y no sé si
   un conflicto debería tener su propio desenlace o basta con marcarlo en
   `conflicto`.
2. **Q4, la frontera entre `si` y el dato que falta.** Las dos ramas llevan
   `si` («el acceso viene del norte/sur») y justamente eso es el dato que se
   pregunta al usuario; no sé si ese supuesto debe ir en `si` o registrarse
   como dependencia faltante de K.
3. **Q6 frente a Q5.** En Q6 traté la premisa de K como revisión (sin
   `conflicto`) y en Q5 como conflicto de fuentes; la línea entre «se revisa
   el dato» y «dos fuentes chocan» no está decidida en el esquema.
4. **Q1 y Q3, «aparecen distinciones».** El validador marca «24 literas» y
   «al amanecer» como distinción además de sostén, por ser filas nuevas;
   seguí la regla literal, pero una única posición que cierra la pregunta
   quizá no sea una «distinción» en el sentido del marco.

## Salida de `python3 validar.py tablas_ds.json`

```
== Q1 ==
  pregunta: ¿Cuántas literas tiene el refugio de Peña Alta?
  R: solo el documento
  desenlace: cerrada
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: admisible→inadmisible: resto; ganan o pierden sostén: 24 literas; aparecen distinciones: 24 literas
    {"cambian_de_estado": {"admisible_a_inadmisible": ["resto"], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": ["24 literas"], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": ["24 literas"]}
  efecto: SÍ
  condición 2 (solo el documento, sin datos K): SÍ
  salida esperada (JSON): El refugio tiene 24 literas (oración 2): única posición admisible con sostén D1 y resto inadmisible.

== Q2 ==
  pregunta: ¿Cuántas horas de autonomía tiene el generador del refugio de Peña Alta?
  R: solo el documento
  desenlace: no establecido
  [nota] campo mudo (considerado y sin ruta): D5
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  [nota] tabla_final: admisibles sin ruta (no es error): resto
  diff inicial->final: (sin efecto)
    {"cambian_de_estado": {"admisible_a_inadmisible": [], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": [], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": []}
  efecto: NO
  condición 2 (solo el documento, sin datos K): SÍ
  salida esperada (JSON): El documento no lo establece: diff vacío; D5 (generador de 3 kW) queda mudo y ninguna posición gana sostén.

== Q3 ==
  pregunta: ¿Cuándo sale la excursión al refugio de Peña Alta?
  R: solo el documento
  desenlace: cerrada
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: admisible→inadmisible: resto; ganan o pierden sostén: al amanecer; aparecen distinciones: al amanecer
    {"cambian_de_estado": {"admisible_a_inadmisible": ["resto"], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": ["al amanecer"], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": ["al amanecer"]}
  efecto: SÍ
  condición 2 (solo el documento, sin datos K): SÍ
  salida esperada (JSON): La excursión sale al amanecer (oración 4): única posición admisible con sostén D3 y resto inadmisible.

== Q4 ==
  pregunta: ¿Dónde está el refugio de Peña Alta?
  R: libre
  desenlace: no cerrable
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  [nota] tabla_final: admisibles sin ruta (no es error): resto
  diff inicial->final: ganan o pierden sostén: junto al collado Norte, junto al collado Sur; aparecen distinciones: junto al collado Norte, junto al collado Sur
    {"cambian_de_estado": {"admisible_a_inadmisible": [], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": ["junto al collado Norte", "junto al collado Sur"], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": ["junto al collado Norte", "junto al collado Sur"]}
  efecto: SÍ
  condición 2: no aplica (R = libre)
  salida esperada (JSON): No cerrable: K1 (regla genérica) da sostén a dos ramas —«junto al collado Norte» si el acceso viene del norte y «junto al collado Sur» si viene del sur—, el resto queda admisible sin sostén, y se pregunta al usuario: «¿por qué collado se sube al refugio?».

== Q5 ==
  pregunta: ¿Cuántas mantas hay en el refugio de Peña Alta?
  R: libre
  desenlace: cerrada
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: admisible→inadmisible: resto; ganan o pierden sostén: 40 mantas; aparecen distinciones: 40 mantas
    {"cambian_de_estado": {"admisible_a_inadmisible": ["resto"], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": ["40 mantas"], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": ["40 mantas"]}
  diff final->revisada: inadmisible→admisible: 55 mantas; ganan o pierden sostén: 40 mantas; cambia la razón de exclusión: resto; aparecen distinciones: 55 mantas
    {"cambian_de_estado": {"admisible_a_inadmisible": [], "inadmisible_a_admisible": ["55 mantas"]}, "ganan_o_pierden_sosten": ["40 mantas"], "cambia_la_razon_de_exclusion": ["resto"], "aparecen_distinciones": ["55 mantas"]}
  efecto: SÍ
  condición 2: no aplica (R = libre)
  condición 3 (conflicto ⇒ salida): conflicto=['D4', 'K2']; salida_esperada presente
  salida esperada (JSON): Conflicto de fuentes: el documento dice 40 mantas (D4) y la premisa simulada de K dice 55 (K2, inventario consultado el 1-10-2026); la tabla revisada muestra ambas admisibles con conflicto [D4, K2].
  [avisos]
    - conflicto ['D4', 'K2'] declarado; salida_esperada presente

== Q6 ==
  pregunta: ¿Qué día reabre la senda de acceso al refugio de Peña Alta tras las obras?
  R: libre
  desenlace: cerrada
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: admisible→inadmisible: resto; ganan o pierden sostén: 1 de noviembre de 2026; aparecen distinciones: 1 de noviembre de 2026
    {"cambian_de_estado": {"admisible_a_inadmisible": ["resto"], "inadmisible_a_admisible": []}, "ganan_o_pierden_sosten": ["1 de noviembre de 2026"], "cambia_la_razon_de_exclusion": [], "aparecen_distinciones": ["1 de noviembre de 2026"]}
  diff final->revisada: admisible→inadmisible: 1 de noviembre de 2026; inadmisible→admisible: 18 de octubre de 2026; cambia la razón de exclusión: resto; aparecen distinciones: 18 de octubre de 2026
    {"cambian_de_estado": {"admisible_a_inadmisible": ["1 de noviembre de 2026"], "inadmisible_a_admisible": ["18 de octubre de 2026"]}, "ganan_o_pierden_sosten": [], "cambia_la_razon_de_exclusion": ["resto"], "aparecen_distinciones": ["18 de octubre de 2026"]}
  efecto: SÍ
  condición 2: no aplica (R = libre)
  salida esperada (JSON): El dato D2 (cierre del 15 al 31 de octubre) excluía el 18 de octubre; la premisa simulada K3 (la clausura se levantó el 18-10-2026, consultada el 2-10-2026) invalida D2 y el 18 de octubre vuelve a ser admisible, mientras el 1 de noviembre deja de serlo.

== resumen ==
  preguntas: 6
  errores: 0
  avisos: 1
    [AVISO] Q5: conflicto ['D4', 'K2'] declarado; salida_esperada presente
  preguntas con efecto: 5/6
```

**Nota.** La Q2 es la única sin efecto (desenlace `no establecido`), y la Q4
es `no cerrable` con el resto admisible; la Q5 y la Q6 ejercitan las cuatro
clases del diff (incluida `inadmisible→admisible`). El validador sale con
código 0 (cero errores).
