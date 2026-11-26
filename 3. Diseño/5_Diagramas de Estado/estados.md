# Diagramas de estados — UMBook (casos implementados)

**Versión:** 1.1 · **Última modificación:** 26/11/2026 · **Etapa:** Diseño

Lámina `Diagramas de Estado.png` (y `.svg`), generada con `docs/generar_estados.py`. Tiene la forma del `Diagrama_de_Estado.pdf` del grupo (un título y un diagrama por entidad, con el estilo de estados de PlantUML), pero modela **cosas que existen en el código actual**. El PDF del grupo modelaba Solicitud de Amistad, Usuario y Notificación, que no tienen estados en el código; está en `_version_anterior/3. Diseño/5_Diagramas de Estado/` (observación D-05).

## Invitación (CU0010)

El estado es la columna `status` de la tabla `invitations` (`backend/app/persistence/models.py`). Lo cambia `InvitationService.invite` a través de `InvitationDAO`.

| Desde | Hacia | Evento [condición] / acción | Dónde |
|---|---|---|---|
| (inicio) | Pendiente | `InvitationDAO.create(email, inviter_id)` [email válido según `InviteSchema`, sesión iniciada] | `InvitationService.invite`, antes de enviar el correo |
| Pendiente | Enviada | el servidor de correo acepta el envío / `update_status(invitation, 'enviada')` | `InvitationService.invite`, después de `NotificationService.send_invitation` |
| Pendiente | Fallida | el servidor de correo rechaza el envío o no responde / `update_status(invitation, 'fallida')` | `InvitationService.invite`, en el `except` (ca 5.1 de la ficha) |
| Enviada, Fallida | (fin) | — | Estados finales: el código no tiene ninguna transición que salga de ellos |

- **Reintentar** (ca 5.1, "ofrece reintentar") crea una invitación **nueva** en Pendiente; la fallida queda como registro.
- **Rebotes:** si el correo rebota después de que el servidor lo aceptó, el estado sigue en Enviada (Ob 2 de la ficha).
- Las tres constantes están en la clase `Invitation`: `PENDIENTE`, `ENVIADA` y `FALLIDA`.

## Sesión del usuario en el frontend (CU0001)

El estado es la presencia del `access_token` en `localStorage` y su validez en el backend. Lo manejan `AuthService`, `AuthGuard` y `TokenInterceptor` (`frontend/src/app/core/`).

| Desde | Hacia | Evento [condición] / acción | Dónde |
|---|---|---|---|
| (inicio) | Sin sesión | abre la aplicación [no hay `access_token`] | — |
| Sin sesión | Sin sesión | pide `/welcome` o `/invite` / `AuthGuard` redirige a `/login` | `AuthGuard.canActivate` |
| Sin sesión | Sesión iniciada | `login()` responde 200 / guarda `access_token` y nombre en `localStorage` | `AuthService.login` (CU0001, paso 7) |
| Sesión iniciada | Sin sesión | `logout()` (botón "Cerrar sesión") | `AppComponent.logout`, `WelcomeComponent.goToLogin` |
| Sesión iniciada | Token vencido | pasan 15 minutos | Flask-JWT-Extended: sin `JWT_ACCESS_TOKEN_EXPIRES` en `config.py`, el token dura 15 minutos |
| Token vencido | Sin sesión | pide una pantalla protegida / `logout()` y navega a `/login` | `AuthGuard.canActivate` → `AuthService.isAuthenticated()`, que lee el `exp` del token |
| Token vencido | Sin sesión | una petición responde 401 / `logout()` y navega a `/login` | `TokenInterceptor.intercept`; el 401 lo da `@token_required` |

- **Token vencido es un estado propio** porque el vencimiento no se avisa: el frontend lo detecta recién cuando el usuario navega a una pantalla protegida (`AuthGuard` lee el `exp` del token) o cuando una petición responde 401. Antes `isAuthenticated()` solo miraba si había token, así que se podían abrir las pantallas con el token vencido (hallazgo H6, resuelto).
- No hay estado final: la aplicación siempre vuelve a Sin sesión.

## Por qué no hay diagrama de Usuario ni de Notificación

`User` no tiene estado (no hay `activo`, `suspendido` ni similares) y las notificaciones no se guardan: `NotificationService` envía el correo y no deja registro propio. El único registro del envío es el estado de la `Invitation`.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 26/11/2026 | Diseño | Versión inicial: Invitación y Sesión del usuario, a partir del código actual, con la forma del PDF del grupo |
| 1.1 | 26/11/2026 | Diseño | `AuthGuard` detecta el token vencido al navegar (H6) |
