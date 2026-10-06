# Paso 2 · comparación de entradas con las unidades de v9 · 06-10-2026

Especificación escrita antes de correr. Candidato: `prompt_ficha_contexto.md`
(derivado de `ficha_v1`, que no se toca).

## Para qué

Elegir con qué entrada se extraen los datos de cada unidad temática y, si la
elegida alcanza la vara, cerrar la integración. No se abre una cadena de
versiones: lo que quede por mejorar se registra.

## Acuerdos que respeta (cierre de la ronda de discusión, 06-10)

- **v9 y `ficha_v1` congelados.** El candidato distingue unidad de extracción y
  contexto de apoyo y conserva el esquema de salida (siete listas). `ficha_v2`
  queda aparte (F6, evaluación pendiente).
- **Se reutilizan las piezas del ejecutor por unidad** (`ficha_doc.verificar` y
  `numerar_oraciones`, las mismas que usa
  `nblm-grafo-semantico/ficha_unidad_deepseek.py`), no su script: ese vive atado a
  `unidades/docs` y llena un solo marcador, sin `{{CONTEXTO}}`. El corredor de la
  comparación conserva la numeración original, guarda las referencias y comprueba
  las citas contra el material efectivamente enviado. Una cita literal válida no
  demuestra que su uso sea correcto.
- **El contexto aclara, no amplía el asunto.** Puede aportar casos necesarios
  para representar lo dicho (identificar el mural) sin importar sus otras
  determinaciones (los dieciocho metros). Las referencias irresueltas conservan su
  duda.
- **Documento completo con foco no equivale a FU2.** FU2 fue una sola extracción
  del documento (69,3 s); repetirlo como contexto por unidad son N llamadas y su
  tiempo se mide, no se supone.
- **`inferido` se localiza donde hubo reconstrucción**, no se marca en bloque por
  usar una referencia: resolver de quién se habla y deducir un contenido nuevo son
  operaciones distintas.

## Material

Unidades congeladas de v9, sin volver a correr el paso 1:

| Texto | Unidades | Referencias | Dudas (`referente` null) |
|---|---|---|---|
| `mvp/pruebas/salida_prueba8-v9-doc4.md` | 6 | 11 | 0 |
| `mvp/pruebas/salida_prueba9-v9-doc5.md` | 5 | 8 | 2 |

Cubre las tres cosas que hay que conservar (identidad, condición, sostén), las
referencias irresueltas y el caso que v9 omitió. **No se corre `doc1` con v9:** su
caso de pertenencia estuvo enseñado como ejemplo del candidato —hoy el ejemplo del
prompt es inventado— y, sobre todo, `doc1` no tiene partición de v9 congelada; el
caso de contexto que no debe importarse va nuevo en la reserva.

**Reserva:** `reserva_a.md` y `reserva_b.md`, con las expectativas en
`expectativas_reserva.md`, fijadas antes de cualquier llamada. Las escribió el mismo
que diseñó el candidato: **no son validación independiente**.

## Las tres entradas

Un solo prompt (`prompt_ficha_contexto.md`) y un solo modelo
(`deepseek-flash`); la única variable es el bloque `CONTEXTO`.

- **(a) unidad sola**: las oraciones de la unidad, `CONTEXTO` vacío (control).
- **(b) unidad + referencias**: las oraciones de la unidad y, en `CONTEXTO`, las
  referencias de v9 con sus respaldos (el candidato).
- **(c) unidad + documento completo**: las oraciones de la unidad y, en
  `CONTEXTO`, el documento numerado entero (las oraciones de la unidad van
  repetidas). Es la asimetría de ENC4 —extraer solo del foco, usar el resto para
  interpretar— con los nombres del candidato, y deja la comparación en una sola
  variable. El literal de ENC4 (documento en `TEXTO` y el foco aparte) exigiría un
  segundo prompt, y entonces la comparación mezclaría prompt y contexto.

## Qué se evalúa, por referencia (fijado antes)

Para cada una de las 19 referencias: qué lleva y qué cuenta como conservado
(identidad, condición o marca en el registro correcto, sostén de una capa, duda).
Anexo al final. Expectativa nombrada: `doc4 [17] «la solicitud»`, que v9 no
registró —en (b) no llega el antecedente, en (c) sí—: se anota qué pasa en cada
entrada.

**Qué cuenta como fallo de contenido:** omisión; deformación (identidad o
diferencia inventada, condición metida en el nombre del caso, lo comparado
convertido en el caso comparado); agregado (determinaciones, acciones o marcas que
la unidad no establece, importadas del contexto). Es juicio, y se decide contra las
expectativas, no contra el texto de la cita.

**Verificación mecánica (forma), por entrada:** los literales de la ficha se
comprueban contra el material efectivamente enviado —en (a) la unidad; en (b) la
unidad y los fragmentos de las referencias recibidas; en (c) el documento
completo—. `ficha_doc.verificar` mira solo las oraciones de la unidad
([ficha_doc.py:36](../../unidades/ficha_doc.py:36)) y marcaría `no_literales` las
citas legítimas del contexto, así que el verificador de esta comparación recibe su
corpus por entrada.

**Lo que la verificación no decide:** una cita fuera del material recibido es un
**respaldo no verificable** —se reporta como tal—, no un dato agregado; y una cita
literal puede acompañar un agregado, porque si la determinación corresponde al foco
y si la unidad la establece no lo dice el texto de la cita.

