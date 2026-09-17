# Backend — UMBook

Flask + SQLAlchemy + SQLite. Patrón en capas: **controller → service → DAO →
model**. El detalle de por qué está armado así (patrones State/Observer/Singleton,
el fix del bug de login, la transacción de aceptar solicitud) está en
[`construccion.md`](./construccion.md); esto es la referencia de arquitectura y
convenciones para seguir tocando el código.

## Cómo correrlo

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # completar JWT_SECRET_KEY y credenciales de mail reales
python run.py           # sirve en :5000, crea instance/umbook.db si no existe
```

Variables de entorno (`backend/.env`, nunca se commitea — ver `.env.example`):
`JWT_SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, `MAIL_SERVER`/`MAIL_PORT`/
`MAIL_USE_TLS`/`MAIL_USERNAME`/`MAIL_PASSWORD`/`MAIL_DEFAULT_SENDER`, `CORS_ORIGIN`.
`MAIL_PASSWORD` es una **app password** de Gmail (no la contraseña de la cuenta),
se genera en https://myaccount.google.com/apppasswords. Con
`MAIL_SUPPRESS_SEND=true` el envío de mail se simula (útil para probar sin
credenciales reales).

## Tests

```bash
cd backend
source venv/bin/activate
pip install -r requirements-dev.txt   # agrega pytest sobre requirements.txt
pytest                                  # o: pytest -v
```

`tests/conftest.py` fuerza las variables de entorno necesarias (JWT secret de
test, `MAIL_SUPPRESS_SEND=true`, una sqlite de archivo temporal que se crea y
destruye por test) **antes** de importar `app`, así los tests no dependen del
`.env` real ni mandan mail de verdad. Cobertura actual:

- `test_estado_solicitud.py` — el patrón State en aislamiento total (sin
  Flask/DB): las 4 transiciones válidas y que los estados terminales
  rechacen cualquier transición nueva.
- `test_observer.py` — que `Usuario.notificar_observadores()` llegue a todos
  sus observadores, que `NotificationService` esté registrado por defecto, y
  que sea Singleton (`get_instance()` siempre devuelve la misma instancia).
- `test_auth_service.py` — regresión del bug de bypass de login (contraseña
  incorrecta / email inexistente / contraseña correcta).
- `test_amistad_service.py` — integración con DB real: que
  `solicitar_amistad` dispare el Observer (y no llame al Notificador
  directo), las validaciones (auto-solicitud, duplicada, ya amigos,
  receptor inexistente), la transacción de `aceptar` (estado + vínculo
  juntos) y la autorización (`responder_solicitud` solo por el receptor).
- `test_api.py` — el mismo flujo pero a través del cliente de test de Flask
  (HTTP real, códigos de estado incluidos), replicando la prueba manual con
  curl que se corrió al construir el proyecto.

## Estructura

```
backend/
  requirements.txt
  requirements-dev.txt      # requirements.txt + pytest
  pytest.ini
  run.py                   # entrypoint: create_app(), db.create_all(), app.run()
  .env.example
  tests/                    # ver sección Tests arriba
  app/
    __init__.py             # create_app(): config, extensiones, blueprints
    config.py                # Config: única fuente de configuración (lee de .env)
    extensions.py             # instancias de Flask-SQLAlchemy/Migrate/JWT/Mail/CORS
    controllers/               # Blueprints Flask. Validan con marshmallow, llaman
                                # al service, jsonify
      auth_controller.py        #   /auth/register, /auth/login, /auth/me
      amistad_controller.py     #   /amistad/solicitudes...
    services/
      auth_service.py            # registro, autenticación (orden correcto: hash
                                  # de password se valida ANTES de decidir éxito/error)
      amistad_service.py          # solicitar/responder solicitud de amistad,
                                   # orquesta el patrón State + dispara el Observer
      notification_service.py      # Singleton (double-checked locking) +
                                    # Observador — envío de email con plantillas
      observer.py                   # interfaz Observador (separada del singleton
                                     # concreto para evitar import circular con models)
      estados/
        estado_solicitud.py          # patrón State: Pendiente/Aceptada/Rechazada
    persistence/
      models.py                # Usuario (Observable), SolicitudAmistad (contexto
                                # del State), Amistad
      daos/
        user_dao.py              # get_by_email, get_by_id, create
        solicitud_dao.py          # SolicitudDao + AmistadDao (incluye listar_amigos)
    templates/
      emails/
        _base.html                 # layout común (header UMBook + footer)
        solicitud_recibida.html/.txt  # mail de "te enviaron una solicitud"
    utils/
      decorators.py              # @token_required: valida JWT, inyecta
                                  # g.current_user
```

