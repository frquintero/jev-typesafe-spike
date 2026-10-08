# Mesa 1b — resultado integrado (Cowork)

Fecha: 2026-10-04. Repetición de la mesa 1 con las reglas adoptadas
(`mvp/temp/mesa1/resultado.md`, «Decisiones tras la revisión»). DeepSeek (misma
sesión de la mesa 1) escribió `documento.md` (aviso del Club de Montaña Peña
Alta), `preguntas.md`, `tablas_ds.json`, `validar.py` ajustado y
`reporte_ds.md`. Cowork llenó `tablas_cowork.json` por separado.

## Resultado

**Las tablas convergen.** Q1, Q2, Q3 y Q5 tienen filas idénticas en los dos
juegos (posiciones, estados, rutas y conflicto). Q4 tiene la misma estructura
(dos ramas con `si`, resto admisible sin sostén: la regla de los genéricos se
sostuvo con un caso limpio). Solo Q6 difiere en sustancia. El comparador,
ahora más estricto (mira también dependencias, campo, conflicto y
desenlace), cuenta 34 diferencias, pero casi todas son de formato. No es
comparable con las 18 de la mesa 1, que solo miraban las filas.

| Diferencia | Dónde | Regla que falta |
|---|---|---|
| Redacción del `valor` (frase frente a «caso · aspecto · valor») | todas | El valor se escribe como en la ficha: caso · aspecto · valor. |
| `condiciones` repite el caso | todas (DeepSeek) | Condiciones solo si la pregunta añade algo al caso y al aspecto. |
| «1 de noviembre de 2026» frente a «1-11-2026» | Q6 | Las fechas se escriben d-m-aaaa (regla de escala). |
| `campo` incluye una regla (K1) | Q4 (DeepSeek) | `campo` lista datos, no reglas. |
| `desenlace` «cerrada» frente a «en conflicto» | Q5, Q6 | Falta el desenlace **en conflicto**: dos posiciones admisibles sostenidas por fuentes que chocan. DeepSeek dudó en lo mismo. |
| Q6: revisión frente a conflicto | Q6 | Ver abajo. |
| Q6: ruta [D2] frente a [D0, D2, K4] | Q6 | La regla «un cierre del X al Y reabre el día Y + 1» y el año (D0) fijan la posición: van en la ruta (regla 4 de la mesa 1). |

**Q6, el punto de fondo.** DeepSeek trató la premisa simulada K3 («la
clausura se levantó el 18-10») como una revisión que invalida D2 (el cierre
del 15 al 31): el 18-10 vuelve a ser admisible y el 1-11 deja de serlo. Yo la
traté como conflicto: las dos admisibles, `conflicto: [D2, K3]`. Propuesta de
regla, desde el ensayo (l. 239, el sensor defectuoso): una determinación
nueva solo revisa otra si queda establecido que compromete su ruta, y eso
exige una regla registrada (por ejemplo, «un hecho posterior prevalece sobre
el anuncio de un plan»). Sin esa regla en la ruta, dos fuentes que chocan son
un conflicto y se muestran. Las dos lecturas prueban lo que Q6 debía probar:
el 18-10 pasa de inadmisible a admisible en ambas.

**Un hallazgo que nadie buscó.** K3 está fechada como consultada el 2-10-2026
y afirma un hecho del 18-10-2026: una fuente no puede informar el 2-10 de algo
que ocurrió el 18-10. Es incoherencia bitemporal (tiempo de consulta anterior
al tiempo de validez de un hecho pasado), y el validador podría detectarla.

**Las dudas de DeepSeek** (`reporte_ds.md`) coinciden con lo anterior en Q5 y
Q6. Sobre Q4: el `si` que separa las ramas es justamente lo que se pregunta
al usuario, y está bien que así sea. Sobre Q1 y Q3: el validador cuenta como
«distinción» una fila única que cierra la pregunta; tiene razón en que no lo
es.

## Para decidir

1. Desenlace **en conflicto**.
2. Revisión solo con una regla registrada que diga qué fuente compromete a
   cuál; sin ella, conflicto.
3. «Aparecen distinciones» = filas cuyo `si` es nuevo o cambia; una fila
   nueva sin `si` es ganancia de sostén.
4. Formato: valor «caso · aspecto · valor»; condiciones solo si añaden;
   fechas d-m-aaaa; `campo` solo con datos.
5. Validador: chequeo bitemporal (consulta anterior a un hecho pasado que la
   fuente afirma) y quitar el aviso que trata toda regla en una ruta de
   exclusión como posible genérico.

Con eso el esquema queda listo para la mesa 2 (DeepSeek llena las tablas por
API y el validador es el criterio).
