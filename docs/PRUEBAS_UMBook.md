# PRUEBAS — UMBook (casos implementados)

**Versión:** 2.2 · **Última modificación:** 26/11/2026 · **Etapa:** Prueba

Plan, casos y procedimientos de prueba de los tres casos de uso implementados (**CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación**), trazados a las 42 pruebas automáticas del backend (`4. Implementacion/codigo/backend/tests/`) y a las 11 del frontend (`frontend/src/app/core/*.spec.ts`). Los códigos de caso de uso están en [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) y los cursos alternativos citados (ca 4.1, ca 5.1, …) son los de las fichas de `1. Requerimientos/4_Casos de Uso/`.

La versión anterior, de la implementación de amistad (CU0011 a CU0013), está en `_version_anterior/docs/PRUEBAS_UMBook (amistad).md`. La columna **Antes** de cada caso indica el caso equivalente de esa versión, si lo había.

## Convenciones

| Marca | Significado |
|---|---|
| **Auto** | Está cubierto por una prueba automática: del backend (`python -m pytest`; se cita la función, `test_…`) o del frontend (`npx ng test`; se cita el nombre de la prueba entre comillas) |
| **Manual** | Se verifica a mano en el navegador, con el backend en `:5000` y el frontend en `:4200` |

Datos de prueba: los usuarios se crean desde la pantalla de registro (PR 0006). Para probar sin enviar correo real, poner `MAIL_SUPPRESS_SEND=true` en `backend/.env`; las pruebas automáticas lo fuerzan siempre.

---

## 0. Plan de pruebas

### Introducción

Este plan describe cómo se prueba UMBook, la red social de la materia Ingeniería de Software. **El alcance son los tres casos de uso implementados**: CU0001, CU0006 y CU0010, más los requisitos de seguridad que los atraviesan (RNF-18 a RNF-25). Los demás casos de uso del grupo no están implementados y no se prueban.

El sistema se prueba a nivel de **integración y de sistema** (automático, contra la API) y de **aceptación** (manual, desde el navegador). `Modelo_Plan_de_Pruebas.docx`, en `5. Pruebas/1_Plan de Pruebas/`, es el modelo del grupo: cubre casos de uso no implementados y nombra JUnit; el plan que se entrega es este.

### Elementos incluidos en las pruebas

- Gestión de Usuarios: registro (CU0006), inicio de sesión (CU0001) e invitación a la aplicación (CU0010).
- Control de acceso: token JWT, rutas protegidas del frontend y del backend.
- Correo: envío de la invitación por Flask-Mail y registro de su resultado.
- Configuración segura: clave de firma, TLS del correo y modo debug.
- Sesión en el navegador: vencimiento del token y dirección del backend (servicios y guard de Angular).
- Esquema de la base: migraciones.

### Funcionalidades a probar

| Subsistema | Funcionalidad | Casos de prueba |
|---|---|---|
| Gestión de Usuarios | Iniciar Sesión (CU0001) | CP 0001.1 a CP 0001.6 |
| Gestión de Usuarios | Registrar Usuario (CU0006) | CP 0006.1 a CP 0006.7 |
| Gestión de Usuarios | Invitación a la aplicación (CU0010) | CP 0010.1 a CP 0010.10 |
| Autenticación y Seguridad | Sesión, configuración, patrones y esquema de la base (transversal) | CP SEG.1 a CP SEG.9 |

### Estrategia de prueba

| Nivel | Qué se prueba | Cómo |
|---|---|---|
| Integración | Servicios y DAO con una base real; el Singleton del notificador | pytest, con una base SQLite temporal por prueba |
| Unidad (frontend) | `AuthService`, `NotificationService` y `AuthGuard` de Angular: vencimiento del token y dirección del backend | Vitest con jsdom (`npx ng test --watch=false`), con `HttpTestingController` |
| Sistema | La API completa: códigos de estado, mensajes, token y estado de las invitaciones | Cliente de pruebas de Flask dentro de pytest; el correo se captura con `mail.record_messages()` o se hace fallar con `monkeypatch` |
| Aceptación | Las pantallas: mensajes, validaciones del navegador, redirecciones y cierre de sesión | Manual, siguiendo los procedimientos de la sección 2 |

### Herramientas

