# Diccionario Jev

Glosario vivo del spike. Definiciones cortas, ilustradas con piezas
reales de nuestras pruebas. Si un ejemplo no se midió, se dice.

Desde la versión 6 de la guía pedagógica
(`jev_typesafe_guia_pedagogica_v2.md`, §1) usamos el **marco del
juez**: el `state` es el **expediente**; lo que Jev juzga va en
`instructions` (Noul) o en `criteria` (Choice, Score), y el resultado
es un **grado de soporte** o su reparto. Jev
no responde preguntas, no extrae datos y no dice verdadero o falso:
**sopesa juicios**. Donde el API dice *question* o *answer*, aquí
decimos juicio y resultado. Los nombres de campo del protocolo no
cambian (regla 3 del README).

## Orden de lectura

1. Expediente (`state`) — el material que se somete a juicio.
2. Juicio — lo que Jev sopesa frente al expediente.
3. Juicio tipado — el juicio con forma de resultado cerrada.
4. Noul, Choice, Score — las tres formas del juicio.
5. Grado y bandas — cómo se lee el resultado de una Noul.
6. Confianza — cuánto se despega el juicio ganador del empate.
7. Criteria — donde viven los juicios de Choice y Score.
8. Instructions — dónde vive el juicio.
9. Regla y verbo — cada palabra del juicio cuenta.
10. Independencia y fan-out — muchos juicios, un request.
11. La lógica va en la estructura — el JSON como lógica, no la prosa.
12. Garantías oficiales — lo que el doc promete.
13. Crudo — el acta de cada llamada.

## Expediente (`state`)

**Qué es**: el material que la aplicación somete a juicio, con un papel
reconocible: un mensaje, un documento, un folleto, el estado de algo.
Se nombra por su papel (`mensaje`, `folleto`), no con etiquetas vacías
(`bloque`, `t0`).

**Formatos**: string (`"Mi carro se averió"`), objeto
(`{"mensaje": "mi carro se averió"}`), array
(`["Hola", "mi carro", "123"]`).

**Uno por request**: cada request sopesa sus juicios frente a un solo
expediente. Dos documentos = dos requests (o se fusionan en un
expediente, decisión del código).

**Pelado u objeto**: si el expediente es una sola cosa, puede ir pelado
(string); si son dos o más piezas, objeto con etiquetas para
nombrarlas (`{"indice": ..., "doc": ...}`). Medido: quitar el envoltorio
`{"doc": ...}` del índice no cambió ni un resultado (11/11 antes y
después).

**Empaque e independencia**: se pueden empacar varios mensajes,
textos o estados en un solo expediente, y cada juicio que apunta a uno
de ellos se sopesa por separado. Medido en vivo: tres mensajes de
distinta urgencia, un Score por campo — juntos y separados dieron lo
mismo (2.0/2.0, 0.0/0.0, 0.98/0.99; la diferencia es la variación
normal entre corridas).

**Expediente y hechos notorios**: Jev sopesa cada juicio con el
expediente **y** con lo que sabe del mundo, sus hechos notorios (lo
notorio no necesita prueba). Un juicio sobre el mundo, sin relación con
el expediente, se sopesa desde lo notorio (verdaderos 0.89–0.93, falsos
0.01–0.04); un juicio sobre el material se sopesa contra él
(0.92–0.99). Si lo que el expediente dice choca con lo notorio, el
grado del juicio sobre lo que dice baja (ver Noul).

**Cuándo se necesita expediente**: cuando el juicio **depende** de cosas
que Jev no puede saber. El estado de un programa no es un hecho
notorio: depende de variables propias de ese código
(`intentos_fallidos: 5`, `cuenta_verificada: true`); si no viaja en
el expediente, Jev no tiene contra qué sopesarlo. Lo mismo el contenido
de un documento concreto (este índice, esta celda, este bloque): no es
sabiduría, es materia.

