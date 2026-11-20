# ESPECIFICACIÓN DE CASOS DE USO — UMBook (casos implementados)

**Versión:** 1.1 · **Última modificación:** 20/11/2026 · **Etapa:** Requisitos

Fichas de los cinco casos de uso que se implementaron, con la plantilla de la cátedra. Los códigos están en [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md), que además marca dónde chocan con otras fichas del repositorio.

Cada ficha se genera también como `.docx` en `1. Requerimientos/Casos de Uso/` con `docs/generar_entregables.py`. **Si el `.docx` y este texto difieren, manda este texto** y hay que volver a generar el `.docx`.

## Convenciones

| Código | Significa |
|---|---|
| `ca n.m` | Curso alternativo `m` del paso `n` del curso normal |
| `rnf n.m` | Requisito no funcional `m` del caso de uso `n` (el número `n` es el del caso de uso dentro de este documento) |
| `Ob n.m` | Observación `m` del caso de uso `n` |
| `RNF-xx` | Requisito del listado general (`REQUISITOS_NO_FUNCIONALES_UMBook.md`) |

Actores: **Visitante** es quien no tiene sesión iniciada; **Usuario** es quien tiene la sesión iniciada. El sistema no distingue otros roles.

---

# PAQUETE: GESTIÓN DE USUARIOS

## CU0001 — Iniciar Sesión

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0001 |
| Paquete | Gestión de Usuarios |
| Nombre | Iniciar Sesión |
| Versión | 1.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez |
| Descripción | Permite a una persona registrada acceder a la aplicación con su correo y su contraseña. |
| Actores | Visitante registrado. |
| Frecuencia | Alta: una vez por cada ingreso a la aplicación. |
| Observaciones | Ver Ob 1.1 a 1.4. |

### Curso normal

**Precondición:** la persona ya está registrada (CU0006) y no tiene sesión iniciada.

| Nº | Paso |
|---|---|
| 1 | El Visitante ingresa a la pantalla de inicio de sesión. |
| 2 | El sistema muestra el formulario con los campos correo y contraseña. |
| 3 | El Visitante completa ambos campos y selecciona "Ingresar". |
| 4 | El sistema valida que ambos campos estén completos y que el correo tenga formato válido. |
| 5 | El sistema busca al usuario por su correo y verifica la contraseña contra la clave guardada. |
| 6 | El sistema genera un token de sesión y lo entrega junto con el nombre del usuario. |
| 7 | El sistema guarda el token en el navegador y lleva al Usuario a la pantalla principal. |
| 8 | FIN CASO DE USO |

### Cursos alternativos

**ca 4.1 — Campos vacíos o con formato inválido**

| Nº | Paso |
|---|---|
| 4.1.1 | Falta el correo o la contraseña, o el correo no tiene formato válido. |
| 4.1.2 | El sistema informa "Por favor complete todos los campos correctamente." y no consulta credenciales. |
| 4.1.3 | El caso de uso continúa en el paso 3 del curso normal. |

**ca 5.1 — Credenciales incorrectas**

| Nº | Paso |
|---|---|
| 5.1.1 | El correo no corresponde a ningún usuario, o la contraseña no coincide. |
| 5.1.2 | El sistema informa "Credenciales incorrectas.", con el mismo mensaje para los dos casos, y no genera token. |
| 5.1.3 | El caso de uso continúa en el paso 3 del curso normal. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 1.1 | Clave con hash | La contraseña se compara contra un hash con salt. Nunca se guarda ni se registra en texto plano. Deriva de RNF-08. |
| rnf 1.2 | Mensaje único | El error no distingue entre correo inexistente y contraseña incorrecta, para no revelar qué correos existen. Deriva de RNF-13. |
| rnf 1.3 | Verificar antes de decidir | La contraseña se verifica antes de elegir entre éxito y error; no existe un camino de éxito que no haya pasado por esa verificación. Deriva de RNF-08. |
| rnf 1.4 | Validación en el servidor | El formato de los datos se valida también en el servidor, no solo en la interfaz. Deriva de RNF-14. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 1.1 | Cuando una petición que **llevaba token** recibe 401 (vencido) o 422 (corrupto), la interfaz cierra la sesión y redirige a la pantalla de inicio de sesión. Si no hay token guardado, el interceptor no interviene. |
| Ob 1.2 | El diagrama de secuencia original del grupo evaluaba la contraseña dentro de la rama de éxito, lo que permitía entrar con cualquier correo existente. La implementación lo corrige (ver `docs/construccion.md` §1). |
| Ob 1.3 | No hay bloqueo por intentos fallidos. |
| Ob 1.4 | "Cerrar sesión" no es un caso de uso aparte: el botón de la pantalla principal borra el token del navegador. |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0001 - Iniciar Sesión | Diagrama de secuencia | `3. Diseño/Diagramas de Secuencia/` |
| CU0001 - Iniciar Sesión | Diagrama de colaboración | `2. Análisis/Diagramas de Colaboración/` |

