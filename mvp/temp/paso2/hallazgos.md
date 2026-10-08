# Paso 2 · qué aprendimos · 06-10-2026 (cierre de la ronda)

Sale de lo ya medido y guardado en `mvp/paso2/`: **69 crudos** (63 en el
análisis: 33 de `deepseek-flash` y 18 de Muse Code en desarrollo, más 12 de
DeepSeek en la reserva; 6 de Muse de la reserva sin uso), **42 expectativas
registradas** en desarrollo y 30 en la reserva, fijadas antes de llamar.
Ninguna llamada nueva. Conteos y respaldos: `evaluacion_items.md`; crudos,
tareas y costos: `inventario_y_costos.md`.

**Regla de lectura:** aquí solo queda lo respaldado. Cada punto dice si es
**observación** (lo que se vio en los archivos) o **hipótesis** (una lectura que
haría falta probar aparte).

## 1. La comparación, en una tabla

Recuperación estricta sobre expectativas válidas (los `parcial` no suman);
fidelidad sobre las afirmaciones producidas:

| Entrada | Recuperación (agregado) | DeepSeek | Muse (solo doc4) | Fidelidad |
|---|---|---|---|---|
| (a) unidad sola | 46/65 = 70,8 % | 29/41 = 70,7 % | 17/24 = 70,8 % | 103/103 = 100 % |
| **(b) unidad + referencias** | **62/65 = 95,4 %** | 39/41 = 95,1 % | 23/24 = 95,8 % | **111/113 = 98,2 %** |
| (c) unidad + documento | 55/65 = 84,6 % | 34/41 = 82,9 % | 21/24 = 87,5 % | 103/103 = 100 % |

Reserva (b), DeepSeek: **29/29 = 100 %** de recuperación y **70/70 = 100 %** de
fidelidad, con una expectativa defectuosa informada aparte. El agregado mezcla
los dos modelos (DeepSeek corrió doc4 y doc5; Muse solo doc4): **no se atribuye a
uno solo**.

## 2. Lecciones

**1. Las referencias ayudaron en casos concretos; no garantizan resolver todas
las identidades.** *(observación)* Con la entrada (b) se recuperaron las
identidades, condiciones y sostenes que v9 había registrado (doc4 U3, U4, U6;
doc5 U2–U5), y por eso (b) es la mejor de las tres. Pero en doc4 U2 **no había
ninguna referencia** y el ítem «la causa del corte» quedó `parcial` en (a) y
(b): lo que el paso 1 no registra no llega al paso 2.

**2. El documento completo sí resolvió conexiones que faltaban.** *(observación)*
En (c) se completaron «la causa del corte» (doc4 U2) y la relación entre los dos
cortes (doc4 U5). **No se sostiene** que «el documento entero no arregla la
identidad»: lo que se observa es que **no las resuelve todas** —dejó sin
identificar «los vecinos» (el barrio), «la ciudad» y «el servicio» del tranvía,
«la red» del tranvía y el taller de los planos—, y por eso (b) queda por delante
(95,4 % frente a 84,6 %).

**3. Detectar toda referencia externa omitida exige interpretar; no es una
comprobación mecánica disponible.** *(observación + límite)* El código puede
comprobar literalidad y listar candidatas, pero decidir que «la solicitud» de
`doc4 [17]` necesita un antecedente externo —y cuáles son admisibles— es lectura.
En doc4 U6 la expectativa que fijaba `[8]` como lectura única resultó
**defectuosa**: el documento admite `[8]`, `[14]` y `[15]`.

**4. Un respaldo no verificable es un problema de trazabilidad, aunque por sí
solo no demuestre falsedad del contenido.** *(observación)* En los 63 crudos del
análisis **no hubo ningún respaldo no verificable** (`no_literales = 0`) ni citas
de oraciones no recibidas; sí hay 39 citas **fuera de la unidad**, legítimas,
porque vienen del contexto recibido. Una cita literal, en cambio, **no prueba**
que el uso sea correcto: la única deformación (doc4 (b) U5) tenía citas
perfectamente literales. Son dos comprobaciones distintas.

**5. Perder la identidad puede perder la determinación; no es un detalle
nominal.** *(observación + marco)* «La empresa» no dice de quién se afirma la
respuesta; «la red» no dice de qué red se predica la longitud. En el marco, la
determinación es de un caso de estudio bajo un aspecto y unas condiciones:
perder de qué se habla compromete la determinación, no solo su etiqueta.

**6. En `doc4 (b) U5` el razonamiento de DeepSeek considera la distinción entre
los dos acontecimientos y acaba siguiendo el referente suministrado.**
*(observación)* El `reasoning_content` guardado dice, literalmente: «But if [1]
is current corte, [11] last year's similar, they are distinct. Yet context says
referent is el corte de agua en barrio San Jorge. Follow context.» **Hipótesis, no
mecanismo general:** es un indicio de tensión entre lo que dice el texto y la
aclaración que se le entrega (el propio referente de v9 fundía los dos cortes),
no prueba de una tendencia del modelo.

