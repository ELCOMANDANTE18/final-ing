# PRUEBAS — UMBook (casos implementados)

**Versión:** 2.1 · **Última modificación:** 26/11/2026 · **Etapa:** Prueba

Plan, casos y procedimientos de prueba de los tres casos de uso implementados (**CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación**), trazados a las 37 pruebas automáticas de `4. Implementacion/codigo/backend/tests/`. Los códigos de caso de uso están en [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) y los cursos alternativos citados (ca 4.1, ca 5.1, …) son los de las fichas de `1. Requerimientos/4_Casos de Uso/`.

La versión anterior, de la implementación de amistad (CU0011 a CU0013), está en `_version_anterior/docs/PRUEBAS_UMBook (amistad).md`. La columna **Antes** de cada caso indica el caso equivalente de esa versión, si lo había.

## Convenciones

| Marca | Significado |
|---|---|
| **Auto** | Está cubierto por una prueba automática de `backend/tests/` (se corre con `python -m pytest`); se cita la función |
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

### Funcionalidades a probar

| Subsistema | Funcionalidad | Casos de prueba |
|---|---|---|
| Gestión de Usuarios | Iniciar Sesión (CU0001) | CP 0001.1 a CP 0001.6 |
| Gestión de Usuarios | Registrar Usuario (CU0006) | CP 0006.1 a CP 0006.7 |
| Gestión de Usuarios | Invitación a la aplicación (CU0010) | CP 0010.1 a CP 0010.10 |
| Autenticación y Seguridad | Sesión, configuración y patrones (transversal) | CP SEG.1 a CP SEG.6 |

### Estrategia de prueba

| Nivel | Qué se prueba | Cómo |
|---|---|---|
| Integración | Servicios y DAO con una base real; el Singleton del notificador | pytest, con una base SQLite temporal por prueba |
| Sistema | La API completa: códigos de estado, mensajes, token y estado de las invitaciones | Cliente de pruebas de Flask dentro de pytest; el correo se captura con `mail.record_messages()` o se hace fallar con `monkeypatch` |
| Aceptación | Las pantallas: mensajes, validaciones del navegador, redirecciones y cierre de sesión | Manual, siguiendo los procedimientos de la sección 2 |

### Herramientas

| Herramienta | Para qué |
|---|---|
| pytest 8.3.3 | Pruebas automáticas del backend (`python -m pytest`, 37 pruebas) |
| Cliente de pruebas de Flask | Pedidos HTTP sin levantar el servidor |
| `mail.record_messages()` de Flask-Mail | Ver los correos que se habrían enviado, sin enviarlos |
| Navegador web actual | Pruebas manuales de las pantallas |

No hay pruebas automáticas del frontend.

### Criterios de éxito

La prueba se completa cuando se ejecutaron todos los casos definidos, pasan las 37 pruebas automáticas y no quedan defectos bloqueantes, críticos ni mayores sin resolver. Hoy pasan las 37. H7 y H8 están resueltos; los demás hallazgos de diseño (H6, H9 a H11 de `DISEÑO_UMBook.md` §9) no son defectos bloqueantes.

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
| CP 0001.1 | Inicio de sesión exitoso | Usuario registrado, sin sesión | Correo y contraseña correctos | 200 con `access_token` y los datos del usuario (`id`, `name`, `email`); la pantalla guarda el token y lleva a `/welcome` | Auto (`test_login_correcto_devuelve_token_y_datos_del_usuario`) y Manual | CP 0001.1 |
| CP 0001.2 | Una contraseña incorrecta no autentica (ca 5.1) | Usuario registrado, sin sesión | Correo correcto, contraseña incorrecta | 401 "Credenciales incorrectas.", sin token y sin redirección | Auto (`test_login_con_clave_incorrecta_devuelve_401`) y Manual | CP 0001.2 |
| CP 0001.3 | Un correo inexistente da el mismo mensaje (ca 5.1, RNF-18) | Usuario registrado, sin sesión | Correo no registrado | Respuesta idéntica a la de CP 0001.2: `{msg: "Credenciales incorrectas."}` | Auto (`test_correo_inexistente_y_clave_incorrecta_dan_el_mismo_mensaje`) y Manual | CP 0001.4 |
| CP 0001.4 | Campos vacíos (ca 4.1) | Sin sesión | Correo y contraseña vacíos | En la pantalla: "Por favor complete todos los campos correctamente." sin llamar al servidor. En la API: 400 con el mismo mensaje | Auto (`test_login_con_campos_vacios_devuelve_400`) y Manual | CP 0001.3 |
| CP 0001.5 | Una pantalla protegida exige sesión | Sin sesión | Abrir `/welcome` o `/invite` | Se redirige a `/login` | Manual | CP 0001.5 |
| CP 0001.6 | Cerrar sesión borra el token | Con sesión | Presionar "Cerrar sesión" | Se borra el token del almacenamiento local y se vuelve a `/login`; `/welcome` ya no abre | Manual | — |

