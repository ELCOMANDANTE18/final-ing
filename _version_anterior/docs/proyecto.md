# UMBook — Proyecto

**Versión:** 1.1 · **Última modificación:** 20/11/2026 · **Etapa:** Gestión del proyecto

> ⚠️ **Desactualizado respecto del código (25/11/2026).** La implementación de `4. Implementacion/` pasó a ser la del repositorio de una compañera del grupo: **CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación**, con correcciones de seguridad y frontend nuevo (ver `4. Implementacion/README.md`). Este documento describe la implementación anterior (amistad y notificaciones: CU0011, CU0012 y CU0013), que ya no está en el código. Queda pendiente de realinear: ver `docs/tareas.md`.

Aplicación de gestión de usuarios para la materia Ingeniería de Software.
Backend Flask + frontend Angular (detalle técnico en [`backend.md`](./backend.md) y
[`frontend.md`](./frontend.md)).

## Casos de uso implementados

| CU | Nombre | Actor | Estado |
|---|---|---|---|
| CU0001 | Login (Iniciar Sesión) | Usuario Registrado | ✅ implementado |
| CU0006 | Registrar Usuario | Usuario no registrado | ✅ implementado |
| CU0011 | Solicitar Amistad | Usuario autenticado | ✅ implementado (patrón State) ⚠️ código con choques |
| CU0012 | Aceptar / Rechazar Solicitud de Amistad | Usuario autenticado | ✅ implementado (patrón State) ⚠️ código con choques |
| CU0013 | Notificar Solicitud de Amistad Recibida | Usuario autenticado | ✅ implementado (patrón Observer + Singleton) ⚠️ código con choques |
| CU0010 | Invitación a la aplicación | Usuario autenticado | ❌ fuera de alcance (ver abajo) |

### CU0001 — Login
- Precondición: no haber iniciado sesión.
- Flujo: form login → valida email+password (hash) → genera JWT → redirige a **Welcome**.
- Alternativos: campos vacíos/formato inválido → "Por favor complete todos los campos
  correctamente"; credenciales incorrectas (email inexistente O contraseña
  incorrecta) → error genérico "Credenciales incorrectas".
- RNF: passwords nunca en texto plano (hash con Werkzeug), JWT, respuesta < 2s. JWT
  se guarda en LocalStorage.

### CU0006 — Registrar Usuario
- Precondición: no haber iniciado sesión.
- Flujo: form registro (nombre, email, password) → valida (email válido, password
  mínimo 8 caracteres) → guarda usuario → redirige a login.
- Alternativos: campos faltantes/formato inválido → error, vuelve al form; email ya
  registrado → "Este correo ya está registrado."

### Solicitar Amistad / Aceptar-Rechazar Solicitud
- Precondición: usuario autenticado.
- Flujo: enviar solicitud por email de otro usuario → queda en estado `pendiente` →
  el receptor la acepta o rechaza.
- Reglas: no podés solicitarte amistad a vos mismo, no se puede duplicar una
  solicitud pendiente para el mismo par de usuarios, no se puede responder una
  solicitud ajena (403), un estado terminal (`aceptada`/`rechazada`) no admite
  nuevas transiciones (409).
- Diseño: patrón **State** — ver [`construccion.md` sección 2](./construccion.md#2-solicitar-amistad--aceptar-rechazar-solicitud--patrón-state).

### Notificar Solicitud de Amistad Recibida
- Se implementó como **consulta derivada** (no hay entidad `Notificacion` propia):
  la lista de solicitudes pendientes recibidas por un usuario ES la notificación
  que ve en su home. Además, al crearse la solicitud se dispara un email al
  receptor vía el patrón **Observer** sobre el `NotificationService` (Singleton).
- Diseño: ver [`construccion.md` sección 3](./construccion.md#3-notificar-solicitud-de-amistad-recibida--observer-sobre-el-singleton-existente).

### CU0010 — Invitación a la aplicación (fuera de alcance)
No se implementó. Su legitimidad como CU del enunciado real está en discusión (no
tiene base confirmada, se había descartado del diagrama de CU general por este
motivo) y `docs/prompt-construccion.md` es explícito en que no hay que usar su
infraestructura como base para nada nuevo. Como el proyecto se construyó desde
cero, se decidió no implementarlo en vez de construir algo cuya validez está en
duda para después tener que justificarlo en la defensa.

## Decisiones de diseño ya tomadas (no rediscutir sin motivo)

- **Códigos de CU**: no hay lista maestra confirmada de números de CU para
  Solicitar/Aceptar Amistad y Notificar — se referencian por nombre, no se
  inventaron códigos nuevos (`CU0011`/`CU0012` ya habían demostrado estar mal en
  una iteración anterior).
- **Notificación como consulta derivada**, no como entidad propia (ver arriba) —
  opción más simple, explícitamente preferida en `docs/prompt-construccion.md`
  salvo indicación en contra.
- **Token de un solo uso para links de email**: si en algún momento se agrega un
  flujo de aceptar/rechazar solicitud **sin login**, cliqueando un link recibido
  por mail, ese link necesita un token propio, no adivinable y con expiración —
  nunca reutilizar el JWT de sesión para eso. Hoy el flujo implementado es
  autenticado (requiere estar logueado en la app), así que este token todavía no
  existe — ver pendientes en [`tareas.md`](./tareas.md).

## Estructura de la documentación

- [`00_INDICE.md`](./00_INDICE.md) — índice de toda la documentación (leer primero).
- [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) — códigos de los
  casos de uso implementados y choques con otras fichas del repositorio. **Los códigos de
  CU de esta tabla pueden diferir de los de ese catálogo; manda el catálogo.**
- [`backend.md`](./backend.md) — arquitectura y convenciones del backend Flask.
- [`frontend.md`](./frontend.md) — arquitectura y convenciones del frontend Angular.
- [`construccion.md`](./construccion.md) — paso a paso de cómo se construyó cada
  una de las 3 implementaciones y por qué (los patrones de diseño, el bug de login
  que se evitó, las decisiones de transacción/autorización).
- [`tareas.md`](./tareas.md) — checklist de lo que falta antes de la defensa.
- [`prompt-construccion.md`](./prompt-construccion.md) — spec original que se usó
  como input para construir el proyecto (documento histórico, ya ejecutado).
- [`3. Diseño/`](../3.%20Diseño) — diagramas de clases, de estados y de secuencia del
  proyecto (UML propio del alumno, agregado aparte).

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.1 | 20/11/2026 | Gestión del proyecto | Se agrega el control de versiones y la referencia a `CATALOGO_CASOS_DE_USO_UMBook.md` para los códigos de CU |
