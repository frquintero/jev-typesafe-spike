# Plan del orquestador de Zettel (v1)

Fecha: 04-10-2026. Estado: **plan candidato**, para discutir con Frat antes de
escribir el prompt o el código. **05-10-2026:** la mesa de dominio
(`mvp/mesa-dominio-resultado.md`) se ejecutó; su cierre propone sustituir la
exigencia de un índice de casos previo de §4.1 por alcance por dominio y
reidentificación acreditada al consultar. La propuesta está a decisión de Frat:
§4.1 sigue intacto (mesa §9). Integra la visión operativa
(`zettel-vision-operativa.md`), lo acordado en la conversación del 04-10, la
investigación de Cowork y las dos revisiones independientes:
`orquestador-arquitectura-deepseek-2026-10-04.md` y
`orquestador-arquitectura-muse-2026-10-04.md`. Lo fijo es el marco
filosófico; todo lo demás se valida al andar.

## 0. La idea en un párrafo

El orquestador es un LLM que recibe una pregunta y propone cómo cambia lo
admisible al considerar los datos. **No trabaja solo ni suelto**: el código lo
conduce por estaciones fijas, le ofrece en cada una solo las herramientas que
corresponden, verifica lo que propone, hace las cuentas, llama al juez (Jev) y
registra todo. **La respuesta se espera en el corpus**: el orquestador intenta
primero con los datos; el mundo entra solo si falta algo o si el juez dice que
lo hallado no alcanza. Dentro de la estación del mundo, el orquestador sí tiene
libertad: encarga investigaciones y conectores, y decide cómo cerrar la brecha.

## 1. Principios

1. **Corpus primero.** Los datos se le dan porque ahí se espera la respuesta.
2. **El orquestador propone; el código dispone.** Lo que es control (orden de
   estaciones, cuándo se juzga, si se acepta un cierre, topes, R) lo hace el
   código. Lo que es contenido (estructurar la pregunta, leer, proponer filas,
   escribir encargos, redactar la respuesta) lo hace el LLM. (Separación
   control/contenido, arXiv 2609.00621.)
3. **Al código: formato, sintaxis, cálculos y consistencia.** No juzga si una
   ruta sostiene ni si una lectura es correcta.
4. **El juicio es externo.** Ningún modelo juzga su propia respuesta (un LLM
   que se autoevalúa tiende a darse la razón). Juez: Jev.
5. **K no se configura; es lo que entró.** Solo R se configura. Lo disponible
   es inventario. Cada cosa del mundo que entra queda en la ruta con su
   procedencia, y **la procedencia la anota el código**, no el agente.
6. **Nada simulado.** Mundo real: web real, APIs reales.
7. **Gratis y sin registro.** El orquestador solo usa lo que puede usar ya, por
   su cuenta. El usuario nunca entra al ciclo por infraestructura; es fuente de
   último recurso solo sobre el **contenido** de la pregunta.
8. **Simple primero.** Un solo orquestador, subagentes solo de lectura o
   aislados, sin enjambres.

## 2. Las piezas y quién hace qué

| pieza | qué es | qué hace | qué no hace |
|---|---|---|---|
| **Código** (plano de control) | Python de Zettel | lee la configuración, arma los prompts, conduce las estaciones, ejecuta herramientas, anota procedencia y fecha, verifica forma, calcula, llama a Jev, aplica topes, guarda | juzgar contenido |
| **Orquestador** | LLM capaz (`deepseek-v4-pro`, por verificar) | estructura la pregunta, lee el corpus, propone tablas y rutas, declara la brecha, escribe encargos, redacta la respuesta | ejecutar acciones en el mundo; juzgarse |
| **Investigador** | LLM barato (`deepseek-flash`) con búsqueda y lectura web | cumple un encargo de búsqueda y devuelve lo hallado con artefactos recuperables | escribir en ningún lado |
| **Programador** | LLM barato con ejecución aislada | escribe y prueba un conector a una API pública gratuita y sin registro | tocar repos, claves o la red fuera del sitio permitido |
| **Biblioteca de cómputo** | funciones fijas en código, con versión | calendario, husos (`zoneinfo` + `tzdata`), aritmética, «cierre del X al Y» | nada fuera de su lista |
| **Jev** | juez de TypeSafe (`jev-1.13.0`) | dice cuánto sostiene un juicio dado un expediente | responder preguntas, buscar datos |
| **Corpus** | fichas de los documentos + datos derivados + índice de casos | se consulta por búsqueda | — |
| **Caja de conectores** | conectores que ya funcionaron | se reutilizan | — |
| **Registro de corrida** | traza append-only | cada llamada, argumentos, resultado, procedencia, tiempo, tokens | — |
| **Usuario** | quien pregunta | fija R (en la MVP, el archivo de configuración); responde solo preguntas de contenido | resolver infraestructura |