### CU0006 — Registrar Usuario

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0006.1 | Registro exitoso | Correo no registrado | Nombre, correo nuevo, contraseña de 8 o más caracteres | 201 con `id` y `email`; la pantalla muestra "Cuenta creada con éxito. Ya podés iniciar sesión." y lleva a `/login` sin iniciar sesión | Auto (`test_registro_exitoso_devuelve_201`) y Manual | CP 0006.1 |
| CP 0006.2 | La contraseña se guarda cifrada (RNF-09) | Correo no registrado | Contraseña `password123` | El campo `password_hash` de la base no es ni contiene la contraseña | Auto (`test_la_clave_se_guarda_con_hash_y_no_en_claro`) | — |
| CP 0006.3 | Correo ya registrado (ca 6.1) | Correo existente | El mismo correo | 409 "Este correo ya está registrado." | Auto (`test_correo_ya_registrado_devuelve_409`) y Manual | CP 0006.2 |
| CP 0006.4 | El correo no distingue mayúsculas (ca 6.1, RNF-23) | `ana@test.com` registrado | `ANA@Test.com` | 409: es la misma cuenta | Auto (`test_el_correo_no_distingue_mayusculas`) | — |
| CP 0006.5 | Contraseña corta (ca 5.1) | — | Contraseña de menos de 8 caracteres | 400 "Por favor complete todos los campos correctamente." y el usuario no se crea | Auto (`test_clave_corta_devuelve_400_y_no_crea_el_usuario`) y Manual | CP 0006.3 |
| CP 0006.6 | Campos faltantes (ca 5.1) | — | Solo el correo, sin nombre ni contraseña | En la pantalla: el aviso, sin llamar al servidor. En la API: 400 | Auto (`test_registro_con_campos_faltantes_devuelve_400`) y Manual | CP 0006.4 |
| CP 0006.7 | Registro simultáneo con el mismo correo (ca 6.1, RNF-23) | `ana@test.com` registrado; un segundo registro pasa la búsqueda del correo antes de que el primero se guarde | El mismo correo | 409 "Este correo ya está registrado." (no 500) y queda un solo usuario; la base sigue aceptando registros | Auto (`test_registro_simultaneo_con_el_mismo_correo_devuelve_409`, `test_crear_un_usuario_con_correo_repetido_devuelve_none_y_la_base_sigue_usable`) | — |

### CU0010 — Invitación a la aplicación

| Id | Objetivo | Estado inicial | Datos | Resultado esperado | Tipo | Antes |
|---|---|---|---|---|---|---|
| CP 0010.1 | Invitación exitosa | Ana con sesión | Correo `beto@test.com` | 200 "Invitación enviada."; sale un correo a `beto@test.com` que nombra a Ana; la pantalla muestra "Invitación enviada. Le llegará un correo a beto@test.com." | Auto (`test_invitacion_exitosa_envia_un_correo_al_invitado`) y Manual | — |
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
| CP SEG.1 | Un token vencido se rechaza (RNF-20) | Usuario registrado | Token con vencimiento en el pasado | 401 en `/invite`; en la pantalla, la próxima petición cierra la sesión y lleva a `/login` | Auto (`test_token_vencido_devuelve_401`) y Manual | CP 0001.7 (corregido) |
| CP SEG.2 | Un token corrupto se rechaza sin detalles (RNF-20, RNF-22) | — | Token `esto-no-es-un-jwt` | 401 `{msg: "Sesión inválida o vencida. Iniciá sesión de nuevo."}`. Antes se esperaba 422; el código responde 401 | Auto (`test_token_invalido_devuelve_401_sin_detalles`) | CP 0001.7 (corregido) |
| CP SEG.3 | Un token de un usuario que ya no existe se rechaza | — | Token válido con `identity` 999 | 401 | Auto (`test_token_de_un_usuario_que_ya_no_existe_devuelve_401`) | — |
| CP SEG.4 | Un token firmado con la clave vieja no sirve (RNF-21) | Usuario registrado | Token firmado con `super-secret`, la clave que estaba fija en el código original | 401 | Auto (`test_un_token_firmado_con_la_clave_vieja_super_secret_no_sirve`) | — |
| CP SEG.5 | Configuración segura (RNF-21) | — | `JWT_SECRET_KEY` vacía, ausente o con un valor de ejemplo; `MAIL_USE_TLS` en `true`, `True`, `TRUE` o `1`; `run.py` | La aplicación no arranca sin una clave segura (4 variantes); TLS se activa con cualquiera de los 4 valores; `run.py` escucha en `127.0.0.1` y no fija `debug=True` | Auto (`test_la_aplicacion_no_arranca_sin_una_clave_jwt_segura`, `test_mail_use_tls_acepta_true_en_minuscula`, `test_run_no_expone_el_depurador_en_la_red`) | — |
| CP SEG.6 | El notificador es único (Singleton, RNF-25) | — | Dos llamadas a `NotificationService()` | Devuelven la misma instancia | Auto (`test_notification_service_es_singleton`) | CP 0013.6 |

