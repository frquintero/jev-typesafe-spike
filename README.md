# Spike Jev — detección con modelo de decisiones

## Visión: el objetivo primordial de Zettel

Zettel busca construir, a partir de los documentos que el usuario elige, un
**ecosistema de unidades temáticas y datos** sobre el que operen
**preguntas** y se obtenga **información**.

**Información**, en el sentido del marco (`definiciones-del-marco.md`, A.8),
no es algo guardado en el texto que se trae: es el **cambio en A(Q)**, el
conjunto de respuestas admisibles a una pregunta Q, cuando se consideran
datos D conforme a reglas R. Tres modos: respuestas que dejan de ser
admisibles, respuestas que ganan o pierden sostén, distinciones que
aparecen. El mismo dato puede excluir una respuesta, sostener otra y quedar
mudo ante una tercera.

*Ejemplo.* Q: «¿La represa existía en 1980?»; antes de considerar datos,
A₀ = {sí, no}. Dato: *represa · año de construcción · 1972*; regla: lo
construido existe después, salvo demolición. Resultado: el «sí» gana
sostén, y el «no» queda admisible solo si hubo demolición antes de 1980
(una distinción que aparece). Ese cambio, con su ruta, es la información.
El dato *represa · volumen · unos 40 millones* queda mudo ante esa
pregunta.

**Qué se sigue:**

- **Recuperar no es responder.** Traer un pasaje, o reconstruir tal cual un
  dato registrado, es recuperar; la información exige D, R y Q. Por eso la
  literatura de RAG y *chunking*, que mide si se recupera el pasaje, no nos
  sirve de vara.
- **Todo se juzga por lo que permite hacer a una pregunta:** encontrar los
  datos pertinentes (el campo); que cada dato traiga caso, aspecto y
  condiciones, para que las reglas operen sobre él y no quede mudo; mostrar
  el paso de A₀ a A₁ con su sostén y su ruta; y, al evaluar, separar
  recuperar de responder.
- **Las unidades temáticas** dan el contexto que impide que un dato pierda
  su caso y sus condiciones al separarse del texto, y son el terreno donde
  la pregunta opera.

Antecedentes: la pregunta como conjunto de respuestas posibles (Hamblin) y
la información como exclusión de posibilidades (Bar-Hillel y Carnap). El
marco agrega sostén, distinciones nuevas y reglas, y su cambio no es
monótono.

**Cómo lo soñamos, de punta a punta:** `zettel-vision-operativa.md`
(04-10): un ejemplo completo con documento, extracción, pregunta,
orquestador que trae el mundo (K), reglas de la consulta (R), juicio de Jev,
información para el usuario y dato derivado para el sistema.

## Principio de trabajo: el camino se hace al andar

Lo único fijo, o casi fijo, es el **marco filosófico** (`marco filosófico/`)
y lo que se deriva directamente de él. Los planes, arquitecturas candidatas,
niveles, versiones de prompts y anotaciones alrededor de los proyectos son
ideas en desarrollo: algunas ni siquiera llegan a una prueba. No son ley.
Antes de usarlas como base, se valida que sigan vigentes y que se relacionen
con lo que se está haciendo.

## Proyectos en curso

Solo referencia al proyecto que se trabaja; no es bitácora (el detalle vive
en el README, PLAN y tareas de cada carpeta).

- Fecha: 2026-10-01 · Proyecto: ficha de datos con DeepSeek (`unidades/`)
- Fecha: 2026-10-02 · Proyecto: NotebookLM como extractor alternativo o
  complementario (`notebooklm-spike/`)
- Fecha: 2026-10-03 · Proyecto: pruebas NotebookLM — grafo semántico
  (paso 2 en NotebookLM sobre unidades de DeepSeek) (`nblm-grafo-semantico/`)
- Fecha: 2026-10-05 · Proyecto: MVP de Zettel — mesas 1 y 1b (forma de la
  tabla de A(Q), a mano), pieza 1 (conflicto y dato derivado, con
  `pieza1.py`; registro en `mvp/pieza1/registro.md`), plan del orquestador
  (candidato, con dos revisiones), mesa de dominio (T1–T6, ejecutada en
  comprobación guiada; registro en `mvp/mesa-dominio-resultado.md`), que
  actualizó §4.1 del plan, y pruebas del paso 1 con Muse (`mvp/pruebas/`;
  candidato v9 congelado) (`mvp/`)

## Frentes cerrados: lecciones e ideas rescatables

**LangExtract (Google), 2026-10-03 — evaluado, no adoptado**
(`langextract-spike/`). Revisado su código y su documentación, sin llamadas
a modelos. Sirve para extracciones locales (entidades, atributos, citas) en
textos largos. Para lo nuestro no: su unidad es el **trozo por tamaño**
(1000 caracteres por defecto), procesado siempre con la misma instrucción;
nosotros buscamos estructura semántica (quién sostiene qué, identidad del
caso, cómo se desarrolla una idea), y eso exige unidades de sentido
(unidad temática v1). En biomar1, un trozo tocaba cuatro subtemas y un
subtema quedaba repartido entre trozos. **Lección:** «estructurado» no es
solo tener campos, es tener lógica semántica; antes de adoptar una
herramienta, mirar qué unidad de texto usa.

