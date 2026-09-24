# Jev de TypeSafe: guía pedagógica y crítica

> Versión 5 — 23 de septiembre de 2026

## Cómo leer esta guía

Esta guía explica Jev de TypeSafe sin convertir su documentación, sus benchmarks o sus integraciones en una promesa general de inteligencia. Distingue cuatro niveles:

1. **Documentación oficial de TypeSafe**: contratos, primitivas, límites y ejemplos publicados por el proveedor.
2. **Benchmarks o materiales de terceros**: resultados útiles, pero dependientes de su tarea, datos y metodología.
3. **Mediciones propias**: resultados del spike local; no son garantías del producto.
4. **Inferencias arquitectónicas**: conclusiones razonables para diseñar software, que todavía deben validarse en el corpus y operación reales.

La tesis central es sencilla:

> **Jev estima juicios semánticos estrechos y tipados; el código compone esos juicios, aplica las reglas y decide qué acción tomar.**

Es importante conservar el verbo *estimar*. Que la salida sea tipada y probabilística no demuestra que el juicio sea correcto.

Al final hay tres piezas prácticas:

- el **Anexo A**: un caso real paso a paso (cómo se diseñó, corrigió y validó una escala de Score);
- el **Anexo B**: las pruebas con que se sostuvieron varias reglas;
- el **Anexo C, Registro de reglas**: todas las reglas de la guía en tablas, para consultar al diseñar.

Todo lo que aquí llamamos «reglas» son **heurísticas**: sentido común, experiencia y algo de experimentación. Orientan el diseño; no lo reemplazan. Cada aplicación necesita sus propios ajustes y pruebas.

---

## 1. Qué es Jev

TypeSafe presenta Jev como un **System One Model**: un modelo orientado a juicios rápidos, repetibles y acotados, en contraste con sistemas que intentan resolver mediante deliberación abierta una tarea completa.

La forma conceptual es:

```text
state + pregunta tipada + criterios
                  ↓
                Jev
                  ↓
respuesta tipada + probabilidades
                  ↓
                código
```

En términos más formales:

```text
f(state, question, criteria, instructions) → typed probabilistic answer
```

El `state` aporta el material que debe examinarse. La pregunta fija el juicio. El tipo limita la forma de respuesta. Las probabilidades hacen visible la distribución interna de opciones, de modo que el programa puede establecer umbrales, pedir revisión humana o combinar señales.

Jev no es, por sí mismo:

- un agente autónomo;
- un sistema de búsqueda o investigación factual;
- un sustituto de las reglas de negocio;
- una garantía de coherencia entre preguntas;
- un modelo de razonamiento profundo;
- una prueba de que una afirmación es verdadera fuera del contexto proporcionado.

Una comparación útil es esta:

| Sistema | Fortaleza principal | Riesgo típico |
|---|---|---|
| LLM general | generar, explicar, transformar y resolver tareas abiertas | coste, latencia, salidas variables y difícil control de forma |
| Clasificador convencional | tarea fija, datos etiquetados y operación eficiente | requiere entrenamiento y mantenimiento específicos |
| Jev | juicio semántico cerrado, tipado, probabilístico y repetible | puede equivocarse semánticamente y no mantiene una visión global coherente |
| Código/reglas | invariantes, aritmética, política y efectos | no interpreta bien lenguaje ambiguo sin señales semánticas |

La ventaja de Jev aparece cuando el problema se puede expresar como muchas preguntas pequeñas, con respuestas conocidas de antemano, que el código puede componer.

---

## 2. La prueba práctica: ¿merece la pena Jev?

Antes de elegir un modelo, aplica estas preguntas:

1. ¿La respuesta pertenece a un espacio cerrado o a una escala definida?
2. ¿El `state` relevante está disponible y se puede delimitar?
3. ¿Una persona experta podría emitir **ese juicio concreto** en pocos segundos?
4. ¿La salida se puede evaluar con etiquetas, reglas o revisión humana?
5. ¿El juicio se repetirá suficientes veces para que importen la latencia, el coste o la uniformidad?

Si varias respuestas son negativas, no se sigue que Jev sea imposible; sí que hace falta descomponer el problema o usar otra arquitectura.

Ejemplos:

```text
¿Este ticket pide un reembolso?                 → Noul
¿A qué categoría pertenece este documento?      → Choice
¿Qué nivel de urgencia expresa?                 → Score
¿Este pasaje contradice esta afirmación?        → Choice
```

En cambio, esta pregunta es demasiado grande sin descomposición:

```text
¿Cuál es la mejor arquitectura para este sistema?
```

Dentro de ella se esconden requisitos, supuestos, riesgos, costes, alternativas, restricciones operativas y consecuencias futuras. Convertirla directamente en un `Score` oculta el problema; no lo resuelve.

---

## 3. Las primitivas

### 3.1 Noul

Un **Noul** toma **un enunciado** y estima cuánto apoyo tiene. Su respuesta es `noul`: la probabilidad estimada de que el enunciado sea verdadero.

```json
{
  "type": "noul",
  "noul": 0.91
}
```

`noul: 0.91` no significa “la verdad universal es 91%”. Significa que, dado el `state`, la formulación y la versión del modelo, Jev asigna alta probabilidad a la respuesta afirmativa.

Dos Nouls que parecen complementarios no tienen por qué sumar uno. La documentación de jaggedness muestra, por ejemplo, que pueden aparecer `0.72 + 0.47 = 1.19`. Por ello el código no debe asumir que preguntas separadas constituyen una distribución conjunta coherente.

**Un Noul es un juicio de «sí», no de «sí o no».** No reparte entre dos respuestas: gradúa el apoyo a un solo enunciado. De ahí sale una regla de lectura importante:

> **Un valor bajo significa falta de apoyo, no negación.**

Negar un enunciado no es lo mismo que no apoyarlo. Por eso un Noul bajo no distingue dos situaciones opuestas. Si preguntas «`texto` afirma que la capital de Australia es Sídney»:

- con un texto que dice «Canberra», el valor es bajo (el texto lo **contradice**);
- con un texto que no habla de capitales, el valor también es bajo (el texto **calla**).

Si necesitas distinguir contradicción de silencio, usa **dos Nouls sobre enunciados contrarios** («…es Sídney», «…es Canberra») o una **Choice con opción de salida** («no se indica»).

