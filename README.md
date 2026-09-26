# Spike Jev — detección con modelo de decisiones

## Estado actual (2026-09)

El trabajo activo está en `niveles/`: extracción de **datos** de un `texto`
con un LLM (DeepSeek), según el ensayo de Frat «¿Qué es un dato?», con Jev
como auditor posterior. Rondas: `niveles/PLAN.md`. Estado, lecciones y
pendientes: `memoria de trabajo y pendientes.md`.

El objetivo original (Jev en lugar de GLM para la detección de estructura
del piloto EEL; secciones Contexto, Arquitectura y Plan de pruebas) está
**suspendido**, no abandonado. Las reglas 1–26 y el marco conceptual siguen
vigentes.

## Correr las pruebas en local (proxy de claves)

**Por qué hay un proxy.** Los scripts nunca leen claves ni arman la cabecera `Authorization`. En la nube, un proxy agrega la clave a cada llamada. En local hacemos lo mismo con `proxy_local.py`. Así el código es idéntico en los dos entornos, hay un solo repositorio y las claves nunca quedan en archivos del repositorio.

**Claves de los proveedores.** Son variables globales del shell, definidas en `~/.bashrc`:

| Proveedor | Host | Variable |
|---|---|---|
| TypeSafe (Jev) | `api.typesafe.ai` | `TYPESAFE_API_KEY` |
| Z.ai (GLM) | `api.z.ai` | `ZAI_API_KEY` |
| DeepSeek | `api.deepseek.com` | `DEEPSEEK_API_KEY` |

Para agregar o cambiar una clave, pon una línea `export NOMBRE=clave` en `~/.bashrc` y corre `source ~/.bashrc`. El proxy lee las claves solo al arrancar, así que después de cambiar una hay que reiniciarlo.

**Instalar mitmproxy (una vez).** Ubuntu no deja instalar con `pip --user`, así que va en un entorno aparte:

```bash
python3 -m venv ~/.venvs/mitmproxy && ~/.venvs/mitmproxy/bin/pip install mitmproxy
```

**Arrancar el proxy** (terminal 1, desde la raíz del repositorio; escucha solo en localhost):

```bash
~/.venvs/mitmproxy/bin/mitmdump -q --listen-host 127.0.0.1 -p 8080 -s proxy_local.py
```

La primera vez, mitmdump crea su certificado en `~/.mitmproxy/`. Desde un shell no interactivo, como el de Desktop Commander, hay que arrancarlo con `bash -ic '…'` para que cargue `~/.bashrc`.

**Correr un script** (terminal 2):

```bash
export HTTPS_PROXY=http://127.0.0.1:8080 SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem
python3 niveles/extraer_datos.py doc5 deepseek datos_v8 r1
```

El certificado del proxy solo lo usan los procesos que exportan `SSL_CERT_FILE`; no se instala en el sistema. El proxy agrega la clave solo a los tres hosts de la tabla y deja pasar el streaming. Al reiniciar la máquina, el proxy se apaga y hay que arrancarlo de nuevo.

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
