# Políticas de experimentación (MVP de Zettel)

**Qué es.** El **taller de experimentación** del MVP, versionado: `mvp/experimentacion/`. Cada
experimento nace de una **pregunta concreta** y su resultado es **evidencia para decidir** —una
comparación, una medida, un hallazgo—, **no** un «pasa/falla» sobre el código.

**Las preguntas que justifican un experimento:**

- ¿Este **prompt** recupera mejor lo que necesitamos?
- ¿Esta **función** rinde mejor con determinados materiales?
- ¿Este **cambio en el código** produce el efecto buscado?
- ¿Qué cambia en **calidad, tiempo o costo** entre dos alternativas?

Sin pregunta, no hay experimento.

---

## 1. Cómo se plantea

Un experimento se define **antes** de correrlo, y se define por lo que se deja quieto:

| Pieza | Qué es | Ejemplo |
|---|---|---|
| **La pregunta** | qué se quiere saber | ¿la v2 del prompt de UT recupera mejor…? |
| **Lo que se mantiene fijo** | el material, el modelo y su esfuerzo, el resto del código | el mismo documento, el mismo `luna`/`low`, la misma versión de todo lo demás |
| **Lo que se cambia** | **una** cosa | la versión de la plantilla |
| **Lo que se observa** | qué se mide y se guarda | lo que produjo (la partición, los datos, la forma), los tokens, los segundos, el estado |
| **Cómo se interpreta** | contra qué se compara | la vara, fijada **antes** de correr |

Tres reglas que hacen que el resultado signifique algo:

1. **Una cosa por experimento, para atribuir.** Si cambian dos, el resultado no dice cuál de las dos
   hizo qué. Se puede cambiar un **conjunto**, y entonces también hay evidencia, pero la conclusión es
   **del conjunto**: no se le cuelga la mejora a una pieza. El experimento dice cuál de las dos cosas
   hizo.
2. **La vara se fija antes.** Después de ver la salida, cualquiera encuentra un criterio que la
   apruebe.
3. **El material se declara: conocido o nuevo.** Sobre material **conocido** —el que se usó para
   afinar— se **diagnostica** (ver qué hace); sobre material **nuevo** se **evalúa** (generalizar).
   Lo que se midió sobre el texto con el que se ajustó la pieza no dice nada de otro texto, y el
   experimento no lo presenta como si lo dijera.

---

## 2. De dónde salen las respuestas: real, simulado o conservado

| Pregunta | De dónde | Por qué |
|---|---|---|
| sobre el **prompt** o el **modelo** (calidad, forma de lo que devuelve de verdad, costo, tiempo) | **modelo real** | la señal solo la da el modelo |
| sobre la **maquinaria** (el material armado, la forma validada, el efecto de un cambio en las filas) | **modelo simulado** | barato, repetible, sin red |
| sobre **lo que ya salió**: cambiar la vara, comparar particiones, estudiar omisiones, aplicar una función nueva a las mismas salidas | **lo conservado** | no hace falta llamar a nadie: la respuesta ya está |

**Lo conservado, en el MVP, son los productos**: las unidades y sus oraciones, los datos y las
cédulas (modelo, esfuerzo, plantilla y versión, tokens, segundos, estado). **Las respuestas crudas de
los modelos no se guardan**; solo existen en las líneas viejas (`cache/`, el scratch). Eso acota qué
preguntas contesta este modo, y cuáles piden una corrida nueva.

Cuando el guion usa el **modelo real**: se muestra el prompt y se espera el «adelante», la clave se
lee por `bash -ic` y **nunca se imprime**, y el resultado se guarda (§4).

Lo demás también se **monta**: los **relojes** entran por parámetro, y si el experimento necesita una
base, se usa una **en memoria** —no es ninguna de las dos bases y no toca el disco—.

---

## 3. Condiciones de operación

No son el propósito del taller; son las condiciones para que se pueda correr sin romper nada ni
gastar de más.

1. **Las dos bases se abren solo para leer**: `sqlite3.connect("file:…?mode=ro", uri=True)`.
   **Nunca** por `base.conectar()` ni `almacen.conectar()`: esas puertas **escriben** —siembran
   `ajustes` y corren el esquema—, y abrir no es leer.