**Una Noul por dimensión.** Si dos ideas se confunden con facilidad —por ejemplo, la *certeza* con que se afirma algo y la *evidencia* que lo apoya—, pregúntalas en dos Nouls separadas. En el Anexo B (prueba 1), dos Nouls así separaron limpiamente «Según los ensayos…, el fármaco *podría*…» (certeza baja, evidencia alta) de «Los ensayos… *muestran* que…» (ambas altas).

### 3.2 Choice

Un **Choice** selecciona entre opciones conocidas.

```json
{
  "type": "choice",
  "choice": "billing",
  "probabilities": {
    "billing": 0.86,
    "technical": 0.09,
    "account": 0.05
  },
  "confidence": 0.79
}
```

La lista de opciones debe ser explícita y puede contener como máximo 255 opciones. Conviene incluir una opción de no-match —por ejemplo, `other`, `none` o `unknown`— cuando las categorías no cubren todos los casos plausibles. Si las categorías se solapan, están incompletas o cambian con frecuencia, el resultado exige evaluación adicional.

### 3.3 Score

Un **Score** responde a la pregunta *¿cuánto?* sobre una escala ordenada que tú defines.

**Cómo se pregunta.** En `criteria` escribes los niveles de la escala, del más bajo al más alto: entre 2 y 10 niveles. Cada nivel debe describir una situación reconocible, no un grado vago como «poco» o «mucho».

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
| `probabilities` | Cómo reparte Jev su convicción entre los niveles. Suma 1. |
| `score` | El punto medio de ese reparto. Puede caer entre dos niveles. |
| `legend` | Los niveles que definiste, numerados desde 0. |
| `confidence` | Qué tan concentrado está el reparto: 1 = todo en un nivel. |

(`scale` no es un campo del API.)

**Una imagen para entenderlo.** Imagina que Jev tiene 100 fichas y las reparte entre los niveles según dónde cree que está el caso. El `score` es el punto de equilibrio de esas fichas:

```text
0×0,01 + 1×0,04 + 2×0,15 + 3×0,80 = 2,74
```

Es decir: «casi crítico, con algo de peso en urgente».

**Tres reglas para leer un Score.**

1. **El score es una posición, no una medida.** Un 2,74 no significa «el 74 % del camino entre urgente y crítico». Los niveles son palabras, no marcas de una regla. TypeSafe advierte que en Jev 1.13 los niveles tienen una calibración numérica débil: el score sirve para comparar casos y aplicar umbrales («¿supera 2,5?»), no para leer magnitudes exactas.

2. **Si la confianza es baja, mira `probabilities`, no `score`.** El promedio puede esconder la forma de la duda. Estos dos casos tienen el mismo score y significan cosas opuestas:

   | Caso | Reparto | Score | Qué significa |
   |---|---|---|---|
   | A | nivel 1 → 100 % | 1,0 | seguro: es nivel 1 |
   | B | nivel 0 → 50 %, nivel 2 → 50 % | 1,0 | duda entre 0 y 2; **no** cree que sea 1 |

   El caso B ocurrió de verdad en el Anexo A: un score de 1,75 con 0,61 en el nivel 1, 0,34 en el nivel 3 y solo 0,03 en el nivel 2. El número apuntaba justo al nivel que Jev había descartado. La confianza (0,37) daba la alarma.

3. **Combinar Scores es válido, si se hace en código.** El patrón oficial *composite scoring* normaliza cada score (se divide por el número de niveles menos 1, para llevarlo a 0–1) y lo pondera. Lo que se combina son posiciones sobre rúbricas, no cantidades físicas; por eso los pesos y los umbrales del resultado también se calibran con datos propios.

### 3.4 Cómo diseñar una escala de Score

La calidad de un Score depende sobre todo de cómo están escritos sus niveles. Estas seis reglas salen de la documentación oficial y de las pruebas del Anexo A.

| # | Regla | Por qué | Qué pasó en el Anexo A |
|---|---|---|---|
| 1 | **Una sola dimensión por escala.** | Si mezclas dos ideas (por ejemplo, plazo y costo), la escala deja de estar ordenada. Es recomendación oficial. | La escala mixta cambió con una palabra marginal (de 1,00 a 0,68) y repartió el caso claro entre dos niveles. Separada en dos escalas, quedó estable. |
| 2 | **Describe lo que el texto dice o insinúa, no el mundo.** | Jev solo ve el `state`. No puede saber si algo «da igual hoy o en un mes». | El nivel «no hay consecuencia» fallaba porque el mensaje no dice nada sobre consecuencias. |
| 3 | **Que los niveles no se pisen.** | Si un caso cabe en dos niveles, Jev reparte la masa entre ambos. | «El cliente espera» cabía en «alguien espera» y en «una persona queda demorada»: salió 0,50 / 0,50. |
| 4 | **Escribe la frontera como una decisión.** | Dónde termina un nivel y empieza el otro es una política, no un hecho. | La frontera «solo el remitente / alguien más» resolvió el caso: 1,00 con confianza 1,00. |
| 5 | **Redacta en positivo.** | Las negaciones se leen al pie de la letra (límites 1 y 4 de la sección 6). | Un nivel con tres negaciones («solo… nadie más… nada») bajó la confianza de 0,98 a 0,77. |
| 6 | **Los ejemplos no deben parecerse a lo que vas a evaluar.** | Jev puede acertar —o fallar— por parecido de palabras, no por significado. | El ejemplo «Let me know when you can» arrastró un «No rush, whenever you get a chance» hacia el nivel equivocado (0,67). Al cambiar el ejemplo, bajó a 0,0. |

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
- dos escalas nuevas, escritas en español y en otro dominio (la fuerza con que un texto afirma algo), acertaron el nivel en 25 de 25 casos claros **al primer intento**, sin retoques. La confianza bajó solo en los casos que se habían marcado de antemano como dudosos.

Una lección de esa prueba: si la escala tiene una frontera discutible, **escríbela en la rúbrica**. Allí se decidió que la certeza se mide «venga de quien venga la afirmación», y el caso «Los expertos coinciden en que…» quedó sin dudas en «firme».

---

## 4. `state`, `criteria` e `instructions`

### 4.1 State

El `state` es el material que Jev debe inspeccionar: texto, campos, contexto estructurado o una combinación. No es automáticamente una memoria fiable ni un contenedor seguro.