## 3. El recorrido de una consulta: siete estaciones

```
E0 código        preparar
E1 orquestador   encuadrar y responder con el corpus     (herramientas: corpus, calcular)
E2 código        verificar y clasificar
E3 Jev           ¿alcanza lo hallado?                    (solo si hay respuesta candidata)
E4 orquestador   traer mundo (ciclo acotado)             (herramientas según R ∩ inventario)
E5 orq. + código cerrar: propone el orquestador, dispone el código
E6 código        entregar y registrar
```

**E0 · Preparar (código).** Lee la configuración (R, modelos por rol, topes),
fija las **anclas** (fecha y hora del sistema), carga el inventario
(herramientas instaladas y caja de conectores) y el estado del corpus. Abre el
registro de corrida. Arma el prompt de E1.

**E1 · Encuadrar y responder con el corpus (orquestador).** Herramientas
ofrecidas: `buscar_en_corpus`, `leer_ficha`, `calcular`. Ninguna del mundo:
así «corpus primero» es una propiedad del sistema, no un consejo. Produce:

- **Encabezado de la pregunta:** caso (id del índice), aspecto, condiciones,
  dominio (escala y regla). **Queda fijo** para toda la corrida: si cambia, es
  otra pregunta.
- **Tabla inicial** (`resto` admisible).
- **Tabla candidata** solo con lo que da el corpus, más reglas de lectura y
  cálculos si R los admite.
- **Brechas**, cada una con: qué falta; de qué tipo es (dato, regla de lectura,
  cálculo, validación); dónde está la autoridad sobre eso (el corpus, el saber
  del orquestador, el código, una fuente externa nombrada).

Esto es la «encuesta previa» de Magentic-One (hechos dados, a buscar y dónde, a
derivar, conjeturas) puesta en el vocabulario de Zettel: dados = D; a buscar =
brecha con fuente; a derivar = biblioteca de cómputo; conjeturas = saber del
orquestador, que entra como premisa solo si R lo admite.

**E2 · Verificar y clasificar (código).** Verifica forma, que cada id de ruta
exista, que el encabezado no cambió, que **cada id de cada ruta esté admitido
por R** (R se aplica a las premisas, no solo a las herramientas), y recalcula
cada cómputo con la biblioteca. Calcula el efecto (diferencia de tablas).
Clasifica:

- **Sin respuesta candidata** (el corpus no da nada para el caso y aspecto) →
  va directo a E4 si R lo permite y alguna brecha tiene autoridad fuera del
  corpus; si no, a E5 con «no establecido» o «no cerrable». **No se llama a
  Jev**: el resultado sería previsible.
- **Con respuesta candidata** → E3.

**E3 · ¿Alcanza lo hallado? (código llama a Jev).** Un juicio por fila
admisible, anclado al material («Según `aviso`, …»), con un expediente que
contiene solo lo pertinente: los respaldos literales y los valores de la ruta,
nombrados por su papel. El código lee la banda y **ofrece al orquestador las
jugadas permitidas**; el orquestador elige una y la justifica:

| banda de Jev | lectura (guía §3.1) | jugadas que ofrece el código |
|---|---|---|
| > 0,85 | muy seguramente cierto | cerrar |
| 0,65 – 0,85 | seguramente / hay bases | cerrar con cautela, o corroborar (si R lo permite) |
| 0,30 – 0,65 | el juicio no se puede formar | **releer y reformular**: es señal de diseño o de lectura, no de falta de mundo |
| < 0,30 | la base no es firme / falso | revisar la lectura; si persiste, complementar con mundo |

