# Memoria de trabajo y pendientes (spike-jev / Zettel)

Estado al 01-10-2026. **Solo lo vigente:** lo que estamos haciendo y nos guía. Lo superado (enfoque de `datos_pABQ*`, rondas DU/P/ENC/U, sus decisiones y pendientes) está en `historico/memoria-hasta-2026-10-01.md`; el detalle de cada ronda, en `unidades/PLAN.md` y `git log`.

## Dónde quedamos (leer primero)

- **Qué hacemos:** reconstruir con un LLM barato (DeepSeek `deepseek-flash`) todo lo que un texto establece, organizado desde el caso de estudio, en una **ficha** JSON (`unidades/ficha_doc.py`, prompt vigente `unidades/prompts/ficha_v1.md`). El extractor no decide qué es dato: la pertinencia se decide después (Jev o la pregunta). Es la capa de datos del grafo de **Zettel**. Marco: ensayo de Frat «¿Qué es un dato?», versión del 30-09 (§2).
- **Estado:** el núcleo conceptual quedó probado en textos cortos. En la reserva por géneros (F5: divulgación, ensayo, opinión; ~220 palabras; textos y preguntas de ChatGPT) con `ficha_v1` congelada: **fidelidad ≈ 95 %** (60/63 preguntas, tres réplicas) y formato estable. **No es ágil:** 76–127 s y 15–25 mil tokens de razonamiento por texto. Detalle en §3.
- **Decisión abierta (siguiente):** cómo lograr agilidad sin perder fidelidad. Es de **arquitectura o de modelo** (partir el documento, menos registros por llamada, otro modelo o nivel de razonamiento), no de seguir retocando el prompt. Hasta decidirlo, `ficha_v1` queda congelada.
- **Arquitectura candidata (no decidida):** oraciones (código) → subtemas (LLM, `unidades_v5`, ya existe) → inventario de casos de estudio por documento (LLM) → ficha por foco (LLM) → verificación literal (código) → Jev (identidad, correferencias, omisiones mirando el texto).

## 0. Dónde y cómo

- **Carpeta:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/` (máquina local de Frat, Linux). Trabajo activo en `unidades/` (script `ficha_doc.py`, prompts en `prompts/`, textos en `docs/`, preguntas en `gold/`, crudos en `cache/`).
- **Repositorio:** `https://github.com/frquintero/jev-typesafe-spike`, rama `main`.
- **Roles:** Frat y Cowork (Claude) planean. La implementación y las corridas las hacen los ejecutores: Muse Code (Meta Muse Spark) en local, GPT-6 Luna (OpenAI, vía Codex o ChatGPT) y Claude Code en la nube como alternativa. El rol va con la tarea, no con el modelo.

**Flujo de una ronda.**
1. Frat y Cowork discuten y conjeturan. Se corre solo si hay una conjetura nueva.
2. Cowork escribe el prompt en `unidades/prompts/` y la sección de la ronda en `unidades/PLAN.md` (o en `prototipos/PLAN.md`) (cambio, conjetura, comandos, reporte), y hace commit y push.
3. Cowork deja el mensaje para el ejecutor en `unidades/mensaje_<RONDA>.txt` (commit incluido): Frat lo pega en su sesión, o Cowork lo lanza sin terminal con `./muse.sh exec --prompt-file <archivo>`.
4. El ejecutor (Muse, Luna o Claude Code) corre sin modificar nada, reporta sin veredicto y hace commit y push de los crudos.
5. Cowork lee los crudos (`unidades/cache/`) y los evalúa contra la conjetura. Frat decide.

**Aviso de fin de ronda (decisión de Frat):** cuando Cowork lanza a Muse (`nohup bash -ic './muse.sh exec --prompt-file …' &` por Desktop Commander), arma un Monitor que consulta `git ls-remote` del repo en GitHub cada 30 s y avisa cuando aparece el commit nuevo; entonces Cowork le manda a Frat una notificación de escritorio (PushNotification) con el resultado en una línea.

