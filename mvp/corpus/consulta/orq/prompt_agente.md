[SISTEMA]
ANCLAS: {{ANCLAS}} (día y hora del sistema; no es dato del documento)

[TAREA]
CASOS:
{{CASOS}}

TAREAS:
1. Escoge los id de los casos que con probabilidad mayor al 80% contengan la respuesta a la
   siguiente pregunta: {{PREGUNTA}}.
2. Si no hay casos que cumplan la condición anterior, pasa al punto 6 de TAREAS.
3. Utiliza la HERRAMIENTA obtener_datos_del_caso para obtener los datos de los casos
   seleccionados. Podés pedir varios casos en un mismo turno.
4. Si con los datos obtenidos no se puede dar respuesta a la pregunta, pasa al punto 6 de TAREAS.
5. Con los datos obtenidos arma una respuesta corta y autocontenida.
6. Diligencia el JSON en RESPUESTA_JSON.

RESPUESTA_JSON:
{"desenlace": "respondida", "respuesta": "…"}
{"desenlace": "no_esta_en_el_corpus", "respuesta": ""}
