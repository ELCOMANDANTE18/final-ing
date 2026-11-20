# PRUEBAS — UMBook (casos implementados)

**Versión:** 1.0 · **Última modificación:** 20/11/2026 · **Etapa:** Prueba

Plan, casos y procedimientos de prueba de los cinco casos de uso implementados (CU0001, CU0006, CU0011, CU0012 y CU0013), **alineados con el comportamiento real del sistema**. Los códigos están en [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md).

Reemplaza a los casos y procedimientos anteriores (`UMBook_Casos_de_Prueba.xlsx` y `UMBook_Procedimientos_de_Prueba.docx`), que describían un flujo especificado pero no implementado: búsqueda de usuarios, botón "Solicitar amistad" que se oculta y correo con enlace de confirmación con token. La columna **Antes** de cada caso indica de cuál viene.

## Convenciones

| Marca | Significado |
|---|---|
| **Auto** | Está cubierto por una prueba automática de `backend/tests/` (se corre con `python -m pytest`) |
| **Manual** | Se verifica a mano en el navegador, con el backend en `:5000` y el frontend en `:4200` |
| **Falla conocida** | El sistema hoy no cumple el resultado esperado; está anotado como defecto |

Datos de prueba: usuarios creados desde la pantalla de registro o con `python seed.py`. Para probar sin enviar correo real, poner `MAIL_SUPPRESS_SEND=true` en `.env`.

---

## 0. Plan de pruebas

### Introducción

Este plan describe cómo se prueba UMBook, la red social de gestión de usuarios (materia Ingeniería de Software). **El alcance son los cinco casos de uso implementados**: CU0001, CU0006, CU0011, CU0012 y CU0013. Los demás casos de uso del grupo no se implementaron y no se prueban.

El sistema se prueba a nivel de **integración y de sistema** (automático) y de **aceptación** (manual, desde el navegador).

### Elementos incluidos en las pruebas

- Gestión de Usuarios (registro e inicio de sesión)
- Gestión de Amistad (solicitudes y amistades)
- Notificaciones (correo de solicitud recibida)
- Control de accesos (token, rutas protegidas y autorización del receptor)

### Funcionalidades a probar

| Subsistema | Funcionalidad | Casos de prueba |
|---|---|---|
| Gestión de Usuarios | Iniciar Sesión (CU0001) | CP 0001.1 a CP 0001.7 |
| Gestión de Usuarios | Registrar Usuario (CU0006) | CP 0006.1 a CP 0006.4 |
| Gestión de Amistad | Solicitar Amistad (CU0011) | CP 0011.1 a CP 0011.7 |
| Gestión de Amistad | Aceptar / Rechazar Solicitud (CU0012) | CP 0012.1 a CP 0012.7 |
| Notificaciones | Notificar Solicitud Recibida (CU0013) | CP 0013.1 a CP 0013.6 |

### Estrategia de prueba

| Nivel | Qué se prueba | Cómo |
|---|---|---|
| Unidad | El patrón State aislado y las reglas del dominio | pytest, sin base de datos ni Flask |
| Integración | Los servicios con base de datos real; Observer y Singleton | pytest, con una base SQLite temporal por prueba |
| Sistema | La API completa, con códigos de estado y autorización | Cliente de pruebas de Flask, dentro de pytest |
| Aceptación | Las pantallas: mensajes, redirecciones y contadores | Manual, siguiendo los procedimientos de la sección 2 |

### Herramientas

| Herramienta | Para qué |
|---|---|
| pytest 8.3.3 | Pruebas automáticas del backend (`python -m pytest`, 32 pruebas) |
| Cliente de pruebas de Flask | Pedidos HTTP sin levantar el servidor |
| Navegador web actual | Pruebas manuales de las pantallas |
| `MAIL_SUPPRESS_SEND` | Apaga el envío real de correo en las pruebas automáticas |

No hay pruebas automáticas del frontend.

### Criterios de éxito

La prueba se completa cuando se ejecutaron todos los casos definidos, pasan las 32 pruebas automáticas y no quedan defectos bloqueantes, críticos ni mayores sin resolver. **Defecto abierto:** el reenvío de una solicitud tras un rechazo (CP 0011.7, H1) está sin resolver y se clasifica como mayor.