**Costo:** segundos y tokens por unidad y por entrada; total por entrada.

## El código de la comparación

`comparacion.py` (escrito; el modo `seco` verificado, nada corrido todavía):

- Lee la partición congelada de v9 y conserva la numeración original de las
  oraciones en la unidad que envía.
- Arma el bloque `CONTEXTO` de cada entrada: vacío en (a), referencias con su
  respaldo en (b), documento numerado en (c).
- Verifica los literales contra el corpus de la entrada y reporta aparte los
  respaldos no verificables, las citas de fuera de la unidad y las citas de
  oraciones no recibidas; el agregado se decide en la evaluación, no aquí.
- Guarda el crudo con el prompt entero que se envió: sin el material enviado no se
  puede auditar una cita. Idempotente; una réplica nueva lleva un `rN` nuevo.

Reutiliza `numerar_oraciones` y `verificar` del repo y no toca `ficha_v1` ni
`ficha_doc.py`: la verificación con el corpus de cada entrada vive aquí.

## Unidades de contenido

Regla fijada antes de correr, en `expectativas_desarrollo.md` (la misma para la
reserva): un ítem es una determinación, una atribución, una acción o una relación,
cada afirmación contada una sola vez; las condiciones van dentro de su
determinación, una marca solo cuenta si es una posición que no forma ya parte de
una determinación contada, y los casos no se cuentan como contenido (entran en la
identificación y en el control de lo que no debe importarse). Nada de inflar con
campos JSON ni de repetir una afirmación que aparece en dos listas.

## Selección

Con los resultados de desarrollo, primero recuperación y fidelidad. Entre las
entradas que cumplen ambos umbrales gana la de menor tiempo total y, en empate, la
de menor consumo de tokens. Si ninguna cumple, se informa el impedimento y **no se
gastan llamadas en la reserva**. La reserva se prueba con la entrada elegida, sin
tocar el prompt después de ver sus resultados y sin alternativas sucesivas.

## Criterio de cierre

Dos medidas, cada una con su denominador, sobre lo fijado antes:

- **Recuperación ≥ 90 %**: de lo esperado, cuánto se recuperó fielmente. Cuenta
  contra las omisiones.
- **Fidelidad ≥ 90 %**: de lo producido, cuánto es fiel y corresponde al foco.
  Cuenta contra deformaciones y agregados.

Lo esperado incluye las determinaciones, las condiciones y las atribuciones de las
unidades, no solo lo que llevan las referencias. En los textos de desarrollo la
comparación solo elige la entrada; las dos medidas se aplican en la reserva breve,
con el paso 1 (v9) corrido sobre ella —una tarea de Muse, con autorización de
Frat— y con un caso de contexto nuevo que **no** deba importarse. Si alcanza las
dos medidas, la integración se cierra; si no, se registra qué falló y dónde.

## Fuera de alcance

`ficha_v2`; reabrir v9; cambiar el esquema de salida; la pieza mecánica del
orquestador (va después, según el orden del 06-10).

## Anexo · qué lleva cada referencia

`doc4` (unidad · oración · expresión → referente · lleva)

1. `[7]` `[7]` «La empresa» → «La empresa de acueducto» · identidad.
2. `[7]` `[7]` «los vecinos» → «los vecinos del barrio San Jorge» · identidad.
3. `[7]` `[7]` «la noche anterior» → «la noche anterior al jueves del corte» ·
   condición (no en el nombre del caso).
4. `[8,9,10]` `[8]` «el corte» → «el corte de agua en el barrio San Jorge para el
   jueves» · identidad y marca.
5. `[8,9,10]` `[9]` «La empresa» → «La empresa de acueducto» · identidad.
6. `[8,9,10]` `[9]` «la fecha» → «el jueves, la fecha del corte» · marca.
7. `[11,12]` `[11]` «un corte similar» → «el corte de agua en el barrio San Jorge»
   · identidad relativa: el corte del año pasado **no** es el de este año
   (relación, no fusión).
8. `[11,12]` `[11]` «del sector» → «el barrio San Jorge» · identidad.
9. `[13–17]` `[13]` «de la junta» → «la junta de acción comunal» · identidad.
10. `[13–17]` `[13]` «la respuesta de la empresa» → «…de que la fecha ya estaba
    contratada» · sostén: el contenido de la capa, sin volverse determinación
    propia.
11. `[13–17]` `[17]` «de la empresa» → «la empresa de acueducto» · identidad.

`doc5`

12. `[4–7]` `[4]` «de la compañía» → «una compañía inglesa con capital privado» ·
    identidad.
13. `[4–7]` `[7]` «La ciudad» → «la ciudad del primer tranvía» · identidad.
14. `[4–7]` `[7]` «el servicio» → «el servicio del tranvía» · identidad.
15. `[8–11]` `[8]` «la red» → «…que llegó a tener veintiocho kilómetros de vías» ·
    identidad y marca: la cifra no entra en el nombre del caso.
16. `[12,13,17]` `[12]` «Los últimos tranvías» → «los tranvías de la ciudad…» ·
    identidad.
17. `[14,15,16]` `[14]` «del taller» → «uno de los talleres incluidos en la
    compra, sin establecer cuál» · duda dentro del `referente`.
18. `[14,15,16]` `[15]` «Ella» → null · duda: la historiadora o la archivista, las
    dos conservadas.
19. `[14,15,16]` `[16]` «Su» → null · duda que depende de `[15]`, sin declarar que
    son distintas.
