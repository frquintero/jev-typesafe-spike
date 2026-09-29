# Diseño de evaluaciones — unidades temáticas

Segmentación del prompt 1 (`unidades_v5`, DeepSeek). Oraciones numeradas en el orden del texto.

## 1. El propósito de las evaluaciones, su dificultad y la orientación de claude-api

1. Las evaluaciones proporcionan una señal sobre cómo se está desempeñando tu aplicación o skill en tareas específicas.
2. Sin embargo, diseñar evaluaciones y mejorar el rendimiento en ellas sin engañarte a ti mismo es difícil.
3. Hemos añadido orientación para ambas cosas a la skill `claude-api`.
4. Con esta skill, puedes ejecutar `/claude-api build-eval` para construir una evaluación dentro de tu base de código, y ejecutar `/claude-api hillclimb` para mejorar tu aplicación con respecto a esa evaluación, un cambio a la vez, utilizando un conjunto de ejemplos reservados (held-out set) para detectar sobreajuste (overfitting).

## 2. La estructura y el cierre del artículo

5. En este artículo, primero destacamos los principios de un buen diseño de evaluaciones y del hillclimbing, y después mostramos cómo Claude Code, utilizando la skill `claude-api`, aplica esos principios.
6. Cerraremos mostrando algunos ejemplos de estos comandos.

## 3. Las tareas de evaluación que reflejan la producción

7. Las evaluaciones bien diseñadas tienen algunos elementos en común (Figura 1): Las tareas de evaluación reflejan la producción.
8. Selecciona muestras de las tareas que te importan en “producción”, o en el entorno en el que se utilizará la capacidad o aplicación que estás probando.
9. En ocasiones, las tareas se eligen porque son fáciles de generar o fáciles de calificar.
10. Sin embargo, es importante asegurarse de que la distribución de las tareas represente aquello que realmente te importa.

## 4. La mejora del rendimiento con modelos más potentes y mayor razonamiento

11. El rendimiento mejora con modelos más potentes y con mayor razonamiento.
12. Los modelos con mayores capacidades y los niveles de esfuerzo más altos normalmente deberían obtener mejores resultados en una evaluación.
13. Si no ocurre así, con frecuencia el rendimiento está siendo limitado por tareas ambiguas o por un evaluador mal calibrado.

## 5. El margen superable en la frontera de la evaluación

14. Existe margen “superable” (passable headroom) en la frontera.
15. El modelo más capaz, funcionando con el máximo nivel de esfuerzo, debería encontrarse claramente por debajo del 100 % en la evaluación; de lo contrario, no puedes juzgar de manera fiable cómo afectan los cambios al rendimiento.
16. Es importante que esta diferencia no se explique por tareas imposibles o ambiguas: una señal habitual de ello es que una tarea falle en todas las ejecuciones de la evaluación, independientemente del número de réplicas.
17. Una buena tarea es aquella en la que dos expertos del dominio llegarían al mismo veredicto y todo lo que comprueba el evaluador está expresado explícitamente en la tarea.

## 6. La baja variación entre ejecuciones y sus causas

18. Baja variación entre ejecuciones.
19. Una alta variación suele deberse a tareas mal diseñadas o ambiguas, o a un evaluador que produce veredictos diferentes ante una salida idéntica.
20. La variación también puede estar oculta en la configuración.
21. Por ejemplo, el nivel de esfuerzo puede no aplicarse de manera consistente.
22. Además, el entorno puede afectar los resultados de la evaluación: el estado residual de una prueba anterior —un archivo, un historial de Git— puede proporcionarle al agente la respuesta.
