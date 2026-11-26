# Tareas — UMBook

**Versión:** 1.7 · **Última modificación:** 26/11/2026 · **Etapa:** Gestión del proyecto

Actualizado tras construir el proyecto desde cero (no había código previo de la
compañera en este repo — ver [`construccion.md`](../_version_anterior/docs/construccion.md)).

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
  [`proyecto.md`](../_version_anterior/docs/proyecto.md).
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
- [x] Suite de tests con `pytest` (`backend/tests/`, 39 tests): patrón State en
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

- [x] **Migraciones con Flask-Migrate (26/11/2026):** `backend/migrations/` con `0001_users` y
  `0002_invitations`; `run.py` las aplica al arrancar (H11) — clave si te toca Gestión de
  Configuración como tema teórico.
- [ ] Si el CU de Aceptar/Rechazar Solicitud exige también un flujo **sin login**
  (clic en un link recibido por mail), falta un token de un solo uso con
  expiración para ese link — no implementado, no estaba en el alcance original de
  "las 3 implementaciones" (ver `prompt-construccion.md` sección 4).

## No bloqueante

- [ ] Angular se generó con CLI 22 en vez de 15 (el entorno de construcción tenía
  Node 24, incompatible con Angular CLI 15) — ver
  [`construccion.md` sección 0](../_version_anterior/docs/construccion.md#0-desviaciones-respecto-a-la-especificación-original).
  No es necesario resolverlo salvo que la cátedra pida específicamente Angular 15.

## Pendientes de consistencia (revisión del 20/11/2026)

- [ ] **Resolver los choques de códigos de CU** (CU0006, CU0011, CU0012 y CU0013) con el grupo.
  Ver [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) §3 y §5.
- [x] **Casos y procedimientos de prueba alineados con el comportamiento real**, en
  [`PRUEBAS_UMBook.md`](./PRUEBAS_UMBook.md): sin "Buscar usuarios", sin botón que se oculta y sin
  correo con enlace; con casos y procedimiento para CU0006 y trazados a las pruebas automáticas.
- [x] **Entregables de Pruebas generados** desde `PRUEBAS_UMBook.md` con
  `python docs/generar_entregables.py`: plan, 33 casos (`.xlsx`) y procedimientos (`.docx`) en
  `5. Pruebas/`. `Modelo_Plan_de_Pruebas.docx` es el modelo del grupo y se conserva.
- [x] **Fichas `.docx` regeneradas** con el texto 1.2 de `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md`.
- [x] **Diagrama de casos de uso único:** `0-CU_General.pdf` cumple (un solo diagrama para toda la
  aplicación) pero no lleva códigos; se agrega `Diagrama de Casos de Uso - Implementados.png`.
- [x] **Pruebas automáticas que faltaban:** la contraseña corta en el registro está cubierta
  (`test_clave_corta_devuelve_400_y_no_crea_el_usuario`) y el frontend tiene 11 pruebas (Vitest)
  para sus servicios y el guard. La reversión al aceptar una solicitud era de amistad (ya no está).
- [x] **Diagrama de clases de diseño (26/11/2026):** se entrega uno hecho a partir del código
  actual (CU0001, CU0006, CU0010), con Singleton, DAO y Decorator: `3. Diseño/3_Diagramas de
  Clases/diseno-clases.md`. Los de amistad pasan a `_version_anterior/`.
- [x] **Defecto H1 resuelto (25/11/2026):** el reenvío tras un rechazo crea una solicitud nueva
  (la rechazada queda como historial, estado terminal). La restricción única sobre el par pasó a
  ser un índice único parcial sobre las pendientes. Ver [`DISEÑO_UMBook.md`](./DISEÑO_UMBook.md) §9.
- [x] **Defecto H2 resuelto (25/11/2026):** si falla el servidor de correo, el error se registra
  y la solicitud se crea igual (201). RNF-11 cumplido para este aviso.
- [x] **Defecto H5 resuelto (25/11/2026):** la solicitud cruzada (B le pide a A cuando A ya le
  pidió a B) responde 409; antes aceptar las dos daba 500.
- [ ] **Recrear la base local** (`instance/umbook.db`): fue creada con el esquema anterior y
  `db.create_all()` no altera tablas existentes. Borrarla, correr `python run.py` y `python seed.py`.
  Con Flask-Migrate (pendiente de arriba) esto sería una migración.
- [ ] Avisar al grupo de los códigos repetidos dentro de sus propias fichas (CU0005 y CU0007).
- [ ] Reemplazar o archivar `Diseño de Arquitectura - UMBook.docx`: describe un sistema distinto
  del implementado (ver `DISEÑO_UMBook.md` §8).

## Cambio de implementación (25/11/2026)

La implementación pasa a ser la del repositorio de una compañera del grupo
([MaguiMaluff/final-software](https://github.com/MaguiMaluff/final-software)), con su acuerdo:
CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación. Detalle en
`4. Implementacion/README.md`.

- [x] Código de la compañera en `4. Implementacion/codigo/`, con 10 correcciones de seguridad (clave
  JWT fija, depurador expuesto en la red, credenciales en `test_smtp.py`, TLS que no se activaba,
  logout que no cerraba sesión, rutas sin guard, errores con detalles internos, versiones
  vulnerables, etc.).
- [x] Frontend portado a Angular 22 con tema nuevo ("Índigo").
- [x] 29 pruebas automáticas nuevas (el original no tenía).
- [x] Sus fichas y diagramas de secuencia, tal cual, en `4. Implementacion/1_Casos de Uso/` y
  `2_Diagramas de Secuencia/`.
- [x] Verificado en un navegador: registro, login, clave incorrecta, invitación, correo inválido,
  cerrar sesión, ruta protegida sin sesión y token inválido.
- [ ] **Avisarle a la compañera** que revoque la *app password* de Gmail que quedó escrita en
  `backend/test_smtp.py` de su repositorio público, y que saque ese archivo y `instance/umbook.db`.
- [x] **Documentos de etapa realineados** con la implementación nueva (26/11/2026): las cinco
  etapas, con sus diagramas y entregables generados. Pruebas: 29 casos trazados a las 37 pruebas.
  Los documentos técnicos viejos (`proyecto.md`, `backend.md`, `frontend.md`, `construccion.md`,
  `prompt-construccion.md`) pasaron a `_version_anterior/docs/`. Detalle en
  `OBSERVACIONES_POR_ETAPA_UMBook.md`.
- [x] **H7 y H8 resueltos (26/11/2026):** timeout en la conexión SMTP (`MAIL_TIMEOUT`, 5 s) y
  registro simultáneo con el mismo correo respondiendo 409. 4 pruebas nuevas, 37 en total.
- [x] **H6, H9, H10 y H11 resueltos (26/11/2026):** token vencido en `AuthGuard`, `AuthService`
  con una sola convención, dirección del backend en `environment.ts` y migraciones de Alembic.
  Todos los hallazgos de diseño quedan cerrados.
- [ ] Los pendientes de arriba sobre amistad (H1, H2, H5, recrear la base, migración) quedan sin
  efecto: ese código ya no está. El respaldo del código anterior está en el historial de git
  (último commit) salvo los arreglos del 25/11, que no se commitearon.
- [ ] La base local `instance/umbook.db` tiene las tablas viejas (`usuarios`, `solicitudes_amistad`,
  `amistades`) además de la nueva `users`. Se puede borrar: `run.py` la vuelve a crear.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.7 | 26/11/2026 | Gestión del proyecto | H6, H9, H10 y H11 resueltos; migraciones y pruebas del frontend |
| 1.6 | 26/11/2026 | Gestión del proyecto | H7 y H8 resueltos con sus pruebas (37) |
| 1.5 | 26/11/2026 | Gestión del proyecto | Etapas 4 y 5 realineadas; documentos técnicos viejos archivados; hallazgos H6 a H11 como pendiente |
| 1.4 | 26/11/2026 | Gestión del proyecto | Diagrama de clases de diseño del código actual (D-03); Etapa 3 realineada (D-01 a D-08) |