## Modelos (`persistence/models.py`)

- **Usuario**: `id, name, email (unique), password_hash, created_at`. Implementa
  Observable (`agregar_observador`/`eliminar_observador`/`notificar_observadores`)
  con lista de observadores en memoria (no persistida), reconstruida vía
  `@reconstructor` en cada carga desde la DB. El `NotificationService` se registra
  como observador por defecto.
- **SolicitudAmistad**: `emisor_id, receptor_id, estado (string), fecha_creacion`.
  Contexto del patrón State: `aceptar()`/`rechazar()` delegan siempre en el objeto
  State actual (`_estado_obj`, no persistido, reconstruido igual que arriba).
- **Amistad**: `usuario1_id, usuario2_id (id menor primero), fecha_creacion`.
  Vínculo confirmado, creado por `SolicitudAmistad.crear_vinculo_amistad()` en la
  misma transacción que el pasaje a estado `aceptada`.

## Endpoints

| Método | Ruta | Auth | Descripción |
|---|---|---|---|
| POST | `/auth/register` | — | Registrar usuario |
| POST | `/auth/login` | — | Login, devuelve JWT |
| GET | `/auth/me` | JWT | Usuario autenticado actual |
| POST | `/amistad/solicitudes` | JWT | Solicitar amistad (`email_receptor`) |
| GET | `/amistad/solicitudes/pendientes` | JWT | Solicitudes recibidas pendientes |
| POST | `/amistad/solicitudes/<id>/aceptar` | JWT | Aceptar solicitud |
| POST | `/amistad/solicitudes/<id>/rechazar` | JWT | Rechazar solicitud |
| GET | `/amistad/amigos` | JWT | Amigos del usuario autenticado |

Todas las rutas con JWT usan `@token_required` y devuelven 401 sin token, 403 si el
usuario autenticado no es el dueño del recurso que intenta tocar (por ejemplo,
responder una solicitud que no le llegó a él).

## Plantillas de email (`app/templates/emails/`)

`NotificationService._enviar_email_plantilla()` arma el mail renderizando un
`.html` y un `.txt` con el mismo contexto (Jinja, vía `flask.render_template` —
Flask ya resuelve `app/templates/` como carpeta de templates por default) y lo
manda con `flask_mail.Message(body=..., html=...)`. Para agregar un mail nuevo:

1. Crear `templates/emails/<nombre>.html` (extendiendo `emails/_base.html`, bloque
   `contenido`) y `templates/emails/<nombre>.txt` como fallback de texto plano.
2. Llamar `self._enviar_email_plantilla(destinatario, asunto, "<nombre>", contexto)`
   desde donde corresponda (hoy solo desde `actualizar()`, al reaccionar al evento
   `solicitud_recibida`).

`enviar_email(destinatario, mensaje)` (sin plantilla) se mantiene aparte, sin
tocar su firma, como API genérica para el caso en que en algún momento se
retome CU0010.

## Convención para un endpoint nuevo

1. Si hace falta, agregar modelo en `persistence/models.py`.
2. Crear DAO en `persistence/daos/` (métodos estáticos, usa `db.session`).
3. Crear service en `services/` con la lógica de negocio (el service no conoce
   Flask/request; recibe y devuelve objetos de dominio, nunca `request`/`jsonify`).
4. Crear `Schema` de marshmallow + Blueprint en `controllers/`, usando
   `@token_required` si el CU requiere sesión.
5. Registrar el blueprint en `app/__init__.py`.