Ideas que podrían servirnos:

1. **Anclaje exacto con estado de coincidencia.** Cada extracción lleva su
   intervalo de caracteres en el texto original y si se ubicó de forma
   exacta, parcial o aproximada. Nosotros aceptaríamos solo la exacta; lo
   demás va a revisión. Encaja con el respaldo por componente y la
   verificación por código.
2. **Página de revisión automática.** Un HTML con el texto y cada
   extracción resaltada en su lugar, para auditar a ojo sin leer JSON.
3. **Contexto del documento en cada llamada** (su `additional_context`).
   Al procesar una unidad temática, adjuntar un mapa breve del documento
   (subtemas y casos) para que la unidad no se lea aislada.

## Estado actual (2026-10-04)

**04-10: visión operativa de Zettel** (`zettel-vision-operativa.md`): la
pregunta como punto de partida, el mundo (K) junto al corpus (D), reglas de
la consulta (R), orquestador y Jev. Lo que separa de la MVP: etapas 4–6, sin
probar.

**Nuevo enfoque del paso 2; rondas F1–F5 hechas y F6 corrida, sin evaluar; prompt vigente `ficha_v1`, congelado.** El marco
queda fijo: ensayo de Frat «¿Qué es un dato?», versión del 30-09 (resumen
operativo en `memoria de trabajo y pendientes.md`, §2). Las pruebas del
enfoque anterior (`datos_pABQ5`, `datos_pABQ6B`) se suspendieron el 30-09;
lo aprendido con ellas queda en `historico/memoria-hasta-2026-10-01.md`.

**Qué hacemos.** Reconstruir con un LLM barato (DeepSeek `deepseek-flash`)
**todo lo que un texto establece, organizado desde el caso de estudio**, en
el vocabulario del ensayo (caso de estudio, aspecto, marca de posición,
condiciones, valor, dato). El extractor ya no decide «qué es dato»: la
pertinencia se decide después (Jev o la pregunta que se le haga al texto).
Es la capa de datos del grafo datos → argumentos → tesis de **Zettel**.

1. **Subtemas** (`unidades/extraer_unidades.py`, prompt `unidades_v5`): el
   código parte el texto en oraciones y las numera; el LLM las agrupa en
   subtemas. Se conserva, pero queda fuera de la prueba actual.
2. **Ficha** (`unidades/ficha_doc.py`, prompt vigente `unidades/prompts/ficha_v1.md`):
   una llamada por documento, con el texto entero numerado. La ficha tiene
   siete listas: casos, relaciones, capas (creer, recomendar, decir,
   suponer, citar), determinaciones, acciones, marcas y dudas. Toda
   determinación lleva los fragmentos literales que la respaldan. El código
   solo numera y verifica que cada respaldo, mención y marca esté literal en
   su oración; no juzga contenido. El ejemplo del prompt es el texto del
   estanque, que por eso queda fuera de la prueba.

**Pruebas del núcleo conceptual en textos cortos** (DeepSeek; vara de Frat:
cerca del 90 % correcto y ejecución ágil; detalle en la memoria, §3).

| Ronda | Prompt | Textos | Resultado |
|---|---|---|---|
| F1 | `ficha_v0` | `puente1`, `represa1` (desarrollo, de Cowork) | núcleo fiel en lo grueso; inestable en detalles |
| F2 | `ficha_v0` | `pintura1`, `cafe1` (reserva, de ChatGPT; preguntas en `unidades/gold/preguntas_reserva_F2.md`) | 12 preguntas respondidas en 3 réplicas (36/36); forma de relaciones y acciones inestable |
| F3 | `ficha_v1` (contrato de representación) | los cuatro | forma estable, 36/36 conservado; el costo subió (37–79 s, 10–16 mil tokens de razonamiento por texto) |
| F4 | `ficha_v1` + referencias implícitas | `represa1`, una corrida | «otra sequía igual» queda enlazada a la sequía de 2024 sin confundirlas |
| F5 | `ficha_v1` congelada | `jardin1`, `radio1`, `biblioteca1` (reserva por géneros, de ChatGPT; preguntas en `unidades/gold/preguntas_reserva_F5.md`) | fidelidad ≈95 % (60/63); formato estable; no ágil: 76–127 s y 15–25 mil tokens de razonamiento por texto de ~220 palabras |
| F6 | `ficha_v2` (candidato: condiciones del acto de sostener algo) | `jardin1`, `radio1`, `biblioteca1`, tres réplicas | **corrida, sin evaluar** (crudos en `unidades/cache/`); `ficha_v1` sigue siendo la base |

**Directriz de Frat:** los cambios al prompt se piensan como generalización,
para documentos de contenido general (divulgación, ensayo no especializado,
opinión), no para resolver los textos de prueba. **Siguiente paso:** decidir cómo lograr agilidad sin perder fidelidad;
es una decisión de arquitectura o de modelo, no de retocar el prompt
(`ficha_v1` queda congelada mientras tanto).