**Configuración** (detalle en el README, «Correr las pruebas con Muse Code»):
- `muse.sh` (alias `muse` en `~/.bashrc`) levanta el proxy de claves si no corre, arranca Muse sin sandbox en la carpeta actual y apaga el proxy al salir si lo arrancó él.
- Las reglas del ejecutor viven solo en `AGENTS.md`. Muse y Codex (donde corre Luna) lo cargan solos; en el chat de ChatGPT, Luna lo lee porque cada mensaje empieza con «Lee AGENTS.md». `CLAUDE.md` es una línea que apunta ahí (`@AGENTS.md`).
- Claves: `proxy_local.py` las inyecta por host (TypeSafe, Z.ai, DeepSeek, xAI); nunca van en archivos del repo.
- Cowork hace git con Desktop Commander, no con el shell aislado (no ve credenciales y deja bloqueos en `.git/`). Para detener procesos, la herramienta `kill_process` de Desktop Commander (`kill` desde la terminal está bloqueado).
- Muse se colgó una vez (F3: siete minutos sin lanzar comandos). Si pasa, se detiene con `kill_process` y los comandos de `PLAN.md` se corren tal cual, sin modificar nada (exportando `HTTPS_PROXY` y `SSL_CERT_FILE`).

## 1. Reglas de trabajo

- **Ockham:** empezar con lo que funciona. Cada elemento del prompt tiene que servir a la tarea; quitar lo que no se use.
- **Una cosa por ronda.** Varios cambios solo si aplican un mismo principio.
- **Planificar** es pensar y conjeturar; no se ofrecen corridas por reflejo.
- **No reinventar la rueda:** revisar la literatura antes de diseñar.
- **Mostrar el prompt antes de correr** y esperar el «adelante».
- **Sin ejemplos tomados de los documentos de prueba** (invalidan la prueba).
- No se editan README, diccionario ni guía sin aprobación.
- **Crítica constructiva:** valorar la propuesta de Frat y mejorarla con razones, sin aceptar todo.
- **Generalizar, no particularizar (directriz de Frat, 01-10):** todo cambio al prompt se piensa para documentos de contenido general (divulgación, ensayo no especializado, opinión), no para resolver los textos de prueba. No se afina sobre textos de desarrollo; lo que mide es una reserva escrita por otro, con preguntas fijadas antes.

## 2. Marco y decisiones (vigentes desde el 01-10)

Vocabulario del ensayo y decisiones cerradas. Donde algo del histórico las contradiga, mandan estas.

### 2.1 Vocabulario del ensayo

- **Caso** (filosófico): lo que acaece. **Caso de estudio:** unidad individuada y reidentificada acerca de la cual se reúnen determinaciones (l. 87–97). No confundirlos.
- **Aspecto:** aquello bajo lo cual se considera el caso de estudio. **Variable** solo hay cuando una serie comparable muestra variación (l. 129); un texto aislado da aspectos.
- **Marca:** configuración individuada, simple o compuesta, interpretable bajo reglas; una cláusula también es marca. **Marca de posición:** la que, leída con escala, calendario o categorías, señala una posición entre otras («1972», «unos 40 millones de m³», «la mitad», «diciembre»). Una marca puede cumplir varias funciones (expresar posición, identificar, remitir). Ninguna marca determina por sí sola (l. 117).
- **Marca ≠ posición ≠ valor.** El valor es la determinación completa (caso de estudio + aspecto + condiciones + posición), no el número.
- **Condiciones:** constitutivas (si cambian, cambia la pregunta), de representación, de procedencia (cambia la ruta).
- **Dato:** valor que queda (determinación registrada de modo recuperable). **Información:** cambio en las respuestas admisibles a una pregunta.
- Documento y foco **no son conceptos del ensayo**: son arquitectura de Zettel compatible con él.

### 2.2 Decisiones (cerradas el 01-10)

