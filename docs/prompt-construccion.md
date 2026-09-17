# Prompt de construcción — UMBook (Login fixes + Solicitar/Aceptar Amistad + Notificar Solicitud)

> **Documento histórico**: esta es la especificación que se usó como input para
> construir el proyecto. Ya está ejecutada — para ver qué se implementó
> efectivamente y por qué, ir a [`construccion.md`](./construccion.md). Se conserva
> acá tal cual para trazabilidad de las decisiones de diseño.

Contexto para vos (Claude Code): este repo ya tiene un `imple.md` (arquitectura, convenciones,
deuda conocida) y un `tareas.md` (checklist priorizado). Leé los dos primero. Este prompt agrega
el diseño de las 3 funcionalidades nuevas y las decisiones que ya se tomaron para que no haya que
redecidirlas en el camino.

## 0. Antes de tocar código — precondiciones

- [ ] Confirmar que el entorno corre con Python 3.11 o 3.12 (Flask 2.3.2 / Werkzeug 2.3.6 no
      soportan 3.13+). Si no corre, es lo primero a resolver — nada más avanza sin esto.
- [ ] Las credenciales de Gmail en `.env` son las del usuario que ejecuta esta sesión, **no** las
      que estaban hardcodeadas en `backend/test_smtp.py`. Confirmar que `.env` está en
      `.gitignore` antes de escribir nada ahí.
- [ ] La app password anterior fue reportada al dueño original del repo para que la revoque — no
      es una tarea de este repo, solo dejarlo asentado.

## 1. Alcance — 3 implementaciones, en este orden

1. **Cerrar Login** (ya implementado, tiene bugs reales — no es una reescritura, es una
   corrección quirúrgica).
2. **Solicitar Amistad + Aceptar/Rechazar Solicitud** (nuevo, patrón **State**).
3. **Notificar Solicitud de Amistad Recibida** (nuevo, patrón **Observer** sobre el
   `NotificationService` Singleton que ya existe).

No implementar nada fuera de esta lista sin confirmar antes (en particular, no tocar ni extender
`CU0010 — Invitación a la aplicación`: su legitimidad está en discusión, ver sección 5).

## 2. Login — bugs confirmados a corregir

- **Verificar orden real de validación de contraseña en `auth_service.py`.** El diagrama de
  secuencia documentado muestra `check_password_hash` ejecutándose *después* de haber elegido la
  rama "credenciales válidas", no antes de decidir la rama. Si el código tiene el mismo orden,
  es un bypass de autenticación: cualquier contraseña entraría mientras el email exista.
  Corregir para que la verificación de contraseña ocurra *antes* de la bifurcación éxito/error,
  y que el `alt` cubra explícitamente ambos casos (usuario inexistente Y contraseña incorrecta).
- **Aplicar `AuthGuard`** a `/welcome` e `/invite` en `app.module.ts` — hoy no está en ninguna
  ruta, así que cualquiera navega ahí sin token aunque el backend exija `@token_required`.
- **Corregir el redirect post-login**: hoy va a `/invite`, tiene que ir a `/welcome`.
- **Activar `app/config.py`** como fuente única de configuración (`JWT_SECRET_KEY` incluido);
  hoy `create_app()` lo ignora y hardcodea valores propios.

## 3. Diseño de clases — usar exactamente esto (ya reconciliado, no rediseñar)

```
SolicitudAmistad { emisor: Usuario, receptor: Usuario, estado: EstadoSolicitud, fechaCreacion }
  + aceptar()  + rechazar()  + setEstado(EstadoSolicitud)

EstadoSolicitud (interface)  →  Pendiente, Aceptada, Rechazada
  + aceptar(SolicitudAmistad)  + rechazar(SolicitudAmistad)

Usuario implements Observable
  + agregarObservador() + eliminarObservador() + notificarObservadores(evento)

Notificador <<Singleton>> implements Observador   ← YA EXISTE como Singleton puro; sumarle Observador
  - static instance     + static getInstance()
  + actualizar(evento)                              ← método nuevo a agregar (interfaz Observador)
  + enviarEmail(destinatario, mensaje)  + notificar(evento)   ← ya existentes, no tocar firma
```

**Flujo de notificación (importante, es el punto que hace válido el patrón Observer):**
`AmistadService.solicitarAmistad()` NO debe llamar a `Notificador` directamente. Tiene que llamar
a `receptor.notificarObservadores("solicitud_recibida")`, y `Notificador` — ya registrado como
observador de ese `Usuario` — reacciona vía `actualizar()`. Si el service llama al Notificador
directo, no hay Observer, hay una llamada de servicio común y la defensa no se sostiene.

**Transacción:** `aceptarSolicitud()` cambia `estado` a `Aceptada` Y crea el vínculo de amistad en
la misma transacción de SQLAlchemy. Si falla la creación del vínculo, el estado no debe quedar
en `Aceptada` (rollback conjunto).

## 4. Requisitos no funcionales que aplican a este código

- El link de confirmación/rechazo enviado por email usa un token único, no adivinable, con
  expiración — no reutilizar el JWT de sesión para esto, es un token de un solo propósito.
- Toda acción nueva pasa por verificación de autorización (rol/pertenencia) antes de ejecutarse —
  mismo principio que el bug de AuthGuard ya expuso, no repetirlo acá.
- El hashing de contraseñas (Werkzeug) ya está resuelto en Login/Registro — no es parte de este
  alcance.

## 5. No decidir esto solo — preguntar antes si se vuelve relevante

- **Códigos de CU reales.** No hay lista maestra confirmada todavía. Usar los nombres de CU en
  comentarios/commits, no números — no inventar códigos nuevos (`CU0011`, `CU0012` ya
  demostraron estar mal, no repetir el patrón).
- **CU0010 (Invitación a la aplicación)** no tiene base confirmada en el enunciado. No usar su
  infraestructura como base para Solicitar Amistad aunque el flujo se vea parecido (invitar por
  email a un desconocido ≠ pedir amistad a un usuario existente).
- **Si "Notificar Solicitud Recibida" necesita su propio endpoint o alcanza con que la home
  consulte notificaciones pendientes de `Usuario`** — no está cerrado si es un caso de uso con
  entidad propia o una consulta derivada. Implementar la segunda opción (más simple) salvo que
  se indique lo contrario.

## 6. Criterio de aceptación

Cada funcionalidad se valida contra los Casos de Prueba ya escritos (Login: `CP 1.1–1.3`;
Solicitar Amistad: `CP SA.1–SA.3`; Aceptar/Rechazar: `CP AR.1–AR.3`; Notificar: `CP NT.1–NT.3`).
`CP 3.1` de Login es el que confirma o descarta el bug de bypass de contraseña — correrlo primero,
antes de dar Login por cerrado.
