# Smoke de conectividad — NBLM-SMOKE-001

## Alcance vigente: API oficial Google Cloud

Frat precisó que el smoke debe conectar Python a la API oficial de Google Cloud, autenticarse por OAuth y consumirla. `smoke_cloud.py` implementa creación/lectura de notebook y carga/lectura de la fuente sintética usando `google-auth` y credenciales ADC externas al repo. Proyecto y ubicación deben venir de Frat o de configuración existente; no se inventan. No hay `gcloud`, ADC ni proyecto configurado en esta máquina al comprobarlos el 2026-10-02. Endpoint, autenticación y contratos se contrastaron con documentación oficial mediante Exa. La documentación de administración de notebooks no presenta un método de chat/consulta; no se sustituye con endpoints internos.

La corrida anterior de sesión web que sigue documentada abajo no cumple el alcance Cloud. Se conserva sin alterar sus crudos.

Fecha: 2026-10-02. Inicio autorizado por Frat. Solo texto sintético.

## Entrada fijada antes de consultar

- Texto: `docs/smoke-001.txt`.
- Consulta: `prompts/smoke-001.txt`.
- Esperado: Luma contenía 17 fichas violetas; referencia recuperable al pasaje que lo establece.
- Notebook exclusivo de prueba, una única fuente; conservarlo para revisión.

## Pasos y evidencias

1. Comprobar acceso autenticado de lectura.
2. Crear notebook exclusivo con identificador único.
3. Cargar el texto y esperar a que esté disponible.
4. Consultar con el texto exacto del prompt.
5. Recuperar por API la referencia de la cita y el texto de la fuente vinculada.
6. Registrar operaciones, respuestas, tiempos observados y errores sin credenciales ni información de notebooks personales. Preservar cada intento en una carpeta nueva.

## Vías

- Cliente local aislado: `notebooklm-mcp-cli==0.15.0`, instalado fuera del repo en `~/.local/share/nblm-spike/venv/`; perfil previsto `nblm-spike` en almacenamiento externo al repo. El primer intento de login terminó con `Login timeout` tras 300 s; Frat mostró un error de certificado en el Chrome lanzado. No se demostró autenticación del cliente.
- Frat indicó usar el navegador interno y completó allí el inicio de sesión. La prueba por interfaz web se registra por separado: no acredita acceso HTTP autónomo desde Python ni continuidad con el PC apagado.
- La configuración de acceso desde la nube queda para una prueba posterior.

## Corrida HTTP autorizada

Frat pidió ejecutar el smoke de API el 2026-10-02. `smoke_api.py` usa el cliente comunitario como biblioteca y `httpx` como transporte HTTPS. La sesión que Frat inició en el navegador interno se exportó a un archivo privado fuera del repo (directorio 0700, archivo 0600); durante la corrida no se usa control del navegador. Se conserva la cuenta elegida con `authuser=1`, también en la petición de consulta, cuyo cliente HTTP es distinto del empleado por las RPC.

- Réplica: `api-r1`; carpeta exclusiva `cache/api-r1/`.
- Lectura inicial: solo el notebook sintético de la prueba previa; no listar notebooks personales.
- Peticiones: `Content-Type` de formulario y `User-Agent: spike-jev/1.0`; autenticación de sesión gestionada por la biblioteca. Sin claves de API ni construcción de `Authorization` en código del repo.
- Sin transporte CDP, renovación automática de autenticación ni repetición de mutaciones ante fallos. Un fallo de autenticación detiene el intento.
- Proxy y certificado locales exportados solo para el comando de corrida.
- Conservar cuerpos recibidos y `f.req` exacto, omitiendo cookies, `at`, `f.sid` y cabeceras de autenticación; respuestas con eventual información de sesión redactada.
- El resultado de esta corrida se documenta en `reporte-api-r1.md` y en sus crudos; no mide calidad general de extracción ni disponibilidad desde la nube.