La documentación advierte sobre **context rot**: demasiado contexto, contexto irrelevante o una organización poco clara pueden degradar el juicio. También advierte que el contenido puede ser adversarial. Un documento suministrado como `state` debe tratarse como dato, no como instrucciones con autoridad sobre el programa.

Buenas prácticas:

- incluir solo el contexto necesario;
- separar campos de datos de instrucciones del sistema;
- delimitar documentos, citas y metadatos;
- conservar el identificador del modelo y la versión de la pregunta;
- medir el efecto de añadir o quitar contexto.

### 4.2 Criteria estructurado

Los criterios no deberían reducirse siempre a una cadena vaga como “elige la mejor opción”. La documentación de Choice permite describir cada opción con un objeto de campos `what`, `not_for` y `examples`:

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

La estructura hace el juicio más inspeccionable, pero no garantiza que las categorías sean mutuamente excluyentes ni que los ejemplos cubran producción.

### 4.3 Instructions estructurado

Las `instructions` pueden expresar la pregunta y su foco con campos explícitos:

```json
{
  "instructions": {
    "question": "¿Qué función cumple este fragmento?",
    "focus": "La función dentro del documento, no la calidad literaria"
  }
}
```

La documentación usa en sus ejemplos campos como `question`, `focus`, `compare` e `inspect`. Puedes añadir otros campos propios, pero ten presente que sus nombres son diseño de tu aplicación, no parte de un esquema oficial.

Esto ayuda a reducir ambigüedad y a versionar el contrato. No sustituye una definición operacional ni una prueba de calibración.

### 4.4 El `state` y la pregunta: qué podemos afirmar y qué no

Esta sección se revisó en la versión 4. Las versiones anteriores proponían un mecanismo interno («un juicio conjunto», «el state impreciso contamina»). Los experimentos no alcanzan para eso: muestran **sensibilidades observables**, no mecanismos. Aquí separamos lo medido (nivel 3) de lo que todavía es hipótesis (nivel 4).

Una advertencia de método: estos experimentos son **sondas del modelo**. Ponían a propósito enunciados sueltos en el state («2+2=5») para comprobar si Jev tiene un mundo propio y qué hace cuando el state lo contradice. Eso es legítimo para estudiar a Jev, pero en una aplicación el `state` tiene otra función: contiene **material con un papel reconocible** (un mensaje, un documento, un folleto), nombrado por ese papel. Por eso lo que aquí se observa informa sobre el modelo; las reglas de diseño se prueban aparte, con material realista (sección 4.5 y Anexo B).

**Lo que se observó** (`jev-1.13.0`, crudos en `spike-jev/cache/`):

1. **El ancla cambia la pregunta.** Con el mismo state `"2+2=5"` y en el mismo request, `"Is 2+2=5?"` dio 0,02 y `"Does the text say that 2+2=5?"` dio 0,99 (`noul-2mas2.json`). No son dos respuestas a una misma pregunta: son dos preguntas distintas, una sobre el mundo y otra sobre el texto. Incluso la redacción del ancla importa: `"Does the state say that 2+2=5?"` dio 0,71 (`noul-falso.json`).
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
| Desambiguación | El state pertinente fija la referencia de una proposición ambigua. | Escribir la proposición sin ambigüedad: el efecto del state debería desaparecer o casi. |
| Peso del prior | El state pesa más cuando Jev está inseguro. | Casos con líneas base cercanas a 0,1, 0,5 y 0,9, comparados en Δlogit. Si el Δlogit es igual en todas las bandas, la hipótesis cae: el efecto sería simplemente aditivo. |
| Lectura compartida | Varias preguntas sobre el mismo state heredan la misma duda del mensaje. | Ver Anexo A (caso h3): añadir una petición explícita y comprobar si las dos dudas desaparecen juntas. |

Retirado en la versión 4: el ejemplo de la clave `"falso"` (0,91 → 0,10). Solo existe el crudo del 0,10; sin el otro extremo no hay comparación.

**Qué hacer en la práctica** (vale sea cual sea el mecanismo):

- Si quieres juzgar el **material**, dilo en la pregunta: nombra el campo (con backticks) y pregunta por lo que el texto dice.
- Si quieres consultar lo que Jev **sabe**, deja el state vacío o sin relación con la pregunta.
- Si la proposición es **ambigua**, desambíguala en la pregunta; no dejes que el state decida la lectura.
- Incluye solo contexto **pertinente** (la documentación advierte del *context rot*).
- Usa **nombres de campo neutros**, que describan el papel del dato y no sugieran el veredicto. Es una precaución barata.

Límites: pocos casos, un dominio por experimento, un solo modelo.

### 4.5 Noul y Choice no son formas equivalentes del mismo juicio

**Lo que dice la documentación (nivel 1).** Entre los límites de Jev 1.13 figura la falta de *invariantes estructurales*: preguntas que parecen equivalentes no tienen por qué dar respuestas coherentes. Su ejemplo: ante la misma pregunta sobre el mismo ticket, una Noul da 0,22 y una Choice sí/no da 0,01 para «sí». Tiene sentido: una Choice reparte probabilidad entre sus opciones (suman 1), mientras que una Noul evalúa una afirmación por separado.

**Lo que medimos (nivel 3).** State: `"en este mundo 2+2 es 5"`; instrucción: `"2+2=5"`.

| Pregunta | State vacío | State «en este mundo…» |
|---|---|---|
| Noul `"2+2=5"` | sin medir | 0,11 |
| Noul anclada «¿Dice el state que 2+2 es 5?» | — | 0,90 |
| Choice [sí, no] | sí 0,00 | sí 0,48 |
| Choice [sí, sí con dudas, no con dudas, no] | sí 0,01 | sí 0,34 |

Crudos: `noul-2mas2-mundo*.json`, `choice-2mas2-*.json`. (Versiones anteriores de esta tabla ponían 0,04 en la casilla «Noul, state vacío»; ese valor se midió con state `"2+2=5"`.)

Con el mismo state, la Noul dice casi «no» y la Choice duda. En el ejemplo oficial la divergencia iba **en sentido contrario** (la Choice era la más escéptica). Conclusión segura: **la dirección de la divergencia no es fija; no la generalices.** El menú también pesa: con cuatro opciones, «sí» recibió 0,34; con dos, 0,48.

