# Jev de TypeSafe: guía pedagógica y crítica

> Versión 3 — 21 de septiembre de 2026

## Cómo leer esta guía

Esta guía explica Jev de TypeSafe sin convertir su documentación, sus benchmarks o sus integraciones en una promesa general de inteligencia. Distingue cuatro niveles:

1. **Documentación oficial de TypeSafe**: contratos, primitivas, límites y ejemplos publicados por el proveedor.
2. **Benchmarks o materiales de terceros**: resultados útiles, pero dependientes de su tarea, datos y metodología.
3. **Mediciones propias**: resultados del spike local; no son garantías del producto.
4. **Inferencias arquitectónicas**: conclusiones razonables para diseñar software, que todavía deben validarse en el corpus y operación reales.

La tesis central es sencilla:

> **Jev estima juicios semánticos estrechos y tipados; el código compone esos juicios, aplica las reglas y decide qué acción tomar.**

Es importante conservar el verbo *estimar*. Que la salida sea tipada y probabilística no demuestra que el juicio sea correcto.

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

Un **Noul** formula una pregunta binaria de sí/no. Su respuesta es `noul`, que representa la probabilidad estimada de que la respuesta sea “sí”.

```json
{
  "type": "noul",
  "noul": 0.91
}
```

`noul: 0.91` no significa “la verdad universal es 91%”. Significa que, dado el `state`, la formulación y la versión del modelo, Jev asigna alta probabilidad a la respuesta afirmativa.

Dos Nouls que parecen complementarios no tienen por qué sumar uno. La documentación de jaggedness muestra, por ejemplo, que pueden aparecer `0.72 + 0.47 = 1.19`. Por ello el código no debe asumir que preguntas separadas constituyen una distribución conjunta coherente.

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

Un **Score** asigna una respuesta ordinal o discreta a una escala previamente definida.

Pregunta:

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

Respuesta:

```json
{
  "type": "score",
  "score": 3,
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

Un `Score` requiere `criteria`: un array de entre 2 y 10 descripciones de nivel. La respuesta devuelve `score`, `legend` (mapa nivel→descripción), `probabilities` (mapa nivel→probabilidad) y `confidence`; `scale` no es un campo del API. Un score no es una medición física. Es un juicio sobre una escala semántica; la definición de cada nivel y sus ejemplos son parte del contrato.

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

Los criterios no deberían reducirse siempre a una cadena vaga como “elige la mejor opción”. La forma documentada por `how-to-build` permite describir cada opción con estructura:

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
    "focus": "La función dentro del documento, no la calidad literaria",
    "format": "Escoge exactamente una categoría"
  }
}
```

Esto ayuda a reducir ambigüedad y a versionar el contrato. No sustituye una definición operacional ni una prueba de calibración.

### 4.4 Acoplamiento: el juicio es conjunto, no hay dos canales

Lo que sigue es inferencia arquitectónica (nivel 4) apoyada en mediciones propias (nivel 3), no documentación oficial. La hipótesis más simple que explica la evidencia es que Jev no procesa "pregunta" y "contexto" por canales separados: forma **un único juicio conjunto** sobre todo lo que viaja en el request —conocimiento de entrenamiento, `state` y wording— donde cada pieza vota en proporción a su acoplamiento con las demás.

Evidencia (spike local, `jev-1.13.0`, crudos en `spike-jev/cache/`):

- Sin acoplamiento, vota solo el prior: la pregunta desconectada `"Is 2+2=5?"` da 0.01–0.02 aunque el state contenga `"2+2=5"`; la instrucción pelada `"2+2=5"` da 0.04 (`noul-2mas2*.json`).
- El ancla es una señal fuerte de acoplamiento, no un mecanismo aparte: `"Does the text say that 2+2=5?"` da 0.99 sobre el mismo state.
- Sin ancla explícita, el acoplamiento lo decide la pertinencia tópica: ante `"a veces el sol no ilumina la tierra"` (0.72 sin state, replicado 0.72), el state irrelevante (`"Pedro está triste"`) no mueve el número (0.72), el pertinente-impreciso lo hunde (0.32, réplica 0.38) y el pertinente-preciso (`"cada noche Bogotá se oscurece"`) lo eleva (0.79).
- Todo el sobre se lee como señal: una key que sopla el veredicto (`"falso"`) hunde una lectura anclada de 0.91 a 0.10 (`noul-falso2.json`).

Consecuencias prácticas: diseñar el `state` es controlar el acoplamiento —nombres de campo neutros, contenido preciso y pertinente, ancla explícita (path, backticks, deíctico) cuando se juzga material presentado, y `state` vacío cuando se sondea el prior. Un state "de apoyo" impreciso no es neutral: contamina.

Caveats: corridas únicas por probe (los números respiran entre llamadas), un solo modelo y versión, y series cortas en pocos dominios. La dirección del efecto es consistente, la magnitud no está calibrada.

### 4.5 La primitiva elige el mundo de referencia

Inferencia (nivel 4) sobre mediciones propias (nivel 3). El mismo state declarativo (`"en este mundo 2+2 es 5"`) y la misma instrucción (`"2+2=5"`) producen veredictos distintos según la primitiva —luego Noul vs Choice no es formato de salida, sino selección del mundo contra el cual se juzga:

```text
                    state ""    state declarativo
Noul "2+2=5"        0.04        0.11
Noul anclada          —          0.90
Choice [sí,no]      no 1.00     0.48 / 0.52 (réplica idéntica)
Choice 4 opciones   no 0.99     0.64 / 0.34
```

