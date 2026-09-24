# Jev de TypeSafe: guía pedagógica y crítica

> Versión 8.2 — 23 de septiembre de 2026 (§1: quién consume a Jev; en 8.1, §6 actualizado a los once límites oficiales)

## Cómo leer esta guía

Esta guía explica Jev de TypeSafe sin convertir su documentación, sus benchmarks o sus integraciones en una promesa general de inteligencia. Distingue cuatro niveles:

1. **Documentación oficial de TypeSafe**: contratos, primitivas, límites y ejemplos publicados por el proveedor.
2. **Benchmarks o materiales de terceros**: resultados útiles, pero dependientes de su tarea, datos y metodología.
3. **Mediciones propias**: resultados del spike local; no son garantías del producto.
4. **Inferencias arquitectónicas**: conclusiones razonables para diseñar software, que todavía deben validarse en el corpus y operación reales.

La tesis central es sencilla:

> **Jev sopesa juicios estrechos frente a un expediente y devuelve un grado de soporte tipado; el código compone esos grados, aplica las reglas y decide qué acción tomar.**

Es importante conservar el verbo *sopesar*. Que el resultado sea tipado y probabilístico no demuestra que el juicio sea el que queríamos someter, ni que el expediente sea coherente.

**Sobre el vocabulario.** Esta guía se ha construido a lo largo de varios spikes, y su vocabulario ha cambiado con lo aprendido. Desde la versión 6 usa el **marco del juez** (§1): el `state` es el **expediente**, lo que Jev juzga va en `instructions` (Noul) o en `criteria` (Choice, Score), y el resultado es un **grado de soporte** o su reparto. Donde el API dice *question* o *answer*, la guía dice juicio y resultado.

Al final hay tres piezas prácticas:

- el **Anexo A**: un caso real paso a paso (cómo se diseñó, corrigió y validó una escala de Score);
- el **Anexo B**: las pruebas con que se sostuvieron varias reglas;
- el **Anexo C, Registro de reglas**: todas las reglas de la guía en tablas, para consultar al diseñar.

Todo lo que aquí llamamos «reglas» son **heurísticas**: sentido común, experiencia y algo de experimentación. Orientan el diseño; no lo reemplazan. Cada aplicación necesita sus propios ajustes y pruebas.

---

## 1. Qué es Jev: un juez de juicios estrechos

TypeSafe presenta Jev como un **System One Model**: un modelo orientado a decisiones rápidas, repetibles y acotadas, que no genera texto (*«do not write replies, produce code, or generate explanations»*). Según su documentación, se entrena con RLCD (*reinforcement learning for calibrated decisions*), una forma de adaptar un modelo de lenguaje preentrenado para que emita decisiones calibradas en lugar de texto.

La mejor manera de entenderlo es como un **juez**:

- recibe un **expediente** (`state`): el material que la aplicación somete a juicio —un mensaje, un documento, un folleto—;
- recibe un **juicio propuesto** (el campo `instructions`, junto con `criteria` cuando corresponde);
- devuelve **cuánto sostendría ese juicio** si él mismo lo emitiera, con el expediente a la vista.

```text
expediente (state) + juicio (instructions [+ criteria])
                         ↓
                        Jev
                         ↓
      grado de soporte (o su reparto entre los juicios de criteria)
                         ↓
                       código
```

Jev **no responde preguntas, no extrae datos y no dice si algo es verdadero o falso**. Sopesa juicios. «Verdadero» y «falso» son lecturas que hacemos nosotros del grado (§3.1).

**Jev trae sus propios hechos notorios.** Como un juez, no necesita que el expediente le pruebe que la capital de Australia es Canberra: lo notorio no necesita prueba (*notoria non egent probatione*). Jev sopesa cada juicio con el expediente y con lo notorio a la vez. Eso explica varios resultados de esta guía (§4.4, §4.6).

**Dónde viven los juicios.**

| Primitiva | Dónde va lo que Jev juzga | Ejemplo | Qué devuelve Jev |
|---|---|---|---|
| Noul | en `instructions`: **un solo juicio** | «`ticket` pide un reembolso.» | el grado en que sostiene ese juicio |
| Choice | en `criteria`: **varios juicios, como alternativas sin orden** | «`ticket` pide cambiar o devolver un artículo» · «`ticket` reclama por un envío» · «`ticket` reclama por un cobro» · «otra cosa» | cómo reparte su soporte entre esos juicios |
| Score | en `criteria`: **varios juicios, como niveles ordenados** | «`mensaje` no expresa plazo» · «`mensaje` espera respuesta esta semana» · «`mensaje` lo necesita hoy» | el reparto entre niveles y su posición media |

En Choice y Score, **cada opción o nivel es un juicio que Jev sopesa por separado** —la documentación de Score lo dice: cada nivel se evalúa de forma independiente, sin ver los números ni los niveles vecinos—, y después el soporte se reparte para que sume 1, como 100 monedas entre los juicios. La pregunta que suele ir en `instructions` («¿Qué equipo debe atender esto?») **agrupa esos juicios como alternativas**, igual que en la semántica de las preguntas de Hamblin, donde el significado de una pregunta es el conjunto de sus respuestas posibles. Pero la pregunta no es lo que Jev juzga: con `instructions` vacío, el reparto de un caso claro no cambió en nada (Anexo B, prueba 6). Y el `choice` que devuelve no es una decisión de Jev: es la opción que recibió más soporte.

En esta guía, a veces se abrevia una Choice o un Score con un hueco («la urgencia de `mensaje` es ___»); los juicios completos son los que van en `criteria`.

**Principio de diseño: dónde poner lo que Jev juzga, y contra qué.**

- **Qué juzga:** en una Noul, lo que va en `instructions`; en una Choice o un Score, lo que va en `criteria`. Ahí se concentra el trabajo de redacción.
- **Contra qué lo sopesa**, según lo que el diseño le dé:
  1. **solo su conocimiento**, sus hechos notorios, si el expediente va vacío;
  2. **un estado de cosas más su conocimiento**, si el expediente trae material. Jev sopesa con los dos a la vez; si el material choca con lo notorio, el grado lo refleja (§4.6).

Jev no es, por sí mismo:

- un agente autónomo;
- un sistema de búsqueda o investigación factual;
- un sustituto de las reglas de negocio;
- una garantía de coherencia entre juicios distintos;
- un modelo de razonamiento profundo;
- una prueba de que un contenido es verdadero fuera del expediente que se le da.

Una comparación útil:

| Sistema | Fortaleza principal | Riesgo típico |
|---|---|---|
| LLM general | generar, explicar, transformar y resolver tareas abiertas | coste, latencia, salidas variables y difícil control de forma |
| Clasificador convencional | tarea fija, datos etiquetados y operación eficiente | requiere entrenamiento y mantenimiento específicos |
| Jev | sopesar juicios estrechos, tipados y repetibles frente a un expediente | un juicio mal redactado da grados consistentes que no dicen lo que se quería saber; no mantiene una visión global coherente |
| Código/reglas | invariantes, aritmética, política y efectos | no interpreta bien lenguaje ambiguo sin señales semánticas |

La ventaja de Jev aparece cuando el problema se puede expresar como muchos juicios pequeños, de forma conocida de antemano, que el código puede componer.

**Quién consume a Jev: el sistema, no el usuario.** Lo que Jev devuelve —un grado, un reparto, una elección tipada— lo lee un programa. TypeSafe lo dice así: Jev produce *«structured decisions that software can use directly»*. Por eso, **usado correctamente, Jev es transparente para el usuario**: la persona encuentra el sistema, no al juez. El nombre lo sugiere: en Kahneman, el Sistema 1 trabaja por debajo y alimenta al Sistema 2; un *System One Model* ocupa ese lugar dentro de una aplicación.

Meter a Jev en el bucle del usuario —mostrarle el grado como si fuera una respuesta— es un error de diseño, frecuente en textos que vienen del marco de los LLM, donde la salida del modelo sí es para una persona:

- **el grado se vuelve una afirmación**: el usuario lee «0,86» como «86 % verdadero» o como una opinión de la máquina, cuando es el soporte de un juicio redactado de cierta manera frente a cierto expediente;
- **la confianza se lee como acierto**, aunque la calibración vale para grupos de casos, no para el caso que el usuario tiene delante (§5);
- **la decisión queda sin dueño**: si cada usuario interpreta el grado, la política no está en el código, sino en la cabeza de cada uno.

Una imagen: el sensor de un termostato. Nadie quiere que el termostato le diga «el sensor da 0,86 de probabilidad de frío, ¿qué hacemos?»; uno quiere la casa a la temperatura correcta. Si algo falla, el técnico sí mira el sensor.

**Transparente para el usuario no es invisible para el operador.** Quien diseña, opera o audita el sistema debe ver todo: grados, repartos, versión del modelo y del juicio, crudos (§12). Y cuando hay revisión humana, lo que llega a la persona es un caso que el sistema enrutó; las probabilidades pueden acompañarlo como material de auditoría, no como la respuesta.

---

## 2. La prueba práctica: ¿merece la pena Jev?

Antes de elegir un modelo, hazte estas preguntas:

1. ¿Lo que necesitas se puede escribir como un juicio, o como un conjunto de juicios alternativos (opciones o niveles) bien definidos?
2. ¿El expediente relevante está disponible y se puede delimitar?
3. ¿Una persona experta podría emitir **ese juicio concreto** en pocos segundos?
4. ¿El resultado se puede evaluar con etiquetas, reglas o revisión humana?
5. ¿El juicio se repetirá suficientes veces para que importen la latencia, el coste o la uniformidad?

Si varias respuestas son negativas, no se sigue que Jev sea imposible; sí que hace falta descomponer el problema o usar otra arquitectura.

Ejemplos:

```text
«`ticket` pide un reembolso.»                          → Noul
«`documento` pertenece a la categoría ___»             → Choice
«La urgencia que expresa `mensaje` es ___»              → Score
«`pasaje` ___ la afirmación A»                         → Choice
   (la sostiene / la contradice / no la trata)
```

En cambio, esto no se puede escribir como un juicio estrecho:

```text
¿Cuál es la mejor arquitectura para este sistema?
```

Dentro de esa pregunta se esconden requisitos, supuestos, riesgos, costes, alternativas, restricciones operativas y consecuencias futuras. Convertirla directamente en un `Score` oculta el problema; no lo resuelve.

---

## 3. Las primitivas

Las tres primitivas son tres formas de someter un juicio a Jev (§1). Esta sección explica qué devuelve cada una y cómo leerlo.

### 3.1 Noul

Un **Noul** somete a Jev **un solo juicio**, en `instructions`, y devuelve `noul`: el grado en que Jev sostendría ese juicio con el expediente a la vista. La documentación lo describe como la probabilidad de que el enunciado sea verdadero.

```json
{ "type": "noul", "noul": 0.91 }
```

`noul: 0.91` no significa «la verdad universal es 91 %». Significa que, con ese expediente, ese juicio redactado así y esa versión del modelo, Jev sostendría el juicio con mucha fuerza.

**Un Noul gradúa el soporte de un solo juicio.** No reparte entre «sí» y «no». Por eso dos Nouls que parecen complementarios no tienen por qué sumar uno: la documentación muestra un caso con `0.72 + 0.47 = 1.19`. El código no debe asumir que juicios separados forman una distribución coherente.

#### Cómo leer el grado: las bandas

| Grado | Lectura |
|---|---|
| > 0,85 | **muy seguramente** el juicio es cierto |
| 0,75 – 0,85 | **seguramente** es cierto |
| 0,65 – 0,75 | **hay bases** para pensar que es cierto |
| 0,30 – 0,65 | **el juicio no se puede formar con este expediente** |
| 0,20 – 0,30 | **la base no es firme** |
| < 0,20 | **muy seguramente** el juicio es falso |

Tres observaciones:

1. **La franja central es una señal de diseño, no incertidumbre de Jev.** Si Jev no puede sostener ni rechazar un juicio, es porque el juicio, tal como está redactado, no se deja decidir con ese expediente: probablemente está mal formulado o desconectado del contexto. Ejemplo medido (§4.6): «`nota` *afirma* que Robert Scott fue…» quedó en ~0,50; con «`nota` *dice* que…», subió a ~0,70. Si el diseño es bueno y un caso concreto cae en la franja, ese caso se prevé en el flujo: revisión humana, un segundo juicio o más material. TypeSafe, en su cookbook de consistencia, envía a revisión los valores entre 0,30 y 0,70, prácticamente la misma franja.
2. **La escala es asimétrica, y con razón.** Del lado alto hay tres grados. Del lado bajo, primero la base no es firme, y solo muy abajo el juicio es falso.
3. **«Falso» se refiere al juicio tal como está redactado,** no a lo contrario de su contenido. Si «`folleto` dice que la capital de Australia es Sídney» da 0,01, es muy seguramente falso que el folleto lo diga. Pero eso no dice si el folleto nombra otra ciudad (lo **contradice**) o si no habla de capitales (**calla**). Para distinguirlo, usa **dos Nouls sobre juicios contrarios** («…es Sídney», «…es Canberra») o una **Choice con opción de salida** («no se indica»).

Las bandas valen para la Noul. La Choice reparte y tiende a saturar, y se lee por su reparto (§3.2). Cada aplicación puede ajustar los bordes con sus datos: las bandas son el vocabulario común de partida.

#### Cómo redactar el juicio

