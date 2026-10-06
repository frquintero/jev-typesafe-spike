# Expectativas de desarrollo · doc4 y doc5 con las unidades de v9 · 06-10-2026

Escritas y guardadas **antes** de las llamadas. Partición congelada de v9:
`salida_prueba8-v9-doc4.md` (6 unidades) y `salida_prueba9-v9-doc5.md` (5 unidades).
Se evalúan las tres entradas (a) unidad sola, (b) unidad con referencias, (c) unidad
con el documento completo, con el mismo prompt (`prompt_ficha_contexto.md`) y el
mismo modelo.

## Cómo se cuentan las unidades de contenido (fijado antes)

- **Ítem esperado**: una afirmación que la unidad establece, contada una sola vez:
  una determinación (caso · aspecto · valor, con sus condiciones), una atribución
  (quién sostiene qué), una acción o una relación. Las condiciones van dentro de su
  determinación y no se cuentan aparte. Una marca se cuenta solo si es una posición
  que no forma ya parte de una determinación contada. Los casos **no** se cuentan
  como contenido: entran en la identificación de las determinaciones y en el
  control de lo que no debe importarse.
- **Ítem producido**: la misma definición, tomada de la ficha de la corrida, una
  sola vez por afirmación: lo que aparece repetido en dos listas cuenta una vez.
- **Recuperado fielmente**: el ítem esperado aparece en la ficha con su identidad y
  su valor correctos, sin agregarle ni quitarle nada.
- **Producido fiel y del foco**: el ítem tiene respaldo literal en la unidad y no
  deforma ni importa contenido ajeno. Se cuenta como agregado si la unidad no lo
  establece.

Total esperado: **42 ítems** (25 en doc4, 17 en doc5), más las 19 expectativas de
referencia, que se evalúan aparte y no se suman a los 42.

## doc4

### U1 · [1, 2, 3] · el corte anunciado, su duración y sus afectados (6 ítems)

1. La empresa de acueducto anunció un corte de agua.
2. El corte es en el barrio San Jorge.
3. El corte es para el jueves.
4. El corte durará catorce horas.
5. Empieza a las seis de la mañana.
6. Afectará a unos tres mil usuarios, **atribuido a la empresa** («según la
   empresa»).

No debe importarse: nada externo (la unidad no tiene referencias).

### U2 · [4, 5, 6] · la causa: la tubería matriz y la cuadrilla (5 ítems)

7. La causa del corte es la reparación de una tubería matriz.
8. La tubería está en la carrera séptima.
9. La tubería tiene cuarenta años.
10. Ya presentó fugas en 2021.
11. La cuadrilla trabajará con dos bombas de achique.

No debe importarse: nada externo.

### U3 · [7] · la petición a los vecinos (2 ítems + 3 referencias)

12. La empresa de acueducto pidió a los vecinos del barrio San Jorge almacenar agua
    (identidades externas: `[1]`).
13. La noche anterior al jueves del corte (condición externa: `[1]`).

Referencias: `«La empresa»`→la empresa de acueducto (identidad); `«los vecinos»`→los
vecinos del barrio San Jorge (identidad); `«la noche anterior»`→la noche anterior al
jueves del corte (condición en el registro correcto, no en el nombre).

No debe importarse: que el corte sea el jueves o el barrio como determinaciones
propias de este subtema; el contexto solo identifica y condiciona.

### U4 · [8, 9, 10] · la petición de la junta y la respuesta (4 ítems + 3 referencias)

14. La junta de acción comunal pidió que el corte no se hiciera en semana de
    exámenes.
15. La empresa respondió que la fecha ya estaba contratada (atribución con su
    contenido; `«la fecha»` se identifica con `[1]`).
16. La fecha es la del corte, el jueves (identidad externa).
17. La junta insistirá en la próxima reunión.

Referencias: `«el corte»`→el corte de agua en el barrio San Jorge para el jueves;
`«La empresa»`→la empresa de acueducto; `«la fecha»`→el jueves, la fecha del corte.

No debe importarse: la duración, los afectados o la causa del corte.

### U5 · [11, 12] · el corte similar y su duración (3 ítems + 2 referencias)

18. El año pasado un corte similar dejó sin servicio a dos colegios.
19. El corte similar **no** es el corte de este año: van unidos por la semejanza.
20. Aquel episodio duró diecinueve horas.

Referencias: `«un corte similar»`→el corte de agua en el barrio San Jorge (identidad
relativa, sin fundir los dos casos); `«del sector»`→el barrio San Jorge.

