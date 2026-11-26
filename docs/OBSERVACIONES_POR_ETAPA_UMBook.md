# OBSERVACIONES DE CONSISTENCIA POR ETAPA — UMBook

**Versión:** 1.6 · **Última modificación:** 26/11/2026 · **Etapa:** Gestión del proyecto

Revisión de cada carpeta de etapa contra **la implementación actual** (`4. Implementacion/`): **CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación**, con el código de la compañera corregido. El objetivo es que todo sea uno a uno y tenga sentido para la cátedra.

La revisión (versión 1.0) no modificó ningún artefacto. Las correcciones se aplican **etapa por etapa**, y su avance queda en la sección "Avance de las correcciones".

## Avance de las correcciones

**Decisiones tomadas (§8):**
1. **Fichas:** se conservan todas. Las tres que usa la implementación tienen su ficha en Requerimientos (CU0001 → `CU0001_Iniciar_Sesión.docx`; CU0006 → `CU0006.docx` y `CU0006_Registrar_Usuario.docx`; CU0010 → `CU0010.docx`), y se corrigieron para que coincidan con el código.
2. **Invitaciones:** se aplican M-1 (se guardan) y M-2 (enlace de registro en el correo).
3. **Amistad (implementación anterior):** se mueve a `_version_anterior/`.
4. **RNF y diagrama de casos de uso:** se regeneran actualizados.
5. **Códigos repetidos:** se renumeran a códigos libres (ver `docs/CATALOGO_CASOS_DE_USO_UMBook.md` §3).

| Etapa | Estado | Qué se hizo |
|---|---|---|
| Código (M-1, M-2) | ✅ Aplicado | Tabla `invitations` con estado `pendiente` → `enviada` / `fallida`; `InvitationDAO` e `InvitationService`; enlace `FRONTEND_URL/register` en el correo. 33 pruebas (4 nuevas) |
| Código (H6, H9, H10, H11) | ✅ Aplicado | `AuthGuard` detecta el token vencido; `AuthService` devuelve `User` o `None`; dirección del backend en `environment.ts`; migraciones de Alembic. 5 pruebas nuevas del backend (42) y 11 del frontend (Vitest) |
| Código (H7, H8) | ✅ Aplicado | Timeout en la conexión SMTP (`MailConTimeout`, `MAIL_TIMEOUT`=5 s) y registro simultáneo con el mismo correo respondiendo 409; 4 pruebas nuevas, 37 en total |
| 1. Requerimientos | ✅ Corregida | Ver la tabla de abajo |
| 2. Análisis | ✅ Corregida | Ver la tabla de la Etapa 2 |
| 3. Diseño | ✅ Corregida | Ver la tabla de la Etapa 3 |
| 4. Implementación | ✅ Corregida | Ver la tabla de la Etapa 4 |
| 5. Pruebas | ✅ Corregida | Ver la tabla de la Etapa 5 |

**Etapa 1, observación por observación:**

| # | Estado | Cómo se resolvió |
|---|---|---|
| R-01, R-02 | ✅ | Diagrama único `Diagrama de Casos de Uso - UMBook` (.pdf, .png y .svg), generado con `docs/generar_diagrama_casos_de_uso.py`: 24 casos de uso con código, en los 6 paquetes del diagrama de paquetes de Análisis, actores de la lista y los tres implementados resaltados. Los diagramas anteriores (`0-CU_General.pdf`, `CU-7-11-23.pdf`) pasan a `_version_anterior/` |
| R-03 | ✅ | Las fichas corregidas y las generadas usan los actores de `2_Lista de Actores y CU.docx` |
| R-04 | ✅ | Con M-1, `Invitación` se guarda: el modelo de dominio (marcado OK por la cátedra) queda correcto sin cambios. `fechaNacimiento` corresponde a los casos de cumpleaños |
| R-05 | ✅ | Se conservan todas las fichas, con el mismo flujo. `CU0006_Registrar_Usuario.docx` sigue la numeración de `CU0006.docx`. Mapeo en el catálogo §1 |
| R-06 | ✅ | `CU0010.docx`: precondición "sesión iniciada (CU0001)", ca 4.1 y ca 5.1 bien anclados y numerados, invitación registrada (Ob 1), rebotes no detectados (Ob 2), rnf 2.2 a 5 s (Ob 3). El enlace de registro ya es cierto (M-2) |
| R-07 | ✅ en Requerimientos | La ficha oficial de CU0001 tiene rnf 1.1 a 1.5 con código, ca 5.1 "Credenciales incorrectas" y Ob 1 sobre `localStorage`; HTTPS queda en RNF-10 como "No cumplido". La ficha PDF de la compañera se conserva tal cual; sus diferencias se anotan en la Etapa 4 |
| R-08 | ✅ | `CU0006.docx`: título completo, "contraseña de al menos 8 caracteres", ca 5.1 (validación) y ca 6.1 (email registrado) |
| R-09 | ✅ | Fichas generadas regeneradas: 401 como única respuesta de sesión inválida, nombre de 1 a 128, documentación anexa a Análisis, Diseño e Implementación |
| R-10 | ✅ | Fichas de CU0011 a CU0013 (amistad) movidas a `_version_anterior/` |
| R-11 | ✅ | Catálogo reescrito. **Corrección a esta revisión:** `CU0005.docx` y `CU0009.docx` tampoco eran plantillas vacías (son Solicitar Amistad y Notificación de Cumpleaños, sin título); se completaron. Se renumeraron los repetidos (CU0014, CU0015, CU0016, CU0018) y se corrigieron encabezados con código equivocado (CU0016, CU0017, CU0018) |
| R-12 | ✅ | `UMBook_RNF.docx` regenerado desde `docs/REQUISITOS_NO_FUNCIONALES_UMBook.md`: RNF-01 a RNF-17 del documento del grupo, RNF-18 a RNF-25 de los casos implementados, con estado, verificación y trazabilidad con las fichas |
| R-13 | ✅ | `Link al FIgma.docx` indica qué códigos cubre cada prototipo (se asume que "Casos 1, 2 y 3" son CU0001 a CU0003, por el nombre del archivo de Figma). El contenido de Figma no se verificó |