---

## CU0006 — Registrar Usuario

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0006 ⚠️ choca con `CU0006.docx` (plantilla vacía). Ver catálogo, choque (1). |
| Paquete | Gestión de Usuarios |
| Nombre | Registrar Usuario |
| Versión | 1.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez |
| Descripción | Permite a una persona crear una cuenta con su nombre, su correo y una contraseña. |
| Actores | Visitante. |
| Frecuencia | Una vez por persona. |
| Observaciones | Ver Ob 2.1 y 2.2. |

### Curso normal

**Precondición:** no tener sesión iniciada.

| Nº | Paso |
|---|---|
| 1 | El Visitante ingresa a la pantalla de registro. |
| 2 | El sistema muestra el formulario con nombre, correo y contraseña. |
| 3 | El Visitante completa los tres campos y selecciona "Registrarse". |
| 4 | El sistema valida los datos: nombre de 1 a 120 caracteres, correo con formato válido y contraseña de al menos 8 caracteres. |
| 5 | El sistema verifica que el correo no esté registrado. |
| 6 | El sistema guarda el usuario con la contraseña cifrada. |
| 7 | El sistema informa "Cuenta creada con éxito. Ya podés iniciar sesión." y lleva al Visitante a la pantalla de inicio de sesión (CU0001). |
| 8 | FIN CASO DE USO |

### Cursos alternativos

**ca 4.1 — Campos faltantes o inválidos**

| Nº | Paso |
|---|---|
| 4.1.1 | Falta algún campo, el correo no es válido o la contraseña tiene menos de 8 caracteres. |
| 4.1.2 | El sistema informa "Por favor complete todos los campos correctamente." y no guarda nada. |
| 4.1.3 | El caso de uso continúa en el paso 3 del curso normal. |

**ca 5.1 — Correo ya registrado**

| Nº | Paso |
|---|---|
| 5.1.1 | Ya existe un usuario con ese correo. |
| 5.1.2 | El sistema informa "Este correo ya está registrado." y no guarda nada. |
| 5.1.3 | El caso de uso continúa en el paso 3 del curso normal. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 2.1 | Clave con hash | La contraseña se guarda con hash y salt. Deriva de RNF-08. |
| rnf 2.2 | Correo único | El correo es único en el sistema; lo garantiza una restricción de la base de datos, además de la verificación del paso 5. Deriva de RNF-15. |
| rnf 2.3 | Validación en el servidor | Los datos se validan en el servidor, no solo en la interfaz. Deriva de RNF-14. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 2.1 | El registro no inicia la sesión automáticamente: lleva a la pantalla de inicio de sesión. |
| Ob 2.2 | No hay confirmación del correo ni reglas de complejidad de la contraseña más allá del largo mínimo. |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0006 - Registrar Usuario | Diagrama de secuencia | `3. Diseño/Diagramas de Secuencia/` |
| CU0006 - Registrar Usuario | Diagrama de colaboración | `2. Análisis/Diagramas de Colaboración/` |

---

# PAQUETE: GESTIÓN DE AMISTAD

## CU0011 — Solicitar Amistad

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0011 ⚠️ choca con otras dos fichas. Ver catálogo, choque (2). |
| Paquete | Gestión de Amistad |
| Nombre | Solicitar Amistad |
| Versión | 1.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez |
| Descripción | Permite a un Usuario enviar una solicitud de amistad a otro, indicando su correo. La solicitud queda pendiente hasta que el receptor la responda (CU0012). |
| Actores | Usuario. |
| Frecuencia | Media. |
| Observaciones | Ver Ob 3.1 a 3.3. |

