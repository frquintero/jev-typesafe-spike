# Ronda FN2 — determinaciones de jardin1 como tabla de datos (NotebookLM)

Ronda autorizada (sección «Ronda FN2» de `notebooklm-spike/PLAN.md`), ejecutada
en local sin proxy el 2026-10-02. Sin modificaciones de código. No se corrió
`notebooklm auth check` ni nada que liste cuadernos; no se leyó ni imprimió el
archivo de sesión. Todos los crudos anteriores se conservan.

Comando (verbatim del plan, sin cambios):

```bash
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  notebooklm-spike/tabla_nblm.py jardin1 tabla_det_v1 r1 \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json
```

Crudos nuevos (carpeta
`notebooklm-spike/cache/tabla-jardin1-nblm-tabla_det_v1-r1/`, no existía antes):

- `crudo.json` — request/response/parsed/summary de la corrida.
- `tabla.csv` — CSV bajado con `descargar` de la tabla generada.

## Resultado

`completed: true`, `error: null` (campos del crudo y de la salida del script).
La generación pasó de `in_progress` a `completed` (`task_id`
`2b048890-1b5b-4f14-9552-e742a44f3810`).

Cuaderno nuevo `a868d32e-1136-4a6d-80ef-a9ed234d4f0c`, fuente nueva
`afc41397-b4d2-4546-807a-195661ab9f0f`. Cliente `notebooklm-py==0.8.4`,
herramienta `generate_data_table`. Instrucciones enviadas =
`notebooklm-spike/prompts/tabla_det_v1.md` salvo el salto final (1742 frente a
1743 caracteres).

## Tiempos (los que imprimió el script; coinciden con el crudo)

- `crear`: 0,389 s.
- `cargar`: 1,112 s.
- `lista`: 0,340 s.
- `texto`: 0,301 s.
- `pedir_tabla`: 0,884 s.
- `esperar_tabla`: 25,132 s.
- `bajar_csv`: 0,216 s.
- Total (`segundos_total`): 29,199 s.

Referencia F5 (DeepSeek, ficha completa): 102,6–126,5 s.

## Fuente

`fuente_igual_al_texto_numerado: false`. La única diferencia es de blancos:
el texto recuperado duplica tres saltos de párrafo (`\n\n` → `\n\n\n\n`,
1.305 frente a 1.311 caracteres, tres inserciones de `\n\n` en las posiciones
294, 598 y 961 del texto enviado). El contenido y la numeración [1]–[12] son
los mismos.

## Columnas y filas

Recibidas (11, en este orden): Caso de estudio, Aspecto, Valor, Unidad,
Cambio, Condición, Quién lo sostiene, Inferido, Oración, Fragmento literal,
Fuente. La columna `Fuente` (valor `[1]` en todas las filas) no estaba entre
las diez pedidas; `columnas_faltantes: []`.

Filas: 18. Fragmentos no literales (`no_literales`): ninguno (lista vacía).

## CSV completo (18 filas)

```csv
Caso de estudio,Aspecto,Valor,Unidad,Cambio,Condición,Quién lo sostiene,Inferido,Oración,Fragmento literal,Fuente
agua vertida en el jardín durante la demostración,volumen,20,litros,,durante una demostración,autor,no,10,Durante una demostración se vertieron unos 20 litros en el jardín,[1]
agua vertida sobre el camino durante la demostración,volumen,semejante,litros,,durante una demostración,autor,sí,10,una cantidad semejante sobre el camino,[1]
el jardín durante la demostración,comportamiento del agua,fue desapareciendo de la superficie,,desapareciendo de la superficie,durante una demostración,autor,no,11,"en el primero, el agua fue desapareciendo de la superficie",[1]
la forma del jardín,propósito,recibir parte del agua que baja del pavimento cuando llueve,,,cuando llueve,autor,no,3,su forma tiene una función: recibir parte del agua que baja del pavimento cuando llueve,[1]
un conducto situado cerca del borde superior,función,permitir que el exceso salga hacia el desagüe,,,si llega más agua de la que el terreno admite,autor,no,6,"Si llega más de la que el terreno admite, un conducto situado cerca del borde superior permite que el exceso salga hacia el desagüe.",[1]
el camino durante la demostración,resultado tras verter agua,quedó un charco visible,,,durante una demostración,autor,no,11,En este último quedó un charco visible,[1]
una parte del suelo,ubicación,en el patio de la escuela de Valdemora,,,,autor,no,1,"En el patio de la escuela de Valdemora, una parte del suelo está más baja que el camino que la rodea.",[1]
una parte del suelo,nivel con respecto al camino que la rodea,más baja,,,,autor,no,1,una parte del suelo está más baja que el camino que la rodea,[1]
plantas de hojas estrechas y tallos flexibles,lugar de crecimiento,allí,,,,autor,no,2,Allí crecen plantas de hojas estrechas y tallos flexibles.,[1]
jardín,apariencia,corriente,,,,autor,sí,3,Parece un jardín corriente,[1]
el agua,punto de entrada,por una abertura entre las piedras del borde,,,,autor,no,4,El agua entra por una abertura entre las piedras del borde.,[1]
el agua,modo de penetración en la tierra,lentamente,,,,autor,no,5,penetrar lentamente en la tierra,[1]
Clara Beltrán,cargo,encargada del huerto escolar,,,,autor,no,7,"Clara Beltrán, encargada del huerto escolar",[1]
las raíces,función en el suelo,ayudan a mantener pequeños espacios por los que circula el agua,,,,Clara Beltrán,no,7,las raíces ayudan a mantener pequeños espacios por los que circula el agua,[1]
un suelo muy compacto,capacidad de absorción,con dificultad,,,,Clara Beltrán,no,8,un suelo muy compacto puede absorberla con dificultad,[1]
el terreno antes de plantar,acciones de preparación de la tierra,se retiraron cascotes y se mezcló la tierra con material más suelto,,,,autor,no,9,antes de plantar se retiraron cascotes y se mezcló la tierra con material más suelto,[1]
la diferencia entre el camino y el jardín,utilidad de observación,ayuda a entender su función,,,,autor,no,12,La diferencia ayuda a entender su función,[1]
la demostración,capacidad probatoria de recoger toda la lluvia de una tormenta,no prueba que el jardín pueda recoger toda la lluvia de una tormenta,,,,autor,no,12,no prueba que el jardín pueda recoger toda la lluvia de una tormenta,[1]
```

Referencia de contenido (DeepSeek, F5): 27 / 23 / 19 determinaciones en
`unidades/cache/ficha-jardin1-deepseek-ficha_v1-r{1,2,3}.json`. El contenido se
compara después (Cowork y Frat).
