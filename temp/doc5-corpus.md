# doc5 · casos de estudio y datos

Artefacto de trabajo (carpeta `temp/`; no es documentación del repo).

**Documento:** `mvp/pruebas/doc5.md` · **dominio:** TRANVÍA · 17 oraciones. **Extracción:** partición de v9 + candidato `prompt_ficha_contexto` (entrada b), `deepseek-flash`; crudos en `mvp/paso2/cache/comp-doc5-b-u{1..5}-deepseek-r1.json`.

**Criterio (A.2):** caso de estudio = unidad constituida y mantenida por individuación y reidentificación, **acerca de la cual se establecen y reúnen determinaciones**. En el corpus son las anclas del campo `caso` de cada determinación: **12** en `doc5`, dos de ellas acciones. Las demás unidades que el extractor individualizó van en el anexo: no son casos de estudio.

## 1. El documento (numerado como lo vio el extractor)

```
[1] El primer tranvía de la ciudad empezó a rodar en 1893. [2] Lo operaba una compañía inglesa con capital privado. [3] La red llegó a tener veintiocho kilómetros de vías, según los planos de la época.

[4] En 1927, un incendio destruyó las caballerizas de la compañía. [5] El fuego se originó en un depósito de forraje. [6] La compañía no repuso los animales. [7] La ciudad tardó dos años en restablecer el servicio.

[8] En 1948, la municipalidad compró la red. [9] La compra incluyó los talleres y los vehículos que aún servían. [10] El municipio prometió modernizar las líneas. [11] Nunca ejecutó esa promesa.

[12] Los últimos tranvías circularon hasta 1965. [13] Su retiro coincidió con la ampliación de la avenida central. [14] La historiadora y la archivista revisaron los planos del taller. [15] Ella encontró un plano fechado en 1911. [16] Su hallazgo se publicó en la revista municipal. [17] La historiadora, Elvira Sanmiguel, atribuyó el cierre a la presión de los transportadores.
```

## 2. Casos de estudio (12)

| Caso de estudio | Unidad | Tipo | Nombre | Se reconoce por | Aspectos que reúne | Datos |
|---|---|---|---|---|---|---|
| `doc5:U1:C1` | `doc5:U1` | caso | primer tranvía de la ciudad | [1] «El primer tranvía de la ciudad»; [2] «Lo» | año de inicio de rodadura | `doc5:U1:D1` |
| `doc5:U1:C2` | `doc5:U1` | caso | compañía inglesa con capital privado | [2] «una compañía inglesa con capital privado» | nacionalidad, tipo de capital | `doc5:U1:D2`, `doc5:U1:D3` |
| `doc5:U1:C3` | `doc5:U1` | caso | red | [3] «La red» | longitud de vías | `doc5:U1:D4` |
| `doc5:U2:A1` | `doc5:U2` | acción | destruyó (incendio → caballerizas de la compañía) | [4] «un incendio destruyó las caballerizas de la compañía» | año | `doc5:U2:D1` |
| `doc5:U2:A3` | `doc5:U2` | acción | restablecer (ciudad del primer tranvía → servicio del tranvía) | [7] «restablecer el servicio» | duración | `doc5:U2:D2` |
| `doc5:U3:C5` | `doc5:U3` | caso | los vehículos que aún servían | [9] «los vehículos que aún servían» | servicio | `doc5:U3:D1` |
| `doc5:U4:C1` | `doc5:U4` | caso | tranvías de la ciudad iniciados con el primer tranvía | [12] «Los últimos tranvías» | año final de circulación, posición en la serie de tranvías | `doc5:U4:D1`, `doc5:U4:D2` |
| `doc5:U4:C2` | `doc5:U4` | caso | retiro/cierre de los tranvías de la ciudad iniciados con el primer tranvía | [13] «Su retiro»; [17] «el cierre» | causa | `doc5:U4:D4` |
| `doc5:U4:C4` | `doc5:U4` | caso | Elvira Sanmiguel | [17] «La historiadora, Elvira Sanmiguel» | presentada como | `doc5:U4:D3` |
| `doc5:U5:C1` | `doc5:U5` | caso | historiadora | [14] «La historiadora» | presentada como | `doc5:U5:D1` |
| `doc5:U5:C2` | `doc5:U5` | caso | archivista | [14] «la archivista» | presentada como | `doc5:U5:D2` |
| `doc5:U5:C5` | `doc5:U5` | caso | plano | [15] «un plano fechado en 1911» | fecha | `doc5:U5:D3` |

## 3. Datos (14 determinaciones)

