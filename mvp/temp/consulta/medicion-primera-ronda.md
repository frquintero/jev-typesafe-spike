# Registro de la primera ronda de la consulta: `doc4` y `doc6`

**Esto es un registro, no diseño.** Es el detalle de las **trece corridas** de la primera ronda
—las cinco preguntas de `doc4` (26 datos, 5 casos) y las cinco de `doc6` (33 datos, 14 casos), más
réplicas de `doc4` q1, q2 y q5—, corridas con **prompt 3**. El diseño vive en
`mvp/consulta-diseno.md`; los crudos de esas corridas, en
`mvp/temp/consulta/{cache,salida.md,traza.jsonl}`, y la extracción que leyeron, en
`mvp/temp/extraccion/doc4/` y `mvp/temp/extraccion/doc6/`.

## Consumo de las corridas (`prompt_tokens = hit + miss`)

| Corrida | Turnos | Turno 1 | Turnos siguientes |
|---|---|---|---|
| doc4 Q1 r1 | 2 | 1501 = 0 + 1501 | 1887 = 1536 + 351 |
| doc4 Q1 r2 | 2 | 1020 = 0 + 1020 | 2393 = 1280 + 1113 |
| doc4 Q2 r1 | 2 | 1502 = 0 + 1502 | 1886 = 1536 + 350 |
| doc4 Q2 r2 | 2 | 1021 = 0 + 1021 | 1432 = 1024 + 408 |
| doc4 Q3 r1 | 2 | 1016 = 0 + 1016 | 1408 = 1024 + 384 |
| doc4 Q4 r1 | 2 | 1030 = 0 + 1030 | 2155 = 1152 + 1003 |
| doc4 Q5 r1 | 3 | 879 = 0 + 879 | 1604 = 1024 + 580 · 3023 = 2432 + 591 |
| doc4 Q5 r2 | 2 | 879 = 0 + 879 | 1584 = 896 + 688 |
| doc6 Q1 r1 | 2 | 1431 = 0 + 1431 | 2011 = 1664 + 347 |
| doc6 Q2 r1 | 6 | 1421 = 0 + 1421 | 1704 = 1536 + 168 · 2105 = 1920 + 185 · 2445 = 2176 + 269 · 2717 = 2560 + 157 · 3001 = 2816 + 185 |
| doc6 Q3 r1 | 2 | 1426 = 0 + 1426 | 1768 = 1536 + 232 |
| doc6 Q4 r1 | 2 | 1420 = 0 + 1420 | 2221 = 1792 + 429 |
| doc6 Q5 r1 | 2 | 1423 = 0 + 1423 | 1828 = 1536 + 292 |

Lectura: el **prefijo fijo se cachea** (el `hit` aparece desde el segundo turno) y lo que se paga es
lo nuevo —cada resultado de herramienta y cada mensaje del asistente—. El precio se calcula con la
tarifa publicada el día de la corrida; no se estima a ojo.

## Qué entregó cada corrida