- **Escribe el juicio directamente.** No lo envuelvas en «es verdadero que…» ni «es falso que…»: Jev ya devuelve cuánto sostiene el juicio, y «es verdad que p» no añade nada a p (Frege, Ramsey). «Es falso que…» mete además una negación dentro del juicio.
- **Cada palabra forma parte del juicio.** «`nota` afirma que…», «`nota` dice que…» y «Según `nota`,…» son tres juicios distintos (§4.6).
- **Una Noul por dimensión.** Si dos ideas se confunden con facilidad —por ejemplo, la *certeza* con que se afirma algo y la *evidencia* que lo apoya—, somételas en dos Nouls. En el Anexo B (prueba 1), dos Nouls así separaron «Según los ensayos…, el fármaco *podría*…» (certeza baja, evidencia alta) de «Los ensayos… *muestran* que…» (ambas altas).

### 3.2 Choice

En una **Choice**, los juicios van en `criteria`: cada opción es un juicio candidato, sin orden entre ellos. Jev sopesa cada uno y **reparte su soporte** entre todos.

```json
{
  "type": "choice",
  "choice": "billing",
  "probabilities": { "billing": 0.86, "technical": 0.09, "account": 0.05 },
  "confidence": 0.79
}
```

- `probabilities`: cómo reparte Jev su soporte entre los juicios. Suma 1.
- `choice`: el juicio que concentra más soporte. No es una decisión de Jev, sino un cálculo sobre el reparto.
- `confidence`: qué tan concentrado está el reparto (§5).

**Jev no responde: sopesa juicios.** Si le das «¿Qué hora es?» con las opciones 10:00, 11:00 y 1:00, sin expediente, devuelve igual un reparto entre las tres. No sabe la hora: sopesa tres juicios posibles («son las 10:00», «son las 11:00», «es la 1:00»). La pregunta de `instructions` agrupa esos juicios como alternativas, pero puede ir vacía: en la prueba 6 (Anexo B), con `instructions: ""` y los juicios completos en `criteria`, el reparto fue el mismo que con la pregunta. Por eso el esfuerzo de redacción va a los `criteria`: **cada opción se redacta como un juicio**, con las mismas precauciones que el juicio de una Noul (§4.3).

La lista de juicios debe ser explícita y puede tener como máximo 255 opciones. **Incluye una opción de salida** —`otra`, `ninguna`, `no se indica`—, porque puede que ningún juicio se sostenga con el expediente; sin ella, el soporte se reparte a la fuerza entre los que hay. Si los juicios se solapan, están incompletas o cambian con frecuencia, el resultado exige evaluación adicional.

### 3.3 Score

En un **Score**, los juicios van en `criteria` como **niveles ordenados** que tú defines: cada nivel es un juicio sobre el caso («`mensaje` no expresa plazo», «`mensaje` lo necesita hoy»…). Jev sopesa cada nivel por separado y reparte su soporte entre ellos.

**Cómo se escribe.** En `criteria` escribes los niveles de la escala, del más bajo al más alto: entre 2 y 10 niveles. Cada nivel debe describir una situación reconocible, no un grado vago como «poco» o «mucho».

```json
{
  "criteria": [
    "sin urgencia",
    "requiere atención pronto",
    "urgente",
    "crítico"
  ]
}
```

**Qué devuelve.**

```json
{
  "type": "score",
  "score": 2.74,
  "legend": {
    "0": "sin urgencia",
    "1": "requiere atención pronto",
    "2": "urgente",
    "3": "crítico"
  },
  "probabilities": { "0": 0.01, "1": 0.04, "2": 0.15, "3": 0.80 },
  "confidence": 0.73
}
```

Cada campo significa:

| Campo | Qué es |
|---|---|
| `probabilities` | Cómo reparte Jev su soporte entre los niveles. Suma 1. |
| `score` | El punto medio de ese reparto. Puede caer entre dos niveles. |
| `legend` | Los niveles que definiste, numerados desde 0. |
| `confidence` | Qué tan concentrado está el reparto: 1 = todo en un nivel. |

(`scale` no es un campo del API.)

**Una imagen para entenderlo.** Imagina que Jev tiene 100 fichas y las reparte entre los niveles según cuánto sostiene cada uno. El `score` es el punto de equilibrio de esas fichas:

```text
0×0,01 + 1×0,04 + 2×0,15 + 3×0,80 = 2,74
```

Es decir: «casi crítico, con algo de peso en urgente».

**Tres reglas para leer un Score.**

1. **El score es una posición, no una medida.** Un 2,74 no significa «el 74 % del camino entre urgente y crítico». Los niveles son palabras, no marcas de una regla. TypeSafe advierte que en Jev 1.13 los niveles tienen una calibración numérica débil: el score sirve para comparar casos y aplicar umbrales («¿supera 2,5?»), no para leer magnitudes exactas.

2. **Si la confianza es baja, mira `probabilities`, no `score`.** El promedio puede esconder la forma del reparto. Estos dos casos tienen el mismo score y significan cosas opuestas:

   | Caso | Reparto | Score | Qué significa |
   |---|---|---|---|
   | A | nivel 1 → 100 % | 1,0 | sostiene el nivel 1 |
   | B | nivel 0 → 50 %, nivel 2 → 50 % | 1,0 | reparte entre 0 y 2; el nivel 1 **no** tiene soporte |

   El caso B ocurrió de verdad en el Anexo A: un score de 1,75 con 0,61 en el nivel 1, 0,34 en el nivel 3 y solo 0,03 en el nivel 2. El número apuntaba justo al nivel sin soporte. La confianza (0,37) daba la alarma.

3. **Combinar Scores es válido, si se hace en código.** El patrón oficial *composite scoring* normaliza cada score (se divide por el número de niveles menos 1, para llevarlo a 0–1) y lo pondera. Lo que se combina son posiciones sobre rúbricas, no cantidades físicas; por eso los pesos y los umbrales del resultado también se calibran con datos propios.

### 3.4 Cómo diseñar una escala de Score

La calidad de un Score depende sobre todo de cómo están escritos sus niveles. Estas seis reglas salen de la documentación oficial y de las pruebas del Anexo A.

| # | Regla | Por qué | Qué pasó en el Anexo A |
|---|---|---|---|
| 1 | **Una sola dimensión por escala.** | Si mezclas dos ideas (por ejemplo, plazo y costo), la escala deja de estar ordenada. Es recomendación oficial. | La escala mixta cambió con una palabra marginal (de 1,00 a 0,68) y repartió el caso claro entre dos niveles. Separada en dos escalas, quedó estable. |
| 2 | **Describe lo que el texto dice o insinúa, no el mundo.** | Jev sopesa cada nivel frente al expediente, y el expediente no dice si algo «da igual hoy o en un mes». | El nivel «no hay consecuencia» fallaba porque el mensaje no dice nada sobre consecuencias. |
| 3 | **Que los niveles no se pisen.** | Si un caso cabe en dos niveles, Jev reparte su soporte entre ambos. | «El cliente espera» cabía en «alguien espera» y en «una persona queda demorada»: salió 0,50 / 0,50. |
| 4 | **Escribe la frontera como una decisión.** | Dónde termina un nivel y empieza el otro es una política, no un hecho. | La frontera «solo el remitente / alguien más» resolvió el caso: 1,00 con confianza 1,00. |
| 5 | **Sin dobles negaciones ni indirección.** | Jev lee al pie de la letra las negaciones y las palabras de alcance, y sopesa con menos fiabilidad las dobles negaciones y la indirección (límites de lectura literal e indirección, §6). | Un nivel con tres negaciones («solo… nadie más… nada») bajó la confianza de 0,98 a 0,77. Ese nivel tenía además un error conceptual (esperar no es una consecuencia de la demora), así que el caso ilustra la regla, no la prueba. |
| 6 | **Los ejemplos no deben parecerse a lo que vas a evaluar.** | El reparto puede moverse por parecido de palabras, no por significado. | El ejemplo «Let me know when you can» arrastró un «No rush, whenever you get a chance» hacia un nivel que no le correspondía (0,67). Al cambiar el ejemplo, bajó a 0,0. |

Los niveles pueden escribirse como texto simple o como objetos con descripción y ejemplos:

```json
{
  "what": "Today: a same-day deadline is stated or clearly implied.",
  "examples": ["I need your comments before the end of the day."]
}
```

Una pauta final: **cubre el caso intermedio frecuente.** En el Anexo A, el mensaje más común —un recordatorio sin plazo— no tenía nivel propio. Hubo que crearlo.

**¿Funcionan estas reglas fuera del caso donde nacieron?** Se probaron dos veces más (Anexo B, prueba 1):

- la escala de urgencia, traducida al español, dio el mismo nivel que en inglés en 8 de 8 mensajes;
- dos escalas nuevas, escritas en español y en otro dominio (la fuerza con que un texto afirma algo), coincidieron con el nivel predicho en 25 de 25 casos claros **al primer intento**, sin retoques. La confianza bajó solo en los casos que se habían marcado de antemano como dudosos.

Una lección de esa prueba: si la escala tiene una frontera discutible, **escríbela en la rúbrica**. Allí se decidió que la certeza se mide «venga de quien venga la afirmación», y el caso «Los expertos coinciden en que…» quedó sin dudas en «firme».

---

## 4. El expediente y los juicios

En el API, un request tiene tres piezas: `state`, `instructions` y, en Choice y Score, `criteria`. En el marco del juez (§1), `state` es el **expediente**; lo que Jev juzga va en `instructions` en la Noul y en `criteria` en Choice y Score.

### 4.1 El expediente (`state`)

El `state` es el expediente: el **material que la aplicación somete a juicio**, con un papel reconocible —un mensaje, un documento, un folleto— y nombrado por ese papel (`mensaje`, `folleto`; no `bloque` ni `t0`). Puede ser texto, campos o una estructura. No es una memoria fiable ni un contenedor seguro.

La documentación advierte sobre **context rot**: demasiado contexto, contexto irrelevante o una organización poco clara degradan el juicio. También advierte que el contenido puede ser adversarial. Lo que va en el expediente es dato, no instrucciones con autoridad sobre el programa.

Buenas prácticas:

- incluir solo el material pertinente;
- nombrar cada campo por su papel;
- delimitar documentos, citas y metadatos;
- conservar el identificador del modelo y la versión del juicio;
- medir el efecto de añadir o quitar material.

Una advertencia: el expediente no es el único apoyo de Jev. Jev sopesa también con sus **hechos notorios** (§1). Si el expediente choca con ellos, el grado cambia (§4.6).

### 4.2 Los juicios de Choice y Score (`criteria`)

En una Choice o un Score, `criteria` es **donde viven los juicios**: cada opción o nivel es un juicio que Jev sopesa. Por eso no deben reducirse a etiquetas vagas: se redactan como juicios, con las mismas precauciones que el juicio de una Noul (§4.3). La documentación de Choice permite describir cada juicio con un objeto de campos `what`, `not_for` y `examples`:

```json
{
  "criteria": {
    "refund": {
      "what": "La solicitud pide devolver dinero por una compra",
      "not_for": "Preguntas sobre el estado de un envío",
      "examples": [
        "Quiero que me devuelvan el importe"
      ]
    },
    "shipping": {
      "what": "La solicitud pregunta por entrega, envío o seguimiento",
      "not_for": "Disputas sobre cobros",
      "examples": [
        "¿Dónde está mi pedido?"
      ]
    }
  }
}
```

La estructura hace los juicios más inspeccionables, pero no garantiza que sean mutuamente excluyentes ni que los ejemplos cubran producción. En una Noul, `criteria` es opcional: con los campos `true` y `false` describe qué significa sostener o no el juicio.

### 4.3 `instructions`: el juicio de la Noul

El campo se llama `instructions` en el API, y ese nombre no se puede cambiar en el request. Su papel depende de la primitiva:

- **En la Noul contiene el juicio** que Jev sopesa. No son instrucciones ni una pregunta: es el juicio mismo.
- **En Choice y Score**, los juicios están en `criteria` (§4.2). `instructions` suele llevar una pregunta que los agrupa como alternativas, y puede incluso ir vacío (Anexo B, prueba 6). Que esa pregunta tenga algún peso en casos menos claros es una **cuestión abierta**.

Las reglas de redacción que siguen valen para el juicio de la Noul y para **cada juicio de `criteria`**.

Cómo redactar un juicio:

- **Escribe el juicio exacto que quieres que Jev sopese.** Cada palabra forma parte de él: «afirma», «dice» y «según» son juicios distintos (§4.6).
- **Escríbelo directamente,** sin «es verdadero que» ni «es falso que» (§3.1).
- **Redáctalo de modo que el grado alto sea lo que buscas.** Mejor «`mensaje` contiene datos personales» que «`mensaje` está libre de datos personales» (TypeSafe).
- **Evita dobles negaciones e indirección compleja**: Jev las sopesa con menos fiabilidad (límite de indirección, §6).
- **Escribe exactamente lo que quieres decir.** Jev lee al pie de la letra las palabras de alcance («alguno», «todos», «solo»), las negaciones y las condiciones implícitas (límite de lectura literal, §6). Una palabra de alcance bien elegida evita términos medios: «¿Tiene **alguna** experiencia en Python?».
- **Que `instructions` y los juicios de `criteria` no se contradigan** (límite de instrucciones y criterios contradictorios, §6).
- Las negaciones **en el material** no son el problema: en nuestras pruebas se leyeron bien (Anexo B, prueba 1). Las precauciones anteriores son sobre la redacción del juicio.
- **Nombra el material cuando el juicio es sobre él.** En la prueba 3a (Anexo B), «`folleto` afirma…», «El folleto afirma…», «El texto afirma…» y «El documento afirma…» dieron el mismo grado. La forma natural da igual; si el expediente tiene varios campos, usa el nombre del campo entre backticks para que no haya duda de cuál se juzga.

