# Ronda FN3 — tabla de determinaciones de jardin1 con ejemplo resuelto y regla 7 (NotebookLM)

Ronda autorizada (sección «Ronda FN3» de `notebooklm-spike/PLAN.md`), ejecutada
en local sin proxy el 2026-10-02. Sin modificaciones de código. No se corrió
`notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el
archivo de sesión. Todos los crudos anteriores se conservan. Commit de
preparación `be949ec` incluido en la copia (`git pull --ff-only`: ya estaba
actualizada). La carpeta de crudos no existía antes de correr.

Comando (verbatim del plan, sin cambios):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v2 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Crudos nuevos (carpeta
`notebooklm-spike/cache/tabla-jardin1-nblm-tabla_det_v2-r1/`):

- `crudo.json` — request/response/parsed/summary de la corrida.
- `tabla.csv` — CSV bajado con `descargar` de la tabla generada.

## Resultado

`completed: true`, `error: null` (campos del crudo y de la salida del script).
La generación pasó de `in_progress` a `completed` (`task_id`
`e301789d-698a-4e2f-9ba3-d0a34db9c332`).

Cuaderno nuevo `15f3f09b-e874-4116-b3aa-36f53c134203`, fuente nueva
`83a3db77-42f5-4cd4-ac73-f7315bbccdfe`. Cliente `notebooklm-py==0.8.4`,
herramienta `generate_data_table`. Instrucciones enviadas =
`notebooklm-spike/prompts/tabla_det_v2.md` salvo el salto final (3264 frente a
3265 caracteres).

## Tiempos (los que imprimió el script; coinciden con el crudo)

- `crear`: 0,371 s.
- `cargar`: 1,258 s.
- `lista`: 0,352 s.
- `texto`: 0,250 s.
- `pedir_tabla`: 1,009 s.
- `esperar_tabla`: 25,285 s.
- `bajar_csv`: 0,221 s.
- Total (`segundos_total`): 29,499 s.

Referencia FN2 (misma fuente, `tabla_det_v1`): 29,199 s. Referencia F5
(DeepSeek, ficha completa): 102,6–126,5 s.

## Fuente

`fuente_igual_al_texto_numerado: false`. La única diferencia es de blancos, la
misma que en FN2: el texto recuperado duplica tres saltos de párrafo (`\n\n` →
`\n\n\n\n`, 1.305 frente a 1.311 caracteres, tres inserciones de `\n\n` en las
posiciones 294, 598 y 961 del texto enviado). El contenido y la numeración
[1]–[12] son los mismos.

## Columnas y filas

Recibidas (11, en este orden): caso de estudio, aspecto, valor, unidad, cambio,
condición, quién lo sostiene, inferido, oración, fragmento literal, Fuente. La
columna `Fuente` (valor `[1]` en todas las filas) no estaba entre las diez
pedidas; `columnas_faltantes: []`.

Filas: 19 (FN2: 18). Fragmentos no literales (`no_literales`): 2 (FN2: 0):

- Fila 7, oración 2: `hojas estrechas / tallos flexibles`.
- Fila 19, oración 12: `La diferencia ayuda a entender su función / no prueba
  que el jardín pueda recoger toda la lluvia de una tormenta`.

## Datos para los criterios fijados (verbatim del CSV, sin veredicto)

- Valor con aproximador (oración 10): `unos 20`, unidad `litros`, inferido
  `no`, fragmento `se vertieron unos 20 litros en el jardín`.
- Valor de «semejante» (oración 10): `semejante a unos 20 litros`, unidad
  `litros`, inferido `sí`, fragmento `una cantidad semejante sobre el camino`.
- Valor de «allí» (oración 2): `la parte más baja del suelo del patio de la
  escuela de Valdemora`, inferido `sí`, fragmento `Allí crecen plantas`; caso
  de estudio `plantas de la parte más baja del suelo del patio de la escuela
  de Valdemora`.
- Valor de «más baja» (oración 1): `más baja que el camino que la rodea`,
  inferido `no`, fragmento `una parte del suelo está más baja que el camino
  que la rodea`.
- Columna Condición: `Sin información` en 18 de 19 filas; la excepción es la
  fila 1 (`si llega más agua de la que el terreno admite`). Ninguna fila repite
  `durante una demostración` en Condición (FN2 la repetía en 4 filas).
- Atribución a Clara Beltrán (columna «quién lo sostiene»): filas 14–16
  (`raíces, efecto en el suelo`; `terreno con raíces, transformación en
  esponja` con valor `no se convierte automáticamente en una esponja`;
  `suelo muy compacto, capacidad de absorción`). FN2 atribuía a Clara Beltrán
  2 filas (raíces y suelo compacto).

## CSV completo (19 filas)

```csv
caso de estudio,aspecto,valor,unidad,cambio,condición,quién lo sostiene,inferido,oración,fragmento literal,Fuente
conducto situado cerca del borde superior,función,permitir que el exceso salga hacia el desagüe,Sin información,Sin información,si llega más agua de la que el terreno admite,autor,no,6,un conducto situado cerca del borde superior permite que el exceso salga hacia el desagüe,[1]
demostración,volumen de agua vertida en el jardín,unos 20,litros,Sin información,Sin información,autor,no,10,se vertieron unos 20 litros en el jardín,[1]
demostración,volumen de agua vertida sobre el camino,semejante a unos 20 litros,litros,Sin información,Sin información,autor,sí,10,una cantidad semejante sobre el camino,[1]
suelo del patio de la escuela de Valdemora,ubicación,patio de la escuela de Valdemora,Sin información,Sin información,Sin información,autor,no,1,En el patio de la escuela de Valdemora,[1]
una parte del suelo del patio de la escuela de Valdemora,nivel con respecto al camino que la rodea,más baja que el camino que la rodea,Sin información,Sin información,Sin información,autor,no,1,una parte del suelo está más baja que el camino que la rodea,[1]
plantas de la parte más baja del suelo del patio de la escuela de Valdemora,ubicación de crecimiento,la parte más baja del suelo del patio de la escuela de Valdemora,Sin información,Sin información,Sin información,autor,sí,2,Allí crecen plantas,[1]
plantas de la parte más baja del suelo del patio de la escuela de Valdemora,forma de las hojas y características de los tallos,hojas estrechas y tallos flexibles,Sin información,Sin información,Sin información,autor,no,2,hojas estrechas / tallos flexibles,[1]
jardín de la escuela de Valdemora,apariencia,corriente,Sin información,Sin información,Sin información,autor,no,3,Parece un jardín corriente,[1]
forma del jardín de la escuela de Valdemora,función,recibir parte del agua que baja del pavimento cuando llueve,Sin información,Sin información,Sin información,autor,no,3,su forma tiene una función: recibir parte del agua que baja del pavimento cuando llueve,[1]
agua de lluvia,punto de entrada al jardín,por una abertura entre las piedras del borde,Sin información,Sin información,Sin información,autor,no,4,El agua entra por una abertura entre las piedras del borde,[1]
agua de lluvia,comportamiento tras entrar al jardín,"penetrar lentamente en la tierra, en lugar de seguir de inmediato hacia la calle",Sin información,Sin información,Sin información,autor,no,5,"Después puede penetrar lentamente en la tierra, en lugar de seguir de inmediato hacia la calle",[1]
Clara Beltrán,cargo,encargada del huerto escolar,Sin información,Sin información,Sin información,autor,no,7,"Clara Beltrán, encargada del huerto escolar",[1]
raíces,efecto en el suelo,ayudan a mantener pequeños espacios por los que circula el agua,Sin información,Sin información,Sin información,Clara Beltrán,no,7,las raíces ayudan a mantener pequeños espacios por los que circula el agua,[1]
terreno con raíces,transformación en esponja,no se convierte automáticamente en una esponja,Sin información,Sin información,Sin información,Clara Beltrán,no,8,eso no convierte cualquier terreno en una esponja,[1]
suelo muy compacto,capacidad de absorción,puede absorber el agua con dificultad,Sin información,Sin información,Sin información,Clara Beltrán,no,8,un suelo muy compacto puede absorberla con dificultad,[1]
tierra del jardín,acciones de preparación antes de plantar,se retiraron cascotes y se mezcló la tierra con material más suelto,Sin información,Sin información,Sin información,autor,no,9,antes de plantar se retiraron cascotes y se mezcló la tierra con material más suelto,[1]
camino,resultado en la demostración,quedó un charco visible,Sin información,Sin información,Sin información,autor,no,11,En este último quedó un charco visible,[1]
jardín,comportamiento del agua en la superficie durante la demostración,fue desapareciendo de la superficie,Sin información,Sin información,Sin información,autor,no,11,el agua fue desapareciendo de la superficie,[1]
diferencia entre el jardín y el camino en la demostración,utilidad y capacidad probatoria,"ayuda a entender su función, pero no prueba que el jardín pueda recoger toda la lluvia de una tormenta",Sin información,Sin información,Sin información,autor,no,12,La diferencia ayuda a entender su función / no prueba que el jardín pueda recoger toda la lluvia de una tormenta,[1]
```

Referencia de contenido (DeepSeek, F5): 27 / 23 / 19 determinaciones en
`unidades/cache/ficha-jardin1-deepseek-ficha_v1-r{1,2,3}.json`. El contenido se
compara después (Cowork y Frat).
