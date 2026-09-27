# Píldoras

Términos técnicos y filosóficos que aparecieron en la planeación del spike, en
breve, con el contexto en que surgieron. Se agregan a medida que aparecen.

## Índice

1. [MeasEval: entidad, propiedad, cantidad y calificador](#1-measeval-entidad-propiedad-cantidad-y-calificador)
2. [Definición ostensiva](#2-definición-ostensiva)
3. [Niveles de medición de Stevens](#3-niveles-de-medición-de-stevens)
4. [Magnitudes de dimensión uno](#4-magnitudes-de-dimensión-uno)
5. [Símbolos de unidades sin plural](#5-símbolos-de-unidades-sin-plural)
6. [Magnitud individual y magnitud general](#6-magnitud-individual-y-magnitud-general)
7. [Modelo y aplicación (arnés)](#7-modelo-y-aplicación-arnés)
8. [AGENTS.md](#8-agentsmd)
9. [Guías de anotación](#9-guías-de-anotación)
10. [Muestreo por diversidad](#10-muestreo-por-diversidad)
11. [Ejemplo prototípico o medoide](#11-ejemplo-prototípico-o-medoide)
12. [Aprendizaje por *near miss* (ejemplos contrastivos)](#12-aprendizaje-por-near-miss-ejemplos-contrastivos)
13. [Los ejemplares de Kuhn](#13-los-ejemplares-de-kuhn)
14. [Conjunto de desarrollo y conjunto de prueba reservado](#14-conjunto-de-desarrollo-y-conjunto-de-prueba-reservado)
15. [Cómputo en tiempo de inferencia y rendimientos decrecientes](#15-cómputo-en-tiempo-de-inferencia-y-rendimientos-decrecientes)
16. [Entidad medida y propiedad medida](#16-entidad-medida-y-propiedad-medida)
17. [Atributo implícito](#17-atributo-implícito)
18. [Paráfrasis y canonicalización](#18-paráfrasis-y-canonicalización)

---

## 1. MeasEval: entidad, propiedad, cantidad y calificador

**Qué es.** Tarea de evaluación (SemEval-2021, tarea 8) para extraer mediciones
de textos científicos. Anota cuatro piezas: la cantidad (*quantity*), la
entidad medida (*measured entity*), la propiedad medida (*measured property*)
y el calificador (*qualifier*, las condiciones de la medición).

**Contexto.** Revisión de literatura antes de DU4: sus cuatro piezas
corresponden casi una a una a valor, caso, variable y condiciones del ensayo
«¿Qué es un dato?», y sus reglas dicen dónde termina la entidad medida
(el problema de los modificadores del nombre).

## 2. Definición ostensiva

**Qué es.** Enseñar un concepto señalando ejemplos en vez de definirlo.
Wittgenstein (*Investigaciones filosóficas*, §28) mostró su límite: al
señalar un ejemplo no queda claro qué rasgo se señala (¿la forma, el color,
el número?).

**Contexto.** Al pasar de definiciones a ejemplos (DU5). Por eso los ejemplos
tienen que contrastar entre sí; si todos traen cifras con unidad, el modelo
puede aprender «dato = número». En DU5 cada falla correspondió a un rasgo que
los ejemplos no mostraban: la ostensión enseña exactamente lo que muestra.

## 3. Niveles de medición de Stevens

**Qué es.** La tipología de S. S. Stevens (1946): escalas nominal, ordinal, de
intervalo y de razón. Es el sentido más frecuente de «escala» en estadística.

**Contexto.** DU4: con la definición de valor «cuantitativo o cualitativo
(nominal u ordinal)», Grok llenó el campo `escala` con «nominal» y «ordinal», y
todo adjetivo cabía en alguna. De ahí la decisión de cambiar `escala` por
`unidad_de_medida`: una palabra polisémica arrastra al modelo a su sentido más
frecuente.

## 4. Magnitudes de dimensión uno

**Qué es.** En el Vocabulario Internacional de Metrología (VIM), los conteos
son magnitudes de dimensión uno: su unidad es el uno, no «veces» ni «piezas».

**Contexto.** Decisión sobre «dos veces» (ut2): la unidad de medida es
«unidad»; «veces» dice qué se cuenta y va en la variable (número de
arranques).

## 5. Símbolos de unidades sin plural

**Qué es.** En el Sistema Internacional, los símbolos de las unidades no llevan
plural ni punto: «12 kg», no «12 kgs».

**Contexto.** Decisión sobre «caja de 12 kg»: valor 12, unidad kg.

## 6. Magnitud individual y magnitud general

**Qué es.** El VIM distingue la magnitud general («longitud», «peso») de la
magnitud individual («el radio del círculo A», «el peso de esta caja»). Lo que
se mide, el mensurando, es siempre una magnitud individual. VIM4, nota 2:
*«the radius of circle a is an instance of length»*.

**Contexto.** Frat propuso que la variable sea «peso de la caja» y no «peso»
con un caso aparte. Respalda quitar el campo `caso`: la variable ya trae la
pregunta completa `variable(caso) = ?`. La mirada estadística (variable =
columna, caso = fila) es la de la tabla, no la de la medición.

## 7. Modelo y aplicación (arnés)

**Qué es.** Un modelo (GPT-6 Luna, Grok 4.7) no decide qué archivos lee al
empezar; lo decide la aplicación que lo envuelve (Codex, ChatGPT, Muse Code),
a veces llamada arnés (*harness*).

**Contexto.** Luna respondió que no podía garantizar leer `AGENTS.md` al
iniciar. Es cierto del modelo; Codex sí lo carga solo, y en el chat se le pide
en la primera línea de cada mensaje.

## 8. AGENTS.md

**Qué es.** Estándar abierto de un archivo de instrucciones para agentes de
código, en la raíz del repositorio. Nació entre Codex, Amp, Jules, Cursor y
Factory; hoy lo mantiene la Agentic AI Foundation (Linux Foundation). Codex lo
busca desde la raíz del repositorio hasta la carpeta actual.

**Contexto.** El mismo caso de Luna: por qué un solo `AGENTS.md` sirve para
Muse, Codex y Claude Code (este último vía `CLAUDE.md` → `@AGENTS.md`).

## 9. Guías de anotación

**Qué es.** Las instrucciones escritas que definen cada categoría, con sus
casos límite y excepciones, para anotadores humanos. En extracción con LLM,
GoLLIE (ICLR 2024) mostró que las guías detalladas mejoran la extracción;
GuideNER (AAAI 2025), que guías concisas pueden rendir más que ejemplos.

**Contexto.** Diseño de `datos_u6`: definiciones cortas, con las mismas
palabras de los ejemplos, más ejemplos. Las definiciones largas y ambiguas de
DU2–DU4 habían empeorado los resultados.

## 10. Muestreo por diversidad

**Qué es.** Elegir los ejemplos de un prompt de modo que cubran regiones
distintas del espacio de casos, en vez de al azar. Los estudios sobre qué
ejemplos anotar para aprendizaje en contexto encuentran que mejora el
rendimiento de conjunto.

**Contexto.** Cómo escoger los cinco ejemplos de `datos_u6`: cada uno agrupa
formas de dato que ningún otro cubre.

## 11. Ejemplo prototípico o medoide

**Qué es.** El caso real que queda en el centro de un grupo de casos parecidos
y lo representa. En estadística, el medoide (a diferencia de la media, es un
caso que existe). Se emparienta con los prototipos de Eleanor Rosch.

**Contexto.** Nombre técnico de lo que Frat llamó «ejemplo nodo»: ejemplos que
cobijan a su alrededor muchos casos generales, más sus casos límite.

## 12. Aprendizaje por *near miss* (ejemplos contrastivos)

**Qué es.** Patrick Winston (1970): un concepto se aprende mejor viendo lo que
casi es y no es. En prompts, los ejemplos contrastivos o negativos difíciles
reducen los errores de frontera.

**Contexto.** Diseño de los nodos de `datos_u6`: cada uno lleva un casi-dato
junto a los datos («certificado» junto a «acidez alta», «antiguo muelle» junto
a «contenedor de 800 kg»).

## 13. Los ejemplares de Kuhn

**Qué es.** En la posdata de 1969 a *La estructura de las revoluciones
científicas*, Kuhn sostiene que los científicos aprenden un paradigma por
ejemplares (problemas resueltos), no por reglas. Emparentado con el parecido
de familia de Wittgenstein.

**Contexto.** Por qué definiciones cortas + ejemplos nodo: las definiciones
hacen de guía, los ejemplares de práctica.

## 14. Conjunto de desarrollo y conjunto de prueba reservado

**Qué es.** El conjunto de desarrollo es el que se mira mientras se diseña; el
conjunto de prueba reservado (*held-out*) no se toca hasta medir. Lo que se
miró al diseñar ya no sirve para medir con honestidad.

**Contexto.** ut1–ut5 pasaron a ser conjunto de desarrollo al discutir sus
fallas; el ~90 % que busca Frat se mide en unidades nuevas.

## 15. Cómputo en tiempo de inferencia y rendimientos decrecientes

**Qué es.** *Test-time compute*: gastar más cálculo al responder (más tokens de
razonamiento) en lugar de al entrenar. Su curva típica es de rendimientos
decrecientes: los primeros tokens rinden mucho y los siguientes cada vez menos.

**Contexto.** Pregunta de Frat por el `reasoning_effort` de Grok. En Grok 4.6
(Artificial Analysis): low 35, medium 43, high 44, xhigh 44 en el índice de
inteligencia; el salto grande es de low a medium. En tareas cortas como la
nuestra, más razonamiento puede no servir (DU4: 3250 tokens, peor resultado).

## 16. Entidad medida y propiedad medida

**Qué es.** En MeasEval (píldora 1), la entidad medida es lo que tiene la
propiedad (la tos) y la propiedad medida es lo que se mide de ella (el tipo).

**Contexto.** DU6: en ut5 la variable nombraba la entidad sin la propiedad
(«tos» = seca, «dolor abdominal» = moderado). La variable debe llevar las dos.

## 17. Atributo implícito

**Qué es.** En la extracción de atributos, el caso en que el valor está en el
texto pero el nombre del atributo no: en «camisa roja», «color» nunca se dice.
Hay trabajos dedicados a ese problema (ImplicitAVE, 2024).

**Contexto.** Corrección de DU6 a DU7: un ajuste al nodo de cualidades («grano
grande» → «tamaño del grano», «tueste oscuro» → «grado de tueste») y la frase
«Si `texto` no nombra el aspecto, la variable lo nombra».

## 18. Paráfrasis y canonicalización

**Qué es.** La paráfrasis es la variación léxica (lo mismo dicho con otras
palabras), distinta de la semántica (cosas distintas). Canonicalizar es
reducir las paráfrasis a una forma única.

**Contexto.** DU7: la única variación entre tres réplicas fue «temperatura del
termostato» / «temperatura marcada por el termostato». Para comparar variables
entre textos hará falta canonicalizar; es un juicio que Jev puede sopesar
(«estas dos variables nombran la misma magnitud»).
