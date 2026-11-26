# UMBook — código

Aplicación de gestión de usuarios: registro, inicio de sesión e invitación por correo. Backend Flask (API REST) y frontend Angular. Trabajo de Ingeniería de Software.

El código parte del repositorio de una compañera del grupo, con correcciones de seguridad y un frontend nuevo. Qué se cambió y por qué: [`../README.md`](../README.md).

## Qué se puede hacer

| Caso de uso | Función |
|---|---|
| CU0006 Registrar Usuario | Crear una cuenta con nombre, correo y contraseña (al menos 8 caracteres) |
| CU0001 Iniciar Sesión | Entrar con correo y contraseña; se recibe un token JWT |
| CU0010 Invitación a la aplicación | Con la sesión iniciada, mandar a otra persona un correo de invitación con el enlace de registro. La invitación queda guardada con su estado (enviada o fallida) |

## Requisitos

- Python 3.10 o más nuevo (probado con 3.14).
- Node.js y npm, para el frontend (Angular 22; probado con Node 24).
- No hace falta instalar una base de datos: SQLite viene con Python.

## Cómo arrancarlo

### Backend (puerto 5000)

Desde la carpeta `backend/`:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

cp .env.example .env          # completar JWT_SECRET_KEY y los datos de correo
python run.py                 # crea instance/umbook.db si no existe
```

> **Nota:** la ruta de esta carpeta tiene espacios (`4. Implementacion`), y los programas sueltos del entorno virtual (`pip`, `pytest`) no funcionan en rutas con espacios. Por eso se usa `python -m pip` y `python -m pytest`.

El servidor escucha solo en `127.0.0.1`. Para el modo debug de Flask, `FLASK_DEBUG=1` en `.env` (solo en desarrollo).

### Frontend (puerto 4200)

En otra terminal, desde `frontend/`:

```bash
npm install
npx ng serve                  # abre http://localhost:4200
```

## Configuración (`backend/.env`)

Se crea copiando `backend/.env.example`. No se sube al repositorio.

| Variable | Obligatoria | Para qué sirve |
|---|---|---|
| `JWT_SECRET_KEY` | **Sí** | Firma los tokens de sesión. Sin ella, o con un valor de ejemplo, la aplicación no arranca. Generarla con `python -c "import secrets; print(secrets.token_hex(32))"` |
| `SQLALCHEMY_DATABASE_URI` | No | Por defecto `sqlite:///umbook.db`, dentro de `instance/` |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS` | Para enviar correo | Por defecto Gmail: `smtp.gmail.com`, 587, TLS activado |
| `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` | Para enviar correo | `MAIL_PASSWORD` es una *app password* de Gmail (https://myaccount.google.com/apppasswords), no la clave de la cuenta |
| `MAIL_SUPPRESS_SEND` | No | `true` simula el envío: sirve para probar sin mandar correos |
| `MAIL_TIMEOUT` | No | Segundos que espera cada operación SMTP antes de dar el envío por fallido. Por defecto 5 |
| `CORS_ORIGIN` | No | Origen del frontend. Por defecto `http://localhost:4200` |
| `FRONTEND_URL` | No | Dirección del frontend, para el enlace de registro del correo de invitación. Por defecto `http://localhost:4200` |
| `FLASK_DEBUG` | No | `1` activa el modo debug. Por defecto apagado |

## API

| Método y ruta | Sesión | Qué hace | Respuestas |
|---|---|---|---|
| `POST /auth/register` | — | Registra un usuario (`name`, `email`, `password`) | 201 · 400 datos inválidos · 409 correo ya registrado |
| `POST /auth/login` | — | Inicia sesión (`email`, `password`) y devuelve `access_token` | 200 · 400 campos vacíos · 401 credenciales incorrectas |
| `POST /invite` | JWT | Guarda la invitación y la envía por correo (`email`) | 200 · 400 correo inválido · 401 sin sesión · 500 falló el envío |

## Pruebas

Desde `backend/`, con el entorno virtual activo:

```bash
python -m pip install -r requirements-dev.txt   # agrega pytest
python -m pytest                                # tiene que decir "37 passed"
```

`tests/conftest.py` fija una clave de prueba, apaga el envío de correo y usa una base SQLite temporal, así que las pruebas no tocan el `.env` real ni mandan correos.

| Archivo | Qué cubre |
|---|---|
| `test_auth.py` | CU0006 (registro, correo duplicado aun con mayúsculas, clave corta, clave guardada con hash, registro simultáneo con el mismo correo) y CU0001 (login correcto, clave incorrecta, mismo mensaje para correo inexistente, campos vacíos) |
| `test_invite.py` | CU0010: envío correcto, enlace de registro en el correo, invitación guardada como enviada o fallida, sin sesión, correo inválido o de más de 254 caracteres, falla del servidor de correo sin filtrar detalles, token vencido, inválido o de un usuario inexistente, conexión SMTP con timeout y servidor de correo que no responde |
| `test_seguridad.py` | Que un token firmado con la clave vieja `super-secret` no sirva, que la app no arranque sin una clave segura, que `MAIL_USE_TLS=true` active TLS, que `run.py` no exponga el depurador y que `NotificationService` sea Singleton |

El frontend no tiene pruebas automáticas.

## Estructura

```
backend/
├── run.py                    punto de entrada (127.0.0.1:5000)
├── requirements.txt          dependencias
├── requirements-dev.txt      dependencias + pytest
├── .env.example              modelo del archivo de configuración
├── app/
│   ├── __init__.py             create_app(): arma la aplicación y valida la clave JWT
│   ├── config.py               única fuente de configuración (lee .env)
│   ├── controllers/            endpoints: auth_controller (registro y login), invite_controller
│   ├── services/               auth_service (registro y autenticación), invitation_service (guarda la invitación y su estado),
│   │                           notification_service (Singleton, envía el correo)
│   ├── persistence/            models.py (User, Invitation) y daos/ (user_dao.py, invitation_dao.py)
│   └── utils/decorators.py     @token_required
│       utils/mail.py           Flask-Mail con timeout SMTP
└── tests/                    pruebas automáticas (pytest)

frontend/src/
├── styles.css                tema "Índigo" (todos los estilos)
└── app/
    ├── app.module.ts           rutas; /welcome e /invite protegidas con AuthGuard
    ├── app.component.*         barra superior (solo con sesión)
    ├── core/                   auth.service, notification.service, auth.guard, token.interceptor
    └── features/               login, register, welcome, invite
```

## Arquitectura

En capas: controller → service → DAO → base de datos (SQLite).

- Los **controllers** validan el pedido con marshmallow, llaman al servicio y arman la respuesta.
- Los **services** tienen la lógica: `AuthService` registra y autentica; `InvitationService` guarda la invitación, pide el envío y registra el resultado; `NotificationService` arma y envía el correo.
- Los **DAO** (`UserDAO`, `InvitationDAO`) hacen las consultas con SQLAlchemy.
- **Estados de la invitación:** se guarda como `pendiente` y pasa a `enviada` o a `fallida` según el resultado del envío.
- **Patrón Singleton:** `NotificationService` tiene una sola instancia, creada con doble verificación y candado.

## Seguridad

- Las contraseñas se guardan con hash (Werkzeug) y se verifican antes de decidir si el acceso es válido.
- Mismo mensaje para correo inexistente y clave incorrecta: no se revela qué correos existen.
- La clave JWT y las credenciales de correo viven en `.env`, nunca en el código.
- Las rutas privadas del frontend usan `AuthGuard`; un 401 con token cierra la sesión.
- Los errores al cliente son genéricos; el detalle queda en el log del servidor.

## Límites conocidos

- **Invitaciones sin límite:** un usuario con sesión puede mandar todas las invitaciones que quiera. Para producción haría falta un límite por usuario.
- **Contenido del correo:** el correo de invitación incluye el nombre que eligió quien invita, sin revisar.
- **Servidor de desarrollo:** corre sobre el servidor de desarrollo de Flask y de Angular, en local, para la demostración.
- **Sin HTTPS:** las credenciales viajan por HTTP local (RNF-10, "No cumplido"). Para producción hace falta un servidor con TLS delante.
- **Frontend sin pruebas automáticas:** las pantallas se prueban a mano (procedimientos de `5. Pruebas/`).
- **Hallazgos de diseño** (`docs/DISEÑO_UMBook.md` §9): el guard no detecta el token vencido (H6), la dirección del backend está fija en el frontend (H10) y no hay migraciones (H11). El envío SMTP sin timeout (H7) y el registro simultáneo con el mismo correo (H8) están resueltos.