### Entregables

- Este documento (plan, casos y procedimientos), con su versión en `5. Pruebas/`.
- El resultado de `python -m pytest` de cada ciclo.
- El reporte de defectos e incidencias, que hoy es la lista de pendientes de `docs/tareas.md`.

### Ambiente de prueba

| Elemento | Detalle |
|---|---|
| Sistema operativo | Linux |
| Backend | Python 3.14 con las dependencias de `requirements-dev.txt` |
| Frontend | Node.js y Angular CLI 22 (`ng serve`, puerto 4200) |
| Base de datos | SQLite (temporal en las pruebas automáticas; `instance/umbook.db` en las manuales) |
| Correo | Cuenta de Gmail con *app password* para CP 0013.1; apagado en el resto |
| Navegador | Un navegador web de escritorio actual |

---

## 1. Casos de prueba

### CU0001 — Iniciar Sesión

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0001.1 | Inicio de sesión exitoso | Usuario registrado, sin sesión | Correo y contraseña correctos | Se genera el token y se redirige a la pantalla principal | Auto (`test_login_correcto_devuelve_token`) y Manual | CP 1.1 |
| CP 0001.2 | Una contraseña incorrecta no autentica | Usuario registrado, sin sesión | Correo correcto, contraseña incorrecta | "Credenciales incorrectas.", sin token y sin redirección | Auto (`test_login_con_password_incorrecto_devuelve_401`) y Manual | CP 1.2 |
| CP 0001.3 | Campos vacíos | Sin sesión | Correo y contraseña vacíos | "Por favor complete todos los campos correctamente." sin llamar al servidor | Manual | CP 1.3 |
| CP 0001.4 | Un correo inexistente da el mismo mensaje | Sin sesión | Correo no registrado | "Credenciales incorrectas." (idéntico al de CP 0001.2) | Auto (`test_auth_service.py`) y Manual | — |
| CP 0001.5 | Una ruta protegida exige sesión | Sin sesión | Abrir `/welcome` | Se redirige a `/login` | Manual | — |
| CP 0001.6 | Un endpoint protegido rechaza pedidos sin token | Sin sesión | `GET /amistad/solicitudes/pendientes` sin token | 401 | Auto (`test_endpoints_de_amistad_requieren_token`) | — |
| CP 0001.7 | Un token vencido da 401 y uno corrupto da 422 | — | Token vencido; token `esto-no-es-un-jwt` | 401 y 422; la interfaz cierra la sesión y vuelve a `/login` | Auto (`test_token_vencido_devuelve_401`, `test_token_corrupto_devuelve_422`) | — |

### CU0006 — Registrar Usuario

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0006.1 | Registro exitoso | Correo no registrado | Nombre, correo nuevo, contraseña de 8 o más caracteres | "Cuenta creada con éxito. Ya podés iniciar sesión." y redirección a `/login` tras un instante; no se inicia sesión | Manual | — |
| CP 0006.2 | Correo ya registrado | Correo existente | El mismo correo | "Este correo ya está registrado." (409) | Auto (`test_registro_duplicado_devuelve_409`) y Manual | — |
| CP 0006.3 | Contraseña corta | — | Contraseña de menos de 8 caracteres | "Por favor complete todos los campos correctamente." (400) y no se guarda nada | Manual | — |
| CP 0006.4 | Campos vacíos | — | Algún campo vacío | El mismo mensaje, sin llamar al servidor | Manual | — |

