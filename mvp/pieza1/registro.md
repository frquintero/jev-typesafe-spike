# Pieza 1 — registro (04-10-2026)

Primer pedazo de la MVP sobre el aviso del Club de Montaña Peña Alta
(`mvp/mesa1b/documento.md`): Q5 (conflicto de fuentes) y Q6r (dato derivado
con dependencias).

## Archivos

| archivo | qué es | quién |
|---|---|---|
| `esquema2.md` | forma de las tablas y del dato derivado (candidato) | Cowork |
| `ficha_mano.json` | ficha del aviso, a mano, congelada tras revisión de DeepSeek | Cowork |
| `preguntas.md` | Q5, Q6r, premisas y criterio de aceptación | Cowork |
| `tablas_cowork.json`, `tablas_ds.json` | respuestas de referencia, hechas por separado | Cowork; DeepSeek (`dsh`, esfuerzo high) |
| `pieza1.py` | verificador de forma, comparador, `guardar` y `mantener` (solo biblioteca estándar, sin API) | Claude Code (Opus 5.5, esfuerzo medio) |
| `salida_codigo.txt` | su corrida (con el subcomando viejo `validar`, hoy `verificar`) | Claude Code |
| `corpus.jsonl` | DD1 guardado | `pieza1.py guardar` |

Claude Code también editó `tablas_cowork.json` (posiciones con unidad, «40
mantas»; versión de M4). No hizo commit ni documentó; Cowork lo registró aquí.

## Resultado

- Las dos tablas de referencia: 0 errores del verificador de forma. Coinciden
  en lo de fondo (posiciones, estados, rutas, conflicto, desenlaces, dato
  derivado); 12 diferencias de formato o de reglas abiertas.
- DD1 (senda · fecha de reapertura · 1-11-2026) se guarda y se lee de vuelta.
- Mantenimiento: con D3 = «del 15 al 25 de octubre», 1-11-2026 pierde sostén y
  26-10-2026 gana (M4: Python 3.12.3, datetime).

## Qué no prueba

Todo es papel y código sobre tablas escritas a mano: ningún modelo ha hecho de
orquestador. El código verifica forma, sintaxis, cálculos y consistencia; no
juzga si una ruta sostiene su posición.

## Siguiente

Orquestador mínimo sobre el aviso, sin nada simulado. Primer paso: el código
que arma su prompt desde un archivo de configuración que solo lleva R (rol y
tarea; pregunta, corpus y R; herramientas que R admite y el sistema tiene;
salida y formato; reglas de la tabla). K no se da: es lo que el orquestador
trae (su saber, el código, la web real) y queda en las rutas. Por decidir:
el conflicto de la Q5 vendría de un segundo documento del corpus (el
inventario), porque ninguna fuente real habla de esas mantas. Batería: Q1–Q5
y Q6r, tres réplicas.
