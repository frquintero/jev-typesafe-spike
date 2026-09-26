# Memoria: extracción de datos con LLM (spike-jev / Zettel)

Estado al 26-09-2026.

## 0. Dónde y cómo (para retomar)

- **Carpeta de trabajo (máquina local de Frat, Linux):** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/`, subcarpeta `niveles/`.
- **Repositorio en GitHub:** `https://github.com/frquintero/jev-typesafe-spike`, rama `main`.
- **Esta memoria** vive en la raíz del repositorio, junto a `jev_typesafe_guia_pedagogica_v2.md`.

**Forma de trabajo.** La planificación la hacemos Frat y Cowork; las pruebas las corre Claude Code en la nube. Nos coordinamos a través del repositorio de GitHub.

1. **Planificar (Frat + Cowork).** Discutimos, conjeturamos y acordamos un cambio.
2. **Mostrar.** Cowork muestra el prompt y Frat da el «adelante».
3. **Preparar (Cowork, en la máquina local).** Cowork escribe el prompt en `niveles/prompts/` y la sección de la ronda en `niveles/PLAN.md`, con el cambio, la conjetura, el comando y el formato del reporte. Hace commit y push a `main`.
4. **Pasar el mensaje.** Cowork entrega a Frat el mensaje para Claude Code, con el número de commit.
5. **Correr (Claude Code, en una VM de la nube).** Claude Code hace `git pull`, lee la sección de la ronda, corre el comando sin modificar nada y guarda el crudo en `niveles/cache/`. Luego hace commit y push del cache.
6. **Reportar.** Claude Code entrega el JSON verbatim, los tokens y los fragmentos del razonamiento que se le pidan, sin veredicto. Frat pega ese reporte en Cowork.
7. **Evaluar (Cowork + Frat).** Cowork hace `git pull` en la máquina local, lee el crudo, incluido el `reasoning_content`, y lo evalúa contra la conjetura. Frat decide el paso siguiente.

Las claves de API nunca pasan por el repositorio: el proxy de la nube las inyecta a Claude Code.

**Pruebas en local.** También se puede correr en la máquina de Frat, con el mismo código, a través de `proxy_local.py` (instrucciones en el README raíz). Frat arranca el proxy con sus claves en una terminal. Cowork corre los scripts en la máquina local, exportando solo `HTTPS_PROXY` y `SSL_CERT_FILE`, y nunca ve las claves. Los crudos quedan en `niveles/cache/` y se suben con commit y push, igual que en la nube.

## 1. Qué hacemos

Extraer de un `texto` sus **datos**, en el sentido del ensayo de Frat «¿Qué es un dato?», con un LLM guiado por un prompt afinado. Después, Jev (jev-1.13.0) auditará lo extraído. El objeto dato está cerrado sobre doc5 (prompt `datos_v8`); falta probarlo en doc4. Siguen otros objetos: afirmación, información y relaciones.

El objetivo original del spike (Jev en lugar de GLM para la detección de estructura del piloto EEL, fases 1–3 del README) está **suspendido**, no abandonado.

División del trabajo (decidida):
- el prompt dirige;
- el LLM extrae;
- el código solo orquesta: arma, llama y guarda crudos, sin verificar nada;
- Jev juzga el contenido interpretado.

## 2. Cómo trabajamos

- **Roles y flujo:** ver §0.
- **Planificar** es pensar, discutir y conjeturar. Solo se corre cuando hay una conjetura nueva, y cada corrida debe decidir algo. No se ofrecen corridas por reflejo.
- **Una cosa por ronda.** Varios cambios solo si aplican un mismo principio.
- **Mostrar el prompt antes de correr**, y esperar el «adelante».
- **Prompts sin ejemplos ni listas ilustrativas.** Excepción aceptada por Frat: los ejemplos dentro de sus definiciones de Escala y Valor.
- El material se nombra `texto`, entre backticks.
- **Simplicidad:** poca prosa, sin extras que no se hayan pedido.
- **Crítica constructiva:** valorar la idea de Frat y mejorarla con razones, sin aceptar todo.
- **Pruebas:** sin tests de regresión; `py_compile` solo si hay código nuevo.
- **Seguridad:** las claves (TYPESAFE, GLM, DeepSeek) nunca van en archivos. Las inyecta el proxy o las configura Frat. Solo documentos sintéticos. Commit o push solo cuando se pide. No se editan README, diccionario ni guía sin aprobación.