| Herramienta | Para qué |
|---|---|
| pytest 8.3.3 | Pruebas automáticas del backend (`python -m pytest`, 42 pruebas) |
| Vitest 4 y jsdom | Pruebas automáticas del frontend (`npx ng test --watch=false`, 11 pruebas) |
| Cliente de pruebas de Flask | Pedidos HTTP sin levantar el servidor |
| `mail.record_messages()` de Flask-Mail | Ver los correos que se habrían enviado, sin enviarlos |
| Navegador web actual | Pruebas manuales de las pantallas |

Los componentes (pantallas) del frontend no tienen pruebas automáticas: se prueban a mano.

### Criterios de éxito

La prueba se completa cuando se ejecutaron todos los casos definidos, pasan las 42 pruebas del backend y las 11 del frontend, y no quedan defectos bloqueantes, críticos ni mayores sin resolver. Hoy pasan todas. Los hallazgos de diseño H6 a H11 (`DISEÑO_UMBook.md` §9) están resueltos.

### Entregables

- Este documento (plan, casos y procedimientos) y sus versiones en `5. Pruebas/`: `1_Plan de Pruebas/UMBook_Plan_de_Pruebas.docx`, `2_Procedimientos de Prueba.docx` y `3_Casos de Prueba.xlsx`.
- El resultado de `python -m pytest` de cada ciclo.
- El reporte de defectos e incidencias: la lista de pendientes de `docs/tareas.md` y los hallazgos de `DISEÑO_UMBook.md` §9.

### Ambiente de prueba

| Elemento | Detalle |
|---|---|
| Sistema operativo | Linux |
| Backend | Python 3.14 con las dependencias de `requirements-dev.txt` |
| Frontend | Node.js y Angular CLI 22 (`ng serve`, puerto 4200) |
| Base de datos | SQLite (temporal en las pruebas automáticas; `instance/umbook.db` en las manuales) |
| Correo | Cuenta de Gmail con *app password* para CP 0010.1 en manual; apagado o simulado en el resto |
| Navegador | Un navegador web de escritorio actual |

---

## 1. Casos de prueba

### CU0001 — Iniciar Sesión

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0001.1 | Inicio de sesión exitoso | Usuario registrado, sin sesión | Correo y contraseña correctos | 200 con `access_token` y los datos del usuario (`id`, `name`, `email`); la pantalla guarda el token y lleva a `/welcome` | Auto (`test_login_correcto_devuelve_token_y_datos_del_usuario`; frontend: "el login usa la dirección configurada y guarda el token (H10)") y Manual | CP 0001.1 |
| CP 0001.2 | Una contraseña incorrecta no autentica (ca 5.1) | Usuario registrado, sin sesión | Correo correcto, contraseña incorrecta | 401 "Credenciales incorrectas.", sin token y sin redirección | Auto (`test_login_con_clave_incorrecta_devuelve_401`) y Manual | CP 0001.2 |
| CP 0001.3 | Un correo inexistente da el mismo mensaje (ca 5.1, RNF-18) | Usuario registrado, sin sesión | Correo no registrado | Respuesta idéntica a la de CP 0001.2: `{msg: "Credenciales incorrectas."}` | Auto (`test_correo_inexistente_y_clave_incorrecta_dan_el_mismo_mensaje`) y Manual | CP 0001.4 |
| CP 0001.4 | Campos vacíos (ca 4.1) | Sin sesión | Correo y contraseña vacíos | En la pantalla: "Por favor complete todos los campos correctamente." sin llamar al servidor. En la API: 400 con el mismo mensaje | Auto (`test_login_con_campos_vacios_devuelve_400`) y Manual | CP 0001.3 |
| CP 0001.5 | Una pantalla protegida exige sesión | Sin sesión | Abrir `/welcome` o `/invite` | Se redirige a `/login`; con un token vigente se entra | Auto (frontend: "sin token no hay sesión", "con un token vigente hay sesión", "sin token redirige a /login", "deja pasar con un token vigente") y Manual | CP 0001.5 |
| CP 0001.6 | Cerrar sesión borra el token | Con sesión | Presionar "Cerrar sesión" | Se borra el token del almacenamiento local y se vuelve a `/login`; `/welcome` ya no abre | Manual | — |

