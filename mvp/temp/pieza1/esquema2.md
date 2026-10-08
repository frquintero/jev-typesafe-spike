# Esquema 2 — CANDIDATO (pieza 1 de la MVP)

Estado: **a prueba**, 04-10-2026. Sello en cada archivo: `"esquema": "2-candidato"`.
Si la pieza 1 pasa, se adopta y se lleva a los documentos vivos (con aprobación
de Frat). Hasta entonces convive con lo vigente, como `ficha_v2` con `ficha_v1`.

**Divergencias declaradas** (este esquema difiere de lo vigente y está a prueba):

- `definiciones-del-marco.md`, fila «Tabla de A(Q)»: «Ids: D corpus, K mundo,
  R consulta». Aquí el mundo se nombra **M**.
- `mvp/temp/mesa1/resultado.md`, decisión 7 («K = mundo»): sustituida por la misma
  razón.
- `definiciones-del-marco.md`, parte C (mundo): los documentos vivos llaman
  **mundo del agente** al saber general del LLM. Aquí sigue rotulado
  `orquestador` —`mundo: orquestador` en §2 y en la lista de R de §3— por
  compatibilidad con la pieza 1 en prueba; se renombra al adoptar el esquema.

## 1. Letras: notación e ids

- **Fórmula** `A(Q | K, D; R)`: notación del ensayo, no ids. Ahí **K = el mundo**.
- **Ids de la ficha** (`ficha_v1`): C caso, R relación, **K capa**, D
  determinación, A acción, Q duda. Los datos del documento se citan con su id
  de ficha.
- **Ids del mundo: M** (M1, M2…). Nunca K.
- La pregunta se cita en el campo `pregunta` (Q5, Q6r); el nombre del campo la
  distingue de una duda de la ficha.
- En `caso` puede ir el id de una determinación, como en el ejemplo de
  `ficha_v1` (D4 sobre D2): una determinación también es caso de estudio.
- La voz base del documento (su autor o emisor) **no es una capa**: es
  procedencia del documento. Las capas son atribuciones anidadas («el técnico
  cree que…»).

## 2. Origen de una dependencia

Cada dependencia lleva `origen: documento | mundo`. Si es mundo, además
`mundo: orquestador | código | fuente`:

- **orquestador:** convenciones de lectura y reglas de saber general (p. ej.,
  «un cierre del X al Y deja cerrado el día Y»).
- **código:** cómputo estable (calendario, husos, aritmética). No es fuente:
  siempre admitido, pero se **registra con su versión**, porque si cambia hay
  que poder decir qué se cae.
- **fuente:** datos consultados fuera (API, web, inventario). Llevan fecha de
  consulta.

`tipo: dato | regla`. El verificador de forma reconoce el mundo por `origen`, nunca por la
letra del id.

## 3. R: fuentes admitidas como premisa (lista cerrada)

| valor | D | M orquestador | M fuente | M código |
|---|---|---|---|---|
| `solo el documento` | sí | no | no | sí |
| `sin externas, con el mundo del orquestador` | sí | sí | no | sí |
| `libre` | sí | sí | sí | sí |

## 4. Tabla de A(Q) por pregunta

```
{ "esquema": "2-candidato",
  "pregunta": "Q5", "texto": "…", "R": "<valor de §3>",
  "encabezado": {"caso": "C3", "aspecto": "…", "condiciones": [ … ]},
  "dominio": {"escala": "…", "regla": "…"},
  "dependencias": [ {"id","origen","mundo","tipo","valor","condiciones",
                     "procedencia","radicacion","consulta","version"} ],
  "tablas_esperadas": ["inicial","final"] | ["inicial","final","revisada"],
  "tabla_inicial": {"filas":[…], "conflicto":[], "campo":[], "desenlace":"…"},
  "tabla_final":   { … },
  "tabla_revisada":{ … } }
```

- **Fila:** `posicion · si · estado · ruta`, más la fila `resto` (reglas de la
  mesa 1, que siguen vigentes salvo la 7).
- **Escala:** el aspecto la fija; toda posición se escribe en ella. Fechas
  `d-m-aaaa`.
- **Dependencia:** lleva sus `condiciones` (como en la ficha); `radicacion`
  (lo que está en Zettel) o `consulta` (lo traído de una fuente), d-m-aaaa;
  `version` solo en el mundo del código: la versión real (p. ej., «Python
  3.12, datetime»).
- **`dominio.regla`:** describe las posiciones posibles, no las filas listadas.
- **`ruta`:** conjunto de ids; el orden no importa.
- **`valor` de una dependencia:** `caso · aspecto · valor`, como en la ficha.
- **`condiciones`** del encabezado: solo si la pregunta añade algo al caso y al
  aspecto.
- **`campo`:** solo datos (D, y M de `tipo: dato`), nunca reglas.
- **`dependencias`:** exactamente lo que aparece en alguna ruta.
- **`desenlace`** (por tabla): `cerrada | en conflicto | no establecido | no
  cerrable`. **En conflicto:** dos o más posiciones admisibles sostenidas por
  fuentes que chocan.
- **Revisión o conflicto:** una determinación solo revisa a otra si una regla
  registrada en la ruta dice cuál prevalece. Sin esa regla, es conflicto y se
  muestra.
- **Aparecen distinciones:** filas cuyo `si` es nuevo o cambia. Una fila nueva
  sin `si` es ganancia de sostén.

## 5. Dato derivado (`corpus.jsonl`, una línea por dato)

Tiene la forma de una determinación de la ficha más un bloque de derivación:

```
{ "esquema": "2-candidato",
  "id": "DD1", "caso": "C4", "aspecto": "…", "valor": "…", "unidad": null,
  "condiciones": [ … ], "inferido": true, "respaldo": [ … ],
  "derivacion": { "pregunta": "Q6r", "R": "…", "radicacion": "d-m-aaaa",
                  "dependencias": [ … con valor, origen y versión … ],
                  "rutas": 1, "juicio": null } }
```

`juicio` existe y queda en null en esta pieza (Jev fuera).

## 6. Respuesta al usuario con conflicto

Muestra todas las posiciones admisibles en conflicto, cada una con su
procedencia (oración, o fuente y fecha de consulta), y no elige entre ellas.

## 7. Verificador de forma (lo que hay que ajustar)

Comprueba formato, sintaxis, cálculos y consistencia interna; no juzga si una
ruta sostiene ni si una lectura es correcta. Será `verificar_forma.py`; el
`mvp/temp/mesa1b/validar.py` queda como registro de la mesa.

- R contra la lista cerrada de §3, con la regla de cada modo sobre `origen` y
  `mundo`.
- Mundo por `origen`, no por la letra del id.
- Comparador: normaliza fechas antes de comparar.
- Encabezado y filas: compara también las **condiciones** (hoy
  `mvp/temp/mesa1b/validar.py` solo mira caso y aspecto). Dos filas en
  `conflicto` deben tener las mismas condiciones constitutivas.
- Bitemporal: una M de fuente no puede tener fecha de consulta anterior a un
  hecho pasado que afirma.
- Q6r: recalcula la posición aplicando las reglas M a los valores de la ruta
  (código) y la compara con la tabla.
- Mantenimiento: dado un cambio en una dependencia, dice qué posiciones pierden
  o ganan sostén usando solo `corpus.jsonl`.
- Quitar el aviso que trata toda regla en una ruta de exclusión como posible
  genérico.
