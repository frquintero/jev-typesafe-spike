# Arquitectura del orquestador de Zettel — evaluación

Leí [AGENTS.md](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/AGENTS.md), [zettel-vision-operativa.md](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/zettel-vision-operativa.md), [definiciones-del-marco.md](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/definiciones-del-marco.md), [mvp/pieza1/registro.md](/home/fratquintero/Documentos/Claude/jev-typesafe-spike/mvp/pieza1/registro.md) (más esquema2 y preguntas de la pieza 1) y la guía de Jev §1 y §3.1. Investigué con Exa (búsquedas y lecturas web, sin llamar a APIs de modelos). No leí el archivo del otro revisor. No escribo prompt ni código, y de Jev solo hablo de su lugar en la arquitectura.

Veredicto en una línea: la propuesta de Cowork apunta en la dirección correcta y la literatura 2024-2026 la respalda en lo grueso, pero hay que mover tres cosas de sitio (el corpus necesita búsqueda desde el MVP, no solo listar+leer; juzgar y terminar deben ser etapas del código, no herramientas del LLM; el anti-ciclo necesita un guardia mecánico además de la pregunta introspectiva) y completar ciclo de vida de conectores, persistencia, evaluación y seguridad.

## 1. Qué corroboro (con fuentes)

**Magentic-One y los dos registros: corroborado, con un matiz de fechas.** El paper (Microsoft Research, nov-2024) describe exactamente lo citado: outer loop con registro de tarea (hechos dados, hechos a buscar, hechos a derivar, conjeturas + plan) e inner loop con registro de progreso de cinco preguntas (¿satisfecho?, ¿ciclo?, ¿avance?, ¿quién sigue?, ¿qué instrucción?), contador de estancamiento (umbral 2 en el paper) y replanificación con reseteo de contextos. El patrón "magentic" existe en Agent Framework. Matiz: el framework llegó a 1.0 el 03-04-2026; lo que llegó a 1.0 en julio-2026 (08-07) fue el paquete de orquestaciones. Detalle útil para Zettel: el `StandardMagenticManager` emite el registro de progreso en JSON, con `max_stall_count` (defecto 3), `max_round_count`, `max_reset_count` y reintentos ante JSON malformado; y la documentación advierte que fuera del diseño original de Magentic-One su comportamiento está sin probar. Adoptar la forma (dos registros + replanificación) es sólido; copiar los prompts verbatim, no.

**Anthropic multiagente (jun-2025): corroborado punto por punto.** Patrón orquestador-trabajadores con subagentes en paralelo y un agente de citas separado. Las lecciones citadas existen literales: enseñar a delegar (objetivo, formato de salida, fuentes y herramientas, límites claros — el "research the semiconductor shortage" vago produjo trabajo duplicado), escalar esfuerzo a la pregunta (1 agente con 3-10 llamadas para hechos simples; 2-4 subagentes para comparaciones; 10+ para investigación compleja), y el modo de fallo "buscar sin fin fuentes que no existen" (más el de "50 subagentes para una pregunta simple"). Dos datos para el diseño: Opus 4 orquestando + Sonnet 4 como workers superó al Opus 4 solo en 90,2%; el costo multiagente es ~15x el de un chat (~4x un agente simple). En 2026 Anthropic añadió: multiagente solo compensa ante polución de contexto, paralelismo real o especialización; y el patrón "subagente verificador" (con su modo de fallo típico: declarar éxito tras 1-2 pruebas superficiales).

**Alita / Alita-G: corroborado, con advertencias del propio autor.** Alita (may-2025): predefinición mínima (un web agent) + auto-evolución máxima generando MCPs al vuelo (brainstorming de la brecha, ScriptGeneratingTool, CodeRunningTool en entorno aislado), con caja de MCPs reutilizable; 75,15% pass@1 en GAIA-val. Alita-G (oct-2025): generación dirigida por tareas, abstracción (generalizar parámetros, quitar contexto, estandarizar interfaz, documentar) y selección por recuperación en inferencia; 83,03% pass@1, −15% tokens. Las advertencias importan para Zettel: "MCP Overload" (herramientas solapadas confunden al agente) y sobreajuste si no hay paso de abstracción; la caja se construye tras las corridas, no dentro de cada una. Respalda el pipeline investigador→programador y la reutilización, pero exige un paso de abstracción y un registro versionado, no una pila de conectores crudos por tarea.