### Curso normal

**Precondición:** el Usuario tiene la sesión iniciada (CU0001).

| Nº | Paso |
|---|---|
| 1 | El Usuario ve en su pantalla principal el bloque "Solicitar amistad". |
| 2 | El Usuario escribe el correo de la persona y selecciona enviar. |
| 3 | El sistema valida que el correo no esté vacío y tenga formato válido. |
| 4 | El sistema verifica que exista un usuario con ese correo. |
| 5 | El sistema verifica que el receptor no sea el propio Usuario, que no sean ya amigos y que no haya una solicitud pendiente entre ambos. |
| 6 | El sistema crea la solicitud en estado "pendiente". |
| 7 | El sistema avisa al receptor de la solicitud recibida (CU0013). |
| 8 | El sistema informa "Solicitud enviada." y vacía el campo. |
| 9 | FIN CASO DE USO |

### Cursos alternativos

**ca 3.1 — Correo vacío o inválido**

| Nº | Paso |
|---|---|
| 3.1.1 | El campo está vacío o el correo no tiene formato válido. |
| 3.1.2 | El sistema informa "Por favor complete todos los campos correctamente." y no crea nada. |
| 3.1.3 | El caso de uso continúa en el paso 2 del curso normal. |

**ca 4.1 — El destinatario no existe**

| Nº | Paso |
|---|---|
| 4.1.1 | No hay ningún usuario con ese correo. |
| 4.1.2 | El sistema informa "No existe un usuario con ese email." |
| 4.1.3 | El caso de uso continúa en el paso 2 del curso normal. |

**ca 5.1 — Solicitud a uno mismo**

| Nº | Paso |
|---|---|
| 5.1.1 | El correo es el del propio Usuario. |
| 5.1.2 | El sistema informa "No podés enviarte una solicitud a vos mismo." y no crea nada. |
| 5.1.3 | El caso de uso continúa en el paso 2 del curso normal. |

**ca 5.2 — Ya son amigos**

| Nº | Paso |
|---|---|
| 5.2.1 | Entre ambos ya existe una amistad confirmada. |
| 5.2.2 | El sistema informa "Ya son amigos." y no crea nada. |
| 5.2.3 | El caso de uso continúa en el paso 2 del curso normal. |

**ca 5.3 — Solicitud pendiente duplicada**

| Nº | Paso |
|---|---|
| 5.3.1 | El Usuario ya envió a esa persona una solicitud que sigue pendiente. |
| 5.3.2 | El sistema informa "Ya existe una solicitud pendiente para este usuario." y no crea nada. |
| 5.3.3 | El caso de uso continúa en el paso 2 del curso normal. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 3.1 | Sesión obligatoria | La operación exige un token de sesión válido; sin él, el servidor responde 401. Deriva de RNF-16. |
| rnf 3.2 | Estados de la solicitud | La solicitud se modela con el patrón State: pendiente, aceptada y rechazada. Deriva de RNF-17. |
| rnf 3.3 | Aviso desacoplado | El servicio de amistad no llama al notificador: publica un evento y quien esté suscripto reacciona (patrón Observer). Deriva de RNF-17. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 3.1 | El destinatario se identifica por su **correo exacto**. En la aplicación no hay búsqueda de usuarios (CU0005 es un caso de otra persona del grupo que no se implementó). El procedimiento de prueba de CU0011 parte de "Buscar usuarios" y debe ajustarse. |
| Ob 3.2 | ⚠️ **Defecto conocido:** si el receptor *rechazó* una solicitud, volver a solicitarle amistad falla con un error 500, porque la base tiene una restricción única sobre el par emisor-receptor y la validación del paso 5 solo mira las pendientes. Está anotado en `docs/tareas.md`. |
| Ob 3.3 | La solicitud no tiene vencimiento. |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0011 - Solicitar Amistad | Diagrama de secuencia | `3. Diseño/Diagramas de Secuencia/` |
| CU0011 - Solicitar Amistad | Diagrama de colaboración | `2. Análisis/Diagramas de Colaboración/` |
| Diagrama de Estados - SolicitudAmistad | Diagrama de estados | `3. Diseño/Diagramas de Estado/` |