Los bordes son el punto de partida de la guía; se calibran con datos (patrón
oficial *confidence routing*). La forma exacta de los juicios se fija con una
sonda pequeña antes de usarla (fase F2).

**E4 · Traer mundo (orquestador, ciclo acotado).** Herramientas ofrecidas:
las que R admite **y** el inventario tiene: `encargar`, `usar_conector`,
`calcular`, `buscar_en_corpus`, `preguntar_usuario` (solo contenido). Aquí el
orquestador tiene libertad: decide qué encargar, a quién y en qué orden. Cada
resultado vuelve por el código, que lo **verifica** (por ejemplo, vuelve a
llamar a la API o a abrir la URL) y le asigna el origen: si hay artefacto
recuperable, es fuente consultada con fecha; si no, queda marcado como saber de
una herramienta sin respaldo. El orquestador actualiza la tabla; el código la
reverifica (como en E2) y Jev juzga **solo lo que cambió**.

Guardias del código en E4: un **detector de ciclos** (si la misma herramienta,
con los mismos argumentos, devuelve lo mismo 2 o 3 veces, se corta o se
replanifica), contador de estancamiento (sin cambio en la tabla), y topes de
encargos y de tiempo. Si se agota un tope, el desenlace es **agotada**.

**E5 · Cerrar (propone el orquestador, dispone el código).** El orquestador
propone: tabla final, desenlace, respuesta al usuario y, si hay, dato derivado.
El código acepta o devuelve lo que falta (con un número máximo de vueltas):
forma; encabezado intacto; toda ruta resuelve; R por premisa; efecto calculado;
condiciones de entrega de la visión §5 (hubo efecto, se respetó R, los
conflictos se muestran). Si entró mundo después de E3, Jev juzga el sostén del
cierre; su banda fija el **tono** de la entrega.

**E6 · Entregar y registrar (código).** Entrega la respuesta. Guarda el dato
derivado en el corpus, con radicación de hoy, dependencias completas (valor,
origen, procedencia, fecha de consulta, versión), rutas y juicio. Guarda los
conectores nuevos en la caja, en estado candidato. Cierra el registro.

## 4. Las conexiones

### 4.1 Con el corpus

**Ingesta (antes de cualquier pregunta; ya existe en parte):** oraciones
numeradas (código) → ficha (`ficha_v1`, LLM) → verificación literal (código) →
**índice de casos** (nuevo) → radicación.

El índice de casos es el hueco que señalaron las dos revisiones: saber que
«el refugio» de un documento y «el refugio» de otro son el mismo caso. Ese
juicio se hace **una vez, al incorporar** (el LLM propone la reidentificación,
el código la guarda y queda revisable, como la fusión de ítems en Wikidata).
Después, al consultar, emparejar es mecánico. Sin índice no hay conflicto
entre documentos ni promoción de dependencias.

**Ids globales:** `documento:id` (`aviso:D6`); derivados `DD…`; mundo `M…` por
corrida. La K de la ficha sigue siendo **capa**.

**Consulta:** `buscar_en_corpus(caso, aspecto, texto)` devuelve
**determinaciones** (la unidad del marco), no fragmentos: id, caso, aspecto,
valor, condiciones, respaldo literal, documento, radicación y, si es derivado,
su bloque de derivación. **En la MVP la implementación es trivial (devuelve
todas las fichas)**; el contrato queda fijo y la implementación crece con el
corpus. Los **datos derivados son corpus**: se recuperan igual, y si otra
pregunta los reutiliza se aplica la promoción.

### 4.2 Con la pregunta

La pregunta llega como texto. El orquestador la estructura en E1 (caso,
aspecto, condiciones, dominio); el código congela ese encabezado. R viene de la
configuración. Las anclas (fecha y hora) las inyecta el código: el orquestador
no las recuerda ni las supone.