2. **No se escribe en las bases, y no se copian.** El experimento que necesite escribir, escribe en
   una base **en memoria**.
3. **Nada se escribe fuera de `mvp/experimentacion/`**: sus resultados van a
   `experimentacion/resultados/`, y las corridas con API llevan `rN` —una réplica nueva es un archivo
   nuevo, no se sobrescribe—.
4. **El gasto se controla**: la API se usa **solo cuando el guion lo declara**. Un guion que la use
   sin declararlo falla, para que no se gaste por olvido.
5. **Todo se versiona** con el experimento: el guion, lo que monta y sus resultados. Y **un resultado
   sin su expediente no dice qué se comparó**: cada uno lleva en su encabezado las **referencias** —no
   copias— a la pregunta, lo que se dejó fijo, lo que se cambió, la vara, el material (id y sello), el
   modelo y su esfuerzo, la repetición (`rN`) y el **commit** (y si el árbol estaba sucio, se dice).
   La corrida y la cédula ya guardan el modelo, el esfuerzo, la plantilla y su versión, los tokens,
   los segundos y el estado; el sello identifica el material; el commit, el código. `temp/` sigue
   siendo scratch, sin versionar.

---

## 4. Qué hay adentro

```
mvp/experimentacion/
  README.md        qué es, cómo se corre, y las condiciones de operación
  montar.py        lo que se monta: modelo simulado, relojes, base en memoria; y los lectores de
                   solo lectura de las bases reales
  correr.py        el comando: lista los experimentos o corre uno
  experimentos/    uno por pregunta, con su nombre y su vara
  resultados/      lo que dejan: respuestas de la API (`<experimento>-rN.json`), medidas, reportes
```

Las pruebas que hoy están sueltas en `temp/prueba-r1/` se **portan** acá como experimentos y de ahí
en adelante se escriben en esta carpeta.

---

## 5. Las costuras que el código tiene que ofrecer

Para que un experimento pueda montar sin tocar nada, el código de producción tiene que dejar tres
puertas abiertas. Ninguna cambia su comportamiento:

| Costura | Hoy | Qué hace falta |
|---|---|---|
| **El momento** | `acto.abrir()` y `cerrar()` llaman a `datetime.now()` adentro | que el momento entre **por parámetro**, con `now()` como defecto |
| **La base** | los actos abren `conectar()` por dentro | que el acto pueda trabajar sobre **una conexión dada** (así apunta a la de memoria) |
| **El modelo** | `llamar` es una función | ya está: se sustituye sin tocar el acto |

**El aislamiento concreto** —las dos bases **en memoria** con `cache=shared`, y el `ATTACH` del espejo
apuntando a la referencia en memoria— se resuelve al construir `montar.py`. Ojo: hoy `esquema.abrir()`
abre por ruta y sin `uri=True`, que es lo primero que hay que resolver.

---

## 6. Procedimientos

- **Listar los experimentos:** `python3 mvp/experimentacion/correr.py`
- **Correr uno:** `python3 mvp/experimentacion/correr.py <experimento>`
- **Escribir un experimento nuevo:** un archivo en `experimentos/`, con la pregunta arriba, lo que
  deja fijo y lo que cambia, la vara, y lo que observa. Devuelve su resultado de forma legible —una
  comparación, una medida o un hallazgo— y no escribe fuera de la carpeta.
- **Leer las bases (siempre solo lectura):** abrir con `mode=ro` y usar el registro para comparar
  corridas —modelo, esfuerzo, plantilla y versión, tokens, segundos, estado—.
- **Si el guion usa la API:** mostrar el prompt, esperar el «adelante», y guardar la respuesta en
  `resultados/<experimento>-rN.json`, citada en el commit.

---

## 7. Lo que este documento manda a actualizar

- **La memoria** (pendiente 11): «el scratch no se versiona» pasa a «el scratch no se versiona
  **salvo los experimentos**, que viven en `mvp/experimentacion/`».
- **`AGENTS.md`**: el mapa suma `mvp/experimentacion/`, y la regla «tras tocar código: `py_compile`;
  no hay tests ni lint» pasa a incluir el comando del taller.
- **`política.md`**: `mvp/experimentacion/` queda como carpeta del proyecto (no se mueve).