### CU0006 — Registrar Usuario

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0006.1 | Registro exitoso | Correo no registrado | Nombre, correo nuevo, contraseña de 8 o más caracteres | 201 con `id` y `email`; la pantalla muestra "Cuenta creada con éxito. Ya podés iniciar sesión." y lleva a `/login` sin iniciar sesión | Auto (`test_registro_exitoso_devuelve_201`; frontend: "el registro usa la dirección configurada (H10)") y Manual | CP 0006.1 |
| CP 0006.2 | La contraseña se guarda cifrada (RNF-09) | Correo no registrado | Contraseña `password123` | El campo `password_hash` de la base no es ni contiene la contraseña | Auto (`test_la_clave_se_guarda_con_hash_y_no_en_claro`) | — |
| CP 0006.3 | Correo ya registrado (ca 6.1) | Correo existente | El mismo correo | 409 "Este correo ya está registrado." | Auto (`test_correo_ya_registrado_devuelve_409`) y Manual | CP 0006.2 |
| CP 0006.4 | El correo no distingue mayúsculas (ca 6.1, RNF-23) | `ana@test.com` registrado | `ANA@Test.com` | 409: es la misma cuenta | Auto (`test_el_correo_no_distingue_mayusculas`) | — |
| CP 0006.5 | Contraseña corta (ca 5.1) | — | Contraseña de menos de 8 caracteres | 400 "Por favor complete todos los campos correctamente." y el usuario no se crea | Auto (`test_clave_corta_devuelve_400_y_no_crea_el_usuario`) y Manual | CP 0006.3 |
| CP 0006.6 | Campos faltantes (ca 5.1) | — | Solo el correo, sin nombre ni contraseña | En la pantalla: el aviso, sin llamar al servidor. En la API: 400 | Auto (`test_registro_con_campos_faltantes_devuelve_400`) y Manual | CP 0006.4 |
| CP 0006.7 | Registro simultáneo con el mismo correo (ca 6.1, RNF-23) | `ana@test.com` registrado; un segundo registro pasa la búsqueda del correo antes de que el primero se guarde | El mismo correo | 409 "Este correo ya está registrado." (no 500) y queda un solo usuario; la base sigue aceptando registros | Auto (`test_registro_simultaneo_con_el_mismo_correo_devuelve_409`, `test_crear_un_usuario_con_correo_repetido_devuelve_none_y_la_base_sigue_usable`) | — |

### CU0010 — Invitación a la aplicación

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0010.1 | Invitación exitosa | Ana con sesión | Correo `beto@test.com` | 200 "Invitación enviada."; sale un correo a `beto@test.com` que nombra a Ana; la pantalla muestra "Invitación enviada. Le llegará un correo a beto@test.com." | Auto (`test_invitacion_exitosa_envia_un_correo_al_invitado`; frontend: "la invitación usa la dirección configurada (H10)") y Manual | — |
| CP 0010.2 | El correo lleva el enlace de registro | Ana con sesión | Correo válido | El cuerpo del correo contiene `http://localhost:4200/register` (CU0006) | Auto (`test_el_correo_de_invitacion_incluye_el_enlace_de_registro`) y Manual | — |
| CP 0010.3 | La invitación queda guardada como enviada (Ob 1) | Ana con sesión | `Beto@Test.com` | Una fila en `invitations`: correo normalizado `beto@test.com`, estado `enviada`, quien invita es Ana y tiene fecha | Auto (`test_la_invitacion_enviada_queda_guardada_como_enviada`) | — |
| CP 0010.4 | Correo con formato inválido (ca 4.1) | Ana con sesión | `esto-no-es-un-correo` | En la pantalla: "Ingresá un correo válido." sin llamar al servidor. En la API: 400 y no sale ningún correo | Auto (`test_correo_invalido_devuelve_400_y_no_envia_nada`) y Manual | — |
| CP 0010.5 | Correo de más de 254 caracteres (ca 4.1, rnf 2.1) | Ana con sesión | Correo de 312 caracteres | 400 | Auto (`test_correo_de_mas_de_254_caracteres_devuelve_400`) | — |
| CP 0010.6 | Fallo del servidor de correo (ca 5.1, RNF-22) | Ana con sesión; el servidor de correo rechaza el envío | Correo válido | 500 "No se pudo enviar la invitación. Intentá de nuevo.", sin detalles del servidor de correo en la respuesta; la pantalla deja el formulario listo para reintentar | Auto (`test_falla_del_correo_responde_500_sin_detalles_internos`) y Manual | — |
| CP 0010.7 | El fallo queda registrado (ca 5.1, RNF-24) | Igual que CP 0010.6 | Correo válido | La invitación queda guardada con estado `fallida` | Auto (`test_si_falla_el_envio_la_invitacion_queda_guardada_como_fallida`) | — |
| CP 0010.8 | Invitar exige sesión | Sin sesión | `POST /invite` sin token | 401 | Auto (`test_invitar_sin_token_devuelve_401`) | — |
| CP 0010.9 | Sin sesión o con correo inválido no se guarda nada | — | Pedido sin token; pedido con correo inválido | La tabla `invitations` queda vacía | Auto (`test_sin_sesion_o_con_correo_invalido_no_se_guarda_ninguna_invitacion`) | — |
| CP 0010.10 | El envío no queda esperando a un servidor que no responde (ca 5.1, rnf 2.2) | Ana con sesión; el servidor de correo acepta la conexión y no contesta | Correo válido | La conexión SMTP se abre con `MAIL_TIMEOUT` (5 s); al vencer, 500 "No se pudo enviar la invitación. Intentá de nuevo." y la invitación queda `fallida` | Auto (`test_la_conexion_smtp_se_abre_con_timeout`, `test_si_el_servidor_de_correo_no_responde_la_invitacion_queda_fallida`) | — |

