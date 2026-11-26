# CATÁLOGO DE CASOS DE USO — UMBook

**Versión:** 2.0 · **Última modificación:** 25/11/2026 · **Etapa:** Requerimientos

Un código por caso de uso, sin repetidos. Es la referencia que comparten la lista de actores y casos de uso (`2_Lista de Actores y CU.docx`), el diagrama único (`3_Diagrama de Casos de Uso/Diagrama de Casos de Uso - UMBook.pdf`) y las fichas (`4_Casos de Uso/`).

## 1. Casos de uso implementados

| Código | Caso de uso | Actor | Fichas en `1. Requerimientos/4_Casos de Uso/` | Ficha de la implementación (`4. Implementacion/1_Casos de Uso/`) |
|---|---|---|---|---|
| CU0001 | Iniciar Sesión | Usuario Registrado | `CU0001_Iniciar_Sesión.docx` (Victor Gimenez) | `CU001-login.docx.pdf` |
| CU0006 | Registrar Usuario | Usuario No Registrado | `CU0006.docx` (Alexis Martin Yassuff) y `CU0006_Registrar_Usuario.docx` (Victor Gimenez, mismo flujo con más detalle) | `CU0006-registro.docx.pdf` |
| CU0010 | Invitación a la aplicación | Usuario Autenticado | `CU0010.docx` (Juan Pablo Samsó) | `CU0010-invitar.docx.pdf` |

**Las tres fichas que usa la implementación tienen su ficha en Requerimientos.** Las de la implementación son copias de las del grupo, con dos diferencias que las fichas de Requerimientos ya resuelven a favor del código:

| Caso | Diferencia | Cómo quedó |
|---|---|---|
| CU0006 | La ficha del grupo decía en el paso 7 "redirige al inicio de sesión **o lo loguea automáticamente**"; la de la implementación, solo "redirige al inicio de sesión" | Redirige al inicio de sesión (Ob 1) |
| CU0010 | rnf 2.2: **2 segundos** en la ficha del grupo, **5 segundos** en la de la implementación | 5 segundos (Ob 3 de `CU0010.docx`) |

Además, las fichas de Requerimientos corrigen errores de numeración que las de la implementación conservan (por ejemplo, ca 1.1 y ca 2.1 de CU0010 pasan a ser ca 4.1 y ca 5.1). Las fichas de la implementación quedan como están: son la entrega original de la compañera.

## 2. Todos los casos de uso

| Código | Caso de uso | Paquete | Actor | Ficha | Estado |
|---|---|---|---|---|---|
| CU0001 | Iniciar Sesión | Gestión de Usuarios | Usuario Registrado | `CU0001_Iniciar_Sesión.docx` | **Implementado** |
| CU0002 | Aceptar / Rechazar solicitud de amistad | Gestión de Relaciones | Usuario Autenticado | `CU0002.docx` (Magdalena Maluff) | — |
| CU0003 | Gestionar usuarios, comentarios y fotos | Administración | Administrador | `CU0003.docx` (Magdalena Maluff) | — |
| CU0004 | Publicar en el Muro | Gestión de Contenido | Usuario Autenticado | `CU0004.docx` (Alexis Martin Yassuff) | — |
| CU0005 | Solicitar Amistad | Gestión de Relaciones | Usuario Autenticado | `CU0005.docx` (Alexis Martin Yassuff) | — |
| CU0006 | Registrar Usuario | Gestión de Usuarios | Usuario No Registrado | `CU0006.docx`, `CU0006_Registrar_Usuario.docx` | **Implementado** |
| CU0007 | Gestionar Álbum | Gestión de Contenido | Usuario Autenticado | `CU0007.docx` (Facundo Mala) | — |
| CU0008 | Gestionar Comentarios | Administración | Administrador | `CU0008.docx` (Facundo Mala) | — |
| CU0009 | Notificación de Cumpleaños | Notificaciones | Sistema | `CU0009.docx` (Facundo Mala) | — |
| CU0010 | Invitación a la aplicación | Gestión de Usuarios | Usuario Autenticado | `CU0010.docx` | **Implementado** |
| CU0011 | Eliminar comentarios | Gestión de Contenido | Usuario Autenticado | `CU0011.docx` (Juan Pablo Samsó) | — |
| CU0012 | Crear grupos de amigos | Gestión de Relaciones | Usuario Autenticado | `CU0012.docx` (Juan Pablo Samsó) | — |
| CU0013 | Hacer publicaciones en la página | Gestión de Contenido | Usuario Autenticado | Sin ficha | — |
| CU0014 | Comentar Publicación | Gestión de Contenido | Usuario Autenticado | `CASO DE USO CU0014 – COMENTAR PUBLICACIÓN.docx` (Victor Gimenez) | — |
| CU0015 | Mostrar usuarios con amigos en común | Gestión de Relaciones | Usuario Autenticado | `CASO DE USO CU0015 – MOSTRAR USUARIOS CON AMIGOS EN COMÚN.docx` (Victor Gimenez) | — |
| CU0016 | Eliminar Amigos | Gestión de Relaciones | Usuario Autenticado | `CU0016 - Eliminar amigos.docx` (Adriano Tisera) | — |
| CU0017 | Gestionar permisos en el sitio | Control de Accesos | Administrador | `CU0017 - Gestión de permisos en el sitio del usuario.docx` (Adriano Tisera) | — |
| CU0018 | Buscar Usuarios | Gestión de Usuarios | Usuario Autenticado | `CU0018 - Buscar usuarios.docx` (Adriano Tisera) | — |
| CU0019 | Modificar Perfil | Gestión de Usuarios | Usuario Autenticado | Sin ficha | — |
| CU0020 | Consultar Página Principal | Gestión de Contenido | Usuario Autenticado | Sin ficha | — |
| CU0021 | Notificar solicitud de amistad recibida | Notificaciones | (incluido por CU0020) | Sin ficha | — |
| CU0022 | Notificar comentario en foto propia | Notificaciones | (incluido por CU0020) | Sin ficha | — |
| CU0023 | Enviar notificación de cumpleaños cercanos por email | Notificaciones | Sistema | `CASO DE USO CU0023 – Envió de Mails para Notificar Cumpleaños Cercanos.docx` (Victor Gimenez) | — |
| CU0024 | Notificar actualización de perfil de amigo | Notificaciones | (incluido por CU0020) | Sin ficha | — |