**AOrchestra (feb-2026): corroborado.** Subagente como tupla composiciónal (instrucción, contexto, herramientas, modelo), orquestador que nunca actúa en el entorno (solo delega o termina), contexto curado por el orquestador. Su ablación: contexto curado 96% frente a sin-contexto 86% y contexto-completo 84%. Respalda directamente "subagentes con contexto curado" y "modelo por subtarea" (su enrutamiento consciente de costo mejoró precisión y bajó costo 18,5%).

**Uno-Orchestra (may-2026): corroborado.** Una sola política que decide a la vez si descomponer y a qué par (modelo, primitiva) enviar cada subtarea; delegación selectiva (respuesta directa con costo de despacho ~cero para lo simple); 77% macro pass@1, ~16% sobre el mejor baseline con ~10x menos costo. Respalda el principio 1 (no salir al mundo cuando el corpus basta) llevado a mecanismo. Limitación: esa selectividad se entrena (SFT + RL); en el MVP de Zettel tendrá que ser regla explícita en prompt + código, no política aprendida.

**Separación control/contenido (arXiv 2609.00621): corroborado, y es la corroboración más profunda de los principios 2 y 5.** El paper existe (sep-2026, EMNLP Findings): el control crítico (ruteo, formato, terminación) como objetos tipados y validados en código, el contenido como flujo de datos optimizable; 100% validez de protocolo. Converge con toda una línea: Control Plane as a Tool, Sovereign Agentic Loops, Arbiter-K, y sobre todo Source Code Agent ("blueprint first, model second": +97,6% en TravelPlanner, −96% violaciones de restricciones). Traducción a Zettel: R, allowlist de herramientas, procedencia, presupuesto y terminación son control (código); la pregunta estructurada, la brecha y las filas son contenido (orquestador). Nada de lo crítico puede depender de que el LLM "se acuerde" de hacerlo.

**CRAG (2024): corroborado.** Evaluador liviano de recuperación (T5, 0,77B — superó a ChatGPT como evaluador) que dispara Correcto / Incorrecto / Ambiguo → refinar lo recuperado / descartar e ir a la web / combinar. Respalda "corpus primero, mundo ante brecha". Matiz: CRAG evalúa relevancia de lo recuperado, no suficiencia de la respuesta; Zettel necesita ambas compuertas (ver §2).

**MCP como estándar de herramientas: corroborado.** Spec activa, registro público (preview sep-2025), y guías oficiales que confirman dos decisiones: toolsets acotados y descubrimiento progresivo cuando las definiciones saturan contexto; llamadas programáticas (el modelo escribe código que compone herramientas, ejecutado en sandbox) para encadenamientos.

## 2. Qué refuto o cambiaría y por qué

**a) Corpus por listar+leer: lo acepto para 1-2 documentos, pero el contrato real debe ser búsqueda desde el MVP.** La guía de Anthropic para escribir herramientas lo desaconseja explícito: no exponer `list_*` que vuelcan contexto; construir `search_*` que devuelvan rebanadas pertinentes; consolidar operaciones encadenadas en una sola herramienta. La literatura 2026 de búsqueda agéntica coincide: espacios de interacción acotados por relevancia (RISE, RARG) superan al rastreo crudo, y hasta una interfaz mínima "grep + read" supera a un baseline de recuperación densa. Y hay un argumento interno decisivo: la Q5 exige detectar que D6 (documento) y M2 (inventario) hablan del mismo caso+aspecto+condiciones; ese JOIN entre documentos debe hacerlo el código sobre un índice caso→[(doc, ids)] construido al incorporar, no el LLM comparando a ojo dos fichas. Propuesta: `buscar_en_corpus(caso?, aspecto?, texto?)` (devuelve snippets con respaldo e ids), `leer_ficha(doc, ids?, paginado)`, y `listar_documentos` como affordance de auditoría/código, no como ruta feliz. Con 2 documentos todo esto es trivial de implementar y evita re-arquitecturizar al tercer documento.

**b) El orden fijo "responder con D → juzgar → encargos" desperdicia llamadas de juez.** Si la brecha es estructural (falta un dato que el corpus no puede dar, ej. la duración del vuelo), juzgar la respuesta-con-D tiene resultado predecible ("no establecido") y cuesta una llamada. Cambio: dos compuertas baratas antes del juez caro. Primero, cobertura por código (¿el campo contiene determinaciones del caso+aspecto+condiciones, o la brecha es ausencia total?). Si hay respuesta candidata con D, juicio de suficiencia; si la brecha es ausencia estructural, directo a encargos. Tras los encargos, re-juzgar solo el delta (lo que cambió), no toda la respuesta. Es la delegación selectiva de Uno-Orchestra aplicada al juez.