**Etapa 2, observación por observación:**

| # | Estado | Cómo se resolvió |
|---|---|---|
| A-01 | ✅ | Nuevo `1_Diagrama de Clases de Análisis - Casos implementados.png`: interfaz (`PantallaLogin`, `PantallaRegistro`, `PantallaPrincipal`, `PantallaInvitar`, `InterfazCorreo`), control (`ControlAutenticacion`, `ControlInvitacion`) y entidad (`Usuario`, `Invitacion`). El del grupo se conserva (cubre toda la aplicación, marcado OK) y sus tres diferencias con el código quedan explicadas en `docs/ANALISIS_UMBook.md` §3.1 |
| A-02 | ✅ | `2_Diagrama de Paquetes.png` rehecho con los paquetes del grupo: Invitación en *Gestión de Usuarios*, Iniciar Sesión agregado, Solicitud de amistad en un solo paquete, los 24 códigos, más *Administración* y *Correo* (sin ciclos). El diagrama de casos de uso usa los mismos paquetes. El original está en `_version_anterior/` |
| A-03 | ✅ | `3_Diagramas de Colaboración/CU0010 - Invitación a la aplicación.png`: 11 mensajes numerados, entidad `Invitacion` (M-1), servidor de correo como actor externo |
| A-04 | ✅ | Para los tres casos implementados mandan las colaboraciones de `3_Diagramas de Colaboración/`. El `.docx` del grupo lleva una nota que lo dice, y las diferencias están en `ANALISIS_UMBook.md` §5.4 |
| A-05 | ✅ | Las tres colaboraciones se dibujan con los íconos del Proceso Unificado (interfaz, control, entidad) y mensajes numerados, con `docs/generar_colaboraciones.py`. CU0001 y CU0006 regeneradas con los actores de la lista ("Usuario Registrado", "Usuario No Registrado") y "email" como en las fichas |
| A-06 | ✅ | Colaboraciones de CU0011 a CU0013 movidas a `_version_anterior/` |

**Etapa 3, observación por observación:**

| # | Estado | Cómo se resolvió |
|---|---|---|
| D-03 | ✅ | Nuevo `3_Diagramas de Clases/Diagrama de clases de diseño.png`, generado desde `diseno-clases.md` y hecho a partir del código actual. Tiene cinco paquetes: presentación y servicios de Angular, controladores Flask (Blueprints, esquemas marshmallow), servicios y persistencia. Marca los patrones **Singleton** (`NotificationService`), **DAO** (`UserDAO`, `InvitationDAO`) y **Decorator** (`@token_required`), y relaciona cada clase con CU0001, CU0006 y CU0010. El integral de amistad y los de State y Observer + Singleton pasan a `_version_anterior/`; `DISEÑO_UMBook.md` §4 deja de regenerar el diagrama viejo |
| D-01 | ✅ | `1_Diagrama de Despliegue.png` (y `.svg`) generado con `docs/generar_despliegue_subsistemas.py`, con la forma del original del grupo (nodos en 3D y componentes). Nodos: Equipo local (127.0.0.1) con Cliente Web (navegador, SPA Angular 22), Servidor Frontend (`ng serve` :4200) y Servidor Backend (Flask :5000 con SQLite `instance/umbook.db`); Servidor de Correo (Gmail, SMTP + TLS :587) externo. HTTP, no HTTPS (RNF-10). El original pasa a `_version_anterior/` |
| D-02 | ✅ | `2_Diagrama de Subsistemas.png` (y `.svg`), mismo script y la misma forma que el original (cuatro capas). Aplicación Específica = los seis paquetes de Análisis, con Gestión de Usuarios «implementado»; Aplicación General: Autenticación y Seguridad, Gestión de Correos (Singleton), Persistencia (DAO) y Validación de Datos; Capa Intermedia: Flask, extensiones, marshmallow y Angular; Software del Sistema: Python, Node.js, SQLite, navegador, HTTP y SMTP/TLS. Sin Spring, Android/iOS, JDBC, Gestión de Sesiones ni Auditoría. El original pasa a `_version_anterior/` |
| D-04 | ✅ | Una secuencia por caso en `4_Diagramas de Secuencia/`: CU0001 y CU0006 rehechas y CU0010 nueva (`invitacion-secuencia.md`), con los nombres del código (`AuthService.authenticate` / `register_user`, `UserDAO`, `InvitationService`, tabla `users`, respuestas con `msg` y `access_token`) y los cursos alternativos de las fichas (ca 4.1, 5.1, 6.1) más la sesión vencida. Estética de la compañera (Mermaid `redux-color`, numeradas). Corrigen I-01 a I-03 dentro de Diseño. `Diagrama_Secuencia.pdf` del grupo se conserva para los casos no implementados; su Registrar Usuario queda reemplazado. Las de amistad pasan a `_version_anterior/` |
| D-05 | ✅ | `5_Diagramas de Estado/Diagramas de Estado.png` (`docs/generar_estados.py`, explicado en `estados.md`), con la forma del PDF del grupo: **Invitación** (pendiente → enviada / fallida, M-1) y **Sesión del usuario** en el frontend (sin sesión → sesión iniciada → token vencido a los 15 minutos → sin sesión ante un 401). El PDF del grupo y `amistad-estados.md` pasan a `_version_anterior/` |
| D-06 | ✅ | `Diseño de Arquitectura - UMBook.docx` lleva al final la sección **"Estado de la implementación (26/11/2026)"**: una tabla con cada elemento de la propuesta (capas, mecanismos, patrones, clases, despliegue y subsistemas) marcado como implementado, con otro nombre, agregado, parcial o no implementado, y dónde está en el código. El título "Controladores REST (Spring @RestController)" pasa a "(Flask Blueprints)". El `.odt` se regeneró desde el `.docx`; los originales están en `_version_anterior/` |
| D-07 | ✅ | `7_Implementacion.docx` enlaza a `github.com/MaguiMaluff/final-software` (commit `fe825751`), nombra los tres casos implementados y remite a `4. Implementacion/codigo/` y a su `README.md`. Una nota aclara que el enlace anterior era de otro repositorio |
| D-08 | ✅ | `docs/DISEÑO_UMBook.md` 2.0: capas, estructura del código (backend y frontend), endpoints, mecanismos con los RNF vigentes (RNF-09, 16 a 25), patrones Singleton, DAO y Decorator, diferencias con la propuesta y hallazgos nuevos H6 a H11 (token vencido en `AuthGuard`, SMTP sin timeout, registro simultáneo, convenciones de `AuthService`, URL fija del backend, sin migraciones). `3. Diseño/README.md` 2.0 sin el aviso de desactualizado. La versión de amistad del documento pasa a `_version_anterior/docs/` |

