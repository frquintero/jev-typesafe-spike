# Diccionario Jev

Glosario vivo del spike. Definiciones cortas, ilustradas con piezas
reales de nuestras pruebas. Si un ejemplo no se midió, se dice.

## Orden de lectura

1. State — el mundo a juzgar.
2. Pregunta — el juicio sobre ese mundo.
3. Pregunta tipada — la pregunta con respuesta cerrada.
4. Noul, Choice, Score — los tres tipos, en palabras.
5. Confianza — cuánto se despega la ganadora del empate.
6. Criteria — el volante: qué significan las respuestas.
7. Instructions — el dedo que señala qué parte juzgar.
8. Regla y verbo — la regla decide el lado, el verbo lo tajante.
9. Independencia y fan-out — muchas preguntas, un request.
10. La lógica va en la estructura — el JSON como lógica, no la prosa.
11. Garantías oficiales — lo que el doc promete.
12. Crudo — el acta de cada llamada.

## State

**Qué es**: lo que se quiere evaluar. Punto. Un mensaje, un texto,
un estado de algo.

**Formatos**: string (`"Mi carro se averió"`), objeto
(`{"mensaje": "mi carro se averió"}`), array
(`["Hola", "mi carro", "123"]`).

**Uno por request**: cada request evalúa un solo state. Dos
documentos = dos requests (o se fusionan en un state, decisión del
código).

**Pelado u objeto**: si el state es una sola cosa, va pelado (string);
si son dos o más piezas, objeto con etiquetas para apuntarlas
(`{"indice": ..., "doc": ...}`). Medido: quitar el envoltorio
`{"doc": ...}` del índice no cambió ni un veredicto (11/11 antes y
después).

**Empaque e independencia**: se pueden empacar varios mensajes,
textos o estados en un solo JSON, y cada uno se evalúa
independientemente de los otros. Medido en vivo: tres mensajes de
distinta urgencia, un Score por campo — juntos y separados dieron lo
mismo (2.0/2.0, 0.0/0.0, 0.98/0.99, la diferencia es la respiración
normal entre corridas).

**Dos fuentes del juicio**: Jev juzga con el mundo con el que fue
entrenado **más** el state que se le dé. Si la pregunta no señala el
state, juzga solo con lo entrenado (verdaderas 0.89–0.93, falsas
0.01–0.04); si lo señala, juzga contra él (0.92–0.99), porque ahí
está lo que el entrenamiento no sabe.

**Cuándo se necesita state**: cuando la decisión **depende** del
state — de cosas que Jev no puede saber. El estado de un programa no
es una verdad del mundo: depende de variables propias de ese código
(`intentos_fallidos: 5`, `cuenta_verificada: true`); si no viaja en
el state, Jev no tiene de dónde juzgarlo. Lo mismo el contenido de un
documento concreto (este índice, esta celda, este bloque): no es
sabiduría, es materia.

**Verdades del mundo no requieren state**: Jev incluye el
conocimiento del mundo — si el material a juzgar va en la
`instruction` misma, el state puede quedar vacío y el juicio sale
igual. Medido con `state: ""` y la sentencia pelada en instructions:
`Ojalá el fallo sea favorable.` → desiderativa 1.0; `Hechos
relevantes.` → frase_nominal 1.0; `¿Quién presentó la demanda?` →
interrogativa 0.89 (`spike-jev/cache/tipo-state-vacio.json`,
`-1.json`, `-2.json`).

**El state como caso**: el state es el caso particular que el código
propone y Jev juzga — los hechos que el veredicto necesita y el modelo
no sabe. Como analogía interna sirve "caso estadístico": en los
barridos de clasificación cada sentencia/celda/bloque es una
observación que recibe etiqueta bajo la misma regla (fan-out). Aviso:
no es término oficial — el doc habla de *content, material, facts* y
nunca de *case/instance/observation/sample* — y el state puede ser un
expediente entero (conversación + orden + política en un solo state),
no una fila.

**Dos casos medidos**:

