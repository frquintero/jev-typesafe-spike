# Jev como juez: resumen pedagógico

> Resumen de `jev_typesafe_guia_pedagogica_v2.md`, versión 8.2 (23 de septiembre de 2026).
> Las referencias entre corchetes, como [§4.6] o [B-P7], remiten a la guía y a sus anexos.

---

## 0. Antes de empezar

Este resumen sigue el hilo que organiza la guía: el **marco del juez**. Todo lo demás —primitivas, redacción, confianza, límites, método— se ordena alrededor de él.

Conviene tener presentes dos advertencias de la guía:

- **Cuatro niveles de evidencia.** Hay que distinguir lo que dice la documentación oficial de TypeSafe (1), lo que dicen terceros (2), lo que medimos en el spike (3) y lo que inferimos para diseñar (4). En este resumen, cuando algo es oficial se dice; cuando es medición propia, también.
- **Todas las reglas son heurísticas.** Orientan el diseño; no lo reemplazan. Cada aplicación necesita sus propios ajustes y pruebas.

---

## 1. La tesis en una línea

> **Jev sopesa juicios estrechos frente a un expediente y devuelve un grado de soporte tipado; el código compone esos grados, aplica las reglas y decide.**

O, más corto: **Jev sopesa; el sistema decide.**

El verbo importa. Jev no *responde*, no *extrae*, no *dice si algo es verdadero o falso*: **sopesa**. Que el resultado sea tipado y probabilístico no garantiza que el juicio sea el que queríamos someter.

---

## 2. El marco del juez

TypeSafe presenta Jev como un *System One Model*: decisiones rápidas, repetibles y acotadas, sin generar texto. La guía propone entenderlo como un **juez**. El marco tiene cuatro piezas:

| Pieza | En el API | Qué es |
|---|---|---|
| **Expediente** | `state` | El material que la aplicación somete a juicio: un mensaje, un documento, un folleto. Tiene un papel reconocible y se nombra por ese papel. |
| **Juicio** | `instructions` (Noul) o `criteria` (Choice, Score) | Lo que Jev sopesa. |
| **Hechos notorios** | — (van dentro del modelo) | Lo que Jev sabe del mundo y usa sin que el expediente lo pruebe. |
| **Grado de soporte** | `noul` o `probabilities` | Cuánto sostendría Jev el juicio con el expediente a la vista, o cómo reparte su soporte entre varios juicios. |

```text
expediente + juicio  ──►  Jev (con sus hechos notorios)  ──►  grado de soporte  ──►  código
```

**Lo notorio no necesita prueba** (*notoria non egent probatione*). Un juez no pide que el expediente le demuestre que la capital de Australia es Canberra. Jev tampoco: sopesa cada juicio **con el expediente y con lo notorio a la vez**. Buena parte de lo que la guía descubrió se explica desde aquí [§1, §4.6].

**Lo que Jev no es:** un agente autónomo, un buscador, un sustituto de las reglas de negocio, una garantía de coherencia entre juicios, un razonador profundo ni una prueba de que algo es verdadero fuera del expediente.

**Quién consume a Jev: el sistema, no el usuario** [§1]. Lo que Jev devuelve lo lee un programa: TypeSafe habla de *«structured decisions that software can use directly»*. Por eso, **usado correctamente, Jev es transparente para el usuario**: la persona encuentra el sistema, no al juez. El nombre lo sugiere: en Kahneman, el Sistema 1 trabaja por debajo y alimenta al Sistema 2.

Meter a Jev en el bucle del usuario es un error de diseño: el grado se vuelve una afirmación («0,86» leído como «86 % verdadero»), la confianza se lee como acierto y la decisión queda sin dueño. Pero **transparente para el usuario no es invisible para el operador**: quien diseña, opera o audita debe ver grados, repartos, versiones y crudos.

**Vocabulario.** Donde el API dice *question* o *answer*, el marco dice **juicio** y **resultado**. Los nombres de campo del API no cambian.

---

## 3. Dónde viven los juicios

Este es el hallazgo conceptual más útil para diseñar [§1, B-P6].

