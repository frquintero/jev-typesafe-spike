# reporte_ds.md — prueba de mesa 1, tablas a mano (DeepSeek)

**Qué es.** Las tablas de A(Q) de `tablas_ds.json`, escritas a mano para las
cuatro preguntas de `preguntas.md` sobre `documento.md` (bodega de San Martín,
radicación 3-10-2026). Sin API de modelos.

**Comando:**

```
python3 validar.py tablas_ds.json
```

## Dónde dudé al llenar el esquema (2–3 líneas)

1. **P3, la fila «resto».** El documento fija la regla (vendimia a los 22
   °Brix) pero no la fecha; dejé «resto» como *admisible sin ruta* en vez de
   inadmisible, porque no me pareció que las dos quincenas distinguidas
   agoten el dominio. No sé si eso es lo que el marco espera de una
   distinción por `si`.
2. **P4, cómo mostrar el conflicto.** Lo representé como dos filas admisibles
   con rutas distintas (D2 documento / K4 premisa simulada) y sin `si`, en vez
   de volver inadmisible la del documento o de marcar la fuente con `si`; no
   hay una decisión escrita sobre cuál de las dos formas es la correcta.
3. **P2, una dependencia que no sostiene.** Dejé D5 (barricas de roble) en
   `dependencias` aunque no entra en ninguna ruta, para que se vea el dato
   mudo; no sé si el esquema admite dependencias consideradas que no
   establecen el estado.

## Salida de `python3 validar.py tablas_ds.json`

```
== P1 ==
  pregunta: ¿Cuántos kilos de uva prensa la bodega de San Martín al día?
  R: solo el documento
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: dejan de ser admisibles: resto; ganan o pierden sostén: 8 000
    {"dejan_de_ser_admisibles": ["resto"], "ganan_o_pierden_sosten": ["8 000"], "aparecen_distinciones": []}
  condición 1 (diff != vacío): SÍ
  condición 2 (solo el documento, sin datos K): SÍ
  salida esperada (JSON): La bodega prensa 8 000 kilos de uva al día (oración 4); la tabla pasa de todo el dominio admisible a 8 000 admisible con sostén D4 y el resto inadmisible.

== P2 ==
  pregunta: ¿Cuántas barricas de roble tiene la bodega de San Martín?
  R: solo el documento
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  [nota] tabla_final: admisibles sin ruta (no es error): resto
  diff inicial->final: (sin efecto)
    {"dejan_de_ser_admisibles": [], "ganan_o_pierden_sosten": [], "aparecen_distinciones": []}
  condición 1 (diff != vacío): NO
  condición 2 (solo el documento, sin datos K): SÍ
  salida esperada (JSON): El documento no lo establece: la tabla no se mueve (diff vacío); D5 queda mudo y ninguna posición gana sostén.

== P3 ==
  pregunta: ¿Cuándo empieza la vendimia en la parcela Los Olivos?
  R: libre
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  [nota] tabla_final: admisibles sin ruta (no es error): resto
  diff inicial->final: ganan o pierden sostén: primera quincena de septiembre, primera quincena de octubre; aparecen distinciones: primera quincena de septiembre, primera quincena de octubre
    {"dejan_de_ser_admisibles": [], "ganan_o_pierden_sosten": ["primera quincena de septiembre", "primera quincena de octubre"], "aparecen_distinciones": ["primera quincena de septiembre", "primera quincena de octubre"]}
  condición 1 (diff != vacío): SÍ
  condición 2: no aplica (R = libre)
  salida esperada (JSON): Dos inicios admisibles según el supuesto no fijado: primera quincena de septiembre si el año es cálido y primera quincena de octubre si es frío; el resto de fechas sigue admisible sin sostén.

== P4 ==
  pregunta: ¿Cuántas hectáreas tiene la parcela Los Olivos?
  R: libre
  [nota] tabla_inicial: admisibles sin ruta (no es error): resto
  diff inicial->final: dejan de ser admisibles: resto; ganan o pierden sostén: 3
    {"dejan_de_ser_admisibles": ["resto"], "ganan_o_pierden_sosten": ["3"], "aparecen_distinciones": []}
  diff final->revisada: ganan o pierden sostén: resto; aparecen distinciones: 2,5
    {"dejan_de_ser_admisibles": [], "ganan_o_pierden_sosten": ["resto"], "aparecen_distinciones": ["2,5"]}
  condición 1 (diff != vacío): SÍ
  condición 2: no aplica (R = libre)
  salida esperada (JSON): Conflicto: el documento dice 3 hectáreas (D2) y la premisa simulada de K dice 2,5 hectáreas (K4, catastro consultado el 28-9-2026); la tabla revisada muestra ambas admisibles con rutas distintas y el resto inadmisible por las dos.

== resumen ==
  preguntas: 4
  errores: 0
  preguntas con efecto (condición 1): 3/4
```

**Nota.** La P2 es la única sin efecto (condición 1 = NO): es la salida
correcta «el documento no lo establece». El validador sale con código 0
(cero errores) y deja la P4 con dos diffs: inicial→final y final→revisada.
