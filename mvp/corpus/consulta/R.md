# R — las condiciones de la consulta

Se fija antes de correr y queda registrada con la corrida: si cambia, es otra corrida.

## Esbozo (lo lee el código para aplicar R)

```json
{ "fuentes_admitidas": ["solo el documento"],
  "herramientas": ["leer_caso", "entregar"],
  "operaciones": [] }
```

Si el esbozo y la prosa se separan, manda el esbozo y se corrige la prosa. Los topes de
turnos y de llamadas **no son R**: son guardias del orquestador.

## Prosa (lo que lee el agente)

- La respuesta se sostiene **solo con lo que el documento radicado establece**. Nada de fuera:
  ni internet, ni otras herramientas, ni otros agentes.
- **Tu saber no es premisa.** Lo que el documento no establece, no se responde.
- **No hay interacción con el usuario**: no se pregunta nada; se entrega.
- **No hay operaciones**: nada de aritmética ni de fechas calculadas. Si la respuesta exigiera
  un cálculo, no se responde.
- **Los conflictos se muestran, no se eligen**: si dos datos se oponen, se entrega la
  contradicción.
- **Lo que no se puede cerrar se entrega explícito**: «no establecido» y la duda, con la brecha
  nombrada. No se completa con una respuesta aproximada.
- **Si la respuesta no está en los datos de los casos que leíste**, pedí otros casos de la lista.
  Si agotás los casos disponibles, entregá el estado de «no está en los datos del corpus» con el
  reporte de lo que hiciste. No se inventa.