**¿Qué causaba esa divergencia? El objeto del juicio.** En el ejemplo de arriba, la pregunta no decía qué se juzgaba: si la verdad de «2+2=5» o lo que dice el texto. Se probó con material realista (Anexo B, prueba 2): un folleto de viaje que dice «Su capital, Sídney, …», con dos objetos de juicio distintos, cada uno como Noul y como Choice.

| Folleto dice «Sídney» | Noul | Choice |
|---|---|---|
| ¿qué dice el folleto? | 0,82 | «Sídney» 1,00 |
| ¿el dato es correcto? | 0,11 | «incorrecto» 0,99 |

Con el mismo material, los dos objetos dan respuestas opuestas, y **las dos primitivas siguen al objeto**. En el folleto que dice «Canberra» ocurrió lo mismo, con los valores invertidos. De ahí la regla:

> **Escribe en la pregunta qué se juzga: qué dice el material, o si lo que dice es correcto. La primitiva solo decide la forma de la respuesta.**

Una diferencia que conviene conocer: **la Noul es más «blanda» que la Choice**. La Choice reparte entre opciones que compiten y tiende a saturar (1,00 / 0,99); la Noul juzga un enunciado aislado y queda más lejos de los extremos (0,82 / 0,11). Por eso Noul y Choice se comparan por el **lado de 0,5**, no por la magnitud, y cada primitiva necesita sus propios umbrales.

Retirado en la versión 4: la tesis «la primitiva elige el mundo de referencia». Era una sobreinterpretación de un solo dominio.

**Qué hacer en la práctica:**

- Elige la primitiva por lo que significa la respuesta: condición sí/no → Noul; una opción de un conjunto → Choice; grado en una escala → Score.
- Escribe siempre qué se juzga. Si el objeto queda implícito, Noul y Choice pueden divergir; si queda explícito, coinciden.
- En una Choice, trata el menú como parte de la pregunta: cada opción con su descripción y, por regla general, una opción de no-match.

---

## 5. Confidence: qué es y qué no es

La confianza no debe presentarse como una garantía de exactitud individual.

**Qué dice la documentación (nivel 1).** `confidence` es un estadístico calculado a partir de la distribución de probabilidades: si la probabilidad se concentra en una opción, la respuesta es segura; si se reparte, es incierta. Como ejemplo da la fórmula para tres opciones, `(3 × probabilidad máxima − 1) / 2`, y aclara que es una medida práctica, no una definición cerrada: si otra medida te sirve mejor, calcúlala tú desde `probabilities`.

**Lo que reconstruimos (nivel 3).** Esta generalización reproduce nuestros datos con 2 y 4 opciones (máximo 0,52 → 0,04; máximo 0,64 → 0,51):

```python
count = len(values)
peak = max(values)
confidence = (count * peak - 1) / (count - 1)
confidence = max(0.0, min(1.0, confidence))
```

Sirve para entender qué mide la confianza. No la uses como contrato de producción: el proveedor no la publica como tal.

**Sobre calibración.** TypeSafe dice que sus modelos se entrenan para dar decisiones *calibradas* —probabilidades ajustadas para reflejar la incertidumbre— y precisa que la calibración se mide sobre grupos de predicciones y no garantiza que una respuesta individual sea correcta. Eso no valida ningún umbral concreto: la propia documentación indica que el umbral depende de la acción y del dominio, y que se fija con datos propios.

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

### La confianza como alarma

Una confianza baja suele indicar una de dos cosas:

- **el caso es ambiguo**: el propio texto admite dos lecturas; o
- **la rúbrica tiene niveles que se pisan**: el caso cabe en dos opciones.

En el Anexo A, la confianza baja señaló los tres casos problemáticos (0,37; 0,25; alrededor de 0,70). Cuando aparece, no leas solo la respuesta: mira `probabilities` para ver entre qué opciones duda Jev.

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

## 6. Nueve límites que la documentación hace visibles

La página de jaggedness de Jev 1.13 describe límites que deben formar parte del modelo mental del lector:

1. **Literalidad**: puede tomar la formulación demasiado al pie de la letra.
2. **Números**: no es una calculadora fiable.
3. **Fechas**: las fechas relativas y temporales necesitan tratamiento explícito.
4. **Indirection**: varios saltos semánticos degradan el juicio.
5. **Context rot**: demasiado contexto o contexto mal seleccionado perjudica.
6. **Contenido adversarial**: el `state` puede contener instrucciones o texto manipulador.
7. **Criterios contradictorios**: definiciones ambiguas o incompatibles dañan la separación de opciones.
8. **Invariantes entre preguntas**: resultados de preguntas independientes no tienen por qué ser coherentes globalmente.
9. **Generación**: la generación abierta no es el núcleo de Jev.

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

1. **Un Noul bajo significa «probablemente no», no «no sé».** Un valor bajo puede venir de al menos cuatro causas distintas:
   - **desconocimiento**: el hecho es posterior al entrenamiento;
   - **conocimiento antiguo**: para un modelo que no vio la final de 2025, el PSG *nunca había ganado* la Champions, así que responder «no» con seguridad es coherente con lo que sabe;
   - **tasa base**: en preguntas del tipo «¿ganó X?», casi cualquier candidato concreto tiene una probabilidad baja de antemano;
   - **semántica temporal**: ver el punto 2.
2. **Quitar la fecha cambia la pregunta.** «¿Ganó el PSG la Champions 2025?» pregunta por un hecho fechado. «¿Ganó el PSG la Champions?» se evalúa desde el «ahora» implícito del modelo. Son preguntas distintas. Al quitar las fechas del enunciado, 7 de 33 probes se movieron 0,15 o más. (Los IDs de las preguntas no llegan al modelo, así que retirar fechas de los IDs no pudo influir.)
3. **Pocas mediciones y sin réplicas.** El «borde» entre 0,69 y 0,08 descansa en un probe (OMS) que pasó de 0,42 a 0,69 al cambiar su redacción.

**Cómo debería ser una segunda versión:**

- **Parejas**: para cada hecho, un contrafáctico plausible del mismo evento («¿ganó el Inter?» junto a «¿ganó el PSG?»). La señal es la **brecha** entre el verdadero y el contrafáctico, no el valor absoluto.
- **Choice entre desenlaces plausibles**, con una opción «todavía no ha ocurrido / no lo sé».
- **Clases separadas**: resultados (solo se saben después) y anuncios programados (se pueden saber antes).
- **Controles** anteriores y posteriores al intervalo, y **réplicas**.