`2_Lista de Actores y CU.docx` lleva ahora el código de cada caso de uso y los cinco casos del diagrama del grupo que no estaban en la lista (CU0019 a CU0022 y CU0024).

**Etapa 4, observación por observación:**

| # | Estado | Cómo se resolvió |
|---|---|---|
| I-01 a I-03 | ✅ | Los diagramas de la compañera se conservan tal cual (son su trabajo). `4. Implementacion/README.md` anota, diagrama por diagrama, en qué difieren del código, y remite a las secuencias corregidas de `3. Diseño/4_Diagramas de Secuencia/` (D-04), que tienen su misma estética |
| I-04 | ✅ | Igual criterio para sus fichas: el README anota las diferencias (rnf inexistentes, títulos copiados o sin completar, cursos alternativos mal anclados, precondición de CU0010) y remite a las fichas corregidas de `1. Requerimientos/4_Casos de Uso/` |
| I-05 | ✅ | "Límites conocidos" de `codigo/README.md` suma: sin HTTPS (RNF-10), frontend sin pruebas automáticas y los hallazgos H6 a H11 de `DISEÑO_UMBook.md` §9 |
| I-06 | ✅ | `proyecto.md`, `backend.md`, `frontend.md`, `construccion.md` y `prompt-construccion.md` pasan a `_version_anterior/docs/`: describían la implementación anterior, y lo vigente ya está en `4. Implementacion/README.md` y `codigo/README.md`. `00_INDICE.md` 2.0 actualizado |

**Etapa 5, observación por observación:**

| # | Estado | Cómo se resolvió |
|---|---|---|
| P-01 | ✅ | `PRUEBAS_UMBook.md` 2.0: casos y procedimientos de CU0001, CU0006 y **CU0010** (CP 0010.1 a 0010.9, PR 0010), con los cursos alternativos de las fichas. Los de amistad pasan a `_version_anterior/docs/` |
| P-02 | ✅ | Cada caso cita las pruebas actuales por nombre: las 36 funciones del backend (42 pruebas, contando los parámetros) y las 11 pruebas del frontend están citadas. Hoy pasan todas |
| P-03 | ✅ | Token corrupto: se espera **401** (CP SEG.2) |
| P-04 | ✅ | `Modelo_Plan_de_Pruebas.docx` se conserva como modelo del grupo; el plan dice explícitamente que el entregado es `UMBook_Plan_de_Pruebas.docx` y que la herramienta es pytest |
| P-05 | ✅ | Bloque "Transversal — Seguridad y configuración" (CP SEG.1 a SEG.6) trazado a `test_seguridad.py` y a las pruebas de token de `test_invite.py` |

Entregables regenerados con `docs/generar_entregables.py pruebas`: plan, procedimientos y `3_Casos de Prueba.xlsx` (32 casos). El generador ahora acepta el bloque transversal, toma la versión del `.md` y numera los pasos de cada procedimiento desde 1.

## Cómo leer este documento

| Marca | Significado |
|---|---|
| 🔴 | **Contradice el código** o deja sin resolver algo que la cátedra marcó como FALTA |
| 🟡 | Inconsistencia entre documentos, o detalle que no coincide con el código |
| 🔵 | Mejora sugerida: no está mal, pero suma |

Las observaciones llevan un código por etapa (R = Requerimientos, A = Análisis, D = Diseño, I = Implementación, P = Prueba) para poder citarlas.

**Qué se revisó:** el texto de todos los `.docx`, `.pdf` y `.xlsx` de las carpetas de etapa; las imágenes de los diagramas (modelo de dominio, clases de análisis, paquetes, colaboraciones dentro del `.docx`, despliegue, subsistemas, secuencias y estados del grupo); el código del backend y del frontend, y sus 29 pruebas. **No se revisó** el prototipo de Figma: son enlaces externos.