---

## 2. Procedimientos de prueba

Pasos numerados = curso normal; cada bloque "Alternativo N.M" reemplaza o continúa el paso N y usa la misma numeración que los cursos alternativos de la ficha.

### Preparación

1. Backend: `cd "4. Implementacion/codigo/backend"`, activar el entorno (`source venv/bin/activate`) y ejecutar `python run.py` (puerto 5000). Requiere `backend/.env` con `JWT_SECRET_KEY` (ver `.env.example`).
2. Frontend: `cd "4. Implementacion/codigo/frontend"` y `npx ng serve` (puerto 4200).
3. Para probar sin enviar correo: `MAIL_SUPPRESS_SEND=true` en `backend/.env`.
4. Pruebas automáticas: en `backend/`, `python -m pytest` (deben pasar las 37).

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

**Alternativo 1.1 — Sesión vencida (CP SEG.1).** Iniciar sesión, esperar más de 15 minutos (o borrar a mano el token del almacenamiento local y poner uno inválido) e intentar enviar una invitación. Verificar que la aplicación vuelve a `/login`.

### PR SEG — Seguridad y configuración (CP SEG.1 a SEG.6)

Son pruebas automáticas: en `backend/`, `python -m pytest tests/test_seguridad.py tests/test_invite.py -v`. Verificar que pasan todas. CP SEG.1 tiene además el procedimiento manual del alternativo 1.1 de PR 0010.

---

## 3. Cobertura y vacíos

| Tema | Estado |
|---|---|
| API de los tres casos de uso: códigos, mensajes, token, estado de las invitaciones y correo | Cubiertos por las 37 pruebas automáticas |
| Configuración segura (clave JWT, TLS, depurador) y Singleton | Cubiertos por las pruebas automáticas (`test_seguridad.py`) |
| Pantallas: validaciones del navegador, mensajes, redirecciones, cierre de sesión | Solo **manual**: no hay pruebas automáticas del frontend |
| `AuthGuard` con el token vencido (H6) | Solo manual: deja abrir las pantallas hasta la primera petición |
| Envío real del correo | Solo manual (PR 0010, pasos 1 a 6) |
| Registro simultáneo con el mismo correo (H8) y servidor de correo que no responde (H7) | Cubiertos por pruebas automáticas (CP 0006.7 y CP 0010.10), con la carrera y el servidor simulados |

Trazabilidad: las 37 pruebas automáticas están citadas en algún caso (31 funciones; dos de ellas se ejecutan con 4 valores cada una).

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Prueba | Versión inicial: plan, casos y procedimientos alineados con el comportamiento real y trazados a las pruebas automáticas |
| 1.1 | 25/11/2026 | Prueba | Se resuelven H1, H2 y H5: CP 0011.7 pasa a automático; se agregan CP 0011.8 (solicitud cruzada) y CP 0013.7 (falla del correo) con sus procedimientos; 39 pruebas automáticas |
| 2.0 | 26/11/2026 | Prueba | Realineado con la implementación actual: CU0001, CU0006 y CU0010 (nuevo) más casos transversales de seguridad, trazados a las 33 pruebas. Token corrupto: 401 (antes 422). Se quitan los casos de amistad, que pasan a `_version_anterior/docs/` |
| 2.1 | 26/11/2026 | Prueba | CP 0006.7 (registro simultáneo, H8) y CP 0010.10 (servidor de correo que no responde, H7); 29 casos trazados a las 37 pruebas |
