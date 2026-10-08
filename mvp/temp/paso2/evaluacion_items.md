# Paso 2 · evaluación por ítem (conteo auditable) · 06-10-2026

Sustituye, para la recuperación, a las tablas agregadas de
`evaluacion_desarrollo.md` y `evaluacion_reserva.md`. **Ninguna llamada nueva:**
todo sale de los crudos de `cache/` y de las expectativas fijadas antes de
llamar (`expectativas_desarrollo.md`, `expectativas_reserva.md`).

## La regla

- **Ítem**: cada expectativa **tal como quedó escrita y numerada** en
  `expectativas_desarrollo.md` (25 en doc4, 17 en doc5) y en
  `expectativas_reserva.md` (15 por documento, 30). No se inventó una lista
  nueva de ítems ni se movieron las expectativas después de ver las salidas.
- **cumple**: aparece lo que el ítem pide —contenido **y** la identidad, la
  condición o la duda que el propio ítem exige— sin deformarlo.
- **parcial**: aparece una parte y falta la otra (p. ej., el contenido sin la
  identidad externa, o la identidad sin el contenido).
- **no**: no aparece, o aparece deformado (fusión de dos acontecimientos).
- **n/e**: no evaluable; la corrida no produjo ficha (JSON inválido).
- **def.**: expectativa defectuosa; se informa aparte y **no entra** en el
  denominador de expectativas válidas.
- **Recuperación estricta** = `cumple` sobre expectativas válidas. Los
  `parcial` no se suman.
- **Fidelidad** = afirmaciones producidas fieles y del foco sobre producidas
  evaluables; se cuenta por código (determinaciones + capas + acciones +
  relaciones de cada ficha guardada).

Columnas de doc4: **aD aM = entrada (a) con DeepSeek y con Muse**; igual bD bM
y cD cM. doc5 solo tiene corridas de DeepSeek (aD bD cD). El respaldo cita el
registro de la ficha que sustenta la calificación; cuando la calificación no
es `cumple`, el motivo va en la misma celda.

---

## doc4 · 25 expectativas (24 válidas; la 25 es defectuosa)

