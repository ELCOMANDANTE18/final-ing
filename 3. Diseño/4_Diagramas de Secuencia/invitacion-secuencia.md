# CU0010 — Invitación a la aplicación — Diagrama de secuencia

**Versión:** 1.0 · **Última modificación:** 26/11/2026 · **Etapa:** Diseño

Curso normal y cursos alternativos de la ficha CU0010 (ca 4.1 y ca 5.1), más el caso de sesión vencida, con los nombres del código actual. Sigue la estética del diagrama de la compañera (`4. Implementacion/2_Diagramas de Secuencia/caso10-invitacion.png`) y corrige lo anotado en la observación I-03: el correo **se envía de verdad**, la invitación se guarda con su estado y están los caminos alternativos.

<!-- png: 3. Diseño/4_Diagramas de Secuencia/CU0010 - Invitación a la aplicación.png -->
```mermaid
---
config:
  theme: redux-color
---
sequenceDiagram
    autonumber
    actor U as Usuario Autenticado
    participant I as InviteComponent (Angular)
    participant N as NotificationService (Angular)
    participant T as TokenInterceptor
    participant K as @token_required
    participant C as invite_controller (Flask)
    participant S as InvitationService
    participant D as InvitationDAO
    participant M as NotificationService «Singleton»
    participant B as Base de Datos (SQLite)
    participant G as Servidor de Correo (Gmail)

    U->>I: Ingresa el email del invitado y presiona "Enviar invitación"
    alt ca 4.1 — Formato inválido o más de 254 caracteres
        I-->>U: Muestra "Ingresá un correo válido."
    else Email con formato válido
        I->>N: sendInvite(email)
        N->>T: POST /invite {email}
        T->>T: Agrega Authorization: Bearer access_token
        T->>K: POST /invite {email} + Bearer
        activate K
        K->>K: verify_jwt_in_request() y UserDAO.get_by_id(identity)
        alt Token inválido o vencido
            K-->>T: 401 {msg: "Sesión inválida o vencida. Iniciá sesión de nuevo."}
            T->>T: logout() y navega a /login
        else Sesión válida
            K->>C: invite(current_user)
            activate C
            Note right of C: InviteSchema (marshmallow):<br/>email RFC 5322, máx. 254
            alt ca 4.1 — Email inválido
                C-->>N: 400 {msg: "Ingresá un correo válido."}
                N-->>I: error
                I-->>U: Muestra el mensaje
            else Email válido
                C->>S: invite(inviter=current_user, email)
                activate S
                S->>D: create(email, inviter_id)
                D->>B: INSERT INTO invitations (status = 'pendiente')
                B-->>D: id asignado
                D-->>S: Invitation (pendiente)
                Note over S,M: NotificationService() devuelve siempre la misma instancia
                S->>M: send_invitation(email, inviter.name)
                M->>G: SMTP + TLS: correo con el enlace FRONTEND_URL/register
                alt ca 5.1 — El servidor de correo rechaza el envío o no responde
                    G-->>M: error
                    M-->>S: excepción
                    S->>D: update_status(invitation, 'fallida')
                    D->>B: UPDATE invitations SET status = 'fallida'
                    S-->>C: excepción
                    C->>C: Registra el detalle en el log
                    C-->>N: 500 {msg: "No se pudo enviar la invitación. Intentá de nuevo."}
                    N-->>I: error
                    I-->>U: Muestra el aviso y deja el formulario listo para reintentar
                else Envío aceptado
                    G-->>M: aceptado
                    M-->>S: ok
                    S->>D: update_status(invitation, 'enviada')
                    D->>B: UPDATE invitations SET status = 'enviada'
                    S-->>C: Invitation (enviada)
                    C-->>N: 200 {msg: "Invitación enviada."}
                    N-->>I: {msg}
                    I-->>U: Muestra "Invitación enviada. Le llegará un correo a (email)."
                end
                deactivate S
            end
            deactivate C
        end
        deactivate K
    end
```

## Notas

- **La invitación se guarda antes de enviar el correo** (Ob 1 de la ficha) y su estado cambia según el resultado: `pendiente` → `enviada`, o `pendiente` → `fallida`. El diagrama de estados está en `5_Diagramas de Estado/`.
- **Singleton:** `InvitationService` crea `NotificationService()` en cada invitación, pero `__new__` devuelve siempre la misma instancia. El diagrama de la compañera usaba `getInstance()`, que no existe en el código (I-03).
- **El envío es real:** Flask-Mail se conecta a Gmail por SMTP con TLS. Solo se simula si `MAIL_SUPPRESS_SEND=true` en el `.env` (sirve para probar sin credenciales).
- **Servidor de correo que no responde** (ca 5.1): la conexión SMTP espera como máximo `MAIL_TIMEOUT` segundos (5 por defecto) por operación; al vencer, el envío falla por el mismo camino del diagrama (mensajes 21 a 29).
- **Mensaje genérico ante el fallo** (ca 5.1): el detalle del error del servidor de correo queda en el log del backend y no llega al navegador.
- **Sesión vencida:** no es un curso alternativo de la ficha (la precondición pide sesión iniciada), pero el código lo maneja: `@token_required` responde 401 y `TokenInterceptor` cierra la sesión local y lleva a `/login`.
- **Rebotes:** si el correo rebota después de aceptado, el sistema no se entera (Ob 2 de la ficha).

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 26/11/2026 | Diseño | Versión inicial, a partir del código actual y la ficha CU0010, con la estética de los diagramas de la compañera |