### 4.3 Con las herramientas

| herramienta | estación | qué hace | quién ejecuta |
|---|---|---|---|
| `buscar_en_corpus`, `leer_ficha` | E1, E4 | consultar datos | código |
| `calcular(funcion, args)` | E1, E4 | biblioteca de cómputo con versión | código |
| `encargar(encargo)` | E4 | lanzar un subagente (investigador o programador) | código + subagente |
| `usar_conector(id, args)` | E4 | reutilizar un conector de la caja | código (aislado) |
| `preguntar_usuario(pregunta)` | E4 | último recurso, solo contenido; termina la corrida con la pregunta | código |

El juez y el cierre **no** son herramientas del orquestador: son estaciones que
impone el código.

**El encargo tiene forma fija** (AOrchestra: instrucción, contexto, herramientas,
modelo; Anthropic: objetivo, formato, fuentes, límites):

```
rol:               investigador | programador
objetivo:          uno solo, verificable
contexto:          solo lo pertinente (caso, aspecto, condiciones, valores de la ruta)
fuente sugerida:   dónde está la autoridad sobre el dato
condiciones:       gratis, sin registro, solo lectura
devolución:        forma fija (abajo)
```

Ejemplo de la visión: «Investiga si Avianca ofrece una API pública, gratuita y
sin registro que dé la duración del vuelo AV-569 del 28-9-2026. Devuelve: si
existe; dónde está documentada; un ejemplo de consulta sin credenciales y su
respuesta real».

**Devolución del investigador:** valor hallado, URL, fecha de consulta, cita
literal de la fuente, cómo reverificarlo; para una API: si existe, documentación,
llamada de prueba sin credenciales y su respuesta. «El agente encontró una API»
no prueba nada: el código la vuelve a llamar.

**El programador** sigue el orden que funcionó en la literatura (ConnectorForge,
Alita): sondear la API viva sin credenciales → sacar el esquema de lo que
devuelve → armar el conector desde una plantilla → probar → reparar hasta 3
veces. Corre **aislado**: sin red salvo el sitio de la API, sin acceso a repos
ni claves, con tope de tiempo. Devuelve el script, su resultado y la versión del
intérprete.

**La caja de conectores** (Alita-G): cada conector guardado lleva autor, fecha,
fuente verificada, la condición «gratis y sin registro» con su fecha de
verificación (caduca) y versión. Se reutiliza con `usar_conector`. La
abstracción de conectores (parametrizarlos para otros casos) queda para
después.

### 4.4 Con el código

Lo que el código hace, en una lista: conducir estaciones; ofrecer herramientas
por estación y por R ∩ inventario; ejecutarlas y anotar procedencia y fecha;
verificar forma (esquemas estrictos); verificar ids, encabezado, R por premisa;
recalcular con la biblioteca; calcular el efecto; llamar a Jev; detectar ciclos y
aplicar topes; guardar dato derivado, conectores y traza. Base existente:
`mvp/pieza1/pieza1.py` (verificador de forma, comparador, guardar, mantener).

### 4.5 Con Jev

- **Lo llama el código**, en dos lugares: E3 (¿alcanza lo hallado?) y E5
  (sostén del cierre, si entró mundo después de E3).
- **Jev no responde preguntas: sopesa juicios.** Se le pasa la respuesta escrita
  como juicio anclado al material, con un expediente curado.
- **La franja central no significa «falta mundo»:** significa juicio mal
  formado o desconectado; se reformula, no se sale a buscar.
- **Banda → jugadas** (E3) y **banda → tono** (E5).
- Pendiente de la fase F2: la redacción exacta de los juicios (y si conviene un
  segundo juicio sobre el mundo, sin ancla, para distinguir «el mundo no sabe»
  de «el mundo contradice»). Se decide con una sonda, no a priori.
- Costo despreciable (0,042 USD por millón de tokens de entrada; 1–2,5 s por
  llamada medidos en el spike).

## 5. El expediente: estado y traza

