# Píldoras

Una píldora es una precisión o aclaración necesaria en el lenguaje que usa Frat;
un dato relevante dentro del contexto de la charla; o un dato nuevo que amplía
su vocabulario y su conocimiento y es pertinente a la discusión. Cada una lleva
el contexto en que surgió. Se agregan a medida que aparecen.

## Índice

1. [Definición ostensiva](#1-definición-ostensiva)
2. [Símbolos de unidades sin plural](#2-símbolos-de-unidades-sin-plural)
3. [Magnitud individual y magnitud general](#3-magnitud-individual-y-magnitud-general)
4. [Ejemplo prototípico o medoide](#4-ejemplo-prototípico-o-medoide)
5. [Aprendizaje por *near miss* (ejemplos contrastivos)](#5-aprendizaje-por-near-miss-ejemplos-contrastivos)
6. [Los ejemplares de Kuhn](#6-los-ejemplares-de-kuhn)
7. [Conjunto de desarrollo y conjunto de prueba reservado](#7-conjunto-de-desarrollo-y-conjunto-de-prueba-reservado)
8. [Cómputo en tiempo de inferencia y rendimientos decrecientes](#8-cómputo-en-tiempo-de-inferencia-y-rendimientos-decrecientes)
9. [Entidad medida y propiedad medida](#9-entidad-medida-y-propiedad-medida)
10. [Atributo implícito](#10-atributo-implícito)
11. [Paráfrasis y canonicalización](#11-paráfrasis-y-canonicalización)
12. [Segmentación lineal y enumeración de oraciones](#12-segmentación-lineal-y-enumeración-de-oraciones)
13. [Enunciados genéricos](#13-enunciados-genéricos)
14. [Operacionalismo](#14-operacionalismo)
15. [Incertidumbre definicional](#15-incertidumbre-definicional)
16. [Tipo y ejemplar](#16-tipo-y-ejemplar)
17. [La moda como estadístico: dato de segundo orden](#17-la-moda-como-estadístico-dato-de-segundo-orden)
18. [Correferencia](#18-correferencia)
19. [Granularidad de la segmentación](#19-granularidad-de-la-segmentación)
20. [Teoría de la estructura retórica (RST)](#20-teoría-de-la-estructura-retórica-rst)
21. [Caché de prefijo (prompt caching)](#21-caché-de-prefijo-prompt-caching)
22. [Chunking semántico](#22-chunking-semántico)
23. [Prefill y decodificación](#23-prefill-y-decodificación)

---

## 1. Definición ostensiva

**Qué es.** Enseñar un concepto señalando ejemplos en vez de definirlo.
Wittgenstein (*Investigaciones filosóficas*, §28) mostró su límite: al
señalar un ejemplo no queda claro qué rasgo se señala (¿la forma, el color,
el número?).

**Contexto.** Al pasar de definiciones a ejemplos (DU5). Por eso los ejemplos
tienen que contrastar entre sí; si todos traen cifras con unidad, el modelo
puede aprender «dato = número». En DU5 cada falla correspondió a un rasgo que
los ejemplos no mostraban: la ostensión enseña exactamente lo que muestra.

## 2. Símbolos de unidades sin plural

**Qué es.** En el Sistema Internacional, los símbolos de las unidades no llevan
plural ni punto: «12 kg», no «12 kgs».

**Contexto.** Decisión sobre «caja de 12 kg»: Frat escribió «kgs»; la unidad de medida queda «kg».

## 3. Magnitud individual y magnitud general

**Qué es.** El VIM distingue la magnitud general («longitud», «peso») de la
magnitud individual («el radio del círculo A», «el peso de esta caja»). Lo que
se mide, el mensurando, es siempre una magnitud individual. VIM4, nota 2:
*«the radius of circle a is an instance of length»*.

**Contexto.** Frat propuso que la variable sea «peso de la caja» y no «peso»
con un caso aparte. Respalda quitar el campo `caso`: la variable ya trae la
pregunta completa `variable(caso) = ?`. La mirada estadística (variable =
columna, caso = fila) es la de la tabla, no la de la medición.

## 4. Ejemplo prototípico o medoide

**Qué es.** El caso real que queda en el centro de un grupo de casos parecidos
y lo representa. En estadística, el medoide (a diferencia de la media, es un
caso que existe). Se emparienta con los prototipos de Eleanor Rosch.

**Contexto.** Nombre técnico de lo que Frat llamó «ejemplo nodo»: ejemplos que
cobijan a su alrededor muchos casos generales, más sus casos límite.

## 5. Aprendizaje por *near miss* (ejemplos contrastivos)

**Qué es.** Patrick Winston (1970): un concepto se aprende mejor viendo lo que
casi es y no es. En prompts, los ejemplos contrastivos o negativos difíciles
reducen los errores de frontera.

**Contexto.** Diseño de los nodos de `datos_u6`: cada uno lleva un casi-dato
junto a los datos («certificado» junto a «acidez alta», «antiguo muelle» junto
a «contenedor de 800 kg»).

## 6. Los ejemplares de Kuhn

**Qué es.** En la posdata de 1969 a *La estructura de las revoluciones
científicas*, Kuhn sostiene que los científicos aprenden un paradigma por
ejemplares (problemas resueltos), no por reglas. Emparentado con el parecido
de familia de Wittgenstein.

**Contexto.** Por qué definiciones cortas + ejemplos nodo: las definiciones
hacen de guía, los ejemplares de práctica.

## 7. Conjunto de desarrollo y conjunto de prueba reservado

**Qué es.** El conjunto de desarrollo es el que se mira mientras se diseña; el
conjunto de prueba reservado (*held-out*) no se toca hasta medir. Lo que se
miró al diseñar ya no sirve para medir con honestidad.

**Contexto.** ut1–ut5 pasaron a ser conjunto de desarrollo al discutir sus
fallas; el ~90 % que busca Frat se mide en unidades nuevas.

## 8. Cómputo en tiempo de inferencia y rendimientos decrecientes

**Qué es.** *Test-time compute*: gastar más cálculo al responder (más tokens de
razonamiento) en lugar de al entrenar. Su curva típica es de rendimientos
decrecientes: los primeros tokens rinden mucho y los siguientes cada vez menos.

**Contexto.** Pregunta de Frat por el `reasoning_effort` de Grok. En Grok 4.6
(Artificial Analysis): low 35, medium 43, high 44, xhigh 44 en el índice de
inteligencia; el salto grande es de low a medium. En tareas cortas como la
nuestra, más razonamiento puede no servir (DU4: 3250 tokens, peor resultado).

## 9. Entidad medida y propiedad medida

**Qué es.** En MeasEval (SemEval-2021, tarea 8, extracción de mediciones), la entidad medida es lo que tiene la
propiedad (la tos) y la propiedad medida es lo que se mide de ella (el tipo).

**Contexto.** DU6: en ut5 la variable nombraba la entidad sin la propiedad
(«tos» = seca, «dolor abdominal» = moderado). La variable debe llevar las dos.

## 10. Atributo implícito

**Qué es.** En la extracción de atributos, el caso en que el valor está en el
texto pero el nombre del atributo no: en «camisa roja», «color» nunca se dice.
Hay trabajos dedicados a ese problema (ImplicitAVE, 2024).

**Contexto.** Corrección de DU6 a DU7: un ajuste al nodo de cualidades («grano
grande» → «tamaño del grano», «tueste oscuro» → «grado de tueste») y la frase
«Si `texto` no nombra el aspecto, la variable lo nombra».

## 11. Paráfrasis y canonicalización

**Qué es.** La paráfrasis es la variación léxica (lo mismo dicho con otras
palabras), distinta de la semántica (cosas distintas). Canonicalizar es
reducir las paráfrasis a una forma única.

**Contexto.** DU7: la única variación entre tres réplicas fue «temperatura del
termostato» / «temperatura marcada por el termostato». Para comparar variables
entre textos hará falta canonicalizar; es un juicio que Jev puede sopesar
(«estas dos variables nombran la misma magnitud»).

## 12. Segmentación lineal y enumeración de oraciones

**Qué es.** La segmentación lineal de texto divide un texto en tramos
contiguos, sin reordenar nada (lo estándar en segmentación temática desde
TextTiling, de Hearst, 1997). Se distingue del agrupamiento, que puede juntar
oraciones separadas. La enumeración de oraciones numera la entrada para que el
modelo conteste con índices (dónde empieza y termina cada tramo) en vez de
copiar texto (*Topic Segmentation Using Generative Language Models*, 2026).

**Contexto.** Rediseño del paso 1 tras ENC1: `unidades_v2` agrupaba por
entidad (coherencia por entidades, teoría del centrado) aunque se llamaba
«temática», y en bio1 oscilaba entre tema y entidad. `unidades_v3` segmenta
linealmente por tema, con oraciones numeradas; el código arma cada unidad
con el texto original, así que la literalidad queda garantizada.

## 13. Enunciados genéricos

**Qué es.** En lingüística y filosofía del lenguaje, un enunciado genérico
habla de una clase o de una regularidad, no de un individuo: «Los herbívoros
controlan las algas», «Donde escasean, las algas cubren el sustrato en pocas
semanas». Se opone al enunciado particular («El pez loro fue la especie más
abundante en T-1 y T-3»). El estudio de estos enunciados se llama genericidad.

**Contexto.** Revisión crítica de la cadena sobre bio1 (U4): el modelo no
extrajo «pocas semanas». Es correcto según el ensayo «¿Qué es un dato?»: un
dato determina un caso individuado, y un enunciado genérico no tiene caso.
Sirve como criterio explícito para distinguir datos de regularidades.

## 14. Operacionalismo

**Qué es.** Posición de Percy Bridgman (*The Logic of Modern Physics*, 1927):
un concepto se define por la operación con que se mide. «Abundancia según
censo visual» y «abundancia según captura» serían variables distintas. Es la
tensión clásica entre definir lo medido por la cosa o por el procedimiento.

**Contexto.** Análisis de «número de peces registrados por los censos
visuales» en bio1: ¿el censo es procedencia (fuera de la variable) o parte de
lo que se pregunta (dentro)?

## 15. Incertidumbre definicional

**Qué es.** En el VIM (2.27), la incertidumbre que resulta de una definición del
mensurando sin todo el detalle necesario: si la variable no dice lo
suficiente, hay una ambigüedad sobre qué se mide que ninguna precisión del
valor corrige.

**Contexto.** Respalda el criterio de Frat de completitud de la variable
(decisión tras U4): la variable debe dejar claro qué varía, con su contexto,
incluido el método cuando define qué se midió; la procedencia queda para la
fuente del dicho.

## 16. Tipo y ejemplar

**Qué es.** Distinción de Charles S. Peirce (*type / token*): el tipo es la
clase o forma general (la especie «pez loro», la palabra «casa»); el ejemplar
es cada instancia concreta (este pez que nada en T-1, esta aparición de la
palabra).

**Contexto.** Revisión de «especie más abundante = pez loro» en bio1. La
regla vieja («un valor no es otro caso») confundía los dos: un tipo sí puede
ser valor (categoría del soporte de una variable nominal); lo que no puede
serlo es un ejemplar, que sería otro caso y daría una relación entre casos.

## 17. La moda como estadístico: dato de segundo orden

**Qué es.** La moda es el valor más frecuente de una variable en una muestra;
es el único resumen de tendencia central que tiene una variable nominal (no
tiene media ni varianza). Un dato que reporta un estadístico calculado sobre
una muestra es un dato de segundo orden.

**Contexto.** Marco de Frat: la variable tiene la estructura del fenómeno
(distribución, escala, momentos) y los valores son la muestra. «Especie más
abundante = pez loro» es la moda de «especie de cada pez» sobre los 215 y 98
peces del censo: el texto no reporta una observación, sino un estadístico.

## 18. Correferencia

**Qué es.** En lingüística, dos o más expresiones de un texto que se refieren a
la misma cosa forman una cadena de correferencia: «el oxígeno… este gas…»,
«los nódulos… estos fragmentos… estos nódulos». La expresión que remite hacia
atrás es una anáfora; la primera mención, su antecedente. Resolver la
correferencia es saber a qué remite cada «este», «su», «esas».

**Contexto.** Análisis de ENC3 (oxi1): la segmentación lineal dejó «este gas»
en una unidad y su antecedente («oxígeno») en otra, y la variable salió
incompleta («fuente de este gas»). En textos explicativos las cadenas de
correferencia cruzan las unidades mucho más que en textos de registro como
bio1.

## 19. Granularidad de la segmentación

**Qué es.** Qué tan fino se corta un texto al segmentarlo (por idea, por
subtema, por tema). No hay una granularidad correcta en abstracto: depende de
para qué se usan las unidades.

**Contexto.** Discusión del paso 1 tras ENC3: en oxi1, la premisa vieja y el
hallazgo que la contradice van juntas por subtema y separadas por idea. Frat
fijó el subtema como unidad del paso 1 y el tema como unión de subtemas.

## 20. Teoría de la estructura retórica (RST)

**Qué es.** Mann y Thompson (1988): un texto se describe como tramos unidos
por relaciones (elaboración, causa, consecuencia, contraste, explicación). En
cada relación, un tramo es el núcleo (lo central) y el otro el satélite (lo que
lo desarrolla).

**Contexto.** La definición de Frat del subtema («un asunto nuclear y su
desarrollo») coincide con ella, y dio el criterio operativo de `unidades_v4`:
una oración va con el subtema si lo detalla, explica, continúa, contradice o
saca su consecuencia. `unidades_v1`/`v2` usaban «núcleo» y «satélite» para
entidades; la RST los usa para tramos de texto.

## 21. Caché de prefijo (prompt caching)

**Qué es.** Cuando varias llamadas a un modelo comparten el mismo comienzo, el
proveedor no lo vuelve a procesar: lo cobra más barato y responde más rápido.
Por eso importa el orden del prompt: lo fijo primero, lo que cambia al final.

**Contexto.** Diseño de `datos_u8` (opción A): instrucciones, ejemplos y
documento completo primero; el foco (las oraciones de la unidad) al final. Los
crudos ya muestran `cached_tokens` en cada llamada.

## 22. Chunking semántico

**Qué es.** Partir o unir fragmentos de un texto según la similitud de sus
embeddings (por ejemplo, similitud coseno sobre un umbral). Es la versión
moderna de TextTiling.

**Contexto.** Propuesta de Frat para unir unidades del mismo asunto tras el
paso 1. Riesgo: la similitud no distingue asunto de entidad. Quedó para el
nivel de tema, combinado con Jev (los embeddings proponen candidatos, Jev
juzga).

## 23. Prefill y decodificación

**Qué es.** Un modelo responde en dos fases. El *prefill* procesa todo el
prompt de entrada de una vez (rápido: miles de tokens en fracciones de
segundo). La *decodificación* genera la salida token por token (lenta: unas
decenas de tokens por segundo), y en los modelos de razonamiento incluye los
tokens de razonamiento. La caché de prefijo solo ahorra prefill.

**Contexto.** Investigación de la caché en ENC4: sin `x-grok-conv-id`, las
llamadas casi nunca reutilizaron el documento; pero el tiempo de ENC4 (hasta
49 s por foco) venía de 2000–3350 tokens de razonamiento, es decir, de la
decodificación. Arreglar la caché baja el costo de entrada, no ese tiempo.