**c) `juzgar(respuesta)` no debe ser una herramienta que el orquestador decide llamar: debe ser una etapa que el código impone.** Si juzgar es optativo para el LLM, aparece el modo de fallo documentado (verificador que aprueba sin verificar) y el riesgo de 2609.00621 (una edición de prompt corrompe el protocolo). Precedente implementado: SearchClaw rechaza por hooks las respuestas sin citas suficientes antes de finalizar. En Zettel: el orquestador propone tabla+respuesta; el código invoca al juez en checkpoints fijos y devuelve veredicto tipado + obligaciones residuales si no pasa. Lo mismo vale para `terminar(salida)`: el LLM propone el cierre; el código valida (verificador de forma + cumplimiento de R + toda ruta resuelve a ids existentes) y acepta o devuelve qué falta. Esto extiende la filosofía de `pieza1.py` al orquestador.

**d) Investigador y programador como dos herramientas fijas: generalizar a una primitiva de delegación con plantillas.** Los roles estáticos exigen ingeniería humana por tipo de tarea; AOrchestra muestra que componer (instrucción, contexto, herramientas, modelo) en runtime es superior y deja la orquestación como política aprendible. En el MVP, una sola primitiva `encargar(brief tipado)` —objetivo, contexto curado, herramientas permitidas, modelo, formato de devolución, presupuesto— con dos plantillas de brief (investigador, programador) cuesta lo mismo y deja abierta la puerta a validador, citador, etc. sin nuevas herramientas. Y el brief del programador debe mandar el orden que ConnectorForge demostró: sondear la API viva primero, extraer esquema de la evidencia, ensamblar desde plantillas (no código libre: ~40%→fiable), auto-reparar ≤3 iteraciones, todo en sandbox (Docker o equivalente; guía Plan-then-Execute: sandbox no negociable).

**e) Anti-ciclo solo con "¿estamos en un ciclo?": necesario pero insuficiente.** La práctica 2025-2026 es unánime: el límite de recursión/rondas es backstop, no defensa; la defensa es un guardia mecánico que hashea la tupla (herramienta, argumentos canónicos, firma del resultado) y detiene/replanifica a las 2-3 repeticiones idénticas (LangChain cerró sin implementar el suyo propio: es código que cada uno escribe). Magentic añade el contador de estancamiento con reset+replanificación acotada. Importante: incluir la firma del resultado distingue el sondeo legítimo (misma llamada, resultado cambiante) del no-avance (misma llamada, mismo resultado). La pregunta introspectiva del registro queda como una señal más, no como el mecanismo.

**f) Al conjunto de herramientas le faltan tres piezas.** Presupuesto visible (R trae tope de costo/tiempo: el registro debe mostrar saldo restante para que el orquestador lo considere, como Uno-Orchestra hace el costo first-class); `preguntar_usuario` (el principio 4 lo exige como último recurso sobre contenido, con precedente en SearchClaw, y el código debe impedir su uso para infraestructura); y resolución de citas del lado del código (cada id de ruta debe resolver mecánicamente, como ya hace el verificador de la pieza 1).

## 3. Qué falta

- **Persistencia y reanudación.** Llamadas de ~50s y ciclos multi-ronda exigen checkpoints (LangGraph, Magentic, Anthropic: estado durable + despliegues sin romper corridas). El crudo por llamada ya es práctica del repo; elevarlo a run ledger append-only (cada llamada, hash de resultado, snapshot de registros) que sirva a la vez de auditoría de K y de datos para futuras reglas de esfuerzo.
- **Gestión de contexto explícita.** La ventana del orquestador es el recurso escaso (plan + resúmenes de workers la llenan). Contrato de devolución tipado (resultado conciso, artefactos/ids, errores — el observation contract de AOrchestra); ledger de llamadas a herramientas en zona protegida de la sumarización; corpus con revelado progresivo (snippets primero, ficha completa a pedido).
- **Arnés de evaluación desde el día uno.** Batería Q1–Q6r × 3 réplicas como regresión obligatoria ante cada cambio del orquestador, más métricas de costo, latencia y estancamientos por corrida; medir tasa de éxito por tipo de subtarea (es el denominador de la ecuación de costo de delegar). Precedente: el harness de SearchClaw aportó +20pp sobre el mismo modelo y herramientas.
- **Ciclo de vida del conector (la lección Alita-G que la propuesta no recoge).** Investigar → sondear → escribir → probar → abstraer (parametrizar, documentar) → registro versionado → selección por recuperación en la siguiente pregunta. Más política de re-sondeo vs confianza, conectada con el mantenimiento de la verdad de la pieza 1 (si K1 cambia de 10h35 a 11h10, ¿qué se cae?).
- **R como código, enumerado.** Matriz herramienta×modo-R (extensión del esquema2 §3), presupuestos, autorización de agentes, anclas inyectadas por código (la hora la da el sistema, no la recuerda el LLM), schema de config versionado, denegación por defecto ante cualquier llamada fuera del allowlist.
- **Taxonomía de fallos con jugada de recuperación por clase.** Reintentar, re-rutear a segunda fuente, replanificar el resto, o detenerse — decidida por el código según la clase de error, no improvisada por el LLM.
- **Modelo de amenazas mínimo.** El corpus es input no confiable para las herramientas (inyección vía documentos); herramientas de subagentes con privilegio mínimo y alcance por tarea; el corpus no se escribe desde lectores; sin credenciales en fichas (la condición "gratis sin registro" también es control de seguridad).
- **Índice caso-céntrico entre documentos (promover el "luego" a "ahora").** La Q5 lo exige: mismo caso+aspecto+condiciones en dos documentos. Construido al incorporar, consultado por `buscar_en_corpus`.

