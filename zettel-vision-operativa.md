# Zettel: cómo lo soñamos (visión operativa)

Fecha: 2026-10-04. Origen: discusión de Frat y Cowork. Este documento recuerda,
con un ejemplo completo, cómo debería funcionar Zettel de punta a punta. Es
visión, no especificación: el marco filosófico es lo único fijo
(`marco filosófico/`, `definiciones-del-marco.md`); todo lo demás se valida
al andar. Al final se separa lo probado de lo por probar.

## La idea en una frase

Lo que Zettel entrega es **información**: el cambio en el conjunto de
respuestas admisibles a una pregunta, cuando se consideran los datos del
corpus y del **mundo** conforme a unas reglas. El inventario de datos es
útil como inventario; lo útil de verdad sale de **pregunta + datos + mundo**.
Por eso la pregunta es el punto de partida, y un orquestador trae el mundo
que la pregunta necesita.

## Notación y vocabulario

- **Q:** la pregunta. Se estructura en caso de estudio, aspecto, condiciones
  y **dominio** (las posiciones admisibles bajo el aspecto, en una escala;
  ensayo l. 133). El aspecto queda fijado; la respuesta será una posición
  del dominio.
- **D:** los datos del corpus que eligió el usuario (fichas extraídas de sus
  documentos).
- **K:** el **mundo**. Lo que el modelo sabe, hechos estables, reglas de
  inferencia (sumar duraciones, convertir zonas horarias), la web y las APIs
  (aerolíneas, Wikidata, tablas de zonas horarias). Todo lo que entra de K
  lleva su procedencia: quién lo sostiene y cuándo se consultó.
- **R:** las **reglas de la consulta**, impuestas sobre todo el corpus por el
  usuario, el documento o el sistema: fecha de radicación del texto, hora del
  sistema, «sin fuentes externas». R decide, entre otras cosas, cuánto de K
  se admite.
- **A(Q | K):** las completaciones que **estarían** admisibles antes de
  declarar datos. Nunca hay un estado sin nada: es un límite construido para
  comparar.
- **A(Q | K, D; R):** las completaciones admisibles después de considerar D
  conforme a R, con el mundo K. Estructura: orden, equivalencia, distinción
  y sostén. No es monótono: pueden aparecer distinciones nuevas, así que no
  siempre está contenido en A(Q | K).
- **Efecto informativo** (lo que recibe el usuario): el paso de A(Q | K) a
  A(Q | K, D; R), con su ruta. Ocurrió o no, y depende de lo que el usuario
  ya sabía.
- **Contenido informativo** (lo que puede guardar el sistema): la
  determinación que queda sostenida. Es verdadera o falsa; registrada con su
  esquema, es un **dato derivado**.

## El ejemplo completo

### 1. El documento

Una agencia de viajes envía un boletín a sus clientes, radicado el jueves
24-9-2026:

> El vuelo AV-569 despega a las 8:15 de El Dorado el lunes. Lleva 280 pasajeros.

El usuario lo incorpora a su dominio de trabajo en Zettel.

### 2. Extracción de datos (al incorporar el documento)

- **Código:** parte el texto en oraciones y las numera, [1] y [2].
- **DeepSeek** (barato): arma las unidades temáticas (`unidades_v5`). Aquí,
  una sola: «el vuelo AV-569».
- **DeepSeek:** reconstruye la ficha (`ficha_v1`), todo lo que el texto
  establece, por caso de estudio.
- **Código:** verifica que cada respaldo sea literal y esté en la oración
  citada.

Se almacena un registro por determinación, con la forma caso · aspecto ·
valor · condiciones · respaldo (la misma de Wikidata: elemento, propiedad,
valor, calificadores, referencias):

```
D1 · AV-569 · hora de despegue · 8:15 · condiciones: desde El Dorado, «el lunes»
     respaldo: [1] «despega a las 8:15 de El Dorado el lunes»
D2 · AV-569 · pasajeros · 280
     respaldo: [2] «Lleva 280 pasajeros»
```

Con la ficha se guarda la fecha de radicación. Esto es inventario: datos,
todavía no información.

### 3. La consulta

El usuario pregunta: «¿A qué hora local llega el AV-569 a París?». No
restringe las fuentes, así que R admite el mundo.

### 4. El orquestador (un modelo inteligente)

1. **Estructura la pregunta.** Caso de estudio: el vuelo AV-569. Aspecto:
   hora local de llegada. Condición: París. Dominio: las posiciones x:yy, de
   0:00 a 23:59.
2. **Fija R.** Fecha de radicación 24-9-2026 (del documento); fuentes
   externas admitidas (el usuario no las restringió).