---

## CU0012 — Aceptar / Rechazar Solicitud de Amistad

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0012 ⚠️ choca con otras dos fichas y duplica a `CU0002.docx`. Ver catálogo, choque (3). |
| Paquete | Gestión de Amistad |
| Nombre | Aceptar / Rechazar Solicitud de Amistad |
| Versión | 1.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez |
| Descripción | Permite al receptor de una solicitud pendiente aceptarla, con lo que se crea la amistad, o rechazarla. |
| Actores | Usuario (receptor de la solicitud). |
| Frecuencia | Media. |
| Observaciones | Ver Ob 4.1 a 4.3. |

### Curso normal

**Precondición:** el Usuario tiene la sesión iniciada (CU0001) y tiene al menos una solicitud pendiente recibida (CU0011).

| Nº | Paso |
|---|---|
| 1 | El sistema muestra en la pantalla principal las solicitudes de amistad pendientes recibidas, con el nombre de quien la envió. |
| 2 | El Usuario selecciona "Aceptar" en una solicitud. |
| 3 | El sistema verifica que la solicitud exista y que el Usuario sea su receptor. |
| 4 | El sistema pasa la solicitud al estado "aceptada" y crea el vínculo de amistad entre ambos, en una sola operación. |
| 5 | El sistema quita la solicitud de la lista de pendientes y muestra a la otra persona entre los amigos del Usuario. |
| 6 | FIN CASO DE USO |

### Cursos alternativos

**ca 2.1 — Rechazar la solicitud**

| Nº | Paso |
|---|---|
| 2.1.1 | El Usuario selecciona "Rechazar". |
| 2.1.2 | El sistema pasa la solicitud al estado "rechazada" y no crea ninguna amistad. |
| 2.1.3 | El caso de uso continúa en el paso 5 del curso normal, sin el alta en la lista de amigos. |

**ca 3.1 — La solicitud no existe**

| Nº | Paso |
|---|---|
| 3.1.1 | No existe una solicitud con ese identificador. |
| 3.1.2 | El sistema informa "La solicitud no existe." y no cambia nada. |

**ca 3.2 — El Usuario no es el receptor**

| Nº | Paso |
|---|---|
| 3.2.1 | La solicitud pertenece a otra persona. |
| 3.2.2 | El sistema informa "Esta solicitud no te pertenece." y no cambia nada. |

**ca 4.1 — La solicitud ya fue respondida**

| Nº | Paso |
|---|---|
| 4.1.1 | La solicitud ya está aceptada o rechazada. |
| 4.1.2 | El sistema rechaza la transición e informa el error; el estado no cambia. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 4.1 | Transacción única | El cambio de estado y la creación de la amistad se confirman juntos. Si una de las dos falla, no queda nada guardado. Deriva de RNF-12. |
| rnf 4.2 | Autorización en el servidor | Solo el receptor puede responder. Se verifica en el servidor; ocultar el botón en la interfaz no alcanza. Deriva de RNF-10. |
| rnf 4.3 | Estados terminales | Una solicitud aceptada o rechazada no admite ninguna transición nueva. Deriva de RNF-17. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 4.1 | La notificación en la aplicación **es** la lista de solicitudes pendientes: no existe una entidad "Notificación" propia. |
| Ob 4.2 | El procedimiento de prueba de CU0012 describe un aviso por correo con un enlace y su vencimiento. El correo implementado **no incluye enlace**: pide iniciar sesión en la aplicación. El procedimiento debe ajustarse. |
| Ob 4.3 | No hay forma de deshacer una amistad (eliminar amigos es CU0012 de otra persona del grupo, no implementado). |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0012 - Aceptar - Rechazar Solicitud | Diagrama de secuencia | `3. Diseño/Diagramas de Secuencia/` |
| CU0012 - Aceptar - Rechazar Solicitud | Diagrama de colaboración | `2. Análisis/Diagramas de Colaboración/` |
| Diagrama de Estados - SolicitudAmistad | Diagrama de estados | `3. Diseño/Diagramas de Estado/` |

