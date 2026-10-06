# Evaluación de la reserva · entrada (b) · 06-10-2026

Documentos `reserva_a.md` y `reserva_b.md` (sintéticos nuevos, sin los ejemplos del
prompt ni los textos de `mvp/pruebas/`). Expectativas fijadas antes de cualquier
llamada en `expectativas_reserva.md` (30 ítems: 15 por documento).

Partición: **v9 congelado**, una tarea de Muse por documento, sin correcciones a
mano (`salida_reservaA-v9.md`: 14/14 oraciones; `salida_reservaB-v9.md`: 15/15; sin
huecos ni solapes). 7 unidades en la reserva A y 5 en la B.

Extracción: candidato `prompt_ficha_contexto.md` (sha256 `889e2ecb…`), entrada (b),
`deepseek-flash`, 12 unidades, 36–81 s cada una (632 s en total).

**Esta reserva no es validación independiente:** la escribió el mismo que diseñó el
candidato y las expectativas.

## Recuperación · 30/30 = 100 %

### Reserva A (7 unidades, 15 ítems)

| Unidad | Ítems | Qué se recuperó |
|---|---|---|
| U1 (1) | 1, 2 | nació en 1998; once familias se repartieron las primeras colmenas |
| U2 (2) | 3 | «Su» → la cooperativa (referencia conservada); miel en tres ferias |
| U3 (3) | 4 | ciento cuarenta colmenas, dentro de la capa «según» el censo |
| U4 (4–6) | 5, 6, 7 | el hongo en marzo; Hernán Duque atribuyó a la humedad (capa con su contenido); quince por ciento |
| U5 (7–9) | 8, 9, 10 | la junta pidió; la alcaldía respondió con el presupuesto de julio; insistirá en agosto |
| U6 (10–11) | 11, 12 | el brote parecido (relación con el de marzo, **sin fundirlos**); cuatro meses |
| U7 (12–14) | 13, 14, 15 | revisión del informe; «Ella» y «Su» conservadas como duda |

### Reserva B (5 unidades, 15 ítems)

| Unidad | Ítems | Qué se recuperó |
|---|---|---|
| U1 (1–3) | 1, 2, 3 | pintado en 1962; lo encargó la asociación; dieciocho metros en la capa «según» |
| U2 (4–6) | 4, 5, 6 | humedad en 1998; Inés Vargas atribuyó a una filtración antigua; la asociación decidió no intervenir |
| U3 (7–10) | 7, 8, 9, 10 | campaña de 2020; la mitad de lo previsto; pidieron al distrito; el distrito respondería en marzo |
| U4 (11–12) | 11, 12 | la obra anterior se perdió en 1975; la pérdida duró décadas sin registro |
| U5 (13–15) | 13, 14, 15 | revisión de fotografías; el boceto de 1961; la publicación, con las dos dudas |

**Ninguna importación indebida.** Los cuatro controles «no debe importarse» se
cumplieron: la unidad del hongo no trajo 1998, las once familias ni las ferias; la
del brote no trajo las ciento cuarenta colmenas; la de la humedad no trajo 1962 ni
los dieciocho metros; la de la pérdida no trajo el encargo. Tampoco hubo respaldos
no verificables: 0 en las 12 fichas.

**Un defecto de mis expectativas, no del prompt:** el ítem 11 de la reserva B decía
que «del mismo autor» quedaba sin resolver. v9 lo resolvió como relación —«el autor
del mural del mercado viejo»—, que es lo que el prompt manda hacer cuando el texto
no da un nombre («la falta de nombre no vuelve irresoluble una referencia»). Se
cuenta como recuperado y la expectativa queda corregida aquí.

## Fidelidad · 70/70 = 100 %

Ítems producidos (determinaciones, capas, acciones y relaciones; las marcas van
dentro de su determinación): 34 en la reserva A y 36 en la B. Todos con respaldo
literal en la unidad o en el respaldo de una referencia recibida, ninguno fuera del
foco, ninguno inventado.

Ruido menor, que no es error: determinaciones vacías que repiten el nombre
(«la presidenta · rol = presidenta», «una filtración antigua · antigüedad =
antigua», «obra anterior · orden = anterior»).

## Las dos medidas

| Medida | Resultado | Umbral |
|---|---|---|
| Recuperación fiel del contenido esperado | 30/30 = **100 %** | ≥ 90 % |
| Contenido producido fiel y del foco | 70/70 = **100 %** | ≥ 90 % |

Las dos se alcanzan, y se mantienen al rehacer la cuenta con ítems atómicos (abajo).
Con la verificación mecánica sin problemas (0 respaldos no verificables), la entrada
(b) queda como **base de trabajo provisional** del paso 2.

## Segunda cuenta (06-10): verificación con la regla atómica

Después de la revisión de Astra se rehízo la cuenta de desarrollo separando contenido
de identidad externa. Los 30 ítems de esta reserva **ya estaban escritos así**, uno
por afirmación, y se revisaron uno a uno contra los crudos: siguen **30/30**, y los
**70 ítems producidos** siguen fieles y del foco.

Dos cosas que conviene no confundir:

- El 100 % de aquí **no contradice** el 85,1 % de desarrollo: es un conjunto más
  pequeño, con las referencias completas —todas las identidades externas venían
  dadas— y escrito por quien diseñó el candidato.
- Lo que sí se sostiene es que, **con las referencias completas, la entrada (b)
  recupera todo lo esperado en estos dos documentos sin importar nada ajeno**.
