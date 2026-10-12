#!/usr/bin/env python3
"""Inserta MiMo-V2.6-Flash en mvp/proveedores.md. Idempotente."""
import pathlib

RUTA = pathlib.Path("mvp/proveedores.md")
t = RUTA.read_text(encoding="utf-8")

# --- 1) fila en la tabla de §1 ---
FILA_LUNA = "| `gpt-6-luna` — GPT 6 Luna (sin alias fijo en `ALIAS`) | OpenCode Go, familia `responses` | Etapa 2 (pruebas en `temp/`: low ×2, high ×2) |\n"
FILA_MIMO = "| `mimo-v2.6-flash` — MiMo-V2.6-Flash (sin alias fijo en `ALIAS`) | OpenCode Go, familia `chat/completions` | Etapa 2 (pruebas en `temp/`: low ×3, medium ×2, high ×3) |\n"
if "mimo-v2.6-flash` — MiMo" not in t:
    assert FILA_LUNA in t, "no encontré la fila de Luna"
    t = t.replace(FILA_LUNA, FILA_LUNA + FILA_MIMO, 1)

# --- 2) nota de mimo en §4 (etapa 3 abierta) ---
VIEJO4 = """proveedor por defecto para Etapa 3 queda abierto hasta hacer pruebas específicas sobre el
orquestador."""
NUEVO4 = """proveedor por defecto para Etapa 3 queda abierto hasta hacer pruebas específicas sobre el
orquestador.

Un candidato ya queda descartado para esta etapa sin necesidad de probarlo: **MiMo exige que
`reasoning_content` se devuelva completo en las rondas siguientes de un diálogo con herramientas, o
la API responde 400** (documentación de Xiaomi). `orq/bucle.py` hoy no lo hace, así que mimo no entra
en la etapa 3 sin tocar el bucle (§7)."""
if "Un candidato ya queda descartado para esta etapa" not in t:
    assert VIEJO4 in t, "no encontré el final de §4"
    t = t.replace(VIEJO4, NUEVO4, 1)