### Transversal — Seguridad y configuración

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP SEG.1 | Un token vencido se rechaza (RNF-20, H6) | Usuario registrado | Token con vencimiento en el pasado | 401 en `/invite`. En el navegador, `AuthGuard` lee el vencimiento: al abrir una pantalla protegida cierra la sesión y lleva a `/login` | Auto (`test_token_vencido_devuelve_401`; frontend: "con un token vencido no hay sesión y se borra la sesión local (H6)", "con el token vencido redirige a /login y cierra la sesión (H6)") y Manual | CP 0001.7 (corregido) |
| CP SEG.2 | Un token corrupto se rechaza sin detalles (RNF-20, RNF-22) | — | Token `esto-no-es-un-jwt` | 401 `{msg: "Sesión inválida o vencida. Iniciá sesión de nuevo."}`. Antes se esperaba 422; el código responde 401 | Auto (`test_token_invalido_devuelve_401_sin_detalles`; frontend: "un token ilegible o sin vencimiento se trata como vencido") | CP 0001.7 (corregido) |
| CP SEG.3 | Un token de un usuario que ya no existe se rechaza | — | Token válido con `identity` 999 | 401 | Auto (`test_token_de_un_usuario_que_ya_no_existe_devuelve_401`) | — |
| CP SEG.4 | Un token firmado con la clave vieja no sirve (RNF-21) | Usuario registrado | Token firmado con `super-secret`, la clave que estaba fija en el código original | 401 | Auto (`test_un_token_firmado_con_la_clave_vieja_super_secret_no_sirve`) | — |
| CP SEG.5 | Configuración segura (RNF-21) | — | `JWT_SECRET_KEY` vacía, ausente o con un valor de ejemplo; `MAIL_USE_TLS` en `true`, `True`, `TRUE` o `1`; `run.py` | La aplicación no arranca sin una clave segura (4 variantes); TLS se activa con cualquiera de los 4 valores; `run.py` escucha en `127.0.0.1` y no fija `debug=True` | Auto (`test_la_aplicacion_no_arranca_sin_una_clave_jwt_segura`, `test_mail_use_tls_acepta_true_en_minuscula`, `test_run_no_expone_el_depurador_en_la_red`) | — |
| CP SEG.6 | El notificador es único (Singleton, RNF-25) | — | Dos llamadas a `NotificationService()` | Devuelven la misma instancia | Auto (`test_notification_service_es_singleton`) | CP 0013.6 |
| CP SEG.7 | La dirección del backend se configura en un solo lugar (H10) | — | `API_URL` sin reemplazar; `API_URL` reemplazada por `http://api.prueba` | Por defecto vale `environment.apiUrl`; con otro valor, login, registro e invitación van a esa dirección (ver CP 0001.1, 0006.1 y 0010.1) | Auto (frontend: "por defecto la dirección es la de environment.ts (H10)") | — |
| CP SEG.8 | El servicio de autenticación devuelve el usuario o nada (H9) | — | Registro nuevo y repetido; login correcto, con clave incorrecta y con correo inexistente | `register_user` y `authenticate` devuelven el `User` o `None`, nunca una tupla | Auto (`test_auth_service_devuelve_el_usuario_o_none_en_registro_y_login`) | — |
| CP SEG.9 | El esquema de la base sale de las migraciones (H11) | Base nueva; base creada con `create_all()` con un usuario; base vieja con solo `users` | — | La base nueva queda igual a los modelos; la vieja se adopta sin perder el usuario; a la que no tiene `invitations` se le agrega la tabla; `run.py` aplica las migraciones | Auto (`test_las_migraciones_crean_el_mismo_esquema_que_los_modelos`, `test_una_base_creada_con_create_all_se_adopta_sin_perder_datos`, `test_una_base_vieja_sin_invitaciones_recibe_la_tabla`, `test_run_usa_las_migraciones_y_no_create_all`) | — |