| Tema | Decisión |
|---|---|
| Qué se reconstruye | Todo lo que el texto establece; la pertinencia, después |
| Genéricos, constantes, valoraciones | Producen determinaciones (l. 91, 129, 215) |
| Organización | Desde el caso de estudio |
| Caso de estudio o condición | Por **qué cambia si se modifica**, no por cuántas veces aparece |
| Campo `valor` | Guarda la posición; la ficha completa es el valor |
| Marca de posición | Solo donde hay escala, calendario o categorías; no se recorta a la fuerza |
| Respaldo | Toda determinación lleva los fragmentos que sostienen sus componentes (pueden ser varias oraciones) |
| Aspecto | Con respaldo textual; no se inventa para alojar algo («pesaba» respalda «peso») |
| Capas (creer, recomendar, decir, suponer, citar) | Dos niveles: lo que el texto establece (que alguien cree/recomienda, como hecho) y el contenido, con su modalidad y quién lo sostiene (puede ser el propio autor) |
| Recomendación | Capa cuyo contenido es una acción; no se le inventa una propiedad al objeto |
| Comparación | Puede nombrar un caso de estudio; lo comparado no se vuelve ese caso («otra sequía igual» ≠ la sequía de 2024) |
| Cambios | Se conservan («bajó a la mitad» ≠ «está a la mitad») |
| Lo dicho al pasar | Aposiciones y ubicaciones también se registran («el técnico», «en su anexo 4») |
| `modo` | Se parte en tres: cómo se presenta el contenido, quién lo sostiene, cuánto reconstruyó el extractor |
| Dudas | Se registran, no se resuelven («almacena»: ¿volumen o capacidad?; «la mitad»: ¿de qué?) |
| Código | Solo numera y verifica que los respaldos estén literales. Se descartó la lista de control de números: explicar las marcas es trabajo del LLM |
| Evaluación | Qué recupera y qué agrega o deforma, más preguntas escritas antes de correr (que el texto responde, que deja abiertas, en conflicto); «el documento no lo establece» es respuesta explícita |

### 2.3 Textos de desarrollo (inventados en la sesión; solo desarrollo, no medición)

- **Estanque:** «(1) En la superficie, el agua del estanque norte de la finca El Roble está a 18 °C. (2) Además tiene un color verdoso, algo preocupante según la bióloga Ana Ruiz.»
- **Puente:** «(1) El puente colgante de San Rafael mide 120 metros de largo y fue inaugurado en 1958. (2) En invierno, sus cables se contraen hasta 4 centímetros. (3) Según el ingeniero Luis Mora, ese movimiento es normal en puentes de acero.»
- **Represa:** «(1) La represa El Cóndor, construida en 1972, almacena unos 40 millones de metros cúbicos de agua. (2) Durante la sequía de 2024, su nivel bajó a la mitad. (3) El técnico Pablo Ríos cree que la compuerta 2 no resistiría otra sequía igual. (4) El informe municipal, en su anexo 4, recomienda revisarla antes de diciembre.»

### 2.4 Errores cometidos al leer esos textos (Cowork y ChatGPT)

Casi todos son de **identidad**: la ficha agrega o pierde algo.

1. Meter una condición en el caso de estudio («agua *en la superficie*» arrastró la superficie al color).
2. Decidir caso o condición por frecuencia (la altura vale para tres determinaciones y sigue siendo condición).
3. Inventar un aspecto («plazo de revisión» de la compuerta; «nivel de preocupación»).
4. Recortar marcas a la fuerza («antes de diciembre», «no resistiría»).
5. Exigir que todo número sea valor («camión 7», «anexo 4»).
6. Confundir mencionar con reidentificar («otra sequía igual»).
7. Mezclar los dos niveles de una creencia.
8. Perder un cambio («bajó a»).
9. Perder lo dicho al pasar («el técnico», «anexo 4»).
10. Una sola etiqueta (`modo`) para tres preguntas.
11. Sobrevender el código (lista de control de números).

Dos lectores atentos discreparon sobre todo al individuar el caso de estudio, como los anotadores de MeasEval (acuerdo 0,55): ahí se espera que falle el modelo.

### 2.5 Antecedentes revisados

- **MeasEval** (SemEval-2021, tarea 8): cantidad, unidad, entidad medida, propiedad medida y calificador, todos anclados en el texto; relaciones opcionales. Acuerdo humano: cantidad 0,94; propiedad 0,64; entidad 0,55; calificador 0,33. Solo mediciones.
- **GraphRAG** (Microsoft, 2024): entidades, relaciones y *claims* extraídos por LLM; trozos chicos recuperan casi el doble; *gleaning* para omisiones. Fusiona entidades por nombre exacto y resume en prosa: dos cosas a evitar.
- **Wikidata:** §2.6.