| Corrida | Casos pedidos | Distintos | Turnos · llamadas | Qué entregó |
|---|---|---|---|---|
| doc4 Q1 `-r1` | `U1` | 1 | 2 · 2 | respondida: la empresa de acueducto, en el barrio San Jorge |
| doc4 Q1 `-r2` | `U1`, `U3`, `U4` | 3 | 2 · 4 | respondida: la empresa de acueducto, en el barrio San Jorge |
| doc4 Q2 `-r1` | `U1` | 1 | 2 · 2 | respondida: catorce horas |
| doc4 Q2 `-r2` | `U1` | 1 | 2 · 2 | respondida: catorce horas (desde las seis de la mañana del jueves) |
| doc4 Q3 `-r1` | `U2` | 1 | 2 · 2 | respondida: la reparación de una tubería matriz en la carrera séptima |
| doc4 Q4 `-r1` | `U4`, `U1` | 2 | 2 · 2 | sin entrega: el JSON vino como texto |
| doc4 Q5 `-r1` | `U4`, `U4` | 1 | 3 · 2 | sin JSON leído: vino envuelto en ```json |
| doc4 Q5 `-r2` | `U4` | 1 | 2 · 1 | sin JSON leído: prosa + ```json |
| doc6 Q1 `-r1` | `U1`, `U3` | 2 | 2 · 2 | respondida: la avenida Los Nogales, sesenta metros |
| doc6 Q2 `-r1` | `U4`, `U13`, `U1`, `U2`, `U4` | 4 | 6 · 5 | sin JSON leído: el JSON vino envuelto en una cerca |
| doc6 Q3 `-r1` | `U5` | 1 | 2 · 1 | respondida: la muerte de un estudiante atropellado en 2023 |
| doc6 Q4 `-r1` | `U7`, `U12` | 2 | 2 · 2 | sin JSON leído: prosa, y el JSON decía `no_esta_en_el_corpus` |
| doc6 Q5 `-r1` | `U12` | 1 | 2 · 1 | respondida: la secretaria de Infraestructura |

Nunca pidió todos los casos —ni los 5 de `doc4` ni los 14 de `doc6`: filtra por el umbral del 80 %
sobre los nombres. La más larga fue `doc6` Q2, que pidió `U4` dos veces y gastó 6 turnos y 5
llamadas.

**Dos mecanismos de entrega, no comparables en ese detalle.** Las seis primeras corridas de `doc4`
—q1, q2, q3 y sus réplicas— entregaban con la herramienta `entregar`: su crudo trae `datos` y
`reporte`, y su `contenido_final` está vacío. Desde «fuera la herramienta entregar» (07-10), la
entrega es el **mensaje final**, y así corrieron `doc4` q4–q5 y todo `doc6`. El campo `herramientas`
del crudo dice con cuál se hizo cada corrida.

**Lo que la medición dejó a la vista:**

1. **El JSON como texto** (`doc4` Q4): con la entrega por herramienta, el agente escribió el JSON en
   su mensaje final y no llamó `entregar`, así que la entrega quedó ausente (`cerrado: false`,
   `contenido_final` vacío). Con la entrega por mensaje final, ese JSON se lee.
2. **El JSON envuelto** (`doc4` Q5, las dos réplicas; `doc6` Q2; `doc6` Q4): el agente escribe,
   además del JSON, la prosa que le pide la tarea 5 y/o la cerca de código. El ORQ de entonces exigía
   que **todo** el mensaje fuera JSON, así que no lo leía aunque el JSON estuviera a la vista.
   **Corregido el 08-10:** el ORQ lo ubica donde prompt 3 lo ponga; la relectura de los crudos
   guardados —sin volver a llamar al modelo— recupera las cinco que quedaron en `None` y deja como
   estaban las cinco del mecanismo viejo que ya traían su entrega.
3. **El referente abierto** (`doc4` Q5): la corrida entregó `respondida`, con el reclamo atribuido a
   la junta de acción comunal. Los datos leídos de `U4` no incluyen el referente del reclamo; la
   extracción del paso 2 declaró dos dudas sobre los referentes («Su reclamo», «Su decisión»).

## La extracción de esos dos documentos

- **`doc4`**: paso 1 (v10, Muse) → 5 unidades (`[1–3]`, `[4–6]`, `[7]`, `[8,9,10,13–17]`,
  `[11,12]`); paso 2 → **5 casos y 26 datos**. Las dos dudas de `U4` —el referente de «Su reclamo» y
  de «Su decisión»— quedaron en el crudo del paso 2: la base no las guarda.
- **`doc6`**: paso 1 (v10, Muse) → **14 unidades**; paso 2 → **14 casos y 33 datos**.
- **`unidad_valor` se usa poco**: 3 de 26 datos en `doc4` y 4 de 33 en `doc6` (de ahí que D16 siga
  abierta en el diseño).
