# Materiales de la mesa de dominio

Fecha de preparación: 5-10-2026. **Corpus sintético de desarrollo, preparado
a mano.** No es una extracción producida por un modelo.

## 1. Pertenencia documental dada

| Dominio | Documentos |
|---|---|
| MONTAÑA | M1, M2, M3 |
| RIBERA | B1 |

La persona que consulta elige uno de estos dominios. Que varios documentos
pertenezcan a MONTAÑA no establece que todas sus menciones de «el refugio»
sean el mismo caso. Los ids de caso son locales a cada documento.

La ficha de cada documento se conserva completa al incorporarlo. Las unidades
pertinentes se seleccionan cuando llega una consulta.

## 2. Documentos completos

### M1 · Parte del refugio

Dominio: MONTAÑA. Radicación: 2-10-2026.

> [M1:S1] Parte del refugio Peña Clara, en el valle del Pinar, referido a la noche del 27 de septiembre de 2026.
>
> [M1:S2] Para esa noche, el refugio tenía 42 plazas habilitadas para pernoctar.
>
> [M1:S3] De esas plazas, 30 estaban reservadas.
>
> [M1:S4] Esa noche, el comedor del refugio tenía 60 sillas.
>
> [M1:S5] La senda del Robledal mide 3 kilómetros.

### M2 · Control de plazas

Dominio: MONTAÑA. Radicación: 4-10-2026.

> [M2:S1] Este control corresponde al mismo refugio y a la misma noche que el parte M1.
>
> [M2:S2] Cuenta 47 plazas habilitadas para pernoctar.
>
> [M2:S3] Este control no corrige ni sustituye el parte M1.

La fecha de radicación indica cuándo se incorporó el control. La relación
con el caso y la noche de M1 está declarada en S1; no se deduce de esa fecha.

### M3 · Nota sin identificación del refugio

Dominio: MONTAÑA. Radicación: 5-10-2026.

> [M3:S1] El refugio tenía goteras la noche del 27 de septiembre de 2026.
>
> [M3:S2] Esta nota no indica el nombre del refugio ni su ubicación.

### B1 · Parte del refugio

Dominio: RIBERA. Radicación: 3-10-2026.

> [B1:S1] Parte del refugio Puerto Azul, en la bahía del Astillero, referido a la noche del 27 de septiembre de 2026.
>
> [B1:S2] Para esa noche, el refugio tenía 88 plazas habilitadas para pernoctar.
>
> [B1:S3] El refugio se inauguró en 1998.

## 3. Unidades dadas antes de preguntar

| Unidad | Núcleo y satélites | Texto completo que entrega |
|---|---|---|
| M1:U1 | Núcleo M1:C1, refugio Peña Clara; satélite M1:C2, su comedor. | M1:S1–S4 |
| M1:U2 | Núcleo M1:C3, senda del Robledal. | M1:S5 |
| M2:U1 | Núcleo M2:C1, refugio al que se refiere el control; contexto documental de la correspondencia y del control. | M2:S1–S3 |
| M3:U1 | Núcleo M3:C1, refugio sin nombre ni ubicación establecidos. | M3:S1–S2 |
| B1:U1 | Núcleo B1:C1, refugio Puerto Azul. | B1:S1–S3 |

Al elegir una unidad se entregan todas esas oraciones y sus datos preparados.
El lector puede dejar datos mudos. Los nombres locales de M2:C1 y M3:C1 no
anticipan una fusión con M1:C1.

## 4. Datos preparados

Estos ocho registros son los que se usan para las rutas de la mesa. Los
textos completos de las unidades conservan el contexto y las declaraciones
documentales adicionales; esta lista no pretende ser una ficha exhaustiva de
siete listas del extractor.

| Id | Unidad | Caso · aspecto · posición | Condiciones | Respaldo de sus componentes |
|---|---|---|---|---|
| M1:D1 | M1:U1 | M1:C1 · plazas habilitadas para pernoctar · 42 plazas | Noche del 27-9-2026. | M1:S1, M1:S2 |
| M1:D2 | M1:U1 | M1:C1 · plazas reservadas entre las habilitadas · 30 plazas | Misma noche y mismo conjunto de plazas que M1:D1. | M1:S1, M1:S2, M1:S3 |
| M1:D3 | M1:U1 | M1:C2 · número de sillas · 60 sillas | Comedor del refugio; noche del 27-9-2026. | M1:S1, M1:S4 |
| M1:D4 | M1:U2 | M1:C3 · longitud · 3 kilómetros | No añade condiciones temporales. | M1:S5 |
| M2:D1 | M2:U1 | M2:C1 · plazas habilitadas para pernoctar · 47 plazas | «al mismo refugio y a la misma noche que el parte M1». | M2:S1, M2:S2 |
| M3:D1 | M3:U1 | M3:C1 · presencia de goteras · sí | Noche del 27-9-2026; refugio no identificado. | M3:S1, M3:S2 |
| B1:D1 | B1:U1 | B1:C1 · plazas habilitadas para pernoctar · 88 plazas | Noche del 27-9-2026. | B1:S1, B1:S2 |
| B1:D2 | B1:U1 | B1:C1 · año de inauguración · 1998 | No añade condiciones. | B1:S1, B1:S3 |

Cada dato conserva el documento y su fecha de radicación declarados en §2.
Las citas se recuperan por los ids de oración, no por una paráfrasis.

## 5. Declaraciones que pueden usarse como evidencia

- M2:S1 declara la correspondencia del refugio y la noche con M1. Durante la
  consulta permite acreditar esa reidentificación y la comparabilidad de los
  dos recuentos, conservando M1:C1 y M2:C1 como referencias documentales.
- M2:S3 declara que el control no corrige ni sustituye M1. No hay en este
  paquete una regla que otorgue prioridad al control por su radicación.
- M3:S2 deja sin establecer el nombre y la ubicación de su refugio. No
  establece que sea distinto de Peña Clara: faltan criterios para decidir.

Estas declaraciones forman parte del material literal. No son decisiones
globales de identidad guardadas por el diseñador.

## 6. Operación admitida

Para T4 se admite restar el número de plazas reservadas del total de plazas
habilitadas, bajo las mismas condiciones. Registrar las entradas por id y
valor, la expresión y el resultado. El comedor y la senda no aportan entradas
a esa operación. El cálculo de la mesa se hace en papel; no se atribuye a una
herramienta ejecutada ni a una versión de software.