El juicio también puede escribirse como objeto, con campos que precisan su foco:

```json
{
  "instructions": {
    "question": "¿Qué función cumple este fragmento dentro del documento?",
    "focus": "La función dentro del documento, no la calidad literaria"
  }
}
```

La documentación usa en sus ejemplos campos como `question`, `focus`, `compare` e `inspect`. En una Noul, lo que va en `question` es el juicio; en una Choice o un Score, la pregunta que agrupa los juicios de `criteria`. Puedes añadir campos propios, pero sus nombres son diseño de tu aplicación, no parte de un esquema oficial.

Esto ayuda a reducir ambigüedad y a versionar el contrato. No sustituye una definición operacional ni una prueba de calibración.

### 4.4 El expediente y el juicio: qué podemos afirmar y qué no

Esta sección se revisó en la versión 4. Las versiones anteriores proponían un mecanismo interno («un juicio conjunto», «el state impreciso contamina»). Los experimentos no alcanzan para eso: muestran **sensibilidades observables**, no mecanismos. Aquí separamos lo medido (nivel 3) de lo que todavía es hipótesis (nivel 4).

Una advertencia de método: estos experimentos son **sondas del modelo**. Ponían a propósito enunciados sueltos en el state («2+2=5») para comprobar si Jev tiene un mundo propio y qué hace cuando el state lo contradice. Eso es legítimo para estudiar a Jev, pero en una aplicación el `state` tiene otra función: contiene **material con un papel reconocible** (un mensaje, un documento, un folleto), nombrado por ese papel. Por eso lo que aquí se observa informa sobre el modelo; las reglas de diseño se prueban aparte, con material realista (sección 4.5 y Anexo B).

**Lo que se observó** (`jev-1.13.0`, crudos en `spike-jev/cache/`):

1. **El ancla cambia el juicio.** Con el mismo state `"2+2=5"` y en el mismo request, `"Is 2+2=5?"` dio 0,02 y `"Does the text say that 2+2=5?"` dio 0,99 (`noul-2mas2.json`). No son dos grados de un mismo juicio: son dos juicios distintos, uno sobre el mundo y otro sobre el texto. Incluso la redacción del ancla importa: `"Does the state say that 2+2=5?"` dio 0,71 (`noul-falso.json`).
2. **Un state irrelevante no movió el juicio.** `"a veces el sol no ilumina la tierra"` dio 0,72 sin state y 0,72 con `"Pedro está triste"`.
3. **Un state pertinente sí lo movió, y en ambos sentidos.** La misma proposición bajó a 0,32 y 0,38 con `"cuando en Bogotá es de día en los países del hemisferio oriental es de noche"`, y subió a 0,79 con `"cada noche Bogotá se oscurece"`.

**Cómo leer el punto 3.** La proposición es ambigua. «La tierra» puede ser el planeta —que el sol siempre ilumina a medias, y entonces la frase es falsa— o el suelo de un lugar —que de noche queda a oscuras, y entonces es verdadera—. Cada state favorece una de esas lecturas. Lo más probable es que el state no «contamine» el juicio sino que **resuelva la referencia** de la proposición. Por eso retiramos la moraleja de versiones anteriores: este experimento no permite concluir que un contexto impreciso contamine.

**Una trampa de medida: comparar en log-odds, no en probabilidad.** Un mismo empujón se ve grande cerca de 0,5 y pequeño cerca de 0 o de 1. Para comparar efectos se usa:

```text
Δlogit = logit(p con state) − logit(p sin state),   donde logit(p) = ln(p / (1 − p))
```

Ejemplo con nuestros datos:

| Caso | Sin state | Con state | Δp | Δlogit |
|---|---|---|---|---|
| sol, state de hemisferios | 0,72 | 0,32 | −0,40 | −1,70 |
| 2+2=5, state «en este mundo 2+2 es 5» | 0,04 (*) | 0,11 | +0,07 | +1,09 |

En probabilidad, la aritmética parece inmóvil; en log-odds, el state la movió casi tanto como al sol. (*) La línea base de la aritmética no es buena: el 0,04 se midió con state `"2+2=5"`, no con state vacío. Falta esa medición.

Dos cuidados prácticos: el API devuelve dos decimales, así que cerca de 0 o de 1 la resolución es pobre (de 0,01 a 0,02 hay 0,7 logits); conviene usar casos cuya línea base esté entre 0,1 y 0,9. Y la línea base se **mide**, no se supone.

**Hipótesis abiertas (nivel 4).**

| Hipótesis | Qué afirma | Cómo probarla |
|---|---|---|
| Desambiguación | El expediente pertinente fija la referencia de un juicio ambiguo. | Escribir el juicio sin ambigüedad: el efecto del state debería desaparecer o casi. |
| Peso de lo notorio | El expediente pesa más cuando, sin expediente, el juicio cae en la franja central. | Casos con líneas base cercanas a 0,1, 0,5 y 0,9, comparados en Δlogit. Si el Δlogit es igual en todas las bandas, la hipótesis cae: el efecto sería simplemente aditivo. |
| Lectura compartida | Varios juicios sobre el mismo expediente heredan la misma ambigüedad del mensaje. | Ver Anexo A (caso h3): añadir una petición explícita y comprobar si los dos repartos se concentran a la vez. |

Retirado en la versión 4: el ejemplo de la clave `"falso"` (0,91 → 0,10). Solo existe el crudo del 0,10; sin el otro extremo no hay comparación.

**Qué hacer en la práctica** (vale sea cual sea el mecanismo):

- Si quieres juzgar el **material**, dilo en el juicio: nómbralo y juzga lo que dice (§4.3).
- Si quieres sondear los **hechos notorios** de Jev, deja el expediente vacío.
- Si el juicio es **ambiguo**, desambígualo en su redacción; no dejes que el expediente decida la lectura.
- Incluye solo contexto **pertinente** (la documentación advierte del *context rot*).
- Usa **nombres de campo neutros**, que describan el papel del dato y no sugieran el veredicto. Es una precaución barata.

Límites: pocos casos, un dominio por experimento, un solo modelo.

### 4.5 Noul y Choice no son formas equivalentes del mismo juicio

**Lo que dice la documentación (nivel 1).** Entre los límites de Jev 1.13 figura la falta de *invariantes estructurales*: juicios que parecen equivalentes no tienen por qué dar grados coherentes. Su ejemplo: ante el mismo juicio sobre el mismo ticket, una Noul da 0,22 y una Choice sí/no da 0,01 para «sí». Tiene sentido: una Choice reparte su soporte entre sus juicios (suman 1), mientras que una Noul sopesa un juicio aislado.

**Lo que medimos (nivel 3).** State: `"en este mundo 2+2 es 5"`; instrucción: `"2+2=5"`.

| Juicio | Expediente vacío | Expediente «en este mundo…» |
|---|---|---|
| Noul `"2+2=5"` | sin medir | 0,11 |
| Noul anclada «¿Dice el state que 2+2 es 5?» | — | 0,90 |
| Choice [sí, no] | sí 0,00 | sí 0,48 |
| Choice [sí, sí con dudas, no con dudas, no] | sí 0,01 | sí 0,34 |

Crudos: `noul-2mas2-mundo*.json`, `choice-2mas2-*.json`. (Versiones anteriores de esta tabla ponían 0,04 en la casilla «Noul, state vacío»; ese valor se midió con state `"2+2=5"`.)

Con el mismo expediente, la Noul casi no sostiene el juicio y la Choice reparte su soporte. En el ejemplo oficial la divergencia iba **en sentido contrario** (la Choice sostenía menos el juicio). Conclusión segura: **la dirección de la divergencia no es fija; no la generalices.** El menú también pesa: con cuatro opciones, «sí» recibió 0,34; con dos, 0,48.

**¿Qué causaba esa divergencia? El objeto del juicio.** En el ejemplo de arriba, el juicio no decía qué se juzgaba: si la verdad de «2+2=5» o lo que dice el texto. Se probó con material realista (Anexo B, prueba 2): un folleto de viaje que dice «Su capital, Sídney, …», con dos objetos de juicio distintos, cada uno como Noul y como Choice.

| Folleto dice «Sídney» | Noul | Choice |
|---|---|---|
| ¿qué dice el folleto? | 0,82 | «Sídney» 1,00 |
| ¿el dato es correcto? | 0,11 | «incorrecto» 0,99 |

Con el mismo material, los dos objetos dan grados opuestos, y **las dos primitivas siguen al objeto**. En el folleto que dice «Canberra» ocurrió lo mismo, con los valores invertidos. De ahí la regla:

> **Escribe en el juicio qué se juzga: qué dice el material, o si lo que dice es correcto. La primitiva solo decide la forma del resultado.**

Una diferencia que conviene conocer: **la Noul es más «blanda» que la Choice**. La Choice reparte entre opciones que compiten y tiende a saturar (1,00 / 0,99); la Noul juzga un enunciado aislado y queda más lejos de los extremos (0,82 / 0,11). Por eso no se comparan magnitudes: se compara lo que dice cada una —la banda de la Noul (§3.1) y el juicio que concentra el soporte en la Choice—, y cada primitiva necesita sus propios umbrales.

Retirado en la versión 4: la tesis «la primitiva elige el mundo de referencia». Era una sobreinterpretación de un solo dominio.

**Qué hacer en la práctica:**

- Elige la primitiva por dónde van los juicios: uno solo → Noul; varios, alternativos y sin orden → Choice; varios, como niveles ordenados → Score.
- Escribe siempre qué se juzga. Si el objeto queda implícito, Noul y Choice pueden divergir; si queda explícito, coinciden.
- En una Choice, trata el menú como parte del juicio: cada opción redactada como juicio y, por regla general, una opción de salida.

### 4.6 Cuando el expediente choca con lo notorio

**Lo medido** (Anexo B, prueba 3). Notas breves, cada una en dos versiones idénticas salvo un dato: en una, el dato coincide con lo notorio; en la otra, choca con ello. Sobre la versión que choca, el juicio «`nota` afirma que [lo que la nota dice]»:

| Expediente (versión que choca con lo notorio) | Grado | Lectura |
|---|---|---|
| «La ballena azul, que es un pez, puede encontrarse en todos los océanos…» | 0,92 | muy seguramente cierto |
| «…Su capital, Sídney, es una ciudad moderna y ordenada…» | 0,82 | seguramente cierto |
| «Lope de Vega escribió Don Quijote de la Mancha…» | 0,76 | seguramente cierto |
| «Para pintar las hojas, mezcla azul y amarillo: así obtendrás el morado…» | 0,76 | seguramente cierto |
| «…Su capital, Toronto, es una ciudad tranquila y bilingüe…» | 0,64 | el juicio no se puede formar |
| «Robert Scott fue la primera persona en llegar al Polo Sur. Su expedición avanzó con trineos tirados por perros.» | 0,45–0,55 | el juicio no se puede formar |
| «Yuri Gagarin fue la primera persona en caminar sobre la Luna. Su hazaña se transmitió por televisión a millones de personas.» | 0,36–0,43 | el juicio no se puede formar |

Con las versiones que coinciden con lo notorio, el mismo juicio dio entre 0,91 y 0,99. Con un expediente que es solo el enunciado —`"2+2=5"`—, «`texto` afirma que 2+2=5» dio 0,97. El caso Gagarin se repitió en dos días con el mismo resultado.

**Lo que eso dice.** Jev sopesa el juicio sobre lo que dice el expediente **junto con lo notorio**. Cuando lo que el expediente dice choca con lo notorio, el grado baja, y a veces cae en la franja central.

**Cada palabra del juicio cuenta.** Con la nota de Scott, cambiando solo el verbo:

| Juicio | Grado | Lectura |
|---|---|---|
| «`nota` **afirma** que Robert Scott fue…» | ~0,50 | el juicio no se puede formar |
| «`nota` **dice** que Robert Scott fue…» | ~0,70 | hay bases |
| «**Según** `nota`, Robert Scott fue…» | ~0,70 | hay bases |
| «`note` **states** that Robert Scott was…» | ~0,56 | el juicio no se puede formar |

«Afirmar» (y *to state*) es sostener algo como cierto; «decir» solo reporta un contenido; «según» lo sitúa en la perspectiva de la nota. Son juicios distintos, y Jev los distingue. Con «2+2=5», en cambio, «afirma» y «dice» dieron lo mismo (0,97).

**Una hipótesis retirada: la incoherencia interna del expediente.** La versión 7 proponía que el grado bajaba más cuando el resto de la nota describía al protagonista notorio (los perros de Amundsen, la transmisión del paseo de Armstrong). Se probó quitando esos detalles: con la nota de Gagarin reducida a la sola oración, «`nota` afirma…» no subió, **bajó** (0,13–0,23). La hipótesis queda retirada.

