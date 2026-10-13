# Evaluación de las cuatro consultas de la base viva (12-10-2026)

**Qué es.** La evidencia para juzgar las cuatro consultas que corrieron en la base viva, contra la
vara de `mvp/diseño-mvp.md` §8. **El juicio es de Frat y se escribe acá**: no hay tabla de
evaluaciones, la evaluación es este documento. Todo lo que sigue sale **literal** de la base o del
documento radicado; nada se parafrasea.

**La vara** (§8, literal): la respuesta se sostiene en lo que el documento establece; lo que no se
puede establecer se dice con precisión; **no cuenta acertar por casualidad ni citar texto que no
sostiene la respuesta**; se distingue «no está en los datos extraídos» de «el documento no lo dice»;
las **unidades examinadas** quedan registradas (`consulta_casos`) y se distinguen del campo; no
interviene Jev.

**La referencia.** `batería_sol_respuestas.md`, escrita **a ciegas de las extracciones**. Su pregunta
1 es la de `q1`, `q3` y `q4`; las preguntas 2 a 5 **no corrieron** en la base viva. Las cuatro
preguntas radicadas quedaron con `fuente = 'tecleada'` en `preguntas`, incluidas las tres que
coinciden con la batería.

| consulta | corrida | modelo | esfuerzo | turnos | llamadas | tokens (entrada/salida) | segundos | casos leídos |
|---|---|---|---|---|---|---|---|---|
| `q1` | `C000005` | gpt-6-luna | low | 2 | 1 | 1962 / 118 | 4,7 | `C000001:U2` |
| `q2` | `C000006` | gpt-6-luna | low | 1 | **0** | **100** / 20 | 1,5 | **ninguno** |
| `q3` | `C000007` | gpt-6-luna | low | 2 | 1 | 1962 / 120 | 4,8 | `C000001:U2` |
| `q4` | `C000008` | deepseek-flash | low | 2 | 2 | 3092 / 360 | 2,9 | `C000001:U1`, `C000001:U2` |

Las cuatro: `prompt_id = ORQ`, `prompt_version = 1`, `dominio = GENERAL`,
`documentos = aviacion,sol`, `estado = exitoso`, `desenlace = respondida`.

---

## Las unidades que se leyeron (literal)

### `C000001:U1` · «El Sol como fuente de energía y sus características»

| oración | tramo | texto |
|---|---|---|
| 1 | 26–80 | El Sol es la principal fuente de energía de la Tierra. |
| 2 | 81–204 | Situado a unos 150 millones de kilómetros de nuestro planeta, tiene aproximadamente 1,4 millones de kilómetros de diámetro. |
| 3 | 205–282 | Aunque está muy lejos, su luz y su calor hacen posible la vida que conocemos. |

| dato | aspecto | valor | unidad_valor |
|---|---|---|---|
| `C000003:U1:D1` | importancia del Sol como fuente de energía de la Tierra | la principal | — |
| `C000003:U1:D2` | distancia del Sol a la Tierra | unos 150 millones | kilómetros |
| `C000003:U1:D3` | diámetro del Sol | aproximadamente 1,4 millones | kilómetros |
| `C000003:U1:D4` | efectos de la luz y el calor del Sol que hacen posible la vida conocida | la luz y el calor del Sol | — |

### `C000001:U2` · «Producción de energía y temperatura del Sol»

| oración | tramo | texto |
|---|---|---|
| 1 | 284–426 | Su energía se produce en el núcleo, donde la temperatura alcanza unos 15 millones de °C y la presión ronda los 250.000 millones de atmósferas. |
| 2 | 427–503 | Allí, la fusión une núcleos de hidrógeno para formar helio y libera energía. |
| 3 | 504–565 | La superficie visible es mucho menos caliente: unos 5.500 °C. |

| dato | aspecto | valor | unidad_valor |
|---|---|---|---|
| `C000003:U2:D1` | lugar de producción de la energía del Sol | el núcleo | — |
| `C000003:U2:D2` | temperatura del núcleo del Sol | unos 15 millones | °C |
| `C000003:U2:D3` | presión en el núcleo del Sol | ronda los 250.000 millones | atmósferas |
| `C000003:U2:D4` | proceso que produce energía en el núcleo del Sol | la fusión une núcleos de hidrógeno para formar helio y libera energía | — |
| `C000003:U2:D5` | temperatura de la superficie visible del Sol | unos 5.500 | °C |

**Lo que el documento dice sobre luz y calor** (las dos únicas oraciones que los nombran): «Aunque
está muy lejos, su luz y su calor hacen posible la vida que conocemos» (`U1`, oración 3) y «La
superficie visible es mucho menos caliente: unos 5.500 °C» (`U2`, oración 3). **El documento no dice
que la energía del núcleo «se manifieste como luz y calor en la superficie».**

---

## `q1` · `C000005` · gpt-6-luna `low`

**Pregunta** (`consultas.pregunta_texto`): «Un estudiante afirma que el Sol produce su energía en la
superficie visible, a unos 5.500 °C. ¿Cómo corregirías esa explicación indicando el lugar, el proceso
y las condiciones de temperatura y presión correspondientes?»

