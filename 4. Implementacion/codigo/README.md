# UMBook

Aplicación de gestión de usuarios con amistades y notificaciones por correo. Trabajo de Ingeniería de Software. Backend Flask (API REST) y frontend Angular.

## Qué se puede hacer

| Función | Estado |
|---|---|
| Registrarse con nombre, correo y clave (al menos 8 caracteres) | Disponible |
| Iniciar sesión: la clave se valida con hash antes de decidir si el acceso es válido | Disponible |
| Cerrar sesión automáticamente y volver al login cuando la sesión vence o el token es inválido | Disponible |
| Solicitar amistad a otro usuario por su correo | Disponible |
| Aceptar o rechazar una solicitud recibida | Disponible |
| Ver las solicitudes pendientes y la lista de amigos | Disponible |
| Recibir un correo cuando llega una solicitud de amistad | Disponible |
| Invitación a la aplicación | Fuera de alcance |

## Cómo funciona una solicitud de amistad

- **Estados.** Una solicitud está `pendiente`, `aceptada` o `rechazada`. Solo desde `pendiente` se puede pasar a los otros dos; `aceptada` y `rechazada` son terminales y cualquier transición nueva se rechaza (409).
- **Validaciones al solicitar.** No se puede enviar una solicitud a uno mismo, ni duplicar una pendiente para el mismo par de usuarios, ni solicitar a quien ya es amigo. Si el receptor no existe, se avisa.
- **Autorización.** Solo el receptor puede aceptar o rechazar. Cualquier otro usuario recibe 403, aunque conozca el identificador de la solicitud.
- **Aceptar.** Cambiar el estado a `aceptada` y crear el vínculo de amistad ocurren en una sola transacción: si una de las dos falla, no queda nada guardado.
- **Notificación.** Al crearse la solicitud se publica un evento; el `NotificationService` lo recibe como observador y manda el correo al receptor. `AmistadService` nunca llama al notificador directamente. Además, las solicitudes pendientes que ve el receptor en su pantalla de inicio son la notificación visible en la aplicación.

## Requisitos

- Python 3.10 o más nuevo (probado con 3.14).
- Node.js y npm, para el frontend (Angular 22).
- Las dependencias del backend están en `backend/requirements.txt`: Flask, Flask-SQLAlchemy, Flask-Migrate, Flask-JWT-Extended, Flask-Mail, Flask-Cors, marshmallow y python-dotenv.
- No hace falta instalar ninguna base de datos: SQLite viene con Python.

## Cómo arrancarlo

### Backend (puerto 5000)

Los comandos se corren desde la carpeta `backend/`.

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt

cp .env.example .env          # y completar JWT_SECRET_KEY y los datos de correo
python run.py                 # crea instance/umbook.db si no existe
```

> **Nota:** la ruta de esta carpeta tiene espacios (`4. Implementacion`), y los programas sueltos del entorno virtual (`pip`, `pytest`) no funcionan en rutas con espacios. Por eso los comandos usan `python -m pip` y `python -m pytest`, que sí funcionan.

### Frontend (puerto 4200)

En otra terminal, desde la carpeta `frontend/`:

```bash
npm install
npx ng serve                  # abre http://localhost:4200
```

## Configuración

Se hace con un archivo `backend/.env` (se crea copiando `backend/.env.example`). El `.env` no se sube al repositorio.

| Variable | Obligatoria | Para qué sirve |
|---|---|---|
| `JWT_SECRET_KEY` | Sí | Clave con la que se firman los tokens de sesión. Usar un valor largo y al azar. |
| `SQLALCHEMY_DATABASE_URI` | No | Base de datos. Por defecto `sqlite:///umbook.db`, dentro de `instance/`. |
| `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS` | Para enviar correo | Servidor SMTP (por defecto Gmail: `smtp.gmail.com`, 587, TLS). |
| `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER` | Para enviar correo | Cuenta que envía. `MAIL_PASSWORD` es una *app password* de Gmail, no la clave de la cuenta (se genera en https://myaccount.google.com/apppasswords). |
| `MAIL_SUPPRESS_SEND` | No | Con `true`, el envío de correo se simula. Sirve para probar sin credenciales reales. |
| `CORS_ORIGIN` | No | Origen del frontend que la API acepta. Por defecto `http://localhost:4200`. |

## API

| Método y ruta | Qué hace |
|---|---|
| `POST /auth/register` | Registra un usuario |
| `POST /auth/login` | Inicia sesión y devuelve el token |
| `GET /auth/me` | Datos del usuario con sesión abierta |
| `POST /amistad/solicitudes` | Solicita amistad a otro usuario |
| `GET /amistad/solicitudes/pendientes` | Solicitudes pendientes recibidas |
| `GET /amistad/amigos` | Amigos confirmados |
| `POST /amistad/solicitudes/<id>/aceptar` | Acepta una solicitud (solo el receptor) |
| `POST /amistad/solicitudes/<id>/rechazar` | Rechaza una solicitud (solo el receptor) |

## Datos de demostración

Para probar el flujo de amistad sin cargar todo a mano, hay un script que llena la base con usuarios, solicitudes pendientes, una rechazada y amistades confirmadas. Se corre desde `backend/`:

```bash
python seed.py            # agrega los datos (falla si el correo ya existe)
python seed.py --reset    # borra usuarios, solicitudes y amistades antes de sembrar
```

- Inserta directamente contra los modelos, sin pasar por `AmistadService`: no dispara el Observer, así que **no se manda ningún correo real** aunque el `.env` tenga credenciales configuradas.
- Es una herramienta de apoyo, no forma parte de la aplicación. No usarla sobre una base con datos reales.

## Pruebas

Desde `backend/`, con el entorno virtual activo:

```bash
python -m pip install -r requirements-dev.txt   # agrega pytest
python -m pytest                                # o: python -m pytest -v
```

Son 32 pruebas; la última línea de la salida tiene que decir `32 passed`. `tests/conftest.py` fuerza la configuración de prueba antes de importar la aplicación (clave de prueba, envío de correo apagado y una base SQLite temporal por prueba), así que nunca tocan el `.env` real ni mandan correo. Cubren:

- el patrón State en aislamiento, sin Flask ni base de datos: las transiciones válidas y que los estados terminales rechacen cualquier transición;
- el Observer y el Singleton: que el evento llegue a todos los observadores y que `NotificationService` siempre sea la misma instancia;
- la regresión del bug de login: contraseña incorrecta, correo inexistente y contraseña correcta;
- el servicio de amistad contra una base real: que solicitar dispare el Observer sin llamar al notificador directo, cada validación, la transacción de aceptar y la autorización del receptor;
- el flujo completo a través de HTTP, con el cliente de pruebas de Flask, incluidos los códigos de estado (también el 401 por token vencido y el 422 por token corrupto).

## Estructura del proyecto

```
backend/
├── run.py                   punto de entrada: arranca el servidor en :5000
├── seed.py                  llena la base con datos de demostración
├── requirements.txt         dependencias
├── requirements-dev.txt     dependencias + pytest
├── pytest.ini               configuración de pytest
├── .env.example             modelo del archivo de configuración
├── app/
│   ├── __init__.py            create_app(): arma la aplicación y conecta las capas
│   ├── config.py              única fuente de configuración (lee el .env)
│   ├── extensions.py          instancias de db, JWT, mail y CORS
│   ├── controllers/           capa de presentación: endpoints HTTP (auth y amistad)
│   ├── services/              capa de lógica: las reglas del sistema
│   │   ├── auth_service.py      registro e inicio de sesión
│   │   ├── amistad_service.py   solicitar, aceptar y rechazar
│   │   ├── estados/             patrón State de la solicitud
│   │   ├── observer.py          interfaces de Observable y Observador
│   │   └── notification_service.py  Singleton que envía el correo
│   ├── persistence/           capa de acceso a datos
│   │   ├── models.py            Usuario, SolicitudAmistad y Amistad
│   │   └── daos/                un DAO por entidad
│   ├── templates/emails/      plantillas del correo (HTML y texto plano)
│   └── utils/                 decoradores comunes
├── tests/                   pruebas automáticas (pytest)
└── instance/                se crea al correr: acá queda la base de datos (umbook.db)

frontend/
└── src/app/
    ├── core/                  servicios de autenticación y amistad, guard e interceptor del token
    ├── features/              pantallas: login, registro y welcome
    └── app.module.ts          módulo raíz y rutas
```

## Arquitectura

El backend tiene tres capas, y cada una solo le habla a la siguiente: controller → service → DAO → base de datos (SQLite).

- Los controllers solo traducen HTTP: validan el pedido, llaman a un service y devuelven la respuesta con su código de estado.
- Los services concentran las reglas del sistema y abren y cierran las transacciones (`commit` / `rollback`).
- Los DAO son quienes hacen las consultas a la base con SQLAlchemy; controllers y services no arman consultas.
- `create_app()` es el único lugar que arma las piezas y las conecta entre sí.

Patrones de diseño que se usan:

- **State:** `SolicitudAmistad` delega su comportamiento en un objeto de estado (`Pendiente`, `Aceptada`, `Rechazada`). Cada estado sabe a cuáles puede pasar; los terminales rechazan cualquier transición. Sumar un estado nuevo no obliga a tocar el servicio.
- **Observer:** `Usuario` es el observable y publica el evento de solicitud recibida. Quien quiera reaccionar se registra como observador, sin que el servicio de amistad lo conozca.
- **Singleton:** `NotificationService` es el observador que envía el correo y existe una sola instancia (`get_instance()`).

## Seguridad

- Las claves se guardan con hash (Werkzeug), nunca en claro.
- La sesión es un JWT. En el login, la contraseña se valida con `check_password_hash` **antes** de decidir la rama de éxito o error: no hay forma de entrar sin la clave correcta.
- Los errores de inicio de sesión son siempre el mismo mensaje ("Credenciales incorrectas"), para no revelar qué correos existen.
- Las rutas privadas del frontend están protegidas con un `AuthGuard`, y un interceptor cierra la sesión y redirige a `/login` ante un 401 o un 422.
- Aceptar y rechazar solo lo puede hacer el receptor, y eso se verifica en el servidor.
- La clave de firma y las credenciales de correo viven en `.env`, nunca en el código.

## Límites conocidos

- **Invitación a la aplicación:** no se implementó. Se decidió no construir algo cuya validez como caso de uso está en duda.
- **Aceptar o rechazar desde el correo sin iniciar sesión:** no existe. Si se agregara, el enlace necesitaría un token propio, de un solo uso y con vencimiento, nunca el JWT de sesión.
- **Servidor de desarrollo:** el sistema corre sobre el servidor de desarrollo de Flask y de Angular, en un ambiente local, para la demostración.
