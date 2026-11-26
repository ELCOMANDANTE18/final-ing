# LISTA DE REQUISITOS NO FUNCIONALES — UMBook

**Versión:** 3.0 · **Última modificación:** 25/11/2026 · **Etapa:** Requerimientos

Listado de los requisitos no funcionales de UMBook, **con código**, para que las fichas de caso de uso puedan citarlos. Responde al ítem "Listado de requerimientos no funcionales" que la cátedra marcó FALTA.

- **RNF-01 a RNF-17** salen del documento del grupo `Requisitos No Funcionales.docx` (está en la misma carpeta), que los describe en prosa. Acá se separan uno por uno y se les asigna un código; el texto se conserva.
- **RNF-18 a RNF-25** salen de las fichas de los casos de uso implementados (CU0001, CU0006 y CU0010) y del código.

La columna **Estado** refleja la revisión contra el código de `4. Implementacion/codigo/` a la fecha de este documento. La columna **Verificación** dice con qué se comprueba: una prueba automática de `backend/tests/` o una revisión.

| Estado | Significado |
|---|---|
| Cumplido | Implementado y verificado |
| Parcial | Se cumple solo para el alcance de esta versión, o en parte |
| No cumplido | Aplica a esta versión pero no está implementado |
| Fuera de alcance | Depende de un caso de uso que no se implementó |

---

## 1. Rendimiento

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-01 | **Capacidad concurrente.** El sistema debe soportar al menos 1000 usuarios conectados al mismo tiempo sin fallos ni degradación significativa. | **No cumplido.** La versión corre sobre el servidor de desarrollo de Flask y SQLite, pensados para la demostración. Requiere un servidor de producción. | — |
| RNF-02 | **Tiempo de respuesta.** Las acciones más frecuentes deben completarse en un máximo de 3 segundos en condiciones normales. | **Parcial.** No hay una medición formal de los tiempos de respuesta. El envío de la invitación depende del servidor de correo (ver rnf 2.2 de CU0010: 5 segundos). | Revisión manual |
| RNF-03 | **Carga de imágenes.** Las fotos de hasta 5 MB deben subirse y previsualizarse en menos de 5 segundos. | **Fuera de alcance** (Gestionar álbum, CU0007). | — |
| RNF-04 | **Envío programado de notificaciones.** Una tarea diaria envía los correos de cumpleaños y notificaciones, y termina en menos de 1 hora. | **Fuera de alcance** (CU0023). | — |
| RNF-05 | **Escalabilidad del rendimiento.** El sistema debe poder ampliarse horizontalmente (más instancias de servidor) en períodos de alta demanda. | **Parcial.** El backend no guarda estado de sesión en memoria (la sesión viaja en el token), así que admite varias instancias. SQLite no: haría falta un motor cliente-servidor (RNF-16). | Revisión de diseño |

## 2. Fiabilidad

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-06 | **Disponibilidad.** Al menos 99,5 % mensual, salvo mantenimientos programados. | **No cumplido.** No se puede verificar con el servidor de desarrollo; es un requisito de la puesta en producción. | — |

## 3. Usabilidad

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-07 | **Interfaz simple.** La interfaz debe ser simple e intuitiva, usable sin capacitación, con mensajes claros de éxito y de error. | **Cumplido** para lo implementado: los mensajes son los de las fichas ("Credenciales incorrectas.", "Este correo ya está registrado.", "Invitación enviada."). | Revisión manual de las pantallas |
| RNF-08 | **Funciones a pocos pasos.** Las funciones principales deben estar en la pantalla principal y no requerir más de dos o tres pasos. | **Cumplido** para lo implementado: invitar está en la pantalla principal (un clic, completar el correo, enviar). | Revisión manual |