**Sondas de lo notorio**: para estudiar qué sabe Jev, el expediente
puede quedar vacío y el material ir dentro del juicio. Medido con
`state: ""`: `Ojalá el fallo sea favorable.` → desiderativa 1.0;
`Hechos relevantes.` → frase_nominal 1.0; `¿Quién presentó la
demanda?` → interrogativa 0.89 (`spike-jev/cache/tipo-state-vacio.json`,
`-1.json`, `-2.json`). Es una sonda del modelo, no un patrón de
aplicación: en una aplicación, el material va en el expediente.

**El expediente como caso**: el expediente es el caso particular que el
código propone y Jev juzga. En los barridos de clasificación cada
sentencia/celda/bloque es un caso que recibe resultado bajo el mismo
juicio (fan-out). El expediente puede ser entero —conversación + orden
+ política en un solo state—, no una fila.

**Dos casos medidos**:

- *Biblioteca* (`spike-jev/cache/biblioteca-noul*.json`): socio L-08
  con 2 préstamos, solicitud con ejemplares 0→1, regla de tope.
  Juicio computable (`puede socio.id retirar solicitud.libro`): el
  código lo resuelve exacto (`prestamos < 3 and ejemplares > 0`); Jev
  lo sostuvo (0.91) con verbo + paths, pero con paths pelados sin
  predicado dio 0.21 aun con ejemplar disponible: sin predicado no había
  juicio que sopesar.