---

## 2. Procedimientos de prueba

Pasos numerados = curso normal; cada bloque "Alternativo N.M" reemplaza o continúa el paso N y usa la misma numeración que los cursos alternativos de la ficha.

### Preparación

1. Backend: `cd "4. Implementacion/codigo/backend"`, activar el entorno (`source venv/bin/activate`) y ejecutar `python run.py` (puerto 5000). Requiere `backend/.env` con `JWT_SECRET_KEY` (ver `.env.example`).
2. Frontend: `cd "4. Implementacion/codigo/frontend"` y `npx ng serve` (puerto 4200).
3. Para probar sin enviar correo: `MAIL_SUPPRESS_SEND=true` en `backend/.env`.
4. Pruebas automáticas del backend: en `backend/`, `python -m pytest` (deben pasar las 42).
5. Pruebas automáticas del frontend: en `frontend/`, `npx ng test --watch=false` (deben pasar las 11).

### PR 0001 — Iniciar Sesión (CP 0001.1 a 0001.6)

1. Abrir `http://localhost:4200/login`.
2. Completar el correo de un usuario registrado y su contraseña correcta.
3. Presionar "Ingresar".
4. Verificar que se abre la pantalla principal con el nombre del usuario.
5. Verificar que el token quedó guardado en el almacenamiento local del navegador (`access_token`).

**Alternativo 4.1 — Campos vacíos (CP 0001.4).** Dejar la contraseña vacía y presionar "Ingresar". Verificar "Por favor complete todos los campos correctamente." y que no se hizo ninguna petición de red.

**Alternativo 5.1 — Credenciales incorrectas (CP 0001.2 y 0001.3).** Usar una contraseña incorrecta y luego un correo que no existe. Verificar que los dos casos muestran "Credenciales incorrectas.", sin token y sin redirección.

**Alternativo 6.1 — Pantalla protegida (CP 0001.5).** Sin sesión, abrir `http://localhost:4200/welcome` y luego `/invite`. Verificar que las dos redirigen a `/login`.

**Alternativo 6.2 — Cerrar sesión (CP 0001.6).** Con sesión, presionar "Cerrar sesión". Verificar que se vuelve a `/login`, que el token ya no está en el almacenamiento local y que `/welcome` redirige a `/login`.

### PR 0006 — Registrar Usuario (CP 0006.1 a 0006.7)

1. Abrir `http://localhost:4200/register`.
2. Completar nombre, un correo nuevo y una contraseña de 8 o más caracteres.
3. Presionar "Registrarse".
4. Verificar "Cuenta creada con éxito. Ya podés iniciar sesión.".
5. Verificar que, tras un instante, se abre `/login` y que no hay sesión iniciada.
6. Iniciar sesión con la cuenta nueva (PR 0001).

**Alternativo 5.1 — Datos inválidos (CP 0006.5 y 0006.6).** Dejar un campo vacío y enviar; después usar una contraseña de menos de 8 caracteres. Verificar en los dos casos "Por favor complete todos los campos correctamente.", que no se hizo ninguna petición de red y que la cuenta no existe (no se puede iniciar sesión con ella).

**Alternativo 6.1 — Correo ya registrado (CP 0006.3 y 0006.4).** Repetir el registro con el mismo correo y luego con el mismo correo en mayúsculas. Verificar en los dos casos "Este correo ya está registrado.".

**Alternativo 6.2 — Registro simultáneo (CP 0006.7).** Es una prueba automática: `python -m pytest tests/test_auth.py -k "simultaneo or repetido" -v`.

### PR 0010 — Invitación a la aplicación (CP 0010.1 a 0010.10)

1. Con `MAIL_SUPPRESS_SEND=false` y credenciales de correo válidas en `.env`, iniciar sesión (PR 0001).
2. En la pantalla principal, abrir "Invitar amigos".
3. Escribir un correo al que se tenga acceso y presionar "Enviar invitación".
4. Verificar "Invitación enviada. Le llegará un correo a <correo>." y que el campo quedó vacío.
5. Revisar la bandeja del correo invitado. Verificar que el mensaje "¡Te invitaron a UMBook!" nombra a quien invita y trae el enlace `http://localhost:4200/register`.
6. Abrir el enlace y verificar que lleva a la pantalla de registro (CU0006).