**Lo que leyó** (`consulta_casos`): `C000001:U2`. **Operación** (`consulta_llamadas`): turno 1,
orden 1, `obtener_datos_del_caso`, `ok = 1`.

**Respuesta** (`consultas.respuesta`): «El Sol produce su energía en el núcleo, no en la superficie
visible. Allí, a unos 15 millones de °C y una presión de alrededor de 250.000 millones de atmósferas,
la fusión une núcleos de hidrógeno para formar helio y libera energía. Los aproximadamente 5.500 °C
corresponden a la superficie visible.»

**Referencia** (batería, pregunta 1): «La energía se produce en el núcleo, donde la fusión une
núcleos de hidrógeno para formar helio y libera energía. Allí la temperatura alcanza unos 15 millones
de °C y la presión ronda los 250.000 millones de atmósferas. Los 5.500 °C corresponden a la
superficie visible.»

**Señales para el juicio:** el lugar, el proceso, la temperatura y la presión que responde están en
los datos de `U2` (`D1`, `D4`, `D2`, `D3`), y los 5.500 °C en `D5`; la unidad que leyó es la que
contiene todo lo que respondió. No cita texto del documento.

**Veredicto:**

---

## `q3` · `C000007` · gpt-6-luna `low`

**Pregunta**: la misma de `q1`. **Lo que leyó**: `C000001:U2`. **Operación**: turno 1, orden 1,
`obtener_datos_del_caso`, `ok = 1`.

**Respuesta**: «El Sol produce su energía en el núcleo, no en la superficie visible. Allí, la fusión
une núcleos de hidrógeno para formar helio y libera energía. El núcleo alcanza unos 15 millones de °C
y una presión de alrededor de 250.000 millones de atmósferas. Los 5.500 °C corresponden
aproximadamente a la superficie visible.»

**Señales para el juicio:** mismo sostén que `q1`; cambia el orden de la respuesta, no lo que dice.

**Veredicto:**

---

## `q4` · `C000008` · deepseek-flash `low`

**Pregunta**: la misma de `q1`. **Lo que leyó**: `C000001:U1` y `C000001:U2`. **Operación**: turno 1,
órdenes 1 y 2, `obtener_datos_del_caso`, `ok = 1` las dos.

**Respuesta**: «La afirmación es incorrecta: los 5.500 °C corresponden a la temperatura de la
superficie visible del Sol, pero ahí no se produce la energía. La energía solar se genera en el
núcleo, donde la temperatura ronda los 15 millones de °C y la presión alcanza unos 250.000 millones de
atmósferas. En esas condiciones tiene lugar la fusión nuclear, que une núcleos de hidrógeno para
formar helio y libera energía. Esa energía producida en el núcleo es la que luego se manifiesta como
luz y calor en la superficie.»

**Señales para el juicio:** el sostén es `U2` (`D1`, `D2`, `D3`, `D4`, `D5`); **`U1` no sostiene nada
de lo respondido** (sus datos son la importancia, la distancia, el diámetro y los efectos de la luz y
el calor). El cierre —«esa energía… se manifiesta como luz y calor en la superficie»— **no está en el
documento** (arriba, las dos únicas oraciones que nombran luz y calor). Fue el único que leyó dos
casos, y el único con `cache_hit` distinto de cero (1280) y pensamiento declarado (123 tokens).

**Veredicto:**

---

## `q2` · `C000006` · gpt-6-luna `low` · tecleada

**Pregunta** (`consultas.pregunta_texto`): «¿Dónde se produce la energía del Sol?»

**Lo que leyó** (`consulta_casos`): **ningún caso**. **Operación** (`consulta_llamadas`): **ninguna
llamada**. Un turno.

**Respuesta**: «En el núcleo, a 15 millones de °C.»

**Referencia**: no está en la batería (pregunta tecleada).

**Señales para el juicio:** el contenido coincide con `U2` (`D1` y `D2`), pero **no leyó nada**: el
prompt no lleva el texto del documento, solo los nombres de los casos, así que la respuesta no pudo
salir del corpus. Es el caso de la vara «no cuenta acertar por casualidad». Aparte, el consumo de
esta corrida no cuadra con las otras: **100 tokens de entrada** contra 1.962 de `q1` y `q3`, con 1,5 s
y `terminado` en el mismo segundo que `iniciado` (el diseño lo deja abierto en §9: o el `usage` de la
familia `responses` declara solo lo nuevo, o el prompt salió casi vacío).

**Veredicto:**

---

## Lo que la base no registra

- **De dónde salió cada respuesta**: el sostén es `consulta_casos`, y en `q2` está vacío. El registro
  no distingue «entregó» de «se sostiene» (`mvp/diseño-mvp.md` §7.9).
- **Qué tanda de DATOS se leyó**: los casos dicen la UT (`C000001:U2`), no la tanda; se deriva por
  orden de tokens (§9).