- *Vecinos* (`spike-jev/cache/vecinos-noul.json`): "Qué curioso que el
  pasillo del tercero siempre esté impecable menos los lunes, que es
  cuando pasa la señora del 3B con el perro." Noul `se insinúa que
  alguien ensucia` → 0.9, sin la palabra clave en el texto y sin campo
  de contexto. Ningún `if` lo precomputa.

**El talento de Jev**: puede sopesar casos determinísticos (if/else),
pero su verdadero talento está donde lo determinístico falla por
construcción — juicios irreductiblemente semánticos (insinuación,
intención, ambigüedad). Lo computable va en código (regla 13); lo que
ningún `if` precomputa va a Jev.

**En una línea**: el expediente es lo que el juicio necesita y Jev no
sabe.

## Juicio

**Qué es**: lo que Jev sopesa frente al expediente. Jev devuelve cuánto
sostendría ese juicio si él mismo lo emitiera. Sin juicios no hay
resultado: el expediente es solo material hasta que un juicio se sopesa
contra él.

**Dónde vive**:

- **Noul**: un solo juicio, en `instructions` — «`ticket` pide un
  reembolso».
- **Choice**: varios juicios alternativos, sin orden, en `criteria` —
  «`ticket` pide cambiar o devolver un artículo», «`ticket` reclama
  por un cobro», «otra cosa». Jev los sopesa y reparte su soporte
  entre ellos (100 monedas).
- **Score**: varios juicios alternativos, como niveles ordenados, en
  `criteria` — «`mensaje` no expresa plazo», «`mensaje` lo necesita
  hoy».

En Choice y Score, `instructions` suele llevar una pregunta que agrupa
los juicios como alternativas (Hamblin: el significado de una pregunta
es el conjunto de sus respuestas posibles), pero no es lo que Jev
juzga: con `instructions: ""`, el reparto no cambió (prueba 6,
`vacio-*`). El peso de esa pregunta en casos menos claros es una
cuestión abierta.

**Principio de diseño**: lo que queremos que Jev juzgue va en
`instructions` (Noul) o en `criteria` (Choice, Score). Jev lo sopesa
(1) solo con su conocimiento, si el expediente va vacío, o (2) con un
estado de cosas más su conocimiento, si el expediente trae material.

**En una línea**: el juicio es lo que se sopesa; el expediente, contra
qué se sopesa.

## Juicio tipado

**Qué es**: un juicio que lleva cerrado de antemano qué forma puede
tener el resultado. Tres piezas, siempre: `type` (la forma: `noul`,
`choice` o `score`), `instructions` (el juicio de la Noul, o la
pregunta que agrupa en Choice/Score) y `criteria` (los juicios
alternativos).

**Ilustrado** (de `spike-jev/cache/eel-indice-bare.json`, juicio `n02`
— con instructions mínimas, solo la cita):

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

El resultado solo puede repartirse entre esos tres juicios
(concentró `subtitulo`, 0.88):

```json
"n02": {
  "type": "choice",
  "choice": "subtitulo",
  "confidence": 0.88,
  "probabilities": { "titulo": 0.0, "subtitulo": 0.93, "capitulo": 0.07 }
}
```

**En una línea**: es un `enum` con reparto de soporte, no una pregunta
de examen.

## Noul

**Qué es**: **un solo juicio**, en `instructions`. Devuelve el grado en que Jev lo
sostendría, de 0 a 1 (el doc lo llama probabilidad de que el enunciado
sea verdadero). No reparte entre «sí» y «no»: gradúa el soporte de un
solo juicio. Sin confianza separada. El criteria es opcional y se omite
por defecto (medido: con y sin, 0.02/0.99 → 0.01/0.99).

**Se lee por bandas** (guía §3.1):

| Grado | Lectura |
|---|---|
| > 0,85 | muy seguramente el juicio es cierto |
| 0,75 – 0,85 | seguramente es cierto |
| 0,65 – 0,75 | hay bases para pensar que es cierto |
| 0,30 – 0,65 | el juicio no se puede formar con este expediente |
| 0,20 – 0,30 | la base no es firme |
| < 0,20 | muy seguramente el juicio es falso |

**La franja central es una señal de diseño**, no una duda de Jev: el
juicio está mal formulado o desconectado del expediente. Si el diseño
es bueno y un caso concreto cae ahí, se prevé en el flujo (revisión,
un segundo juicio, más material).

**Un grado bajo no dice por qué**: «`folleto` afirma que la capital es
Sídney» da bajo tanto si el folleto dice Canberra (lo contradice) como
si no habla de capitales (calla). Para distinguirlo: dos Nouls sobre
juicios contrarios, o una Choice con opción de salida.

**Juicios sobre el mundo y juicios sobre el material** (sonda con
`state: {"t": ["2+2=5"]}`):

| Juicio | Grado |
|---|---|
| Sobre el mundo, verdadero ("El sol es una estrella.", "Simón Bolívar nació en Caracas.") | 0.89–0.93 |
| Sobre el mundo, falso ("Is 2+2=5?", "El padre de la química moderna es Marco Fidel Suárez.") | 0.01–0.04 |
| Sobre el material ("Does \`t0\` say that 2+2=5?") | 0.92–0.99 |

Crudos: `spike-jev/cache/noul-2mas2.json`, `noul-sol.json`,
`noul-bolivar.json`, `noul-suarez.json`. Nombrar el material convierte
el juicio en otro: uno sobre el mundo, otro sobre el texto. Un
expediente pertinente también puede mover un juicio sobre el mundo
(sol: 0.72 → 0.32/0.38 y 0.79), probablemente porque desambigua el
juicio; uno irrelevante no movió nada (guía §4.4).

**Cuando el material choca con lo notorio** (guía §4.6, pruebas 3a y
3c): el juicio «`nota` afirma [lo que la nota dice]» baja cuando lo que
dice choca con lo notorio — ballena-pez 0.92, Sídney 0.82, Lope 0.76,
morado 0.76, Toronto 0.64, Scott ~0.50, Gagarin 0.36–0.43 — frente a
0.91–0.99 cuando coincide. Con un expediente que es solo el enunciado
(`"2+2=5"`), 0.97. Crudos: `falso-c{1..6}-*`, `nombrar-*`,
`diag-2mas2-*`. La hipótesis de que bajara más cuando la nota «se
contradice a sí misma» quedó retirada: con la nota de Gagarin reducida
a la sola oración, el grado bajó más (0.13–0.23; prueba 7a).

**Cuando el expediente es un relato** (guía §4.6, prueba 7b): con
«Un hombre encontró un libro antiguo que señalaba, entre otras cosas,
que…», el juicio sobre lo que el libro señalaba queda en 0.85–0.93
—Gagarin 0.85, Jesús 0.86, Frat en la Luna 0.89, la isla inventada
0.92—, casi con independencia de que el contenido sea falso,
verdadero o inventado. Si el juicio deja de referirse al libro («Frat
encontró la isla de los durmientes.»), baja a 0.72: ya se juzga el
hecho, no el testimonio.

**Nombres de campo neutros**: describen el papel del dato, nunca el
veredicto. Es una precaución barata. Las claves de los juicios no
llegan al modelo (doc oficial, y medido en la prueba 7c: `q1`,
`libro_senalaba` y `falso` dieron 0.85–0.87 con el mismo juicio);
aun así, claves neutras (`q1`, `q2`…).

**Ilustrado**: `ticket` pide reembolso, sobre el ticket mixto → 0.99
(`spike-jev/cache/ticket-mixto.json`).

## Choice

**Qué es**: varios juicios alternativos, sin orden, en `criteria`. Jev
sopesa cada uno y reparte su soporte entre ellos. Devuelve el juicio
que concentra más soporte (`choice`, que no es una decisión de Jev
sino un cálculo sobre el reparto) + el reparto + la confianza. Jev no
responde: con «¿Qué hora es?» y las opciones 10:00, 11:00, 1:00, sin
expediente, igual reparte — sopesa tres juicios posibles. Y con
`instructions: ""` el reparto no cambió (prueba 6).

**Opción de salida siempre**: puede que ningún juicio se
sostenga; sin salida explícita, el soporte se reparte a la fuerza (la
confianza no detecta "ninguna vale"). Cuando algún juicio
encaja, la salida no roba soporte (≤ 0.01, prueba 2).

**Lee el reparto, no solo `choice`** (guía §4.6, prueba 7d): con el
relato del libro, `instructions` vacío y los juicios «un libro antiguo
señalaba que…» / «no hay evidencia de que un libro antiguo señalara
que…» (el segundo desmentido por el propio expediente), Jesús dio
0.99; Gagarin «fue» 0.84–0.87 y «no fue» 0.80–0.82, con confianza
0.60–0.73; quitando «antiguo», 0.91–0.95. `choice` fue siempre el
juicio que el expediente sostiene, pero lo notorio y el marco le
quitaron soporte en el reparto.

**Ilustrado**: `ruta` del ticket → `billing`, 1.0 unánime; categoría
del fan-out → `billing` 0.81 con reparto hacia bug (0.11) y account
(0.08) porque el mensaje mezcla tres asuntos.

## Score

**Qué es**: varios juicios alternativos en `criteria`, como **niveles
ordenados** que uno define; cada nivel se sopesa por separado. Jev reparte su soporte entre los niveles; el `score` es la
posición media de ese reparto, no un nivel elegido. Si el soporte se
reparte entre vecinos, el número cae en el medio (1.4); si se
concentra, cae en un nivel (2.0). Devuelve score + reparto + confianza
+ `legend` (tus niveles numerados desde 0).

**Ilustrado**: urgencia del ticket mixto → 1.4, confianza 0.33
(0.02/0.56/0.42): el mensaje no trae presión temporal explícita.
Frustración del fan-out → 1.0 unánime.

## Grado y bandas

**Qué es**: el resultado de una Noul es un grado de soporte; se lee por
bandas (ver Noul). «Verdadero» y «falso» son lecturas nuestras del
grado, no respuestas de Jev, y se refieren al juicio tal como está
redactado. En Choice y Score no hay bandas: se lee el reparto y su
confianza. La Noul es más «blanda» que la Choice (prueba 2: 0.82 frente
a 1.00 para el mismo objeto), así que no se comparan magnitudes entre
primitivas: se compara lo que dice cada una.

**Heurísticos, no valores calibrados**: las bandas (y los umbrales de
confianza) orientan la lectura. Jev es consistente —un juicio fijado
da casi el mismo grado en cada réplica (±0.01–0.02)— pero sensible:
una palabra del juicio o del marco («afirma» / «dice», «libro antiguo»
/ «libro») mueve el grado de forma que no se predice. El modelo es una
caja negra: no se buscan mecanismos; el diseño sigue líneas generales
y se afina en cada caso de uso, con casos de referencia y réplicas.

## Confianza

**Qué es**: el número 0–1 que acompaña a Choice y Score. No es un
juicio nuevo del modelo: es una cuenta determinista sobre
`probabilities`, recalculable en código. No agrega información.

**Fórmula** (reconstruida por nosotros; el doc solo publica el caso de
tres opciones y no la ofrece como contrato): `(N·p_max − 1)/(N − 1)`,
con N = opciones/niveles y p_max = soporte de la ganadora. En
palabras: qué fracción del camino va el pico **desde el empate hasta
la concentración total**. 0 = todas empatadas; 1 = todo en una; 0.5 =
mitad del camino, **no** "50 % de acertar".

**Verificado**: los 10 casos Choice/Score de nuestros crudos la
reproducen (`strawberry*`, `rapidisimo-opciones`, `fanout-5`,
`ticket-mixto`, `urgency-structured`). Las centésimas que no cuadran
(urgencia 0.33 vs 0.340 de la fórmula) son el redondeo a 2 decimales
de `probabilities`: la confianza se calcula sin redondear.

**Ilustrado**: `rapidísimo`, 4 opciones → empate = pico 0.25; pico
real 0.84 → (0.84 − 0.25)/(1 − 0.25) = **0.79**. Es decir: "la
ganadora va al 79 % del camino entre el empate a cuatro y la
concentración total", nada más.

**Tres trampas**:

- **Solo mira el pico, no la forma**: con 3 opciones, `[0.5, 0.5, 0]`
  y `[0.5, 0.25, 0.25]` dan 0.25 igual. La cola no se ve; si importa
  (la segunda pisándole los talones), leer `probabilities`.
- **No se compara entre distinto N**: mismo pico 0.56 → 0.34 con 3
  opciones, 0.47 con 6.
- **No es garantía individual**: 0.9 no es "90 % de acierto". TypeSafe
  habla de decisiones calibradas, pero la calibración vale para grupos
  de casos. El 82–92 % que cita el README es de classifier.dev (otro
  sistema).

**Noul no lleva** confianza: su grado se lee directamente por bandas.

**Para qué sirve**: enrutar. Una confianza baja es una **señal de
diseño** (juicio mal redactado, juicios de `criteria` que se pisan o un caso
que el expediente no decide), igual que la franja central de la Noul.
El 0,7 de la regla 21 es un valor de partida, no un umbral calibrado:
los umbrales se fijan por acción, dominio, primitiva e idioma, con
datos propios (regla 11), y lejos de grupos de casos reales.

**En una línea**: la confianza mide qué tan lejos está el pico del
empate — geometría del reparto, no promesa de acierto.

## Criteria (donde viven los juicios de Choice y Score)

**Qué es**: en Choice y Score, los juicios alternativos: cada opción
o nivel es un juicio que Jev sopesa frente al expediente. Por eso se
redactan como juicios, con las mismas reglas que el juicio de una
Noul. Medido: reescribir
dos descripciones movió las edades de 0.60–0.78 a 0.97–0.98.

**Reglas del doc, todas verificables**:

- **Situaciones, no grados**: "roto o degradado, pero existe
  workaround" le da a Jev algo que sopesar; "moderadamente grave", no.
- **Cada nivel se sopesa solo**: Jev no ve el número del nivel ni a sus
  vecinos; "peor que el anterior" no significa nada. Niveles
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
  Medido: urgency intermedia pasó de 0.98/0.97 a 1.0/1.0 unánime
  (`spike-jev/cache/urgency-structured.json`).
- **La confianza sola no valida una redacción**: se valida contra
  ejemplos etiquetados, nunca por el número.

Reglas propias (guía §3.4 y Anexo C): niveles sobre lo que el texto
dice o insinúa, sin solaparse, sin dobles negaciones ni indirección;
frontera discutible escrita
como decisión; ejemplos sin parecido con el material evaluado; caso
intermedio frecuente cubierto.

**En una línea**: los criteria no describen el resultado — son los
juicios que lo producen.

## Instructions

**Qué es**: un campo del API cuyo papel depende de la primitiva:

- **Choice y Score**: los juicios viven en `criteria`, y
  `instructions` agrupa esos juicios como alternativas o señala qué
  parte del expediente se juzga. Puede reducirse al mínimo e incluso ir
  vacío (prueba 6: `""` → mismo reparto). Cadena medida (cada ablación mantuvo el
  resultado):
  - juicio completo ("¿qué nivel ocupa la entrada X? Usa su posición
    entre las vecinas") → 11/11;
  - solo la cita (`'Hechos relevantes'`) → 11/11;
  - solo el path (`sentencias[0]`) → 5/5 al 1.00
    (`spike-jev/cache/tipo-path-pelado.json`).
- **Noul**: el juicio entero vive en `instructions`, y
  **cada palabra forma parte de él**. «`nota` afirma que…» (~0.50),
  «`nota` dice que…» (~0.70) y «Según `nota`,…» (~0.70) son juicios
  distintos (`diag-scott-*`). Sin predicado no hay juicio (caso
  biblioteca: paths pelados → 0.21).

**Cómo nombrar el material**: con un solo campo, la forma natural da
igual (`folleto`, «el folleto», «el texto», «el documento»: 0.98 /
0.01–0.02, prueba 3a); con varios campos, el nombre del campo entre
backticks.

**Lo que no funciona**: ordinales en prosa (`elemento 6 de doc`) —
hacia el final de la lista Jev pierde qué se juzga y los repartos
colapsan a uniforme (~0.2 por clase). El path ancla (`sentencias[2]`,
`` `tabla[3].edad` ``); el ordinal flota.

**Cómo redactar el juicio** (TypeSafe, con un complemento nuestro):

- Directamente, sin «es verdadero que» ni «es falso que».
- De modo que el grado alto sea lo que buscas: mejor «`mensaje`
  contiene datos personales» que «`mensaje` está libre de datos
  personales».
- Sin dobles negaciones ni indirección compleja: se sopesan con menos
  fiabilidad (límite de indirección).
- Diciendo exactamente lo que quieres: las palabras de alcance, las
  negaciones y las condiciones implícitas se leen al pie de la letra
  (límite de lectura literal). «¿Tiene **alguna** experiencia en
  Python?» no deja término medio.
- Sin contradicción entre `instructions` y los juicios de `criteria`
  (límite de instrucciones y criterios contradictorios).
- Complemento nuestro: las negaciones **en el material** se leen bien
  («No es seguro que…» 0.02; «No cabe duda de que…» 0.97, prueba 1).

(Los límites se citan por su nombre: la lista oficial tiene once y su
numeración cambió; guía §6, actualizada el 2026-09-23.)

**En una línea**: en Choice y Score, señalar con path basta; en Noul,
el juicio es la redacción.

## Regla y verbo

**Qué es**: en los casos con regla, dos palancas separadas — la regla
decide hacia qué lado se concentra el soporte, el verbo del juicio
decide cuánto. Medido en el caso biblioteca (socio con 4 préstamos,
nivel desconocido, tope pregrado 3 / posgrado 5), Choice [pregrado,
posgrado]:

| | regla simbólica | regla en prosa |
|---|---|---|
| "qué es" | pregrado 0.82 ✗ | posgrado 0.82 ✓ |
| "determinar" | pregrado 0.60 ✗ | posgrado 0.97 ✓ |

Crudos: `spike-jev/cache/biblioteca-*.json` (réplica de "determinar":
0.96).

**Lecciones**:

- **La regla se dice, no se simboliza**: topes en prosa (`max. 3
  préstamos`) cambian el resultado; flechas y pipes (`->`, `|`) no —
  cinco corridas fallaron con notación simbólica. La relación tiene
  que ser explícita y legible.
- **El verbo es parte del juicio**: con regla legible, "qué es"
  (reportar) dio 0.82 y "determinar" (derivar) dio 0.97. Lo mismo en
  Noul: «afirma» ≠ «dice» ≠ «según» (prueba 3). Los paths señalan el
  *qué*; el verbo dice qué juicio se sopesa.
- **Sin predicado no hay juicio (Noul)**: paths pelados (`socio.id
  solicitud.libro`) dieron 0.21 aun con el hecho a favor. El path
  pelado funcionaba en Choice porque el criteria carga el juicio; en
  Noul el juicio vive en instructions o no hay juicio.

**En una línea**: la regla decide el lado, el verbo decide el juicio.

## Independencia y fan-out

**Qué es**: todos los juicios se sopesan frente al mismo expediente,
aislados y en paralelo. Agregar o quitar juicios no mueve a los demás
(regla 25 del README). Medido: `titulo` 1.00 solo y en grupo de 11;
tres urgencias iguales juntas y separadas.

**Fan-out especulativo** (patrón oficial): mandar en un request todos
los juicios que el sistema pueda necesitar —incluso los que quizá no
importen (severidad de bug aunque no sea bug)— y que el código decida
después qué era relevante. Medido en `spike-jev/cache/fanout-5.json`:
5 juicios mezclados (Choice, Score, Noul, Noul, Score) en una llamada;
el código rutearía billing e ignoraría severidad.

**Solo cambia la operación**: 1 llamada en ~1 s vs N llamadas, N
latencias, N cobros de expediente.

## La lógica va en la estructura

**Qué es**: el JSON del request ya es lógica — legible por máquina,
no prosa para convencer. Cada campo cumple un rol lógico:

- `state`: el expediente (el material que se juzga).
- `questions`: los juicios (uno por ID, independientes).
- `type`: cómo se sopesa (un juicio / juicios alternativos sin orden /
  juicios alternativos ordenados).
- `criteria`: los juicios alternativos de Choice y Score (lo decible,
  cerrado).
- `instructions`: el juicio de la Noul; en Choice y Score, la pregunta
  que agrupa o el path que señala dónde mirar (`sentencias[2]`).

**Contraste con LLM**: en un LLM la lógica vive en el prompt
("analizá, clasificá, respondé en este formato...") — prosa que
instruye y se reza para que se obedezca. Acá la lógica vive en el
esquema. Por eso en Choice quitar prosa nunca dolió. Matiz: en la
Noul, la redacción **es** el juicio, y cambiar una palabra cambia lo
que se sopesa.

**Evidencia**: la cadena de ablaciones en Choice (state pelado, cita,
path) mantuvo resultados idénticos; lo único que rompió algo fue
salirse de la estructura (ordinales en prosa → colapso).

**En una línea**: estructura, no prosa — salvo en la Noul, donde la
prosa es el juicio.

## Garantías oficiales

Del doc de TypeSafe, textuales:

- **Resultados acotados**: *"Every answer is constrained to the
  options you supplied... Your code never has to recover a value from
  generated prose."* Salirse del tipo es imposible por construcción,
  no por obediencia — a diferencia de un LLM con structured output.
- **Resultados independientes**: *"Every answer is independent... You
  can add or remove questions without changing the others' results."*
  La base oficial de nuestra regla 25. Matiz nuestro (no está en el
  doc): vale con buen direccionamiento; con ordinales vimos
  degradación.

## Crudo

**Qué es**: el resultado del API **tal cual llegó por el cable**
(*raw response*), guardado en disco antes de que el código lo toque:
JSON íntegro con `answers`, `usage`, `model`.

**Para qué**: evidencia (el número se demuestra, no se copia),
re-correr sin re-pagar (se lee el archivo), auditoría (el spike
informa con números y los números viven en los crudos).

**Dónde**: `spike-jev/cache/`. Primeras sondas: `modalidad-50.json`,
`tabla-30.json`, `eel-indice-20.json`, `eel-indice-bare.json`,
`ticket-mixto.json`, `fanout-5.json`, `urgency-structured.json`,
`tipo-una.json`, `tipo-dos.json`, `tipo-array5.json`,
`tipo-path-pelado.json`, `noul-2mas2.json`, `noul-sol.json`,
`noul-bolivar.json`, `noul-suarez.json`, `noul-falso2.json`,
`noul-falso4.json`, `noul-array-t0.json`. Pruebas de reglas (guía,
Anexos A y B): `urg-*`, `noul-fuerza-*`, `score-urg-es-*`,
`score-fuerza-es-*`, `objeto-*`, `nombrar-*`, `falso-c{1..6}-*`,
`diag-scott-*`, `diag-2mas2-*`, `vacio-*`, `decimos-gagarin-*`,
`libro-*`, `claves-jesus-*`, `choice-jesus-*`, `choice-jesus-b-*`,
`choice-gagarin-*`.

**En una línea**: el acta de cada llamada.
