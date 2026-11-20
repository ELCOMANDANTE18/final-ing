# Tareas — UMBook

**Versión:** 1.1 · **Última modificación:** 20/11/2026 · **Etapa:** Gestión del proyecto

Actualizado tras construir el proyecto desde cero (no había código previo de la
compañera en este repo — ver [`construccion.md`](./construccion.md)).

## Resuelto

- [x] Login: la contraseña se valida con `check_password_hash` **antes** de decidir
  la rama éxito/error — no hay bypass de autenticación posible. Ver
  `backend/app/services/auth_service.py`.
- [x] `AuthGuard` aplicado a `/welcome` en `app.module.ts`.
- [x] Redirect post-login a `/welcome` (no a `/invite` — CU0010 no se implementó).
- [x] `app/config.py` como única fuente de configuración; `JWT_SECRET_KEY` y
  credenciales de mail viven en `backend/.env` (nunca commiteado), no hardcodeadas.
- [x] Solicitar Amistad + Aceptar/Rechazar con patrón State
  (`backend/app/services/estados/estado_solicitud.py`).
- [x] Transacción única para estado `aceptada` + creación del vínculo `Amistad`
  (rollback conjunto si falla cualquiera de las dos).
- [x] Verificación de autorización: solo el receptor de una solicitud puede
  aceptarla/rechazarla (403 si no).
- [x] Notificar Solicitud Recibida con Observer sobre `NotificationService`
  (Singleton). `AmistadService` nunca llama al Notificador directo.
- [x] Endpoint de solicitudes pendientes, usado como notificación derivada en la
  home, y endpoint de amigos (`GET /amistad/amigos`) para verse la amistad
  confirmada.
- [x] Plantillas de email reales (`backend/app/templates/emails/`) para la
  notificación de solicitud recibida (HTML + texto plano vía Jinja).
- [x] CU0010 (Invitación): decidido explícitamente **fuera de alcance** — ver
  [`proyecto.md`](./proyecto.md).
- [x] Backend corriendo sobre Python 3.14 con versiones actuales de Flask.
- [x] Frontend con diseño propio (`chamba.css` + `frontend/src/styles.css`):
  login/register en split-screen, welcome con sidebar/topbar/cards.
- [x] **Credenciales reales cargadas y probadas**: se mandó un mail real de
  notificación de solicitud de amistad y llegó a la bandeja — el flujo de
  Observer + Singleton + Gmail SMTP funciona de punta a punta.
- [x] **Verificación visual en navegador hecha por el alumno** (no en el
  entorno de construcción): confirmado que login → welcome → amigos →
  solicitar/aceptar/rechazar funciona en un browser real.
- [x] Bug de carga inicial en Welcome (los datos no aparecían hasta interactuar
  con la página): el scaffold de Angular 22 no trae `zone.js` por defecto.
  Se agregó `zone.js` a `angular.json` (`polyfills`) y, como refuerzo, un
  `ChangeDetectorRef.detectChanges()` explícito después de cada respuesta
  HTTP en `WelcomeComponent`/`LoginComponent`/`RegisterComponent` — ver
  `construccion.md`.
- [x] Suite de tests con `pytest` (`backend/tests/`, 32 tests): patrón State en
  aislamiento, Observer + Singleton, regresión del bug de login, y flujo
  completo de amistad tanto a nivel service como HTTP end-to-end. Correr con
  `pip install -r requirements-dev.txt && pytest` desde `backend/`.
- [x] Diagramas de las 3 implementaciones en `3. Diseño/` (Mermaid):
  secuencia de Login, clases State + diagrama de estados + 2 secuencias de
  Solicitar/Aceptar-Rechazar Amistad, clases Observer+Singleton + secuencia de
  Notificar.
