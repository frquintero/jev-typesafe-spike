# Smoke notebooklm-py — py-r1

Intento autorizado por Frat el 2026-10-02, iniciado a las 17:26:37 UTC (12:26:37 Bogotá). **S0–S3 incompleto: detenido en autenticación S0.**

## Observaciones

- Cliente `notebooklm-py==0.8.4`, Python 3.12, backend Web/HTTP. Sesión anterior adaptada al storage del nuevo cliente, conservando cuenta `authuser=1`; archivo privado externo al repo con permisos 0600.
- `GET /?authuser=1` devolvió HTTP 302; se siguió a `/login`, que devolvió otro HTTP 302 hacia `accounts.google.com`. El hook detuvo el intento antes de seguir a Google Accounts.
- Dos GET, 0,493 s, salida del script 1. Sin reintentos de autenticación, creación de cuadernos, cargas ni consultas generativas. S0 no completó lectura del cuaderno/cupos; S1–S3 no se ejecutaron.
- La sesión guardada no fue aceptada; no se estableció si por caducidad, invalidación u otro requisito. Renovar sesión antes de otra réplica; conservar `py-r1`.

## Entradas previstas, no enviadas

Texto (`docs/smoke-001.txt`):

```text
En el ensayo ficticio NBLM-SMOKE-001, el recipiente Luma contenía 17 fichas violetas. El recipiente Neri contenía 8 fichas blancas.
```

Pregunta (`prompts/smoke-001.txt`):

```text
Según la fuente, ¿cuántas fichas contenía Luma y de qué color eran? Incluye la cita que respalda la respuesta.
```

Esperado: 17 fichas violetas con fuente/pasaje recuperables. Lectura inicial prevista: cuaderno sintético `f113873f-7fdb-416a-bb83-d429c4a3ce1b`.

## Evidencia y reproducción

`cache/py-r1/` contiene las dos peticiones, metadatos de sus respuestas y `summary.json`. Sin HTML de autenticación ni cookies/tokens/cabeceras privadas. La redirección a Google Accounts se detectó en `Location`; no se guardaron sus parámetros privados.

`smoke_py.py` implementa S0–S3, registros HTTP redactados y reconexión en otro proceso. Instrumenta `httpx.AsyncClient` y el punto interno `WebSessionAuth.refresh_base` de la versión fijada para detener recuperación automática; no modifica el paquete instalado. La biblioteca gestiona cookies; el script no construye `Authorization` ni lee claves de API.

Tras el fallo se migraron argumentos deprecados a `ClientConfig` y se adelantó el registro de entradas para futuros fallos de apertura. Compilación comprobada; no se repitió la llamada con la sesión rechazada. Las ramas S1–S3 aún no están validadas por ejecución. No hubo búsqueda web en esta corrida; se usó la revisión anterior y el código instalado.

Comando ejecutado:

```bash
export HTTPS_PROXY=http://127.0.0.1:8080
export SSL_CERT_FILE="$HOME/.mitmproxy/mitmproxy-ca-cert.pem"
/home/fratquintero/.local/share/nblm-spike/venv-notebooklm-py/bin/python notebooklm-spike/smoke_py.py py-r1 --session-file /home/fratquintero/.local/share/nblm-spike/auth-import/iab-r1.json --storage /home/fratquintero/.local/share/nblm-spike/auth-py-r1/storage_state.json
```

Próxima corrida: sesión renovada, `py-r2` y storage externo nuevo. No sobrescribir `py-r1`.