### CU0011 — Solicitar Amistad

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0011.1 | Solicitud exitosa | Sin amistad ni solicitud previa entre Ana y Beto | Ana envía a `beto@…` | "Solicitud enviada.", el campo se vacía y la solicitud queda "pendiente" | Auto (`test_solicitar_amistad_crea_solicitud_pendiente…`, `test_flujo_completo_de_amistad_por_http`) y Manual | CP SA.1 |
| CP 0011.2 | No se duplica una solicitud pendiente | Se ejecutó CP 0011.1 | Ana envía de nuevo a Beto | Error "Ya existe una solicitud pendiente para este usuario." (409). **No se oculta ningún botón** | Auto (`test_no_se_puede_duplicar_una_solicitud_pendiente`) y Manual | CP SA.2 (corregido) |
| CP 0011.3 | No se puede solicitar a uno mismo | Ana con sesión | El correo de Ana | "No podés enviarte una solicitud a vos mismo." | Auto (`test_no_se_puede_solicitar_amistad_a_uno_mismo`) | — |
| CP 0011.4 | Destinatario inexistente | Ana con sesión | Correo no registrado | "No existe un usuario con ese email." (404) | Auto (`test_solicitud_a_email_inexistente_devuelve_404`) | — |
| CP 0011.5 | No se solicita a un amigo | Ana y Beto ya son amigos | Ana envía a Beto | "Ya son amigos." (409) | Auto (`test_no_se_puede_solicitar_amistad_a_alguien_que_ya_es_amigo`) | — |
| CP 0011.6 | Correo vacío o inválido | Ana con sesión | Campo vacío | "Por favor complete todos los campos correctamente." | Manual | — |
| CP 0011.7 | Volver a solicitar a quien rechazó | Beto rechazó la solicitud de Ana | Ana envía de nuevo a Beto | **Esperado:** un aviso claro (409) o que se reabra la solicitud. **Hoy:** error 500 | **Falla conocida** (H1, ver `DISEÑO_UMBook.md` §9) | — |

### CU0012 — Aceptar / Rechazar Solicitud de Amistad

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0012.1 | El receptor ve la solicitud recibida | Se ejecutó CP 0011.1 | Beto inicia sesión | La pantalla principal lista la solicitud de Ana como "pendiente", con "Aceptar" y "Rechazar" | Auto (`test_flujo_completo_de_amistad_por_http`) y Manual | CP AR.1 |
| CP 0012.2 | Aceptar crea la amistad | Se ejecutó CP 0012.1 | Beto selecciona "Aceptar" | La solicitud sale de los pendientes y cada uno ve al otro en "Tus amigos" | Auto (`test_aceptar_solicitud_crea_amistad_en_la_misma_transaccion`, `test_amigos_de_devuelve_solo_amistades_confirmadas`) y Manual | CP AR.2 |
| CP 0012.3 | Rechazar no crea amistad | Se ejecutó CP 0012.1 | Beto selecciona "Rechazar" | La solicitud sale de los pendientes y no se crea ninguna amistad | Manual | CP AR.2.1 |
| CP 0012.4 | El estado cambia en una sola operación | Se ejecutó CP 0012.2 o CP 0012.3 | — | El estado queda "aceptada" o "rechazada"; si se acepta, el vínculo existe | Auto (`test_aceptar_solicitud_crea_amistad_en_la_misma_transaccion`) | CP AR.3 |
| CP 0012.5 | Solo el receptor puede responder | Solicitud pendiente de Ana a Beto | Ana intenta aceptarla | "Esta solicitud no te pertenece." (403) | Auto (`test_solo_el_receptor_puede_responder_la_solicitud`, `test_flujo_completo_de_amistad_por_http`) | — |
| CP 0012.6 | No se responde dos veces | Solicitud ya aceptada | Beto la acepta de nuevo | Error 409 y el estado sigue "aceptada" | Auto (`test_no_se_puede_aceptar_dos_veces_la_misma_solicitud`) | — |
| CP 0012.7 | Solicitud inexistente | — | Identificador que no existe | "La solicitud no existe." (404) | Auto (`test_responder_solicitud_inexistente_da_error`) | — |

### CU0013 — Notificar Solicitud de Amistad Recibida

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0013.1 | Se envía el correo al receptor | `MAIL_SUPPRESS_SEND=false` con credenciales válidas | Ana solicita amistad a Beto | Beto recibe un correo "Ana te envió una solicitud de amistad", sin enlace, que indica iniciar sesión | Manual | CP SA.3 (corregido) |
| CP 0013.2 | La notificación aparece en la pantalla principal | Se ejecutó CP 0011.1 | Beto inicia sesión | Aparece la solicitud de Ana en "Solicitudes de amistad recibidas", con el contador de pendientes | Auto (`test_flujo_completo_de_amistad_por_http`) y Manual | CP NT.1 |
| CP 0013.3 | Sin pendientes | Usuario sin solicitudes | Ana inicia sesión | La sección **sigue visible** con el mensaje "No tenés solicitudes pendientes…". No se oculta | Manual | CP NT.2 (corregido) |
| CP 0013.4 | La notificación está desacoplada (Observer) | — | Evento "solicitud recibida" | El servicio de amistad publica el evento en el receptor y `NotificationService` lo recibe, sin que el servicio lo llame directamente | Auto (`test_solicitar_amistad_crea_solicitud_pendiente_y_dispara_el_observer`, `test_observer.py`) | CP NT.3 |
| CP 0013.5 | Con el envío apagado, la solicitud igual se crea | `MAIL_SUPPRESS_SEND=true` | Ana solicita amistad a Beto | La solicitud se crea y no se envía ningún correo | Auto (la configuración de pruebas lo fuerza) | — |
| CP 0013.6 | El notificador es único (Singleton) | — | Dos llamadas a `get_instance()` | Devuelven la misma instancia | Auto (`test_observer.py`) | — |

