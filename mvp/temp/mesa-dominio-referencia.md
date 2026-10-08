# Referencia fijada antes de ejecutar la mesa de dominio

Preparada el 5-10-2026. **Se abre al cotejar el recorrido.** Estos resultados
esperados no son resultados observados. Se acepta una presentación equivalente
que cumpla las obligaciones del plan.

## 1. Matriz de resultados esperados

| Caso | Unidades necesarias | Contexto adicional admitido | Campo de datos con las unidades necesarias | Posiciones sostenidas y rutas | Desenlace |
|---|---|---|---|---|---|
| T1 | M1:U1 | Ninguno. | M1:D1, M1:D2, M1:D3 | 42 plazas, según M1, con M1:D1. | Cerrada respecto de lo que dice el parte. |
| T2 | B1:U1 | Ninguno. | B1:D1, B1:D2 | 88 plazas, según B1, con B1:D1. | Cerrada respecto de lo que dice el parte. |
| T3 | M1:U1, M2:U1 | Ninguno. | M1:D1, M1:D2, M1:D3, M2:D1 | 42 por M1:D1 y 47 por M2:D1; conflicto entre ambos. | En conflicto. |
| T4 | M1:U1 | Ninguno. | M1:D1, M1:D2, M1:D3 | 12 plazas sin reservar, según M1; M1:D1, M1:D2 y operación OP1. | Cerrada respecto del parte y del cálculo. |
| T5 | M1:U1, M3:U1 | M2:U1, si se declara como contexto del refugio identificado. | M1:D1, M1:D2, M1:D3, M3:D1 | Ni «es Peña Clara» ni «es otro refugio» tienen ruta que lo establezca. | Identidad no establecida. |
| T6 | Ninguna unidad determina el año. | M1:U1 y M2:U1, como contexto del caso; se acepta campo vacío o con una o ambas. | Según el contexto elegido: vacío o datos de esas unidades. | Ningún año tiene una ruta documental admitida. | Año no establecido. |

Las unidades de contexto opcional aportan todos sus datos preparados al
campo. En T5 y T6 esos datos adicionales permanecen mudos respecto de la
posición preguntada. M1:U2, sobre la senda, no es pertinente para ninguna de
las seis consultas.

## 2. Evidencia y efecto, por consulta

### T1 · MONTAÑA, según el parte

La referencia documental es M1:U1. M1:S1 identifica Peña Clara y la noche;
M1:S2 establece 42 plazas habilitadas. M1:D2 y M1:D3 entran con la unidad,
pero no sostienen el número de plazas habilitadas.

- **A(Q) antes:** ningún número sostenido para esta pregunta.
- **A(Q) después:** 42 plazas gana sostén documental, con procedencia M1.
- **Respuesta suficiente:** «Según el parte de Peña Clara, había 42 plazas
  habilitadas para pernoctar la noche del 27-9-2026».
- **Falla:** contestar 60 sillas, 88 plazas o introducir el conflicto de T3
  como si T1 hubiera pedido resolver ambos recuentos.

### T2 · RIBERA, misma pregunta

B1:S1 identifica Puerto Azul y la noche; B1:S2 establece 88 plazas.
B1:D2, el año 1998, entra con la unidad y queda mudo.

- **A(Q) antes:** ningún número sostenido.
- **A(Q) después:** 88 plazas gana sostén por B1:D1.
- **Respuesta suficiente:** «Según el parte de Puerto Azul, había 88 plazas
  habilitadas para pernoctar la noche del 27-9-2026».
- **Falla:** reutilizar Peña Clara o su cifra por la coincidencia «el refugio».

### T3 · Mismo caso acreditado, recuentos incompatibles

M2:S1 vincula explícitamente el caso y la noche de M2 con M1. Junto con
M1:S1 permite tratar ambos recuentos como relativos al mismo refugio y a la
noche del 27-9-2026. Los respaldos de las cifras son M1:S2 y M2:S2. M2:S3
no establece una corrección ni una sustitución.

- **A(Q) antes:** ninguna posición sostenida por el material declarado.
- **A(Q) después:** 42 y 47 tienen sus respectivas rutas documentales y se
  registra el conflicto `[M1:D1, M2:D1]`. No se dispone una cifra única.
- **Respuesta suficiente:** «El parte registra 42 plazas y el control 47,
  para el mismo refugio y la misma noche. El control dice que no sustituye
  el parte; estos documentos dejan el recuento en conflicto».
- **Falla:** fusionar por compartir dominio sin citar la correspondencia;
  elegir 47 por la radicación posterior; tratar las dos cifras como
  referidas a noches o aspectos distintos.

Se conservan los ids locales M1:C1 y M2:C1. La correspondencia se acredita
en este recorrido con M2:S1 y M1:S1; no requiere borrar uno de ellos ni
construir un registro de identidad para todo el corpus.

### T4 · Un derivado con contexto y entradas recuperables

