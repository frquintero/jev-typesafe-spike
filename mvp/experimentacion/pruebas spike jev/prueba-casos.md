# Prueba: ¿el agente eligió los casos que hacen falta?

**Pregunta.** ¿Los casos que el agente encargado consultó son los correctos para responder la
pregunta, comparados con **todos** los del dominio?

**Lo que se mantiene fijo.** El catálogo (los 17 casos del dominio `GENERAL`, tal como el ORQ los
recibió) y la pregunta, literales de la base. El agente encargado no cambia: son corridas que ya
están.

**Lo que se cambia.** Nada entre `q1` y `q3`: son **dos corridas del ORQ de la misma pregunta**
(`C000005` y `C000007`) y el `state` que sale de la base es **idéntico** (comprobado con `diff`), así
que la segunda es una **réplica de Jev** —sin `temperature`, la estabilidad se mide con réplicas—.
`q4` sí cambia el material: es otra corrida de la misma pregunta (`C000008`, `deepseek-flash`), con
**dos** casos consultados en vez de uno.

**La vara.** Fijada antes de correr, sobre el Noul (las bandas de siempre): > 0,85 muy seguramente;
0,75–0,85 seguramente; 0,65–0,75 hay bases; **0,30–0,65 no se puede formar el juicio** (señal de
diseño, no duda de Jev). Y la decisión en código: `confidence ≥ 0,80` el veredicto se sostiene solo;
por debajo, lo mira una persona.

**Lo que se observa.** El grado de cada caso elegido, la elección contra el catálogo entero, y cuánto
se mueve entre réplicas.

**El material.** Corpus en la versión 5; documentos `sol` (sello `c9c3de7534d3…`) y `aviacion`
(`e546d95e8b13…`); UT vigentes `C000001` y `C000002`. Corridas del ORQ: `q1` = `C000005` y `q3` =
`C000007` (`gpt-6-luna` `low`, 2 turnos, 1 llamada, 1.962 tokens), las dos consultaron `C000001:U2`;
`q4` = `C000008` (`deepseek-flash` `low`, 2 turnos, 2 llamadas, 3.092 tokens), consultó
`C000001:U2` y después `C000001:U1`.

**El comando.** Los dos archivos los arma `armar_expediente.py <q>` leyendo la base con `mode=ro`; la
llamada, `utiliarios/jev.py correr`.

```bash
python3 "mvp/experimentacion/pruebas spike jev/armar_expediente.py" q1   # y q3, q4
bash -ic 'python3 utiliarios/jev.py correr \
  "mvp/experimentacion/pruebas spike jev/expediente-<q>.json" \
  "mvp/experimentacion/pruebas spike jev/preguntas-<q>.json" \
  "mvp/experimentacion/pruebas spike jev/resultados/jev-casos-<q>-r1.json"'
```

**Los resultados** (crudos en `resultados/`, `jev-1.13.0`):

| juicio | forma | `q1` | `q3` | `q4` |
|---|---|---|---|---|
| `elegido_1` — «`elegidos[0]` es un caso que permite responder `pregunta`» | Noul | **0,92** | **0,92** | **0,91** |
| `elegido_2` — «`elegidos[1]`…» | Noul | — | — | **0,47** |
| `eleccion` — la elección contra el catálogo | Choice | `correcta` · conf. 0,93 · 0,95/0,01/0,02/0,02 | `correcta` · conf. 0,92 · 0,94/0,01/0,02/0,03 | **`sobran`** · conf. **0,44** · 0,40/**0,58**/0,01/0,01 |
| tokens de entrada / salida | | 1.256 / 75 | 1.256 / 75 | 1.356 / 94 |

**Lo que dicen las tres.**

- `q1` y `q3`: la elección es correcta, con el Noul en 0,92 y el reparto concentrado. Réplica: el
  Noul no se movió y el reparto se movió 0,01 (la variación que la guía documenta para réplicas).
- `q4` **separa los dos casos**: `C000001:U2` (el primero que pidió) en **0,91**; `C000001:U1` en
  **0,47**, o sea **en la franja central** —«no se puede formar el juicio con este expediente»—. Y la
  elección sale **`sobran`** con **confianza 0,44**: por debajo del umbral de 0,80, así que **va a
  revisión**.
- La franja central del segundo Noul es, según la guía, **señal de diseño antes que veredicto**: o el
  juicio está mal formulado para ese caso (un caso «sobre el Sol» que no trata lo que la pregunta
  pide), o el caso es marginal. No es un «no»: un grado bajo no dice por qué.
- La `eleccion` de `q4` tiene el reparto casi plano (`correcta` 0,40 contra `sobran` 0,58), y eso es
  lo que la confianza 0,44 está diciendo: **no la uses sin mirarla**.

**Lo que no dice.** No dice **de qué oración** sale el sostén ni si la respuesta del ORQ se sostiene
en los casos leídos; esta prueba juzga la elección, no la respuesta. Con un solo elegido,
`elegido_1` y `eleccion` dicen casi lo mismo —se separan con `q4`—; y con ninguno (`q2`) el molde
cambia, porque no hay elección que juzgar.
