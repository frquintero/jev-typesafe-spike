# NotebookLM — exploración de API

- **Origen:** evaluar NotebookLM como posible extractor para Zettel/Jev.
- **Objetivo:** explorar conexión, respuestas, citas, formatos, tiempos y límites.
- **Criterio futuro:** ≈90 % de contenido correcto, coste bajo y ejecución ágil.
- **Acceso:** HTTP directo o cliente existente. MCP se evaluará después.
- **Aislamiento:** scripts, textos sintéticos y resultados propios en esta carpeta; conservar el trabajo previo.

## Plan

1. [ ] **Verificar API y autenticación:** endpoints, contratos y operaciones de carga/consulta.
   - Enterprise: proyecto Google Cloud, servicio habilitado, licencia, permisos y autenticación.
   - Interfaz interna: cuenta con acceso, sesión autenticada y tokens; revisar el cliente existente.
   - Documentar disponibilidad y requisitos de cada vía; habilitar acceso desde la nube.
2. [ ] **Smoke test:** crear notebook de prueba → cargar texto breve → esperar procesamiento → consultar con cita. Éxito: respuesta sobre el texto y respaldo recuperable.
3. [ ] **Explorar:** hechos, atribuciones, condiciones, JSON, preguntas sin respuesta y selección de fuentes.
4. [ ] **Dimensionar:** calidad observada, latencia total, cupos, longitud, errores y continuidad con el PC apagado.
5. [ ] **Diseñar la prueba independiente de extracción** según resultados.

## Registro

Por intento: texto/petición exactos, ruta y versión del cliente, respuesta cruda sin credenciales, citas, duración y resultado. Identificadores únicos; secretos fuera del repo.

**Estado:** smoke test pendiente de configurar acceso; el proxy local no se transfiere a la nube.

## Referencias

- [API oficial Enterprise](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks)
- [Interfaz interna y cliente comunitario](https://github.com/jacob-bd/gemini-notebook-mcp-cli/blob/main/docs/API_REFERENCE.md)