Solo con eso tendría sentido estimar una ventana temporal, y siempre para una versión concreta del modelo.

---

## 7. Las diez formas oficiales de decisión

La taxonomía de `use-case-map` organiza usos de Jev en diez formas. No todas tienen la misma dificultad ni el mismo nivel de validación en un proyecto concreto.

| Forma | Pregunta típica | Salida habitual |
|---|---|---|
| Classification | ¿A qué clase pertenece? | `Choice` |
| Detection | ¿Está presente este fenómeno? | `Noul` |
| Scoring | ¿En qué nivel está? | `Score` |
| Routing | ¿A qué flujo se envía? | `Choice` + código |
| Search | ¿Qué elementos responden a una intención? | señal o ranking |
| Retrieval | ¿Qué pasajes son pertinentes? | relevancia por elemento |
| Ranking | ¿Cuál debe aparecer antes? | score relativo |
| Verification | ¿Está soportado, contradicho o ausente? | `Choice` |
| ML Feature Extraction | ¿Qué atributo semántico conviene materializar? | feature tipada |
| Structured Data Extraction | ¿Qué campos aparecen en el texto? | estructura tipada |

Search, retrieval y ranking no significan que Jev sustituya un índice, un buscador o un sistema de recuperación completo. Puede aportar juicios semánticos dentro del pipeline; la recuperación, la diversidad, la deduplicación y las garantías de cobertura siguen siendo problemas de ingeniería.

Del mismo modo, una feature extraída por Jev es una señal probabilística. Antes de persistirla como dato canónico hay que especificar versión, esquema, confianza, evidencia, fecha de cálculo y política de revisión.

---

## 8. Los cuatro patterns oficiales

### Fan-out

Ejecutar varias preguntas independientes sobre el mismo `state` y reunir las respuestas.

```text
state ─┬─ ¿es claim? ───────────┐
       ├─ ¿qué modalidad? ──────┼─ resultados tipados
       ├─ ¿qué función? ────────┤
       └─ ¿qué urgencia? ────────┘
```

Es útil para enriquecer registros, pero la independencia operacional no implica coherencia semántica conjunta.

### Confidence routing

Usar la confianza para seleccionar el siguiente camino: automatización, revisión, otra pregunta o un modelo más costoso. El umbral debe calibrarse con datos reales.

### Composite scoring

Combinar scores o señales en código para producir una decisión compuesta. La fórmula, los pesos, las normalizaciones y los límites deben ser explícitos; Jev no debe recibir una pregunta que oculte toda la política.

La receta oficial tiene tres pasos: normalizar cada score dividiéndolo por (número de niveles − 1), multiplicarlo por su peso y sumar. Recuerda la sección 3.3: se combinan posiciones sobre rúbricas, no magnitudes físicas.

### Intent routing

Detectar la intención y dirigir la solicitud al flujo correspondiente. Es un caso natural de `Choice`, pero las categorías deben cubrir la distribución real y tener una ruta para ambigüedad o “desconocido”.

---

## 9. Dónde encaja frente a un LLM

Un LLM es adecuado cuando hay que generar, explicar, sintetizar, explorar alternativas o trabajar con instrucciones abiertas. Jev es atractivo cuando el trabajo puede compilarse en una pregunta estrecha que se repetirá muchas veces.

Un patrón híbrido frecuente es:

```text
LLM u operador
  └─ define o revisa la tarea abierta
       ↓
preguntas, criterios y opciones versionados
       ↓
Jev ejecuta juicios repetitivos
       ↓
código calcula, valida, enruta y actúa
```

La etapa de compilación no elimina la necesidad de revisión. Una pregunta mal definida puede producir resultados muy consistentes y muy equivocados.

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

La documentación de modelos de TypeSafe asocia Jev 1.13.0 con, entre otros datos publicados, precio de entrada de 0,042 USD por millón de tokens, salida sin coste, aproximadamente 250k tokens por segundo y 1.200 requests por minuto. En los límites de contexto, `64k` corresponde al `state` más todas las preguntas, mientras que `32k` corresponde al `state` más la pregunta más larga: no es un límite de salida. Estos valores dependen del modelo, el endpoint y la fecha; para producción debe fijarse una versión, especialmente si los umbrales están calibrados.

Hay una discrepancia interna en la documentación sobre el ejemplo de batching: la página de primitivas cita el cookbook *Parallel questions* con **11,5× más barato y 9,6× más rápido**, mientras que el propio cookbook, con las mismas 13 preguntas, reporta **12,2× y 10,0×**. No se debe forzar una cifra única. La conclusión segura es que reenviar el mismo estado en muchas llamadas puede ser sustancialmente menos eficiente que agrupar preguntas; la ventaja de latencia puede cambiar cuando las llamadas separadas se ejecutan concurrentemente.

La latencia promocional u orientativa —por ejemplo, aproximadamente 100 ms en *How to build with System One* o 70–500 ms en materiales de marketing— no debe mezclarse con las mediciones del spike. Las mediciones propias observadas de aproximadamente 0,7–2,5 segundos pertenecen a ese entorno, transporte, carga y configuración. Antes de comparar, hay que fijar:

- endpoint y región;
- versión del modelo;
- tamaño del `state`;
- número de preguntas;
- concurrencia y batching;
- tiempo de red y serialización;
- si se mide p50, p95 o tiempo total.

También existe `jev-preview`, un alias documentado en `models` que se adelanta a `jev-latest` y que actualmente apunta al mismo modelo. Al ser un alias móvil, no conviene usarlo para thresholds calibrados ni mezclar resultados de `preview` con los de una versión fijada.

---

## 12. Versionado, evaluación y operación segura

Si una decisión depende de un threshold, la versión del modelo y de la pregunta forma parte del dato. Un registro de producción debería conservar, como mínimo:

```json
{
  "model": "jev-1.13.0",
  "question_id": "ticket.intent.v3",
  "criteria_version": "2026-09-21",
  "state_id": "ticket-123",
  "answer": "billing",
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
5. prueba de sensibilidad a wording, criterios y orden;
6. revisión adversarial del `state`;
7. comparación con una línea base sencilla;
8. política de abstención y escalamiento humano;
9. monitorización de drift y de cambios de versión.

Y cuatro hábitos de método que el Anexo A mostró útiles:

10. **escribir la predicción antes de correr**, y que sea puntual («nivel 1»), no un rango («1–2»): un rango casi siempre acierta y por eso enseña poco;
11. **pares mínimos**: cambiar una sola cosa del caso cada vez, para saber qué movió el resultado;
12. **réplicas**: correr cada caso varias veces y reportar media, rango y desviación, no solo un número. La variación es pequeña pero real: en un cookbook de TypeSafe, 15 repeticiones dieron una desviación media de 0,0102 por pregunta, y aun así una pregunta osciló entre 0,43 y 0,53, cruzando el umbral de 0,5. Una variación grande (en el spike, `snorfle` dio 0,74 y luego 0,21) merece investigarse, no despacharse como ruido. Y para robustez semántica, la réplica útil es la **paráfrasis**: la misma pregunta con otras palabras;
13. **separar ajuste y validación**: una rúbrica corregida sobre ciertos casos acierta en ellos casi por construcción. Solo un conjunto nuevo, que no se usó para ajustar, muestra si la rúbrica generaliza;
14. **distinguir sondas del modelo y pruebas de diseño**: una sonda puede usar el state de forma artificial para estudiar a Jev; una prueba de diseño usa material realista. Lo que sale de una sonda no se convierte en regla de diseño sin probarlo así;
15. **casos sencillos pero ilustrativos**: cada prueba parte de un caso mínimo que muestre con claridad una sola regla.

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
    ├─ relevancia para una pregunta
    └─ relación con otra unidad
```

Esto puede alimentar SQL, reglas, grafos, embeddings, modelos clásicos o nuevas preguntas Jev. El beneficio no es que Jev “comprenda el documento entero” de una vez, sino que puede convertir juicios locales repetibles en señales reutilizables.

El límite es decisivo: la ontología, la estructura persistida y las relaciones canónicas no deben modificarse automáticamente solo porque una salida probabilística parezca convincente. Conviene guardar candidatos, evidencia, versión y posibilidad de arbitraje humano.

---

## 14. Glosario breve

| Término | Definición pedagógica |
|---|---|
| System One Model | Modelo orientado a juicios rápidos, locales y estructurados. |
| State | Material contextual que Jev debe examinar. |
| Pregunta tipada | Pregunta cuyo tipo de respuesta está definido de antemano. |
| Noul | Pregunta sí/no; su valor es la probabilidad estimada de “sí”. |
| Choice | Selección entre opciones declaradas. |
| Score | Posición sobre una escala ordenada de niveles; es el punto medio del reparto de probabilidades, no un nivel elegido. |
| Probabilities | Distribución que Jev asigna a las respuestas posibles. |
| Confidence | Transformación de la distribución, útil para enrutar; no garantía individual de acierto. |
| Criteria | Definición de qué significa cada opción, incluyendo límites y ejemplos. |
| Instructions | Especificación estructurada de la pregunta y su foco. |
| Fan-out | Varias preguntas sobre el mismo `state`. |
| Confidence routing | Uso de la confianza para escoger el siguiente camino. |
| Composite scoring | Composición explícita de señales o scores en código. |
| Intent routing | Clasificación de intención para dirigir a un flujo. |
| Context rot | Degradación por exceso, irrelevancia o mala organización del contexto. |
| Type safety | Restricción de la forma de salida; no equivale a corrección semántica. |
| Calibración | Comprobación de cómo se relacionan confianza y error en grupos de casos. |
| Regla de precaución | «Esto puede pasar; evítalo». Basta un caso que muestre el riesgo, porque evitarlo es barato. |
| Regla predictiva | «Esto normalmente ocurre así». Necesita varios casos y, si es posible, más de un dominio. |
| Sonda del modelo | Experimento para estudiar a Jev; puede usar el state de forma artificial. |
| Prueba de diseño | Experimento para decidir cómo usar Jev en una aplicación; usa material realista. |

---

## 15. Conclusión

Jev es más interesante cuando se entiende como una primitive intermedia entre lenguaje y software:

```text
texto o estado
      ↓
juicio semántico tipado y probabilístico
      ↓
reglas, composición, validación y acción en código
```

Su promesa no es que una pregunta `Choice` convierta cualquier decisión compleja en segura. Su promesa es permitir que determinados juicios semánticos repetitivos entren en pipelines ordinarios con una forma de salida que el programa puede inspeccionar y combinar.

La frontera sana es:

> **Jev estima; el sistema decide.**

Cuando el juicio es estrecho, el contexto está disponible, las categorías son explícitas y existe evaluación, Jev merece una prueba. Cuando la tarea exige investigación, deliberación prolongada, aritmética, invariantes globales o autoridad sobre efectos irreversibles, hay que dividirla y dejar esas responsabilidades fuera del modelo.

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
4. **Instrucción vaga**: «urgency of the message» no dice urgencia *de quién*.

### Paso 2. Preguntar con pares mínimos

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
- **Un score intermedio puede engañar.** En v3, el horizonte 1,75 parece «en los próximos días», pero ese nivel tenía solo 0,03. Jev dudaba entre «sin plazo» (0,61) y «hoy» (0,34). Es el caso B de la sección 3.3.
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

La lección de este paso: **cuando Jev reparte la masa en partes iguales, casi siempre hay dos niveles que se pisan.** La salida no es forzar a Jev, sino escribir la frontera. «Un tercero que espera cuenta como costo» es una decisión de política: podría haberse decidido lo contrario, pero había que decidir.

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

- **h3** es el caso más blando. Las dos escalas dudaron en la misma proporción (≈ 0,2 hacia su nivel 0). Probablemente el mensaje admite dos lecturas: petición o simple información (ver sección 4.4). Además, su confianza (0,71 · 0,69 · 0,72) cae justo sobre un umbral de 0,70: es el ejemplo de la sección 5.
- **h5** aprobó con facilidad porque la predicción fue un rango (1–2). Un rango enseña poco.

### Paso 5. Lo que salió mal (y por qué importa)

De 18 predicciones escritas en el paso 2, cinco fallaron. La más reveladora: se esperaba que Jev dudara entre leer el recordatorio al pie de la letra («no hay plazo, luego no es urgente») y leerlo como lo leería una persona («si insiste, alguien espera»). No dudó: eligió la segunda lectura con confianza 0,94. Sin la predicción escrita, este aprendizaje se habría perdido: cualquier resultado habría parecido razonable después.