| Dato | Caso · aspecto · valor | Condiciones | Capa | Respaldo |
|---|---|---|---|---|
| `doc5:U1:D1` | primer tranvía de la ciudad (C1) · **año de inicio de rodadura** = 1893 | — | — | [1] «empezó a rodar en 1893» |
| `doc5:U1:D2` | compañía inglesa con capital privado (C2) · **nacionalidad** = inglesa | — | — | [2] «compañía inglesa» |
| `doc5:U1:D3` | compañía inglesa con capital privado (C2) · **tipo de capital** = privado | — | — | [2] «con capital privado» |
| `doc5:U1:D4` | red (C3) · **longitud de vías** = veintiocho kilómetros | — | K1 «según planos de la época» | [3] «La red llegó a tener veintiocho kilómetros de vías» |
| `doc5:U2:D1` | destruyó (incendio → caballerizas de la compañía) (A1) · **año** = 1927 | — | — | [4] «En 1927» |
| `doc5:U2:D2` | restablecer (ciudad del primer tranvía → servicio del tranvía) (A3) · **duración** = dos años | — | — | [7] «tardó dos años» |
| `doc5:U3:D1` | los vehículos que aún servían (C5) · **servicio** = aún servían | — | — | [9] «que aún servían» |
| `doc5:U4:D1` | tranvías de la ciudad iniciados con el primer tranvía (C1) · **año final de circulación** = 1965 | — | — | [12] «circularon hasta 1965» |
| `doc5:U4:D2` | tranvías de la ciudad iniciados con el primer tranvía (C1) · **posición en la serie de tranvías** = últimos | — | — | [12] «Los últimos tranvías» |
| `doc5:U4:D3` | Elvira Sanmiguel (C4) · **presentada como** = historiadora | — | — | [17] «La historiadora, Elvira Sanmiguel» |
| `doc5:U4:D4` | retiro/cierre de los tranvías de la ciudad iniciados con el primer tranvía (C2) · **causa** = presión de los transportadores | — | K1 «atribuyó Elvira Sanmiguel» | [17] «atribuyó el cierre a la presión de los transportadores» |
| `doc5:U5:D1` | historiadora (C1) · **presentada como** = historiadora | — | — | [14] «La historiadora» |
| `doc5:U5:D2` | archivista (C2) · **presentada como** = archivista | — | — | [14] «la archivista» |
| `doc5:U5:D3` | plano (C5) · **fecha** = 1911 | — | — | [15] «fechado en 1911» |

## 4. Dudas registradas (3)

| Duda | Texto | Respaldo |
|---|---|---|
| `doc5:U5:Q1` | No se establece si «Ella» en [15] es la historiadora o la archivista. | [14]; [15] |
| `doc5:U5:Q2` | No se establece de quién fue el hallazgo, pues «Su» depende de «Ella» en [15]: la historiadora o la archivista. | [14]; [15]; [16] |
| `doc5:U5:Q3` | No se establece cuál de los talleres incluidos en la compra es el taller cuyos planos se revisaron. | [14]; [9] |

## Anexo · menciones que **no** son casos de estudio (21)

Unidades que el extractor individualizó por menciones pero que **no anclan ninguna determinación**: participantes, lugares, fuentes o valores.

| Mención | Unidad | Nombre | Menciones | Papel |
|---|---|---|---|---|
| `doc5:U1:C4` | `doc5:U1` | planos de la época | [3] «los planos de la época» | quien de una capa |
| `doc5:U1:C5` | `doc5:U1` | ciudad | [1] «la ciudad» | extremo de una relación |
| `doc5:U2:C1` | `doc5:U2` | compañía inglesa con capital privado | [4] «de la compañía»; [6] «La compañía» | agente de una acción |
| `doc5:U2:C2` | `doc5:U2` | incendio | [4] «un incendio»; [5] «El fuego» | agente de una acción |
| `doc5:U2:C3` | `doc5:U2` | caballerizas de la compañía | [4] «las caballerizas de la compañía» | objeto de una acción |
| `doc5:U2:C4` | `doc5:U2` | depósito de forraje | [5] «un depósito de forraje» | extremo de una relación |
| `doc5:U2:C5` | `doc5:U2` | animales | [6] «los animales» | objeto de una acción |
| `doc5:U2:C6` | `doc5:U2` | ciudad del primer tranvía | [7] «La ciudad» | agente de una acción |
| `doc5:U2:C7` | `doc5:U2` | servicio del tranvía | [7] «el servicio» | objeto de una acción |
| `doc5:U3:C1` | `doc5:U3` | municipalidad/municipio | [8] «la municipalidad»; [10] «El municipio»; [11] «Nunca ejecutó» | agente de una acción |
| `doc5:U3:C2` | `doc5:U3` | red del tranvía | [8] «la red» | objeto de una acción |
| `doc5:U3:C3` | `doc5:U3` | la compra | [9] «La compra» | extremo de una relación |
| `doc5:U3:C4` | `doc5:U3` | los talleres | [9] «los talleres» | extremo de una relación |
| `doc5:U3:C6` | `doc5:U3` | las líneas | [10] «las líneas» | objeto de una acción |
| `doc5:U3:C7` | `doc5:U3` | promesa de modernizar las líneas | [10] «prometió modernizar las líneas»; [11] «esa promesa» | objeto de una acción |
| `doc5:U4:C3` | `doc5:U4` | ampliación de la avenida central | [13] «la ampliación de la avenida central» | extremo de una relación |
| `doc5:U4:C5` | `doc5:U4` | presión de los transportadores | [17] «la presión de los transportadores» | solo mencionado |
| `doc5:U5:C3` | `doc5:U5` | planos | [14] «los planos del taller» | objeto de una acción |
| `doc5:U5:C4` | `doc5:U5` | taller | [14] «del taller» | extremo de una relación |
| `doc5:U5:C6` | `doc5:U5` | hallazgo | [16] «Su hallazgo» | objeto de una acción |
| `doc5:U5:C7` | `doc5:U5` | revista municipal | [16] «la revista municipal» | extremo de una relación |

**Nota.** El campo `casos` de la ficha es la traducción del extractor («aquello de lo que el texto dice algo…, se reconoce por sus menciones»), registrada en `definiciones-del-marco.md` parte B; no es el caso de estudio de A.2. La unidad temática de parte B (núcleo, satélites y sus oraciones) no se recupera de v9, cuyo eje es el asunto: pendiente 7 de la memoria.