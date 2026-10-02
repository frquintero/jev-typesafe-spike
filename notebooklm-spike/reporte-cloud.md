# API oficial de NotebookLM en Google Cloud

Alcance precisado por Frat el 2026-10-02: conectar código Python a la API oficial de Google Cloud, autenticar por OAuth y consumirla. La prueba anterior de endpoints internos (`api-r1`) no cierra esta tarea.

## Endpoint y contrato comprobados

Base REST: `https://discoveryengine.googleapis.com/v1alpha/`.

Crear notebook:

```text
POST /v1alpha/projects/PROJECT_NUMBER/locations/LOCATION/notebooks
Content-Type: application/json
{"title": "NBLM-CLOUD-SMOKE-001 ..."}
```

Leer notebook: `GET /v1alpha/projects/PROJECT_NUMBER/locations/LOCATION/notebooks/NOTEBOOK_ID`.

Cargar texto: `POST .../notebooks/NOTEBOOK_ID/sources:batchCreate`, con el cuerpo:

```json
{"userContents": [{"textContent": {"sourceName": "NBLM-SMOKE-001", "content": "texto sintético"}}]}
```

Autenticación: OAuth de Google Cloud, con scope `https://www.googleapis.com/auth/cloud-platform`; `google-auth` obtiene y adjunta el token a partir de credenciales ADC externas al repo. El código del repo no construye la cabecera de autenticación ni lee claves API. La sesión de la web de NotebookLM no se utiliza.

Los contratos se revisaron con Exa en documentación oficial y se contrastaron con el documento Discovery recibido directamente desde Python. Para multirregiones, la guía ofrece también los hosts `us-discoveryengine.googleapis.com`, `eu-discoveryengine.googleapis.com` y `global-discoveryengine.googleapis.com`; la ubicación debe corresponder a la configuración del proyecto.

## Qué se ejecutó y qué falta

- Se hizo una petición Python al documento público `https://discoveryengine.googleapis.com/$discovery/rest?version=v1alpha`: HTTP **200**, **1,497 s**. `rootUrl` confirmó `https://discoveryengine.googleapis.com/` y versión `v1alpha`.
- El contrato publicado incluye `create`, `get`, `listRecentlyViewed`, `share`, `batchDelete`, además de fuentes y audio. No publica un método de chat/consulta en ese recurso. No se sustituyó por un endpoint interno.
- Dos intentos previos de reducir el documento mediante `fields` devolvieron HTTP 400. El segundo cuerpo explica que el selector de campos no se admite como se envió; el tercero sin `fields` devolvió el documento. Se conservan los intentos en carpetas separadas.
- Esto comprueba acceso al endpoint público de descripción. **No comprueba autenticación ni consumo de notebooks de un proyecto.**
- Antes de la instalación: `gcloud` ausente del PATH; directorio convencional de configuración gcloud y ADC ausentes; `GOOGLE_APPLICATION_CREDENTIALS`, `GOOGLE_CLOUD_PROJECT` y `GCLOUD_PROJECT` no configuradas en el entorno inspeccionado. No se buscaron secretos por vías alternativas.
- Al preparar el script faltaban proyecto, ubicación y credenciales OAuth. El avance de autenticación se registra debajo.

Google documenta como requisitos un proyecto con facturación y Discovery Engine habilitados, permisos Cloud NotebookLM y licencia Enterprise. La cuenta que abre la web de consumo no acredita por sí sola estos requisitos.

### Autenticación configurada por Frat (2026-10-02)

Frat instaló Google Cloud SDK 587.0.0 y completó `gcloud auth application-default login`. Se comprobó que el archivo ADC existe fuera del repo y es de tipo `authorized_user`, con refresh token presente, sin imprimirlo. `gcloud config get-value project` devolvió `(unset)`; ADC aún no tiene `quota_project_id`.

Python utilizó esas ADC y ejecutó una lectura autenticada de Cloud Resource Manager (`projects.search`): **HTTP 200**, 14 proyectos, sin página adicional. Esto acredita autenticación OAuth y acceso a ese servicio Cloud; todavía no acredita permisos ni licencia de NotebookLM. Se pidió a Frat elegir el proyecto. El inventario completo no se guardó en el repo; los metadatos observados están en `cache/cloud-auth-r1/observations.json`.

### Proyecto exclusivo creado (2026-10-02)

Frat eligió crear «NotebookLM Spike». `crear_proyecto_cloud.py` ejecutó `POST https://cloudresourcemanager.googleapis.com/v3/projects` con `projectId: notebooklm-spike-20261002` y `displayName: NotebookLM Spike`; siguió la operación con dos lecturas hasta su finalización. Proyecto **ACTIVE**, número **265423575040**. Creación y comprobaciones: cinco respuestas HTTP 200, conservadas en `cache/cloud-setup-r1/`.

Las lecturas de Cloud Billing y Service Usage confirmaron `billingEnabled: false` y Discovery Engine `DISABLED`. No se asoció una cuenta de facturación ni se compraron licencias. La lectura adicional de cuentas de facturación devolvió tres cuentas, una abierta; el inventario permanece en almacenamiento privado fuera del repo.

Siguiente acción preparada: asociar el proyecto a la cuenta abierta «My Billing Account 1» y habilitar Discovery Engine, previa autorización de Frat para la asociación de cobros. La licencia Enterprise y la configuración de identidad siguen pendientes. Consultadas mediante Exa: la [documentación de licencias](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/set-up-licensing) describe una prueba gratuita de 14 días; la [página comercial](https://cloud.google.com/gemini-enterprise/gemini-notebook) anuncia 30 días y USD 9 por licencia/mes, mínimo 15 licencias. Las condiciones concretas de la prueba deben verificarse en la consola antes de activarla; no se activó ninguna suscripción.

El smoke `smoke_cloud.py` todavía no se ejecutó contra este proyecto. Crear el proyecto y leer la configuración no acreditan funcionamiento de la API de notebooks.

## Código listo para el smoke autenticado

`smoke_cloud.py` usa `google-auth==2.59.1` y `requests==2.34.2`, instalados en el entorno aislado existente. Verificación realizada: compilación Python y `--help`; el recorrido autenticado aún no se ha ejecutado.

Con los valores reales y ADC ya configuradas fuera del repo:

```bash
export HTTPS_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
/home/fratquintero/.local/share/nblm-spike/venv/bin/python notebooklm-spike/smoke_cloud.py cloud-r1 \
  --project-number NUMERO_REAL --location UBICACION_REAL \
  --credentials-file /ruta/externa/credenciales-adc.json
```

El script crea un notebook exclusivo, lo recupera, carga el texto sintético y consulta la fuente hasta recibir `SOURCE_STATUS_COMPLETE` o agotar el tiempo. Conserva el notebook. Detiene fallos HTTP/autenticación sin repetir mutaciones; cada réplica requiere carpeta nueva. Registra cuerpos exactos sin tokens. No habilita facturación, compra licencias ni modifica IAM.

## Fuentes

- [Administración de notebooks (guía)](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks).
- [Contrato REST create](https://docs.cloud.google.com/gemini/enterprise/docs/reference/rest/v1alpha/projects.locations.notebooks/create).
- [Fuentes y texto sintético](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/api-notebooks-sources).
- [Configuración de NotebookLM Enterprise](https://docs.cloud.google.com/gemini/enterprise/notebooklm-enterprise/docs/set-up-notebooklm).
- [Autenticación ADC local](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment).
- Contrato recibido desde el servicio: `cache/cloud-preflight-r3/response.json`; petición, estado y resumen junto a ese archivo.