### Resumen de lecciones

| Lección | Dónde se explica |
|---|---|
| El score es un punto medio; con confianza baja, lee `probabilities`. | 3.3 |
| Una dimensión por escala; niveles sobre el texto, sin solaparse, en positivo; ejemplos sin parecido con el material. | 3.4 |
| Preguntas separadas pueden heredar la misma duda del mensaje (hipótesis). | 4.4 |
| La confianza baja es una alarma; un umbral sobre casos reales enruta de forma inestable. | 5 |
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

- **Idioma**: en los casos claros, mismo veredicto en ambos idiomas (9 de 9). En los casos de borde, el español fue algo más generoso con la evidencia.
- **Dos dimensiones separadas**: «Según los ensayos…, *podría*…» → certeza 0,14, evidencia 0,92; «Los ensayos… *muestran*…» → 0,92 y 0,93.
- **Evidencia graduada**: de los ensayos con código (0,93) a la cita (0,86), el registro (0,82), «varios estudios» (0,36), los expertos (0,11) y la anécdota (0,07). «Está demostrado» (0,18) no cuenta como evidencia: invoca una prueba sin mostrarla.
- **Negaciones en el material**: «No es seguro que…» → 0,02; «No cabe duda de que…» → 0,97.
- **Un hallazgo del lenguaje, no del modelo**: atribuir la afirmación a otros («varios estudios muestran») la vuelve algo menos categórica (0,80 frente a 0,95). La fuente y la fuerza de una afirmación están ligadas en el propio lenguaje.

**Paso 2, con Scores** (crudos `score-urg-es-*`, `score-fuerza-es-*`).

- **Urgencia en español**: la rúbrica final del Anexo A, traducida, eligió el mismo nivel que en inglés en **8 de 8** mensajes, en las dos escalas. Pero la seguridad no siempre se conserva: un mensaje dio confianza 0,79 en inglés y 0,33 en español.
- **Dos escalas nuevas en español** —*certeza* (5 niveles) y *verificabilidad* (4 niveles)—, escritas con las reglas del §3.4 y con ejemplos sobre otro tema (un puente): **25 de 25** aciertos en los casos claros, sin retoques. La confianza bajó solo en los dos casos marcados de antemano como dudosos («Está demostrado», entre firme y enfática; el registro público, entre evidencia vaga y fuente localizable).

**Qué quedó establecido**: las reglas del §3.4 funcionan como heurística de partida en dos dominios y dos idiomas; los umbrales se calibran en el idioma del corpus. Matiz: las escalas se escribieron después de ver cómo leía Jev esas frases en el paso 1, así que no fue una prueba del todo a ciegas.

### Prueba 2. ¿Qué decide lo que Jev juzga: la pregunta o la primitiva?

**Qué se quería saber.** Si la divergencia entre Noul y Choice del §4.5 venía de la primitiva o de que la pregunta no decía qué se juzgaba.

**Material realista**: un folleto de viaje, en dos versiones idénticas salvo la ciudad (crudos `objeto-*`):

> «Australia combina playas extensas y desiertos rojos. Su capital, **Sídney** / **Canberra**, es una ciudad moderna y ordenada. La mejor época para visitarla va de septiembre a noviembre.»

**Dos objetos de juicio, cada uno como Noul y como Choice**: qué dice el folleto sobre la capital, y si ese dato es correcto.

| Folleto | Objeto | Noul | Choice |
|---|---|---|---|
| dice Sídney | qué dice | 0,82 | «Sídney» 1,00 |
| dice Sídney | ¿es correcto? | 0,11 | «incorrecto» 0,99 |
| dice Canberra | qué dice (¿Sídney?) | 0,01 | «Canberra» 1,00 |
| dice Canberra | ¿es correcto? | 0,94 | «correcto» 1,00 |

**Qué quedó establecido**: en los cuatro casos, Noul y Choice quedan del mismo lado; al cambiar el objeto, cambian juntas. Lo decisivo es **qué se juzga**, y eso se escribe en la pregunta. Dos observaciones: la Noul es más blanda que la Choice (se comparan por el lado de 0,5), y el 0,82 de «qué dice» es bajo para una pregunta sobre el texto, quizá porque el folleto no *afirma* que Sídney sea la capital sino que lo presupone (pendiente, Anexo C).

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
| Usa Jev para juicios estrechos, repetibles y evaluables; descompón las preguntas grandes. | P | diseño | oficial | §2 |
| Jev estima; el código decide. Reglas, cálculos, permisos y efectos quedan en código. | P | diseño | oficial | §12 |
| No delegues aritmética, conteos ni fechas. | P | diseño | oficial | §6 |
| En el `state` va material con un papel reconocible, nombrado por ese papel, y solo lo pertinente. | P | diseño | oficial + aceptada | §4.1, §4.4 |
| Trata el contenido del `state` como dato, no como instrucciones. | P | diseño | oficial | §4.1 |
| Usa nombres de campo neutros, que describan el papel del dato y no sugieran el veredicto. | P | diseño | aceptada | §4.4 |
| Si la pregunta es sobre el material, nómbralo en ella (campo entre backticks). | P | diseño | medida | §4.4 |
| Si la proposición es ambigua, desambíguala en la pregunta; no lo dejes al state. | P | diseño | aceptada | §4.4 |
| Fija la versión del modelo; no uses `jev-preview` con umbrales calibrados. | P | diseño | oficial | §11 |
| Los IDs de pregunta no llegan al modelo. | Pr | modelo | oficial | §6 |
| Agrupar preguntas sobre un mismo state no cambia sus respuestas. | Pr | modelo | oficial + medida | §8 |
| En los casos claros, una pregunta en español da el mismo veredicto que en inglés. | Pr | modelo | sostenida | Anexo B, P1 |
| Las negaciones dentro del material se leen bien («no es seguro», «no cabe duda»). | Pr | modelo | medida | Anexo B, P1 |
| Redacta las instrucciones en positivo; el riesgo de las negaciones está en la pregunta. | P | diseño | oficial | §3.4, §6 |
| Con preguntas bien definidas, las réplicas casi no varían. | Pr | modelo | medida | Anexo B, P1–P2 |
| Un state irrelevante no mueve el juicio. | Pr | modelo | conjetura | §4.4 |
| Un state pertinente resuelve la ambigüedad de una proposición. | Pr | modelo | conjetura | §4.4 |
| El state pesa más cuando el conocimiento previo es incierto (en log-odds). | Pr | modelo | conjetura | §4.4 |