# --- 3) sección propia de MiMo ---
SECCION = """
## 7. MiMo-V2.6-Flash por OpenCode Go: contrato, costo y medidas (10-10)

**Modelo válido para la etapa 2**, con el contrato establecido y la calidad pendiente de la batería.

**Ruta, y es la fácil.** `POST https://opencode.ai/zen/go/v1/chat/completions`, que es la forma que
**ya consume nuestro transporte `openai_compatible`**: no hace falta transporte nuevo, al contrario
que Luna (§6). Clave `OPENCODE_API_KEY`; correr con `bash -ic '…'`.

**Corredor.** `temp/datos-test/paso2_seco_v1_mimo.py <doc> mimo <esfuerzo> <rN>`, que envuelve a
`paso2_seco_v1.py` y declara todo en memoria: el alias, el host en `CLAVE_POR_HOST` y la cabecera
`x-opencode-session`. **Si se adopta**, el registro necesita tres cosas: el alias con la URL de Go,
`opencode.ai → OPENCODE_API_KEY` en `claves.py`, y **una manera de poner cabeceras por alias** —hoy
no existe: el `extra` del registro va al cuerpo, no a las cabeceras—. Eso último vale para cualquier
modelo que se adopte por Go, no solo para mimo.

**Esfuerzos: `none`, `low`, `medium`, `high`.** Rechaza con 400 `minimal`, `xhigh`, `max` y cualquier
valor inventado. **El contrato hubo que sacarlo enumerando**, porque —a diferencia de Luna— **Go
opaca el error del upstream**: devuelve `{"error":{"param":"","type":"server_error","message":
"Upstream request failed: [400] Invalid request parameters"}}`, sin `param` y sin la lista de válidos.
De ahí una lección sobre el método: **la sonda del error no sirve igual en todas las familias de Go**.

Lo llamativo es que `reasoning_effort` **no está documentado en ninguna de las dos páginas** —Xiaomi
solo documenta `thinking`, y Go no documenta parámetros de razonamiento— y sin embargo **se valida**.
Hay un conjunto real detrás que nadie publica.

**`thinking` también pasa, y manda, pero no se valida.** `thinking: {"type": "disabled"}` da 0 tokens
de razonamiento y `reasoning_content` vacío; con `disabled` más `reasoning_effort: low`, el
razonamiento sigue en 0, o sea que `thinking` pisa al esfuerzo. Pero `thinking: {"type": "pepino"}`
devuelve **200 y piensa** (16 tokens): un error de tipeo ahí se acepta en silencio. **Por eso, para
apagar el razonamiento conviene `reasoning_effort: "none"`, que sí está validado:** un parámetro
validado falla de frente, uno sin validar miente.

**Precio, cupo y retención** (página de Go, 10-10-2026). Entrada US$0.14/1M, salida US$0.28/1M,
lectura de caché US$0.0028/1M, sin tramos por contexto. Cupo de **US$60/mes** en el plan Go, del orden
de 150.400 peticiones al mes según la estimación de la página. **No entrena y retiene 0 días**: el
mejor perfil de privacidad de todos los candidatos hasta hoy.

**El caché de Go funciona también en `chat/completions`, y sin hacer nada.** Desde la segunda llamada
reusó 2.048 de 2.066 tokens de entrada; no hizo falta mandar el `[SISTEMA]` por un campo aparte como
en `responses`: el prefijo invariante de `messages` basta.

**Medido sobre `preparacion_cafe`** (5 UT, `temp/prompt_DATOS_v1.md`), ocho corridas:

| esfuerzo | réplica | tiempo | salida | razonamiento | costo (USD) | datos |
|---|---|---|---|---|---|---|
| `low` | s4 | 29,0 s | 2.497 | 932 | 0.00099 | 32 |
| `low` | s4r2 | 26,7 s | 2.467 | 1.130 | 0.00070 | 30 |
| `low` | s4r3 | 20,0 s | 1.443 | **11** | 0.00041 | 31 |
| `medium` | s4 | 29,8 s | 2.583 | 1.355 | 0.00073 | 26 |
| `medium` | s4r2 | 38,4 s | 2.681 | 1.300 | 0.00076 | 30 |
| `high` | s4 | 31,0 s | 2.318 | 1.010 | 0.00066 | 28 |
| `high` | s4r2 | 18,5 s | 1.385 | **12** | 0.00040 | 29 |
| `high` | s4r3 | 40,6 s | 2.414 | 1.157 | 0.00068 | 27 |

Forma limpia en las ocho: parseo bien, 0 problemas, 0 avisos. Costo plano entre US$0.0004 y
US$0.0010 en todo el rango.

**Tres cosas que las ocho corridas sí establecen, y no son sobre calidad:**

**El nivel de esfuerzo no ordena el razonamiento.** `medium` pensó más que `high` en la mayoría de las
comparaciones posibles entre esos dos niveles, y la dispersión entre réplicas del mismo nivel es del
mismo orden que la dispersión entre niveles. El interruptor fiable es `none` frente a cualquier otro;
entre `low`, `medium` y `high` no hay escalera que subir con esta muestra.

**El modelo a veces decide no pensar, con independencia del nivel pedido:** 11 tokens en `low` s4r3 y
12 en `high` s4r2, en los dos casos con salida normal (31 y 29 datos, forma limpia) y la mitad de
tiempo y de costo. Es intermitente, no un rasgo del nivel.

**El tiempo es el más disperso del banco:** de 18,5 a 40,6 s con el mismo modelo y el mismo esfuerzo,
más del doble entre la más rápida y la más lenta. Para una fase que va a correr sobre muchos
documentos, esa dispersión pesa tanto como la media.

**Dos defectos observados, menores pero registrables.** En `high` s4r3 un valor salió con una falta de
ortografía —«por gravadad» donde el texto dice «gravedad»—: `forma()` no lo detecta ni puede, porque
no juzga contenido, así que es un fallo que **pasa la verificación sin ser visto** y rompe el cotejo
del valor con el texto. Y la notación de la unidad varía entre corridas: `°C` en siete y «grados
Celsius» en una, más un «minutos» en plural con el valor «menos de medio». Si la unidad va a servir
para comparar o convertir, habrá que normalizarla.

**La calidad de la extracción no está medida**, por lo que dice el aviso de §2: solo la **forma** quedó
establecida. Lo que sí hay es una **lectura de Frat (10-10): `low` le parece de más calidad** que
`medium` y `high`. Es el juicio de quien trae el interés, no una medición, y queda pendiente de
confirmación con la batería de preguntas.
"""
if "## 7. MiMo-V2.6-Flash" not in t:
    t = t.rstrip("\n") + "\n" + SECCION

RUTA.write_text(t, encoding="utf-8")
print("listo")