| Primitiva | Dónde va lo que Jev juzga | Qué devuelve |
|---|---|---|
| **Noul** | en `instructions`: **un solo juicio** | el grado en que sostiene ese juicio |
| **Choice** | en `criteria`: **varios juicios, alternativas sin orden** | cómo reparte su soporte entre ellos |
| **Score** | en `criteria`: **varios juicios, niveles ordenados** | el reparto entre niveles y su posición media |

Tres ideas que se desprenden de esta tabla:

1. **En Choice y Score, cada opción es un juicio.** Jev sopesa cada uno por separado (la documentación de Score lo dice: cada nivel se evalúa sin ver a los vecinos) y luego reparte el soporte para que sume 1. Una imagen: 100 monedas repartidas entre los juicios.
2. **La pregunta no es lo que Jev juzga.** En Choice y Score, la pregunta de `instructions` agrupa los juicios como alternativas, igual que en la semántica de Hamblin: el significado de una pregunta es el conjunto de sus respuestas posibles. La prueba 6 lo mostró: con `instructions` vacío, el reparto de un caso claro fue idéntico. (Su peso en casos difíciles es una **cuestión abierta**.)
3. **`choice` no es una decisión de Jev.** Es la opción que recibió más soporte: un cálculo sobre el reparto. Con «¿Qué hora es?» y tres horas posibles, sin expediente, Jev igual reparte: no sabe la hora, sopesa tres juicios.

**Principio de diseño.**

- **Qué juzga:** lo que va en `instructions` (Noul) o en `criteria` (Choice, Score). Ahí se concentra el trabajo de redacción.
- **Contra qué lo sopesa:**
  1. solo contra lo notorio, si el expediente va vacío;
  2. contra un estado de cosas más lo notorio, si el expediente trae material.

---

## 4. Las tres formas de sentencia

### 4.1 Noul: un juicio, un grado

Devuelve un número entre 0 y 1. La guía lo lee por **bandas** [§3.1]:

| Grado | Lectura |
|---|---|
| > 0,85 | muy seguramente el juicio es cierto |
| 0,75 – 0,85 | seguramente es cierto |
| 0,65 – 0,75 | hay bases para pensar que es cierto |
| **0,30 – 0,65** | **el juicio no se puede formar con este expediente** |
| 0,20 – 0,30 | la base no es firme |
| < 0,20 | muy seguramente el juicio es falso |

Cuatro claves de lectura:

- **La franja central es una señal de diseño, no una duda de Jev.** Si un juicio cae ahí, probablemente está mal formulado o desconectado del expediente. Ejemplo: «`nota` *afirma* que Robert Scott fue…» dio ~0,50; con «`nota` *dice* que…», ~0,70. (TypeSafe, en su cookbook de consistencia, manda a revisión casi la misma franja: 0,30–0,70.)
- **La escala es asimétrica.** Arriba hay tres grados de «cierto»; abajo, primero «la base no es firme» y solo muy abajo «falso».
- **«Falso» se refiere al juicio tal como está redactado.** Un grado bajo en «`folleto` dice que la capital es Sídney» no distingue si el folleto dice otra cosa (**contradice**) o no habla del tema (**calla**). Para separarlo: dos Nouls sobre juicios contrarios, o una Choice con opción de salida.
- **Nouls que parecen complementarias no suman 1** (oficial: 0,72 + 0,47 = 1,19). La Noul no reparte entre «sí» y «no»: gradúa un solo juicio. Por eso no lleva `confidence`.

### 4.2 Choice: alternativas sin orden

Devuelve `probabilities` (el reparto, suma 1), `choice` (la de más soporte) y `confidence` (qué tan concentrado está el reparto) [§3.2].

- **Cada opción se redacta como un juicio**, con las mismas precauciones que el juicio de una Noul.
- **Siempre una opción de salida** (`otra`, `ninguna`, `no se indica`). Sin ella, el soporte se reparte a la fuerza entre las que hay, y la confianza no avisa.
- **Lee `probabilities`, no solo `choice`.** Lo notorio puede quitar soporte al juicio que el expediente sostiene sin cambiar la elección (ver §7 de este resumen).