**El marco del expediente también pesa** (Anexo B, prueba 7). Con el expediente escrito como relato —«Un hombre encontró un libro antiguo que señalaba, entre otras cosas, que…»—, el juicio que repite lo que el libro señalaba no llega a 1,00:

| Lo que el libro señalaba | Noul |
|---|---|
| Gagarin caminó en la Luna (choca con lo notorio) | 0,85–0,87 |
| Jesús murió crucificado (coincide con lo notorio) | 0,86–0,87 |
| Frat caminó en la Luna | 0,89–0,90 |
| Frat encontró la isla de los durmientes (inventado) | 0,92–0,93 |

(En Gagarin y Frat, el relato decía «señalaba… que la verdad fue que…» y el juicio «El libro antiguo dice que…»; en Jesús, «señalaba… que…» y «Un libro antiguo señalaba que…».)

Que el contenido sea falso, verdadero o inventado mueve el grado apenas unas centésimas; lo que lo sitúa en esa franja es la forma del expediente: un testimonio contado por un narrador. Con el expediente como documento (el folleto) el mismo tipo de juicio llegaba a 0,98. Y si del juicio se quita la referencia al libro —«Frat encontró la isla de los durmientes.»—, el grado baja a 0,72–0,73 (hay bases): ya no se juzga lo que el libro señalaba, sino el hecho, y para eso el expediente solo aporta un testimonio.

**En una Choice, lo notorio se asoma en el reparto.** Con el relato en la forma del caso Jesús, `instructions` vacío y dos juicios en `criteria` —«Un libro antiguo señalaba que…» y «No hay evidencia de que un libro antiguo señalara que…»—, el segundo está desmentido por el propio expediente. Aun así:

| Lo que el libro señalaba | P(señalaba) | P(no hay evidencia) | Confianza |
|---|---|---|---|
| Jesús murió crucificado | 0,99 | 0,01 | 0,98–0,99 |
| Gagarin **fue** el primero en la Luna | 0,84–0,87 | 0,13–0,16 | 0,68–0,73 |
| Gagarin **no fue** el primero en la Luna | 0,80–0,82 | 0,18–0,20 | 0,60–0,64 |
| Igual, pero «un libro» en vez de «un libro antiguo»: fue / no fue | 0,93–0,95 / 0,91–0,93 | 0,05–0,09 | 0,82–0,89 |

`choice` fue siempre el juicio que el expediente sostiene, pero el reparto cambió con el contenido y con una sola palabra del marco («antiguo»), y la confianza de Gagarin quedó alrededor del umbral habitual de revisión. No lo explica la verdad del contenido: el libro que niega un hecho falso recibió **menos** que el que lo afirma.

**Por qué no buscamos el mecanismo.** Jev es una caja negra. Podríamos encontrar una explicación para Gagarin (el anacronismo de un libro antiguo que habla de la Luna encaja con parte de los datos) y que esa explicación no sirviera para Einstein. Lo que sí queda:

- **Consistencia**: un juicio fijado da casi el mismo grado en cada réplica (±0,01–0,02).
- **Sensibilidad**: cambios pequeños de redacción o de marco («afirma» / «dice», «libro antiguo» / «libro», «fue» / «no fue») mueven el grado de forma que no se predice.
- **Por lo tanto**: las bandas y los umbrales son **heurísticos**, y el diseño de los juicios sigue líneas generales pero **se afina en cada caso de uso**, con casos de referencia y réplicas, si se quieren buenos rendimientos y consistencia.

**Qué hacer en la práctica:**

- Para juzgar lo que un texto **reporta**, usa verbos de reporte: «dice», «según». Usa «afirma» solo si quieres juzgar lo que el texto sostiene.
- Si el material puede contener errores —respuestas de estudiantes, documentos por verificar—, espera grados más bajos en el juicio sobre lo que dice, y calibra los umbrales con ese material.
- En una Choice, lee `probabilities`, no solo `choice`: lo notorio puede quitar soporte al juicio que el expediente sostiene sin cambiar la elección.
- Si un caso cae en la franja central, revisa primero el juicio y luego cómo está escrito el expediente (§3.1).

Crudos: `falso-c{1..6}-*`, `diag-scott-*`, `diag-2mas2-*`, `decimos-gagarin-*`, `libro-*`, `claves-jesus-*`, `choice-jesus-b-*`, `choice-gagarin-*`.

---

## 5. Confidence: qué es y qué no es

La confianza no debe presentarse como una garantía de exactitud individual. La Noul no devuelve `confidence`: su grado se lee directamente con las bandas del §3.1.

**Qué dice la documentación (nivel 1).** `confidence` es un estadístico calculado a partir de la distribución de probabilidades: si el soporte se concentra en un juicio, el reparto es nítido; si se reparte, no lo es. Como ejemplo da la fórmula para tres opciones, `(3 × probabilidad máxima − 1) / 2`, y aclara que es una medida práctica, no una definición cerrada: si otra medida te sirve mejor, calcúlala tú desde `probabilities`.

**Lo que reconstruimos (nivel 3).** Esta generalización reproduce nuestros datos con 2 y 4 opciones (máximo 0,52 → 0,04; máximo 0,64 → 0,51):

```python
count = len(values)
peak = max(values)
confidence = (count * peak - 1) / (count - 1)
confidence = max(0.0, min(1.0, confidence))
```

Sirve para entender qué mide la confianza. No la uses como contrato de producción: el proveedor no la publica como tal.

**Sobre calibración.** TypeSafe dice que sus modelos se entrenan para dar decisiones *calibradas* —probabilidades ajustadas para reflejar la incertidumbre— y precisa que la calibración se mide sobre grupos de predicciones y no garantiza que un resultado individual sea correcto. Eso no valida ningún umbral concreto: la propia documentación indica que el umbral depende de la acción y del dominio, y que se fija con datos propios.

La distinción importante es:

```text
confidence alta ≠ accuracy garantizada
```

Para usar un umbral se necesita un conjunto etiquetado representativo:

```text
confidence → agrupar predicciones → medir accuracy/error por grupo
```

La calibración es una propiedad estadística de grupos, no una promesa de que un caso concreto sea correcto. Conviene medir cobertura, precisión, abstención, distribución de clases, falsos positivos y falsos negativos.

Ejemplo de compuerta:

```python
if result.confidence >= 0.90:
    accept_for_automation(result)
else:
    send_to_review(result)
```

Ese umbral es una decisión del sistema. No viene validado por el hecho de que la salida sea tipada.

### La confianza baja es una señal de diseño

Como la franja central de la Noul, una confianza baja en Choice o Score no describe una duda de Jev: señala algo del diseño. Suele ser una de tres cosas:

- **el juicio está mal redactado** o desconectado del expediente;
- **los juicios de `criteria` se pisan**: el caso cabe en dos opciones o niveles;
- **el expediente no decide ese caso**: el propio texto admite dos lecturas.

En el Anexo A, la confianza baja señaló los tres casos problemáticos (0,37; 0,25; alrededor de 0,70). Cuando aparece, mira `probabilities` para ver entre qué juicios se reparte el soporte, y actúa sobre esos juicios, sobre `instructions` o sobre el flujo.

### Cuidado con los umbrales que caen sobre casos reales

Los números varían un poco entre corridas. Si el umbral queda justo donde caen casos reales, **el mismo caso cambia de camino de una corrida a otra**.

Ejemplo medido: un mensaje dio confianza 0,71 · 0,69 · 0,72 en tres réplicas. Con un umbral de 0,70, una corrida iba a revisión humana y las otras dos no.

Dos remedios:

1. coloca el umbral en una zona donde casi no caigan casos (mira la distribución de confianzas de tus datos);
2. o decide con la confianza más baja de varias réplicas.

Y dos precisiones medidas en el Anexo B:

- **Los umbrales van por primitiva.** Una Noul y una Choice que dicen lo mismo no dan la misma cifra (la Noul es más blanda).
- **Los umbrales se calibran en el idioma del corpus.** Una rúbrica traducida conserva el veredicto, pero no siempre la seguridad: el mismo mensaje dio confianza 0,79 en inglés y 0,33 en español, con el mismo nivel elegido.

---

## 6. Once límites que la documentación hace visibles

> **Actualizado el 23 de septiembre de 2026** según la página oficial [Jev 1.13 — model jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13). Versiones anteriores de esta guía resumían la lista en nueve puntos: «números» agrupaba lo que hoy son los límites 2 y 3, y la calibración débil del Score (hoy el 4) solo se trataba en §3.3. La numeración de abajo sigue la de la página oficial. En el resto de la guía los límites se citan por su nombre, no por su número, para que un cambio futuro de numeración no la desfase.

La página de jaggedness de Jev 1.13 describe límites que deben formar parte del modelo mental del lector:

1. **Lectura literal**: las palabras de alcance, las negaciones y las condiciones implícitas se leen al pie de la letra.
2. **Conteos**: Jev reconoce la forma de una respuesta, no cuenta; los errores crecen con el tamaño.
3. **Representaciones numéricas**: rinde peor con valores como hexadecimal o RGB que con descripciones semánticas, y no juzga bien la cercanía entre números. No es una calculadora fiable.
4. **Interpolación del Score**: los niveles de Score tienen una calibración numérica débil; el score no sirve para calcular magnitudes exactas (§3.3).
5. **Fechas y horas**: las trata como texto, no como cantidades ordenadas; con formatos mezclados o fechas relativas, necesitan tratamiento explícito.
6. **Indirección**: los juicios con dobles negaciones o razonamiento de varios pasos se sopesan con menos fiabilidad.
7. **Expediente grande e irrelevante** (*context rot*): el detalle ajeno distrae y perjudica.
8. **Contenido adversarial**: Jev trata el `state` como no hostil; instrucciones inyectadas en él pueden influir en el resultado.
9. **Instrucciones y criterios contradictorios**: si `instructions` y `criteria` chocan, o los juicios de `criteria` son ambiguos o incompatibles, Jev puede confundirse.
10. **Invariantes estructurales**: no hay garantía de coherencia entre primitivas ni entre juicios (una Noul da 0,22 y una Choice sí/no 0,01 para lo mismo; dos Nouls complementarias suman 1,19).
11. **Generación**: Jev no está entrenado para generar texto.

Estos límites no son una nota al pie: explican por qué la composición debe quedarse en código. Cálculos, fechas normalizadas, reglas de autorización, invariantes, transacciones y efectos externos deben tener una fuente determinista o una revisión adecuada.

### Un límite por explorar: el horizonte del conocimiento

TypeSafe no publica la fecha de corte del entrenamiento de Jev. Hicimos una exploración (nivel 3): 27 hechos fechados entre enero de 2024 y julio de 2026 (verificados con fuentes externas) y 6 hechos falsos de control, cada uno como una Noul con state vacío, en `jev-1.13.0`.

**Lo que se observó.** Los hechos de comienzos de 2024 tienden a recibir valores altos, y los más recientes, valores bajos, con una zona intermedia irregular. Algunos ejemplos:

| Hecho | Fecha | noul |
|---|---|---|
| Los Chiefs ganan el Super Bowl LVIII | feb. 2024 | 0,95 |
| SpaceX atrapa un propulsor de Starship | oct. 2024 | 0,58 |
| La OMS adopta el Acuerdo sobre Pandemias | may. 2025 | 0,69 |
| El PSG gana la Champions League | may. 2025 | 0,08 |
| España gana la final del Mundial 2026 | jul. 2026 | 0,10 |

**Lo que no permite concluir: una fecha de corte.** Versiones anteriores de la guía situaban el corte «hacia el 2T de 2025». Retiramos esa conclusión, por tres razones:

1. **Un grado bajo dice que el juicio no se sostiene, no por qué.** Puede venir de al menos cuatro causas distintas:
   - **desconocimiento**: el hecho es posterior al entrenamiento;
   - **conocimiento antiguo**: para un modelo que no vio la final de 2025, el PSG *nunca había ganado* la Champions, así que no sostener el juicio es coherente con sus hechos notorios;
   - **tasa base**: en juicios del tipo «X ganó», casi cualquier candidato concreto tiene una probabilidad baja de antemano;
   - **semántica temporal**: ver el punto 2.
2. **Quitar la fecha cambia el juicio.** «El PSG ganó la Champions 2025» es un juicio fechado. «El PSG ganó la Champions» se sopesa desde el «ahora» implícito del modelo. Son juicios distintos. Al quitar las fechas del enunciado, 7 de 33 probes se movieron 0,15 o más. (Los IDs de los juicios no llegan al modelo, así que retirar fechas de los IDs no pudo influir.)
3. **Pocas mediciones y sin réplicas.** El «borde» entre 0,69 y 0,08 descansa en un probe (OMS) que pasó de 0,42 a 0,69 al cambiar su redacción.

**Cómo debería ser una segunda versión:**

- **Parejas**: para cada hecho, un contrafáctico plausible del mismo evento («ganó el Inter» junto a «ganó el PSG»). La señal es la **brecha** entre el verdadero y el contrafáctico, no el valor absoluto.
- **Choice entre desenlaces plausibles**, con una opción de salida «no ha ocurrido / no consta».
- **Clases separadas**: resultados (solo se saben después) y anuncios programados (se pueden saber antes).
- **Controles** anteriores y posteriores al intervalo, y **réplicas**.

Solo con eso tendría sentido estimar una ventana temporal, y siempre para una versión concreta del modelo.

---

## 7. Las diez formas oficiales de decisión