- *Biblioteca* (`spike-jev/cache/biblioteca-noul*.json`): socio L-08
  con 2 préstamos, solicitud con ejemplares 0→1, regla de tope.
  Pregunta computable (`puede socio.id retirar solicitud.libro`): el
  código la resuelve exacta (`prestamos < 3 and ejemplares > 0`); Jev
  cayó del lado correcto con verbo + paths (0.91), pero con paths
  pelados sin predicado marcó 0.21 aun con ejemplar disponible — ni
  registró el cambio 0→1 hasta que se apuntó al hecho.
- *Vecinos* (`spike-jev/cache/vecinos-noul.json`): "Qué curioso que el
  pasillo del tercero siempre esté impecable menos los lunes, que es
  cuando pasa la señora del 3B con el perro." Noul `se insinúa que
  alguien ensucia` → 0.9, sin la palabra clave en el texto y sin campo
  de contexto. Ningún `if` lo precomputa.

**El talento de Jev**: resuelve casos determinísticos (if/else), pero
su verdadero talento está donde lo determinístico falla por
construcción — juicios irreductiblemente semánticos (insinuación,
intención, ambigüedad). Lo computable va en código (regla 13); lo que
ningún `if` precomputa va a Jev.

**En una línea**: state = lo que la decisión necesita y Jev no sabe.

## Pregunta

**Qué es**: define un juicio que el modelo hace sobre el State. Sin
preguntas no hay juicios — el state solo es mundo hasta que una
pregunta lo interroga.

**Tres tipos**, por lo que la respuesta significa: Noul (¿es
verdad?), Choice (¿cuál es?), Score (¿cuánto?).

**En una línea**: la pregunta es el juicio; el state, lo juzgado.

## Pregunta tipada

**Qué es**: una pregunta que lleva cerrado de antemano qué formas
puede tener la respuesta. Tres piezas, siempre: `type` (la forma:
`noul`, `choice` o `score`), `instructions` (qué juzgar y contra qué
parte del state) y `criteria` (qué significa cada respuesta posible).

**Ilustrada** (de `spike-jev/cache/eel-indice-bare.json`, pregunta
`n02` — con instructions mínimas, solo la cita):

```json
"n02": {
  "type": "choice",
  "instructions": "'Hechos relevantes'",
  "criteria": {
    "titulo": "Nombra el documento completo, va primero y no cuelga de nada",
    "capitulo": "Nombra una parte mayor, deriva directamente del título",
    "subtitulo": "Nombra una subsección que deriva lógicamente del capítulo al que pertenece"
  }
}
```

Y la respuesta solo puede ser una de esas tres etiquetas (salió
`subtitulo`, 0.88):

```json
"n02": {
  "type": "choice",
  "choice": "subtitulo",
  "confidence": 0.88,
  "probabilities": { "titulo": 0.0, "subtitulo": 0.93, "capitulo": 0.07 }
}
```

**En una línea**: es un `enum` con probabilidades, no una pregunta de
examen.

## Noul

**Qué es**: *¿es verdad?* — ¿la afirmación de `instructions` es
cierta? Devuelve P(verdad), un número 0–1. Sin confianza separada:
~0.5 es incertidumbre, no intensidad media. El criteria es opcional y
se omite por defecto (medido: con y sin, 0.02/0.99 → 0.01/0.99).

**Conocimiento del mundo vs state**: Jev tiene conocimiento propio y
solo consulta el state **cuando la pregunta lo señala** (path,
backticks, referencia explícita). Si la pregunta va desconectada, la
juzga por su conocimiento aunque el state diga otra cosa. Medido con
`state: {"t": ["2+2=5"]}`:

| Pregunta | Resultado |
|---|---|
| Desconectada verdadera ("El sol es una estrella.", "Simón Bolívar nació en Caracas.") | 0.89–0.93 |
| Desconectada falsa ("Is 2+2=5?", "El padre de la química moderna es Marco Fidel Suárez.") | 0.01–0.04 |
| Anclada al state ("Does \`t0\` say that 2+2=5?") | 0.92–0.99 |

Crudos: `spike-jev/cache/noul-2mas2.json`, `noul-sol.json`,
`noul-bolivar.json`, `noul-suarez.json`. La desconectada verdadera da
alto pero con descuento (0.89–0.93 vs 0.92–0.99 anclada); la falsa,
baja fulminante. El "¿es 2+2=5?" confunde porque el state contiene el
mismo texto — pero es coincidencia, no vínculo.

*Corrección 2026-09-22*: «solo consulta el state cuando la pregunta lo
señala» es demasiado fuerte. Una pregunta sin ancla también se movió
con un state pertinente (sol: 0.72 → 0.32/0.38 y 0.79), aunque
probablemente porque el state desambiguaba la proposición. Lo firme:
el ancla convierte la pregunta en otra (sobre el texto, no sobre el
mundo), y un state irrelevante no movió nada. Ver guía §4.4.

**Los nombres del state no son neutros**: describen roles, jamás
veredictos. Una clave que sopla la respuesta contamina el juicio:
con `{"falso": "La capital de Francia es Berlín."}`, preguntar "Is
Berlin the capital of France, according to `falso`?" dio **0.1** (la
clave dijo el veredicto); con clave neutra `t1`, la misma pregunta
dio **0.91** (se leyó como contenido). Crudo: `noul-falso2.json`.

*Corrección 2026-09-22*: `noul-falso2.json` solo contiene el 0.1; el
0.91 con clave `t1` no tiene crudo. La comparación queda retirada hasta
re-medirla. Nombres neutros siguen siendo buena precaución.

**Ilustrado**: `¿el cliente pide reembolso?` sobre el ticket mixto →
0.99 (`spike-jev/cache/ticket-mixto.json`).

## Choice

**Qué es**: *¿cuál es?* — elige una opción entre varias **sin
orden**. Devuelve la elegida + distribución + confianza. Toda Choice
lleva su no-match explícito (la confianza no detecta "ninguna vale").

**Ilustrado**: `ruta` del ticket → `billing`, 1.0 unánime; categoría
del fan-out → `billing` 0.81 con fugas reales a bug (0.11) y account
(0.08) porque el mensaje mezcla tres asuntos.

## Score

**Qué es**: *¿cuánto?* — grado sobre **niveles ordenados** que uno
define. Si duda entre vecinos, el número cae en el medio (1.4); si
está seguro, cae en un nivel (2.0). Devuelve score + distribución +
confianza + `legend` (tus niveles numerados desde 0).

**Ilustrado**: urgencia del ticket mixto → 1.4, confianza 0.33
(0.02/0.56/0.42): ambiguo de verdad, sin presión temporal explícita.
Frustración del fan-out → 1.0 unánime.

## Confianza

**Qué es**: el número 0–1 que acompaña a Choice y Score. No es un
juicio nuevo del modelo: es una cuenta determinista sobre
`probabilities`, recalculable en código. No agrega información.

**Fórmula**: `(N·p_max − 1)/(N − 1)`, con N = opciones/niveles y
p_max = probabilidad de la ganadora. En palabras: qué fracción del
camino va el pico **desde el empate hasta la certeza**. 0 = todas
empatadas; 1 = todo en una; 0.5 = mitad del camino, **no** "50% de
acertar".

**Verificado**: los 10 casos Choice/Score de nuestros crudos la
reproducen (`strawberry*`, `rapidisimo-opciones`, `fanout-5`,
`ticket-mixto`, `urgency-structured`). Las centésimas que no cuadran
(urgencia 0.33 vs 0.340 de la fórmula) son el redondeo a 2 decimales
de `probabilities`: la confianza se calcula sin redondear.

**Ilustrado**: `rapidísimo`, 4 opciones → empate = pico 0.25; pico
real 0.84 → (0.84 − 0.25)/(1 − 0.25) = **0.79**. Es decir: "la
ganadora va al 79% del camino entre el empate a cuatro y la certeza",
nada más.

**Tres trampas**:

- **Solo mira el pico, no la forma**: con 3 opciones, `[0.5, 0.5, 0]`
  y `[0.5, 0.25, 0.25]` dan 0.25 igual. La cola no se ve; si importa
  (la segunda pisándole los talones), leer `probabilities`.
- **No se compara entre distinto N**: mismo pico 0.56 → 0.34 con 3
  opciones, 0.47 con 6.
- **No es calibración**: 0.9 no es "90% de acierto". El 82–92% que
  cita el README es de classifier.dev (otro sistema, re-pregunta a un
  razonador).

**Noul no lleva** confianza: su número ya es P(verdad). Es solo de
Choice y Score.

**Para qué sirve**: routing <0,7 (regla 21) — umbral cómodo sobre "el
pico no se despega del empate" (el doc: para *"threshold on it without
doing the math yourself"*). Umbrales propios se calibran con datos
(regla 11), nunca se copian.

**En una línea**: la confianza mide qué tan lejos está el pico del
empate — geometría del reparto, no promesa de acierto.

## Criteria

**Qué es**: el volante del modelo — el *juicio* es el criteria
aplicado a los hechos. Medido: reescribir dos descripciones movió las
edades de 0.60–0.78 a 0.97–0.98.

**Reglas del doc, todas verificables**:

- **Situaciones, no grados**: "roto o degradado, pero existe
  workaround" le da al modelo algo que matchear; "moderadamente
  grave", no.
- **Cada nivel compite solo**: el modelo no ve el número del nivel ni
  a sus vecinos; "peor que el anterior" no significa nada. Niveles
  `["0","1","2"]` → 0.55 con confianza 0.33 (reparte); con
  descripciones → 0.0 al 1.0.
- **Un Score, una dimensión**: si la descripción mide tres cosas, una
  entrada alta en una y baja en otra no tiene dónde caer. Se parte en
  un Score por dimensión y se combinan en código.
- **El extremo raro merece nivel propio**: sin él, lo grave y lo
  gravísimo colapsan arriba y el score no los distingue.
- **Sin continuo no hay Score**: categorías discretas → Choice o
  Nouls.
- **Niveles estructurados**: cada nivel puede ser objeto
  `{what, examples}` con los mismos campos (few-shot en la escala).
  Medido: urgency intermedia pasó de 0.98/0.97 (repartía) a 1.0/1.0
  unánime (`spike-jev/cache/urgency-structured.json`).
- **La confianza sola no valida un wording**: se valida contra
  ejemplos etiquetados, nunca por el número.

**En una línea**: el criteria no describe la respuesta — la produce.

## Instructions

**Qué es**: el señalamiento de qué parte del state juzgar — y nada
más. La pregunta tipada queda completamente especificada por
**(type + criteria + path)**: el `type` da la forma del juicio, el
`criteria` da qué juzgar, el path da dónde. La prosa en instructions
nunca aportó un punto.

**Cadena medida** (cada ablación mantuvo el resultado):

- Pregunta completa ("¿qué nivel ocupa la entrada X? Usa su posición
  entre las vecinas") → 11/11.
- Solo la cita (`'Hechos relevantes'`) → 11/11.
- Solo el path (`sentencias[0]`) → 5/5 al 1.00
  (`spike-jev/cache/tipo-path-pelado.json`).

**Lo que no funciona**: ordinales en prosa (`elemento 6 de doc`) —
hacia el final de la lista el modelo pierde qué juzga y las
respuestas colapsan a uniforme (~0.2 por clase). El path ancla
(`sentencias[2]`, `` `tabla[3].edad` ``); el ordinal flota.

**En una línea**: señalar con path; la prosa es ceremonia.

## Regla y verbo

**Qué es**: en los casos con regla, dos palancas separadas — la regla
decide el *lado* del veredicto, el verbo de instructions decide lo
*tajante*. Medido en el caso biblioteca (socio con 4 préstamos, nivel
desconocido, tope pregrado 3 / posgrado 5), Choice [pregrado,
posgrado]:

| | regla simbólica | regla en prosa |
|---|---|---|
| "qué es" | pregrado 0.82 ✗ | posgrado 0.82 ✓ |
| "determinar" | pregrado 0.60 ✗ | posgrado 0.97 ✓ |

Crudos: `spike-jev/cache/biblioteca-*.json` (réplica de "determinar":
0.96).

**Lecciones**:

- **La regla se dice, no se simboliza**: topes en prosa (`max. 3
  préstamos`) voltean el veredicto; flechas y pipes (`->`, `|`) no —
  cinco corridas fallaron con notación simbólica. La relación tiene
  que ser explícita y legible (`max.` porta el tope; `->` es ambiguo).
- **El verbo nombra la operación**: con regla legible, "qué es"
  (reportar) dio 0.82 y "determinar" (derivar) dio 0.97; con regla
  ilegible, "determinar" ablandó el error (0.82→0.60) sin voltearlo.
  Los paths señalan el *qué*; el verbo dice el *cómo*.
- **Sin predicado no hay juicio (Noul)**: paths pelados (`socio.id
  solicitud.libro`) marcaron 0.21 aun con el hecho a favor. El path
  pelado funcionaba en Choice porque el criteria carga el juicio; en
  Noul el juicio vive en instructions o no hay juicio.

**En una línea**: la regla decide el lado, el verbo decide lo tajante.

## Independencia y fan-out

**Qué es**: todas las preguntas ven el mismo state y se juzgan
aisladas, en paralelo. Agregar o quitar preguntas no mueve a las
demás (regla 25 del README). Medido: `titulo` 1.00 sola y en grupo de
11; tres urgencias iguales juntas y separadas.

**Fan-out especulativo** (patrón oficial): mandar en un request todas
las preguntas que el sistema pueda necesitar —incluso las que quizá
no importen (severidad de bug aunque no sea bug)— y que el código
decida después qué era relevante. Medido en
`spike-jev/cache/fanout-5.json`: 5 preguntas mezcladas (Choice, Score,
Noul, Noul, Score) en una llamada; el código rutearía billing e
ignoraría severidad.

**Solo cambia la operación**: 1 llamada en ~1 s vs N llamadas, N
latencias, N cobros de state.

## La lógica va en la estructura

**Qué es**: el JSON del request ya es lógica — legible por máquina,
no prosa para convencer. Cada campo cumple un rol lógico:

- `state`: el mundo (los hechos, lo juzgado).
- `questions`: los juicios (uno por ID, independientes).
- `type`: la forma de cada juicio (¿verdad? / ¿cuál? / ¿cuánto?).
- `criteria`: el espacio de respuestas (lo decible, cerrado).
- el path en instructions: dónde mirar (`sentencias[2]`).

**Contraste con LLM**: en un LLM la lógica vive en el prompt
("analizá, clasificá, respondé en este formato...") — prosa que
instruye y se reza para que se obedezca. Acá la lógica vive en el
esquema: no hay nada que interpretar, solo campos que ocupar. Por eso
quitar prosa nunca dolió — la lógica no estaba en las palabras,
estaba en la forma.

**Evidencia**: toda la cadena de ablaciones (state pelado, cita,
path) mantuvo veredictos idénticos; lo único que rompió algo fue
salirse de la estructura (ordinales en prosa → colapso). La forma
sostiene; la prosa adorna.

**En una línea**: estructura, no prosa.

## Garantías oficiales

Del doc de TypeSafe, textuales:

- **Respuestas acotadas**: *"Every answer is constrained to the
  options you supplied... Your code never has to recover a value from
  generated prose."* Salirse del tipo es imposible por construcción,
  no por obediencia — a diferencia de un LLM con structured output.
- **Respuestas independientes**: *"Every answer is independent... You
  can add or remove questions without changing the others' results."*
  La base oficial de nuestra regla 25. Matiz nuestro (no está en el
  doc): vale con buen direccionamiento; con ordinales vimos
  degradación.

## Crudo

**Qué es**: la respuesta del API **tal cual llegó por el cable**
(*raw response*), guardada en disco antes de que el código la toque:
JSON íntegro con `answers`, `usage`, `model`.

**Para qué**: evidencia (el número se demuestra, no se copia),
re-correr sin re-pagar (se lee el archivo), auditoría (el spike
informa con números y los números viven en los crudos).

**Dónde**: `spike-jev/cache/` — `modalidad-50.json`, `tabla-30.json`,
`eel-indice-20.json`, `eel-indice-bare.json`, `ticket-mixto.json`,
`fanout-5.json`, `urgency-structured.json`, `tipo-una.json`,
`tipo-dos.json`, `tipo-array5.json`, `tipo-path-pelado.json`,
`noul-2mas2.json`, `noul-sol.json`, `noul-bolivar.json`,
`noul-suarez.json`, `noul-falso2.json`, `noul-falso4.json`,
`noul-array-t0.json`.

**En una línea**: el acta de cada llamada.