### 4.3 Score: niveles ordenados

Devuelve el reparto entre niveles, `score` (la posición media de ese reparto), `legend` y `confidence` [§3.3].

- **El score es una posición, no una medida.** 2,74 no es «74 % del camino entre urgente y crítico». TypeSafe advierte que los niveles de Jev 1.13 tienen calibración numérica débil.
- **Con confianza baja, mira el reparto.** Un score de 1,0 puede venir de «todo en el nivel 1» o de «mitad en 0 y mitad en 2», con el nivel 1 vacío. En el Anexo A pasó: un 1,75 apuntaba justo al nivel sin soporte.
- **Combinar Scores se hace en código**: normalizar, ponderar y sumar (patrón oficial *composite scoring*).

**Seis reglas para escribir una escala** [§3.4, Anexo A]:

1. Una sola dimensión por escala.
2. Niveles sobre lo que el texto dice o insinúa, no sobre el mundo.
3. Que los niveles no se pisen: si un caso cabe en dos, Jev reparte 0,50 / 0,50.
4. Escribe la frontera como decisión: dónde termina un nivel es política, no un hecho.
5. Sin dobles negaciones ni indirección.
6. Los ejemplos no deben parecerse al material que se evalúa.

Y una pauta: cubre el caso intermedio frecuente. Estas reglas funcionaron al primer intento en otro idioma y otro dominio: 8 de 8 y 25 de 25 en casos claros [B-P1].

---

## 5. Redactar el juicio

Diseñar con Jev es, sobre todo, **redactar bien dos cosas**: el juicio y el expediente. Primero, el juicio [§4.3].

**Reglas oficiales de TypeSafe** (se adoptan, no se vuelven a probar):

- Redacta de modo que **el grado alto sea lo que buscas**: «`mensaje` contiene datos personales», mejor que «`mensaje` está libre de datos personales».
- Un enunciado funciona tan bien como una pregunta.
- Jev lee **al pie de la letra** las palabras de alcance, las negaciones y las condiciones implícitas: escribe exactamente lo que quieres decir.
- Evita **dobles negaciones e indirección**.
- Que `instructions` y `criteria` **no se contradigan**.

**Reglas que añadió el spike:**

- **Escribe el juicio directamente**, sin «es verdadero que» ni «es falso que». «Es verdad que p» no añade nada a p (Frege, Ramsey).
- **Cada palabra forma parte del juicio.** «`nota` afirma…», «`nota` dice…» y «Según `nota`…» son tres juicios distintos, y Jev los distingue [§4.6]:

  | Juicio sobre la nota de Scott | Grado |
  |---|---|
  | «`nota` **afirma** que Robert Scott fue…» | ~0,50 |
  | «`nota` **dice** que…» | ~0,70 |
  | «**Según** `nota`, …» | ~0,70 |

  «Afirmar» es sostener algo como cierto; «decir» reporta; «según» sitúa el contenido en la perspectiva del texto.
- **Escribe qué se juzga: lo que dice el material, o si lo que dice es correcto.** Es la regla de la prueba 2. Con un folleto que dice «Sídney», «qué dice» dio 0,82 en la Noul y 1,00 en la Choice, y «¿es correcto?» dio 0,11 y 0,99. **Las dos primitivas siguen al objeto del juicio; la primitiva solo da la forma del resultado** [§4.5, B-P2].
- **Nombra el material cuando el juicio es sobre él.** La forma natural da igual («`folleto` afirma», «El texto afirma»: todas 0,98); con varios campos, usa el nombre del campo entre backticks [B-P3a].
- **Una Noul por dimensión.** Certeza y evidencia, por ejemplo, van en dos Nouls: así se separaron «Según los ensayos… *podría*…» (certeza 0,14, evidencia 0,92) y «Los ensayos… *muestran*…» (0,92 y 0,93) [B-P1].
- **Las negaciones en el material no son el problema**: se leyeron bien. Las precauciones son sobre la redacción del juicio.

