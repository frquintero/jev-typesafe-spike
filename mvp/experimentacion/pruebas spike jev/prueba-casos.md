# Prueba: ¿el agente eligió los casos que hacen falta?

**Pregunta.** ¿Los casos que el agente encargado consultó son los correctos para responder la
pregunta, comparados con **todos** los del dominio?

**Lo que se mantiene fijo.** El catálogo (los 17 casos del dominio `GENERAL`, tal como el ORQ los
recibió) y la pregunta, literales de la base. El agente encargado no cambia: es la corrida que ya
está.

**Lo que se cambia.** Nada: primera medición (`r1`).

**La vara.** Fijada antes de correr, sobre el Noul (las bandas de siempre): > 0,85 muy seguramente;
0,75–0,85 seguramente; 0,65–0,75 hay bases; 0,30–0,65 no se puede formar el juicio. Y la decisión en
código: `confidence ≥ 0,80` el veredicto se sostiene solo; por debajo, lo mira una persona.

**Lo que se observa.** El grado del caso elegido y la elección contra el catálogo entero.

**El material.** Consulta `q1`, corrida `C000005` (`gpt-6-luna` `low`, plantilla `ORQ` v1, 2 turnos,
1 llamada). Corpus en la versión 5; documentos `sol` (sello `c9c3de7534d3…`) y `aviacion`
(`e546d95e8b13…`); UT vigentes `C000001` y `C000002`; el agente consultó `C000001:U2`
(`consulta_casos`).

**El comando.** Los dos archivos los arma `armar_expediente.py q1` leyendo la base con `mode=ro`; la
llamada, `utiliarios/jev.py correr`.

```bash
python3 "mvp/experimentacion/pruebas spike jev/armar_expediente.py" q1
bash -ic 'python3 utiliarios/jev.py correr \
  "mvp/experimentacion/pruebas spike jev/expediente-q1.json" \
  "mvp/experimentacion/pruebas spike jev/preguntas-q1.json" \
  "mvp/experimentacion/pruebas spike jev/resultados/jev-casos-q1-r1.json"'
```

**El resultado** (`resultados/jev-casos-q1-r1.json`, `jev-1.13.0`, 1.256 tokens de entrada y 75 de
salida, una llamada):

| juicio | forma | salida |
|---|---|---|
| `elegido_1` — «`elegidos[0]` es un caso que permite responder `pregunta`» | Noul | **0,92** — muy seguramente |
| `eleccion` — la elección contra todo el catálogo | Choice | **`correcta`**, confianza 0,93 · reparto `correcta` 0,95 / `sobran` 0,01 / `faltan` 0,02 / `no_sirve` 0,02 |

Las dos por encima del umbral: no piden revisión.

**Lo que no dice.** No dice **de qué oración** sale el sostén ni si la respuesta del ORQ se sostiene
en ese caso; esta prueba juzga la elección, no la respuesta. Y con un solo elegido, `elegido_1` y
`eleccion` son casi la misma afirmación: se separan cuando la corrida consulta dos o más casos
(`q4`) o ninguno (`q2`).
