# Prototipos: curva de ejemplos para el paso 2 (datos)

Pedido de Frat: fijar los ejemplos prototípicos del prompt de datos en vez de
parchar palabras. Un ejemplo por forma en que llegan los datos (nodo), cada
uno corto, con un solo fenómeno y una línea de descripción; agregarlos de a
uno y medir aciertos y tokens de razonamiento. El número de ejemplos lo decide
la curva. Solo paso 2 (foco = texto entero), sin paso 1.

Apoyo: cobertura de aspectos sin redundancia (Gupta et al. 2023; Levy et al.
2023); *over-prompting*: más ejemplos pueden empeorar y el óptimo depende del
modelo (Tang et al. 2025); medir también con cero ejemplos; los ejemplos
enseñan sobre todo formato y espacio de respuesta (Min et al. 2022).

## Archivos

- `base.md`: definiciones y «No son datos» de `datos_u10`, más una línea de
  formato (para que k0 sepa la forma del JSON). `{{TAREA}}`, `{{EJEMPLOS}}`,
  `{{DOCUMENTO_NUMERADO}}`, `{{FOCO}}`.
- `ejemplos/A.md` número con unidad (medida, conteo, porcentaje);
  `B.md` fecha u hora de un hecho; `C.md` cualidad (aspecto nombrado o no);
  `D.md` cantidad aproximada o vaga; `E.md` lo que no es dato junto a su
  gemelo que sí lo es.
- `bateria.json`: 15 textos (3 por nodo) con su respuesta correcta, escrita
  antes de correr (29 datos).
- `correr.py <modelo> <rN> [configs]`: configs k0, A, AB, ABC, ABCD, ABCDE.
  Crudos en `cache/<config>-<id>-<modelo>-<rN>.json`.
- `evaluar.py <modelo> <rN>`: sin API; tabla por configuración.

## Ronda P1

```
python3 prototipos/correr.py grok r1
```

**Reporte:** una línea por llamada (config, id, datos, segundos, tokens de
razonamiento). Sin veredicto ni cálculos.

## Ronda P2: candidatos AB y ABE sobre documentos reales (Grok)

Pedido de Frat tras P1: correr la cadena real con los dos candidatos y comparar
contra `datos_u10` (ENC8). `unidades/prompts/datos_pAB.md` y `datos_pABE.md` =
`base.md` + ejemplos A y B (y E). El paso 1 se reutiliza. Una corrida (r1).

```
python3 unidades/extraer_datos_doc.py tec1 grok unidades_v5 datos_pAB r1
python3 unidades/extraer_datos_doc.py oxi1 grok unidades_v5 datos_pAB r1
python3 unidades/extraer_datos_doc.py bio1 grok unidades_v5 datos_pAB r1
python3 unidades/extraer_datos_doc.py tec1 grok unidades_v5 datos_pABE r1
python3 unidades/extraer_datos_doc.py oxi1 grok unidades_v5 datos_pABE r1
python3 unidades/extraer_datos_doc.py bio1 grok unidades_v5 datos_pABE r1
```

## Ronda P3: `datos_pAB` con DeepSeek (tec1, oxi1, bio1)

Pedido de Frat: la misma cadena de P2 con DeepSeek (`deepseek-flash`), solo AB.
El paso 1 se reutiliza (crudos de ENC5 y ENC7). Una corrida (r1). Comparar
contra `datos_u9` de DeepSeek (ENC6, ENC7).

```
python3 unidades/extraer_datos_doc.py tec1 deepseek unidades_v5 datos_pAB r1
python3 unidades/extraer_datos_doc.py oxi1 deepseek unidades_v5 datos_pAB r1
python3 unidades/extraer_datos_doc.py bio1 deepseek unidades_v5 datos_pAB r1
```

## Ronda P4: `datos_pABF` con DeepSeek sobre oxi1

En P3, DeepSeek con AB sacó de más en el ensayo oxi1 (creencias, posibilidades,
comparaciones, tono). `ejemplos/F.md`: prototipo negativo de ensayo (lo que se
creía, lo que podría pasar, una comparación) junto a un dato real.
`datos_pABF` = `base.md` + A, B, F. Una corrida (r1).

```
python3 unidades/extraer_datos_doc.py oxi1 deepseek unidades_v5 datos_pABF r1
```

## Ronda P5: cadena completa con `datos_pABF` sobre oxi1 (GLM y DeepSeek)

Pedido de Frat: sacar a Grok mientras se recargan créditos y probar GLM 5.3
Flash (alias `flash`, `reasoning_effort: low`) con el mismo texto (oxi1, que es
el fragmento que pegó Frat). Cadena completa (paso 1 `unidades_v5` + paso 2
`datos_pABF`), una corrida. DeepSeek en r2 para que el paso 1 también sea
nuevo y los dos modelos se comparen en igualdad.

```
python3 unidades/extraer_datos_doc.py oxi1 flash unidades_v5 datos_pABF r1
python3 unidades/extraer_datos_doc.py oxi1 deepseek unidades_v5 datos_pABF r2
```

## Ronda P6: GLM 5.3 Flash con `reasoning_effort: high` sobre oxi1

En P5, GLM corrió en `low` (el mínimo; la doc de Z.ai recomienda `max`, que es
el valor por defecto) y razonó 0–87 tokens por foco: perdió las cualidades
(«no numeric values») y trajo un dato de fuera del foco. Alias nuevo
`flash_high` en `niveles/run_niveles.py` (mismo modelo, `reasoning_effort:
high`). Cadena completa, una corrida.

```
python3 unidades/extraer_datos_doc.py oxi1 flash_high unidades_v5 datos_pABF r1
```