---

## 6. El expediente

### 6.1 Qué va en el expediente

El `state` es el **material que se somete a juicio** [§4.1]. Buenas prácticas:

- material con un **papel reconocible**, nombrado por ese papel (`mensaje`, `folleto`; no `bloque` ni `t0`);
- **solo lo pertinente**: TypeSafe advierte del *context rot* (el exceso o lo irrelevante degradan el juicio);
- el contenido del expediente es **dato, no instrucciones**: puede ser adversarial;
- **nombres de campo neutros**, que no sugieran el veredicto. Las claves de los juicios no llegan al modelo (oficial, y medido: con `q1`, `libro_senalaba` o `falso`, el mismo juicio dio 0,85–0,87 [B-P7c]); aun así se usan claves neutras.

**Sondas del modelo y pruebas de diseño.** Poner a propósito un enunciado suelto en el `state` («2+2=5») sirve para estudiar a Jev: ¿tiene un mundo propio?, ¿qué hace si el expediente lo contradice? Pero en una aplicación el `state` lleva material realista. Lo que sale de una sonda **no se convierte en regla de diseño** sin probarlo con material realista [§4.4, §12].

### 6.2 Sensibilidades observadas (no mecanismos)

La versión 4 de la guía retiró sus explicaciones de mecanismo («el state impreciso contamina») y se quedó con lo observado [§4.4]:

- **El objeto del juicio lo cambia todo.** Con state `"2+2=5"`: «Is 2+2=5?» → 0,02; «Does the text say that 2+2=5?» → 0,99. Son dos juicios distintos, uno sobre el mundo y otro sobre el texto.
- **Un expediente irrelevante no movió el juicio** (0,72 → 0,72).
- **Un expediente pertinente lo movió en ambos sentidos** (0,72 → 0,32 / 0,79), probablemente porque **resolvía la ambigüedad** de «la tierra» (¿el planeta o el suelo?).

**Comparar en log-odds.** Un mismo empujón se ve grande cerca de 0,5 y pequeño cerca de 0 o 1. Por eso los efectos se comparan en Δlogit, con líneas base **medidas**, no supuestas.

---

## 7. Cuando el expediente choca con lo notorio

Aquí el marco del juez da su fruto más importante, y también su lección más humilde [§4.6, B-P3, B-P7].

### 7.1 Jev sopesa con los dos a la vez

Notas breves en dos versiones, idénticas salvo un dato. Juicio: «`nota` afirma que [lo que la nota dice]».

| Lo que la nota dice (choca con lo notorio) | Grado |
|---|---|
| la ballena azul es un pez | 0,92 |
| la capital de Australia es Sídney | 0,82 |
| Lope de Vega escribió el Quijote | 0,76 |
| azul + amarillo da morado | 0,76 |
| la capital de Canadá es Toronto | 0,64 |
| Scott fue el primero en el Polo Sur | 0,45–0,51 |
| Gagarin fue el primero en caminar sobre la Luna | 0,36–0,43 |

Con el dato notorio, el mismo juicio dio 0,91–0,99. **El juicio sobre lo que dice un expediente baja cuando lo que dice choca con lo notorio**, y a veces cae en la franja central (6 de 6 casos).

Consecuencia práctica: si el material puede contener errores (respuestas de estudiantes, documentos por verificar), hay que esperar grados más bajos y calibrar los umbrales con ese material.

### 7.2 El marco del expediente también pesa

Con el expediente escrito como **relato** —«Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que…»—, el juicio que repite lo que el libro señalaba no llega a 1,00:

| Lo que el libro señalaba | Noul |
|---|---|
| Gagarin caminó en la Luna (choca con lo notorio) | 0,85–0,87 |
| Jesús murió crucificado (coincide con lo notorio) | 0,86–0,87 |
| Frat caminó en la Luna | 0,89–0,90 |
| Frat encontró la isla de los durmientes (inventado) | 0,92–0,93 |

