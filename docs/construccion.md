# Construcción de UMBook — paso a paso

Este documento explica cómo se construyó el proyecto y por qué, organizado en las
3 implementaciones definidas en `prompt-construccion.md`. No es un tutorial genérico
de Flask/Angular: son las decisiones concretas que se tomaron en este repo.

> Punto de partida real: al empezar, el repo solo tenía `Readme.md` — el código de
> backend/frontend que describían `imple.md`/`tareas.md` (implementado supuestamente
> por una compañera) no estaba en este repositorio ni en el remoto de GitHub. Todo lo
> que sigue se construyó desde cero, usando `imple.md` y `prompt-construccion.md` como
> especificación de arquitectura y diseño. `imple.md` ya no existe como archivo: su
> contenido quedó repartido entre [`backend.md`](./backend.md), [`frontend.md`](./frontend.md)
> y [`proyecto.md`](./proyecto.md) al reorganizar el repo en `docs/`.

## 0. Desviaciones respecto a la especificación original

- **Python**: la spec pedía fijar 3.11/3.12 porque Flask 2.3.2/Werkzeug 2.3.6 no
  corren en 3.13+. El entorno disponible tiene Python 3.14. En vez de instalar una
  versión vieja de Python, se subieron las versiones de Flask/Werkzeug/extensiones a
  las últimas compatibles con 3.14 (`backend/requirements.txt`). No cambia ninguna
  decisión de diseño, solo evita pelear con un intérprete viejo.
