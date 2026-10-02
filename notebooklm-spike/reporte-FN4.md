# Ronda FN4 — tabla de determinaciones de jardin1 con la forma del marco (NotebookLM)

Ronda autorizada (sección «Ronda FN4» de `notebooklm-spike/PLAN.md`), ejecutada
en local sin proxy el 2026-10-02. Sin modificaciones de código. No se corrió
`notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el
archivo de sesión. Todos los crudos anteriores se conservan. Commit de
preparación `0c6e86e` incluido en la copia (`git pull --ff-only`: ya estaba
actualizada). La carpeta de crudos no existía antes de correr.

Comando (verbatim del plan, sin cambios):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v3 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Crudos nuevos (carpeta
`notebooklm-spike/cache/tabla-jardin1-nblm-tabla_det_v3-r1/`):

- `crudo.json` — request/response/parsed/summary de la corrida.
- `tabla.csv` — CSV bajado con `descargar` de la tabla generada.

## Resultado

`completed: true`, `error: null` (campos del crudo y de la salida del script).
La generación pasó de `in_progress` a `completed` (`task_id`
`94fc6198-9e2b-445f-8873-fef4534eec5e`).

Cuaderno nuevo `3ef72021-06af-48ed-92b6-6150ddfbbecb`, fuente nueva
`75ba1fb9-6d8e-4b0f-b69f-97b64f536e38`. Cliente `notebooklm-py==0.8.4`,
herramienta `generate_data_table`. Instrucciones enviadas =
`notebooklm-spike/prompts/tabla_det_v3.md` salvo el salto final (3825 frente a
3826 caracteres).

## Tiempos (los que imprimió el script; coinciden con el crudo)

- `crear`: 0,369 s.
- `cargar`: 1,208 s.
- `lista`: 0,392 s.
- `texto`: 0,242 s.
- `pedir_tabla`: 0,968 s.
- `esperar_tabla`: 25,215 s.
- `bajar_csv`: 0,194 s.
- Total (`segundos_total`): 29,361 s.

Referencia FN3 (misma fuente, `tabla_det_v2`): 29,499 s. Referencia FN2
(`tabla_det_v1`): 29,199 s. Referencia F5 (DeepSeek, ficha completa):
102,6–126,5 s.

## Fuente

`fuente_igual_al_texto_numerado: false`. La única diferencia es de blancos, la
misma que en FN2 y FN3: el texto recuperado duplica tres saltos de párrafo
(`\n\n` → `\n\n\n\n`, 1.305 frente a 1.311 caracteres, tres inserciones de
`\n\n` en las posiciones 294, 598 y 961 del texto enviado). El contenido y la
numeración [1]–[12] son los mismos.

## Columnas y filas

Recibidas (12, en este orden): caso de estudio, aspecto, valor, unidad,
respecto de, cambio, condición, quién lo sostiene, inferido, oración,
fragmento literal, Fuente. La columna `Fuente` (valor `[1]` en todas las
filas) no estaba entre las once pedidas; `columnas_faltantes: []`.

Filas: 17 (FN3: 19; FN2: 18). Fragmentos no literales (`no_literales`): 1
(FN3: 2; FN2: 0):

- Fila 3, oración 2: `Allí crecen plantas de [...] tallos flexibles`.

## CSV completo (17 filas)

```csv
caso de estudio,aspecto,valor,unidad,respecto de,cambio,condición,quién lo sostiene,inferido,oración,fragmento literal,Fuente
una parte del suelo del patio de la escuela de Valdemora,posición relativa del suelo,más baja,Sin información,el camino que la rodea,Sin información,Sin información,autor,no,1,"En el patio de la escuela de Valdemora, una parte del suelo está más baja que el camino que la rodea",[1]
plantas de la parte baja del patio,ancho de las hojas,estrechas,Sin información,Sin información,Sin información,Sin información,autor,sí,2,Allí crecen plantas de hojas estrechas,[1]
plantas de la parte baja del patio,flexibilidad de los tallos,flexibles,Sin información,Sin información,Sin información,Sin información,autor,sí,2,Allí crecen plantas de [...] tallos flexibles,[1]
la parte baja del patio,apariencia,corriente,Sin información,un jardín corriente,Sin información,Sin información,autor,sí,3,Parece un jardín corriente,[1]
función de la forma de la parte baja del patio,objetivo,recibir parte del agua que baja del pavimento cuando llueve,Sin información,Sin información,Sin información,Sin información,autor,sí,3,su forma tiene una función: recibir parte del agua que baja del pavimento cuando llueve,[1]
punto de entrada del agua,ubicación,entre las piedras del borde,Sin información,Sin información,Sin información,Sin información,autor,no,4,El agua entra por una abertura entre las piedras del borde,[1]
penetración del agua en la tierra,velocidad,lentamente,Sin información,Sin información,Sin información,Sin información,autor,no,5,penetrar lentamente en la tierra,[1]
salida del exceso de agua,mecanismo,un conducto situado cerca del borde superior,Sin información,Sin información,Sin información,Si llega más agua de la que el terreno admite,autor,sí,6,"Si llega más de la que el terreno admite, un conducto situado cerca del borde superior permite que el exceso salga hacia el desagüe",[1]
Clara Beltrán,cargo o rol,encargada del huerto escolar,Sin información,Sin información,Sin información,Sin información,autor,no,7,"Clara Beltrán, encargada del huerto escolar",[1]
raíces,función,ayudan a mantener pequeños espacios por los que circula el agua,Sin información,Sin información,Sin información,Sin información,Clara Beltrán,no,7,las raíces ayudan a mantener pequeños espacios por los que circula el agua,[1]
suelo muy compacto,capacidad de absorción de agua,con dificultad,Sin información,Sin información,Sin información,Sin información,Clara Beltrán,sí,8,un suelo muy compacto puede absorberla con dificultad,[1]
tierra del jardín,preparación antes de plantar,se retiraron cascotes y se mezcló la tierra con material más suelto,Sin información,Sin información,Sin información,antes de plantar,autor,sí,9,antes de plantar se retiraron cascotes y se mezcló la tierra con material más suelto,[1]
volumen de agua vertido en el jardín,volumen,unos 20,litros,Sin información,Sin información,durante una demostración,autor,no,10,Durante una demostración se vertieron unos 20 litros en el jardín,[1]
volumen de agua vertido sobre el camino,volumen,semejante,Sin información,unos 20 litros,Sin información,durante una demostración,autor,sí,10,una cantidad semejante sobre el camino,[1]
agua en el jardín,comportamiento en la superficie,fue desapareciendo,Sin información,Sin información,fue desapareciendo de la superficie,tras verter la agua,autor,sí,11,"en el primero, el agua fue desapareciendo de la superficie",[1]
camino,resultado tras verter el agua,un charco visible,Sin información,Sin información,Sin información,tras verter la cantidad semejante de agua,autor,sí,11,En este último quedó un charco visible,[1]
demostración,capacidad probatoria de recoger toda la lluvia de una tormenta,no prueba,Sin información,Sin información,Sin información,Sin información,autor,sí,12,no prueba que el jardín pueda recoger toda la lluvia de una tormenta,[1]
```

Referencia de contenido (DeepSeek, F5): 27 / 23 / 19 determinaciones en
`unidades/cache/ficha-jardin1-deepseek-ficha_v1-r{1,2,3}.json`. El contenido se
compara después (Cowork y Frat).