La taxonomía de `use-case-map` organiza usos de Jev en diez formas. No todas tienen la misma dificultad ni el mismo nivel de validación en un proyecto concreto.

| Forma | Juicio típico | Primitiva habitual |
|---|---|---|
| Classification | «`x` pertenece a la clase ___» | `Choice` |
| Detection | «En `x` está presente el fenómeno F» | `Noul` |
| Scoring | «`x` está en el nivel ___» | `Score` |
| Routing | «`x` corresponde al flujo ___» | `Choice` + código |
| Search | «`elemento` responde a la intención I» | señal o ranking |
| Retrieval | «`pasaje` es pertinente para P» | grado por elemento |
| Ranking | «`a` debe aparecer antes que `b`» | score relativo |
| Verification | «`pasaje` ___ la afirmación A» (la sostiene / la contradice / no la trata) | `Choice` |
| ML Feature Extraction | «`x` tiene el atributo ___» | feature tipada |
| Structured Data Extraction | «El campo C de `texto` es ___» | estructura tipada |

Search, retrieval y ranking no significan que Jev sustituya un índice, un buscador o un sistema de recuperación completo. Puede aportar juicios semánticos dentro del pipeline; la recuperación, la diversidad, la deduplicación y las garantías de cobertura siguen siendo problemas de ingeniería.

Del mismo modo, una feature extraída por Jev es una señal probabilística. Antes de persistirla como dato canónico hay que especificar versión, esquema, confianza, evidencia, fecha de cálculo y política de revisión.

---

## 8. Los cuatro patterns oficiales

### Fan-out

Someter varios juicios independientes al mismo expediente y reunir los resultados.

```text
expediente ─┬─ «es una afirmación» ───┐
            ├─ «su modalidad es ___» ─┼─ resultados tipados
            ├─ «su función es ___» ───┤
            └─ «su urgencia es ___» ──┘
```

Es útil para enriquecer registros, pero la independencia operacional no implica coherencia semántica conjunta.

### Confidence routing

Usar la confianza para seleccionar el siguiente camino: automatización, revisión, otro juicio o un modelo más costoso. El umbral debe calibrarse con datos reales.

### Composite scoring

Combinar scores o señales en código para producir una decisión compuesta. La fórmula, los pesos, las normalizaciones y los límites deben ser explícitos; Jev no debe recibir un juicio que oculte toda la política.

La receta oficial tiene tres pasos: normalizar cada score dividiéndolo por (número de niveles − 1), multiplicarlo por su peso y sumar. Recuerda la sección 3.3: se combinan posiciones sobre rúbricas, no magnitudes físicas.

### Intent routing

Detectar la intención y dirigir la solicitud al flujo correspondiente. Es un caso natural de `Choice`, pero las categorías deben cubrir la distribución real y tener una ruta para ambigüedad o “desconocido”.

---

## 9. Dónde encaja frente a un LLM

Un LLM es adecuado cuando hay que generar, explicar, sintetizar, explorar alternativas o trabajar con instrucciones abiertas. Jev es atractivo cuando el trabajo puede compilarse en juicios estrechos que se repetirán muchas veces.

La diferencia no es solo de tamaño: un LLM responde; Jev sopesa. Por eso lo que se sabe del comportamiento de los LLM —por ejemplo, ante información que contradice lo que saben— sirve como analogía, no como explicación de Jev.

Un patrón híbrido frecuente es:

```text
LLM u operador
  └─ define o revisa la tarea abierta
       ↓
juicios versionados
       ↓
Jev ejecuta juicios repetitivos
       ↓
código calcula, valida, enruta y actúa
```

La etapa de compilación no elimina la necesidad de revisión. Un juicio mal redactado puede producir grados muy consistentes que no dicen lo que se quería saber.

---

## 10. Integraciones y nivel de evidencia

### MotherDuck / SQL

MotherDuck presenta Jev como una función semántica aplicable a datos tabulares, una idea cercana a una UDF probabilística. Su benchmark publicado sobre 100.000 artículos del *training split* de AG News reporta 89% de accuracy, aproximadamente 40 segundos y 0,50 USD en esa tarea concreta. Es evidencia interesante de throughput y ergonomía analítica, no una demostración general de calidad ni de generalización fuera de ese conjunto.

### pgjev / extensión PostgreSQL

La integración de terceros `jev`/`pgjev` expone funciones como `jev()`, `jev_prob()`, `jev_choice()` y `jev_score()`. El material asociado describe batching aproximado de 20 filas por request, concurrencia 16 y un `jev.threshold` por defecto de 0,5. Estos parámetros y los resultados publicados deben tratarse como características de esa integración y versión, no como contrato universal de Jev. El propio material reporta una posible caída de accuracy con batching: hay que medirla en el workload real.

### Vercel AI Gateway

La integración `typesafe-ai/jev` muestra cómo enrutar Jev mediante un gateway de IA. El gateway puede resolver credenciales, observabilidad o selección de proveedor, pero no valida la semántica de los criterios ni calibra los umbrales.

### Cloudflare Workers AI

El paquete `typesafe/jev` documenta un camino para ejecutar Jev en Workers AI. La ventaja arquitectónica es acercar el juicio a la aplicación distribuida; las restricciones reales de región, latencia, límites, versionado y tratamiento de datos deben comprobarse en el despliegue elegido.

### LangChain

`langchain-typesafe` integra Jev en flujos de LangChain, por ejemplo para routing o evaluación. Esto no convierte automáticamente una cadena de agentes en un sistema seguro. El estado, los efectos de herramientas, el control de permisos y la política de reintentos siguen requiriendo límites explícitos.

En conjunto, estas integraciones confirman un patrón de uso: **el significado puede aparecer como una columna, señal o decisión intermedia dentro de un pipeline**. No prueban que Jev deba ser la autoridad final del sistema.

---

## 11. Coste, latencia y batching

La documentación de modelos de TypeSafe asocia Jev 1.13.0 con, entre otros datos publicados, precio de entrada de 0,042 USD por millón de tokens, salida sin coste, aproximadamente 250k tokens por segundo y 1.200 requests por minuto. En los límites de contexto, `64k` corresponde al `state` más todos los juicios (*questions*, en el API), mientras que `32k` corresponde al `state` más el juicio más largo: no es un límite de salida. Estos valores dependen del modelo, el endpoint y la fecha; para producción debe fijarse una versión, especialmente si los umbrales están calibrados.

Hay una discrepancia interna en la documentación sobre el ejemplo de batching: la página de primitivas cita el cookbook *Parallel questions* con **11,5× más barato y 9,6× más rápido**, mientras que el propio cookbook, con las mismas 13 preguntas, reporta **12,2× y 10,0×**. No se debe forzar una cifra única. La conclusión segura es que reenviar el mismo estado en muchas llamadas puede ser sustancialmente menos eficiente que agrupar juicios; la ventaja de latencia puede cambiar cuando las llamadas separadas se ejecutan concurrentemente.

La latencia promocional u orientativa —por ejemplo, aproximadamente 100 ms en *How to build with System One* o 70–500 ms en materiales de marketing— no debe mezclarse con las mediciones del spike. Las mediciones propias observadas de aproximadamente 0,7–2,5 segundos pertenecen a ese entorno, transporte, carga y configuración. Antes de comparar, hay que fijar:

- endpoint y región;
- versión del modelo;
- tamaño del `state`;
- número de juicios;
- concurrencia y batching;
- tiempo de red y serialización;
- si se mide p50, p95 o tiempo total.

También existe `jev-preview`, un alias documentado en `models` que se adelanta a `jev-latest` y que actualmente apunta al mismo modelo. Al ser un alias móvil, no conviene usarlo para thresholds calibrados ni mezclar resultados de `preview` con los de una versión fijada.

---

## 12. Versionado, evaluación y operación segura

Si una decisión depende de un threshold, la versión del modelo y del juicio forma parte del dato. Un registro de producción debería conservar, como mínimo:

```json
{
  "model": "jev-1.13.0",
  "juicio_id": "ticket.area.v3",
  "criteria_version": "2026-09-21",
  "state_id": "ticket-123",
  "resultado": "billing",
  "probabilities": {
    "billing": 0.86,
    "technical": 0.09,
    "account": 0.05
  },
  "confidence": 0.79,
  "decision_path": "human_review"
}
```

Un plan mínimo de evaluación incluye:

1. conjunto etiquetado y representativo;
2. casos ambiguos y fuera de distribución;
3. matriz de errores por clase;
4. calibración por grupos de confianza;
5. prueba de sensibilidad a la redacción del juicio, a los juicios de `criteria` y a su orden;
6. revisión adversarial del `state`;
7. comparación con una línea base sencilla;
8. política de abstención y escalamiento humano;
9. monitorización de drift y de cambios de versión.

Y varios hábitos de método que las pruebas mostraron útiles:

10. **escribir la predicción antes de correr**, y que sea puntual («nivel 1»), no un rango («1–2»): un rango casi siempre acierta y por eso enseña poco;
11. **pares mínimos**: cambiar una sola cosa del caso cada vez, para saber qué movió el resultado;
12. **réplicas**: correr cada caso varias veces y reportar media, rango y desviación, no solo un número. La variación es pequeña pero real: en un cookbook de TypeSafe, 15 repeticiones dieron una desviación media de 0,0102 por juicio, y aun así un juicio osciló entre 0,43 y 0,53, cruzando el umbral de 0,5. Una variación grande (en el spike, `snorfle` dio 0,74 y luego 0,21) merece investigarse, no despacharse como ruido. Y para robustez semántica sirve la **paráfrasis**, con un cuidado: cambiar una palabra puede cambiar el juicio («afirma» no es «dice», §4.6). Una paráfrasis que conserve el sentido debería caer en la misma banda; si no cae, las palabras llevaban juicios distintos;
13. **separar ajuste y validación**: una rúbrica corregida sobre ciertos casos acierta en ellos casi por construcción. Solo un conjunto nuevo, que no se usó para ajustar, muestra si la rúbrica generaliza;
14. **distinguir sondas del modelo y pruebas de diseño**: una sonda puede usar el state de forma artificial para estudiar a Jev; una prueba de diseño usa material realista. Lo que sale de una sonda no se convierte en regla de diseño sin probarlo así;
15. **casos sencillos pero ilustrativos**: cada prueba parte de un caso mínimo que muestre con claridad una sola regla;
16. **ante la franja central, primero el diseño**: si un grado cae entre 0,30 y 0,65, revisa la redacción del juicio y su conexión con el expediente antes de interpretar el resultado.

Para permisos, herramientas, pagos, borrado de datos o acciones irreversibles, Jev puede aportar una señal de clasificación. La autorización final debe permanecer en código, política y control humano apropiado.

---

## 13. Jev para extracción y enriquecimiento documental

Un uso prometedor es producir features semánticas sobre unidades documentales:

```text
source unit
    ├─ función estructural
    ├─ es una afirmación
    ├─ modalidad
    ├─ fuerza de evidencia
    ├─ relevancia para un tema de consulta
    └─ relación con otra unidad
```

Esto puede alimentar SQL, reglas, grafos, embeddings, modelos clásicos o nuevos juicios Jev. El beneficio no es que Jev “comprenda el documento entero” de una vez, sino que puede convertir juicios locales repetibles en señales reutilizables.

El límite es decisivo: la ontología, la estructura persistida y las relaciones canónicas no deben modificarse automáticamente solo porque una salida probabilística parezca convincente. Conviene guardar candidatos, evidencia, versión y posibilidad de arbitraje humano.

---

## 14. Glosario breve

| Término | Definición pedagógica |
|---|---|
| System One Model | Modelo que emite decisiones rápidas, locales y estructuradas, sin generar texto. |
| Expediente (`state`) | El material que la aplicación somete a juicio, con un papel reconocible. |
| Juicio | Lo que Jev sopesa frente al expediente. En la Noul va en `instructions`; en Choice y Score, en `criteria`. |
| Juicios alternativos | Los juicios de `criteria` en Choice y Score, entre los que Jev reparte su soporte (100 monedas). |
| Grado de soporte | Cuánto sostendría Jev un juicio con el expediente a la vista. |
| Hechos notorios | Lo que Jev sabe del mundo y usa al sopesar, sin que el expediente lo pruebe. |
| Noul | Un solo juicio, en `instructions`; su valor es el grado de soporte de ese juicio. |
| Choice | Juicios alternativos sin orden, en `criteria`; Jev reparte su soporte entre ellos. |
| Score | Juicios alternativos como niveles ordenados, en `criteria`; su `score` es la posición media del reparto, no un nivel elegido. |
| Bandas | Lectura del grado de una Noul: de «muy seguramente falso» a «muy seguramente cierto». |
| Franja central | Grados entre 0,30 y 0,65: el juicio no se puede formar con ese expediente; es una señal de diseño. |
| Probabilities | Reparto del soporte entre los juicios de `criteria`. |
| Confidence | Qué tan concentrado está el reparto; útil para enrutar, no garantía individual de acierto. |
| Criteria | En Choice y Score, los juicios alternativos (opciones o niveles), con sus límites y ejemplos. En la Noul, opcional. |
| Instructions | Campo del API. En la Noul contiene el juicio; en Choice y Score, la pregunta que agrupa los juicios de `criteria` (puede ir vacía). |
| Fan-out | Varios juicios sobre el mismo expediente. |
| Confidence routing | Uso de la confianza para escoger el siguiente camino. |
| Composite scoring | Composición explícita de grados o scores en código. |
| Intent routing | Juicio sobre la intención para dirigir a un flujo. |
| Context rot | Degradación por exceso, irrelevancia o mala organización del expediente. |
| Type safety | Restricción de la forma del resultado; no garantiza que el juicio sea el que se quería. |
| Calibración | Comprobación de cómo se relacionan confianza y error en grupos de casos. |
| Regla de precaución | «Esto puede pasar; evítalo». Basta un caso que muestre el riesgo, porque evitarlo es barato. |
| Regla predictiva | «Esto normalmente ocurre así». Necesita varios casos y, si es posible, más de un dominio. |
| Sonda del modelo | Experimento para estudiar a Jev; puede usar el expediente de forma artificial. |
| Prueba de diseño | Experimento para decidir cómo usar Jev en una aplicación; usa material realista. |