La lectura es en dos dimensiones: qué recupera y qué agrega o deforma, con
los 11 errores de la memoria (§2.4) como guía; se admiten errores nuevos.
**Fuera de alcance:** subtemas, inventario de casos, documentos largos y
Jev. **Arquitectura propuesta para después (no decidida):** oraciones
(código) → subtemas (LLM) → inventario de casos de estudio por documento
(LLM) → determinaciones por foco (LLM) → verificación literal (código) → Jev
(identidad, correferencias, omisiones mirando el texto).

**Dónde está cada cosa.**

- Estado vigente, marco, decisiones, errores, lecciones y pendientes:
  `memoria de trabajo y pendientes.md` (fuente única del estado; §2 manda
  sobre lo anterior).
- Definiciones del marco (filosóficas con líneas del ensayo, operativas y
  homónimos): `definiciones-del-marco.md` (documento vivo).
- Visión operativa de Zettel (ejemplo completo de punta a punta: documento,
  extracción, pregunta, orquestador, mundo K, reglas R, Jev, información y
  dato derivado): `zettel-vision-operativa.md` (documento vivo).
- Rondas (cambio, conjetura, gold, comandos, reporte): `unidades/PLAN.md`
  (F1–F6 al final); mensaje para el ejecutor de cada ronda en
  `unidades/mensaje_<RONDA>.txt`. Prompts en `unidades/prompts/`, textos en
  `unidades/docs/`, golds y preguntas en `unidades/gold/`, crudos en
  `unidades/cache/`.
- Enfoque anterior: `unidades/extraer_datos_doc.py` (cadena subtemas → datos)
  y `prototipos/` (batería de ejemplos prototípicos, `prototipos/PLAN.md`).
- Reglas del ejecutor (red, claves, comandos, reportes): `AGENTS.md`.
- Píldoras (precisiones de vocabulario y conceptos que surgen en la
  planeación): viven fuera del repo, en `~/Claude-memoria/pildoras.md`.
- Vocabulario de Jev: `jev_typesafe_guia_pedagogica_v2.md` y
  `diccionario.md` (no se editan sin aprobación; la guía no cambia mientras
  estemos en pruebas de extracción).

**Cómo se trabaja.** Frat y Cowork planean (piensan, discuten, conjeturan);
solo hay corrida cuando hay una conjetura nueva, y el prompt se muestra antes
de correr. Cowork escribe prompt y ronda, hace commit y push; el ejecutor
(Muse Code, GPT-6 Luna o Claude Code) corre sin modificar nada, reporta sin
veredicto y sube los crudos; Cowork evalúa contra la conjetura y Frat decide.

**Antecedentes.** `niveles/` (extracción sobre el texto entero, `datos_v1`–
`v8`) queda sin trabajo activo. El objetivo original del spike (Jev en lugar
de GLM para la detección de estructura del piloto EEL; secciones Contexto,
Arquitectura y Plan de pruebas, más abajo) está **suspendido**, no
abandonado. Las reglas 1–26 y el marco conceptual de Jev siguen vigentes.

## Correr las pruebas en local (claves)

**Sin proxy desde el 04-10.** Antes, un proxy local (`proxy_local.py`) ponía
la clave en cada llamada para que el código fuera idéntico en la nube y en
el PC. Frat decidió que eso no hace falta (la nube la cubre Claude Code), y
se retiró: más simple. Ahora `call_model` (`niveles/run_niveles.py`), por
donde pasan las llamadas del trabajo activo, lee la clave del entorno según
el proveedor. Las claves nunca se imprimen ni quedan en archivos del repo.

**Claves de los proveedores.** Son variables globales del shell, definidas en `~/.bashrc`:

| Proveedor | Host | Variable |
|---|---|---|
| TypeSafe (Jev) | `api.typesafe.ai` | `TYPESAFE_API_KEY` |
| Z.ai (GLM) | `api.z.ai` | `ZAI_API_KEY` |
| DeepSeek | `api.deepseek.com` | `DEEPSEEK_API_KEY` |
| xAI (Grok) | `api.x.ai` | `XAI_API_KEY` |

`ZAI_API_KEY` no está escrita en `~/.bashrc`: la carga desde `~/.config/zai/api_key.env`. Para agregar o cambiar una clave, pon una línea `export NOMBRE=clave` en `~/.bashrc` y corre `source ~/.bashrc` (para xAI hay un asistente: `bash configurar_clave_xai.sh`, que la pide sin mostrarla).

**Correr un script** (desde un shell no interactivo, como Desktop Commander, con `bash -ic` para que cargue `~/.bashrc`):

```bash
bash -ic 'python3 unidades/ficha_doc.py puente1 deepseek ficha_v0 r1'
```

## Muse Code y agentes delegados