---

## 1. Resumen

### Los ítems que la cátedra marcó en la corrección

| Ítem de la corrección | Marca de la cátedra | Estado hoy | Observaciones |
|---|---|---|---|
| Diagrama de casos de uso (uno solo para toda la aplicación) | FALTA | 🔴 **Sigue abierto**: el diagrama general no incluye Invitación, y el de lo implementado fue borrado | R-01, R-02 |
| Listado de requerimientos no funcionales | FALTA | 🔴 **Sigue abierto**: el listado con códigos fue borrado; queda un texto en prosa sin códigos | R-13 |
| Diagrama de clases de diseño (con patrones) | FALTA | ✅ **Resuelto (26/11/2026)**: diagrama del código actual con Singleton, DAO y Decorator (`3_Diagramas de Clases/diseno-clases.md`) | D-03 |
| Procedimientos y casos de prueba | OK, falta completar | 🔴 **Desalineados**: cubren amistad y no tienen ningún caso de CU0010 | P-01, P-02 |
| Implementar una parte | OK | ✅ CU0001, CU0006 y CU0010 implementados, 29 pruebas | — |

### Cantidad de observaciones por etapa

| Etapa | 🔴 | 🟡 | 🔵 | Lo principal |
|---|---|---|---|---|
| 1. Requerimientos | 7 | 5 | 1 | Diagrama de CU sin Invitación; hasta tres fichas distintas por caso de uso; modelo de dominio con `Invitación` que el código no guarda |
| 2. Análisis | 3 | 3 | 0 | Clases de análisis sin estereotipos; colaboración de Invitación con entidades que no existen |
| 3. Diseño | 6 | 2 | 0 | Despliegue y subsistemas en Spring Boot y JDBC; ningún diagrama de clases ni de estados corresponde al código |
| 4. Implementación | 0 | 4 | 2 | Diferencias menores entre los diagramas de la compañera y el código |
| 5. Pruebas | 2 | 2 | 1 | Sin casos de CU0010; citan pruebas automáticas que ya no existen |

### Artefactos que describen la implementación anterior

La implementación anterior (amistad y notificaciones: CU0011, CU0012 y CU0013) **ya no está en el código**, pero sus artefactos siguen en las carpetas de etapa como si estuvieran implementados:

| Etapa | Artefactos |
|---|---|
| 1. Requerimientos | `4_Casos de Uso/CU0011_Solicitar_Amistad.docx`, `CU0012_Aceptar_Rechazar_Solicitud.docx`, `CU0013_Notificar_Solicitud_Recibida.docx` |
| 2. Análisis | `3_Diagramas de Colaboración/CU0011 …`, `CU0012 …`, `CU0013 ….png` |
| 3. Diseño | `3_Diagramas de Clases/` (integral, State, Observer y Singleton, y sus `.md`) · `4_Diagramas de Secuencia/CU0011 …`, `CU0012 …`, `CU0013 ….png` y sus `.md` · `5_Diagramas de Estado/amistad-estados.md` |
| 5. Pruebas | Plan, procedimientos y casos (generados desde `docs/PRUEBAS_UMBook.md`) |
| `docs/` | Todos los documentos de etapa (llevan un aviso de desactualizados) |

---

## 2. Etapa 1 — Requerimientos (`1. Requerimientos/`)

