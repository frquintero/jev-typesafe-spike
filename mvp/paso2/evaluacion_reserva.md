# Evaluación de la reserva · entrada (b) · 06-10-2026 (corregida)

Documentos `reserva_a.md` y `reserva_b.md` (sintéticos nuevos, sin los ejemplos
del prompt ni los textos de `mvp/pruebas/`). Expectativas fijadas antes de
cualquier llamada en `expectativas_reserva.md` (30 ítems: 15 por documento).

Partición: **v9 congelado**, una tarea de Muse por documento, sin correcciones a
mano (`salida_reservaA-v9.md`: 14/14 oraciones; `salida_reservaB-v9.md`: 15/15;
sin huecos ni solapes). 7 unidades en la reserva A y 5 en la B.

Extracción: candidato `prompt_ficha_contexto.md`, entrada (b),
`deepseek-flash`, 12 unidades, 32,9–80,5 s cada una (646,2 s en total).

**Esta reserva no es validación independiente:** la escribió el mismo que diseñó
el candidato y las expectativas, y es breve.

Detalle por ítem y respaldo: `evaluacion_items.md`.

## Recuperación estricta

| Medida | Resultado | Umbral |
|---|---|---|
| Recuperación estricta del contenido esperado | **29/29 = 100 %** | ≥ 90 % |

De las 30 expectativas, **una es defectuosa y se informa aparte**: la B11
(«del mismo autor»). Queda **una expectativa defectuosa** y **29 válidas**;
ninguna casilla quedó `parcial` ni `no`.

### La expectativa defectuosa, con su corrección

- **Lo que se fijó antes** (`expectativas_reserva.md`, ítem B11): «Una obra
  anterior **del mismo autor** se perdió en un incendio en 1975: el autor no está
  nombrado en el texto, así que la identificación queda sin resolver.»
- **Lo observado:** el crudo la resuelve como **relación** —«obra anterior del
  autor del mural del mercado viejo»—, que es lo que manda el prompt: la falta
  de nombre no vuelve irresoluble una referencia.
- **Conclusión:** era un defecto de la expectativa, no del prompt. Se conserva
  la expectativa original tal como se escribió y la corrección se registra aquí;
  **no se presenta como expectativa acertada fijada antes**.

## Fidelidad

| Medida | Resultado | Umbral |
|---|---|---|
| Afirmaciones producidas fieles y del foco | **70/70 = 100 %** | ≥ 90 % |

Ítems producidos (determinaciones + capas + acciones + relaciones; las marcas
van dentro de su determinación): **70**, todos con respaldo literal en la unidad
o en el respaldo de una referencia recibida, ninguno fuera del foco, ninguno
inventado. **0 respaldos no verificables en las 12 fichas.**

Ruido menor, que no es error: determinaciones que repiten el nombre del caso
(«la presidenta · rol = presidenta», «una filtración antigua · antigüedad =
antigua», «obra anterior · orden = anterior»).

## Ninguna importación indebida

Los cuatro controles «no debe importarse» se cumplieron: la unidad del hongo no
trajo 1998, las once familias ni las ferias; la del brote no trajo las ciento
cuarenta colmenas; la de la humedad no trajo 1962 ni los dieciocho metros; la de
la pérdida no trajo el encargo.

## Las dos medidas y su lectura

Las dos se alcanzan. Dos cosas que conviene no confundir:

- El 100 % de aquí **no contradice** el 70,8 % / 95,4 % / 84,6 % de desarrollo:
  es un conjunto más pequeño, con las referencias completas —todas las
  identidades externas venían dadas— y escrito por quien diseñó el candidato.
- Lo que sí se sostiene es que, **con las referencias completas, la entrada (b)
  recupera todo lo esperado en estos dos documentos sin importar nada ajeno**,
  dentro de los límites del evaluador (uno solo, sin réplicas).

## Los crudos de Muse de la reserva

`muse_reserva.sh` lanzó 7 tareas de la reserva A (entrada b): 6 dejaron crudo y
la U7 quedó lanzada sin resultado; la reserva B no llegó a lanzarse. Esos 6
crudos **quedan fuera del análisis** (corrida interrumpida) y no entran en los
totales de arriba.
