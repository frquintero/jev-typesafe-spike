# PLAN — NotebookLM, grafo semántico

Una sección por ronda. Plan general en `README.md`; estado en `tareas.md`.

## Ronda FU1: ficha por unidad, DeepSeek frente a NotebookLM (gen1, una réplica)

**Cambio.** Primera corrida del paso 2 de la arquitectura mixta. Las unidades
son las del paso 1 de DeepSeek sobre gen1
(`unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json`; las tres
réplicas son idénticas): U1 `[1, 2, 3]`, U2 `[4]`, U3 `[5, 9]`, U4
`[6, 7, 8]`, U5 `[10]`. Cada unidad conserva sus números de oración
originales («[5] … [9] …»). El mismo prompt, `unidades/prompts/ficha_v1.md`
sin cambios, con dos extractores:

- **DeepSeek** (`ficha_unidad_deepseek.py`): una llamada por unidad; el texto
  de la unidad entra en `{{TEXTO_NUMERADO}}`.
- **NotebookLM** (`ficha_unidad_nblm.py`): un cuaderno; el prompt va en
  `chat.configure` (`goal` CUSTOM, `response_length` LONGER; 6.4 mil
  caracteres frente al tope de 10 mil que documenta el cliente, no verificado
  en la cuenta), con `{{TEXTO_NUMERADO}}` remitido a la fuente. Cada unidad
  es una fuente aparte. Una pregunta corta por unidad con
  `source_ids=[esa unidad]`; tras cada una se borra la conversación (sin
  borrarla, el siguiente `ask` hereda el historial). Al final, una **sonda de
  aislamiento**: desde U2 (oración 4) se pregunta la altura del Tumbal, que
  solo está en U3.

Única pregunta enviada a NotebookLM por unidad: «Reconstruye la ficha JSON
del texto de la fuente seleccionada, según tus instrucciones. Responde solo
con el JSON.» Remisión en la sección TEXTO del prompt: «El texto con sus
oraciones numeradas es la fuente seleccionada en cada pregunta.»

**Conjetura.** NotebookLM, por el chat y con las reglas en los ajustes del
cuaderno, produce por unidad una ficha comparable a la de DeepSeek (forma
completa, respaldos literales, contenido parecido), en menos tiempo por
unidad, y respeta el foco de `source_ids`.

**Instrumento y criterios (fijados antes de correr; juzgan Frat y Cowork
leyendo).** `ficha_v1` midió 95 % por documento entero; por unidad es otro
régimen, así que la vara es la comparación pareada, no ese número.

1. **Gold de gen1** (`unidades/gold/gen1.json`, numeración original
   conservada). La ficha registra todo, así que los 13 ítems deben aparecer
   en la ficha de su unidad: los 6 `firmes` (or. 5–8) y el `borde` (or. 5)
   como determinaciones; los 6 `no_dato` (or. 1, 2, 3, 4, 9, 10) también,
   como genéricos o valoraciones con su modalidad. Se cuenta, por
   extractor, cuántos se recuperan bien.
2. **Qué agrega o deforma**, con los 11 errores de la memoria (§2.4) como
   guía; se admiten errores nuevos.
3. **El referente perdido por partir:** U4 empieza con «Su última
   erupción», cuyo antecedente (el Tumbal) está en U3. Se mira qué hace cada
   extractor: inventarlo sin marca, marcarlo `inferido`, registrarlo en
   `dudas` o dejarlo sin caso.
4. **Mecánica:** respaldos literales (verificador), las siete listas,
   errores de parseo; en NotebookLM, `fuente_igual_al_texto`, citas fuera de
   la unidad y si las marcas `[n]` del chat contaminan los valores.
5. **Aislamiento:** la sonda debe responder que la fuente no lo establece; si
   da «2300 metros» o cita otra fuente, la selección se filtró.
6. **Tiempo:** segundos por unidad y total, por extractor.

gen1 es reserva: con una sola corrida y sin iterar sobre ella, sigue
sirviendo.

**Antes de ejecutar:** `git pull --ff-only` (copia limpia); comprobar que
no existen `nblm-grafo-semantico/cache/fu-gen1-deepseek-ficha_v1-r1.json` ni
`nblm-grafo-semantico/cache/fu-gen1-nblm-ficha_v1-r1.json`. No correr
`notebooklm auth check` ni listar cuadernos; no leer el archivo de sesión.

**Comandos** (desde la raíz; los dos pueden correr en paralelo):

```bash
# 1. DeepSeek (con el proxy)
export HTTPS_PROXY=http://127.0.0.1:8080 SSL_CERT_FILE=$HOME/.mitmproxy/mitmproxy-ca-cert.pem
python3 nblm-grafo-semantico/ficha_unidad_deepseek.py gen1 deepseek ficha_v1 r1 \
  unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json

# 2. NotebookLM (sin el proxy)
env -u HTTPS_PROXY -u SSL_CERT_FILE \
  /home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python \
  nblm-grafo-semantico/ficha_unidad_nblm.py gen1 ficha_v1 r1 \
  unidades/cache/unidades-gen1-deepseek-unidades_v5-r1.json \
  --storage /home/fratquintero/.notebooklm/profiles/nblm-spike/storage_state.json \
  --sonda-unidad U2 --sonda-pregunta "¿Qué altura tiene el volcán Tumbal?"
```

Si uno falla, no reintentar ni cambiar nada: conservar crudos y reportar.

**Reporte (sin veredicto), en `nblm-grafo-semantico/reporte-FU1.md`:** por
extractor y por unidad: segundos, modelo efectivo (DeepSeek), conteo de las
siete listas, fragmentos y no literales, errores de parseo; en NotebookLM,
`fuente_igual_al_texto`, citas totales y fuera de la unidad, y la respuesta
de la sonda verbatim con sus citas. Totales de tiempo por extractor. El JSON
`parsed` de cada unidad, tal como llegó, en un anexo (gen1 es corto). Commit
de los crudos y del reporte, y push.