- **Estado = la tabla de A(Q)**, con su encabezado, dependencias, campo,
  conflicto y desenlace. Hace de los dos registros de Magentic-One: la tabla
  inicial más las brechas es el registro de la tarea; la diferencia entre la
  tabla vigente y la anterior es el registro del progreso. De las cinco preguntas
  de progreso de Magentic-One, cuatro las responde el código (¿resuelto?, ¿ciclo?,
  ¿avance?, ¿qué estación sigue?); solo «¿qué hago ahora?» es del orquestador.
- **Traza = registro de corrida** (append-only): cada llamada a modelo o
  herramienta, con argumentos, resultado, procedencia, tiempo y tokens. Sirve
  para auditar K, depurar y medir costo por estación.

## 6. Salidas y desenlaces

- **Al usuario:** la respuesta en lenguaje natural, con su ruta en palabras
  (oraciones, fuentes, fechas), sin ids internos; el tono según la banda.
- **Al sistema:** el dato derivado (forma de determinación + bloque de
  derivación; esquema 2 §5) y la traza.
- **Desenlaces de la pregunta:** cerrada · en conflicto · no establecido · no
  cerrable. **Desenlace de la corrida:** agotada (se cortó por un tope; se
  entrega la tabla parcial y la brecha pendiente). No se mezclan.

## 7. El prompt del orquestador (qué partes tiene; no está escrito)

Lo arma el código, **uno por estación** (E1, E4, E5), desde el archivo de
configuración. Partes:

1. Rol y tarea de la estación.
2. Vocabulario mínimo (caso, aspecto, condiciones, dominio, tabla, ruta,
   brecha), con ejemplos que **no** vengan de los documentos de prueba.
3. Entrada: pregunta, R, anclas, inventario del corpus.
4. Herramientas ofrecidas en esa estación: qué hace cada una, cuándo usarla.
5. Cómo escribir un encargo (solo en E4).
6. Reglas de la tabla (las de la mesa 1 y el esquema 2).
7. Formato de salida: esquema JSON estricto, que el código verifica.

## 8. Configuración (ejemplo)

```yaml
R:
  fuentes_admitidas: libre        # solo el documento | sin externas, con el mundo del orquestador | libre
  autorizacion_agentes: si
  anclas: hora_del_sistema
modelos:
  orquestador: deepseek-v4-pro    # por verificar con la clave
  investigador: deepseek-flash
  programador: deepseek-flash
  juez: jev-1.13.0
guardias:                         # de seguridad, no de R
  max_encargos: 6
  max_vueltas_cierre: 2
  repeticiones_iguales: 2
  tiempo_max_s: 600
jev:
  umbral_cerrar: 0.85
  umbral_cautela: 0.65
  franja_central: [0.30, 0.65]
```

## 9. Seguridad

- El texto que llega de la web o de un documento es **dato, nunca
  instrucción**.
- El investigador solo lee; el programador corre aislado (el aislamiento hay
  que pedirlo explícitamente: ningún entorno lo trae por defecto).
- Sin credenciales en ningún lado («gratis y sin registro» es también control
  de seguridad).

## 10. Evaluación (escrita antes de construir)

Batería fija, tres réplicas, con respuestas de referencia escritas antes:

| caso | qué prueba | resultado esperado |
|---|---|---|
| Aviso Q1, Q3, Q5 | corpus primero | cerrada con D, sin salir al mundo |
| Aviso Q2 | sin efecto | no establecido; diferencia de tablas vacía |
| Aviso Q4 | brecha de contenido | busca, no encuentra; no cerrable; pregunta al usuario por el collado |
| Aviso Q6r | regla de lectura + cálculo | 1-11-2026; dato derivado guardado; mantenimiento |
| Q6r con R «solo el documento» | **trampa de R** | no usa la regla de lectura: «el documento no establece la reapertura» |
| Documento real + Wikidata | conector gratis y sin registro | lo encuentra, lo prueba, cierra con fuente consultada |
| Vuelo de la visión | mundo real que no se puede consultar gratis | busca, no hay API gratuita sin registro; deja la brecha abierta y lo dice |
| Dos documentos | conflicto real (fase F4) | en conflicto, ambas posiciones con su procedencia |