Que el contenido sea falso, verdadero o inventado mueve el grado apenas unas centésimas. Lo que lo sitúa en esa franja es la forma del expediente. Y si el juicio deja de referirse al libro («Frat encontró la isla de los durmientes.»), baja a 0,72: ya no se juzga el testimonio, sino el hecho.

### 7.3 En una Choice, lo notorio se asoma en el reparto

Mismo relato, `instructions` vacío, dos juicios: «un libro antiguo señalaba que…» y «no hay evidencia de que un libro antiguo señalara que…». El segundo está desmentido por el propio expediente. Aun así:

| Lo que el libro señalaba | P(señalaba) | Confianza |
|---|---|---|
| Jesús murió crucificado | 0,99 | 0,98–0,99 |
| Gagarin **fue** el primero en la Luna | 0,84–0,87 | 0,68–0,73 |
| Gagarin **no fue** el primero en la Luna | 0,80–0,82 | 0,60–0,64 |
| Igual, con «un libro» en vez de «un libro antiguo» (fue / no fue) | 0,93–0,95 / 0,91–0,93 | 0,82–0,89 |

`choice` fue siempre el juicio que el expediente sostiene, pero **el reparto cambió con el contenido y con una sola palabra del marco**. Y no lo explica la verdad del contenido: el libro que niega un hecho falso recibió *menos* que el que lo afirma.

**Implicación de diseño:** esta influencia solo se ve en la distribución. Una aplicación que lea solo `choice` no la verá nunca. Por eso: **lee `probabilities`**.

### 7.4 Por qué no buscamos el mecanismo

Jev es una **caja negra**. Podríamos encontrar una explicación para Gagarin —el anacronismo de un libro antiguo que habla de la Luna encaja con parte de los datos— y que esa explicación no sirviera para Einstein. La guía probó una hipótesis de mecanismo (la «incoherencia interna» del expediente) y los datos la refutaron: al quitar los detalles que supuestamente delataban la incoherencia, el grado bajó en vez de subir [B-P7a]. La hipótesis se retiró, y con ella la búsqueda de mecanismos.

---

## 8. Consistente pero sensible

Esta es la síntesis a la que llegó la guía en su versión 8 [§4.6, §15]:

| Propiedad | Qué significa | Evidencia |
|---|---|---|
| **Consistencia** | Un juicio fijado da casi el mismo grado en cada réplica. | ±0,01–0,02 en las pruebas de reglas; TypeSafe reporta una desviación media de 0,0102 en 15 repeticiones. |
| **Sensibilidad** | Cambios pequeños de redacción o de marco mueven el grado de forma que no se predice. | «afirma» / «dice»; «libro antiguo» / «libro»; «fue» / «no fue». |

De ahí salen dos reglas de operación:

1. **Las bandas y los umbrales son heurísticos.** Orientan la lectura; no son valores calibrados.
2. **El diseño sigue líneas generales, pero se afina en cada caso de uso**, con casos de referencia y réplicas, si se quieren buenos rendimientos y consistencia.

La consistencia no garantiza sentido: **un juicio mal redactado da grados muy consistentes que no dicen lo que se quería saber** [§1, §9].

---

## 9. La confianza

**Qué es** (oficial): un estadístico calculado a partir del reparto. Si el soporte se concentra en un juicio, la confianza es alta; si se reparte, es baja. No es un juicio nuevo del modelo: es geometría del reparto [§5].

**Fórmula.** TypeSafe da el caso de tres opciones: `(3 × p_max − 1) / 2`. El spike la generaliza como `(N·p_max − 1)/(N − 1)`, que reproduce los datos con 2 y 4 opciones. Es una reconstrucción nuestra, no un contrato.

**Lo que no es.** Confianza alta no garantiza acierto. TypeSafe describe sus modelos como calibrados, pero la calibración es una propiedad de **grupos** de predicciones, no una promesa sobre un caso.

**La confianza baja, como la franja central, es una señal de diseño.** Suele indicar una de tres cosas:

- el juicio está mal redactado o desconectado del expediente;
- los juicios de `criteria` se pisan;
- el expediente no decide ese caso: admite dos lecturas.

**Umbrales:**

