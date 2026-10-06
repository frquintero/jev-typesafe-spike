# Paso 2 · qué aprendimos · 06-10-2026 (corregido)

Sale de lo ya medido y guardado en `mvp/paso2/`: **63 crudos** (33 de
`deepseek-flash` y 18 de Muse Code en desarrollo; 12 de DeepSeek en la reserva),
**57 ítems** esperados en desarrollo y 30 en la reserva, fijados antes de llamar.
Ninguna llamada nueva.

**Corregido tras la revisión de Astra (06-10).** Se rehízo el conteo con ítems
atómicos —separando «el contenido» de «la identidad externa que ese contenido
necesita»—, se corrigieron los costos y se rebajaron cinco afirmaciones que iban más
allá de lo observado. La versión anterior concedía ítems enteros por su contenido
aunque faltara la identidad que el propio ítem pedía: eso infló los porcentajes.

## 1. La comparación, en una tabla

| Entrada | Qué recibe el modelo | Recuperación | Fidelidad | Tiempo (DeepSeek) | Tokens de salida |
|---|---|---|---|---|---|
| (a) unidad sola | sus oraciones | 59/87 = 67,8 % | 100 % | 636,9 s | 147 967 |
| **(b) unidad + referencias** | sus oraciones y las referencias de v9 con sus respaldos | **74/87 = 85,1 %** | 111/113 = **98,2 %** | **616,3 s** | **145 171** |
| (c) unidad + documento | sus oraciones y el documento entero | 71/87 = 81,6 % | 100 % | 650,7 s | 148 630 |

Casillas = ítem esperado × corrida. En desarrollo —donde la comparación **solo elige la
entrada**— ninguna llega al 90 % de recuperación: la mejor es (b), con 85,1 %. Las dos
medidas se aplican en la reserva, y allí (b) alcanzó **30/30 ítems y 70/70 producidos**,
con referencias completas y sin importar nada ajeno. Varios de los ítems que (b) no
recupera en desarrollo son **inalcanzables** con lo que v9 registró: miden lo que el
paso 1 entrega al paso 2, no un defecto de la entrada.

## 2. Ocho hallazgos

**1. Lo que falla sin contexto son las identificaciones que viven fuera de la unidad,
y eso no es un asunto de nombres.** Sin la identidad, la determinación no queda
completa: «la empresa» no dice de quién se afirma la respuesta, «la red» no dice de qué
red se predica la longitud. En el marco, perder de qué se habla puede perder la
determinación, no solo su etiqueta.

**2. (c) resolvió algunas identificaciones que (b) no podía, y dejó otras sin
resolver.** No es que el documento entero no sirva: en `doc4 U5` (c) distinguió los dos
cortes y en `doc4 U2` relacionó la reparación con el corte, dos cosas que (b) no pudo
hacer porque v9 no había registrado esas relaciones. Lo que se observa es más concreto:
**(c) no resolvió *todas* las identificaciones externas** (el barrio de los vecinos, la
ciudad del tranvía, el servicio, la red), mientras que (b) resolvió todas las que le
fueron entregadas. Repartido el crédito, (b) sigue delante: 85,1 % frente a 81,6 %.

**3. Las referencias llevan tres cosas distintas, y se fallan por separado.**
Identidad («Su» → la escuela), condición («la noche anterior» → «al jueves del corte»)
y sostén (el contenido de una capa que quedó en otra unidad: «la respuesta de la
empresa… de que la fecha ya estaba contratada»). Conviene que cada expectativa diga
cuál de las tres prueba.

**4. Lo que el paso 1 no registra deja de estar disponible para el paso 2.** En `doc4
U2` la relación «la causa **del corte**» no estaba registrada: (b) no la alcanzó y (c)
sí. En `doc4 [17] «la solicitud»`, v9 tampoco la registró y **el documento admite varias
lecturas plausibles** (la petición de `[8]`, la de `[14]`, el reclamo de `[15]`): (b)
propuso las que estaban a su alcance y (c) llegó a incluir también la de `[8]`. No es
que (b) inventara: es que **no pudo considerar** la lectura que quedó fuera. Aviso
metodológico: **detectar «esta expresión necesita un antecedente externo» no es una
comprobación mecánica** —reconocerlo exige interpretar—; el código puede listar
candidatas, no decidir.

