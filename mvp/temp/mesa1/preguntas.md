# preguntas.md — cuatro preguntas y su R

Documento: `documento.md` (radicación 3-10-2026). Reglas de la consulta (R)
según `zettel-vision-operativa.md`, «Las reglas de la consulta (R)».

Encabezado común de toda fila: `posicion · si · estado · ruta`. `si` lleva
solo los supuestos **no establecidos** de los que depende la fila; lo que
establecen los datos o las reglas sale por `ruta`. El caso, el aspecto y las
condiciones de la pregunta van en el encabezado de la pregunta.

---

## P1 — la responde el documento sin mundo externo

**Pregunta:** ¿Cuántos kilos de uva prensa la bodega de San Martín al día?

**R:** fuentes admitidas como premisa: **«solo el documento»**. No entra
ninguna premisa externa; el mundo del orquestador no hace falta.

**Tablas:** `tabla_inicial` y `tabla_final`.

**Salida esperada (una línea):** la bodega prensa 8 000 kilos de uva al día
(oración 4); la tabla pasa de todo el dominio admisible a 8 000 admisible con
sostén D4 y el resto inadmisible.

---

## P2 — el documento no la responde; R = «solo el documento»

**Pregunta:** ¿Cuántas barricas de roble tiene la bodega de San Martín?

**R:** fuentes admitidas como premisa: **«solo el documento»**.

**Tablas:** `tabla_inicial` y `tabla_final`, iguales.

**Salida esperada (una línea):** **el documento no lo establece**: la tabla no
se mueve (diff vacío), D5 queda mudo y ninguna posición gana sostén.

---

## P3 — dos respuestas posibles según un supuesto no fijado

**Pregunta:** ¿Cuándo empieza la vendimia en la parcela Los Olivos?

**R:** fuentes admitidas como premisa: **libre** (por defecto); aun así, el
supuesto que decide la fecha (año cálido o frío) no está fijado por el
documento y se registra en `si`, no en una premisa externa.

**Tablas:** `tabla_inicial` y `tabla_final` (dos filas admisibles con `si`
distintos).

**Salida esperada (una línea):** la tabla final distingue dos inicios
admisibles según el supuesto no fijado —primera quincena de septiembre si el
año es cálido y primera quincena de octubre si es frío—, y el resto de fechas
sigue admisible sin sostén.

---

## P4 — conflicto y revisión

**Pregunta:** ¿Cuántas hectáreas tiene la parcela Los Olivos?

**R:** fuentes admitidas como premisa: **libre**.

**Premisa de K (simulada):** catastro municipal de San Martín, «la parcela Los
Olivos mide 2,5 hectáreas»; **procedencia:** K: catastro municipal (premisa
simulada); **fecha de consulta:** 28-9-2026. La palabra «simulada» marca que
la premisa es inventada para la prueba.

**Tablas:** tres.
- `tabla_inicial`: A(Q | K), sin datos.
- `tabla_final`: solo con el documento y las reglas (D2: 3 hectáreas).
- `tabla_revisada`: tras entrar la premisa de K (K4: 2,5 hectáreas).

**Salida esperada (una línea):** conflicto: el documento dice 3 hectáreas (D2)
y la premisa simulada de K dice 2,5 hectáreas (K4, catastro consultado el
28-9-2026); la tabla revisada muestra ambas admisibles con rutas distintas y
el resto inadmisible por las dos.

---

## Índice para el validador

- P1: `R.fuentes = "solo el documento"`; efecto SÍ.
- P2: `R.fuentes = "solo el documento"`; efecto NO → «el documento no lo
  establece».
- P3: `R.fuentes = "libre"`; efecto SÍ (distinción por `si`).
- P4: `R.fuentes = "libre"`; efecto SÍ y revisión con conflicto D↔K.