| # | Ítem esperado | aD | aM | bD | bM | cD | cM | Respaldo / motivo |
|---|---|---|---|---|---|---|---|---|
| 1 | La empresa de acueducto anunció un corte de agua. | cumple | cumple | cumple | cumple | cumple | cumple | C1 «empresa de acueducto» + K1/A1 |
| 2 | El corte es en el barrio San Jorge. | cumple | cumple | cumple | cumple | cumple | cumple | C2/C3 y el nombre del caso |
| 3 | El corte es para el jueves. | cumple | cumple | cumple | cumple | cumple | cumple | D3/D1 o el nombre del caso |
| 4 | Durará catorce horas. | cumple | cumple | cumple | cumple | cumple | cumple | D1 |
| 5 | Empieza a las seis de la mañana. | cumple | cumple | cumple | cumple | cumple | cumple | D2 |
| 6 | Afectará a unos tres mil usuarios, atribuido a la empresa. | cumple | cumple | cumple | cumple | cumple | cumple | D4 «dentro de» la capa «según» |
| 7 | La causa es la reparación de una tubería matriz, y es la causa **del corte**. | parcial | parcial | parcial | parcial | cumple | cumple | (a) y (b): «causa = reparación» sin ligarla al corte; v9 no registró esa referencia en U2. (c): R3 «causa de» → corte |
| 8 | La tubería está en la carrera séptima. | cumple | cumple | cumple | cumple | cumple | cumple | C3 |
| 9 | La tubería tiene cuarenta años. | cumple | cumple | cumple | cumple | cumple | cumple | D1/D2 |
| 10 | Ya presentó fugas en 2021. | cumple | cumple | cumple | cumple | cumple | cumple | D2 o A1 con condición en 2021 |
| 11 | La cuadrilla trabajará con dos bombas de achique. | cumple | cumple | cumple | cumple | cumple | cumple | D3 / A1–A2 |
| 12 | La empresa **de acueducto** pidió a los vecinos **del barrio San Jorge** almacenar agua. | parcial | parcial | cumple | cumple | parcial | n/e | (a): contenido sin identidades. (c) DeepSeek: identifica la empresa y deja «los vecinos» sin barrio. (c) Muse: JSON inválido |
| 13 | La noche anterior **al jueves del corte**. | no | no | cumple | cumple | cumple | n/e | (a): queda como duda sin resolver; (b) y (c) DeepSeek la resuelven |
| 14 | La junta **de acción comunal** pidió que el corte no se hiciera en semana de exámenes. | cumple | cumple | cumple | cumple | cumple | cumple | C1/C3 + K1 + A1 negada |
| 15 | La empresa **de acueducto** respondió que la fecha ya estaba contratada. | parcial | parcial | cumple | cumple | cumple | cumple | (a): «la empresa» sin identificar; (b) y (c) con el referente |
| 16 | La fecha es la del corte, **el jueves**. | parcial | parcial | cumple | cumple | parcial | cumple | (a): relación fecha–corte sin el jueves. (b): «el jueves, la fecha del corte». (c) DeepSeek: la fecha del corte sin el jueves |
| 17 | La junta insistirá en la próxima reunión. | cumple | cumple | cumple | cumple | cumple | cumple | A2 |
| 18 | El año pasado un corte similar dejó sin servicio a dos colegios. | cumple | cumple | cumple | cumple | cumple | cumple | A1 + D2/D3 |
| 19 | El corte similar **no** es el de este año: unidos por la semejanza. | no | no | no | cumple | cumple | cumple | (a): sin relación y con duda del término de comparación. (b) DeepSeek: sigue el referente suministrado («el corte de agua en el barrio San Jorge») y **funde** los dos acontecimientos. (b) Muse: distingue (C1 «corte del año pasado») y relaciona |
| 20 | Aquel episodio duró diecinueve horas. | cumple | cumple | cumple | cumple | cumple | cumple | D1 |
| 21 | La personera y la secretaria **de la junta** revisaron la respuesta de la empresa (con el contenido de `[9]`). | parcial | parcial | cumple | cumple | parcial | parcial | (a): faltan la identidad de la empresa y el contenido de `[9]`; (c): falta el contenido de `[9]` en el caso «respuesta» |
| 22 | «Ella» pidió que se publicara el cronograma, sin resolver quién es. | cumple | cumple | cumple | cumple | cumple | cumple | A2 + duda |
| 23 | «Su reclamo» quedó registrado en el acta, sin resolver de quién. | cumple | cumple | cumple | cumple | cumple | cumple | R4/R1/D1 + duda |
| 24 | «Su decisión» se conocerá el miércoles, sin resolver de quién. | cumple | cumple | cumple | cumple | cumple | cumple | D2/D1/A3 + duda |
| 25 | El gerente dijo que evaluará «la solicitud» (remite a `[8]`). | def. | def. | def. | def. | def. | def. | **Expectativa defectuosa:** el documento admite `[8]`, `[14]` y `[15]`; conservar la duda es la conducta correcta. Todas las corridas conservan una duda y ninguna inventa una lectura única, así que no se califica |

Totales doc4 (24 válidas): (a) 17/24 = **70,8 %** en los dos modelos;
(b) DeepSeek 22/24 = **91,7 %**, Muse 23/24 = **95,8 %**;
(c) 21/24 = **87,5 %** en los dos modelos. Parciales: (a) 5+5; (b) 1+1;
(c) 3+1. «no»: (a) 2+2; (b) 1+0. n/e: (c) Muse 2 (fallo de `doc4 U3`).

---

## doc5 · 17 expectativas (todas válidas; solo DeepSeek)

| # | Ítem esperado | aD | bD | cD | Respaldo / motivo |
|---|---|---|---|---|---|
| 26 | El primer tranvía empezó a rodar en 1893. | cumple | cumple | cumple | D1 |
| 27 | Lo operaba una compañía inglesa con capital privado. | cumple | cumple | cumple | A1 + C2 |
| 28 | La red llegó a tener veintiocho kilómetros de vías, «según los planos». | cumple | cumple | cumple | D4 dentro de la capa «según» |
| 29 | En 1927 un incendio destruyó las caballerizas de la compañía **inglesa**. | parcial | cumple | cumple | (a): «compañía» sin identificar como la inglesa |
| 30 | El fuego se originó en un depósito de forraje. | cumple | cumple | cumple | R2 |
| 31 | La compañía no repuso los animales. | cumple | cumple | cumple | A2 negada |
| 32 | La ciudad **del primer tranvía** tardó dos años en restablecer el **servicio del tranvía**. | parcial | cumple | parcial | (b): el referente resuelve las dos identidades; (a) y (c) dejan «la ciudad» y «el servicio» |
| 33 | En 1948 la municipalidad compró la red **del tranvía** (la de los veintiocho kilómetros). | parcial | cumple | parcial | (b): «red del tranvía»; (a) y (c): «la red» |
| 34 | La compra incluyó los talleres y los vehículos que aún servían. | cumple | cumple | cumple | R1/R2/R3 |
| 35 | El municipio prometió modernizar las líneas. | cumple | cumple | cumple | K1 + A2 |
| 36 | Nunca ejecutó esa promesa. | cumple | cumple | cumple | A3 negada |
| 37 | Los últimos tranvías circularon hasta 1965 (los tranvías de la ciudad). | parcial | cumple | parcial | (b): los identifica con los tranvías de la ciudad |
| 38 | Su retiro coincidió con la ampliación de la avenida central. | cumple | cumple | cumple | R1 |
| 39 | La historiadora Elvira Sanmiguel atribuyó el cierre a la presión de los transportadores. | cumple | cumple | cumple | K1 + R2 (el contenido dentro de la capa) |
| 40 | Revisaron los planos **del taller**, sin establecer cuál de los talleres. | parcial | cumple | parcial | (b): registra la duda de cuál taller; (a) y (c) no |
| 41 | «Ella» encontró un plano fechado en 1911, sin resolver quién es. | cumple | cumple | cumple | A2 + D1 + duda |
| 42 | «Su hallazgo» se publicó en la revista municipal, sin resolver de quién. | cumple | cumple | cumple | D2/R2 + duda |