| # | Artefacto | Observación | Qué hace el código | Propuesta |
|---|---|---|---|---|
| R-01 🔴 | `3_Diagrama de Casos de Uso/0-CU_General.pdf` | **No incluye "Invitación a la aplicación"**, uno de los tres casos implementados. Tampoco lleva códigos. Es el diagrama único que pidió la cátedra. | CU0010 está implementado (`POST /invite`) | Agregar "Invitación a la aplicación" al paquete *Cuenta* y rotular los casos con su código |
| R-02 🔴 | `3_Diagrama de Casos de Uso/` | `Diagrama de Casos de Uso - Implementados.png` fue borrado (además mostraba CU0011–CU0013). **Hoy ningún diagrama muestra los tres casos implementados** con sus códigos. | — | Resolverlo con R-01 (un solo diagrama, con códigos y los implementados marcados) |
| R-03 🟡 | Varios | Los **actores tienen nombres distintos** según el artefacto: la lista dice *Usuario No Registrado / Registrado / Autenticado / Administrador / Sistema*; el diagrama general, *Visitante / Usuario / Admin / Temporizador*; las fichas generadas, *Visitante / Visitante registrado*; las de la compañera, *Usuario no registrado / Usuario Registrado / Usuario autenticado*. | — | Usar en todos los artefactos los nombres de `2_Lista de Actores y CU.docx` |
| R-04 🔴 | `1_Modelo de Dominio/` | Hay una entidad **`Invitación` (id, emailInvitado, fecha) que el código no guarda**: la invitación solo se manda por correo. `Usuario` tiene `fechaNacimiento` (no existe en el código) y no tiene contraseña. | `User`: id, name, email, password_hash, created_at. No hay tabla de invitaciones | Mejora de código M-1 (guardar las invitaciones), o aclarar en el modelo que `Invitación` no se persiste en esta versión |
| R-05 🔴 | `4_Casos de Uso/` y `4. Implementacion/1_Casos de Uso/` | **Hasta tres fichas del mismo caso de uso, con contenido distinto.** CU0001: la generada y la de la compañera. CU0006: la del grupo (`CU0006.docx`, Alexis Martin Yassuff), la generada y la de la compañera; la del grupo dice en el paso 7 "redirige al inicio de sesión **o lo loguea automáticamente**". CU0010: la del grupo (`CU0010.docx`, Juan Pablo Samsó) y la de la compañera; difieren en rnf 2.2 (**2 s** contra **5 s**) y solo la del grupo tiene autor. | Registro → redirige a `/login`, sin login automático | Decidir **una ficha oficial por caso de uso** y dejar las otras como antecedentes |
| R-06 🔴 | Fichas de CU0010 (las dos) | **La descripción dice que el correo lleva "enlace de registro"**: el correo implementado no tiene enlace. **La precondición es "Ninguna"**, pero el actor es un usuario autenticado y el endpoint exige sesión. ca 1.1 cuelga del paso 1, pero valida el formato (paso 4). ca 2.1 cuelga del paso 2, pero el envío es el paso 5, y salta de 2.1.1 a 2.1.3. ca 2.1 dice "recibe notificación de fallo de entrega": el sistema solo detecta errores al enviar, no rebotes posteriores. | `POST /invite` exige JWT; si el envío falla responde 500 con "No se pudo enviar la invitación. Intentá de nuevo." | Mejora de código M-2 (enlace de registro en el correo). En la ficha: precondición "sesión iniciada (CU0001)", ca 4.1 y ca 5.1 bien anclados, numeración corregida |
| R-07 🟡 | Ficha CU0001 de la compañera (`CU001-login.docx.pdf`) | Los pasos citan **{rnf 4.1} y {rnf 5.1}, que no existen** (la tabla tiene rnf 1.1, rnf 1.2 y una fila sin código). **ca 5.1 se titula "Email ya registrado"** pero describe credenciales incorrectas (título copiado de CU0006). rnf 1.1 exige **HTTPS**, que no está implementado. Ob 1 dice que el token se guarda "de forma segura (LocalStorage)": `localStorage` es accesible desde JavaScript, así que no es almacenamiento seguro. El archivo dice "CU001" y el código es CU0001. Error de tipeo "JWTnpara". | HTTP local; token en `localStorage` | Corregir referencias y título; aclarar que HTTPS queda para producción y que `localStorage` es una decisión aceptada, no "segura" |
| R-08 🟡 | Fichas CU0006 del grupo y de la compañera | Título **"CASO DE USO CU0006 – NOMBRE CASO DE USO"** (plantilla sin completar). "Contraseña segura" no está definida. ca 3.1 cuelga del paso 3, pero la validación es el paso 5. | Contraseña de al menos 8 caracteres | Completar el título y definir "mínimo 8 caracteres" |
| R-09 🟡 | Fichas generadas CU0001 y CU0006 (`docs/ESPECIFICACIONES_…`) | CU0001 Ob 1.1 dice que la sesión se cierra ante **401 o 422**. CU0006 paso 4 dice nombre de **1 a 120** caracteres. Ob 1.2 remite a `docs/construccion.md`, que describe la implementación anterior. La documentación anexa apunta a los diagramas de `2. Análisis` y `3. Diseño`, no a los de la compañera. | El backend responde siempre 401; nombre de 1 a 128 caracteres | Actualizar si se decide que las generadas son las oficiales (ver R-05) |
| R-10 🔴 | `4_Casos de Uso/CU0011_…`, `CU0012_…`, `CU0013_…` | **Fichas de casos que ya no están implementados**, presentados como implementados. | No existen | Retirarlas o marcarlas como "implementación anterior" |
| R-11 🟡 | `docs/CATALOGO_CASOS_DE_USO_UMBook.md` | El choque (1) dice que `CU0006.docx` es una **"plantilla vacía"**: es la **ficha completa de Registrar Usuario** de Alexis Martin Yassuff (solo le falta el título). No es un choque, es el mismo caso. Además el catálogo no lista CU0010 como implementado. | — | Corregir el choque (1) y agregar CU0010 |
| R-12 🔴 | `5_Requisitos No Funcionales/` | La cátedra marcó el listado **FALTA**. `UMBook_RNF.docx` (listado con códigos RNF-01 a RNF-18) **fue borrado**. Queda `Requisitos No Funcionales.docx` del grupo, **en prosa y sin códigos**, así que las fichas no pueden referenciarlo. Ese texto pide HTTPS, 1000 usuarios simultáneos y 99,5 % de disponibilidad, que no se pueden verificar con el servidor de desarrollo. | HTTP local; servidor de desarrollo | Volver a tener un listado **con códigos** (actualizado a CU0001, CU0006 y CU0010) y marcar qué se cumple |
| R-13 🔵 | `6_Prototipo de Interfaces/` | Cuatro enlaces de Figma ("Casos 1, 2 y 3", "4, 5 y 6"…) sin decir a qué códigos de caso de uso corresponden. No se pudo verificar si coinciden con las pantallas actuales (tema "Índigo"). | Login, registro, inicio e invitar | Indicar qué prototipo corresponde a CU0001, CU0006 y CU0010 |

---

## 3. Etapa 2 — Análisis (`2. Análisis/`)