Muse Code (Meta Muse Spark) es el implementador; DeepSeek Harness, el
agente de investigación y verificación; NotebookLM, una herramienta en
evaluación. Cómo se arrancan, se delegan tareas y se recibe el aviso al
terminar, con sus reglas (autorización previa de Frat; exclusivo de Claude
y ChatGPT): `/home/fratquintero/Claude-memoria/memoria/agentes-delegados.md`.

**Qué lee Muse.** Muse carga solo `AGENTS.md` en cada sesión, interactiva o no. Ahí están sus reglas de red, claves, comandos y reportes. `CLAUDE.md` es una sola línea (`@AGENTS.md`): si se usa Claude Code, lee las mismas reglas. Hay una sola fuente.

## Contexto

*Objetivo suspendido (ver Estado actual).*

El piloto EEL detecta estructura con GLM vía prompts JSON (tareas A/B/C)
más post-proceso determinista. Funciona (golds 05/06 exactos), pero cada
corrida total cuesta minutos por el razonamiento del modelo, y la
"confianza" que usábamos era un número sin calibrar (eliminado del
esquema 2026-09-19).

El cookbook `autoformat` de TypeSafe muestra otro paradigma: el modelo
nunca genera texto, solo sopesa juicios angostos y devuelve grados de
soporte, y el código decide y renderiza. Trabajamos directo contra
`api.typesafe.ai` con Jev (`TYPESAFE_API_KEY` por entorno; SDK 0.7.0
instalado como referencia, runtime con urllib + dicts). `classifier.dev`
(mismo modelo, sin clave) quedó archivado como plan B: fue el puente
mientras no había acceso.

Fuentes leídas (verificadas, mandan sobre blogs de terceros):
`https://docs.typesafe.ai/cookbooks/autoformat`, `https://docs.typesafe.ai/api.md`,
páginas de primitivas/State/confianza, skill oficial, `https://classifier.dev`
(+ `/docs`, `/benchmark`), índice en `https://docs.typesafe.ai/llms.txt`.

## Marco conceptual vigente (guía v8.2)

Lo que Jev devuelve lo consume **el sistema, no el usuario**: usado
correctamente, Jev es transparente para el usuario (el operador y el
auditor sí ven grados, versiones y crudos). Guía §1.

Pensamos Jev como un **juez**: el `state` es el **expediente** (el
material que se somete a juicio, con un papel reconocible) y el
resultado es un **grado de soporte** o su reparto. Jev no responde
preguntas, no extrae datos y no dice verdadero o falso. Sopesa juicios
con el expediente y con sus hechos notorios. **Dónde va lo que Jev
juzga**: en la Noul, un solo juicio en `instructions`; en Choice y
Score, varios juicios alternativos en `criteria` (sin orden / como
niveles), entre los que Jev reparte su soporte. En Choice y Score,
`instructions` agrupa esos juicios y puede ir vacío (prueba 6). El
juicio se sopesa solo con lo notorio (expediente vacío) o con un
estado de cosas más lo notorio. El grado de una Noul se lee por bandas; la franja central
(0,30–0,65) es una señal de diseño. Jev es **consistente** (un juicio
fijado da casi el mismo grado en cada réplica) pero **sensible** (una
palabra del juicio o del marco del expediente puede mover el grado), y
es una caja negra: no se buscan mecanismos. Las bandas y los umbrales
son heurísticos, y el diseño de los juicios sigue líneas generales que
se afinan en cada caso de uso, con casos de referencia y réplicas.
Detalle en `jev_typesafe_guia_pedagogica_v2.md` §1, §3.1 y §4.6, y en
`diccionario.md`.
Los nombres de campo del protocolo no cambian (regla 3).

Las secciones fechadas más abajo (evidencia, plan, cierres) son
registro histórico y conservan el vocabulario de su momento
(«pregunta», «respuesta»).

## Lo que trae classifier.dev (plan B archivado; era el puente sin clave)

- Zero-shot por HTTP: texto + etiquetas → label, confianza 0–1 y scores
  por etiqueta. Sin key. Batch de hasta 1.000 inputs por request (~1 s
  por millar). Límite de input 32.000 caracteres.
- **Dimensiones**: hasta 20 decisiones independientes por input en un
  request, cada una con sus `instructions` (= los criterios del cookbook).
- **Tiers** (`fast`/`smart`): existen solo ahí, no en el API crudo;
  `smart` es su orquestación (re-pregunta < 0,7 a un razonador). Si
  queremos revisión, el escalado es nuestro.
- Confianza calibrada medida (≥0,9 acierta 82–92% según set). **No** es
  detección de fuera-de-distribución: sin etiqueta que capture el "no",
  todo cae en la mejor etiqueta igual → hay que poner el negativo
  explícito (`contenido`, `continuacion`, `ninguna`).
- Multi-label, MCP, CLI y skill disponibles.
- Privacidad: el texto no se almacena ni se loguea (igual usaremos solo
  documentos sintéticos).
- No genera texto: sirve para detección (A/B), **no para títulos (C)**.

## Principios y reglas acordadas (sesión 2026-09-19)