Métricas: errores de forma (código), errores de fondo (lectura humana), llamadas,
tokens, tiempo y encargos por estación, estancamientos.

## 11. Fases de construcción

Cada fase tiene una conjetura; se corre solo si la hay. El prompt se muestra
antes de correr.

- **F0 · Código sin LLM.** Biblioteca de cómputo; verificador ampliado (R por
  premisa, encabezado fijo, efecto); registro de corrida; contrato de
  `buscar_en_corpus`. Base: `pieza1.py`.
- **F1 · Solo corpus** (E0, E1, E2, E5, E6; sin Jev ni mundo). Conjetura: con el
  corpus, el orquestador cierra Q1, Q3, Q5 y Q6r, declara bien las brechas de Q2
  y Q4, y respeta R en la trampa.
- **F2 · Jev.** Sonda chica sobre la redacción de los juicios; después, E3 y E5.
  Conjetura: la banda separa lo que el corpus sostiene de lo que no.
- **F3 · Mundo.** E4 con investigador, programador, aislamiento y caja.
  Conjetura: encuentra lo gratis y sin registro cuando existe, y deja la brecha
  abierta cuando no.
- **F4 · Varios documentos.** Índice de casos y conflicto real.

## 12. Decisiones para Frat

1. **Estaciones fijadas por el código, con libertad del orquestador en E4.**
   Lo proponen las dos revisiones; Cowork coincide.
2. **Guardias de seguridad en la configuración** (encargos, vueltas, tiempo).
   No son R ni limitan qué herramientas usa: solo cortan si se enreda. Las dos
   revisiones insisten (AWS: un tope que vive solo en el prompt se puede
   saltar).
3. **Modelos por rol:** `deepseek-v4-pro` para orquestar, `deepseek-flash` para
   encargos. V4-Pro cuesta unas 4 veces más que Flash; los subagentes hacen el
   volumen.
4. **Biblioteca fija de cómputo** (los tres coincidimos).
5. **Contrato de búsqueda del corpus desde ya**, con implementación trivial en la
   MVP.
6. **Tras el juicio de Jev, el código ofrece jugadas y el orquestador elige.**

## 13. Qué se tomó de cada fuente

| fuente | se tomó | se dejó |
|---|---|---|
| Magentic-One (Microsoft, 2024; orquestaciones 1.0, jul-2026) | la encuesta previa (dados / a buscar y dónde / a derivar / conjeturas); las cinco preguntas de progreso; replanificar al estancarse | copiar sus prompts; el equipo que «habla por turnos»; la revisión humana del plan |
| Anthropic, sistema multiagente (2025) | cómo escribir un encargo; escalar el esfuerzo; no buscar sin fin lo que no existe; reglas de calidad de fuentes | el paralelismo masivo (aquí no hay búsquedas a lo ancho) |
| CRAG (2024) | corpus primero y un evaluador que decide si salir | medir relevancia de documentos (aquí se juzga la ruta) |
| Alita / Alita-G (2025) | fabricar conectores; guardarlos y reutilizarlos | generar herramientas para todo (el cómputo va en biblioteca fija) |
| AOrchestra (2026) | encargo = instrucción + contexto curado + herramientas + modelo | — |
| Uno-Orchestra (2026) | no delegar cuando no hace falta | una política aprendida por RL |
| Separación control/contenido (2026) | el control tipado en código | — |
| Revisión de DeepSeek | estaciones; la tabla como único estado; R por premisa; origen asignado por el código; encabezado fijo; desenlace «agotada»; aislamiento explícito | preseleccionar datos por código en la consulta (es juicio: va en la ingesta) |
| Revisión de Muse | juez y cierre impuestos por el código; detector de ciclos mecánico; una sola primitiva `encargar`; índice de casos en la ingesta; contrato de búsqueda; registro de corrida; orden sondear→esquema→plantilla del programador | — |

Fuentes: las URL están en las dos revisiones y en la conversación del 04-10.
Modelos y API de DeepSeek: api-docs.deepseek.com (precios, herramientas en
modo de razonamiento, modo estricto).