---

## 15. Conclusión

Jev se entiende mejor como un **juez** intermedio entre lenguaje y software:

```text
expediente + juicio
        ↓
grado de soporte, tipado y probabilístico
        ↓
reglas, composición, validación y acción en código
```

Su promesa no es que un juicio convierta cualquier decisión compleja en segura. Su promesa es permitir que determinados juicios semánticos repetitivos entren en pipelines ordinarios con un resultado que el programa puede inspeccionar y combinar.

Diseñar con Jev es, sobre todo, **redactar bien dos cosas**: el juicio exacto que se quiere sopesar y el expediente frente al que se sopesa. Cuando el grado no es el esperado, lo primero es preguntarse si el juicio es el que se quería y cómo está escrito el expediente.

Jev es consistente —un juicio fijado da casi el mismo grado cada vez— pero sensible: una palabra del juicio o del marco del expediente puede mover el grado, y el modelo es una caja negra. Por eso las bandas y los umbrales son heurísticos, y el diseño sigue líneas generales que **se afinan en cada caso de uso**, con casos de referencia y réplicas.

La frontera sana es:

> **Jev sopesa; el sistema decide.**

Y quien consume lo que Jev sopesa es el sistema: usado correctamente, Jev es transparente para el usuario.

Cuando el juicio es estrecho, el expediente está disponible, los juicios alternativos son explícitos y existe evaluación, Jev merece una prueba. Cuando la tarea exige investigación, deliberación prolongada, aritmética, invariantes globales o autoridad sobre efectos irreversibles, hay que dividirla y dejar esas responsabilidades fuera del modelo.

---

## Anexo A. Caso trabajado: ¿qué tan urgente es este mensaje?

Este anexo cuenta, paso a paso, cómo se diseñó una escala de Score, qué falló y cómo se corrigió. Incluye los errores: son la parte más instructiva. Todas las cifras son mediciones propias (nivel 3) con `jev-1.13.0`; los crudos están en `spike-jev/cache/`.

### Paso 1. El punto de partida

El mensaje:

```text
Gosh, did you get a chance to review what I sent you yesterday?
```

Es un recordatorio con algo de impaciencia, sin plazo y sin consecuencia. La primera escala de urgencia tenía cuatro niveles:

| Nivel | Descripción (resumida) |
|---|---|
| 0 | No urgente: sin fecha ni consecuencia; da igual hoy o en un mes. |
| 1 | Poco urgente: bien esta semana; nada se rompe si se demora. |
| 2 | Urgente: la demora tiene un costo visible para alguien. |
| 3 | Muy urgente: hay una pérdida concreta e inmediata. |

Antes de correr nada, la revisión encontró cuatro problemas:

1. **Mezcla dos dimensiones**: los niveles 0–1 hablan de plazo; los 2–3, de costo.
2. **Describe el mundo, no el texto**: el mensaje no dice si «da igual hoy o en un mes».
3. **Falta un nivel**: un recordatorio sin plazo no encaja en ninguno.
4. **Juicio vago**: «urgency of the message» no dice urgencia *de quién*.

### Paso 2. Probar con pares mínimos

En lugar de un solo mensaje, se probaron seis variantes. Cada una cambia **una sola cosa** respecto al original. Además de la escala original, se añadieron dos escalas de una sola dimensión: **horizonte** (¿para cuándo espera respuesta el remitente?) y **costo** (¿qué consecuencia tiene la demora?). Tres réplicas por variante.

| Variante | Qué cambia | Horizonte | Costo | Escala original |
|---|---|---|---|---|
| v0 | nada (referencia) | 1,05 | 0,99 | 1,00 |
| v1 | sin «Gosh» | 1,05 | 0,97 | 1,00 |
| v2 | sin «yesterday» | 1,00 | 0,99 | **0,68** |
| v3 | + «The client is waiting on it.» | **1,75** (conf 0,37) | 1,88 | 2,00 |
| v4 | + «I need it by 5pm today.» | 3,00 | 1,17 | 2,38 (conf 0,62) |
| v5 | «No rush at all: whenever you get a chance…» | 0,02 | **0,67** | 0,35 |

Qué enseñó esta tabla:

- **La interjección no pesa.** Quitar «Gosh» no movió nada (≤ 0,03).
- **La escala mixta es frágil.** Quitar «yesterday» la bajó de 1,00 a 0,68; las escalas de una dimensión no se movieron. Con el plazo explícito (v4), la escala mixta dudó entre dos niveles; el horizonte, no (3,00 con confianza 1,00).
- **Un score intermedio puede engañar.** En v3, el horizonte 1,75 parece «en los próximos días», pero ese nivel tenía solo 0,03. El soporte se repartía entre «sin plazo» (0,61) y «hoy» (0,34). Es el caso B de la sección 3.3.
- **Un ejemplo puede contaminar.** En v5, el costo dio 0,67 en vez de 0. El ejemplo del nivel 1 era «Let me know when you can», casi igual al mensaje.

### Paso 3. Corregir la escala de costo

La escala de horizonte funcionó desde el principio. La de costo necesitó cuatro versiones. Cada fila muestra qué se cambió y qué falló.

| Versión | Idea central | v0 | v3 | v5 | Qué falló |
|---|---|---|---|---|---|
| 1 | 0 sin consecuencia · 1 alguien espera · 2 bloqueo · 3 pérdida | 0,99 | 1,88 | 0,67 | El ejemplo del nivel 1 se parecía a v5. |
| 2 | nivel 1 = «solo el remitente espera; nadie más; nada bloqueado» | 0,78 (conf 0,77) | — | — | Esperar no es una consecuencia de la demora: *es* la demora. Y el nivel tenía tres negaciones. |
| 3 | fusionar 0 y 1: «a lo sumo, alguien espera» | 0,00 | **0,50** (conf 0,25) | 0,00 | «El cliente espera» cabía en dos niveles a la vez. |
| 4 | frontera: **solo el remitente / alguien más** | 0,01 | 1,00 | 0,00 | — |

(Las versiones 2 a 4 se corrieron una sola vez.)

La lección de este paso: **cuando Jev reparte su soporte en partes iguales, casi siempre hay dos niveles que se pisan.** La salida no es forzar a Jev, sino escribir la frontera. «Un tercero que espera cuenta como costo» es una decisión de política: podría haberse decidido lo contrario, pero había que decidir.

La escala final:

| Nivel | Horizonte (¿para cuándo?) | Costo (¿a quién afecta la demora?) |
|---|---|---|
| 0 | Sin expectativa de tiempo | Solo al remitente, que espera respuesta |
| 1 | Espera respuesta, sin plazo (incluye «alguien espera») | Alcanza a alguien más: un cliente, un equipo, un proceso |
| 2 | En los próximos días | Se declara una pérdida concreta e inmediata |
| 3 | Hoy | — |
| 4 | Ya mismo | — |

### Paso 4. Validar con mensajes nuevos

Cuatro versiones sobre los mismos mensajes tienen un riesgo: la escala puede acertar solo porque se ajustó a ellos. Para saber si generaliza, se probaron **ocho mensajes nuevos**, con la predicción escrita antes y tres réplicas cada uno.

| Mensaje | Predicción (H / C) | Horizonte | Costo |
|---|---|---|---|
| h1 «Hey, any update on the budget file?» | 1 / 0 | 1,00 | 0,06 |
| h2 «My boss asked me again about the report.» | 1 / 1 | 1,06 | 1,00 |
| h3 «Legal can't send the contract until you approve the draft.» | 1 / 1 | 1,01 (conf ≈ 0,70) | 0,85 (conf 0,77) |
| h4 «Please send it by Thursday.» | 2 / 0 | 2,00 | 0,14 |
| h5 «The launch is on Monday and your section is still missing.» | 2 / 1–2 | 2,19 | 1,01 |
| h6 «If we don't pay the supplier today, they cancel the order.» | 3 / 2 | 3,00 | 2,00 |
| h7 «Whenever you can, no pressure.» | 0 / 0 | 0,00 | 0,00 |
| h8 «The client is waiting on the quote.» | 1 / 1 | 1,05 | 1,00 |

Resultado: **8 de 8** con el pico en el nivel predicho. Dos observaciones:

- **h3** es el caso más blando. Las dos escalas repartieron en la misma proporción (≈ 0,2 hacia su nivel 0). Probablemente el mensaje admite dos lecturas: petición o simple información (ver sección 4.4). Además, su confianza (0,71 · 0,69 · 0,72) cae justo sobre un umbral de 0,70: es el ejemplo de la sección 5.
- **h5** aprobó con facilidad porque la predicción fue un rango (1–2). Un rango enseña poco.

### Paso 5. Lo que salió mal (y por qué importa)

De 18 predicciones escritas en el paso 2, cinco fallaron. La más reveladora: se esperaba que el soporte se repartiera entre la lectura al pie de la letra («no hay plazo, luego no es urgente») y la de una persona («si insiste, alguien espera»). No se repartió: se concentró en la segunda, con confianza 0,94. Sin la predicción escrita, este aprendizaje se habría perdido: cualquier resultado habría parecido razonable después.

### Resumen de lecciones

| Lección | Dónde se explica |
|---|---|
| El score es un punto medio; con confianza baja, lee `probabilities`. | 3.3 |
| Una dimensión por escala; niveles sobre el texto, sin solaparse, sin dobles negaciones ni indirección; ejemplos sin parecido con el material. | 3.4 |
| Juicios separados pueden heredar la misma ambigüedad del mensaje (hipótesis). | 4.4 |
| La confianza baja es una señal de diseño; un umbral sobre casos reales enruta de forma inestable. | 5 |
| Predicción puntual y escrita, pares mínimos, réplicas, validación con casos nuevos. | 12 |

### Límites de este caso

Una sola familia de mensajes, en inglés, un solo modelo y ocho mensajes de validación. Falta probarlo en español —el idioma del corpus real— y con más casos antes de fijar umbrales.

Crudos: `urg-v0…v5-r1…r3.json` (paso 2), `urg-rubrica2-v0.json`, `urg-costo3-*.json`, `urg-costo4-*.json` (paso 3), `urg-holdout-h1…h8-r1…r3.json` (paso 4).

---

## Anexo B. Pruebas de reglas

Cada prueba parte de un caso sencillo pero ilustrativo, con las predicciones escritas antes de correr. Todas las cifras son mediciones propias con `jev-1.13.0`, con 3 réplicas por caso; los crudos están en `spike-jev/cache/`.

### Prueba 1. ¿Funcionan las reglas de diseño en otro idioma y en otro dominio?

**Qué se quería saber.** Si las reglas del §3.4, nacidas con un caso de urgencia en inglés, sirven para diseñar escalas que funcionen al primer intento en español y en un tema distinto.

**Dominio nuevo: la fuerza con que un texto afirma algo.** Material: una sola afirmación sobre un fármaco ficticio (*nortavel*) dicha de quince maneras, de «Quizá el nortavel reduzca la fiebre» a «No cabe duda de que…», y con distintos apoyos: ensayos con código (NTV-201…), una cita con autor y año, un registro público, «varios estudios», «los expertos», una anécdota.

**Paso 1, con Nouls** (crudos `noul-fuerza-*`). Dos Nouls por frase, en español y en inglés: «`texto` asevera categóricamente que…» y «`texto` apoya la afirmación en evidencia identificable…».

- **Idioma**: en los casos claros, mismo resultado en ambos idiomas (9 de 9). En los casos de borde, el español fue algo más generoso con la evidencia.
- **Dos dimensiones separadas**: «Según los ensayos…, *podría*…» → certeza 0,14, evidencia 0,92; «Los ensayos… *muestran*…» → 0,92 y 0,93.
- **Evidencia graduada**: de los ensayos con código (0,93) a la cita (0,86), el registro (0,82), «varios estudios» (0,36), los expertos (0,11) y la anécdota (0,07). «Está demostrado» (0,18) no cuenta como evidencia: invoca una prueba sin mostrarla.
- **Negaciones en el material**: «No es seguro que…» → 0,02; «No cabe duda de que…» → 0,97.
- **Un hallazgo del lenguaje, no del modelo**: atribuir la afirmación a otros («varios estudios muestran») la vuelve algo menos categórica (0,80 frente a 0,95). La fuente y la fuerza de una afirmación están ligadas en el propio lenguaje.

**Paso 2, con Scores** (crudos `score-urg-es-*`, `score-fuerza-es-*`).