| # | Artefacto | Observación | Qué hace el código | Propuesta |
|---|---|---|---|---|
| A-01 🔴 | `1_Diagrama de Clases de Análisis.png` | **No usa los estereotipos de análisis** (interfaz, control y entidad): es un diagrama de dominio con métodos. `Usuario` tiene `apellido`, `usuario` y `contraseña`. **`invitarAmigo(usuario: Usuario)` recibe un `Usuario`**, pero el invitado todavía no tiene cuenta: es un correo. **No hay operación de iniciar sesión.** No aparece la clase `Invitación` que sí está en el modelo de dominio (R-04). | `User`: name, email, password_hash. La invitación recibe un correo | Agregar las clases de análisis de los tres casos implementados con su estereotipo: `PantallaLogin`, `PantallaRegistro` y `PantallaInvitar` (interfaz); `ControlAutenticacion` y `ControlInvitacion` (control); `Usuario` (entidad) |
| A-02 🟡 | `2_Diagrama de Paquetes.png` | *Gestión_de_Usuarios* no tiene Iniciar Sesión. **Invitación a la Aplicación está en *Notificaciones***, pero las dos fichas de CU0010 dicen paquete "Gestión de Usuarios". Solicitud de Amistad aparece en dos paquetes. | — | Unificar el paquete de CU0010 entre fichas y diagrama, y agregar Iniciar Sesión |
| A-03 🔴 | Colaboración "Invitación a la Aplicación" (dentro de `4_Diagrama de paquetes y colaboracion.docx`) | Está **solo dentro del `.docx`**, no en `3_Diagramas de Colaboración/`. Muestra "Registrar Invitación" sobre una entidad `Invitación` y "Enviar Notificación" sobre una entidad `Notificación`, **que el código no tiene**. El actor "Selecciona Amigo", cuando en realidad escribe un correo. **Los mensajes no están numerados**, y en un diagrama de colaboración el orden lo da la numeración. | Interfaz → controller → `NotificationService` → servidor de correo | Rehacerlo numerado para CU0010 (o aplicar M-1 si se decide guardar las invitaciones) y guardarlo en `3_Diagramas de Colaboración/` |
| A-04 🟡 | Colaboración "Registrar Usuario" del grupo (dentro del `.docx`) | **Estereotipos invertidos**: "Gestor Usuario" está dibujado como entidad y "Usuario" como control. "IU Registro" no tiene estereotipo de interfaz, **el actor no está conectado** a nada y los mensajes no están numerados. Además hay otra versión generada de este caso en `3_Diagramas de Colaboración/`. | — | Quedarse con una sola versión (la generada coincide con el código) |
| A-05 🟡 | `3_Diagramas de Colaboración/CU0001 …` y `CU0006 ….png` | **Coinciden con el código** (interfaz → control de autenticación → entidad Usuario, numerados). Solo hay que tener en cuenta que el grupo no tiene una colaboración de Iniciar Sesión, así que esta es la única. | — | Mantener |
| A-06 🔴 | `3_Diagramas de Colaboración/CU0011 …`, `CU0012 …`, `CU0013 ….png` | Casos que **ya no están implementados**. **No hay colaboración de CU0010** en esta carpeta. | — | Retirar los de amistad y agregar el de CU0010 (A-03) |

---

## 4. Etapa 3 — Diseño (`3. Diseño/`)

| # | Artefacto | Observación | Qué hace el código | Propuesta |
|---|---|---|---|---|
| D-01 🔴 | `1_Diagrama de Despliegue.png` | Muestra **Spring Boot**, **JDBC**, **PostgreSQL/MySQL** y **HTTPS**. Falta el nodo del frontend Angular. | Flask (Python) con SQLAlchemy sobre **SQLite**; HTTP local; Angular servido en `:4200`; Gmail por SMTP con TLS | Rehacerlo: navegador (SPA Angular) → HTTP/JSON → Flask `:5000` → SQLite; Flask → SMTP/TLS → Gmail |
| D-02 🔴 | `2_Diagrama de Subsistemas.png` | "Spring Boot Framework", "Android/iOS" y "Drivers JDBC" **no aplican**. "Gestión de Sesiones" y "Auditoría y Logs" no existen como subsistemas. | Flask, Flask-JWT-Extended, Flask-Mail, SQLAlchemy | Reemplazar la capa intermedia y el software del sistema por lo que se usa |
| D-03 🔴 | `3_Diagramas de Clases/` | **La cátedra lo marcó FALTA y sigue sin resolverse para el código actual.** `Diagrama de clases de diseño.png` y los diagramas de State y Observer describen la implementación anterior (`AmistadService`, `SolicitudAmistad`, State, Observer). **No hay ningún diagrama de clases del código actual.** | `User`, `UserDAO`, `AuthService`, `NotificationService` «Singleton», blueprints `auth` e `invite`, `@token_required`; en el frontend, cuatro componentes, dos servicios, guard e interceptor | Hacer el diagrama de clases de diseño del código actual, marcando los patrones: **Singleton** (`NotificationService`), DAO (`UserDAO`) y el decorador `@token_required` |
| D-04 🔴 | `4_Diagramas de Secuencia/` | `Diagrama_Secuencia.pdf` del grupo **no tiene Iniciar Sesión ni Invitación**. Su "Registrar Usuario" pide `apellido` y `usuario`, pasa por un `UsuarioService`, no controla el correo duplicado y no aplica hash: no coincide con el código. Las secuencias generadas de CU0001 y CU0006 tienen la estructura correcta pero **nombres viejos** (`autenticar`/`registrar`, `UserDao`, tabla `usuarios`, claves `error`/`token`, excepciones). Las de la compañera, que son las que se usan, están en `4. Implementacion/`, no en Diseño. **Hoy conviven tres versiones de Registrar Usuario y dos de Iniciar Sesión.** | `AuthService.register_user` / `authenticate`, `UserDAO`, tabla `users`, respuestas con `msg` y `access_token` | Una sola secuencia por caso en `3. Diseño/4_Diagramas de Secuencia/`: las de la compañera (corrigiendo el login, ver I-01) o las generadas con los nombres actuales |
| D-05 🔴 | `5_Diagramas de Estado/` | `Diagrama_de_Estado.pdf` modela **Solicitud de Amistad** con los estados Creado → Editado → Eliminado (`editar()`, `eliminar()`), que no corresponden a una solicitud y contradicen el modelo de dominio (pendiente/aceptada/rechazada). Modela **Usuario** (Registrado → Activo → Suspendido → Deshabilitado) y **Notificación** (Creada → Enviada → Leída). **Ninguno existe en el código actual.** `amistad-estados.md` es de la implementación anterior. | El código no tiene estados: ni de usuario, ni de invitación, ni de notificación | Hacer un diagrama de estados de algo que exista: la **sesión** en el frontend (sin sesión → autenticado → sesión vencida), o la **Invitación** (pendiente → enviada / fallida) si se aplica M-1 |
| D-06 🟡 | `6_Propuesta de Arquitectura/` | Se cumple: capas, Flask con Blueprints, marshmallow, JWT, Flask-Mail y **Singleton** del notificador. **No se cumple:** Observer, Composite, Factory Method (que la propuesta usaba "para Invitación") y Strategy; `JwtTokenProvider`, `SecurityConfig` y `AuthFilter`; `UsuarioService`; migraciones con Alembic (Flask-Migrate está configurado pero no hay migraciones); manejo global de errores; Android/iOS y JDBC. El texto todavía dice "Spring @RestController". | Un decorador `@token_required`, `AuthService`, sin carpeta `migrations/` ni `errorhandler` | Agregar al documento qué se implementó de la propuesta y qué no (como hacía `DISEÑO_UMBook.md` §8) |
| D-07 🔴 | `7_Implementacion.docx` | Solo tiene un enlace a **`github.com/MaguiMaluff/implementacion_login_UMBook.git`**, que es **otro repositorio**. La implementación usada es `MaguiMaluff/final-software` (commit `fe825751`). | — | Corregir el enlace o remitir a `4. Implementacion/README.md` |
| D-08 🟡 | `3. Diseño/README.md` y `docs/DISEÑO_UMBook.md` | Describen la implementación anterior (llevan el aviso). | — | Actualizar junto con D-03, D-04 y D-05 |

