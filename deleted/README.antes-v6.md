# Spike Jev — detección con modelo de decisiones

## Contexto

El piloto EEL detecta estructura con GLM vía prompts JSON (tareas A/B/C)
más post-proceso determinista. Funciona (golds 05/06 exactos), pero cada
corrida total cuesta minutos por el razonamiento del modelo, y la
"confianza" que usábamos era un número sin calibrar (eliminado del
esquema 2026-09-19).

El cookbook `autoformat` de TypeSafe muestra otro paradigma: el modelo
nunca genera texto, solo responde preguntas angostas con probabilidades,
y el código decide y renderiza. Trabajamos directo contra
`api.typesafe.ai` con Jev (`TYPESAFE_API_KEY` por entorno; SDK 0.7.0
instalado como referencia, runtime con urllib + dicts). `classifier.dev`
(mismo modelo, sin clave) quedó archivado como plan B: fue el puente
mientras no había acceso.

Fuentes leídas (verificadas, mandan sobre blogs de terceros):
`https://docs.typesafe.ai/cookbooks/autoformat`, `https://docs.typesafe.ai/api.md`,
páginas de primitivas/State/confianza, skill oficial, `https://classifier.dev`
(+ `/docs`, `/benchmark`), índice en `https://docs.typesafe.ai/llms.txt`.

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

4. Los IDs de pregunta viajan pero el modelo no los usa (doc literal);
   sirven para casar cada respuesta en código.
5. Sobre interno vs cable: en código/crudos vive el sobre completo
   (payload + metadata: `usuario`, hashes, latencia, tokens, modelo
   efectivo); al cable se serializa solo `model`/`state`/`questions`.
6. Sin SDK en runtime: urllib + dicts planos (patrón `llm.py` del
   piloto); el SDK queda como referencia de tipos.
7. Invariante de entrada original también con Jev: el modelo ve el
   verbatim; el anclaje se resuelve en código.
8. State con nombres que digan qué es cada cosa (`texto_a_evaluar`, no
   `bloque`); las instrucciones nombran los campos (backticks), nunca
   "this block" a secas.

Preguntas y juicio:

9. Se elige primitiva por lo que la respuesta significa: Noul para
   condición sí/no, Choice para una opción de un conjunto, Score para
   grado en escala.
10. Toda Choice lleva su no-match explícito (la confianza no detecta
    "ninguna vale") y descripciones por opción.
11. Umbrales calibrados con datos propios (gold/sembrado), nunca los del
    cookbook ni 0,5 a ciegas.
12. Noul ~0,5 = incertidumbre (sí y no igual de probables), no intensidad
    media; no hay confianza separada en Noul.
13. A Jev, juicios; al código, cómputo: contar letras, offsets y
    aritmética los hace `comun.py`, nunca una pregunta (medido: en el
    borde 9/11 letras responde ~0,5).
14. Wording e idioma se testean con datos (gold + pares ES/EN), no se
    opinan: lo claro sale igual en ambos (0,99/0,99); las diferencias
    aparecen en el borde.

Método del spike:

15. El spike no concluye (mala práctica): junta evidencia, informa con
    números; decide la auditoría con Frat.
16. Esta API no tiene `temperature`: la estabilidad se mide re-corriendo
    (los números respiran entre llamadas: 0,87–0,95 lo mismo).
17. No hay tiers en el API crudo (`fast`/`smart` son orquestación de
    classifier.dev); si hace falta revisión, el escalado lo construimos
    (Jev + GLM = `confidence-routing`).
18. Inglés rinde algo más por diseño (oficial); calibrar en español con
    datos propios.
19. State solo texto, sin adjuntos (ni imágenes/audio); docs de 1–4 KB
    sobrados; si algo no entra, se parte en código.
20. Solo documentos sintéticos (aunque el texto no se almacena).
21. La confianza calibrada del modelo sí se usa: routing < 0,7 a
    revisión/escalado/fallback (reemplaza al número inventado que
    eliminamos del esquema).
    *Corrección 2026-09-22*: TypeSafe describe sus modelos como
    entrenados para probabilidades calibradas (a nivel de grupo), pero
    el 0,7 no está calibrado: es un valor de partida. Se fija por acción
    y dominio con datos propios, lejos de grupos de casos reales (en la
    batería de urgencia, h3 dio 0,71/0,69/0,72 y cruzaba el 0,7 entre
    réplicas). Ver guía §5.