- se fijan **por acción y dominio, con datos propios** (oficial: acciones distintas se controlan con umbrales distintos según el costo del error);
- **por primitiva**: la Noul es más «blanda» que la Choice (0,82 frente a 1,00 para el mismo objeto);
- **en el idioma del corpus**: una rúbrica traducida conserva el veredicto pero no siempre la seguridad (0,79 en inglés, 0,33 en español, mismo nivel);
- **lejos de los casos reales**: un mensaje dio 0,71 · 0,69 · 0,72 en tres réplicas; con umbral 0,70, cambiaba de camino según la corrida.

---

## 10. Jev dentro de un sistema

### 10.1 Los límites oficiales explican por qué el código decide

La documentación de TypeSafe publica once límites de Jev 1.13 [§6, actualizado el 23 de septiembre de 2026]: lectura literal, conteos, representaciones numéricas, calibración numérica débil del Score, fechas y horas, indirección, expediente grande e irrelevante (*context rot*), contenido adversarial, instrucciones y criterios contradictorios, invariantes estructurales y generación de texto.

Por eso **cálculos, fechas normalizadas, reglas, permisos, invariantes y efectos quedan en código** o bajo revisión adecuada.

### 10.2 ¿Merece la pena Jev? Cinco preguntas [§2]

1. ¿Lo que necesitas se puede escribir como un juicio o como juicios alternativos bien definidos?
2. ¿El expediente está disponible y se puede delimitar?
3. ¿Una persona experta emitiría ese juicio en pocos segundos?
4. ¿El resultado se puede evaluar?
5. ¿El juicio se repetirá lo bastante para que importen latencia, costo y uniformidad?

«¿Cuál es la mejor arquitectura para este sistema?» no es un juicio estrecho: convertirla en un Score oculta el problema, no lo resuelve.

### 10.3 Patrones y usos

- **Cuatro patrones oficiales** [§8]: *fan-out* (varios juicios, un expediente; independencia no es coherencia conjunta), *confidence routing*, *composite scoring* (la política, explícita en código) e *intent routing* (con ruta para lo desconocido).
- **Diez formas de decisión** [§7]: clasificación, detección, scoring, routing, búsqueda, recuperación, ranking, verificación, extracción de features y extracción de datos estructurados. En búsqueda y recuperación, Jev aporta juicios dentro del pipeline; no sustituye al índice.
- **Frente a un LLM** [§9]: un LLM responde; Jev sopesa. Lo que se sabe de los LLM sirve como analogía, no como explicación de Jev. Patrón híbrido: el LLM o el operador define la tarea abierta, Jev ejecuta los juicios repetitivos y el código decide.
- **Extracción documental** [§13]: Jev convierte juicios locales repetibles en señales reutilizables (función, modalidad, fuerza de evidencia…), pero la estructura canónica no se modifica solo porque una salida probabilística parezca convincente.

### 10.4 Costo, latencia y versión [§11, §12]

- Precio publicado: 0,042 USD por millón de tokens de entrada; salida sin costo.
- Agrupar juicios sobre el mismo expediente es mucho más eficiente. La documentación da 11,5× / 9,6× en una página y 12,2× / 10,0× en otra: no se fuerza una cifra única.
- Las latencias promocionales no se mezclan con las medidas (0,7–2,5 s en el spike).
- **Se fija la versión del modelo** (`jev-1.13.0`); `jev-preview` es un alias móvil. La versión del modelo y del juicio forma parte del dato.

---

## 11. Cómo se aprendió: el método

La guía no solo dice qué hacer con Jev; muestra cómo se llegó a saberlo [§12, Anexos A y B].