Fuente y vocabulario:

1. La fuente que vale es `docs.typesafe.ai/api.md` + los tipos del SDK
   instalado (verificados entre sí; los modelos del SDK se generan desde
   el openapi oficial). Blogs y terceros no valen para nombres de campos
   (`options`/`levels`/`state_format` no existen).
2. Vocabulario en tres grupos: campos del protocolo (`model`, `state`,
   `questions`, `type`, `instructions`, `criteria`, `answers`, `usage`);
   tipos del SDK (`TypeSafeClient`, `Noul`, `Choice`, `Score`); e IDs
   nuestros (`explica`, `es_rotulo_3`).
3. Al cable, solo campos del protocolo: si no está en `api.md`, no se
   envía. Regla mnemotécnica: si se puede renombrar sin cambiar el
   resultado, es nuestro; si rompe el request, es del protocolo.

Request/response y anclaje:

4. Los IDs de los juicios viajan pero el modelo no los usa (doc
   literal; confirmado en la prueba 7: con la clave `q1`, `libro_senalaba`
   o `falso`, el mismo juicio dio 0,85–0,87); sirven para casar cada
   resultado en código. Aun así, claves neutras (`q1`, `q2`…).
5. Sobre interno vs cable: en código/crudos vive el sobre completo
   (payload + metadata: `usuario`, hashes, latencia, tokens, modelo
   efectivo); al cable se serializa solo `model`/`state`/`questions`.
6. Sin SDK en runtime: urllib + dicts planos (patrón `llm.py` del
   piloto); el SDK queda como referencia de tipos.
7. Invariante de entrada original también con Jev: el modelo ve el
   verbatim; el anclaje se resuelve en código.
8. Expediente con nombres que digan qué es cada cosa (`texto_a_evaluar`,
   no `bloque`); el juicio nombra el material cuando es sobre él. Con un
   solo campo la forma natural da igual (prueba 3a); con varios, el
   nombre del campo entre backticks, nunca "this block" a secas.

Juicios:

9. Se elige primitiva por dónde van los juicios: uno solo, en
   `instructions` → Noul; varios alternativos sin orden, en `criteria`
   → Choice; varios como niveles ordenados, en `criteria` → Score. El juicio dice qué se juzga (qué dice el
   material o si lo que dice es correcto); la primitiva solo da la
   forma del resultado (prueba 2).
10. Toda Choice lleva su opción de salida explícita (puede que ningún
    juicio se sostenga; la confianza no lo detecta), y cada opción se
    redacta como un juicio.
11. Umbrales calibrados con datos propios (gold/sembrado), nunca los del
    cookbook ni 0,5 a ciegas.
12. El grado de una Noul se lee por bandas (guía §3.1): > 0,85 muy
    seguramente cierto · 0,75–0,85 seguramente · 0,65–0,75 hay bases ·
    0,30–0,65 el juicio no se puede formar con este expediente · 0,20–0,30
    la base no es firme · < 0,20 muy seguramente falso. La franja central
    es una señal de diseño (juicio mal formulado o desconectado), no una
    duda de Jev. Un grado bajo no distingue contradicción de silencio. No
    hay confianza separada en Noul.
13. A Jev, juicios; al código, cómputo: contar letras, offsets y
    aritmética los hace `comun.py`, nunca un juicio (medido: en el
    borde 9/11 letras el grado cae en la franja central, ~0,5: mal
    diseño).
14. La redacción del juicio y el idioma se testean con datos (gold +
    pares ES/EN), no se opinan: lo claro sale igual en ambos (0,99/0,99);
    las diferencias aparecen en el borde. Cada palabra forma parte del
    juicio: «afirma», «dice» y «según» son juicios distintos (prueba 3).
    El juicio se escribe directamente, sin «es verdadero que»; de modo
    que el grado alto sea lo que se busca; sin dobles negaciones ni
    indirección; diciendo exactamente lo que se quiere (alcance y
    negaciones se leen al pie de la letra); y sin contradecir sus
    juicios de `criteria` (TypeSafe, límites de lectura literal, indirección e
    instrucciones y criterios contradictorios; guía §6, actualizada
    el 2026-09-23 a los once límites oficiales). Vale igual
    para cada juicio de `criteria`. Las negaciones en el
    material se leen bien (prueba 1).

Método del spike:

15. El spike no concluye (mala práctica): junta evidencia, informa con
    números; decide la auditoría con Frat.
16. Esta API no tiene `temperature`: la estabilidad se mide re-corriendo
    (los números respiran entre llamadas: 0,87–0,95 lo mismo en las
    primeras corridas; en las pruebas de reglas, con juicios fijados,
    ±0,01–0,02).
17. No hay tiers en el API crudo (`fast`/`smart` son orquestación de
    classifier.dev); si hace falta revisión, el escalado lo construimos
    (Jev + GLM = `confidence-routing`).
18. Inglés rinde algo más por diseño (oficial); calibrar en español con
    datos propios.
