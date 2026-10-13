# Prueba: ¿el agente eligió los casos que hacen falta?

**Pregunta.** ¿Los casos que el agente encargado consultó son los correctos para responder la
pregunta, comparados con **todos** los del dominio?

**Lo que se mantiene fijo.** El catálogo (los 17 casos del dominio `GENERAL`, tal como el ORQ los
recibió) y la pregunta, literales de la base. El agente encargado no cambia: son corridas que ya
están.

**Lo que se cambia.**

- `q1` y `q3`: **nada**. Son dos corridas del ORQ de la misma pregunta (`C000005` y `C000007`) y el
  `state` que sale de la base es **idéntico** (comprobado con `diff`): la segunda es una **réplica de
  Jev** —sin `temperature`, la estabilidad se mide con réplicas—.
- `q4`: el material cambia porque la corrida (`C000008`, `deepseek-flash`) consultó **dos** casos.
- `q4-inyectados`: **el control**. Al `q4` limpio se le agregan **tres casos que no tienen nada que
  ver con la pregunta**, todos de `aviacion`: `C000002:U4` (motores turbofán), `C000002:U8`
  (queroseno e hidrógeno) y `C000002:U10` (nudos). Cinco elegidos, un Noul por cada uno, y la misma
  `eleccion` al final.

**La vara.** Fijada antes de correr, sobre el Noul (las bandas de siempre): > 0,85 muy seguramente;
0,75–0,85 seguramente; 0,65–0,75 hay bases; **0,30–0,65 no se puede formar el juicio** (señal de
diseño, no duda de Jev); < 0,20 muy seguramente falso. Y la decisión en código: `confidence ≥ 0,80`
el veredicto se sostiene solo; por debajo, lo mira una persona.

**Lo que se observa.** El grado de cada caso elegido, la elección contra el catálogo entero, y qué
pasa cuando entre los elegidos hay casos que no van.

**El material.** Corpus en la versión 5; documentos `sol` (sello `c9c3de7534d3…`) y `aviacion`
(`e546d95e8b13…`); UT vigentes `C000001` y `C000002`. Corridas del ORQ: `q1` = `C000005` y `q3` =
`C000007` (`gpt-6-luna` `low`, 2 turnos, 1 llamada, 1.962 tokens), las dos consultaron `C000001:U2`;
`q4` = `C000008` (`deepseek-flash` `low`, 2 turnos, 2 llamadas, 3.092 tokens), consultó
`C000001:U2` y después `C000001:U1`.

**El comando.** Los dos archivos los arma `armar_expediente.py` leyendo la base con `mode=ro`; la
llamada, `utiliarios/jev.py correr`.

```bash
python3 "…/armar_expediente.py" q1                     # y q3
python3 "…/armar_expediente.py" q4
python3 "…/armar_expediente.py" q4 --nombre q4-inyectados \
        --elegidos-extra C000002:U4,C000002:U8,C000002:U10
bash -ic 'python3 utiliarios/jev.py correr "…/expediente-<nombre>.json" \
        "…/preguntas-<nombre>.json" "…/resultados/jev-casos-<nombre>-r1.json"'
```

**Los resultados** (crudos en `resultados/`, `jev-1.13.0`):

| juicio | forma | `q1` | `q3` | `q4` | `q4` + 3 inyectados |
|---|---|---|---|---|---|
| `elegido_1` · `C000001:U2` | Noul | 0,92 | 0,92 | 0,91 | **0,91** |
| `elegido_2` · `C000001:U1` | Noul | — | — | 0,47 | **0,44** |
| `elegido_3` · `C000002:U4` (turbofán) | Noul | — | — | — | **0,02** |
| `elegido_4` · `C000002:U8` (queroseno) | Noul | — | — | — | **0,02** |
| `elegido_5` · `C000002:U10` (nudos) | Noul | — | — | — | **0,02** |
| `eleccion` | Choice | `correcta` · conf. 0,93 | `correcta` · conf. 0,92 | **`sobran`** · conf. **0,44** | **`sobran`** · conf. **0,87** |
| reparto (`correcta`/`sobran`/`faltan`/`no_sirve`) | | 0,95/0,01/0,02/0,02 | 0,94/0,01/0,02/0,03 | 0,40/**0,58**/0,01/0,01 | 0,06/**0,90**/0,01/0,03 |
| tokens de entrada / salida | | 1.256 / 75 | 1.256 / 75 | 1.356 / 94 | 1.675 / 154 |

**Lo que dicen las cuatro.**

- `q1` y `q3`: la elección es correcta y se sostiene sola. Réplica: el Noul no se movió y el reparto
  se movió 0,01 (la variación que la guía documenta para réplicas).
- `q4` **separa los dos casos** —`U2` 0,91 contra `U1` 0,47— y la `eleccion` sale `sobran` con
  **confianza 0,44**: por debajo del umbral, **va a revisión**. La franja central de `U1` es, según la
  guía, **señal de diseño antes que veredicto**: un grado bajo no dice por qué.
- **El control**: los tres inyectados dan **0,02** los tres —«muy seguramente falso»—, mientras el
  caso bueno sigue en 0,91. Y la `eleccion` pasa a `sobran` con **confianza 0,87**: el mismo
  veredicto que en `q4`, pero ahora por encima del umbral, **se sostiene solo**. La confianza se movió
  0,44 → 0,87 porque la evidencia dejó de ser ambigua: tres casos claramente de más no admiten duda.
- El `elegido_2` se movió 0,47 → 0,44 entre las dos corridas de `q4`. No es una réplica: el `state`
  cambió (tres elegidos más). La garantía de independencia del proveedor es sobre las **preguntas**;
  cambiar el material es cambiar el expediente.

**Lo que no dice.** No dice **de qué oración** sale el sostén ni si la respuesta del ORQ se sostiene
en los casos leídos; esta prueba juzga la elección, no la respuesta. Con un solo elegido,
`elegido_1` y `eleccion` dicen casi lo mismo —se separan con `q4`—; y con ninguno (`q2`) el molde
cambia, porque no hay elección que juzgar.