---

## 2. Procedimientos de prueba

Pasos numerados = curso normal; cada bloque "Alternativo N.M" reemplaza o continúa el paso N, con la misma numeración que las fichas de caso de uso.

### Preparación

1. Backend: `cd backend && source venv/bin/activate && python run.py` (puerto 5000).
2. Frontend: `cd frontend && npx ng serve` (puerto 4200).
3. Para empezar con datos: `python seed.py --reset` en `backend/`. Para probar sin enviar correo: `MAIL_SUPPRESS_SEND=true` en `backend/.env`.
4. Pruebas automáticas: `cd backend && python -m pytest` (deben pasar las 32).

### PR 0001 — Iniciar Sesión (CP 0001.1 a 0001.5)

1. Abrir `http://localhost:4200/login`.
2. Completar el correo de un usuario registrado y su contraseña correcta.
3. Presionar "Ingresar".
4. Verificar que se redirige a la pantalla principal y que muestra "Hola, <nombre>".
5. Verificar que el token quedó guardado en el almacenamiento local del navegador.

**Alternativo 3.1 — Campos vacíos (CP 0001.3).** Dejar la contraseña vacía y presionar "Ingresar". Verificar "Por favor complete todos los campos correctamente." y que no se hizo ninguna petición de red.

**Alternativo 3.2 — Credenciales incorrectas (CP 0001.2 y 0001.4).** Usar una contraseña incorrecta y luego un correo que no existe. Verificar que ambos casos muestran "Credenciales incorrectas.", sin token y sin redirección.

**Alternativo 4.1 — Ruta protegida (CP 0001.5).** Sin sesión, abrir `http://localhost:4200/welcome`. Verificar que se redirige a `/login`.

### PR 0006 — Registrar Usuario (CP 0006.1 a 0006.4)

1. Abrir `http://localhost:4200/register`.
2. Completar nombre, un correo nuevo y una contraseña de 8 o más caracteres.
3. Presionar el botón de registro.
4. Verificar "Cuenta creada con éxito. Ya podés iniciar sesión.".
5. Verificar que, tras un instante, se redirige a `/login` y que no hay sesión iniciada.
6. Iniciar sesión con la cuenta nueva (PR 0001).

**Alternativo 3.1 — Campos vacíos (CP 0006.4).** Dejar un campo vacío y enviar. Verificar el aviso y que no se hizo ninguna petición.

**Alternativo 4.1 — Contraseña corta (CP 0006.3).** Usar menos de 8 caracteres. Verificar "Por favor complete todos los campos correctamente." y que el usuario no se creó (no se puede iniciar sesión con él).

**Alternativo 5.1 — Correo ya registrado (CP 0006.2).** Repetir el registro con el mismo correo. Verificar "Este correo ya está registrado.".

### PR 0011 — Solicitar Amistad (CP 0011.1 a 0011.7)

1. Iniciar sesión como Ana (PR 0001).
2. En el bloque "Solicitar amistad", escribir el correo de Beto, que no es su amigo.
3. Presionar "Enviar".
4. Verificar "Solicitud enviada." y que el campo quedó vacío.

**Alternativo 3.1 — Campo vacío (CP 0011.6).** Presionar "Enviar" sin escribir nada. Verificar "Por favor complete todos los campos correctamente.".

**Alternativo 4.1 — Destinatario inexistente (CP 0011.4).** Usar un correo no registrado. Verificar "No existe un usuario con ese email.".

