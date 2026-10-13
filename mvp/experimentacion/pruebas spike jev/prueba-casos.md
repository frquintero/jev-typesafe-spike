# Prueba: ¿el agente eligió los casos que hacen falta?

**Pregunta.** ¿Los casos que el agente encargado consultó son los correctos para responder la
pregunta, comparados con **todos** los del dominio?

**Lo que se mantiene fijo.** El catálogo (los 17 casos del dominio `GENERAL`, tal como el ORQ los
recibió) y la pregunta, literales de la base. El agente encargado no cambia: son corridas que ya
están.

**Lo que se cambia.** Nada del material. `q1` y `q3` son **dos corridas del ORQ de la misma
pregunta** (`C000005` y `C000007`), y el `state` que sale de la base es **idéntico** en las dos
(comprobado con `diff`): misma pregunta, mismos 17 casos, mismo elegido (`C000001:U2`). La segunda
llamada es, entonces, una **réplica de Jev**: sin `temperature`, la estabilidad se mide con réplicas.

**La vara.** Fijada antes de correr, sobre el Noul (las bandas de siempre): > 0,85 muy seguramente;
0,75–0,85 seguramente; 0,65–0,75 hay bases; 0,30–0,65 no se puede formar el juicio. Y la decisión en
código: `confidence ≥ 0,80` el veredicto se sostiene solo; por debajo, lo mira una persona.

**Lo que se observa.** El grado del caso elegido y la elección contra el catálogo entero, y cuánto se
mueve entre réplicas.

**El material.** Corpus en la versión 5; documentos `sol` (sello `c9c3de7534d3…`) y `aviacion`
(`e546d95e8b13…`); UT vigentes `C000001` y `C000002`. Corridas del ORQ: `q1` = `C000005` y `q3` =
`C000007`, las dos `gpt-6-luna` `low`, plantilla `ORQ` v1, 2 turnos, 1 llamada, 1.962 tokens de
entrada; las dos consultaron `C000001:U2`.

**El comando.** Los dos archivos los arma `armar_expediente.py <q>` leyendo la base con `mode=ro`; la
llamada, `utiliarios/jev.py correr`.

```bash
python3 "mvp/experimentacion/pruebas spike jev/armar_expediente.py" q1   # y q3
bash -ic 'python3 utiliarios/jev.py correr \
  "mvp/experimentacion/pruebas spike jev/expediente-<q>.json" \
  "mvp/experimentacion/pruebas spike jev/preguntas-<q>.json" \
  "mvp/experimentacion/pruebas spike jev/resultados/jev-casos-<q>-r1.json"'
```

**Los resultados** (crudos en `resultados/`, `jev-1.13.0`, 1.256 tokens de entrada y 75 de salida por
llamada):

| juicio | forma | `q1` | `q3` |
|---|---|---|---|
| `elegido_1` — «`elegidos[0]` es un caso que permite responder `pregunta`» | Noul | **0,92** | **0,92** |
| `eleccion` — la elección contra todo el catálogo | Choice | **`correcta`** · conf. 0,93 · 0,95 / 0,01 / 0,02 / 0,02 | **`correcta`** · conf. 0,92 · 0,94 / 0,01 / 0,02 / 0,03 |

Las cuatro por encima del umbral: ninguna pide revisión. Con el mismo `state` y los mismos juicios,
el grado del Noul **no se movió** y el reparto del Choice se movió **0,01**: la variación de réplica
que la guía documenta (≈0,01), sin cruzar ningún umbral.

**Lo que no dice.** No dice **de qué oración** sale el sostén ni si la respuesta del ORQ se sostiene
en ese caso; esta prueba juzga la elección, no la respuesta. Y con un solo elegido, `elegido_1` y
`eleccion` son casi la misma afirmación: se separan cuando la corrida consulta dos o más casos
(`q4`) o ninguno (`q2` — y ahí el molde cambia, porque no hay nada que juzgar como elección).
