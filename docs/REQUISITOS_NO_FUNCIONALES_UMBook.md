# LISTA DE REQUISITOS NO FUNCIONALES — UMBook

**Versión:** 2.0 · **Última modificación:** 20/11/2026 · **Etapa:** Requisitos

Requisitos adicionales (no asociados a un caso de uso particular) y los de las fichas de los casos de uso implementados. Reemplaza al listado `UMBook_RNF` anterior: **se conservan los RNF-01 a RNF-12 con su numeración**, con el estado y el stack actualizados contra el código, y se agregan RNF-13 a RNF-18.

Los requisitos específicos de cada caso de uso van en su ficha (`rnf n.m`) y **derivan** de uno de los de esta lista.

**Estado** refleja la revisión contra el repositorio a la fecha de este documento.

| Marca | Significado |
|---|---|
| Cumplido | Implementado y probado |
| Parcial | Implementado solo para el alcance de esta versión |
| Fuera de alcance | Depende de un caso de uso que no se implementó |

---

## 1. Interfaces y restricciones técnicas

| ID | Categoría | Descripción | Estado |
|---|---|---|---|
| RNF-02 | Interfaces | El sistema debe integrarse con un servicio de correo (SMTP) para avisar las solicitudes de amistad. | **Cumplido.** Flask-Mail con Gmail (587, TLS). Se probó con un correo real. |
| RNF-03 | Interfaces | La aplicación debe ser accesible desde un navegador web estándar, sin instalación en el cliente. | **Cumplido.** SPA Angular. |
| RNF-04 | Diseño físico / implementación | Backend: Python 3.14, Flask 3.0.3, Flask-SQLAlchemy 3.1.1 sobre SQLite, Flask-JWT-Extended 4.6.0, Flask-Mail 0.9.1, Flask-Cors 4.0.1 y marshmallow 3.21.3. Frontend: Angular 22 (TypeScript) por HTTP/JSON, con el token en `localStorage`. Correo saliente por SMTP. | **Cumplido.** Versiones tomadas de `requirements.txt` y `package.json`. *El listado anterior decía Python 3.11/3.12, Flask 2.3 y Angular 15.* |

## 2. Arquitectura y persistencia

| ID | Categoría | Descripción | Estado |
|---|---|---|---|
| RNF-05 | Restricciones arquitectónicas | Arquitectura en capas: controller → service → DAO → modelo. | **Cumplido.** |
| RNF-06 | Persistencia | Los datos deben persistir en una base de datos relacional. | **Parcial.** Se persisten usuarios, solicitudes de amistad y amistades. Grupos, álbumes, fotos y comentarios son de casos de uso no implementados. |
| RNF-07 | Distribución y concurrencia | El sistema debe soportar accesos concurrentes sobre el mismo recurso sin pérdida de datos. | **Parcial.** SQLite serializa las escrituras; aceptable en un entorno académico. Las restricciones únicas de la base evitan duplicados aun con pedidos simultáneos. |
| RNF-12 | Gestión de transacciones | Aceptar una solicitud de amistad (cambio de estado y creación del vínculo) debe ejecutarse de forma atómica. | **Cumplido.** Un solo `commit`, con `rollback` ante cualquier falla. |
| RNF-17 | Patrones de diseño | La solicitud de amistad se modela con el patrón **State**; el aviso de solicitud recibida, con **Observer** sobre un **Singleton**. | **Cumplido.** Probados en aislamiento. |

## 3. Seguridad

| ID | Categoría | Descripción | Estado |
|---|---|---|---|
| RNF-08 | Seguridad | Las contraseñas deben almacenarse con hash y salt, nunca en texto plano. | **Cumplido.** Werkzeug (`generate_password_hash` / `check_password_hash`). |
| RNF-10 | Seguridad | Toda operación, salvo registro e inicio de sesión, exige sesión, y se verifica en el servidor que el usuario sea el dueño del recurso que toca. | **Cumplido** para lo implementado: `@token_required` en cada endpoint, `AuthGuard` en la pantalla principal y solo el receptor puede responder una solicitud. *El control por roles y grupos de permisos es de un caso de uso no implementado.* |
| RNF-13 | Seguridad | Los errores de inicio de sesión no deben revelar qué correos existen: mismo mensaje para correo inexistente y contraseña incorrecta. | **Cumplido.** |
| RNF-14 | Seguridad | Los datos de entrada se validan en el servidor, no solo en la interfaz. | **Cumplido.** Esquemas de marshmallow. |
| RNF-16 | Seguridad | La sesión se mantiene con un token firmado y con vencimiento. Ante un token vencido (401) o corrupto (422), la interfaz cierra la sesión y vuelve al inicio de sesión. | **Cumplido.** Interceptor del frontend. Cubierto por pruebas. |
| RNF-18 | Seguridad | La clave de firma y las credenciales del servidor de correo se leen de variables de entorno (`.env`) y no se versionan. | **Cumplido.** `.env` en `.gitignore`; la plantilla es `.env.example`. |
| RNF-09 | Seguridad | El enlace de aceptación o rechazo enviado por correo debe usar un token único, no adivinable y con vencimiento. | **Fuera de alcance.** El correo implementado no trae enlace: indica iniciar sesión. Si se agregara uno, este requisito pasa a ser obligatorio. |

## 4. Integridad de datos

| ID | Categoría | Descripción | Estado |
|---|---|---|---|
| RNF-15 | Integridad | El correo de un usuario es único; la base lo garantiza con una restricción además de la validación del servicio. | **Cumplido.** |

## 5. Rendimiento y tolerancia a fallos

| ID | Categoría | Descripción | Estado |
|---|---|---|---|
| RNF-01 | Rendimiento | La consulta de "amigos en común" y las notificaciones de la pantalla principal deben resolverse en un tiempo aceptable aun con un grafo de amistades grande. | **Fuera de alcance** para "amigos en común" (caso de uso no implementado). Las notificaciones de la pantalla principal son una consulta simple por receptor y estado; no se midió su rendimiento. |
| RNF-11 | Tolerancia a fallos | Si falla el envío de un correo a un usuario, debe registrarse y no bloquear el resto. | **Fuera de alcance** para el lote de cumpleaños. *Hallazgo:* el aviso de solicitud recibida se envía en forma síncrona, así que una falla del servidor de correo hace fallar la petición que crea la solicitud (ver CU0013, Ob 5.2). |

---

## 6. Trazabilidad con las fichas

| Requisito de la ficha | Deriva de |
|---|---|
| rnf 1.1, 1.3 | RNF-08 |
| rnf 1.2 | RNF-13 |
| rnf 1.4, 2.3 | RNF-14 |
| rnf 2.1 | RNF-08 |
| rnf 2.2 | RNF-15 |
| rnf 3.1 | RNF-16 |
| rnf 3.2, 3.3, 4.3, 5.1, 5.2 | RNF-17 |
| rnf 4.1 | RNF-12 |
| rnf 4.2 | RNF-10 |
| rnf 5.3 | RNF-18 |

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 2.0 | 20/11/2026 | Requisitos | Reemplaza a `UMBook_RNF` 1.0. Se actualiza el stack y el estado de RNF-01 a RNF-12 contra el código, se agregan RNF-13 a RNF-18 y la trazabilidad con las fichas de CU. |