3. **Busca el campo.** Recorre las unidades, encuentra «el vuelo AV-569» y
   trae D1 y D2.
4. **Mide la brecha.** Para pasar del dominio entero a una respuesta faltan:
   la fecha concreta de «el lunes», la duración del vuelo, las zonas
   horarias y una validación del horario.
5. **Genera tareas para traer el mundo (K).**
   - Al código: resolver «el lunes» desde el 24-9-2026, lo que da el
     28-9-2026.
   - A la tabla de zonas horarias (IANA): Bogotá UTC−5; París UTC+2 ese día
     (horario de verano).
   - A la API de la aerolínea: validar el AV-569 del 28-9. Confirma salida a
     las 8:15 y duración programada de 10 h 35 min (valor ilustrativo),
     «consultada el 4-10-2026».
6. **Hace calcular al código.** 8:15 en Bogotá = 13:15 UTC; 13:15 + 10 h 35
   min = 23:50 UTC; 23:50 UTC = 1:50 en París.
7. **Lleva la respuesta al juicio de Jev.** Le presenta el expediente (D1 y
   lo traído de K) y el juicio «el AV-569 llega a París hacia la 1:50, hora
   local». Supuesto: Jev devuelve 0,88 (muy seguramente cierto). La API
   confirmó lo que dice el documento, así que no hay conflicto que baje la
   banda.

Los obreros: DeepSeek extrae, el código calcula, las APIs y la web traen el
mundo, Jev juzga. El modelo caro piensa y orquesta; el barato trabaja. Lo
propio de Zettel frente a los agentes genéricos (patrón ReAct,
orquestador-obreros) es que cada tarea la orienta la brecha en A(Q), no una
búsqueda a ciegas.

### 5. Lo que recibe el usuario: información

Se entrega una respuesta solo si se cumplen cuatro condiciones:

1. A(Q | K, D; R) se movió respecto del dominio: hubo efecto.
2. Se respetó R.
3. Los conflictos entre D y K están resueltos o se muestran (si la API
   dijera 8:40 y el documento 8:15, se dice, no se resuelve en silencio).
4. La banda de Jev alcanza para formar juicio: por encima de 0,85 se afirma;
   entre 0,65 y 0,85 se dice con cautela («es probable que…»); por debajo de
   0,65 no se forma juicio y se explica qué falta. El grado no se muestra;
   guía el tono.

Aquí se cumplen las cuatro:

> El AV-569 llega a París hacia la 1:50, hora local, en condiciones normales.
>
> Ruta: la salida es del boletín de la agencia (oración 1), confirmada por la
> aerolínea. «El lunes» es el 28-9-2026, resuelto con la fecha del boletín.
> La duración es de la aerolínea, consultada el 4-10-2026. La conversión de
> zonas horarias la hizo el código.

D2 (280 pasajeros) quedó **mudo**: está en el documento, no en el campo de
la pregunta. El efecto fue el paso del dominio entero a una sola posición, y
ocurrió para este usuario.

### 6. Lo que recibe el sistema: un dato nuevo

Se almacena solo si la banda de Jev fue suficiente y R no prohíbe registrar
derivados. Se guarda aparte de los datos del documento, marcado como
derivado:

```
AV-569 · hora local de llegada · 1:50 · condiciones: París, 28-9-2026, duración normal
inferido: sí · sostén: 0,88
depende de: D1; K (zona horaria Bogotá, zona horaria París,
            API de la aerolínea del 4-10-2026); R (fecha de radicación)
```

Si cambia una dependencia (la aerolínea modifica la duración), el dato
pierde sostén y se revisa: mantenimiento de la verdad (Doyle, 1979; en el
ensayo, atribución relacional, l. 293). La próxima pregunta puede usarlo,
sabiendo que no lo dijo el documento. El ecosistema crece preguntando.

### Variante: cambiar solo R

Con R = {fecha de radicación 24-9-2026; **sin fuentes externas**}, la
duración no puede entrar. A(Q | K, D1; R) se queda en el dominio entero y la
respuesta es: «El documento no establece la hora de llegada; solo la de
salida». Con el mismo documento y la misma pregunta, R decide si hay
respuesta.

## Lo probado y lo por probar

- **Probado en el spike:** la etapa 2 (oraciones numeradas por código,
  unidades con `unidades_v5`, ficha con `ficha_v1`, verificación literal).
  Ver `memoria de trabajo y pendientes.md`.
- **Por probar:** la etapa 4 completa (estructurar Q, fijar R, buscar el
  campo, medir la brecha, generar tareas al mundo, Jev en este papel) y las
  condiciones de entrega (5) y de registro (6). Es la visión de cómo unir
  los puntos, todavía sin evidencia.