## 3. Repositorio y pruebas

- **Repositorio:** `/home/fratquintero/Documentos/Claude/jev-typesafe-spike/`, rama `main`, remoto github `frquintero/jev-typesafe-spike`.
- **Carpeta `niveles/`:**
  - `PLAN.md`: una sección por ronda (1–9, 6b, 6c, 8b, D1–D10). Cada sección dice qué cambia, cuál es la conjetura, el comando y el formato del reporte.
  - `extraer_datos.py`: el orquestador. Uso: `python3 niveles/extraer_datos.py <doc> <modelo> <prompt> <rN>`. Reemplaza `{{TEXTO}}`, llama a `call_model` y guarda `cache/datos-<doc>-<modelo>-<prompt>-<rN>.json` con request, response (incluido el `reasoning_content`), parsed, venia_con_cerca y error_parseo. Es idempotente.
  - `run_niveles.py`: `call_model` por streaming. `deepseek` corresponde a deepseek-flash, con thinking y reasoning_effort bajo; `flash` corresponde a glm-5.3-flash.
  - `jev_sopesa.py`: builds de Jev de la etapa Toulmin (v6), sin uso por ahora.
  - `prompts/`: `datos_v1` a `datos_v8`, más prompts históricos (toulmin, A, B, clasif).
  - `docs/`: documentos sintéticos:
    - doc1: ciclorrutas;
    - doc2: horario escolar;
    - doc3: peatonalización;
    - doc4: árboles de la avenida Central;
    - doc5: pozo de Los Robles, con variables repetidas bajo distintas condiciones, escalas nominal y ordinal, dichos, un plan y una norma.
- **Mensaje tipo para Claude Code:** `git pull (main, <commit>). Lee la sección "Ronda Dn" de niveles/PLAN.md. No hay código nuevo; no modifiques nada. Corre: <comando>. Repórtame el JSON verbatim, si venía con cerca o hubo error de parseo, y los tokens (incluidos los de razonamiento). Sin veredicto. Haz commit y push del cache.`
- **Diagnóstico:** pedir fragmentos del `reasoning_content` donde el modelo duda. Buscar «omit», «maybe», «awkward», «not a dat». Así se vio en D9 la contradicción del prompt, y en D10 por qué la corrección funcionó.
- **Costo:** unos 14–16 mil tokens de razonamiento por corrida con deepseek-flash.

## 4. Marco: qué es un dato (ensayo de Frat)

- **Caso:** lo distinguido al observar. Es una unidad que reúne determinaciones, y puede no tener ninguna.
- **Variable:** el aspecto bajo el cual se considera el caso; fija qué diferencias cuentan.
- **Pregunta:** una estructura con posiciones fijadas y abiertas, como `T(agua del vaso A, 8:15) = ?`.
- **Escala:** el sistema de unidades, categorías, precisión y reglas de conversión. **Valor:** una posición o elemento admitido en una escala. Si cambia la escala, cambia el valor y la determinación permanece (21,4 °C y 70,52 °F).
- **Atribución:** la operación que vincula el valor con el caso bajo la variable. Produce una **determinación**, que cierra la pregunta.
- **Condiciones**, clasificadas por el efecto de modificarlas:
  - constitutivas: cambia la pregunta;
  - de representación: cambia la forma y se conserva la determinación;
  - de procedencia: cambia la ruta y la pregunta sigue igual.
- **Dato:** la determinación de un caso bajo una variable y ciertas condiciones constitutivas, registrada de modo que puede recuperarse.
- **Verdad:** recae en la determinación, que puede ser verdadera, falsa o indeterminada. El valor tiene predicados propios: admisible, preciso, impreciso, mal codificado.
- **Información:** no forma parte del dato. Es el cambio en las respuestas admisibles a una pregunta cuando se considera un dato según unas reglas.

## 5. Objeto dato: estado actual (`datos_v8`, cerrado sobre doc5)

Estructura del prompt: TAREA, DEFINICIONES PARA CUMPLIR LA TAREA, REGLAS y ESTRUCTURA DEL JSON DE RESPUESTA.