---

# PAQUETE: NOTIFICACIONES

## CU0013 — Notificar Solicitud de Amistad Recibida

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0013 ⚠️ también se usa para "amigos en común" en `UMBook_RNF`. Ver catálogo, choque (4). |
| Paquete | Notificaciones |
| Nombre | Notificar Solicitud de Amistad Recibida |
| Versión | 1.0 |
| Prioridad | Media |
| Confeccionó | Victor Gimenez |
| Descripción | Cuando se crea una solicitud de amistad, el sistema avisa al receptor por correo electrónico. En la aplicación, el aviso es la lista de solicitudes pendientes de su pantalla principal. |
| Actores | Sistema (se dispara desde CU0011). Receptor del aviso: Usuario. |
| Frecuencia | Una vez por cada solicitud creada. |
| Observaciones | Ver Ob 5.1 a 5.3. |

### Curso normal

**Precondición:** se creó una solicitud de amistad (CU0011, paso 6).

| Nº | Paso |
|---|---|
| 1 | El sistema publica un evento "solicitud recibida" en el usuario receptor, con su correo y el nombre de quien envió la solicitud. |
| 2 | El notificador, suscripto como observador de todo usuario, recibe el evento. |
| 3 | El sistema arma el correo con la plantilla de solicitud recibida, en versión HTML y en texto plano. |
| 4 | El sistema envía el correo al receptor por el servidor de correo configurado. |
| 5 | Al iniciar sesión, el receptor ve la solicitud en la lista de pendientes de su pantalla principal (CU0012, paso 1). |
| 6 | FIN CASO DE USO |

### Cursos alternativos

**ca 4.1 — El envío del correo está desactivado**

| Nº | Paso |
|---|---|
| 4.1.1 | La configuración tiene `MAIL_SUPPRESS_SEND=true`. |
| 4.1.2 | El sistema simula el envío y no manda ningún correo. La solicitud y la lista de pendientes no se ven afectadas. |

**ca 5.1 — No hay solicitudes pendientes**

| Nº | Paso |
|---|---|
| 5.1.1 | El receptor no tiene solicitudes en estado "pendiente". |
| 5.1.2 | El sistema **mantiene visible** la sección "Solicitudes de amistad recibidas" y muestra el mensaje "No tenés solicitudes pendientes. Cuando alguien te agregue, te va a aparecer acá y te llega un mail." |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 5.1 | Notificador único | El notificador es un Singleton: existe una sola instancia, creada con doble verificación y candado. Deriva de RNF-17. |
| rnf 5.2 | Desacoplamiento | Quien crea la solicitud no conoce al notificador; solo publica el evento. Deriva de RNF-17. |
| rnf 5.3 | Credenciales fuera del código | Las credenciales del servidor de correo se leen del archivo `.env`, que no se versiona. Deriva de RNF-18. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 5.1 | El correo no tiene enlace de aceptación: indica iniciar sesión y responder desde la pantalla principal. Si se agregara un enlace, necesita un token propio, de un solo uso y con vencimiento, no el token de sesión. |
| Ob 5.2 | El envío del correo es **síncrono**, dentro de la misma petición que crea la solicitud. Si el servidor de correo falla, la petición falla. |
| Ob 5.3 | `NotificationService` conserva `enviar_email` y `notificar`, que venían del caso de invitaciones (no implementado). |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0013 - Notificar Solicitud Recibida | Diagrama de secuencia | `3. Diseño/Diagramas de Secuencia/` |
| CU0013 - Notificar Solicitud Recibida | Diagrama de colaboración | `2. Análisis/Diagramas de Colaboración/` |
| Diagrama de clases - Observer y Singleton | Diagrama de clases | `3. Diseño/Diagramas de Clases/` |

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Requisitos | Versión inicial: fichas de CU0001, CU0006, CU0011, CU0012 y CU0013, derivadas del código |
| 1.1 | 20/11/2026 | Requisitos | Se verifica contra el frontend: CU0013 agrega ca 5.1 (la sección de pendientes no se oculta, muestra un mensaje de vacío) y CU0001 Ob 1.1 precisa que el interceptor solo actúa si la petición llevaba token |