**5. La duda viaja bien; lo que hay que vigilar es la resolución inventada.** Las dos
referencias sin resolver del conjunto se conservaron como duda en las tres entradas,
con sus dos lecturas, y ninguna corrida declaró que fueran distintas.

**6. Una cita literal no prueba que el uso sea correcto, y un respaldo no verificable
no es por sí solo un error de contenido.** La única deformación (DeepSeek en (b):
fundió «un corte similar» con el corte de este año y le atribuyó la duración del otro)
tenía citas perfectamente literales. Y en 63 crudos no hubo **ninguna** cita fuera del
material recibido. Son dos comprobaciones distintas: la forma por código; el contenido,
contra expectativas. Que un respaldo no se pueda verificar **sí es un problema de
respaldo**, aunque no demuestre por sí solo que el contenido esté mal.

**7. El campo `referente` mezcla identidad con condición y con contenido** («la red…
que llegó a tener veintiocho kilómetros de vías»; «la respuesta de la empresa… de que
la fecha ya estaba contratada»). Con la entrada (b) los cuatro controles de «esto no
debe importarse» se cumplieron, así que la frontera aguanta escrita en el prompt; pero
esos referentes largos son los que hay que mirar.

**8. Cambiar el prompt del paso 1 mueve la partición.** En `doc2`, v7 daba 4 unidades y
v8 dio 7. Por eso las expectativas por unidad solo valen contra una partición
congelada, y por eso las de doc4/doc5 tuvieron que corregirse (tres casos no
evaluables por escribir expectativas sin fijar el corte).

## 3. Costos

- **DeepSeek `deepseek-flash`:** **45 llamadas** (33 de desarrollo + 12 de la reserva),
  **590 789 tokens de salida** (441 768 + 149 021). 29–84 s por unidad; **85–90 % de lo
  generado es razonamiento**. La reserva tardó 646,2 s.
- **Muse Code:** 65 s–2 646 s por tarea con la misma entrada. Sirve para pocas tareas,
  no para una barrida de 30.
- **Tiempo comparado, solo DeepSeek:** (b) saca 20–34 s a las otras dos (3–5 %). La
  diferencia grande que se vio primero era una tarea de Muse de 44 minutos.
- **Fidelidad y costo no se pelearon:** la entrada más fiel fue también la más barata.

## 4. Lo que sigue sin saberse

- **Un solo juez**, sin segunda lectura de las casillas.
- **Sin réplicas por unidad y entrada:** una pasada permite decidir entre alternativas,
  no medir estabilidad. (Hay un indicio: tres unidades sin referencias, donde (a) y (b)
  son la misma entrada, dieron fichas distintas.)
- `doc5` sin Muse; la reserva no es independiente.
- **La referencia hacia adelante sigue sin ejercitarse** y todos los textos son cortos
  (14–17 oraciones).

## 5. Cómo correr esto la próxima vez

1. **Fijar el modelo y la partición antes de escribir expectativas**, y no moverlos
   durante la medición.
2. **Escribir primero qué se espera**, con un ítem por cosa (contenido, identidad,
   condición, duda) y contando por afirmación, no por campo del JSON. Cada ítem debe
   poder señalar el registro que lo satisface.
3. **Anunciar antes de cada tramo:** cuántas llamadas, con qué modelo, cuánto tarda y
   cuánto puede costar — **como estimación**, y volver a avisar si la medición la
   contradice.
4. **Una pasada por alternativa, y comparar solo lo que se midió igual.**
5. **Parar es parar:** no abrir el tramo siguiente hasta que se pida.
6. **Dos comprobaciones separadas:** forma por código (literales contra el material
   enviado) y contenido por juicio contra lo esperado.
7. **No usar ejemplos tomados de los documentos de prueba** ni esperar que un ítem se
   recupere sin haber fijado antes el corte de la unidad.