19. State solo texto, sin adjuntos (ni imágenes/audio); docs de 1–4 KB
    sobrados; si algo no entra, se parte en código.
20. Solo documentos sintéticos (aunque el texto no se almacena).
21. La confianza (Choice/Score) y la franja central (Noul) se usan para
    enrutar a revisión/escalado/fallback (reemplazan al número inventado
    que eliminamos del esquema). Ambas son señales de diseño. TypeSafe
    describe sus modelos como calibrados a nivel de grupo, pero el 0,7
    es solo un valor de partida: los umbrales se fijan por acción,
    dominio, primitiva e idioma, con datos propios y lejos de grupos de
    casos reales (en la batería de urgencia, h3 dio 0,71/0,69/0,72 y
    cruzaba el 0,7 entre réplicas). Bandas y umbrales son heurísticos,
    no valores calibrados. En una Choice se lee `probabilities`, no solo
    `choice`: lo notorio y el marco del expediente pueden quitar soporte
    al juicio que el expediente sostiene sin cambiar la elección (prueba
    7: Gagarin 0,80–0,87 frente a Jesús 0,99, mismo marco). Ver guía §4.6
    y §5.
22. Reportar antes de inventar; prompts y campos, tal cual.
23. Una Choice (juicios alternativos en `criteria`) y N Nouls (un
    juicio cada una) son dos estructuras de decisión con distinto costo y auditabilidad; la elección se justifica
    por caso y se mide, no se prefiere por defecto.
24. Las tablas viajan como state estructurado (array de objetos, no
    prosa); cada celda/fila se juzga por separado con juicios que
    apuntan a su campo.
25. El batch no cambia el resultado (observación importante): cada
    juicio se sopesa en paralelo y aislado frente al mismo expediente
    (patrón oficial `speculative fan-out`); mandar N juntos o uno por
    uno da el mismo grado (medido: `titulo` 1.00 sola y en grupo de
    11). Solo cambia la operación: 1 llamada en ~1 s vs N llamadas.
    Los números respiran entre corridas (regla 16), pero no el lado ni
    el orden de magnitud.
26. El diseño de los juicios sigue líneas generales, pero se afina en
    cada caso de uso, con casos de referencia y réplicas, si se quieren
    buenos rendimientos y consistencia. Jev es una caja negra: no se
    buscan mecanismos para explicar grados concretos (una explicación
    que sirva para Gagarin puede no servir para Einstein); se retienen
    márgenes como heurísticos (guía §4.6, prueba 7).

**Antecedentes revisados para retomar EEL (2026-10-02).**