- **Casos sencillos pero ilustrativos.** Cada prueba parte de un caso mínimo que muestra una sola regla.
- **La predicción se escribe antes de correr**, y es puntual («nivel 1»), no un rango. En el Anexo A, cinco predicciones fallaron, y la más reveladora solo se aprendió porque estaba escrita.
- **Pares mínimos**: se cambia una sola cosa cada vez, para saber qué movió el resultado.
- **Réplicas**: media y rango, no un número.
- **Paráfrasis con cuidado**: cambiar una palabra puede cambiar el juicio. Si una paráfrasis cae en otra banda, las palabras llevaban juicios distintos.
- **Separar ajuste y validación**: la escala de urgencia se corrigió sobre unos mensajes y se validó con ocho nuevos (8 de 8).
- **Sondas del modelo frente a pruebas de diseño**: las primeras estudian a Jev; solo las segundas dan reglas de diseño.
- **Ante la franja central, primero el diseño.**
- **Lo oficial se adopta, no se vuelve a probar**; lo nuestro lo complementa.
- **El crudo siempre a la vista**: el número se demuestra, no se copia.

### El registro de reglas [Anexo C]

Cada regla se clasifica en tres ejes:

| Eje | Valores |
|---|---|
| **Clase** | **Precaución** (P): «esto puede pasar; evítalo». Basta un caso. **Predictiva** (Pr): «esto normalmente ocurre así». Necesita varios casos. |
| **Ámbito** | **modelo** (cómo se comporta Jev) o **diseño** (cómo usarlo). |
| **Estado** | oficial · sostenida · medida · aceptada · conjetura |

Las reglas se ordenan por nivel: modelo, Noul, Choice, Score, entre primitivas y operación. Una regla «sostenida» es una buena apuesta de partida, no una garantía.

---

## 12. Lo que se retiró (y por qué eso importa)

La guía es honesta con sus errores. Retirar afirmaciones fue parte del aprendizaje:

| Afirmación retirada | Por qué |
|---|---|
| «Un state impreciso contamina el juicio» | El expediente más probablemente resolvía la ambigüedad del juicio [§4.4]. |
| «La primitiva elige el mundo de referencia» | Sobreinterpretación de un solo dominio: lo decisivo es el objeto del juicio [§4.5]. |
| «La fecha de corte está hacia el 2T de 2025» | Un grado bajo no dice por qué: desconocimiento, conocimiento antiguo, tasa base o semántica temporal [§6]. |
| La franja central como «no sé» o «duda» de Jev | Es una señal de diseño [§3.1]. |
| «Baja más cuanto más se contradice el propio expediente» | Al quitar los detalles, bajó más [B-P7a]. |
| La búsqueda de mecanismos internos | Caja negra: una explicación para un caso puede no servir para otro [§4.6]. |

El patrón es claro: cada vez que la guía propuso un **mecanismo**, tuvo que retirarlo; lo que resistió fueron las **sensibilidades observadas** y las **reglas de diseño**.

---

## 13. Preguntas abiertas

- **El peso de la pregunta de `instructions` en Choice y Score** cuando el caso no es claro. En un caso claro no pesó nada; en casos difíciles, seguramente algo [B-P6].
- **Hipótesis sobre el expediente**, todavía por probar [§4.4]: si un expediente pertinente fija la referencia de un juicio ambiguo; si el expediente pesa más cuando, sin él, el juicio cae en la franja central; si varios juicios sobre el mismo expediente heredan la misma ambigüedad.
- **El horizonte de conocimiento** de Jev: requiere un diseño con parejas de hechos y contrafácticos, clases separadas, controles y réplicas [§6].

---

## 14. Asociaciones que el marco deja ver

Esta sección no está en la guía como tal: son lecturas de conjunto que se desprenden de ella. No son mecanismos del modelo, sino maneras de ordenar lo observado.

**1. Una sola señal de diseño, en dos formas.** La franja central de la Noul y la confianza baja de Choice y Score dicen lo mismo: el juicio, tal como está redactado, no se deja decidir con ese expediente. En ninguno de los dos casos describen una duda de Jev. En los dos, la respuesta es revisar el juicio, los `criteria` o el expediente antes de interpretar el número.

**2. Fiabilidad no es validez.** La psicometría distingue entre un instrumento **fiable** (mide lo mismo cada vez) y uno **válido** (mide lo que se quiere medir). Jev es muy fiable: las réplicas casi no varían. La validez depende de la redacción del juicio. De ahí la advertencia que recorre toda la guía: un juicio mal redactado da grados muy consistentes que no dicen lo que se quería saber.