Los paquetes son los mismos en el diagrama de casos de uso y en el diagrama de paquetes de Análisis (`2. Análisis/2_Diagrama de Paquetes.png`).

Relaciones del diagrama: CU0005 «extend» CU0018 (se solicita amistad desde el resultado de una búsqueda); CU0020 «include» CU0009, CU0021, CU0022 y CU0024. El Administrador es un Usuario Autenticado (generalización).

## 3. Cambios de código aplicados (25/11/2026)

Había cuatro códigos asignados a dos casos distintos. Se renumeró una ficha de cada par a un código libre; **el contenido de las fichas no se tocó**, solo el código, el título y el encabezado.

| Código anterior | Caso | Código nuevo | Archivo |
|---|---|---|---|
| CU0005 | Buscar Usuarios (Tisera) | **CU0018** | `CU0005 - Buscar usuarios.docx` → `CU0018 - Buscar usuarios.docx` |
| CU0007 | Comentar Publicación (Gimenez) | **CU0014** | `CASO DE USO CU0007 – …` → `CASO DE USO CU0014 – …` |
| CU0011 | Mostrar usuarios con amigos en común (Gimenez) | **CU0015** | `CASO DE USO CU0011 – …` → `CASO DE USO CU0015 – …` |
| CU0012 | Eliminar Amigos (Tisera) | **CU0016** | `CU0012 - Eliminar amigos.docx` → `CU0016 - Eliminar amigos.docx` |

Conservan su código CU0005 Solicitar Amistad, CU0007 Gestionar Álbum, CU0011 Eliminar comentarios y CU0012 Crear grupos de amigos.

Otros errores de plantilla corregidos en las fichas:

| Ficha | Error | Corrección |
|---|---|---|
| `CU0005.docx` | Título "Nombre Caso de Uso" | "Solicitar Amistad" |
| `CU0006.docx` | Título "Nombre Caso de Uso" | "Registrar Usuario" |
| `CU0009.docx` | Título "Nombre Caso de Uso" | "Notificación de Cumpleaños" |
| `CU0018 - Buscar usuarios.docx` | Código `CU0001` en la tabla y en el encabezado; encabezado "Registrar Usuario" | CU0018, "Buscar Usuarios" |
| `CU0016 - Eliminar amigos.docx` | Encabezado con código `CU0001` y "Registrar Usuario" | CU0016, "Eliminar Amigos" |
| `CU0017 - Gestión de permisos….docx` | Código `CU0001` en la tabla y en el encabezado; encabezado "Registrar Usuario" | CU0017, "Gestión de permisos en el sitio del usuario" |

Los códigos CU0013 y CU0019 a CU0024 son nuevos: corresponden a casos de uso que figuraban en la lista o en el diagrama del grupo y no tenían código.

## 4. Implementación anterior

La implementación anterior (amistad y notificaciones) usaba CU0011 Solicitar Amistad, CU0012 Aceptar / Rechazar y CU0013 Notificar Solicitud Recibida. Esas fichas, y la versión anterior de este catálogo, están en `_version_anterior/`. Ya no forman parte de la entrega.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 – 1.1 | 20/11/2026 | Requisitos | Catálogo de la implementación anterior. Archivado en `_version_anterior/docs/` |
| 2.0 | 25/11/2026 | Requerimientos | Catálogo completo con un código por caso de uso (CU0001 a CU0024), renumeración de los cuatro códigos repetidos, mapeo con las fichas de la implementación |
