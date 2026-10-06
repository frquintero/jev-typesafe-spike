# Evaluación · doc4 y doc5 con el candidato congelado v9 · 5-10-2026

Candidato: `prompt_v9.md`, **sin ajustar durante la evaluación**.
Criterios fijados antes de correr: `criterios_doc4-doc5.md`.
Textos nuevos, ninguno usado antes: `doc4.md` (nota de servicio) y `doc5.md`
(divulgación histórica). Una réplica por texto, Muse Code, esfuerzo `high`.

## Resumen

| | doc4 | doc5 |
|---|---|---|
| Sesión | `f410bd31-910f-4750-ab81-0866a3e27d84` | `76eb8671-20be-4068-8040-851bdb4071cf` |
| Tiempo | 100 s | 121 s |
| Tokens: entrada / salida / razonamiento | 32 245 / 14 296 / 12 807 | 32 232 / 17 537 / 16 251 |
| Unidades | 6 | 5 |
| Referencias registradas | 11 | 8 |
| Verificación mecánica | sin problemas | sin problemas |
| Cobertura | 17/17, sin huecos ni solapes | 17/17, sin huecos ni solapes |

## Fidelidad (requisito)

**doc5 · limpia en los cuatro criterios.**

- `[3] «según los planos de la época»` → fuente, no registrada. ✅
- `[7] «el servicio»` → «el servicio del tranvía». ✅
- `[15] «Ella»` → `null` + duda: «No se establece si fue la historiadora o la
  archivista». ✅ Conserva las dos.
- `[16] «Su hallazgo»` → `null` + duda: «No se establece de quién fue el
  hallazgo, pues depende de Ella en [15]: la historiadora o la archivista».
  ✅ Conserva las dos y **no** declara que sean distintas.
- Las internas (`[9] «La compra»`, `[11] «esa promesa»`, `[13] «Su retiro»`) no
  se registraron. ✅

**doc4 · un fallo real y tres casos no evaluables.**

- `[11] «un corte similar»` → «el corte de agua en el barrio San Jorge», sin
  `null`. ✅ Conserva la identidad relativa.
- `[3] «según la empresa»` → fuente, no registrada. ✅
- `[17] «la solicitud»` → **no registrada**, y sí es externa: remite a la
  petición de [8], que quedó en otra unidad. ❌ Fallo de fidelidad por omisión.
- `[14] «Ella»`, `[15] «Su reclamo»`, `[16] «Su decisión»` → **no evaluables con
  los criterios escritos**. Los tres quedaron dentro de la unidad
  `[13,14,15,16,17]`, así que son referencias internas y la regla manda no
  registrarlas. Mis expectativas suponían que la partición los separaría, y la
  partición no estaba fijada.

**Clase grave: vacía en los dos textos.** No apareció ninguna identidad ni
diferencia inventada, ni propiedades o relaciones que el texto no establezca.

## Economía (preferencia)

- **Redundancia, sí.** En doc4, `[13] «la respuesta de la empresa»` → «la
  respuesta de la empresa de que la fecha ya estaba contratada» (63 caracteres,
  repite [9]). En doc5, `[8] «la red»` → «la red del tranvía, que llegó a tener
  veintiocho kilómetros de vías» (67 caracteres, arrastra la cifra de [3]).
  Las dos son **redundancia, no error**: nada de eso es falso.
- **Referencias que quizá sobran.** doc4 registra 11: tres de ellas
  (`«la noche anterior»`, `«la fecha»`, `«del sector»`) no parecen necesarias
  para interpretar la unidad.
- **Sin comparación entre versiones.** No extraje los tokens de las corridas v7
  y v8 sobre doc2/doc3, así que el tiempo y el razonamiento de v9 no se pueden
  contrastar aquí. Lo de arriba es solo el candidato congelado.

## Dos fallos de los criterios, no del prompt

1. **Escribí expectativas sin fijar la partición.** Tres casos de doc4
   dependían de que ciertas oraciones cayeran en unidades distintas, y no lo
   fijé. Los criterios deben decir, o bien la partición esperada, o bien que la
   expectativa solo aplica si el antecedente queda fuera.
2. **La incertidumbre tiene ahora dos sitios.** El criterio decía «ambigua →
   `null`», pero en doc5 `[14] «del taller»` salió con referente no nulo:
   «uno de los talleres incluidos en la compra, sin establecer cuál». La
   indecisión viaja en el `referente`, no en la `duda`. Para evaluar habrá que
   leer los dos campos, no solo `duda`.

## Lo que sigue sin probarse

- **La referencia hacia adelante.** En doc4 se plantó en `[16] «Su decisión»`
  con el referente en `[17]`, pero las dos oraciones cayeron en la misma unidad
  y la regla manda no registrarla. El caso sigue sin ejercitarse.
- **Estabilidad.** Una réplica por texto; nada de esto dice si el resultado se
  repite.
