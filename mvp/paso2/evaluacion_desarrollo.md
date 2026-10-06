# Evaluación de la comparación de entradas · 06-10-2026 (segunda cuenta)

Corrige y sustituye la primera versión. La revisión de Astra destapó dos celdas
mal contadas; al rehacerlas se encontró que el defecto era de la regla de conteo, no
solo de esas dos celdas. **Ninguna llamada nueva.**

## La regla, ahora atómica

Cada ítem esperado prueba **una sola cosa**, y hay cuatro clases:

- **contenido**: una afirmación que la propia unidad establece;
- **identidad o relación externa**: completar de quién o de qué se habla con material
  de otra oración (la empresa **de acueducto**, la red **del tranvía**, la causa **del
  corte**), o la relación entre dos casos;
- **condición o marca**: el punto de referencia que una oración necesita;
- **duda**: conservar dos lecturas sin elegir.

Una casilla cuenta **solo si aparece lo que el ítem pide**. Antes, varios ítems
mezclaban contenido e identidad: si estaba el contenido se concedía el ítem entero.
Eso infló la cuenta. Al separarlos, el denominador sube (doc4 pasa de 25 a 32 ítems;
doc5, de 17 a 23) y las casillas se pueden auditar una por una.

Casillas = ítems × corridas de esa entrada en esa unidad (doc4 tiene dos modelos, doc5
uno).

## doc4 (32 ítems; 64 casillas por entrada)

| Unidad (ítems) | (a) | (b) | (c) | Lo que decide la diferencia |
|---|---|---|---|---|
| U1 (6) | 12/12 | 12/12 | 12/12 | sin identidades externas |
| U2 (6) | 10/12 | 10/12 | **12/12** | «la causa **del corte**»: solo (c) lo completa (v9 no registró esa relación) |
| U3 (4) | 1/4 | **4/4** | 2/4 | (a) deja «la empresa» y «los vecinos» sin identificar; (c) no identificó el barrio |
| U4 (5) | 3/6 | 5/6 | 5/6 | (a) sin «de acueducto» ni «el jueves» |
| U5 (4) | 6/8 | 6/8 | **8/8** | (a) sin la relación de semejanza; en (b) DeepSeek fundió los dos cortes |
| U6 (7) | 10/14 | **14/14** | **14/14** | (a) sin «de acción comunal» ni la empresa de la respuesta |
| **Total** | **42/64 = 65,6 %** | **51/64 = 79,7 %** | **53/64 = 82,8 %** | |

## doc5 (23 ítems; 23 casillas por entrada, solo DeepSeek)

| Unidad (ítems) | (a) | (b) | (c) | Lo que decide la diferencia |
|---|---|---|---|---|
| U1 (3) | 3/3 | 3/3 | 3/3 | sin identidades externas |
| U2 (7) | 4/7 | **7/7** | 5/7 | (a) sin la compañía inglesa, sin la ciudad del tranvía, sin el servicio del tranvía; (c) tampoco completó «la ciudad» ni «el servicio» |
| U3 (5) | 4/5 | **5/5** | 4/5 | (c) no completó «la red del tranvía» |
| U4 (4) | 3/4 | **4/4** | 3/4 | (c) no completó «los tranvías de la ciudad» |
| U5 (4) | 3/4 | **4/4** | 3/4 | (b) registró la duda de cuál taller; (a) y (c) no |
| **Total** | **17/23 = 73,9 %** | **23/23 = 100 %** | **18/23 = 78,3 %** | |

## Total del conjunto

| Entrada | Recuperación (87 casillas) | Fidelidad |
|---|---|---|
| (a) unidad sola | 59/87 = **67,8 %** | 103/103 = 100 % |
| (b) unidad + referencias | 74/87 = **85,1 %** | 111/113 = **98,2 %** |
| (c) unidad + documento | 71/87 = **81,6 %** | 103/103 = 100 % |

Fidelidad: ítems producidos fieles y del foco. La única deformación (DeepSeek en
`doc4 (b) U5`) afecta a dos ítems producidos: le atribuyó al corte de este año la
duración y los efectos del corte del año pasado.

**Ninguna entrada alcanza el 90 % de recuperación en desarrollo.** La mejor es (b),
a 5 puntos del umbral; (c) queda 3,5 puntos por debajo de (b), y (a) 17 puntos.

## Las celdas que estaban mal en la primera cuenta

1. `doc4 U2 (a)`: se concedió el ítem «la causa del corte» y el crudo solo dice «la
   causa → la reparación de una tubería matriz» (verificado en los dos modelos).
2. `doc4 U5 (a)`: se concedió «el corte similar no es el de este año, unidos por la
   semejanza», y el crudo tiene un solo corte, ninguna relación y una duda explícita.
3. `doc4 U4 (a)`: se concedió «la empresa respondió» con la empresa sin identificar y
   «la fecha» sin el jueves; ahora son ítems aparte y no se conceden.
4. `doc4 U6 (a)`: lo mismo con «la junta de acción comunal» y con la empresa de la
   respuesta.

## Expectativas de referencia (aparte de los 87)

| Modelo | (a) | (b) | (c) |
|---|---|---|---|
| DeepSeek (19) | 2/19 | 18/19 | 11/19 |
| Muse (11, solo doc4) | 2/11 | 11/11 | 8/11 |

En (a) solo se conservan las dos referencias sin resolver, como duda. En (b) falla una:
la fusión de DeepSeek. En (c) se pierden las identificaciones que el modelo no
completó y, con Muse, las tres de `doc4 U3` por el JSON inválido.

## Consecuencia para la selección

Con la cuenta auditable, **(b) es la mejor de las tres** y queda como **base de trabajo
del paso 2**. En desarrollo ninguna entrada alcanza el 90 %, pero eso no cierra nada:
en desarrollo la comparación **solo elige la entrada**, y las dos medidas se aplican en
la reserva, donde (b) alcanzó 30/30 ítems y 70/70 producidos (véase
`evaluacion_reserva.md`).

## Defectos que quedan dichos

- El juez es uno; ninguna de estas casillas tiene segunda lectura.
- No hay réplicas por unidad y entrada: la estabilidad no está medida.
- `doc5` no tiene corridas de Muse.
- Los ítems de identidad externa que fallan en (b) son, en varios casos,
  *inalcanzables* con lo que v9 registró (U2 no tiene ninguna referencia): miden lo que
  el paso 1 entrega al paso 2, no un defecto de la entrada.