---

## 5. Etapa 4 — Implementación (`4. Implementacion/`)

El código coincide con sus propios documentos en lo esencial: tres casos de uso, mensajes de las fichas, 409 para el correo duplicado, 200 en la invitación y redirección a la pantalla principal. Las diferencias son menores.

| # | Artefacto | Observación | Qué hace el código | Propuesta |
|---|---|---|---|---|
| I-01 🟡 | `2_Diagramas de Secuencia/caso1-login.png` | `check_password_hash` está **dentro de la rama "Credenciales válidas"**, es decir, después de decidir que lo eran. El token lo crea `AuthService` y el método se llama `login`; el DAO se llama `UsuarioDAO`. *(Ya anotado en `4. Implementacion/README.md`.)* | La clave se verifica **antes** de decidir (`AuthService.authenticate`); el token lo crea el controller; `UserDAO` | Si se corrige el diagrama, mover la verificación antes del `alt` |
| I-02 🟡 | `2_Diagramas de Secuencia/caso6-registro.png` | `UsuarioDAO`; el mensaje final dice "Registro Exitoso". No muestra el camino de datos inválidos (400). | `UserDAO`; "Cuenta creada con éxito. Ya podés iniciar sesión."; 400 si faltan datos o la clave es corta | Ajustar nombres y agregar el 400 |
| I-03 🟡 | `2_Diagramas de Secuencia/caso10-invitacion.png` | Llama `getInstance().enviar_invitacion(email_invitado)` y anota **"Simula envío SMTP"**. La respuesta tiene la clave `message`. **No tiene caminos alternativos** (sin sesión, correo inválido, fallo del envío). | `NotificationService().send_invitation(email, inviter_name)`; **envía de verdad** salvo con `MAIL_SUPPRESS_SEND=true`; responde `{msg}`; 401, 400 y 500 | Ajustar nombres y agregar los alternativos de la ficha (ca 1.1 y ca 2.1) |
| I-04 🟡 | `1_Casos de Uso/` | Las fichas de la compañera tienen los problemas de R-06, R-07 y R-08. | — | Ver Requerimientos |
| I-05 🔵 | Código | Sin límite de invitaciones por usuario; sin HTTPS; el frontend no tiene pruebas automáticas. *(Anotados en `codigo/README.md`, "Límites conocidos".)* | — | Dejarlos como límites declarados |
| I-06 🔵 | `docs/backend.md`, `docs/frontend.md`, `docs/construccion.md`, `docs/proyecto.md` | Describen la implementación anterior (llevan el aviso). La fuente actual es `4. Implementacion/README.md` y `codigo/README.md`. | — | Actualizarlos o archivarlos |

---

## 6. Etapa 5 — Prueba (`5. Pruebas/`)