**Alternativo 4.1 — Correo inválido (CP 0010.4).** Escribir `esto-no-es-un-correo` y enviar. Verificar "Ingresá un correo válido." y que no se hizo ninguna petición de red.

**Alternativo 5.1 — Falla el correo (CP 0010.6 y 0010.7).** Poner un `MAIL_PASSWORD` inválido en `.env` y reiniciar el backend. Repetir los pasos 2 y 3. Verificar "No se pudo enviar la invitación. Intentá de nuevo.", que el formulario sigue disponible y que en la consola del backend aparece "No se pudo enviar la invitación a …". Restaurar la clave correcta al terminar.

**Alternativo 5.2 — El servidor de correo no responde (CP 0010.10).** Es una prueba automática: en `backend/`, `python -m pytest tests/test_invite.py -k "timeout or no_responde" -v`. A mano: poner `MAIL_SERVER` apuntando a una máquina que no responde y `MAIL_TIMEOUT=2` en `.env`, reiniciar el backend y enviar una invitación. Verificar que el aviso de fallo aparece a los pocos segundos.

**Alternativo 1.1 — Sesión vencida (CP SEG.1).** Iniciar sesión y esperar más de 15 minutos (o poner a mano un token vencido en el almacenamiento local). Abrir `/invite`: verificar que la aplicación cierra la sesión y vuelve a `/login`. Repetir quedándose en la pantalla de invitar y enviando: la petición responde 401 y también vuelve a `/login`.

### PR SEG — Seguridad y configuración (CP SEG.1 a SEG.9)

Son pruebas automáticas: en `backend/`, `python -m pytest tests/test_seguridad.py tests/test_invite.py tests/test_auth.py -v`, y en `frontend/`, `npx ng test --watch=false`. Verificar que pasan todas. CP SEG.1 tiene además el procedimiento manual del alternativo 1.1 de PR 0010.

---

## 3. Cobertura y vacíos

| Tema | Estado |
|---|---|
| API de los tres casos de uso: códigos, mensajes, token, estado de las invitaciones y correo | Cubiertos por las pruebas automáticas del backend |
| Servicios y guard de Angular: vencimiento del token y dirección del backend | Cubiertos por las 11 pruebas del frontend |
| Esquema de la base (migraciones) | Cubierto por las pruebas automáticas (CP SEG.9) |
| Configuración segura (clave JWT, TLS, depurador) y Singleton | Cubiertos por las pruebas automáticas (`test_seguridad.py`) |
| Pantallas: validaciones del navegador, mensajes, redirecciones, cierre de sesión | Solo **manual**: los componentes no tienen pruebas automáticas |
| Envío real del correo | Solo manual (PR 0010, pasos 1 a 6) |
| Registro simultáneo con el mismo correo (H8) y servidor de correo que no responde (H7) | Cubiertos por pruebas automáticas (CP 0006.7 y CP 0010.10), con la carrera y el servidor simulados |

Trazabilidad: las 42 pruebas del backend (36 funciones; dos de ellas se ejecutan con 4 valores cada una) y las 11 del frontend están citadas en algún caso.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.1 | 25/11/2026 | Prueba | Se resuelven H1, H2 y H5: CP 0011.7 pasa a automático; se agregan CP 0011.8 (solicitud cruzada) y CP 0013.7 (falla del correo) con sus procedimientos; 39 pruebas automáticas |
| 2.0 | 26/11/2026 | Prueba | Realineado con la implementación actual: CU0001, CU0006 y CU0010 (nuevo) más casos transversales de seguridad, trazados a las 33 pruebas. Token corrupto: 401 (antes 422). Se quitan los casos de amistad, que pasan a `_version_anterior/docs/` |
| 2.1 | 26/11/2026 | Prueba | CP 0006.7 (registro simultáneo, H8) y CP 0010.10 (servidor de correo que no responde, H7); 29 casos trazados a las 37 pruebas |
| 2.2 | 26/11/2026 | Prueba | Pruebas del frontend (Vitest, 11) y casos CP SEG.7 a SEG.9 para H6, H9, H10 y H11; 32 casos trazados a 42 pruebas del backend y 11 del frontend |