Crudos: `choice-2mas2-*.json`, `noul-2mas2-mundo*.json` en `spike-jev/cache/`.

Lectura: Noul pregunta "¿es verdad?" y su referencia por defecto es el mundo del entrenamiento —el state sin ancla apenas la mueve (0.04 → 0.11). Choice pregunta "¿cuál de estas encaja?" y su referencia por defecto es el marco presentado: el menú cerrado es un ancla por construcción, recluta al state, y el mismo state parte la masa por la mitad (1.00 → 0.48). Dos Choices en fan-out sobre `""` repiten sus corridas solas (regla 25 intacta).

Consecuencias para el diseño: la sonda de prior es Noul + state vacío; el juicio de material presentado es Choice, o Noul con ancla explícita. Nunca asumir que ambas primitivas coinciden sobre el mismo material. Y el menú configura el veredicto, no solo lo reparte: quitar dos opciones movió el "sí" de 0.34 a 0.48 —las opciones llevan descripciones propias y, por regla general, un no-match explícito.

Caveats: un solo dominio (aritmética), criteria mínimos (etiqueta como descripción), sin no-match en estos probes. Falta replicar en dominios ordinarios antes de tratarlo como ley.

---

## 5. Confidence: qué es y qué no es

La confianza no debe presentarse como una garantía de exactitud individual. La documentación la deriva de las probabilidades de salida; el significado práctico debe comprobarse con datos propios.

El explorer oficial de confidence muestra la forma general:

```python
count = len(values)
peak = max(values)
choice_confidence = (count * peak - 1) / (count - 1)
choice_confidence = max(0.0, min(1.0, choice_confidence))
```

Es decir, para una distribución de probabilidades `values`, se toma la probabilidad máxima, se aplica la transformación correspondiente al número de opciones y se limita el resultado al intervalo `[0, 1]`. La variante con tres opciones que aparece a veces es solo un caso particular de esta fórmula.

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

### Décimo límite (medición propia): el horizonte del conocimiento

TypeSafe no publica la fecha de corte de entrenamiento de Jev. La sondaamos con una medición propia (nivel 3 de esta guía): **preguntas desconectadas** sobre `state: ""`, que fuerzan la respuesta desde el conocimiento entrenado — el mecanismo del caso `"Is 2+2=5?"`, aplicado al eje temporal. Diseño: 27 hechos fechados 2024-01 → 2026-07 (ground truth verificado con Exa) + 6 falsos de control, una sola call fan-out a `jev-1.13.0`, wording e IDs sin fechas ni años (la fecha vive solo en metadata local).

Observaciones de esa corrida:

| Hito | Fecha del hecho | noul |
|---|---|---|
| Último conocido (OMS Pandemic Agreement) | 2025-05-20 | 0.69 |
| Primer desconocido (PSG gana Champions) | 2025-05-31 | 0.08 |
| Cola previa (p. ej. catch de booster Starship) | 2024-10-13 | 0.58 |
| Muerte sostenida (GPT-5, iPhone 17, F1, final del Mundial…) | 2025-07 → 2026-07 | ≤ 0.45 |

Conjeturas — **no son conclusiones**; son observaciones con n bajo, una corrida sin réplicas y probes con ruido:

1. El corte efectivo se ubica hacia **2T 2025** (borde más nítido del corpus: 11 días entre 0.69 y 0.08), no en un año ni un semestre completos. La granularidad honesta es de **trimestre**; el mes sería falso precisión.
2. La degradación **no es un muro**: hay cola progresiva desde ~finales de 2024 — los hechos recientes se "saben" peor conforme se acercan al borde.
3. Algunos probes no miden el corte: los que llevan números (Bitcoin a 100k) heredan el límite 2 de jaggedness, y los redaccionalmente ambiguos ("the election" sin año) miden la formulación, no el conocimiento.
4. Una versión del mismo corpus con fechas en el wording movió resultados ±0.2–0.3 en ambos sentidos: la fecha en la pregunta contamina la medición y hay que dejarla fuera.

Nada de esto se generaliza más allá de `jev-1.13.0` en esa corrida: el corte no está documentado por el proveedor y los alias pueden moverse.

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

Hay una discrepancia interna en la documentación sobre el ejemplo de batching: una página de primitivas habla de **11,5× más barato y 9,6× más rápido**, mientras que el resumen de `llms.txt` habla de **12,2× y 10,0×**. No se debe forzar una cifra única. La conclusión segura es que reenviar el mismo estado en muchas llamadas puede ser sustancialmente menos eficiente que agrupar preguntas; la ventaja de latencia puede cambiar cuando las llamadas separadas se ejecutan concurrentemente.

La latencia promocional u orientativa —por ejemplo, aproximadamente 100 ms en `how-to-build` o 70–500 ms en materiales de marketing— no debe mezclarse con las mediciones del spike. Las mediciones propias observadas de aproximadamente 0,7–2,5 segundos pertenecen a ese entorno, transporte, carga y configuración. Antes de comparar, hay que fijar:

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
| Score | Valor dentro de una escala discreta u ordinal definida. |
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

## Fuentes y lectura adicional

Fuentes oficiales de TypeSafe:

- [Introduction](https://docs.typesafe.ai/introduction)
- [API](https://docs.typesafe.ai/api)
- [Models](https://docs.typesafe.ai/models)
- [Confidence](https://docs.typesafe.ai/confidence)
- [State](https://docs.typesafe.ai/concepts/state)
- [Primitives](https://docs.typesafe.ai/primitives)
- [Jev 1.13 y model jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13)
- [How to build](https://docs.typesafe.ai/concepts/how-to-build)
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