- **Urgencia en español**: la rúbrica final del Anexo A, traducida, eligió el mismo nivel que en inglés en **8 de 8** mensajes, en las dos escalas. Pero la seguridad no siempre se conserva: un mensaje dio confianza 0,79 en inglés y 0,33 en español.
- **Dos escalas nuevas en español** —*certeza* (5 niveles) y *verificabilidad* (4 niveles)—, escritas con las reglas del §3.4 y con ejemplos sobre otro tema (un puente): **25 de 25** aciertos en los casos claros, sin retoques. La confianza bajó solo en los dos casos marcados de antemano como dudosos («Está demostrado», entre firme y enfática; el registro público, entre evidencia vaga y fuente localizable).

**Qué quedó establecido**: las reglas del §3.4 funcionan como heurística de partida en dos dominios y dos idiomas; los umbrales se calibran en el idioma del corpus. Matiz: las escalas se escribieron después de ver cómo leía Jev esas frases en el paso 1, así que no fue una prueba del todo a ciegas.

### Prueba 2. ¿Qué decide lo que Jev juzga: la redacción del juicio o la primitiva?

**Qué se quería saber.** Si la divergencia entre Noul y Choice del §4.5 venía de la primitiva o de que el juicio no decía qué se juzgaba.

**Material realista**: un folleto de viaje, en dos versiones idénticas salvo la ciudad (crudos `objeto-*`):

> «Australia combina playas extensas y desiertos rojos. Su capital, **Sídney** / **Canberra**, es una ciudad moderna y ordenada. La mejor época para visitarla va de septiembre a noviembre.»

**Dos objetos de juicio, cada uno como Noul y como Choice**: qué dice el folleto sobre la capital, y si ese dato es correcto.

| Folleto | Objeto | Noul | Choice |
|---|---|---|---|
| dice Sídney | qué dice | 0,82 | «Sídney» 1,00 |
| dice Sídney | ¿es correcto? | 0,11 | «incorrecto» 0,99 |
| dice Canberra | qué dice (¿Sídney?) | 0,01 | «Canberra» 1,00 |
| dice Canberra | ¿es correcto? | 0,94 | «correcto» 1,00 |

**Qué quedó establecido**: en los cuatro casos, Noul y Choice quedan del mismo lado; al cambiar el objeto, cambian juntas. Lo decisivo es **qué se juzga**, y eso se escribe en el juicio. Dos observaciones: la Noul es más blanda que la Choice (no se comparan magnitudes), y el 0,82 de «qué dice» es bajo para un juicio sobre el texto. La prueba 3 aclaró por qué: no era una presuposición, sino que el dato choca con lo notorio.

### Prueba 3. El juicio sobre lo que dice un expediente

**3a · Cómo nombrar el material** (crudos `nombrar-*`). Sobre el folleto que dice «Canberra», el mismo juicio con cuatro formas de nombrar el material —«`folleto` afirma…», «El folleto afirma…», «El texto afirma…», «El documento afirma…»—, cada una para Canberra (lo dice) y para Sídney (no lo dice).

- Las cuatro formas dieron **0,98** para Canberra y **0,01–0,02** para Sídney. Con un solo campo, la forma de nombrar el material da igual.
- Un resultado de rebote: con la misma construcción («Su capital, X, es una ciudad moderna y ordenada»), «`folleto` afirma que la capital de Australia es X» dio **0,98** con Canberra y **0,82** con Sídney (prueba 2). La construcción es idéntica; solo cambia que el dato choque con lo notorio. Eso descartó la presuposición como explicación del 0,82.

**3c · Expedientes que chocan con lo notorio** (crudos `falso-c{1..6}-*`). Seis notas breves, cada una en dos versiones idénticas salvo un dato, y sobre cada versión dos juicios: «`nota` afirma [el dato notorio]» y «`nota` afirma [el dato que choca]».

| Caso | Nota con el dato notorio → juicio sobre ese dato | Nota con el dato que choca → juicio sobre ese dato |
|---|---|---|
| ballena (mamífero / pez) | 0,99 | 0,92 |
| Quijote (Cervantes / Lope) | 0,97 | 0,76 |
| colores (verde / morado) | 0,98 | 0,76 |
| Canadá (Ottawa / Toronto) | 0,97 | 0,64 |
| Polo Sur (Amundsen / Scott) | 0,91–0,92 | 0,45–0,51 |
| Luna (Armstrong / Gagarin) | 0,94–0,95 | 0,36–0,43 (seis réplicas, dos días) |

Los juicios sobre lo que la nota **no** dice quedaron entre 0,01 y 0,04 en todos los casos. La estructura (aposición o aseveración directa) no marcó diferencia.

**Diagnóstico con Scott** (crudos `diag-scott-*`), cambiando solo la redacción del juicio: «afirma» ~0,50; «dice» y «según» ~0,70; en inglés, «states» ~0,56. **Con «2+2=5»** (crudos `diag-2mas2-*`): «`texto` afirma que 2+2=5» y «`texto` dice que 2+2=5» dieron ambos 0,97.

**Qué quedó establecido**: Jev sopesa el juicio sobre lo que dice un expediente junto con sus hechos notorios; cuando el expediente choca con ellos, el grado baja (6 de 6 casos) y a veces cae en la franja central. El verbo del juicio cuenta. La hipótesis de que bajara más cuanto más se contradice el propio expediente quedó retirada en la prueba 7.

### Prueba 6. ¿Dónde viven los juicios en una Choice?

**Qué se quería saber.** Si en una Choice lo que Jev sopesa está en la pregunta de `instructions` o en los `criteria`. La documentación mezcla las dos lecturas: llama al campo «the question the model answers» y también «the judgment to evaluate».

**Material** (crudos `vacio-*`): el folleto que dice «Su capital, Canberra, es una ciudad moderna y ordenada…», con los `criteria` escritos como juicios completos («`folleto` dice que la capital de Australia es Sídney», «…es Canberra», «…otra ciudad o no dice cuál es») y tres versiones de `instructions`: la pregunta normal, solo el nombre del campo (`` `folleto` ``) y vacío (`""`).

| `instructions` | P(Canberra) | P(Sídney) | P(otra) | confidence |
|---|---|---|---|---|
| «¿Cuál es la capital de Australia según `folleto`?» | 1,00 | 0,00 | 0,00 | 1,00 |
| «`folleto`» | 1,00 | 0,00 | 0,00 | 1,00 |
| `""` (vacío) | 1,00 | 0,00 | 0,00 | 1,00 |

El API aceptó `instructions` vacío, y el reparto fue idéntico en las nueve llamadas.

**Qué quedó establecido**: en una Choice, **los juicios viven en `criteria`**, y Jev opera sopesándolos, no respondiendo la pregunta. El caso es claro y el reparto satura, así que la prueba no mide el peso de la pregunta en casos difíciles, que seguramente lo tiene; lo que muestra es de qué tipo es la operación. Consecuencia de diseño: el esfuerzo de redacción va a `instructions` en la Noul y a `criteria` en Choice y Score.

### Prueba 7. El expediente como relato, y cuánto se asoma lo notorio

**Qué se quería saber.** Hasta dónde lo que Jev sabe se interpone en el juicio sobre lo que dice un expediente, cuando el expediente es un relato en prosa y no una nota con un solo campo. Salvo en 7a, las llamadas llevan el `state` como texto, sin campos; todas con 3 réplicas. Fue una serie exploratoria: a diferencia de las pruebas anteriores, no se escribieron predicciones antes de correr.

**7a · La hipótesis de coherencia interna** (crudos `decimos-gagarin-*`). Expediente con un campo `nota` reducido a la sola oración «Yuri Gagarin fue la primera persona en caminar sobre la Luna.». «`nota` afirma que…» dio 0,13 / 0,22 / 0,23: más bajo que con la nota completa (0,36–0,43). La hipótesis del §4.6 (versión 7) queda retirada. «Decimos que Yuri Gagarin fue…» dio 0,03 en las tres réplicas: sin nombrar el material, el juicio se sopesa contra lo notorio.

**7b · Relato con Noul** (crudos `libro-gagarin-*`, `libro-frat-*`, `libro-frat-isla-*`, `libro-frat-isla-sin-*`, `libro-jesus-*`).

| Lo que el libro señalaba | Juicio | Grado |
|---|---|---|
| Gagarin caminó en la Luna | «El libro antiguo dice que…» | 0,85 / 0,85 / 0,87 |
| Frat caminó en la Luna | «El libro antiguo dice que…» | 0,89 / 0,89 / 0,90 |
| Frat encontró la isla de los durmientes | «El libro antiguo dice que…» | 0,92 / 0,92 / 0,93 |
| Frat encontró la isla de los durmientes | «Frat encontró la isla de los durmientes.» | 0,72 / 0,72 / 0,73 |
| Jesús murió crucificado | «Un libro antiguo señalaba que…» | 0,86 / 0,86 / 0,86 |

**7c · ¿Llegan las claves al modelo?** (crudos `claves-jesus-*`). El caso Jesús, cambiando solo la clave del juicio: `q1` 0,86 / 0,86 / 0,87; `libro_senalaba` 0,86 / 0,86 / 0,86; `falso` 0,85 / 0,85 / 0,85. Una clave que sugiere el veredicto no mueve el grado: se confirma lo que dice la documentación.

**7d · Relato con Choice** (crudos `choice-jesus-b-*`, `choice-gagarin-*`, `choice-gagarin-no-*`, `choice-gagarin-libro-*`). `instructions` vacío; `criteria`: a = «Un libro [antiguo] señalaba que…», b = «No hay evidencia de que un libro [antiguo] señalara que…». Resultados en la tabla del §4.6: Jesús 0,99; Gagarin «fue» 0,84–0,87; «no fue» 0,80–0,82; sin «antiguo», 0,93–0,95 y 0,91–0,93.

**Qué quedó establecido**:

- las claves no llegan al modelo (oficial, ahora también medido);
- con el expediente como relato, el juicio sobre lo que el relato dice queda por debajo de 1,00, casi con independencia del contenido;
- en una Choice, lo notorio y el marco se asoman en el reparto aunque `choice` no cambie;
- no se busca el mecanismo: el modelo es una caja negra, y una explicación que sirva para un caso puede no servir para otro. Lo que se retiene es la consistencia entre réplicas, la sensibilidad a la redacción y al marco, y que el diseño se afina por caso de uso.

---

## Anexo C. Registro de reglas

Este anexo reúne en tablas todas las reglas de la guía. Es para consultar al diseñar: «voy a escribir una Choice, ¿qué debo tener en cuenta?».

### Cómo leer el registro

Hay **dos clases** de reglas:

- **Precaución** (P): «esto puede pasar; evítalo». Basta **un caso** que muestre el riesgo, porque evitarlo cuesta poco.
- **Predictiva** (Pr): «esto normalmente ocurre así». Necesita **varios casos** y, si es posible, más de un dominio o idioma.

Cada regla tiene además un **ámbito**:

- **modelo**: dice cómo se comporta Jev;
- **diseño**: dice cómo usarlo en una aplicación.

Y un **estado**, según su respaldo:

| Estado | Qué significa |
|---|---|
| oficial | lo dice la documentación de TypeSafe |
| sostenida | probada con material realista, en más de un caso |
| medida | observada en nuestros datos, con pocos casos |
| aceptada | razonamiento sólido, sin prueba específica |
| conjetura | hipótesis por probar |

Recuerda: son heurísticas. Una regla «sostenida» es una buena apuesta de partida, no una garantía.