**3. Los contextos indirectos no son del todo opacos para Jev.** Frege observó que en «la nota *dice* que p», la verdad de p no debería importar: p está en un contexto indirecto, y lo que se juzga es el decir, no lo dicho. La sección 7 muestra que Jev distingue esos contextos —«afirma» no es «dice»—, pero no los aísla por completo: lo notorio se filtra en el juicio sobre lo que un texto dice o señala. Esa es, en términos filosóficos, la forma exacta del hallazgo del §4.6.

**4. La distancia entre el juicio y el expediente.** Varios resultados se ordenan en una misma gradación, como heurística de diseño (no como mecanismo):

| Qué relación hay entre el juicio y el expediente | Ejemplo | Grado |
|---|---|---|
| el juicio repite lo que dice el documento mismo | el folleto dice «Canberra» | 0,98 |
| el juicio repite lo que un relato cuenta que dijo un documento | el libro señalaba… | 0,85–0,93 |
| el juicio afirma el hecho del que el expediente solo da testimonio | «Frat encontró la isla…» | 0,72 |

Cuanto más se aleja el juicio de lo que el expediente contiene literalmente, más espacio queda para lo notorio. La regla práctica es simple: **acerca el juicio a lo que el expediente contiene**, y di en el juicio qué se juzga.

**5. Lo que resiste en una caja negra.** La lista de retiradas (§12 de este resumen) muestra un patrón epistemológico: con un modelo que no se puede abrir, los mecanismos propuestos caen y las **sensibilidades observadas** resisten. Es la misma lección de cualquier estudio de conducta: se describen regularidades entre entradas y salidas, y se diseña sobre ellas.

---

## 15. Nota de corroboración con la documentación oficial

Consulté las páginas de TypeSafe el 23 de septiembre de 2026 (`llms.txt`, `primitives/noul`, `confidence`, `model-jaggedness/jev-1.13`). Coinciden con la guía en lo esencial, con tres precisiones:

1. **La página de límites enumera hoy once puntos**, no los nueve que resumía la guía: separa conteos de representaciones numéricas y suma a la lista la calibración numérica débil del Score. **Resuelto el 23 de septiembre de 2026**: el §6 de la guía (versión 8.1) sigue ahora la lista y la numeración oficiales, y en la guía, el README y el diccionario los límites se citan por su nombre, no por su número.
2. **La documentación de la Noul** describe el resultado como «la probabilidad de que la respuesta sea sí», y `instructions` como «la pregunta sí/no que el modelo responde, o un enunciado para que juzgue». El marco del juez es nuestra lectura de ese contrato: no lo contradice, pero tampoco es el vocabulario oficial.
3. **La página de confianza** propone tres franjas de acción (alta: automatizar; media: confirmar o revisar; baja: humano u otro sistema) y dice que el umbral depende del dominio y del desempeño en el caso de uso. Coincide con §5 de la guía y con §9 de este resumen.

---

## 16. En una página

- **Jev es un juez:** recibe un expediente y un juicio, y devuelve cuánto lo sostendría, sopesándolo con el expediente y con lo notorio.
- **Lo que Jev juzga** vive en `instructions` (Noul) o en `criteria` (Choice, Score). La pregunta agrupa; no es lo juzgado.
- **Noul:** un grado, leído por bandas. La franja central (0,30–0,65) es una señal de diseño.
- **Choice y Score:** un reparto de 100 monedas. `choice` no es una decisión; `score` no es una medida. Lee `probabilities`.
- **Redactar es el trabajo:** cada palabra forma parte del juicio; di qué se juzga; acerca el juicio al expediente.
- **Lo notorio se filtra**, también en lo que un texto dice, y en una Choice puede verse solo en el reparto.
- **Consistente pero sensible:** las bandas y los umbrales son heurísticos; el diseño se afina en cada caso de uso.
- **Jev sopesa; el sistema decide.** Y lo consume el sistema: usado correctamente, Jev es transparente para el usuario.