- [x] Manejo de sesión expirada en el front: `token.interceptor.ts` desloguea y
  redirige a `/login` automáticamente ante un 401 (JWT vencido) o 422 (JWT
  corrupto) en cualquier request que llevaba token — nunca en `/auth/login`,
  que va sin token. Confirmado con un JWT realmente vencido (no solo uno
  manipulado a mano) que Flask-JWT-Extended da 401 en ese caso, 422 solo para
  formato inválido — cubierto con tests (`test_token_vencido_devuelve_401`,
  `test_token_corrupto_devuelve_422`).

## Pendiente antes de la defensa

- [ ] Generar la primera migración real con Flask-Migrate (hoy el esquema sale de
  `db.create_all()` en `run.py`, sin carpeta `migrations/`) — clave si te toca
  Gestión de Configuración como tema teórico.
- [ ] Si el CU de Aceptar/Rechazar Solicitud exige también un flujo **sin login**
  (clic en un link recibido por mail), falta un token de un solo uso con
  expiración para ese link — no implementado, no estaba en el alcance original de
  "las 3 implementaciones" (ver `prompt-construccion.md` sección 4).

## No bloqueante

- [ ] Angular se generó con CLI 22 en vez de 15 (el entorno de construcción tenía
  Node 24, incompatible con Angular CLI 15) — ver
  [`construccion.md` sección 0](./construccion.md#0-desviaciones-respecto-a-la-especificación-original).
  No es necesario resolverlo salvo que la cátedra pida específicamente Angular 15.

## Pendientes de consistencia (revisión del 20/11/2026)

- [ ] **Resolver los choques de códigos de CU** (CU0006, CU0011, CU0012 y CU0013) con el grupo.
  Ver [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) §3 y §5.
- [x] **Casos y procedimientos de prueba alineados con el comportamiento real**, en
  [`PRUEBAS_UMBook.md`](./PRUEBAS_UMBook.md): sin "Buscar usuarios", sin botón que se oculta y sin
  correo con enlace; con casos y procedimiento para CU0006 y trazados a las pruebas automáticas.
- [x] **Entregables de Pruebas generados** desde `PRUEBAS_UMBook.md` con
  `python docs/generar_entregables.py`: plan, 31 casos (`.xlsx`) y procedimientos (`.docx`) en
  `5. Pruebas/`. `Modelo_Plan_de_Pruebas.docx` es el modelo del grupo y se conserva.
- [x] **Fichas `.docx` regeneradas** con el texto 1.1 de `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md`.
- [x] **Diagrama de casos de uso único:** `0-CU_General.pdf` cumple (un solo diagrama para toda la
  aplicación) pero no lleva códigos; se agrega `Diagrama de Casos de Uso - Implementados.png`.
- [ ] **Pruebas automáticas que faltan:** reenvío tras un rechazo (H1), contraseña corta en el
  registro y reversión de la transacción al aceptar (RNF-12). El frontend no tiene pruebas
  automáticas.
- [ ] Decidir qué diagrama de clases de diseño se entrega: el integral de este repo (solo lo
  implementado) o `UMBook_Diagrama_Clases_Diseno_Integrado.png` del grupo (Álbum, Strategy,
  Factory, Composite: clases que no existen en el código).
- [ ] **Defecto H1:** volver a solicitar amistad a quien rechazó una solicitud devuelve 500
  (restricción única `(emisor_id, receptor_id)`). Decidir si se reabre la solicitud o se responde
  409. Ver [`DISEÑO_UMBook.md`](./DISEÑO_UMBook.md) §9. Agregar una prueba que lo cubra.
- [ ] Avisar al grupo de los códigos repetidos dentro de sus propias fichas (CU0005 y CU0007).
- [ ] Reemplazar o archivar `Diseño de Arquitectura - UMBook.docx`: describe un sistema distinto
  del implementado (ver `DISEÑO_UMBook.md` §8).

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.1 | 20/11/2026 | Gestión del proyecto | Se agrega el control de versiones; la cantidad de pruebas pasa de 30 a 32; pendientes de consistencia (códigos de CU, procedimientos de prueba, defecto H1) |
