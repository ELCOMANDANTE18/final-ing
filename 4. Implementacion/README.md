# 4. Implementación — UMBook

**Versión:** 2.4 · **Última modificación:** 26/11/2026 · **Etapa:** Implementación

La implementación toma como base el proyecto de una compañera del grupo ([MaguiMaluff/final-software](https://github.com/MaguiMaluff/final-software), commit `fe825751`), con su acuerdo. Se usa **el mismo código, con los errores de seguridad corregidos y un frontend con diseño nuevo**. Sus fichas de caso de uso y sus diagramas de secuencia están acá tal cual.

## Contenido

| Nº | Qué | Dónde | Origen |
|---|---|---|---|
| 1 | Fichas de los casos de uso implementados | `1_Casos de Uso/` | Repositorio de la compañera, sin cambios |
| 2 | Diagramas de secuencia | `2_Diagramas de Secuencia/` | Repositorio de la compañera, sin cambios |
| — | Código fuente (backend Flask y frontend Angular) | `codigo/` | Su código, con las correcciones de abajo. Cómo correrlo: `codigo/README.md` |

## Casos de uso implementados

| Código | Caso de uso | Ficha | Diagrama de secuencia |
|---|---|---|---|
| CU0001 | Iniciar Sesión | `CU001-login.docx.pdf` | `caso1-login.png` |
| CU0006 | Registrar Usuario | `CU0006-registro.docx.pdf` | `caso6-registro.png` |
| CU0010 | Invitación a la aplicación | `CU0010-invitar.docx.pdf` | `caso10-invitacion.png` |

## Qué se cambió respecto del código original

### Seguridad

| # | Problema en el original | Riesgo | Corrección |
|---|---|---|---|
| 1 | Clave de firma JWT fija en el código (`'super-secret'`) | Cualquiera que lea el repositorio puede fabricar un token válido y entrar como cualquier usuario | Se lee de `backend/.env`; la aplicación no arranca sin una clave o con una de ejemplo |
| 2 | `run.py` con `debug=True` en `host='0.0.0.0'` | El depurador de Werkzeug queda expuesto en la red y permite ejecutar código en la máquina | Escucha solo en `127.0.0.1`; el modo debug se activa a propósito con `FLASK_DEBUG=1` |
| 3 | `test_smtp.py` con usuario y contraseña de Gmail escritos en el código, y la base `umbook.db` dentro del repositorio | Credenciales y datos de usuarios públicos | No se copiaron. `.gitignore` excluye `.env`, `instance/` y `*.db` |
| 4 | `MAIL_USE_TLS` solo se activaba con `'True'` (con mayúscula) | Con `MAIL_USE_TLS=true` la contraseña de Gmail viajaba sin cifrar | Acepta `true`, `True`, `1` o `yes` |
| 5 | El botón "Logout" solo navegaba a `/login` | El token quedaba guardado: la sesión nunca se cerraba | Borra el token y el nombre guardados |
| 6 | `AuthGuard` existía pero ninguna ruta lo usaba | `/welcome` e `/invite` se abrían sin iniciar sesión | Aplicado a las dos rutas |
| 7 | Los errores devolvían `str(e)` al cliente | Se filtraban detalles del token y del servidor de correo | Mensaje genérico al cliente; el detalle queda en el log |
| 8 | El registro mostraba `JSON.stringify(err)` en un `alert` | Se mostraba la respuesta HTTP completa | Se muestra solo el mensaje del servidor |
| 9 | Werkzeug 2.3.6 y Flask 2.3.2 | Versiones con vulnerabilidades conocidas | Werkzeug 3.1.8 y Flask 3.0.3 |
| 10 | `ana@x.com` y `ANA@X.COM` eran cuentas distintas | Cuentas duplicadas para la misma persona | El correo se guarda y se busca en minúsculas |

Además, un token vencido o inválido cierra la sesión en el frontend y vuelve a `/login`.

### Alineado con sus fichas y diagramas

- Correo ya registrado: **409** (como en `caso6-registro.png`; el código respondía 400).
- Login exitoso: redirige a la **pantalla principal** (`/welcome`), como dice la ficha CU0001 (el código iba a `/invite`).
- Invitación enviada: **200** con "Invitación enviada." (como en `caso10-invitacion.png`; el código respondía 202).
- Mensajes de error con el texto de las fichas: "Credenciales incorrectas.", "Este correo ya está registrado.", "Por favor complete todos los campos correctamente.".

### Invitación guardada y enlace de registro

Para que el código coincida con el modelo de dominio y con la ficha CU0010 del grupo:

- **La invitación se guarda** (tabla `invitations`: correo del invitado, quién invita, fecha y estado). `InvitationService` la crea como `pendiente` y, según el resultado del envío, la pasa a `enviada` o a `fallida`.
- **El correo lleva el enlace de registro** (`FRONTEND_URL/register`), como dice la descripción de CU0010.

### Frontend

- Angular 22 en lugar de 15: Angular CLI 15 no corre con Node 24. Se portaron sus componentes (login, registro, welcome e invitar) y servicios.
- Tema nuevo "Índigo" en `frontend/src/styles.css`: acceso con fondo degradado y tarjeta central, barra superior con sesión y tarjetas de acción. Los `alert()` pasan a avisos dentro de la página.

### Robustez

- **Timeout en el envío del correo:** Flask-Mail abría la conexión SMTP sin timeout, así que un servidor de correo que no responde dejaba la invitación esperando. Ahora corta a los `MAIL_TIMEOUT` segundos (5 por defecto) y la invitación queda `fallida` (hallazgo H7).
- **Registro simultáneo con el mismo correo:** respondía 500; ahora responde 409 "Este correo ya está registrado." (hallazgo H8).
- **Token vencido en el navegador:** `AuthGuard` solo miraba si había token guardado; ahora lee su vencimiento y, si venció, cierra la sesión y manda a `/login` (hallazgo H6).
- **`AuthService` con una sola convención:** `register_user` devuelve el usuario o `None`, igual que `authenticate` (antes devolvía una tupla; hallazgo H9).
- **Dirección del backend configurable:** sale de `frontend/src/environments/environment.ts` (estaba escrita en cada servicio; hallazgo H10).
- **Migraciones:** el esquema sale de las migraciones de Alembic (`backend/migrations/`) en lugar de `db.create_all()`; una base anterior se adopta sin perder datos (hallazgo H11).

### Pruebas

El original no tenía pruebas automáticas. Se agregaron 42 en `backend/tests/` (pytest), que cubren los tres casos de uso, cada corrección de seguridad y las migraciones, y 11 en el frontend (Vitest) para los servicios y el guard de Angular.

## Diferencias entre los documentos de la compañera y el código

Sus fichas y diagramas se conservan **tal cual**, como los hizo la compañera. Las versiones que coinciden con el código son las de las otras etapas:

| Artefacto | Versión que coincide con el código |
|---|---|
| Fichas de CU0001, CU0006 y CU0010 | `1. Requerimientos/4_Casos de Uso/` (`CU0001_Iniciar_Sesión.docx`, `CU0006.docx` y `CU0006_Registrar_Usuario.docx`, `CU0010.docx`) |
| Diagramas de secuencia de los tres casos | `3. Diseño/4_Diagramas de Secuencia/`, con la misma estética que los de acá |

### Diagramas de secuencia (`2_Diagramas de Secuencia/`)

- **`caso1-login.png`:** `check_password_hash` aparece dentro de la rama "Credenciales válidas", es decir, después de decidir que lo eran; en el código (`AuthService.authenticate`) la contraseña se verifica **antes** de decidir. El token lo crea `AuthService` y el método se llama `login`; en el código lo crea `auth_controller` y el método es `authenticate`. El DAO se llama `UsuarioDAO`; en el código, `UserDAO`.
- **`caso6-registro.png`:** usa `UsuarioDAO` (`UserDAO` en el código) y termina con "Registro Exitoso" (la pantalla dice "Cuenta creada con éxito. Ya podés iniciar sesión."). No muestra el camino de datos inválidos (400).
- **`caso10-invitacion.png`:** llama `getInstance().enviar_invitacion(email_invitado)`; en el código es `NotificationService().send_invitation(email, inviter_name)` (el Singleton está en `__new__`). Anota "Simula envío SMTP", pero el correo **se envía de verdad** salvo con `MAIL_SUPPRESS_SEND=true`. La respuesta usa la clave `message` (el código usa `msg`). No tiene caminos alternativos (sin sesión, correo inválido, fallo del envío) ni muestra que la invitación se guarda.

### Fichas (`1_Casos de Uso/`)

- **`CU001-login.docx.pdf`:** los pasos citan {rnf 4.1} y {rnf 5.1}, que no existen en su tabla; el ca 5.1 se titula "Email ya registrado" pero describe credenciales incorrectas; rnf 1.1 exige HTTPS, que no está implementado (RNF-10, "No cumplido"); Ob 1 llama "segura" a `localStorage`, que es accesible desde JavaScript.
- **`CU0006-registro.docx.pdf`:** el título quedó como "NOMBRE CASO DE USO"; "contraseña segura" no está definida (el código pide 8 caracteres o más); el ca 3.1 cuelga del paso 3, pero la validación es el paso 5.
- **`CU0010-invitar.docx.pdf`:** la precondición es "Ninguna", pero invitar exige sesión; los cursos alternativos cuelgan de pasos que no corresponden (ca 1.1 valida el formato, que es el paso 4; ca 2.1 trata el envío, que es el paso 5); habla de "notificación de fallo de entrega", pero el sistema solo detecta errores al enviar, no rebotes posteriores.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 2.1 | 25/11/2026 | Implementación | Las invitaciones se guardan con su estado y el correo lleva el enlace de registro (para coincidir con el modelo de dominio y la ficha CU0010); 33 pruebas |
| 2.2 | 26/11/2026 | Implementación | Diferencias de los tres diagramas y las tres fichas de la compañera con el código, y dónde están las versiones que coinciden (I-01 a I-04) |
| 2.3 | 26/11/2026 | Implementación | Timeout SMTP y registro simultáneo resueltos (H7, H8); 37 pruebas |
| 2.4 | 26/11/2026 | Implementación | H6, H9, H10 y H11 resueltos; 42 pruebas del backend y 11 del frontend |