- **Angular**: `imple.md` documentaba Angular 15. El Angular CLI 15 no soporta
  Node 24 (el disponible acá). Se generó el proyecto con Angular CLI 22
  (`npx @angular/cli@22 new frontend --standalone=false --routing=false`), pidiendo
  explícitamente módulos NgModule (no standalone) para mantener la convención que
  describe `imple.md` ("Sin lazy loading, todo declarado en `app.module.ts`. No usa
  componentes standalone").
- **CU0010 (Invitación a la aplicación)**: no se implementó. `prompt-construccion.md`
  sección 5 es explícito: su legitimidad está en discusión y no hay que usar su
  infraestructura como base para nada nuevo. Como no había código previo que
  "mantener", directamente se excluyó del alcance en vez de construirlo para
  después dejarlo en duda.

## 1. Login — corrección de un bypass de autenticación

La spec original describía un bug conocido (aunque acá no había código legado con
ese bug: se construyó el login ya corregido, documentando el bug que se **evitó**
para que quede registro de por qué el orden de las validaciones importa).

**El riesgo**: si `check_password_hash` se llama *después* de haber decidido que las
credenciales son válidas (por ejemplo, dentro de la rama "éxito" de un `if usuario
existe`), cualquier contraseña entra mientras el email exista — la verificación deja
de verificar nada.

**Cómo se evitó** (`backend/app/services/auth_service.py`, `AuthService.autenticar`):

```python
usuario = UserDao.get_by_email(email)
if usuario is None or not check_password_hash(usuario.password_hash, password):
    raise CredencialesInvalidasError("Credenciales incorrectas.")
return usuario
```

La condición de error cubre **ambos** casos (usuario inexistente y contraseña
incorrecta) en la misma rama, con el mismo mensaje genérico — no se distingue cuál
de los dos falló, para no filtrar si un email está registrado.

Otras correcciones de la spec, ya aplicadas desde el primer commit del código (no
hubo que "corregirlas" porque no existía la versión con el bug):

- **Redirect post-login a `/welcome`**, no a `/invite`
  (`frontend/src/app/features/login.component.ts`).
- **`AuthGuard` aplicado** a la ruta `/welcome`
  (`frontend/src/app/app.module.ts`, `canActivate: [AuthGuard]`). Como no se
  implementó CU0010, no hay ruta `/invite` que proteger.
- **`app/config.py` como única fuente de configuración**: `create_app()`
  (`backend/app/__init__.py`) llama a `app.config.from_object(Config)` y `Config`
  lee todo de variables de entorno (`backend/.env`, nunca commiteado — ver
  `backend/.env.example`). No hay secretos hardcodeados en el código.

**Cómo probarlo** (equivalente a CP 3.1 — confirma que no hay bypass):

```bash
cd backend && source venv/bin/activate && python run.py   # :5000
# en otra terminal
curl -X POST localhost:5000/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"Ana","email":"ana@test.com","password":"password123"}'
curl -X POST localhost:5000/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"ana@test.com","password":"incorrecta"}'   # debe dar 401
curl -X POST localhost:5000/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"ana@test.com","password":"password123"}'  # debe dar 200 + token
```

## 2. Solicitar Amistad / Aceptar-Rechazar Solicitud — patrón State

**Por qué State**: una `SolicitudAmistad` tiene tres estados (pendiente, aceptada,
rechazada) y las transiciones válidas dependen exclusivamente del estado actual
(pendiente → aceptada/rechazada; aceptada/rechazada → nada). Modelar esto con
`if estado == "pendiente": ...` en el service es exactamente el código que el
patrón State existe para evitar: cada estado nuevo obligaría a tocar todos esos
`if`. En cambio, cada estado es una clase que sabe qué hacer con `aceptar()` /
`rechazar()`, incluido "rechazar con un error" cuando la transición no es válida.

**Estructura** (`backend/app/services/estados/estado_solicitud.py`):

```
EstadoSolicitud (ABC)
  + aceptar(solicitud)
  + rechazar(solicitud)

Pendiente   → aceptar(): crea el vínculo y pasa a Aceptada
              rechazar(): pasa a Rechazada
Aceptada    → aceptar()/rechazar(): EstadoInvalidoError (transición terminal)
Rechazada   → aceptar()/rechazar(): EstadoInvalidoError (transición terminal)
```

`SolicitudAmistad` (`backend/app/persistence/models.py`) es el **contexto** del
patrón: guarda `estado` (string, persistido) y `_estado_obj` (el objeto State, no
persistido — se reconstruye con `@reconstructor` cada vez que SQLAlchemy carga la
fila). `aceptar()`/`rechazar()` en el modelo son una sola línea cada una: delegan en
`_estado_obj`. El modelo nunca decide si la transición es válida.

**Transacción única (requisito explícito de la spec)**: `Pendiente.aceptar()` llama
a `solicitud.crear_vinculo_amistad()` (agrega un `Amistad` a la sesión) y recién
después a `solicitud.set_estado(Aceptada())`. Ninguna de las dos líneas hace
`commit()` — el `commit()` único vive en
`AmistadService.responder_solicitud` (`backend/app/services/amistad_service.py`):
si `crear_vinculo_amistad` fallara, no hay commit y el estado tampoco queda en
"aceptada" en memoria (rollback explícito en el `except`).

**Autorización**: `responder_solicitud` valida que quien responde sea el
`receptor_id` de la solicitud antes de tocar el estado (`NoAutorizadoError`, 403) —
mismo principio que el fix de `AuthGuard` en el frontend: toda acción nueva se valida
contra quién la pide, no contra qué dice el payload.

**Endpoints** (`backend/app/controllers/amistad_controller.py`, todos con
`@token_required`):

| Método | Ruta | Acción |
|---|---|---|
| POST | `/amistad/solicitudes` | Solicitar amistad (`email_receptor` en el body) |
| GET | `/amistad/solicitudes/pendientes` | Solicitudes recibidas pendientes |
| POST | `/amistad/solicitudes/<id>/aceptar` | Aceptar |
| POST | `/amistad/solicitudes/<id>/rechazar` | Rechazar |

**Frontend**: todo vive en `welcome.component.ts/html` — un formulario para enviar
solicitud y una lista de pendientes con botones Aceptar/Rechazar
(`frontend/src/app/core/amistad.service.ts` hace las llamadas HTTP).

**Cómo probarlo** (CP SA.1–SA.3, CP AR.1–AR.3): ver la secuencia completa de curl en
la sección de testing más abajo.

## 3. Notificar Solicitud de Amistad Recibida — Observer sobre el Singleton existente

**Por qué Observer**: el requisito explícito de la spec es que
`AmistadService.solicitar_amistad()` **no llame al Notificador directamente**. Si lo
hiciera, sería una llamada de servicio común disfrazada de patrón. El punto del
Observer acá es que `Usuario` (el que recibe la solicitud) no sabe ni le importa
quién está escuchando sus eventos — hoy es el `Notificador`, mañana podría sumarse
un logger o un servicio de push sin tocar `AmistadService`.

**Usuario como Observable** (`backend/app/persistence/models.py`): mantiene una
lista de observadores **en memoria** (no persistida — no hace falta guardarla, se
reconstruye igual con `@reconstructor` cada vez que SQLAlchemy carga el objeto).
`NotificationService.get_instance()` se registra ahí por defecto: es la única
implementación de `Observador` que existe hoy en el sistema.

```python
def agregar_observador(self, observador): ...
def eliminar_observador(self, observador): ...
def notificar_observadores(self, evento): 
    for observador in self._observadores:
        observador.actualizar(evento)
```

**`NotificationService` (Singleton + Observador)**
(`backend/app/services/notification_service.py`): ya existía conceptualmente como
Singleton puro (double-checked locking) para CU0010; acá se le agregó la interfaz
`Observador` (`backend/app/services/observer.py`) sin tocar la firma de los métodos
que ya tenía (`enviar_email`, `notificar`). El método nuevo es `actualizar(evento)`,
que es por donde entra cualquier evento Observer — hoy solo reacciona a
`"solicitud_recibida"` mandando un email.

`Observador` vive en un módulo propio (`services/observer.py`) separado de
`notification_service.py` a propósito: si `Usuario` (en `persistence/models.py`)
importara directamente la clase concreta `NotificationService`, se generaría un
import circular (`models → services → models`, porque `NotificationService` no
necesita nada de `models`, pero si se lo hiciera depender de la interfaz en vez de
la clase concreta, se evita el problema estructuralmente).

**El flujo real** (`backend/app/services/amistad_service.py`,
`AmistadService.solicitar_amistad`):

```python
solicitud = SolicitudDao.create(...)
receptor.notificar_observadores({
    "tipo": "solicitud_recibida",
    "receptor_email": receptor.email,
    "emisor_nombre": emisor.name,
})
```

El service publica el evento en el `Usuario` (Observable). `Usuario` lo reparte a
sus observadores. `NotificationService.actualizar()` decide qué hacer con ese
evento puntual. El service que originó la solicitud no conoce al `Notificador`.

**"¿Notificación como entidad propia o consulta derivada?"** — la spec deja esto
abierto y pide la opción más simple salvo indicación contraria. Se implementó como
**consulta derivada**: no hay tabla `Notificacion`. `GET
/amistad/solicitudes/pendientes` (la misma que usa el CU de Solicitar Amistad) ES la
notificación que ve la home — el email disparado por el Observer es el canal de
notificación "push", la lista de pendientes es el canal "pull". No hacía falta
duplicar el dato en dos tablas.

**Cómo probarlo** (CP NT.1–NT.3): con `MAIL_SUPPRESS_SEND=true` en `.env` (ver
`backend/.env.example`) el email no sale de verdad pero pasa por
`NotificationService.enviar_email()` igual — sirve para probar el flujo sin
depender de credenciales SMTP reales. Con credenciales reales, revisar la casilla
del receptor.

## 4. Cómo correr todo

```bash
# Backend
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # completar JWT_SECRET_KEY y credenciales de mail
python run.py                # :5000, crea instance/umbook.db si no existe

# Frontend (otra terminal)
cd frontend
npm install
npx ng serve                 # :4200
```

## 5. Prueba end-to-end completa (backend)

Secuencia real que se corrió para validar los 3 CU juntos (dos usuarios, Ana y
Beto):

```bash
B=http://127.0.0.1:5000

curl -X POST $B/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"Ana","email":"ana@test.com","password":"password123"}'
curl -X POST $B/auth/register -H 'Content-Type: application/json' \
  -d '{"name":"Beto","email":"beto@test.com","password":"password123"}'

TOKEN_ANA=$(curl -s -X POST $B/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"ana@test.com","password":"password123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")
TOKEN_BETO=$(curl -s -X POST $B/auth/login -H 'Content-Type: application/json' \
  -d '{"email":"beto@test.com","password":"password123"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['token'])")

# Ana solicita amistad a Beto -> dispara el Observer (email a Beto)
curl -X POST $B/amistad/solicitudes -H "Authorization: Bearer $TOKEN_ANA" \
  -H 'Content-Type: application/json' -d '{"email_receptor":"beto@test.com"}'

# Beto ve la solicitud pendiente (la "notificación")
curl $B/amistad/solicitudes/pendientes -H "Authorization: Bearer $TOKEN_BETO"

# Ana NO puede responder la solicitud de Beto (403 — no es el receptor)
curl -o /dev/null -w "%{http_code}\n" -X POST \
  $B/amistad/solicitudes/1/aceptar -H "Authorization: Bearer $TOKEN_ANA"

# Beto acepta -> estado pasa a "aceptada" y se crea el vínculo Amistad
curl -X POST $B/amistad/solicitudes/1/aceptar -H "Authorization: Bearer $TOKEN_BETO"

# Aceptar de nuevo la misma solicitud -> 409 (Aceptada.aceptar() es transición inválida)
curl -o /dev/null -w "%{http_code}\n" -X POST \
  $B/amistad/solicitudes/1/aceptar -H "Authorization: Bearer $TOKEN_BETO"
```

Resultado obtenido (documentado acá porque es la evidencia de que el diseño
funciona, no solo compila): registro y login OK, contraseña incorrecta rechazada
con 401, solicitud creada en estado `pendiente`, listada en `pendientes`, respuesta
no autorizada rechazada con 403, aceptación exitosa con 200 y estado `aceptada`,
segunda aceptación rechazada con 409. La tabla `amistades` quedó con el vínculo
Ana–Beto.

El frontend (`ng build`) compila sin errores sobre esta misma API; no se pudo hacer
una verificación visual en navegador real en este entorno (sin herramienta de
browser conectada) — recomendado hacer un `ng serve` + click-through manual de
login → welcome → solicitar/aceptar antes de la defensa.

## 6. Puesta en marcha real y ajustes post-construcción

Una vez cargadas las credenciales reales (Gmail app password) y probado en un
navegador de verdad, salieron tres cosas más:

**El mail de notificación funcionaba, pero era texto plano.** Se armaron
plantillas de verdad en `backend/app/templates/emails/` (`_base.html` +
`solicitud_recibida.html`/`.txt`, Jinja) y `NotificationService._enviar_email_plantilla()`
las renderiza y arma el `Message` con `body` (texto) y `html` juntos. `enviar_email()`
genérico se mantuvo sin tocar su firma, por si en algún momento se retoma CU0010.

**Faltaba ver la amistad confirmada.** Se agregó `GET /amistad/amigos`
(`AmistadDao.listar_amigos`, une la tabla `amistades` con `usuarios` para
devolver "el otro" de cada vínculo) y una card "Tus amigos" en Welcome,
arriba de todo — así se puede confirmar a simple vista que aceptar una
solicitud realmente crea el vínculo.

**Bug real de Angular 22: los datos no aparecían hasta interactuar con la
página.** Al entrar a `/welcome`, "Tus amigos" y "Solicitudes recibidas"
quedaban vacíos aunque el backend ya tenía los datos — recién se veían
después de tocar cualquier botón (por ejemplo, el de enviar solicitud).
Causa: el scaffold de Angular CLI 22 no incluye `zone.js` por default (quedó
en modo *zoneless* sin pedirlo), y el código de este proyecto usa el patrón
clásico (`.subscribe()` mutando propiedades del componente) en vez de
signals — sin Zone parcheando las APIs async, Angular no se entera de que
llegó la respuesta HTTP y no dispara un ciclo de detección de cambios por su
cuenta; recién lo hace cuando otro evento (un click) lo fuerza indirectamente.
Arreglo en dos partes:

1. `zone.js` agregado como dependencia y declarado en
   `frontend/angular.json` → `build.options.polyfills: ["zone.js"]` (el
   mecanismo oficial del builder — un `import 'zone.js'` suelto en
   `main.ts` no alcanzó, el orden de carga con Vite no quedaba garantizado).
2. Como refuerzo — para no depender de que Zone y el dev-server de Vite
   terminen de llevarse bien —, `WelcomeComponent`, `LoginComponent` y
   `RegisterComponent` ahora inyectan `ChangeDetectorRef` y llaman
   `detectChanges()` explícitamente apenas llega la respuesta de cada
   llamada HTTP, en vez de confiar en que el framework lo dispare solo.

**Nota para la defensa**: si preguntan por qué hay `detectChanges()` manual
en componentes que "deberían" actualizarse solos, esta es la explicación —
vale la pena poder contarla, muestra manejo real de un problema no trivial
de Angular moderno.

## 7. Tests automáticos

`backend/tests/` (pytest, 30 tests, correr con `pip install -r
requirements-dev.txt && pytest` desde `backend/`) — detalle completo en
[`backend.md`](./backend.md#tests). En resumen, separados por lo que cada uno
prueba:

- **State en aislamiento** (`test_estado_solicitud.py`): nada de Flask ni DB,
  un doble de prueba hace de contexto. Cubre las 4 transiciones válidas y que
  los estados terminales (`Aceptada`, `Rechazada`) rechacen cualquier
  transición nueva con `EstadoInvalidoError`.
- **Observer + Singleton** (`test_observer.py`): que
  `Usuario.notificar_observadores()` le llegue a todos los observadores
  registrados (y deje de llegarle a uno que se sacó), que
  `NotificationService.get_instance()` esté registrado por defecto en todo
  `Usuario` nuevo, que sea Singleton de verdad (dos `get_instance()` dan el
  mismo objeto), y que `actualizar()` solo dispare el mail para el evento
  `solicitud_recibida` (otros eventos no hacen nada).
- **Regresión del bug de login** (`test_auth_service.py`): contraseña
  correcta autentica, contraseña incorrecta y email inexistente dan el mismo
  error genérico — la prueba concreta de que el bug documentado en la
  sección 1 no está.
- **Integración del service de amistad** (`test_amistad_service.py`, con DB
  real de archivo temporal): que `solicitar_amistad` dispare el Observer sin
  llamar al Notificador directo (se verifica interceptando
  `NotificationService.actualizar` y comparando el evento recibido), las
  validaciones (auto-solicitud, duplicada, ya son amigos, receptor
  inexistente), que `aceptar` cree el vínculo `Amistad` en la misma
  transacción que el cambio de estado, y que una segunda aceptación falle
  sin corromper el estado ya persistido.
- **End-to-end por HTTP** (`test_api.py`): el mismo flujo que se probó a mano
  con curl (sección 5), pero como test automático con el cliente de Flask —
  códigos de estado incluidos (401/403/404/409).

## 8. Qué falta para la defensa (no bloquea lo ya construido)

- Generar la primera migración real con Flask-Migrate (hoy el esquema sale de
  `db.create_all()` en `run.py`, sin carpeta `migrations/`) — ver `tareas.md`.
- El token de confirmación/rechazo "no adivinable, con expiración" que menciona
  `prompt-construccion.md` sección 4 aplica al flujo por **email** (link que el
  receptor clickea desde su casilla sin loguearse). Lo que se construyó acá es el
  flujo autenticado (aceptar/rechazar logueado en la app, con el JWT de sesión) —
  si el CU exige también el flujo por link de email, es una implementación
  adicional (token propio, de un solo uso) que no estaba en el alcance de "las 3
  implementaciones" tal como las define la sección 1 de `prompt-construccion.md`.
- Manejo de sesión expirada en el front (JWT vencido → redirect automático a
  `/login`, hoy solo se ve un mensaje de error genérico).