### Noul

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Un Noul es un juicio de «sí» sobre un enunciado: **un valor bajo es falta de apoyo, no negación**. | P | modelo | aceptada | §3.1 |
| Para distinguir contradicción de silencio, usa dos Nouls sobre enunciados contrarios o una Choice con salida. | P | diseño | aceptada | §3.1 |
| ~0,5 es incertidumbre, no intensidad media. | P | modelo | oficial | §3.1 |
| Nouls que parecen complementarios no tienen por qué sumar 1. | P | modelo | oficial | §3.1 |
| Una Noul por dimensión: dos ideas que se confunden van en dos Nouls. | P | diseño | sostenida | §3.1, Anexo B, P1 |
| Redacta la Noul como un enunciado que puede ser verdadero o falso, no como una pregunta de percepción. | P | diseño | aceptada | Anexo B, P1 |
| Para consultar lo que Jev sabe, usa state vacío. | P | diseño | aceptada | §4.4 |
| Una Noul distingue grados de evidencia: identificable, vaga, de autoridad, anecdótica. | Pr | modelo | medida (un dominio) | Anexo B, P1 |
| Invocar una prueba sin mostrarla («está demostrado») no cuenta como evidencia identificable. | Pr | modelo | medida | Anexo B, P1 |

### Choice

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Opciones explícitas, cada una con su descripción. | P | diseño | oficial | §3.2 |
| Incluye una opción de salida (no-match). Cuando el caso encaja, la salida no roba masa (≤ 0,01 en la prueba 2). | P | diseño | oficial + medida | §3.2, Anexo B, P2 |
| Para opciones cercanas, usa `what` / `not_for` / `examples`. | P | diseño | oficial | §4.2 |
| El menú es parte de la pregunta: cambiar las opciones puede cambiar el veredicto. | Pr | modelo | medida (un caso) | §4.5 |

### Score

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| El score es una posición media, no una medida; úsalo para comparar y aplicar umbrales. | P | modelo | oficial | §3.3 |
| Con confianza baja, lee `probabilities`, no `score`. | P | diseño | medida | §3.3 |
| Una sola dimensión por escala. | P | diseño | oficial + sostenida | §3.4 |
| Niveles sobre lo que el texto dice o insinúa, sin solaparse, en positivo. | P | diseño | sostenida | §3.4 |
| Si una frontera es discutible, escríbela en la rúbrica como decisión. | P | diseño | sostenida | §3.4, Anexo A, Anexo B, P1 |
| Los ejemplos de los niveles no deben parecerse al material evaluado. | P | diseño | medida (basta para P) | §3.4 |
| Cubre el caso intermedio frecuente. | P | diseño | medida | §3.4 |
| La fuente y la fuerza de una afirmación están ligadas en el lenguaje (atribuir debilita un poco la aseveración); si tu escala debe separarlas, dilo en la rúbrica («venga de quien venga»). | P | diseño | medida | §3.4, Anexo B, P1 |
| Marca de antemano los casos dudosos: en una escala bien diseñada, la confianza baja se concentra en ellos. | Pr | diseño | sostenida | Anexo B, P1 |
| Una escala diseñada con estas reglas funciona al primer intento en otro dominio e idioma. | Pr | diseño | sostenida | Anexo B, P1 |
| Combina Scores en código: normaliza y pondera. | P | diseño | oficial | §3.3, §8 |

### Entre primitivas

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Elige la primitiva por lo que significa la respuesta: sí/no → Noul; una opción → Choice; grado → Score. | P | diseño | oficial | §4.5 |
| **Escribe en la pregunta qué se juzga; la primitiva solo decide la forma de la respuesta.** | Pr | diseño | sostenida | §4.5, Anexo B, P2 |
| Si el objeto del juicio queda implícito, Noul y Choice pueden divergir, y en cualquier dirección. | P | modelo | oficial + medida | §4.5 |
| Con el mismo material, «qué dice» y «si es correcto» son juicios distintos: pueden dar respuestas opuestas, y Jev los separa. | Pr | modelo | sostenida | §4.5, Anexo B, P2 |
| La Noul es más blanda que la Choice: compáralas por el lado de 0,5, no por la magnitud. | Pr | modelo | medida | §4.5, Anexo B, P2 |

### Operación

| Regla | Clase | Ámbito | Estado | Dónde |
|---|---|---|---|---|
| Confianza alta no garantiza acierto; la calibración vale para grupos de casos. | P | modelo | oficial | §5 |
| La confianza baja es una alarma: caso ambiguo o niveles que se pisan. | P | diseño | medida | §5 |
| Los umbrales se fijan por acción y dominio, con datos propios. | P | diseño | oficial | §5 |
| No pongas un umbral sobre un grupo de casos reales. | P | diseño | medida | §5 |
| Los umbrales van por primitiva y se calibran en el idioma del corpus. | P | diseño | medida | §5, Anexo B, P1 |
| Compara efectos en log-odds, con líneas base medidas. | P | diseño | aceptada | §4.4 |
| Reporta réplicas con media y rango; prueba la robustez con paráfrasis. | P | diseño | oficial + aceptada | §12 |

### Pendientes y retiradas

**Por probar:**

- **Redacción de instrucciones**: cómo nombrar el material en la pregunta («el texto», «el documento», el campo entre backticks) y qué efecto tienen las negaciones dentro de la pregunta.
- **Menú de la Choice**: qué pasa con un caso que no encaja, con y sin opción de salida.
- **Aseveración frente a presuposición**: en «Su capital, Sídney, es moderna», el folleto no *afirma* que Sídney sea la capital; lo da por supuesto. ¿Lo distingue Jev al preguntar «`texto` afirma que…»? (En la prueba 2 ese caso dio 0,82, más bajo de lo habitual.)

**Retiradas:** «un state impreciso contamina» (§4.4), «la primitiva elige el mundo de referencia» (§4.5), la fecha de corte «hacia el 2T de 2025» (§6).

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