22. Reportar antes de inventar; prompts y campos, tal cual.
23. Pregunta vs afirmación son dos estructuras de decisión (1 Choice vs
    N Nouls) con distinto costo y auditabilidad; la elección se justifica
    por caso y se mide, no se prefiere por defecto.
24. Las tablas viajan como state estructurado (array de objetos, no
    prosa); cada celda/fila se juzga por separado con instrucciones que
    apuntan a su campo.
25. El batch no cambia el veredicto (observación importante): cada
    pregunta se evalúa en paralelo y aislada contra el mismo state
    (patrón oficial `speculative fan-out`); mandar N juntas o una por
    una da el mismo juicio (medido: `titulo` 1.00 sola y en grupo de
    11). Solo cambia la operación: 1 llamada en ~1 s vs N llamadas.
    Los números respiran entre corridas (regla 16), pero no el lado ni
    el orden de magnitud.

## Arquitectura que veo (propuesta, a acordar)

Principio: Jev juzga, el código decide. Nada de lo determinista cambia
(bloques, offsets, pila, vistas, contrato EEL).

- A por bloque: Choice [rotulo, contenido] (+scores); nivel por pila
  desde orden + marcador verificado, o dimensión extra [nivel_1,
  nivel_2] a probar.
- B por párrafo: Choice [frontera, continuacion]; umbral calibrado desde
  el gold (estilo cookbook 0.2/0.5), no 0.5 a ciegas.
- Confidence-routing: < 0,7 → revisión humana o fallback al GLM
  actual (escalado propio; no hay tier smart en el API crudo).
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
  re-pregunta a GLM donde Jev dude (< 0,7). Métrica: costo/latencia/
  calidad con y sin escalado.
- Informe: tabla comparativa y recomendación (adoptar / híbrido /
  descartar). Cada fase deja notas acá, no solo código.

## Evidencia reunida (sesión 2026-09-19, sin veredicto: decide auditoría)

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
- Crudos: `spike-jev/cache/modalidad-50.json`, `spike-jev/cache/tabla-30.json`;
  scripts: `spike-jev/probes/modalidad_50.py`, `spike-jev/probes/tabla_30.py`.

## Noul, Choice y Score, en palabras (cierre 2026-09-20)

- **Noul** responde *¿es verdad?* → un número entre 0 y 1 (sí/no con
  duda).
- **Choice** responde *¿cuál es?* → elige una opción entre varias **sin
  orden** (rótulo o contenido, da igual cuál vaya primero).
- **Score** responde *¿cuánto?* → un número sobre **niveles ordenados**
  que uno define (nada / algo / mucho). Si duda entre niveles vecinos,
  el número cae en el medio (1.6); si está seguro, cae justo en un
  nivel. Medido: urgencia de un mensaje ("server down, help now") sobre
  [espera / esta semana / hoy] → `score` 2.0, confianza 1.0.
- La diferencia clave: Noul y Choice deciden entre alternativas; Score
  mide **grado dentro de un orden**.

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
(`spike-jev/probes/modalidad_50.py`, crudo en
`spike-jev/cache/modalidad-50.json`).

**Resultados**: **50/50 en ~2 s** (10.5 k in / 4.1 k out). 43
unánimes (1.00); la única fuga relevante fue q31 (`Que el jurado
delibere con serenidad y justicia` → desiderativa 0.76 / imperativa
0.20), ambigüedad genuina del subjuntivo exhortativo, no ruido. Las
marcas formales (¿?, ¡!, modo verbal, adverbios, ausencia de verbo)
separan casi perfecto, en español.

## Convenciones del spike
- Todo duerme en esta carpeta; README antes de código (política del repo).
- Respuestas cacheadas en disco (estilo `json_cache` del cookbook): un
  re-run no re-paga ni re-llama.
- Ninguna clave en archivos (`TYPESAFE_API_KEY` solo por entorno).
- Rama `spike-jev`; el piloto no se toca. Si resulta, se integra por
  decisión de Frat.