- **Nombre de la tarea en la literatura:** reconstrucción jerárquica de la
  estructura del documento. Banco de prueba: HRDoc (AAAI 2023,
  [arXiv 2303.13839](https://arxiv.org/abs/2303.13839)). Método reciente:
  *Detect-Order-Construct* ([arXiv 2401.11874](https://arxiv.org/abs/2401.11874)):
  detectar qué es título, ordenar los bloques, construir el árbol. Es el mismo
  reparto de EEL: A decide localmente «¿es rótulo?», orden y marcador dan el
  contexto, la pila (código) construye la jerarquía.
- **Por qué es difícil:** el nivel de un título es relacional (depende del uso
  del formato en todo el documento), no una propiedad de la línea. Una línea
  es una marca; «ninguna marca determina por sí sola» (ensayo, l. 117).
- **Para qué serviría:** [PageIndex](https://github.com/VectifyAI/PageIndex)
  (VectifyAI, MIT) consulta documentos largos recorriendo su árbol con un LLM
  en vez de buscar trozos por similitud, pero el árbol lo saca del diseño del
  PDF. EEL lo reconstruiría cuando el documento no trae estructura limpia.
  Camino posible para documentos largos en Zettel: EEL (árbol) → PageIndex
  (consulta) → fichas dentro de cada nodo, una por foco (caso de estudio),
  como en la arquitectura candidata. Un nodo es un tramo del documento y
  puede contener varios focos.

## Arquitectura que veo (propuesta, a acordar)

*Suspendida junto con el objetivo EEL.*

Principio: Jev sopesa, el código decide. Nada de lo determinista cambia
(bloques, offsets, pila, vistas, contrato EEL).

- A por bloque: Choice [rotulo, contenido] (+scores); nivel por pila
  desde orden + marcador verificado, o dimensión extra [nivel_1,
  nivel_2] a probar.
- B por párrafo: Choice [frontera, continuacion]; umbral calibrado desde
  el gold (estilo cookbook 0.2/0.5), no 0.5 a ciegas.
- Confidence-routing: confianza baja o franja central → revisión humana
  o fallback al GLM actual (umbral a calibrar, regla 21) (escalado propio; no hay tier smart en el API crudo).
- C (títulos): queda fuera — sigue GLM o extractivo.

A decidir con DeepSeek:

1. Etiquetas de A: ¿[rotulo, contenido] o [rotulo_n1, rotulo_n2,
   contenido]? ¿Nivel por pila o por dimensión?
2. B: ¿Choice binaria con umbral desde datos, o Score?
3. Criterio de adopción: igualar gold 05/06 + txt-02 y acercarse al
   sembrado, a < 1/10 del costo/latencia GLM.
4. Estabilidad: re-correr cada batch 2–3 veces y medir acuerdo.
5. Qué pasa con títulos C si A/B migran.

## Plan de pruebas

*Fase 0 hecha; fases 1–3 pendientes, suspendidas junto con el objetivo EEL.*

- Fase 0 — probe gratis: 1 bloque de `txt-02` (`rotulo` vs
  `contenido`) + 1 párrafo de `txt-01`.
  - **Hecha 2026-09-19**: SDK `typesafe-sdk` 0.7.0 instalado; clave en
    `~/.bashrc` (los shells no interactivos no lo cargan solo: evaluar
    la línea `export` o `source` explícito). Noul "¿es rótulo?" sobre
    `ANTECEDENTES` → **0.95 en 0.7 s**. Jev responde.
- Fase 1 — barrido A: todos los bloques de 02/05/06, 1 request por doc.
  Métrica: detección vs gold y vs GLM.
- Fase 2 — barrido B: párrafos de txt-01, umbral desde el sembrado.
  Métrica: aciertos/espurias vs B-GLM y vs TextTiling.
- Fase 3 — dimensions + escalado propio: tipo+nivel en una llamada;
  re-consulta a GLM donde el resultado caiga en la franja central o la
  confianza sea baja. Métrica: costo/latencia/
  calidad con y sin escalado.
- Informe: tabla comparativa y recomendación (adoptar / híbrido /
  descartar). Cada fase deja notas acá, no solo código.

## Evidencia reunida (sesión 2026-09-19, sin veredicto: decide auditoría)

*Registro histórico, con el vocabulario de su momento. Lecturas
actualizadas en la guía (§3.1 bandas, §4.6, Anexos A–C).*

- Rótulos sueltos: `ANTECEDENTES` 0.91–0.95, `CONSIDERACIONES` 0.9–0.93,
  `BACKGROUND` 0.94, `CONCLUSIONS` 0.87–0.92; contenido/gibberish ≤ 0.12.
  `DECIDE` pelado: 0.36 (ambiguo sin contexto → el state lleva vecinas).
- Lengua: pares ES/EN casi idénticos en lo claro (0.92/0.87, 0.99/0.99);
  diferencias solo en el borde.
- Conteo de letras: frase de 30 → 0.99; borde 9/10/11 (ES) → 0.53/0.09/
  0.47; mismo borde (EN) → 0.04/0.13/0.72. Rango 2–13, 20 palabras:
  20/20 del lado correcto, incerteza en 6/7/8.
- Palabras inventadas (`florp`, `snorfle`, …): gradúan como las reales
  (7/8); `snorfle` dio 0.74 una vez y 0.21 al repetir: ruido, no
  propiedad.
- Latencias: 0.7–2.5 s por llamada chica; `usage` con `model` efectivo
  (`jev-1.13.0`) y tokens in/out.
- Biología 179 palabras, 5 Noul en 1 request (1.6 s): 0.98/0.96/0.01/
  0.98/0.04, todo correcto (ballenería no se confunde con pesca).
- Tiempos: mismo request ×3 → 1.5/0.6/1.1 s con nouls idénticos;
  10 preguntas → 0.5–4.2 s (mismo rango que 5: duplicar no mueve el
  tiempo, confirma paralelismo).
- Física 451 palabras, 50 Noul en 1 request: **0.7 s, 50/50** correctos
  (2.616 in / 904 out). Único tibio: q42 (`Alain Aspect` por nombre,
  0.56) → candidato a umbral de revisión.
- Presupuesto: sin límite fijo de preguntas, solo tokens (~32 k
  compartidos estado+preguntas); 62 del cookbook y 50 nuestras entran
  sobradas. Lo relacional sigue en código (las respuestas no se ven).
- Selección de span: Jev no devuelve dónde miró; patrón verificado:
  código parte en oraciones, Choice elige (`s1`, confianza 1.0).
- Crudo vs SDK saldados: `criteria` (no `options`/`levels`), legend de
  Score base 0 con claves string, endpoint `POST …/v1/systemone`,
  `model: jev-latest`.
- Modalidad oracional (Zettel): 50 sentencias sintéticas × 7 clases en
  1 request (~2 s, 10.5 k/4.1 k) → **50/50**. Única fuga: q31
  desiderativa 0.76 / imperativa 0.20, ambigüedad real del subjuntivo
  exhortativo, no ruido.
- Tabla como array (30 filas × nombre/edad/sexo), 90 Choice por celda →
  **90/90** frase-nominal en 1.4 s. Gradiente por pobreza de señal:
  nombres 1.00, sexo ~0.92, edad 0.60–0.78 con fuga a enunciativa
  (0.19–0.34).
- Wording medido (regla 14 en acción): exigir predicado con valor de
  verdad en enunciativa + listar números/códigos/letras en
  frase-nominal → edad sube a 0.97–0.98 (fuga ≤ 0.03).
- Criterio conceptual de modalidad: ¿tiene valor de verdad? Fórmulas
  (igualdades) = enunciativas; números, medidas (`5 minutos`) y
  etiquetas = nominales.
- Crudos: `cache/modalidad-50.json`, `cache/tabla-30.json`;
  scripts: `probes/modalidad_50.py`, `probes/tabla_30.py`.

## Noul, Choice y Score, en palabras (actualizado con la guía v6)

- **Noul** sopesa **un solo juicio**, en `instructions` («`ticket` pide un reembolso»)
  → un grado de soporte entre 0 y 1, que se lee por bandas. No reparte
  entre sí y no: gradúa un solo juicio.
- **Choice**: los juicios van en `criteria`, **sin orden** («`ticket`
  reclama por un cobro», «`ticket` reclama por un envío», «otra cosa»)
  → Jev reparte su soporte entre ellos; `choice` es el de más soporte,
  no una decisión de Jev. Con opción de salida.
- **Score**: los juicios van en `criteria` como **niveles ordenados**
  que uno define («`mensaje` no expresa plazo», «`mensaje` lo necesita
  hoy») → Jev reparte su soporte entre los niveles; el `score` es la posición media. Si el soporte se reparte
  entre vecinos, el número cae en el medio (1.6); si se concentra, cae
  justo en un nivel. Medido: urgencia de un mensaje ("server down, help
  now") sobre [espera / esta semana / hoy] → `score` 2.0, confianza 1.0.
- La diferencia clave: la Noul sopesa un juicio aislado; Choice y Score
  reparten soporte entre los juicios de `criteria`, y el Score además
  los ordena.

## Las siete modalidades de sentencia (memoria 2026-09-20)

| Modalidad | Definición (criteria vigente) | Ejemplo |
|---|---|---|
| Enunciativa | Afirmación o negación completa, con predicado: puede ser verdadera o falsa | `La fotosíntesis ocurre en los cloroplastos.` |
| Interrogativa | Formula una pregunta | `¿Qué pigmento capta la luz?` |
| Exclamativa | Expresa emoción o énfasis con exclamación | `¡Qué red tan compleja forman los hongos!` |
| Imperativa | Orden, instrucción o ruego directo | `Añade el reactivo gota a gota.` |
| Desiderativa | Expresa un deseo | `Ojalá la muestra no se contamine.` |
| Dubitativa | Expresa duda o posibilidad | `Quizá el resultado se deba al pH.` |
| Frase nominal | Solo nombra, sin afirmar: etiquetas, nombres propios, números o códigos aislados, cantidades con unidad (`5 minutos`), letras sueltas; sin predicado | `Hechos relevantes.` |

Criterio que ordena: **¿tiene valor de verdad?** Las fórmulas
matemáticas (igualdades como `12! = 479001600`) son enunciativas:
predican algo verificable.

**Prueba hecha**: 50 sentencias sintéticas balanceadas (8
enunciativas + 7 por cada una de las otras seis), etiquetas conocidas
de antemano, un solo request con 50 Choice de 7 clases
(`probes/modalidad_50.py`, crudo en
`cache/modalidad-50.json`).

**Resultados**: **50/50 en ~2 s** (10.5 k in / 4.1 k out). 43
unánimes (1.00); la única fuga relevante fue q31 (`Que el jurado
delibere con serenidad y justicia` → desiderativa 0.76 / imperativa
0.20), ambigüedad genuina del subjuntivo exhortativo, no ruido. Las
marcas formales (¿?, ¡!, modo verbal, adverbios, ausencia de verbo)
separan casi perfecto, en español.

## Convenciones del spike
- Todo duerme en esta carpeta; README antes de código (política del repo).
- Resultados cacheados en disco (estilo `json_cache` del cookbook): un
  re-run no re-paga ni re-llama.
- Ninguna clave en archivos (`TYPESAFE_API_KEY` solo por entorno).
- Rama `main`; el piloto no se toca. Si resulta, se integra por
  decisión de Frat.
- Header `User-Agent: spike-jev/1.0` en cada llamada (Cloudflare bloquea
  el de urllib).
- Pruebas de reglas (2026-09-22/23): scripts en `probes/`
  (`noul_fuerza.py`, `score_prueba1.py`, `objeto_juicio.py`,
  `nombrar_material.py`, `material_falso.py`, `repite_c4.py`,
  `caso_similar.py`, `diag_scott.py`, `diag_2mas2.py`,
  `instructions_vacio.py`, `decimos_gagarin.py`, `libro_gagarin.py`,
  `libro_frat.py`, `libro_frat_isla.py`, `libro_frat_isla_sin.py`,
  `libro_jesus.py`, `claves_jesus.py`, `choice_jesus.py`,
  `choice_jesus_b.py`, `choice_gagarin.py`, `choice_gagarin_no.py`,
  `choice_gagarin_libro.py`); lectura y
  conclusiones en la guía, Anexos A–C.