## 4. Postura sobre las decisiones abiertas

**Mismo modelo para todo vs. uno más capaz para orquestar: distintos por rol desde el MVP.** La evidencia es consistente y cuantificada: líder fuerte + workers baratos gana (Anthropic +90,2%), la calidad de orquestación es la restricción vinculante (AOrchestra: orquestador débil 57% vs fuerte 80%, y aun el débil supera a ReAct solo), y el enrutamiento por paso ahorra ~70% reteniendo ~97% de calidad (AgentRouter, CASTER). Patrón industrial convergente (OpenRouter subagent): el caro planifica e integra con presupuesto chico de tokens; el barato genera volumen. Matiz propio de Zettel: el orquestador aporta "mundo del orquestador" (K3: reglas de lectura), luego más capaz = mejor K… pero también más riesgo de premisa alucinada; el contrapeso ya existe (K-orquestador entra como dependencia tipada regla/no-dato, examinada por verificador y juez). Recomendación: MVP con 2 niveles (orquestador fuerte, encargos baratos, extractor sin cambios), instrumentando tasa de éxito por subtarea; la ecuación de costo (delegar compensa solo si costo_worker/éxito < costo_orquestador) decidirá después. No entrenar un router tipo Uno en el MVP.

**Cálculos simples por el programador vs. funciones fijas de calendario: funciones fijas, sin duda para calendario/husos/aritmética; el programador solo para lo no previsto.** Los LLM no razonan tiempo de forma fiable (OOLONG <50%, "Test of Time" 29% en scheduling y 13% en duraciones; "no se llega con prompt-engineering a expansión RRULE ni a cómputo con husos"). La línea determinista (Source Code Agent, guías de herramientas) muestra que mover cómputo a código es lo que recorta violaciones. Zettel ya tiene la categoría M-código con versión registrada: extenderla a una biblioteca cerrada (resolver fecha relativa, offsets/husos con tzdata fijada, aritmética, cierre X-al-Y→Y+1) y regla dura: si el cálculo cabe en la biblioteca, se llama a la función — el código, que es quien llena la tabla final, puede incluso interceptar briefs de cómputo de fechas y redirigirlos. El programador genera código para APIs y conectores, nunca para restar fechas.

## 5. Fuentes con URL