### 2.6 Referencia: el modelo de statements de Wikidata (30-09)

No es diseño de Zettel (falta mucho para eso). Es literatura para no inventar la rueda, a la mano para cuando toque. Cifras de propiedades escritas de memoria: verificarlas antes de usarlas.

**Las piezas.** Un *statement* = afirmación principal (ítem + propiedad + valor) + **calificadores** (pares propiedad–valor que precisan qué se afirma: fecha P585, «se aplica a la parte» P518, «criterio usado» P1013) + **referencias** (de dónde sale: «publicado en» P248, URL P854, fecha de consulta P813, cita textual P1683) + **rango** (*preferred*, *normal*, *deprecated*, con «motivo del rango obsoleto» P2241). Cada statement tiene GUID: viene reificado.

**Correspondencia con el ensayo.**
- Caso de estudio → ítem. Fusión de ítems y «diferente de» (P1889) = reindividuación a mano.
- Aspecto → propiedad (con tipo de dato fijo). Dominio → restricciones de la propiedad. Escala → unidad, límites y precisión de cantidades y fechas (condiciones de representación).
- Condiciones constitutivas → calificadores (quitarlos cambia la pregunta). Procedencia → referencias (quitarlas deja el dato igual, sin sostén).
- Estatuto → rango; lo *deprecated* no se borra (sigue recuperable, como en el ensayo).
- Pregunta abierta → *somevalue* (existe, se ignora cuál) frente a *novalue* (establecido que no hay).

**Coincidencias de fondo.** (1) «Verificabilidad, no verdad»: fuentes rivales conviven como statements distintos; Wikidata se parece más a la capa Claim («la fuente dice») que a Datum (el caso del sensor del ensayo). (2) Mismo valor y calificadores con dos fuentes = un statement con dos referencias = «un dato sostenido dos veces». (3) Doble vista en RDF: plana `wdt:` (solo el mejor rango, casi `aguaA.temperatura = 35`) y completa reificada (`p:/ps:/pq:/pr:`, con `prov:wasDerivedFrom` de PROV-O).

**Donde el ensayo afina.** Los calificadores mezclan constitutivo y procedencia (P459 «método de determinación» es a veces una y a veces otra; el criterio del ensayo —qué cambia si se modifica— decide). Sin núcleo común: dos referencias pesan igual aunque una copie a la otra. Sin pregunta ni información. Marca débil (la cita es opcional y no se ancla a versión ni posición). Error y falsedad juntos en *deprecated*.

**Tomable tal cual, cuando llegue el momento:** estructura del statement; no borrar lo desaprobado; *somevalue* frente a *novalue*; propiedad tipada con dominio y unidades; doble vista plana y reificada.

## 3. La ficha: qué sabemos

**Prompt `ficha_v1`.** Tarea, definiciones, 11 principios, contrato de representación (función y campos fijos de las siete listas: casos, relaciones, capas, determinaciones, acciones, marcas, dudas; identificadores en el nombre del caso; referencias como ids) y un ejemplo (el estanque). El principio 5 resuelve referencias implícitas con un solo antecedente («otro», «igual», «el mismo»), marcadas `inferido`; lo comparado y el término de comparación son casos distintos unidos por una relación; varios antecedentes → dudas. El código solo numera y verifica que respaldos, menciones y marcas estén literales.

**Textos.** Desarrollo (escritos por Cowork; no miden): `puente1`, `represa1` (y el estanque, ejemplo del prompt). Reserva (escritos por ChatGPT, preguntas fijadas antes en `unidades/gold/`): `pintura1`, `cafe1` (F2), `jardin1`, `radio1`, `biblioteca1` (F5).

**Lo que funciona** (reserva F2 y F5, tres réplicas): capas (quién sostiene qué, incluido el autor como «yo»); negación y alcance («no prueba que…», «el acta no registra» ≠ «no hubo ventas»); modalidades («puede», «tal vez», «puede que», «no sé si»); referencias implícitas («este último», «el primero», «el documento», «otra sequía igual» → la de 2024); atribución al caso correcto (250 g de la muestra, no del lote); no inventa lo que el texto no establece; formato estable y fragmentos literales.