**Alternativo 5.1 — A uno mismo (CP 0011.3).** Usar el correo de Ana. Verificar "No podés enviarte una solicitud a vos mismo.".

**Alternativo 5.2 — Ya son amigos (CP 0011.5).** Después de PR 0012, repetir el paso 2 con Beto. Verificar "Ya son amigos.".

**Alternativo 5.3 — Pendiente duplicada (CP 0011.2).** Repetir los pasos 2 y 3 con Beto sin que él haya respondido. Verificar "Ya existe una solicitud pendiente para este usuario.". **No** se espera que desaparezca ningún botón.

**Alternativo 5.4 — Reenvío tras un rechazo (CP 0011.7).** Después de que Beto rechace (PR 0012, alternativo 2.1), repetir los pasos 2 y 3. **Falla conocida:** el servidor responde 500 y el campo muestra "No se pudo enviar la solicitud.". Anotar el resultado como defecto H1 hasta que se resuelva.

### PR 0012 — Aceptar / Rechazar Solicitud de Amistad (CP 0012.1 a 0012.7)

1. Iniciar sesión como Beto, receptor de una solicitud pendiente (PR 0011).
2. En "Solicitudes de amistad recibidas", localizar la solicitud de Ana, marcada "pendiente".
3. Presionar "Aceptar".
4. Verificar que la solicitud desaparece de los pendientes y que Ana aparece en "Tus amigos".
5. Cerrar sesión, iniciar como Ana y verificar que Beto aparece en "Tus amigos".

**Alternativo 3.1 — Rechazar (CP 0012.3).** Repetir con otra solicitud y presionar "Rechazar". Verificar que la solicitud desaparece de los pendientes y que no aparece ninguna amistad nueva en ninguna de las dos cuentas.

**Alternativo 3.2 — Responder una solicitud ajena (CP 0012.5).** Solo por la API: con el token de Ana, `POST /amistad/solicitudes/<id>/aceptar` sobre una solicitud dirigida a Beto. Verificar 403 "Esta solicitud no te pertenece.".

**Alternativo 4.1 — Responder dos veces (CP 0012.6).** Solo por la API: aceptar de nuevo una solicitud ya aceptada. Verificar 409 y que el estado sigue "aceptada".

### PR 0013 — Notificar Solicitud de Amistad Recibida (CP 0013.1 a 0013.6)

1. Con `MAIL_SUPPRESS_SEND=false` y credenciales válidas en `.env`, iniciar sesión como Ana y solicitar amistad a Beto (PR 0011).
2. Revisar la bandeja de Beto. Verificar el correo "Ana te envió una solicitud de amistad" y que **no contiene un enlace**: indica iniciar sesión en la aplicación.
3. Iniciar sesión como Beto y abrir la pantalla principal.
4. Verificar que "Solicitudes de amistad recibidas" muestra a Ana y el contador "1 pendiente".

**Alternativo 3.1 — Sin pendientes (CP 0013.3).** Iniciar sesión con un usuario sin solicitudes. Verificar que la sección sigue visible, con el mensaje "No tenés solicitudes pendientes…".

**Alternativo 1.1 — Envío apagado (CP 0013.5).** Con `MAIL_SUPPRESS_SEND=true`, repetir el paso 1. Verificar que la solicitud se crea, que aparece en la pantalla de Beto y que no llega ningún correo.

---

## 3. Cobertura y vacíos

| Tema | Estado |
|---|---|
| Reglas del servicio de amistad, State, Observer, Singleton, autorización y tokens | Cubiertos por las 32 pruebas automáticas |
| Pantallas (mensajes, redirecciones, contadores, sección sin pendientes) | Solo **manual**: no hay pruebas automáticas del frontend |
| Validación de la contraseña corta en el registro | Solo manual; **no hay prueba automática** |
| Reversión de la transacción si falla la creación de la amistad (RNF-12) | El código hace `rollback`, pero **no hay una prueba que fuerce el fallo** |
| Reenvío tras un rechazo | **Falla conocida** (CP 0011.7) |
| Envío real del correo | Solo manual (CP 0013.1) |

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Prueba | Versión inicial: plan, casos y procedimientos alineados con el comportamiento real y trazados a las pruebas automáticas |