No debe importarse: que el corte del año pasado sea el mismo acontecimiento que el
de este año.

### U6 · [13, 14, 15, 16, 17] · la revisión y la evaluación de la solicitud (5 ítems + 3 referencias)

21. La personera y la secretaria de la junta revisaron la respuesta de la empresa
    (identidades externas: `[8]`; contenido externo: `[9]`, «que la fecha ya estaba
    contratada»).
22. `Ella` ([14]) pidió que se publicara el cronograma, **sin resolver** si es la
    personera o la secretaria.
23. `Su reclamo` ([15]) quedó registrado en el acta, **sin resolver** de quién.
24. `Su decisión` ([16]) se conocerá el miércoles, **sin resolver** de quién.
25. El gerente de la empresa, Iván Cifuentes, dijo que evaluará **la solicitud**
    (remite a `[8]`; v9 **no** registró esa referencia: es la expectativa nombrada).

Referencias: `«de la junta»`→la junta de acción comunal; `«la respuesta de la
empresa»`→…de que la fecha ya estaba contratada (sostén); `«de la empresa»`→la
empresa de acueducto.

No debe importarse: el contenido de `[9]` como determinación propia de esta unidad
más allá de sostener lo que la unidad establece; las tres dudas deben conservarse,
no resolverse eligiendo una lectura.

## doc5

### U1 · [1, 2, 3] · el inicio del tranvía y la extensión de la red (3 ítems)

26. El primer tranvía de la ciudad empezó a rodar en 1893.
27. Lo operaba una compañía inglesa con capital privado.
28. La red llegó a tener veintiocho kilómetros de vías («según los planos de la
    época» es la fuente, no una referencia).

No debe importarse: nada externo.

### U2 · [4, 5, 6, 7] · el incendio de 1927 (4 ítems + 3 referencias)

29. En 1927 un incendio destruyó las caballerizas de la compañía inglesa
    (identidad externa: `[2]`).
30. El fuego se originó en un depósito de forraje.
31. La compañía no repuso los animales.
32. La ciudad tardó dos años en restablecer el servicio del tranvía (identidades
    externas: `[1]`).

Referencias: `«de la compañía»`→una compañía inglesa con capital privado; `«La
ciudad»`→la ciudad del primer tranvía; `«el servicio»`→el servicio del tranvía.

No debe importarse: la extensión de la red ni el año de inicio como determinaciones
de este subtema.

### U3 · [8, 9, 10, 11] · la compra y la promesa incumplida (4 ítems + 1 referencia)

33. En 1948 la municipalidad compró la red del tranvía (identidad externa: `[3]`).
34. La compra incluyó los talleres y los vehículos que aún servían.
35. El municipio prometió modernizar las líneas.
36. Nunca ejecutó esa promesa.

Referencia: `«la red»`→la red del tranvía, que llegó a tener veintiocho kilómetros
de vías (identidad y marca: la cifra no entra en el nombre del caso).

No debe importarse: los veintiocho kilómetros como determinación propia de esta
unidad.

### U4 · [12, 13, 17] · el retiro y la atribución del cierre (3 ítems + 1 referencia)

37. Los últimos tranvías circularon hasta 1965 (identidad externa: `[1]`).
38. Su retiro coincidió con la ampliación de la avenida central.
39. La historiadora Elvira Sanmiguel atribuyó el cierre a la presión de los
    transportadores (atribución con su contenido).

Referencia: `«Los últimos tranvías»`→los tranvías de la ciudad que empezaron con el
primer tranvía.

No debe importarse: los planos del taller.

### U5 · [14, 15, 16] · los planos del taller y la publicación (3 ítems + 3 referencias)

40. La historiadora y la archivista revisaron los planos del taller
    (identidad externa: `[9]`, con la duda de cuál taller).
41. `Ella` encontró un plano fechado en 1911, **sin resolver** si es la historiadora
    o la archivista.
42. `Su hallazgo` se publicó en la revista municipal, **sin resolver** de quién, y
    sin declarar que las dos sean distintas.

Referencias: `«del taller»`→uno de los talleres incluidos en la compra, sin
establecer cuál (duda en el `referente`); `«Ella»`→sin resolver; `«Su»`→sin
resolver, dependiente de `[15]`.

No debe importarse: la compra o los vehículos como determinaciones de este subtema.

## Las 19 expectativas de referencia

Las del anexo de `especificacion_comparacion.md`, una por una; se evalúan aparte de
los 42 ítems y se informan con ellos.