## 4. Seguridad

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-09 | **Contraseñas cifradas.** Las contraseñas se guardan con hash y salt, nunca en texto plano, y se verifican antes de decidir si el acceso es válido. | **Cumplido.** Werkzeug (`generate_password_hash` / `check_password_hash`). | `test_la_clave_se_guarda_con_hash_y_no_en_claro`, `test_login_con_clave_incorrecta_devuelve_401` |
| RNF-10 | **Conexión HTTPS.** Las credenciales viajan únicamente por conexiones HTTPS. | **No cumplido.** La versión corre en local por HTTP. Queda para la puesta en producción (detrás de un servidor con certificado). El correo saliente sí va cifrado (SMTP con TLS). | `test_mail_use_tls_acepta_true_en_minuscula` (solo TLS del correo) |
| RNF-11 | **Permisos sobre el contenido propio.** Cada usuario gestiona quién ve sus álbumes, muro y comentarios, y el sistema hace cumplir esas restricciones. | **Fuera de alcance** (CU0017). | — |
| RNF-12 | **Acciones administrativas visibles.** Las acciones administrativas, como eliminar un comentario impropio, quedan registradas con un mensaje visible. | **Fuera de alcance** (CU0003). | — |

## 5. Mantenibilidad, escalabilidad y portabilidad

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-13 | **Módulos bien definidos.** La arquitectura se organiza en módulos que permiten corregir o agregar funciones sin afectar al resto. | **Cumplido.** Capas controller → service → DAO → modelo; un Blueprint por área (`auth`, `invite`). | Revisión de diseño |
| RNF-14 | **Crecimiento de datos.** Ante más usuarios o datos, se agregan recursos (servidores, base de datos) sin rediseñar el sistema. | **Parcial.** El acceso a datos pasa por SQLAlchemy y los DAO: cambiar de motor es cambiar `SQLALCHEMY_DATABASE_URI`. | Revisión de diseño |
| RNF-15 | **Portabilidad.** Accesible desde los navegadores principales (Chrome, Firefox, Edge, Safari), en escritorio y en móvil, sin aplicación nativa. | **Parcial.** SPA Angular, sin instalación. No se verificó en todos los navegadores ni en móvil. | Revisión manual |

## 6. Restricciones técnicas

| ID | Requisito | Estado | Verificación |
|---|---|---|---|
| RNF-16 | **Tecnologías y base de datos.** Backend en Java, Node.js o Python; frontend en HTML, CSS y JavaScript con un framework (React o Angular); base de datos relacional (por ejemplo PostgreSQL o MySQL). | **Cumplido** en el lenguaje y el framework: Python 3 con Flask 3.0 y Angular 22. **Parcial** en la base: SQLite, que es relacional pero de un solo archivo; pasar a PostgreSQL o MySQL no cambia el código (RNF-14). | `requirements.txt`, `package.json` |
| RNF-17 | **Servidor de correo.** El sistema se integra con un servidor de correo para el envío automático de notificaciones. | **Cumplido.** Flask-Mail por SMTP (Gmail, puerto 587, TLS). Lo usa CU0010. | `test_invitacion_exitosa_envia_un_correo_al_invitado` |

## 7. Requisitos de los casos de uso implementados

