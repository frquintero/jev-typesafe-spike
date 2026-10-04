# Mesa 1 — resultado integrado (Cowork)

Fecha: 2026-10-04. Prueba de mesa del esquema de la tabla de A(Q), sin API de
modelos. DeepSeek (dsh, sesión nueva, 185 s) escribió `documento.md`,
`preguntas.md`, `tablas_ds.json`, `validar.py` y `reporte_ds.md`. Cowork llenó
`tablas_cowork.json` por separado, leyendo solo el documento y las preguntas.

## Qué se probó

1. Que el **diff de tablas decida el efecto**.
2. Que el esquema (posicion · si · estado · ruta) **no sea ambiguo**: dos
   lectores llenándolo por separado deberían coincidir.

## Resultado

**1. El diff decide el efecto: sí.** En los dos juegos, P2 da diff vacío
(«el documento no lo establece») y P1, P3 y P4 dan efecto. El validador pasa
ambos con 0 errores. La P2, el discriminador, funciona.

**2. El esquema todavía es ambiguo: 18 celdas distintas**
(`python3 validar.py --comparar tablas_ds.json tablas_cowork.json`). Ninguna
contradice el marco; todas señalan una regla que falta.

| # | Dónde | Qué difiere | Regla que falta |
|---|---|---|---|
| 1 | P1, P4 | «8 000» frente a «8 000 kg»; «3» frente a «3 ha» | La posición se escribe con su escala o unidad (marca ≠ posición, A.4). |
| 2 | encabezados | qué va en caso, aspecto y condiciones (texto libre) | El caso se cita por su id de la ficha; el aspecto lleva la unidad; condiciones solo si la pregunta las fija. |
| 3 | P3, fila «resto» | DeepSeek: admisible sin ruta; Cowork: inadmisible por D3, K1, K2 | Una regla genérica («suele») sostiene pero no excluye: el resto sigue admisible. Aquí acierta DeepSeek; mi tabla excluía de más. |
| 4 | P3, filas | DeepSeek: quincenas por «año cálido/frío» con ruta [D3]; Cowork: intervalos por hemisferio con ruta [D1, D3, K1/K2] | Todo saber del mundo que fija una posición entra como dependencia. La ruta [D3] sola no establece «primera quincena de septiembre»: la premisa usada no quedó registrada. |
| 5 | P4, revisada | DeepSeek: 3 y 2,5 admisibles sin `si`; Cowork: con `si` «el aviso es correcto» / «el catastro es correcto» | El conflicto se registra con `si` sobre la fuente. Sin eso, el diff no muestra que «3» pierde sostén: el conflicto queda invisible. |
| 6 | P2, dependencias | DeepSeek lista D5 (mudo); Cowork, ninguna | `dependencias` = solo lo que aparece en alguna ruta. (El comparador no revisa dependencias: no lo detectó.) |

## Lo que la mesa enseñó además

- **Falta un modo en el diff.** En P4, «2,5» pasa de inadmisible (en el
  resto) a admisible, y el validador lo clasifica como «distinción». Es
  otra cosa: una respuesta que **vuelve a ser admisible** (el sensor
  defectuoso del ensayo, l. 287). El primer modo debería ser «cambian de
  estado», en los dos sentidos.
- **El validador revisa la forma, no la suficiencia.** Comprueba que los ids
  de la ruta existan, pero no que la ruta baste para establecer la
  posición (fila 4 de la tabla). Eso es un juicio, no un cómputo, y es un
  lugar natural para Jev: «la ruta [ids] establece la posición p bajo el
  supuesto s». Conjetura, sin probar.
- **«¿Cuándo?» admite dos dominios.** La respuesta directa del documento es
  un evento («cuando la uva alcance 22 °Bx»); en fechas hace falta el mundo.
  La pregunta estructurada debe fijar cuál.

## Para decidir

1. Adoptar las seis reglas de la tabla y el modo «cambian de estado».
2. Ajustar `validar.py`: ese modo, y que `--comparar` incluya dependencias.
3. Si se adoptan, repetir la mesa 1 con un documento nuevo (otro par de
   tablas por separado) antes de la mesa 2 con DeepSeek llenando el esquema.