M1:S3 remite a las plazas habilitadas de S2 y a la noche del parte. OP1 es
la operación de mesa `42 - 30 = 12`, con entradas M1:D1 y M1:D2.

- **A(Q) antes:** ningún número de plazas sin reservar sostenido.
- **A(Q) después:** 12 plazas gana sostén por esas dos entradas y OP1.
- **Respuesta suficiente:** «Según el parte, había 12 plazas sin reservar
  esa noche: 42 habilitadas menos 30 reservadas».
- **Falla:** restar 30 de las 60 sillas; emplear 47 del control para una
  pregunta que pide el resultado según el parte; llamar «desocupadas» a las
  plazas sin reservar sin una premisa que establezca esa equivalencia.

**Registro derivado mínimo, en papel:**

| Elemento | Contenido esperado |
|---|---|
| Identificador de ensayo | DD-mesa-1; no es un id incorporado al corpus real. |
| Pregunta | T4, con su texto, `dominio_consulta: MONTAÑA` y R de la mesa. |
| Determinación | M1:C1, refugio Peña Clara · plazas sin reservar · 12 plazas. |
| Condiciones | Noche del 27-9-2026; plazas habilitadas para pernoctar; resultado según el parte M1. |
| Entrada 1 | M1:D1 = 42 plazas; respaldo M1:S1–S2; documento M1, radicación 2-10-2026. |
| Entrada 2 | M1:D2 = 30 plazas; respaldo M1:S1–S3; documento M1, radicación 2-10-2026. |
| Operación | OP1; cálculo en papel; expresión `42 - 30`; resultado 12. |
| Fecha del registro de ensayo | La fecha real en que se llena el recorrido. |
| Juicio de Jev | No ejecutado. |
| Estado | Candidato en papel; no radicado en el corpus real. |

M1:D3 queda en el campo y no en las entradas del cálculo. Conservar el dominio
de consulta documenta el origen; aquí no se decide la pertenencia ni la
reutilización del derivado en otros dominios.

### T5 · Referencia sin resolver

M3:S1 establece goteras para un refugio no identificado. M3:S2 no aporta
nombre ni ubicación. La fecha compartida y la pertenencia a MONTAÑA no
permiten decidir la identidad con Peña Clara. M2:S1 vincula M2 con M1,
pero no vincula M3 con ninguno.

- **A(Q) antes y después:** tanto «es Peña Clara» como «es otro refugio»
  permanecen abiertas, sin una ruta que establezca una de ellas. No se
  atribuye un cambio de estado a esta falta de identificación.
- **Respuesta suficiente:** «La nota M3 no permite establecer si habla de
  Peña Clara. Hace falta una identificación del refugio o una
  correspondencia documentada con M1».
- **Falla:** unir M3:C1 a M1:C1 por la palabra «refugio», por la noche o por
  el dominio; afirmar que son distintos porque falta nombre.

Los datos del campo pueden servir para examinar la referencia; ninguno
determina la identidad preguntada. La evidencia de la brecha se conserva
sin convertirla en una ruta que sostenga «sí» o «no».

### T6 · Falta el año dentro del alcance

El inventario completo de MONTAÑA se puede recorrer en esta mesa. M1 y M2
no registran la inauguración de Peña Clara; M3 tampoco registra un año de
inauguración. B1 sí tiene 1998, pero es otro documento, de otro dominio y
sobre otro refugio.

- **A(Q) antes y después:** ningún año gana sostén ni se excluyen años por
  estos datos; no hay cambio informativo que determine el año.
- **Respuesta suficiente:** «Los documentos de MONTAÑA no establecen en qué
  año se inauguró Peña Clara».
- **Brecha concreta:** una determinación de inauguración referida a Peña
  Clara, con respaldo documental admitido.
- **Falla:** contestar 1998; considerar la radicación como inauguración;
  declarar que el refugio nunca se inauguró.

Para evaluar la ausencia se registra que se revisó el inventario de
MONTAÑA. Las unidades examinadas para comprobar esa ausencia no tienen que
convertirse todas en campo pertinente. Se aceptan las variantes de contexto
de la matriz, siempre que no se invente una ruta hacia un año.

## 3. Discriminadores del recorrido

La explicación debe permitir contestar estos seis controles:

1. ¿Por qué T1 y T2 tienen respuestas diferentes con el mismo texto de Q?
2. ¿Qué pasajes permiten comparar 42 y 47 en T3?
3. ¿Por qué la radicación posterior de M2 no resuelve T3?
4. ¿Por qué las 60 sillas están en el campo de T4 y fuera de su operación?
5. ¿Qué permite reidentificar M2 y qué falta para reidentificar M3?
6. ¿Por qué 1998 no puede sostener la respuesta de T6?

Si una explicación no puede señalar la evidencia o la regla pertinente, el
cotejo registra el fallo o la imposibilidad de evaluarlo. No se sustituye por
un grado de confianza ni por coincidencia de redacción.
