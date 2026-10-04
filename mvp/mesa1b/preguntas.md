# preguntas.md — seis preguntas y su R

Documento: `documento.md` (radicación 4-10-2026).

Esquema (reglas vigentes de `mvp/mesa1/resultado.md`, «Decisiones tras la
revisión»): cada tabla es un objeto `{filas, conflicto, campo}`; cada fila es
`posicion · si · estado · ruta`, con fila `resto`. El aspecto fija la escala y
toda posición se escribe en ella (con unidad). El caso se cita por su id de
ficha; sin ficha, nombre canónico e `id: pendiente`. Lo ya establecido va en
`ruta`. `dependencias` = solo lo que aparece en alguna ruta. Una regla
genérica («suele») solo sostiene, nunca excluye. D = dato del corpus, K =
mundo (dato o regla), R = regla de la consulta. `desenlace` ∈ {cerrada, no
establecido, no cerrable}.

---

## Q1 — cerrada por el documento

**Pregunta:** ¿Cuántas literas tiene el refugio de Peña Alta?

**R:** fuentes admitidas como premisa: **«solo el documento»**.

**Desenlace:** `cerrada`.

**Salida esperada (una línea):** el refugio tiene 24 literas (oración 2): única
posición admisible con sostén D1 y resto inadmisible.

---

## Q2 — no establecido (diff vacío)

**Pregunta:** ¿Cuántas horas de autonomía tiene el generador del refugio de
Peña Alta?

**R:** fuentes admitidas como premisa: **«solo el documento»**.

**Desenlace:** `no establecido`.

**Salida esperada (una línea):** el documento no lo establece: diff vacío; D5
(generador de 3 kW) queda mudo y ninguna posición gana sostén.

---

## Q3 — «¿cuándo…?» respondida por un evento o condición

**Pregunta:** ¿Cuándo sale la excursión al refugio de Peña Alta?

**R:** fuentes admitidas como premisa: **«solo el documento»**.

**Desenlace:** `cerrada`.

**Salida esperada (una línea):** la excursión sale al amanecer (oración 4):
única posición admisible con sostén D3 y resto inadmisible.

---

## Q4 — no cerrable por falta de K (regla genérica, dos ramas)

**Pregunta:** ¿Dónde está el refugio de Peña Alta?

**R:** fuentes admitidas como premisa: **libre**. Aun así, ni el documento ni
un mundo razonable disponible dan la ubicación (por qué collado se sube).

**Desenlace:** `no cerrable`.

**Salida esperada (una línea):** no cerrable: K1 (regla genérica) da sostén a
dos ramas —«junto al collado Norte» si el acceso viene del norte y «junto al
collado Sur» si viene del sur—, el resto queda admisible sin sostén, y se
pregunta al usuario: «¿por qué collado se sube al refugio?».

---

## Q5 — conflicto de fuentes (tres tablas)

**Pregunta:** ¿Cuántas mantas hay en el refugio de Peña Alta?

**R:** fuentes admitidas como premisa: **libre**.

**Premisa de K (simulada):** inventario del club, «el refugio tiene 55
mantas»; **procedencia:** K: inventario del club (premisa simulada); **fecha
de consulta:** 1-10-2026. «Simulada» marca que la premisa es inventada para la
prueba.

**Desenlace:** `cerrada`.

**Tablas:** `tabla_inicial`, `tabla_final` (solo documento) y `tabla_revisada`
(con K). En la revisada se marca `conflicto: [D4, K2]`.

**Salida esperada (una línea):** conflicto de fuentes: el documento dice 40
mantas (D4) y la premisa simulada de K dice 55 (K2, inventario consultado el
1-10-2026); la tabla revisada muestra ambas admisibles con conflicto
[D4, K2].

---

## Q6 — una posición que vuelve a ser admisible (tres tablas)

**Pregunta:** ¿Qué día reabre la senda de acceso al refugio de Peña Alta tras
las obras?

**R:** fuentes admitidas como premisa: **libre**.

**Premisa de K (simulada):** aviso de obras del parque, «la clausura se
levantó el 18 de octubre de 2026»; **procedencia:** K: aviso de obras del
parque (premisa simulada); **fecha de consulta:** 2-10-2026.

**Desenlace:** `cerrada`.

**Tablas:** `tabla_inicial`, `tabla_final` (solo documento) y `tabla_revisada`
(con K). El dato D2 excluye el 18 de octubre; K3 lo invalida y esa posición
vuelve a ser admisible.

**Salida esperada (una línea):** el dato D2 (cierre del 15 al 31 de octubre)
excluía el 18 de octubre; la premisa simulada K3 (la clausura se levantó el
18-10-2026, consultada el 2-10-2026) invalida D2 y el 18 de octubre vuelve a
ser admisible, mientras el 1 de noviembre deja de serlo.

---

## Índice para el validador

| Q | R | desenlace | tablas | qué prueba |
|---|---|---|---|---|
| Q1 | solo el documento | cerrada | inicial, final | el documento cierra |
| Q2 | solo el documento | no establecido | inicial, final | diff vacío |
| Q3 | solo el documento | cerrada | inicial, final | posición por evento |
| Q4 | libre | no cerrable | inicial, final | genérico que sostiene, no excluye |
| Q5 | libre | cerrada | inicial, final, revisada | conflicto de fuentes (`conflicto`) |
| Q6 | libre | cerrada | inicial, final, revisada | posición que vuelve (inadmisible→admisible) |
