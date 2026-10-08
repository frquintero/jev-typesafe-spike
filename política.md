# Política del repo

Reglas de casa: **qué se actualiza y cuándo**, y **dónde vive cada archivo**. Lo
operativo (comandos, claves, modelos, reportes) está en `AGENTS.md`.

## 1. Política de actualización

**El mismo hecho vive en tres sitios, en el mismo commit:**

| Sitio | Qué lleva |
|---|---|
| `README.md`, «Proyectos en curso» | la lista de proyectos que se trabajan, una línea por proyecto («Fecha: AAAA-MM-DD · Proyecto: … (carpeta)»). Solo referencia, no bitácora. |
| `AGENTS.md`, «Mapa del repo» | qué hay en cada carpeta y en qué estado. |
| `mvp/memoria de trabajo y pendientes.md`, «Dónde quedamos» | el estado vigente y lo que sigue. Fuente única del estado. |

- **Cuándo:** al abrir un proyecto o una línea de trabajo, al cerrarlo o
  suspenderlo, y cada vez que cambia el paso que se está dando.
- **La fecha del encabezado de la memoria** se actualiza con «Dónde quedamos».
- **Los «siguiente» de los tres sitios tienen que decir lo mismo.** Si uno cambia
  de paso, se corrigen los tres; el desajuste entre ellos ya obligó a corregir dos
  veces.
- **El detalle de cada ronda no va a los tres sitios:** vive en el `PLAN.md` o
  `README.md` del proyecto, y los tres sitios solo lo apuntan.
- **Proyecto cerrado o suspendido:** sale de la lista del `README.md`; su carpeta y
  su `PLAN.md` se conservan como antecedente.
- **Nada de duplicar el estado** en otros archivos: si un dato de estado aparece en
  otro sitio, es una copia que hay que quitar.

## 2. Política de ubicación

**Raíz.** Solo los documentos de navegación y vocabulario:

`README.md` · `AGENTS.md` · `CLAUDE.md` · `política.md` ·
`definiciones-del-marco.md` · `zettel-vision-operativa.md`

**El estado vive con su proyecto:** la memoria, en `mvp/memoria de trabajo y pendientes.md`.

Cualquier otro documento va a `otros documentos/`. Las carpetas de proyecto
(`unidades/`, `mvp/`, `prototipos/`, `niveles/`, `probes/`, `cutoff-spike/`,
`notebooklm-spike/`, `nblm-grafo-semantico/`, `langextract-spike/`,
`marco filosófico/`, `historico/`, `deleted/`) se quedan donde están.

**`otros documentos/`.** Documentos de referencia que no son de navegación:
vocabulario de Jev (`diccionario.md`, `jev_typesafe_guia_pedagogica_v2.md`),
la política de agentes delegados (`agentes-delegados.md`) e informes sueltos (una
verificación, un análisis de un proveedor). Si uno pasa a ser un frente de trabajo, se
le da carpeta propia y entra en los tres sitios.

- **`agentes-delegados.md` es una copia**, traída el 06-10-2026 del original que vive
  en `~/Claude-memoria/memoria/agentes-delegados.md`; para Claude y ChatGPT manda el
  original. La copia lleva al principio la nota de qué se ajustó aquí (§1: delega el
  ORQUESTADOR que designe Frat). Si cambia el original, se vuelve a copiar y se
  reaplica ese ajuste.

**`utiliarios/`.** Los guiones que se invocan desde la raíz: `dsh_tarea.sh`,
`muse_tarea.sh`, `proxy_local.py` (retirado, se conserva como antecedente) y
`configurar_clave_xai.sh`. Se invocan como `./utiliarios/<guion>` desde la raíz.

- **Regla para un guion que viva ahí:** el repo se resuelve como
  `"$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"` (el padre de `utiliarios/`),
  nunca como el directorio del propio guion.
- Los guiones de un proyecto se quedan en su carpeta (`mvp/código/paso1_unidades.py`).

**Documentos vivos (no se editan sin aprobación de Frat):** los siete de la raíz y,
en `otros documentos/`, `diccionario.md` y `jev_typesafe_guia_pedagogica_v2.md`.

## 3. Cada commit local se sube

- **Todo commit local se lleva al upstream en el mismo tramo de trabajo:** `main`
  sigue a `origin/main` (`https://github.com/frquintero/jev-typesafe-spike.git`) y no
  se deja el repo local adelantado. Terminar con commits sin subir es dejar la tarea
  a medias.
- La copia de GitHub es de donde se recupera el trabajo desde otro sitio (ChatGPT
  Work lee `main` sin el PC): **un commit que solo existe en el PC no está
  publicado.**
- **Si el push falla** (red, credenciales): detenerse y reportar. No se busca otra
  vía para publicar, y no se reescribe la historia publicada (`push --force` sobre
  `main` no se usa).
- **Si `origin/main` va por delante:** traerlo antes de seguir y decir en el reporte
  qué traía. El trabajo se hace sobre `main`, no sobre ramas sueltas.
- El push va en el mismo commit que el trabajo: crudos, resultados y la
  actualización de estado de los tres sitios.

## 4. Reportes

- Prompts y campos enviados, **verbatim** (regla 22); el JSON `parsed` tal como llegó
  y el crudo detrás de cada afirmación.
- **Sin veredicto** (regla 15); sin mecanismos inventados para un grado concreto
  (regla 26); solo documentos sintéticos (regla 20).

## 5. Cuando algo se mueve

1. `git mv` (conserva la historia), nunca copiar y dejar el original.
2. **Buscar y actualizar todas las referencias** antes de commitear:
   `git grep -n -F "<nombre viejo>" -- '*.md' '*.sh' '*.py'`.
3. Si el archivo movido es un guion, revisar los supuestos de ruta que traía.
4. Lo que **no** se reescribe: los registros históricos (`historico/`, `deleted/`,
   los `PLAN.md` de líneas inactivas y las narraciones de corridas pasadas)
   conservan la redacción de su momento. Las instrucciones vigentes sí se
   actualizan.
5. Verificar al final: en la raíz solo los siete documentos; ningún enlace roto; el
   guion movido arranca (`bash -n` y una invocación sin argumentos).