| # | Artefacto | Observación | Qué hace el código | Propuesta |
|---|---|---|---|---|
| P-01 🔴 | Plan, procedimientos y casos (`1_`, `2_`, `3_`) | Cubren CU0001, CU0006, CU0011, CU0012 y CU0013. **No hay ningún caso ni procedimiento de CU0010.** Es justo lo que la cátedra pidió completar. | CU0010 tiene 8 pruebas automáticas en `test_invite.py` | Escribir los casos y el procedimiento de CU0010 y quitar los de amistad |
| P-02 🔴 | `3_Casos de Prueba.xlsx` y plan | Los casos citan **26 pruebas automáticas por nombre y solo una existe hoy** (`test_token_vencido_devuelve_401`). El plan dice **39** pruebas; hoy son **29**. | `test_auth.py` (10), `test_invite.py` (8), `test_seguridad.py` (11) | Volver a trazar cada caso a las pruebas actuales |
| P-03 🟡 | Casos de CU0001 | CP 0001.7 espera **422** para un token corrupto. | Responde **401** | Actualizar el resultado esperado |
| P-04 🟡 | `1_Plan de Pruebas/Modelo_Plan_de_Pruebas.docx` (grupo) | Cubre CU 002, 003, 004, 005 y 007, **ninguno implementado**, y **no incluye login, registro ni invitación**. Nombra **JUnit** como herramienta, cuando el proyecto es Python y usa pytest. Usa códigos que chocan con el catálogo ("Enviar solicitud" = CU 005, pero CU0005 = Buscar usuarios). | pytest | Conservarlo como modelo del grupo, pero que el plan entregado sea el propio |
| P-05 🔵 | — | Las 11 pruebas de seguridad (`test_seguridad.py`) no tienen caso de prueba documentado. | — | Agregar casos "de seguridad" trazados a esas pruebas: suman en la defensa |

---

## 7. Propuestas de mejora para que sea uno a uno

Ordenadas por impacto en la corrección. **Ninguna está aplicada**: se aplican las que se decidan.

### Cambios de código (el código se acerca a lo que ya dicen los documentos del grupo)

| # | Mejora | Resuelve | Esfuerzo |
|---|---|---|---|
| M-1 | **Guardar las invitaciones**: entidad `Invitacion` (id, email del invitado, fecha, quién invita, estado enviada/fallida), con su DAO y sus pruebas | R-04, A-03 y la entidad del modelo de dominio; además da un diagrama de estados real (D-05) | Bajo |
| M-2 | **Agregar el enlace de registro al correo** de invitación (`http://localhost:4200/register`) | R-06 (la descripción de CU0010 dice "con enlace de registro") | Muy bajo |

### Cambios de documentos

| # | Mejora | Resuelve |
|---|---|---|
| M-3 | Diagrama de casos de uso único con Invitación y los códigos, marcando los implementados | R-01, R-02 (**FALTA** de la cátedra) |
| M-4 | Diagrama de clases de diseño del código actual, con Singleton, DAO y el decorador marcados | D-03 (**FALTA** de la cátedra) |
| M-5 | Listado de RNF con códigos, actualizado a los tres casos | R-12 (**FALTA** de la cátedra) |
| M-6 | Casos, procedimientos y plan de prueba con CU0010, trazados a las 29 pruebas | P-01, P-02, P-03 ("falta completar") |
| M-7 | Despliegue y subsistemas con Flask, SQLite y Angular | D-01, D-02 |
| M-8 | Una sola secuencia por caso de uso dentro de `3. Diseño`, con los nombres del código | D-04, I-01, I-02, I-03 |
| M-9 | Diagrama de estados de algo que exista (sesión, o Invitación si se aplica M-1) | D-05 |
| M-10 | Clases de análisis con estereotipos y colaboración numerada de CU0010 | A-01, A-03, A-06 |
| M-11 | Una ficha oficial por caso de uso, con los actores de la lista | R-03, R-05, R-06, R-07, R-08, R-09 |
| M-12 | Retirar o marcar como "implementación anterior" todo lo de CU0011 a CU0013 | R-10, A-06, D-03, D-04 y los avisos de `docs/` |
| M-13 | Corregir el enlace de `7_Implementacion.docx` y el catálogo | D-07, R-11 |

---

## 8. Decisiones pendientes

Estas no se pueden resolver solo con el código; conviene decidirlas antes de aplicar las mejoras:

1. **¿Qué ficha manda en cada caso de uso?** La del grupo, la generada o la de la compañera (R-05). De esto depende qué se corrige.
2. **¿Se guardan las invitaciones (M-1)?** Si sí, el modelo de dominio y la colaboración del grupo pasan a ser correctos tal como están. Si no, hay que corregirlos.
3. **¿Qué se hace con lo de amistad (CU0011 a CU0013)?** Borrarlo, moverlo a una carpeta de "versión anterior" o dejarlo marcado.
4. **`UMBook_RNF.docx` y `Diagrama de Casos de Uso - Implementados.png` fueron borrados.** ¿Se quieren de vuelta (actualizados) o se reemplazan por versiones del grupo? Los dos responden a ítems que la cátedra marcó FALTA.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.3 | 26/11/2026 | Gestión del proyecto | Etapa 3 en curso: D-03 resuelto con el diagrama de clases de diseño del código actual; D-01 y D-02 con despliegue y subsistemas rehechos con la forma de los del grupo; D-04 y D-05 con secuencias y estados del código actual; D-06 a D-08 con la propuesta, `7_Implementacion.docx` y el documento de diseño realineados. Etapa 3 corregida |
| 1.4 | 26/11/2026 | Gestión del proyecto | Etapas 4 y 5 corregidas: diferencias de los documentos de la compañera anotadas, documentos técnicos viejos archivados, pruebas rehechas para CU0001, CU0006, CU0010 y seguridad. Las cinco etapas quedan alineadas con el código |
| 1.5 | 26/11/2026 | Gestión del proyecto | H7 y H8 corregidos en el código con sus pruebas (37); casos de prueba CP 0006.7 y CP 0010.10 |
| 1.6 | 26/11/2026 | Gestión del proyecto | H6, H9, H10 y H11 corregidos con sus pruebas (42 del backend, 11 del frontend); casos CP SEG.7 a SEG.9 |