Totales doc5 (17 válidas, un solo modelo): (a) 12/17 = **70,6 %**;
(b) 17/17 = **100 %**; (c) 13/17 = **76,5 %**. Parciales: (a) 5; (c) 4.

---

## Total de desarrollo (65 casillas: doc4 24×2 + doc5 17)

| Entrada | Agregado (DeepSeek + Muse) | DeepSeek | Muse (solo doc4) |
|---|---|---|---|
| (a) unidad sola | 46/65 = **70,8 %** | 29/41 = 70,7 % | 17/24 = 70,8 % |
| **(b) unidad + referencias** | **62/65 = 95,4 %** | 39/41 = 95,1 % | 23/24 = 95,8 % |
| (c) unidad + documento | 55/65 = **84,6 %** | 34/41 = 82,9 % | 21/24 = 87,5 % |

El agregado es el que Frat autorizó (los dos modelos juntos) y su composición
es la de la tabla: DeepSeek corrió doc4 y doc5; Muse, solo doc4. **No se
atribuye el agregado a un solo modelo.**

**Parciales y defectuosas, aparte:** en doc4 hay **16 parciales** en (a),
**2** en (b) y **4** en (c); en doc5, **5** en (a) y **4** en (c). Las
expectativas defectuosas son **dos en todo el paso 2**: doc4 #25 (arriba) y
reserva B #11 (abajo).

## Reserva · 30 expectativas (29 válidas; la B11 es defectuosa)

Entrada (b), `deepseek-flash`. Los 6 crudos de Muse de la reserva A quedaron
**fuera del análisis** (corrida interrumpida); no entran en estos totales.

| # | Ítem esperado | bD | Respaldo |
|---|---|---|---|
| A1 | La cooperativa nació en 1998. | cumple | D1 |
| A2 | Once familias se repartieron las primeras colmenas. | cumple | D2 + A1 |
| A3 | Su miel se vende hoy en tres ferias regionales. | cumple | D1 / A1 (referencia «Su» conservada) |
| A4 | Reúne ciento cuarenta colmenas, «según el censo». | cumple | D1 dentro de la capa «según» |
| A5 | En marzo un hongo atacó las colmenas del lote norte. | cumple | A1 |
| A6 | Hernán Duque atribuyó la infección a la humedad. | cumple | K1 + R3 (contenido en la capa) |
| A7 | Perdió el quince por ciento de la producción. | cumple | D2 |
| A8 | La junta pidió a la alcaldía apoyo para comprar tratamiento. | cumple | A1 + D1 |
| A9 | La alcaldía respondió que dependía del presupuesto de julio. | cumple | K1 + R1 dentro de la capa |
| A10 | La junta insistirá en la reunión de agosto. | cumple | A2 |
| A11 | Dos años antes un brote parecido obligó a quemar nueve colmenas del lote sur (**no** es el de marzo). | cumple | R1 «parecido a» → ataque de marzo, sin fundir |
| A12 | Aquel episodio duró cuatro meses. | cumple | D1 |
| A13 | La presidenta y la secretaria revisaron el informe del técnico. | cumple | A1 + R1 |
| A14 | «Ella» propuso repetir el muestreo, sin resolver quién es. | cumple | A2 + duda |
| A15 | «Su propuesta» quedó en el acta, sin resolver de quién. | cumple | R2 + duda |
| B1 | El mural se pintó en 1962. | cumple | D1 |
| B2 | Lo encargó la asociación de comerciantes. | cumple | A1 |
| B3 | Mide dieciocho metros, «según el acta». | cumple | D2 dentro de la capa «según» |
| B4 | En 1998 la humedad levantó la pintura de la esquina norte. | cumple | A1 |
| B5 | Inés Vargas atribuyó el daño a una filtración antigua. | cumple | K1 + R1 |
| B6 | La asociación decidió no intervenir en ese momento. | cumple | K2 + A2 negada |
| B7 | En 2020 una campaña vecinal reunió fondos para la restauración. | cumple | A1 |
| B8 | La campaña alcanzó la mitad de lo previsto. | cumple | D1 |
| B9 | Los organizadores pidieron apoyo al distrito. | cumple | A2 |
| B10 | El distrito respondió que evaluaría la solicitud en marzo. | cumple | K1 + A3 |
| B11 | Una obra anterior **del mismo autor** se perdió en 1975: la identificación queda **sin resolver**. | def. | **Expectativa defectuosa, conservada tal como se fijó.** El crudo la resuelve como relación («del autor del mural del mercado viejo»), que es lo que manda el prompt: la falta de nombre no vuelve irresoluble una referencia. Se cuenta como **corrección posterior**, no como expectativa acertada fijada antes |
| B12 | Aquella pérdida duró décadas sin registro. | cumple | D3 + D4 |
| B13 | La curadora y la historiadora revisaron las fotografías del mural. | cumple | A1 + R1 |
| B14 | «Ella» identificó un boceto de 1961, sin resolver quién es. | cumple | A2 + D3 + duda |
| B15 | «Su identificación» se publicó en el catálogo, sin resolver de quién. | cumple | R2 + duda |