### Nivel modelo (vale para cualquier primitiva)

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Jev sopesa juicios frente a un expediente; no responde preguntas, no extrae datos, no dice verdadero o falso. | P | modelo | aceptada | §1 |
| **Lo que Jev juzga va en `instructions` (Noul) o en `criteria` (Choice, Score)**; se sopesa solo con lo notorio (expediente vacío) o con un estado de cosas más lo notorio. | P | diseño | aceptada + medida | §1, Anexo B, P6 |
| Jev sopesa con el expediente **y** con sus hechos notorios. | Pr | modelo | sostenida | §1, §4.6, Anexo B, P2–P3 |
| Usa Jev para juicios estrechos, repetibles y evaluables; descompón lo que no se pueda escribir así. | P | diseño | oficial | §2 |
| Jev sopesa; el código decide. Reglas, cálculos, permisos y efectos quedan en código. | P | diseño | oficial | §12 |
| **Jev es transparente para el usuario**: lo que devuelve lo consume el sistema, no una persona. No muestres el grado al usuario como respuesta; sí al operador y al auditor. | P | diseño | oficial + aceptada | §1, §12 |
| No delegues aritmética, conteos ni fechas. | P | diseño | oficial | §6 |
| En el expediente va material con un papel reconocible, nombrado por ese papel, y solo lo pertinente. | P | diseño | oficial + aceptada | §4.1 |
| Trata el contenido del expediente como dato, no como instrucciones. | P | diseño | oficial | §4.1 |
| Usa nombres de campo neutros, que describan el papel del dato y no sugieran el veredicto. | P | diseño | aceptada | §4.4 |
| Escribe el juicio exacto que quieres: cada palabra forma parte de él («afirma» ≠ «dice» ≠ «según»). | Pr | modelo | medida | §4.3, §4.6, Anexo B, P3 |
| Escribe el juicio directamente, sin «es verdadero que» ni «es falso que». | P | diseño | aceptada | §3.1 |
| Redacta el juicio de modo que el grado alto sea lo que buscas. | P | diseño | oficial | §4.3 |
| Evita dobles negaciones e indirección compleja en el juicio. | P | diseño | oficial | §4.3, §6 |
| Jev lee al pie de la letra las palabras de alcance, las negaciones y las condiciones implícitas: escribe exactamente lo que quieres decir. | Pr | modelo | oficial | §4.3, §6 |
| `instructions` y los juicios de `criteria` no deben contradecirse. | P | diseño | oficial | §4.3, §6 |
| Nombra el material cuando el juicio es sobre él; la forma natural da igual; con varios campos, usa el nombre del campo entre backticks. | P | diseño | medida | §4.3, Anexo B, P3 |
| Si el juicio es ambiguo, desambígualo en su redacción; no lo dejes al expediente. | P | diseño | aceptada | §4.4 |
| Fija la versión del modelo; no uses `jev-preview` con umbrales calibrados. | P | diseño | oficial | §11 |
| Los IDs de los juicios no llegan al modelo. | Pr | modelo | oficial + medida | §6, Anexo B, P7 |
| Juicios sobre un mismo expediente se sopesan por separado: agruparlos no cambia sus grados. | Pr | modelo | oficial + medida | §8 |
| En los casos claros, un juicio en español da el mismo resultado que en inglés. | Pr | modelo | sostenida | Anexo B, P1 |
| Las negaciones dentro del material se leen bien («no es seguro», «no cabe duda»). | Pr | modelo | medida | Anexo B, P1 |
| Con juicios bien redactados, las réplicas casi no varían. | Pr | modelo | sostenida | Anexo B, P1–P7 |
| Cuando el expediente dice algo que choca con lo notorio, el grado del juicio sobre lo que dice baja, y puede caer en la franja central. | Pr | modelo | sostenida (6 de 6) | §4.6, Anexo B, P3 |
| Para juzgar lo que un texto reporta, usa verbos de reporte («dice», «según»); «afirma» juzga lo que sostiene. | P | diseño | medida | §4.6, Anexo B, P3 |
| Con el expediente como relato («un hombre encontró un libro que señalaba…»), el juicio sobre lo que el relato dice queda por debajo de 1,00 (0,85–0,93), casi con independencia del contenido. | Pr | modelo | medida | §4.6, Anexo B, P7 |
| Un juicio fijado da casi el mismo grado en cada réplica, pero cambios pequeños de redacción o de marco lo mueven de forma que no se predice. No busques el mecanismo: afina con casos de referencia. | Pr | modelo | sostenida | §4.6, Anexo B, P3, P7 |
| Un expediente irrelevante no mueve el juicio. | Pr | modelo | conjetura | §4.4 |
| Un expediente pertinente resuelve la ambigüedad de un juicio. | Pr | modelo | conjetura | §4.4 |
| El expediente pesa más cuando, sin él, el juicio cae en la franja central (medido en log-odds). | Pr | modelo | conjetura | §4.4 |

### Noul

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Una Noul somete un solo juicio (en `instructions`) y devuelve su grado de soporte; no reparte entre «sí» y «no». | P | modelo | oficial + aceptada | §3.1 |
| Lee el grado por bandas: muy seguramente cierto · seguramente · hay bases · no se puede formar juicio · base no firme · muy seguramente falso. | P | diseño | aceptada | §3.1 |
| **La franja central (0,30–0,65) es una señal de diseño**, no incertidumbre de Jev: revisa la redacción del juicio y su conexión con el expediente. | P | diseño | aceptada + medida | §3.1, §4.6 |
| Un grado bajo dice que el juicio, tal como está redactado, no se sostiene; no distingue contradicción de silencio. | P | modelo | aceptada | §3.1 |
| Para distinguir contradicción de silencio, usa dos Nouls sobre juicios contrarios o una Choice con salida. | P | diseño | aceptada | §3.1 |
| Nouls que parecen complementarias no tienen por qué sumar 1. | P | modelo | oficial | §3.1 |
| Una Noul por dimensión: dos ideas que se confunden van en dos Nouls. | P | diseño | sostenida | §3.1, Anexo B, P1 |
| Redacta el juicio de la Noul como un enunciado, no como una pregunta. | P | diseño | aceptada | §3.1, §4.3 |
| Para sondear los hechos notorios de Jev, usa el expediente vacío. | P | diseño | aceptada | §4.4 |
| Una Noul distingue grados de evidencia: identificable, vaga, de autoridad, anecdótica. | Pr | modelo | medida (un dominio) | Anexo B, P1 |
| Invocar una prueba sin mostrarla («está demostrado») no cuenta como evidencia identificable. | Pr | modelo | medida | Anexo B, P1 |

### Choice

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| En Choice y Score, **los juicios viven en `criteria`**; Jev reparte su soporte entre ellos. No responde, y `choice` no es una decisión suya: es el juicio con más soporte. | Pr | modelo | medida | §1, §3.2, Anexo B, P6 |
| `instructions` agrupa los juicios de `criteria` como alternativas y puede ir vacío (en un caso claro, el reparto no cambió). Su peso en casos menos claros es una cuestión abierta. | Pr | modelo | medida (un caso) | §4.3, Anexo B, P6 |
| Redacta cada opción de `criteria` como un juicio, con las mismas reglas que el juicio de una Noul. | P | diseño | aceptada | §3.2, §4.2 |
| Juicios de `criteria` explícitos, cada uno con su descripción. | P | diseño | oficial | §3.2, §4.2 |
| Incluye una opción de salida: puede que ningún juicio se sostenga. Sin ella, lo que no encaja cae igual en el mejor juicio y la confianza no lo detecta (medido con classifier.dev, mismo modelo). Cuando alguna encaja, la salida no roba soporte (≤ 0,01 en la prueba 2). | P | diseño | oficial + medida | §3.2, Anexo B, P2 |
| Para juicios cercanos, usa `what` / `not_for` / `examples`. | P | diseño | oficial | §4.2 |
| El menú es parte del juicio: cambiar los juicios de `criteria` puede cambiar el reparto. | Pr | modelo | medida (un caso) | §4.5 |
| Lo notorio y el marco del expediente se asoman en el reparto: pueden quitar soporte al juicio que el expediente sostiene sin cambiar `choice`. Lee `probabilities`, no solo `choice`. | P | modelo + diseño | medida | §4.6, Anexo B, P7 |

### Score

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| En un Score, los juicios de `criteria` son niveles ordenados; el score es la posición media del reparto, no una medida. | P | modelo | oficial | §3.3 |
| Con confianza baja, lee `probabilities`, no `score`. | P | diseño | medida | §3.3 |
| Una sola dimensión por escala. | P | diseño | oficial + sostenida | §3.4 |
| Niveles sobre lo que el texto dice o insinúa, sin solaparse, sin dobles negaciones ni indirección. | P | diseño | sostenida + oficial | §3.4 |
| Si una frontera es discutible, escríbela en la rúbrica como decisión. | P | diseño | sostenida | §3.4, Anexo A, Anexo B, P1 |
| Los ejemplos de los niveles no deben parecerse al material evaluado. | P | diseño | medida (basta para P) | §3.4 |
| Cubre el caso intermedio frecuente. | P | diseño | medida | §3.4 |
| La fuente y la fuerza de una afirmación están ligadas en el lenguaje; si tu escala debe separarlas, dilo en la rúbrica («venga de quien venga»). | P | diseño | medida | §3.4, Anexo B, P1 |
| Marca de antemano los casos dudosos: en una escala bien diseñada, la confianza baja se concentra en ellos. | Pr | diseño | sostenida | Anexo B, P1 |
| Una escala diseñada con estas reglas funciona al primer intento en otro dominio e idioma. | Pr | diseño | sostenida | Anexo B, P1 |
| Combina Scores en código: normaliza y pondera. | P | diseño | oficial | §3.3, §8 |

### Entre primitivas

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Elige la primitiva por la forma del juicio: cerrado → Noul; abierto sin orden → Choice; abierto con niveles ordenados → Score. | P | diseño | aceptada | §1, §4.5 |
| **Escribe en el juicio qué se juzga; la primitiva solo decide la forma del resultado.** | Pr | diseño | sostenida | §4.5, Anexo B, P2 |
| Si el objeto del juicio queda implícito, Noul y Choice pueden divergir, y en cualquier dirección. | P | modelo | oficial + medida | §4.5 |
| Con el mismo material, «qué dice» y «si es correcto» son juicios distintos; Jev los separa. | Pr | modelo | sostenida | §4.5, Anexo B, P2 |
| La Noul es más blanda que la Choice: no compares magnitudes, compara lo que dice cada una. | Pr | modelo | medida | §4.5, Anexo B, P2 |

### Operación

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Confianza alta no garantiza acierto; la calibración vale para grupos de casos. | P | modelo | oficial | §5 |
| La confianza baja (y la franja central de la Noul) es una señal de diseño: juicio mal redactado, juicios de `criteria` que se pisan o un caso que el expediente no decide. | P | diseño | medida | §3.1, §5 |
| Los umbrales se fijan por acción y dominio, con datos propios. | P | diseño | oficial | §5 |
| No pongas un umbral sobre un grupo de casos reales. | P | diseño | medida | §5 |
| Los umbrales van por primitiva y se calibran en el idioma del corpus. | P | diseño | medida | §5, Anexo B, P1 |
| Si el material puede contener errores, calibra los umbrales con ese material: el juicio sobre lo que dice baja. | P | diseño | medida | §4.6, Anexo B, P3 |
| Compara efectos en log-odds, con líneas base medidas. | P | diseño | aceptada | §4.4 |
| Reporta réplicas con media y rango; en paráfrasis, recuerda que cambiar una palabra puede cambiar el juicio. | P | diseño | oficial + aceptada | §12 |
| **Las bandas de la Noul y los umbrales de confianza son heurísticos**: orientan la lectura; no son valores calibrados. | P | diseño | aceptada + medida | §3.1, §4.6, §5 |
| **El diseño de los juicios sigue líneas generales, pero se afina en cada caso de uso**, con casos de referencia y réplicas, si se quieren buenos rendimientos y consistencia. | P | diseño | sostenida | §4.6, Anexo B, P1–P7 |

### Pendientes, resueltas y retiradas

**Por probar:** nada pendiente por ahora.

**Cuestión abierta (no se determina por ahora):** el peso de la pregunta de `instructions` en Choice y Score cuando el caso no es claro.

**Resueltas:** «¿dónde viven los juicios en una Choice?» (en `criteria`; `instructions` puede ir vacío, Anexo B, P6; con ello se descartó la prueba sobre escribir el campo como juicio abierto o como pregunta); «¿qué pasa en una Choice sin opción de salida?» (cubierta por la documentación y por lo medido con classifier.dev; no requiere prueba propia); «¿aseveración o presuposición?» (el 0,82 del folleto de Sídney): no era la presuposición, sino el choque con lo notorio (Anexo B, P3a).

**Retiradas:** «un state impreciso contamina» (§4.4), «la primitiva elige el mundo de referencia» (§4.5), la fecha de corte «hacia el 2T de 2025» (§6), la lectura de la franja central como «no sé» o como «duda» de Jev (§3.1), «baja más cuanto más se contradice el propio expediente» (§4.6; la nota reducida a la sola oración bajó más, Anexo B, P7), y la búsqueda de mecanismos internos para explicar grados concretos (§4.6: el modelo es una caja negra).

---

## Fuentes y lectura adicional

Fuentes oficiales de TypeSafe:

- [Introduction](https://docs.typesafe.ai/introduction)
- [API](https://docs.typesafe.ai/api)
- [Models](https://docs.typesafe.ai/models)
- [Confidence](https://docs.typesafe.ai/confidence)
- [State](https://docs.typesafe.ai/concepts/state)
- [Primitives](https://docs.typesafe.ai/primitives)
- [Jev 1.13 y model jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [How to build with System One](https://docs.typesafe.ai/concepts/how-to-build-with-system-one)
- [System One](https://docs.typesafe.ai/concepts/system-one)
- [Choice](https://docs.typesafe.ai/primitives/choice) y [Score](https://docs.typesafe.ai/primitives/score)
- [Cookbook: Parallel questions](https://docs.typesafe.ai/cookbooks/parallel_questions)
- [Cookbook: consistencia de Noul](https://docs.typesafe.ai/cookbooks/consistency_noul_cookbook)
- [Use-case map](https://docs.typesafe.ai/concepts/use-case-map)
- [Machine-learning primer](https://docs.typesafe.ai/introduction/machine-learning-primer)
- [Patterns](https://docs.typesafe.ai/patterns)
- [Cookbooks](https://docs.typesafe.ai/cookbooks)
- [LLM-friendly documentation index](https://docs.typesafe.ai/llms.txt)

Materiales de terceros o integraciones, que deben leerse con sus propios caveats:

- [MotherDuck: prompt_jev() y Jev en SQL](https://motherduck.com/blog/motherduck-supports-jev/)
- [Vercel AI Gateway](https://vercel.com/ai-gateway)
- [Cloudflare Workers AI](https://developers.cloudflare.com/workers-ai/)
- [LangChain integrations](https://python.langchain.com/)
- [PostgreSQL / pgjev material](https://pgxn.org/dist/jev/)

Las URL de terceros anteriores sirven como puntos de entrada; los nombres de paquete, parámetros y benchmarks deben verificarse contra la versión concreta utilizada. La guía no presenta esos materiales como documentación oficial de TypeSafe.