**7. Las deliberaciones sobre casos, relaciones, condiciones, acciones e
`inferido` muestran decisiones de representación abiertas.** *(observación)* El
razonamiento es largo (en U5(b), unos 42 000 caracteres) y buena parte se va en
dónde va cada cosa entre las siete listas, qué se cuenta como caso y dónde se
marca `inferido`. **No se les atribuye automáticamente todo el costo:** es una
parte visible, no la medida del costo total.

**8. Los resúmenes de Muse no son su razonamiento completo.** *(límite)* Del lado
de Muse se guarda la respuesta final (`.out`) y el `.jsonl` de la sesión, con
eventos de resumen (`response.reasoning_summary_part.done`) y un timeout de
transporte; **no** el razonamiento entero. Tampoco se reconstruye de ahí la
duración del modelo (las marcas de tiempo del `.jsonl` son sintéticas).

**9. La reserva fue escrita por el diseñador y es breve.** *(límite)* Alcanzó
100 % y 100 %, pero **no es validación independiente**: mismas manos que el
candidato, referencias completas y dos documentos cortos. Lo que sí sostiene es
que, **con las referencias completas, (b) recupera todo lo esperado en esos dos
documentos sin importar nada ajeno**.

**10. El campo `referente` mezcla identidad con condición y con contenido.**
*(observación)* «la red… que llegó a tener veintiocho kilómetros de vías»;
«la respuesta de la empresa… de que la fecha ya estaba contratada». Con la
entrada (b) los cuatro controles de «esto no debe importarse» se cumplieron, así
que la frontera aguanta escrita en el prompt; pero esos referentes largos son los
que hay que mirar.

**11. La duda viaja bien; lo que hay que vigilar es la resolución inventada.**
*(observación)* Las referencias sin resolver (doc4 U6, doc5 U5) se conservaron
como duda con sus lecturas, y ninguna corrida declaró que fueran distintas.

**12. Cambiar el prompt del paso 1 mueve la partición.** *(observación
antecedente)* En `doc2`, v7 daba 4 unidades y v8 dio 7. Por eso las expectativas
por unidad solo valen contra una partición congelada.

## 3. Costos

- **DeepSeek `deepseek-flash`:** 45 llamadas (33 de desarrollo + 12 de la
  reserva), 590 789 tokens de salida y 129 837 de entrada; **91 % de lo generado
  es razonamiento**, incluido en `completion_tokens`. Tiempo de llamada:
  29,0–84,2 s en desarrollo, 32,9–80,5 s en la reserva.
- **Muse Code:** 65 s a 2 646 s por tarea con la misma entrada, y ese tiempo es
  del **envoltorio** (incluye un timeout de transporte de 47 s en la tarea larga),
  no del razonamiento. Sirve para pocas tareas, no para una barrida de 30.
- **Tiempo comparado, solo DeepSeek:** en total, (b) usa 20,6 s menos que (a) y
  34,4 s menos que (c) (≈3–5 %). La diferencia grande que se vio primero era una
  tarea de Muse de 44 minutos.
- **Fidelidad y costo no se pelearon:** la entrada más fiel fue también la más
  barata.

## 4. Lo que sigue sin saberse

- **Un solo juez**, sin segunda lectura de las casillas.
- **Sin réplicas por unidad y entrada:** una pasada permite decidir entre
  alternativas, no medir estabilidad.
- **La lista fina de 55 ítems no se registró:** el conteo auditable usa las 42
  expectativas registradas. Si se quiere el conteo fino, hay que escribir y
  registrar la lista **antes** de volver a mirar las salidas.
- `doc5` sin Muse; la reserva no es independiente.
- **La referencia hacia adelante sigue sin ejercitarse** y todos los textos son
  cortos (14–17 oraciones).

## 5. Cómo correr esto la próxima vez

1. **Fijar el modelo, la partición y la lista de ítems antes de mirar salidas**,
   y no moverlos durante la medición.
2. **Un ítem por cosa** (contenido, identidad, condición, duda) y contar por
   afirmación, no por campo del JSON: un ítem que mezcla contenido e identidad
   se califica `parcial`.
3. **Anunciar antes de cada tramo:** cuántas llamadas, con qué modelo, cuánto
   tarda y cuánto puede costar — como estimación, y avisar si la medición la
   contradice.
4. **Una pasada por alternativa, y comparar solo lo que se midió igual.**
5. **Parar es parar:** no abrir el tramo siguiente hasta que se pida.
6. **Dos comprobaciones separadas:** forma por código (literales contra el
   material enviado) y contenido por juicio contra lo esperado.
7. **No usar ejemplos tomados de los documentos de prueba** ni esperar que un
   ítem se recupere sin haber fijado antes el corte de la unidad.
8. **Guardar y poder re-verificar sin API:** `comparacion.py verificar-todos`
   relee los crudos y vuelve a comprobar los literales contra el material
   enviado (hoy: 69/69 sin diferencias).