| ID | Categoría | Requisito | Estado | Verificación |
|---|---|---|---|---|
| RNF-18 | Seguridad | **Mensaje único de error de acceso.** El inicio de sesión responde lo mismo si el correo no existe o si la contraseña no coincide, para no revelar qué correos están registrados. | **Cumplido.** | `test_correo_inexistente_y_clave_incorrecta_dan_el_mismo_mensaje` |
| RNF-19 | Seguridad | **Validación en el servidor.** Los datos de entrada se validan en el servidor, no solo en la interfaz (formato de correo, largo de nombre y contraseña, correo de hasta 254 caracteres). | **Cumplido.** Esquemas de marshmallow. | `test_clave_corta_devuelve_400_y_no_crea_el_usuario`, `test_registro_con_campos_faltantes_devuelve_400`, `test_login_con_campos_vacios_devuelve_400`, `test_correo_invalido_devuelve_400_y_no_envia_nada`, `test_correo_de_mas_de_254_caracteres_devuelve_400` |
| RNF-20 | Seguridad | **Sesión con token.** La sesión se mantiene con un token JWT firmado y con vencimiento. Las operaciones privadas lo exigen; un token ausente, vencido o inválido se rechaza con 401 y la interfaz cierra la sesión. | **Cumplido.** `@token_required` en el backend; `AuthGuard` e interceptor en el frontend. | `test_invitar_sin_token_devuelve_401`, `test_token_vencido_devuelve_401`, `test_token_invalido_devuelve_401_sin_detalles`, `test_token_de_un_usuario_que_ya_no_existe_devuelve_401` |
| RNF-21 | Seguridad | **Secretos fuera del código.** La clave de firma y las credenciales del correo se leen de variables de entorno (`.env`), que no se versionan. La aplicación no arranca sin una clave segura, y el depurador no se expone en la red. | **Cumplido.** | `test_la_aplicacion_no_arranca_sin_una_clave_jwt_segura`, `test_un_token_firmado_con_la_clave_vieja_super_secret_no_sirve`, `test_run_no_expone_el_depurador_en_la_red` |
| RNF-22 | Seguridad | **Errores sin detalles internos.** Al cliente se le devuelve un mensaje genérico; el detalle técnico queda solo en el log del servidor. | **Cumplido.** | `test_falla_del_correo_responde_500_sin_detalles_internos`, `test_token_invalido_devuelve_401_sin_detalles` |
| RNF-23 | Integridad | **Correo único.** Cada correo pertenece a una sola cuenta, sin distinguir mayúsculas; lo garantiza también una restricción de la base de datos. | **Cumplido.** | `test_correo_ya_registrado_devuelve_409`, `test_el_correo_no_distingue_mayusculas` |
| RNF-24 | Tolerancia a fallos | **Fallo del correo registrado.** Si falla el envío de un correo, se registra (la invitación queda `fallida`), se le avisa al usuario y se puede reintentar. | **Cumplido.** | `test_si_falla_el_envio_la_invitacion_queda_guardada_como_fallida`, `test_falla_del_correo_responde_500_sin_detalles_internos` |
| RNF-25 | Diseño | **Patrones de diseño.** Un solo notificador para toda la aplicación (**Singleton**) y acceso a datos por objetos DAO. | **Cumplido.** `NotificationService` (Singleton), `UserDAO` e `InvitationDAO`. | `test_notification_service_es_singleton` |

---

## 8. Trazabilidad con las fichas de caso de uso

Los requisitos de cada ficha (`rnf n.m`) son la versión concreta, para ese caso de uso, de un requisito de esta lista.

| Ficha | Requisito de la ficha | Deriva de |
|---|---|---|
| CU0001 (`CU0001_Iniciar_Sesión.docx`) | rnf 1.1 Clave con hash · rnf 1.3 Verificar antes de decidir | RNF-09 |
| | rnf 1.2 Mensaje único | RNF-18 |
| | rnf 1.4 Validación en el servidor | RNF-19 |
| | rnf 1.5 Tiempo de respuesta | RNF-02 |
| CU0006 (`CU0006.docx` y `CU0006_Registrar_Usuario.docx`) | rnf 1.1 Validación de datos | RNF-19 |
| | rnf 1.2 Confirmación visual | RNF-07 |
| | rnf 1.3 Clave con hash (solo en `CU0006_Registrar_Usuario.docx`) | RNF-09 |
| | rnf 1.4 Correo único (solo en `CU0006_Registrar_Usuario.docx`) | RNF-23 |
| CU0010 (`CU0010.docx`) | rnf 2.1 Formato de email | RNF-19 |
| | rnf 2.2 Rendimiento del envío | RNF-02, RNF-17 |
| Fichas de la implementación (`4. Implementacion/1_Casos de Uso/`) | CU0001: rnf 1.1 Seguridad (HTTPS) · rnf 1.2 Autenticación (JWT) · Tiempo de respuesta | RNF-10 · RNF-20 · RNF-02 |

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 – 2.1 | 20/11/2026 – 25/11/2026 | Requisitos | Listado de la implementación anterior (amistad y notificaciones). Archivado en `_version_anterior/docs/` |
| 3.0 | 25/11/2026 | Requerimientos | Listado nuevo: RNF-01 a RNF-17 a partir del documento del grupo, RNF-18 a RNF-25 a partir de CU0001, CU0006 y CU0010. Estado y verificación contra el código actual |
