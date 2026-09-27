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
