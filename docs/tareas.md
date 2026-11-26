# Tareas — UMBook

**Versión:** 2.0 · **Última modificación:** 26/11/2026 · **Etapa:** Gestión del proyecto

Estado del proyecto y lo que falta antes de la defensa. La implementación es la del repositorio de una compañera del grupo ([MaguiMaluff/final-software](https://github.com/MaguiMaluff/final-software), commit `fe825751`), con su acuerdo: **CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación**. El detalle de cada etapa está en [`OBSERVACIONES_POR_ETAPA_UMBook.md`](./OBSERVACIONES_POR_ETAPA_UMBook.md).

La versión anterior de esta lista, con las tareas de la implementación de amistad (CU0011 a CU0013), está en `_version_anterior/docs/tareas (hasta 1.7).md`.

## Pendiente

- [ ] **Avisarle a la compañera** que revoque la *app password* de Gmail que quedó escrita en
  `backend/test_smtp.py` de su repositorio público, y que saque de ahí ese archivo y
  `instance/umbook.db`. Es un riesgo de seguridad real y solo lo puede resolver ella.
- [ ] **Pruebas manuales en el navegador**, siguiendo `5. Pruebas/2_Procedimientos de Prueba.docx`
  (PR 0001, PR 0006, PR 0010 y el alternativo de sesión vencida). Para PR 0010, completar
  `backend/.env` con `MAIL_USERNAME`, `MAIL_PASSWORD` (*app password* de Gmail) y
  `MAIL_SUPPRESS_SEND=false`, mandar una invitación a un correo propio y verificar que llega con
  el enlace a `/register` y que el enlace abre el registro.
- [ ] *(Opcional)* **Avisarle al grupo de la renumeración de códigos de caso de uso** (CU0005
  Buscar usuarios → CU0018, CU0007 Comentar publicación → CU0014, y los demás de
  [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) §3), por si usan sus
  copias fuera de este repositorio.

La base local `instance/umbook.db` no requiere ninguna acción: `python run.py` aplica las migraciones y agrega las tablas `users` e `invitations`; las tablas viejas de amistad quedan sin usar.

## Resuelto

- [x] **Implementación** en `4. Implementacion/codigo/`: el código de la compañera con 10
  correcciones de seguridad (clave JWT fija, depurador expuesto, credenciales en el código, TLS
  que no se activaba, cierre de sesión que no cerraba, rutas sin guard, errores con detalles
  internos, versiones vulnerables, correos duplicados por mayúsculas) y frontend portado a
  Angular 22 con tema nuevo.
- [x] **Invitaciones guardadas** con su estado (`pendiente` → `enviada` / `fallida`) y **enlace de
  registro** en el correo, para coincidir con el modelo de dominio y la ficha CU0010.
- [x] **Las cinco etapas alineadas con el código**, con sus diagramas y entregables generados.
  Los ítems que la cátedra marcó **FALTA** (diagrama de casos de uso único, listado de RNF,
  diagrama de clases de diseño) están resueltos.
- [x] **Hallazgos de diseño H6 a H11 resueltos**: token vencido en `AuthGuard`, timeout SMTP,
  registro simultáneo con el mismo correo, `AuthService` con una sola convención, dirección del
  backend en `environment.ts` y migraciones de Alembic. Ver
  [`DISEÑO_UMBook.md`](./DISEÑO_UMBook.md) §9.
- [x] **Pruebas automáticas:** 42 del backend (pytest) y 11 del frontend (Vitest), todas pasan.
  [`PRUEBAS_UMBook.md`](./PRUEBAS_UMBook.md) tiene 32 casos trazados a todas ellas.
- [x] **Material de la implementación anterior y originales reemplazados del grupo** en
  `_version_anterior/`, con su `README.md`.

## Límites declarados

No son pendientes: están anotados como límites de una demostración local, en `4. Implementacion/codigo/README.md`.

- Sin HTTPS: las credenciales viajan por HTTP local (RNF-10, "No cumplido").
- Sin límite de invitaciones por usuario.
- Corre sobre los servidores de desarrollo de Flask y de Angular.
- Las pantallas (componentes de Angular) se prueban a mano; los servicios y el guard tienen
  pruebas automáticas.
- Angular 22 en lugar de 15: Angular CLI 15 no corre con Node 24.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 2.0 | 26/11/2026 | Gestión del proyecto | Lista reescrita con el estado actual: tres pendientes (aviso a la compañera, pruebas manuales con correo real, aviso opcional al grupo), lo resuelto y los límites declarados. Las tareas de la implementación de amistad pasan a `_version_anterior/docs/` |
| 1.7 | 26/11/2026 | Gestión del proyecto | H6, H9, H10 y H11 resueltos; migraciones y pruebas del frontend |
| 1.6 | 26/11/2026 | Gestión del proyecto | H7 y H8 resueltos con sus pruebas (37) |
| 1.5 | 26/11/2026 | Gestión del proyecto | Etapas 4 y 5 realineadas; documentos técnicos viejos archivados; hallazgos H6 a H11 como pendiente |