**Reserva, recuperación estricta: 29/29 = 100 %** (una expectativa
defectuosa, B11, informada aparte).

## Fidelidad (por código, sobre las fichas guardadas)

Producidos = determinaciones + capas + acciones + relaciones de cada ficha;
las marcas van dentro de su determinación y no se cuentan aparte.

| Conjunto | Producidos | Fieles y del foco | Resultado |
|---|---|---|---|
| Desarrollo (a) | 103 (DeepSeek 72 + Muse 31) | 103 | **100 %** |
| Desarrollo (b) | 113 (DeepSeek 76 + Muse 37) | 111 | **98,2 %** (DeepSeek 74/76; Muse 37/37) |
| Desarrollo (c) | 103 (DeepSeek 72 + Muse 31, 5 corridas) | 103 | **100 %** |
| Reserva (b) | 70 (DeepSeek) | 70 | **100 %** |

La única deformación sigue siendo la de `doc4 (b) U5` con DeepSeek (la fusión
de los dos cortes), que toca **dos** afirmaciones producidas. La corrida
`doc4 (c) U3` de Muse no produjo ficha (JSON inválido): queda fuera de
producidos y de fidelidad, y por eso (c) tiene 103 y no 134 producidos.

## Qué se retira del informe anterior

La tabla de la «segunda cuenta» (`evaluacion_desarrollo.md`: 87 casillas,
doc4 32 ítems, doc5 23, totales 67,8 % / 85,1 % / 81,6 %) **no es
reproducible**: la lista de 55 ítems atómicos nunca se registró (solo se
registraron las 42 expectativas de arriba) y sus denominadores por unidad son
inconsistentes — U3 figura sobre 4 con dos modelos (debería ser 8) y U4 sobre
6 (debería ser 10), de modo que la suma de los denominadores de la columna
(56) no da las 64 casillas del encabezado. Con la lista registrada y la regla
de arriba, los totales son los de esta tabla.

**No cambia** lo verificado en las celdas señaladas: `doc4 U2` en (a) y (b)
no liga la causa con el corte; `doc4 U5` en (a) no relaciona los dos cortes y
en (b) DeepSeek los funde; `doc4 U6` «la solicitud» admite varias lecturas
(por eso #25 es defectuosa); la reserva B «del mismo autor» se resuelve como
relación (por eso B11 es defectuosa).

## Límites

- **Un solo juez** (el ejecutor); ninguna casilla tiene segunda lectura.
- **Ítems más gruesos** que la cuenta fina retirada: un ítem que reúne
  contenido e identidad se califica `parcial` si falta una parte, pero sigue
  contando como un solo ítem. Si se quiere el conteo fino hay que escribir y
  registrar la lista de 55 ítems antes de volver a mirar las salidas.
- **Sin réplicas** por unidad y entrada: esto elige entre alternativas, no mide
  estabilidad.
- `doc5` no tiene corridas de Muse; la reserva no es validación independiente.