Orquestación y registros (Magentic):
- Paper Magentic-One: [arxiv.org/html/2411.04468](https://arxiv.org/html/2411.04468)
- Microsoft Research, anuncio: [microsoft.com/research Magentic-One](https://www.microsoft.com/en-us/research/articles/magentic-one-a-generalist-multi-agent-system-for-solving-complex-tasks/)
- Docs de orquestación magentic: [learn.microsoft.com magentic](https://learn.microsoft.com/en-us/agent-framework/workflows/orchestrations/magentic)
- Orquestaciones 1.0 (08-07-2026): [devblogs.microsoft.com](https://devblogs.microsoft.com/agent-framework/agent-frameworks-orchestration-patterns-reach-1-0/); framework 1.0 (03-04-2026): [devblogs.microsoft.com](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)

Multiagente (Anthropic):
- Cómo construimos el sistema multiagente (13-06-2025): [anthropic.com/engineering/multi-agent-research-system](https://www.anthropic.com/engineering/multi-agent-research-system)
- Cuándo y cómo usar multiagente (ene-2026): [claude.com/blog/building-multi-agent-systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them)
- Escribir herramientas efectivas (sep-2025): [anthropic.com/engineering/writing-tools-for-agents](https://www.anthropic.com/engineering/writing-tools-for-agents)

Auto-evolución y conectores (Alita):
- Alita: [arxiv.org/abs/2505.20286](https://arxiv.org/abs/2505.20286), repo: [github.com/CharlesQ9/Alita](https://github.com/CharlesQ9/Alita)
- Alita-G: [arxiv.org/abs/2510.23601](https://arxiv.org/abs/2510.23601)
- ConnectorForge (sondear-antes-de-generar, plantillas): [devpost.com/software/connectorforge](https://devpost.com/software/connectorforge)

Orquestación aprendida y contexto curado:
- AOrchestra: [arxiv.org/abs/2602.03786](https://arxiv.org/abs/2602.03786), repo: [github.com/FoundationAgents/AOrchestra](https://github.com/FoundationAgents/AOrchestra)
- Uno-Orchestra: [arxiv.org/html/2605.05007v1](https://arxiv.org/html/2605.05007v1), repo: [github.com/CuiZHIQ/Uno-Orchestra](https://github.com/CuiZHIQ/Uno-Orchestra)

Control en código, no en prompt:
- Separación control/datos: [arxiv.org/abs/2609.00621](https://arxiv.org/abs/2609.00621)
- Source Code Agent (blueprint first): [arxiv.org/pdf/2508.02721](https://arxiv.org/pdf/2508.02721)
- Plan-then-Execute + sandbox: [arxiv.org/pdf/2509.08646](https://arxiv.org/pdf/2509.08646)
- Control Plane as a Tool: [arxiv.org/html/2505.06817](https://arxiv.org/html/2505.06817)
- Crítica a orquestación por prompt (GraphBit): [arxiv.org/html/2605.13848](https://arxiv.org/html/2605.13848)

Corpus primero, mundo después:
- CRAG: [arxiv.org/html/2401.15884v2](https://arxiv.org/html/2401.15884v2), repo: [github.com/HuskyInSalt/CRAG](https://github.com/HuskyInSalt/CRAG)

Anti-ciclo y guardias mecánicos:
- Guardia de no-avance (hash de tupla, 2-3 repeticiones): [particula.tech](https://particula.tech/blog/stop-ai-agents-looping-same-tool-call-no-progress)
- Límites de recursión en LangGraph: [machinelearningplus.com](https://machinelearningplus.com/gen-ai/langgraph-cycles-recursion-limits-agent-loops/)

Corpus agéntico y procedencia:
- Interacción directa con corpus (DCI): [arxiv.org/pdf/2605.05242.pdf](https://arxiv.org/pdf/2605.05242.pdf), repo: [github.com/DCI-Agent/DCI-Agent-Lite](https://github.com/DCI-Agent/DCI-Agent-Lite)
- RISE (espacio acotado por relevancia): [github.com/texttron/RISE](http://github.com/texttron/RISE)
- Mapa de corpus por entidades: [arxiv.org/html/2609.37226](https://arxiv.org/html/2609.37226)
- Integridad de procedencia: [arxiv.org/pdf/2608.12761](https://arxiv.org/pdf/2608.12761)
- SearchClaw (hooks de calidad, citas mínimas): [github.com/RUC-NLPIR/SearchClaw](https://github.com/RUC-NLPIR/SearchClaw)

MCP:
- Spec herramientas: [modelcontextprotocol.io](https://modelcontextprotocol.io/specification/2025-06-18/server/tools)
- Registro MCP: [blog.modelcontextprotocol.io](https://blog.modelcontextprotocol.io/posts/2025-09-08-mcp-registry-preview/)
- Descubrimiento progresivo: [modelcontextprotocol.io clientes](https://modelcontextprotocol.io/docs/2025-03-26/develop/clients/client-best-practices)

Modelos por rol y costo:
- AgentRouter (72% ahorro, 97,3% calidad): [arxiv.org/pdf/2609.22951v1](https://arxiv.org/pdf/2609.22951v1)
- CASTER: [arxiv.org/pdf/2601.19793v1](https://arxiv.org/pdf/2601.19793v1)
- Patrón subagente barato (OpenRouter): [openrouter.ai cookbook](https://openrouter.ai/docs/cookbook/building-agents/subagent-server-tool)
- Ecuación de costo orquestador-workers: [zorost.com](https://zorost.com/orchestrator-worker-model-loops)

Tiempo determinista:
- Por qué los agentes fallan en scheduling (OOLONG, Test of Time): [temporal-cortex.com](https://temporal-cortex.com/blog/why-ai-agents-fail-at-scheduling/)

Nota de independencia: esta evaluación se hizo sin leer `mvp/orquestador-arquitectura-deepseek-2026-10-04.md`. Solo lectura en todo el trabajo; ningún archivo fue modificado.
