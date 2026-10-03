# Informe para Cowork — `definiciones-del-marco.md` y su relación con el disco

**Fecha:** 2026-10-03. **Autor:** ejecutor (DeepSeek-V41-Flash), por encargo de
Frat. **Sin veredicto** (regla 15): son cuatro observaciones con la evidencia
detrás y opciones para decidir, no recomendaciones. Este informe no modifica
ningún documento del repo.

## Qué leí y cómo

- `definiciones-del-marco.md` completo (207 líneas; commit `9591226`).
- `marco filosófico/Que es un dato - 2026-09-30.md` (317 líneas): contrasté una
  por una las referencias de la parte A.
- `memoria de trabajo y pendientes.md` (§1, §2.1, §2.2, §5), `README.md`
  («Visión», «Estado actual», «Dónde está cada cosa») y `AGENTS.md`.
- Prompts: `ficha_v1.md`, `ficha_v2.md`, `unidades_v1.md`, `unidades_v5.md`;
  `unidades/PLAN.md` (U6, ENC4).

## Comprobaciones hechas, sin hallazgos

1. **Las líneas de la parte A son correctas.** Cada referencia (l. …) apunta al
   pasaje que cita; no encontré ninguna desviada ni ninguna cita deformada.
2. **No hay contradicción con la memoria §2.** Comparé los términos que
   aparecen en ambos (caso, caso de estudio, aspecto, variable, marca, marca de
   posición, marca ≠ posición ≠ valor, las tres condiciones, dato, información,
   campo `valor`) y coinciden.
3. **La reserva anterior queda cerrada.** `memoria…:56` dice: «Referencia
   completa, con líneas del ensayo y definiciones operativas:
   `definiciones-del-marco.md` (raíz). **Lo de abajo es el resumen de
   trabajo**.» El reparto documento = referencia / memoria = resumen de trabajo
   está declarado; no hay dos autoridades en conflicto.

## Observación 1 — La regla de la parte A frente a los bloques DEFINICIONES de los prompts

**Dice el documento** (`definiciones-del-marco.md:17-18`):

> «Ningún prompt ni plan redefine un término de la parte A. Si una ronda
> necesita otro uso, se agrega o corrige en la parte B, con fecha.»

**Muestra el disco:**

- `unidades/prompts/ficha_v2.md:7-22` trae un bloque DEFINICIONES con **Caso de
  estudio, Aspecto, Determinación, Condición, Capa y Marca de posición**.
  `ficha_v1.md` es idéntico en esas líneas (verificado: líneas 1–23 idénticas
  entre v1 y v2; el diff solo toca el principio 12 y el contrato de `capas`).
- De esos términos, `Capa` y `Marca de posición` ya están en B (`:186`, `:189`)
  y el uso de `valor` también (`:185`), pero **Caso de estudio, Aspecto,
  Determinación y Condición no figuran en B**.
- La definición de caso del prompt no coincide con la que B registra:
  - B `:182` (palabras de `unidades_v1`): «La unidad concreta, no una clase,
    que queda distinguida en `texto` y acerca de la cual `texto` dice algo. Es
    la misma unidad aunque `texto` la nombre de varias maneras o con
    pronombres.»
  - `ficha_v2.md:7-9`: «Caso de estudio: aquello de lo que el texto dice algo
    (una cosa, persona, lugar, hecho, estado, o incluso otra determinación). Se
    reconoce por sus menciones: nombre, pronombre, sujeto implícito.»
  - Diferencia concreta: el prompt admite «otra determinación» como caso y fija
    el reconocimiento por menciones; B insiste en «no una clase» y en la
    reidentificación a través de nombres y pronombres.
- La `Condición` del prompt (`ficha_v2.md:15-17`) es solo la **constitutiva**
  («si cambiara, cambiaría la pregunta respondida»); A.5 (`:93-100`) registra
  tres clases (constitutivas, de representación, de procedencia).
- Otros prompts con bloque DEFINICIONES: `unidades_v5.md:4-10` (Oración,
  Subtema, Desarrollo, Nombre del subtema), los `datos_p*` y
  `unidades_v1/v3/v4`. Los de subtema no son términos de A; el de `Oración` sí
  está en B (`:181`) y coincide.

**Opciones (a decidir por Frat y Cowork):** (a) registrar en B el uso de cada
término tal como está en el prompt, con fecha y versión; (b) que los prompts
remitan al documento en vez de definir; (c) dejar en los prompts solo los
términos que no son de la parte A.

## Observación 2 — Unidad temática: decisión registrada vs. artefacto en disco

**Dice el documento** (`:183`): la definición de `unidades_v1`/`v2` «**vuelve a
regir por decisión de Frat, 02-10** (`v3`–`v5` habían cambiado el eje al
asunto)».

**Muestra el disco:**

- El eje de v1 está en `unidades/prompts/unidades_v1.md:8-15`: «Unidad temática:
  un núcleo, sus satélites y todas las oraciones de `texto` que se refieren a
  ellos»; reglas de núcleo/satélite y unicidad de satélite.
- El prompt que el repo usa y documenta sigue siendo `unidades_v5`, con eje de
  **asunto**: `unidades/prompts/unidades_v5.md:6-10` («Subtema: un asunto
  nuclear y su desarrollo…», «lo que las une es el asunto»).
- `unidades/PLAN.md` sigue describiendo v5: ronda U6 (`:516`, «nombres de
  subtema como asuntos») y ENC4 (`:541-545`, cadena con `unidades_v5`).

**Opciones:** escribir el prompt que implemente el eje v1 y decidir si
reemplaza a `unidades_v5` en `extraer_unidades.py`; o dejar anotado en B que la
decisión está registrada pero el artefacto todavía no la implementa.

## Observación 3 — El pendiente 7 de la memoria se lee como abierto

`memoria de trabajo y pendientes.md:179` sigue en **«5. Pendientes vigentes»**.
El encabezado dice «Documento de definiciones (pedido de Frat, 02-10) —
**primera versión hecha: `definiciones-del-marco.md`**», pero el cuerpo conserva
el imperativo original: «crear en la raíz del repo un documento que mantenga las
definiciones…».

**Opciones:** sacarlo de pendientes, o reescribir el cuerpo en pasado
señalando qué queda vivo del pedido.

## Observación 4 — «Documento y foco» no están en los homónimos

`memoria…:64`: «Documento y foco **no son conceptos del ensayo**: son
arquitectura de Zettel compatible con él.» La parte C
(`definiciones-del-marco.md:196-204`) recoge Campo, Dominio, Caso, Valor y
Variable, pero **no** Documento ni Foco.

**Opción:** añadirlos a C (o dejar constancia de dónde viven, si su lugar es
otro).

## Anexo — Reparto de las listas operativas

La tabla B tiene 12 términos: Oración · Caso (en los prompts) · Unidad temática
· Ficha · Campo «valor» de la ficha · Capa · Respaldo · Inferido · Marca de
posición · Dudas · «El documento no lo establece» · Recuperar/responder.

- **Solo en B** (no en la tabla de decisiones de la memoria §2.2): Oración,
  Unidad temática, Ficha, Inferido, «El documento no lo establece»,
  Recuperar/responder.
- **Solo en memoria §2.2** (no en B): genéricos/constantes/valoraciones,
  organización desde el caso de estudio, caso-o-condición por «qué cambia»,
  recomendación, comparación, cambios, lo dicho al pasar, `modo`, el papel del
  código (verificador) y las dimensiones de la evaluación.

Ninguna lista contiene a la otra; es coherente con el reparto
referencia/resumen, pero conviene saber que actualizar una no actualiza la otra.