**Huecos generales del contrato** (vistos en F5; no corregidos porque `ficha_v1` está congelada; se abordan como generalización cuando se descongele):
- Las capas no tienen condiciones: se pierde el tiempo de una creencia o interpretación («durante un tiempo… después»).
- Las acciones no tienen modalidad: lo que se recomienda («debería», «habría que») solo se conserva si el modelo crea una capa; a veces no la crea.
- Exceso de casos (22–34 por texto de ~220 palabras): cantidades, metáforas y pronombres como casos («unos 20 litros», «esponja», «eso»).
- A veces fusiona casos distintos en uno o guarda contenido en el nombre de un caso.
- Los vínculos de razón entre hechos («por esa razón», «porque») no tienen lugar en la ficha (relaciones solo entre casos): son de los niveles 1–2 de Zettel, no de datos.
- El principio 1 usa un ejemplo tomado de la represa («el técnico Pablo Ríos»).

**Costo** (F5, por texto de ~220 palabras): divulgación 103–127 s, 18,5–25 mil tokens de razonamiento; ensayo 96–109 s, 17,6–20,3 mil; opinión 76–102 s, 14,7–20,6 mil. Textos de 3–5 frases: 37–80 s. El costo crece con el texto y con la cantidad de registros; un contrato más explícito estabilizó la forma pero subió el costo (F3).

## 4. Lecciones vigentes

- **Leer el `reasoning_content` antes de proponer cambios:** localiza la causa (DeepSeek lo entrega entero; el de Grok no se puede leer).
- **Una sola corrida no separa el efecto del ruido;** con el mismo prompt el resultado puede variar tanto como el efecto buscado. Réplicas, y comparar prompts con el mismo `rN`.
- **No afinar sobre textos de desarrollo;** medir en una reserva escrita por otro, con preguntas fijadas antes. Un texto escrito por quien diseña el prompt sobreestima el acierto.
- **Un ejemplo enseña exactamente lo que muestra:** una lista vacía no enseña nada; un ejemplo tomado del texto de prueba enseña cautela justo en ese caso. Los ejemplos se eligen desde el marco, no desde las fallas.
- **Si dos señales del prompt se contradicen, el modelo oscila y delibera** (cuesta tokens). Remedio: un solo principio. Referencia implícita con un solo antecedente ≠ ambigüedad.
- **Cada «no va aquí» necesita un «va allá»;** una lista o campo sin forma declarada se inventa distinto en cada réplica; un campo obligatorio no filtra.
- **Un contrato más explícito estabiliza la forma pero no abarata:** abre decisiones nuevas (en qué lista va cada hecho) y el modelo registra más.
- **El género pesa más que el modelo:** un prompt preciso en un género puede no serlo en otro; probar siempre en varios géneros.
- **Al modelo el juicio, al código el cómputo:** numerar oraciones y verificar literalidad lo hace el código.
- **Jev corrige lo que se afirma de más, no lo que se omite:** las omisiones del extractor no se recuperan aguas abajo.
- **Operativo:** DeepSeek solo tiene razonamiento `high` y `max` (nuestro `low` se vuelve `high`); puede dejar el stream colgado (si pasa un minuto sin bytes, relanzar).

## 5. Pendientes vigentes

1. **Agilidad:** decidir arquitectura o modelo con una prueba sobre los mismos textos de reserva (F5) y uno real más largo: partir el documento (subtemas, inventario de casos), menos registros por llamada, otro modelo o nivel de razonamiento. Vara de Frat: ≈90 % correcto y ejecución ágil.
2. **Huecos del contrato (§3):** abordarlos como generalización cuando se descongele el prompt, y medir en reserva nueva.
3. **Vínculos de razón entre afirmaciones** («por esa razón», «porque»): niveles 1–2 del grafo de Zettel; fuera de la ficha de datos.
4. **Jev:** identidad de lo registrado, correferencias, omisiones; después de la arquitectura.
5. Grok sin créditos de xAI: recargar si se quiere compararlo.