Principios operativos:
- Método: identificar primero los casos y unificarlos; luego las variables de cada caso; luego los datos de cada variable.
- Prueba de la pregunta: `<variable>(<caso>, <condiciones constitutivas>) = ?`. Si falta el caso, la variable, el valor o la escala, no hay dato. Dejar fuera lo que no es dato es parte de la tarea.
- Universo de valores cerrado: cantidad, categoría, nivel ordenado o fecha. Si no es ninguna de estas, no es un valor.
- Quien dice, sostiene, atribuye, planea o mide algo es procedencia; lo dicho se examina como cualquier otra parte de `texto`.
- Condiciones constitutivas: si cambiaran, la pregunta sería otra. No incluyen de dónde proviene el valor ni quién lo dice.
- Se registra lo que es, fue o será, no lo que debería ser. Cada determinación va una sola vez, bajo su caso. Un caso sin datos no va en el JSON.

JSON: `{"casos":[{"caso", "oraciones":[{"oracion", "datos":[{"dato", "variable", "valor", "escala", "condiciones_constitutivas":[]}]}]}]}`

## 6. Rondas D1–D10 (deepseek-flash)

| Ronda | Prompt | Doc | Qué se probó | Resultado |
|---|---|---|---|---|
| D1 | datos_v1 | doc2 | Primer smoke test del dato | Buena extracción, pero demasiado amplia |
| D2 | clasif_v1 | doc4 | Datos (caso concreto; «no lo que debería ser») y afirmaciones, en una llamada | Funcionó |
| D3 | datos_v2 | doc4 | Jerarquía oración → casos → datos | Funcionó; un mismo caso salió con dos nombres |
| D4 | datos_v3 | doc4 | Primero los casos, unificados | Unificó; «el tráfico» salió como caso |
| D5 | datos_v4 | doc4 | JSON organizado por caso | Duplicados entre casos y valores que eran enunciados |
| D6 | datos_v5 | doc4 | Dato según el ensayo; escala obligatoria | Sin duplicados; la escala no filtró (seudoescalas); procedencia puesta como condición |
| D7 | datos_v6 | doc4 | Condiciones con el criterio del ensayo | La procedencia salió; hubo variación entre corridas |
| D8 | datos_v6 | doc5 | Documento nuevo | Condiciones y escalas nominal y ordinal bien; siguieron las seudoescalas en actos y dichos |
| D9 | datos_v7 | doc5 | Definiciones de escala y valor de Frat | Sin cambio; el razonamiento mostró la contradicción entre las definiciones y la regla 5 |
| D10 | datos_v8 | doc5 | Quien dice es procedencia; universo de valores cerrado | Conjetura confirmada: salen los actos y dichos, cobertura completa |

## 7. Lecciones

- Un campo obligatorio no filtra: el modelo inventa algo para llenarlo (seudoescalas). Lo que filtra es un universo cerrado.
- Una cláusula del tipo «o cualquier otra…» reabre el universo.
- Si dos señales del prompt se contradicen, el modelo oscila. El remedio es un solo principio, no más definiciones.
- Para que el modelo omita con confianza hay que decirle que omitir es parte de la tarea.
- Parafrasear el ensayo introduce errores («otra cosa» en vez de «otra pregunta»). Conviene citar su criterio casi literal.
- Una sola corrida no separa el efecto del prompt del ruido entre corridas (D7). Frat prefiere probar con otro documento antes que con réplicas.
- El `reasoning_content` es el mejor instrumento de diagnóstico.
- Jev corrige lo que el modelo afirma de más, no lo que omite. Empujar al modelo a omitir tiene ese costo.

## 8. Pendientes

1. Probar si v8 se sostiene en doc4: el plan, lo que dicen los comerciantes, la oficina de tránsito y el caso del tráfico.
2. **Objeto información**, el siguiente. Según el ensayo, es relativo a una pregunta: un dato considerado según reglas cambia las respuestas admisibles. Hay que definir qué se extrae de `texto`: ¿las preguntas que plantea, o las inferencias que hace a partir de datos?
3. **Objeto afirmación.** Qué es y cómo se separa de los datos. Lo que se dice y queda fuera de los datos (causas atribuidas, planes, juicios, normas) es su material.
4. Relaciones entre objetos, auditoría de Jev sobre los datos y reidentificación de casos entre textos.
5. Llevar las definiciones a un catálogo único (`esquema.json`) y actualizar §20.1 del borrador principal.
