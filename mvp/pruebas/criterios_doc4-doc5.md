# Criterios fijados antes de correr · doc4 y doc5 · 5-10-2026

Candidato **congelado**: `prompt_v9.md`. No se ajusta durante esta evaluación.
Textos nuevos: `doc4.md` (nota de servicio, 17 oraciones) y `doc5.md`
(divulgación histórica, 17 oraciones).

## Dos ejes, evaluados por separado

**Fidelidad — requisito.**

1. Cada referencia externa resuelta cita su antecedente con fragmento literal.
2. Las ambiguas quedan `null` y su `duda` enumera las interpretaciones abiertas;
   no afirma que dos menciones sean distintas.
3. Ninguna identidad, diferencia, propiedad o relación que el texto no
   establezca.
4. No se registran las referencias internas al propio grupo ni las fuentes.

**Economía — preferencia.**

5. No repite información innecesaria en el referente.
6. Tiempo y tokens.

## Gravedad

- Descripción larga pero fiel → **redundancia**. No es error.
- Identidad o diferencia inventada → **error de contenido**. Es lo grave.

## Expectativas, escritas antes

### doc4

| Oración | Expresión | Se espera |
|---|---|---|
| [3] | «según la empresa» | fuente: no se registra |
| [5] | «Esa tubería» | interna, si [4] y [5] quedan en el mismo grupo |
| [11] | «un corte similar» | conservar la relación con el corte anunciado, sin `null` |
| [14] | «Ella» | ambigua (personera o secretaria): `null` + duda con las dos |
| [15] | «Su reclamo» | ambigua por depender de [14]: `null` + duda con las dos |
| [16] | «Su decisión» | **hacia adelante**: el referente es el gerente de [17]; debe resolverse |
| [17] | «la solicitud» | externa si [8] queda en otro grupo |

### doc5

| Oración | Expresión | Se espera |
|---|---|---|
| [3] | «según los planos de la época» | fuente: no se registra |
| [7] | «el servicio» | externa: remite a [1] |
| [9] | «La compra» | interna |
| [11] | «esa promesa» y «Nunca ejecutó» | internas: [10] |
| [13] | «Su retiro» | interna: [12] |
| [15] | «Ella» | ambigua (la historiadora o la archivista): `null` + duda |
| [16] | «Su hallazgo» | ambigua encadenada: `null` + duda, sin declarar que las dos menciones son distintas |

## Lo que no se evalúa aquí

- La partición no tiene un esperado fijo: se anota, y solo se marca si funde
  asuntos distintos o parte uno solo. Siete grupos no son por sí solos peor.
- Una sola réplica por texto: esto no mide estabilidad.
