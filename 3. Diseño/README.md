# Diseño — diagramas

**Versión:** 1.1 · **Última modificación:** 20/11/2026 · **Etapa:** Diseño

Índice de los diagramas de la etapa de Diseño. Cada diagrama está **escrito en Mermaid** (en el `.md` indicado) y **dibujado como `.png`** al lado. El `.md` es la fuente: si difieren, manda el `.md` y se regenera la imagen con `python3 docs/generar_diagramas.py`.

El documento de diseño completo (capas, mecanismos, hallazgos y diferencias con la propuesta original) es [`docs/DISEÑO_UMBook.md`](../docs/DISEÑO_UMBook.md). Los códigos de caso de uso están en [`docs/CATALOGO_CASOS_DE_USO_UMBook.md`](../docs/CATALOGO_CASOS_DE_USO_UMBook.md).

## Diagramas generales

Están dentro de `docs/DISEÑO_UMBook.md`:

| Imagen | Diagrama |
|---|---|
| `Diagrama de capas.png` | Arquitectura en capas |
| `Diagrama de clases de diseño.png` | Clases de diseño integral, con State, Observer y Singleton |
| `Diagrama de despliegue.png` | Despliegue |
| `Diagrama de subsistemas.png` | Subsistemas |

## Diagramas de secuencia (`Diagramas de Secuencia/`)

| Caso de uso | Fuente (`.md`) | Imagen |
|---|---|---|
| CU0001 Iniciar Sesión | [`login-secuencia.md`](./Diagramas%20de%20Secuencia/login-secuencia.md) — curso normal y alternativos, con el punto exacto del arreglo del bug de la contraseña | `CU0001 - Iniciar Sesión.png` |
| CU0006 Registrar Usuario | [`registro-secuencia.md`](./Diagramas%20de%20Secuencia/registro-secuencia.md) — correo ya registrado y formato inválido; por qué se redirige a login | `CU0006 - Registrar Usuario.png` |
| CU0011 Solicitar Amistad | [`amistad-secuencia-solicitar.md`](./Diagramas%20de%20Secuencia/amistad-secuencia-solicitar.md) — validaciones y creación de la solicitud | `CU0011 - Solicitar Amistad.png` |
| CU0012 Aceptar / Rechazar | [`amistad-secuencia-aceptar-rechazar.md`](./Diagramas%20de%20Secuencia/amistad-secuencia-aceptar-rechazar.md) — autorización, State y transacción única | `CU0012 - Aceptar - Rechazar Solicitud.png` |
| CU0013 Notificar | [`notificar-secuencia.md`](./Diagramas%20de%20Secuencia/notificar-secuencia.md) — desde el evento hasta el correo | `CU0013 - Notificar Solicitud Recibida.png` |

## Diagramas de estado (`Diagramas de Estado/`)

| Diagrama | Fuente (`.md`) | Imagen |
|---|---|---|
| `SolicitudAmistad`: pendiente, aceptada, rechazada | [`amistad-estados.md`](./Diagramas%20de%20Estado/amistad-estados.md) | `Diagrama de Estados - SolicitudAmistad.png` |

## Diagramas de clases por patrón (`Diagramas de Clases/`)

| Patrón | Fuente (`.md`) | Imagen |
|---|---|---|
| State | [`amistad-clases-state.md`](./Diagramas%20de%20Clases/amistad-clases-state.md) | `Diagrama de clases - Patrón State.png` |
| Observer + Singleton | [`notificar-clases-observer-singleton.md`](./Diagramas%20de%20Clases/notificar-clases-observer-singleton.md) | `Diagrama de clases - Observer y Singleton.png` |

El diagrama integral reúne a los dos en uno solo.

## Faltan

- El **Documento de arquitectura** `Diseño de Arquitectura - UMBook.docx` describe un sistema más grande que el implementado; ver `docs/DISEÑO_UMBook.md` §8.
- No hay diagrama de estados de `Usuario`: no tiene ciclo de vida en esta versión.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 16/09/2026 | Diseño | Índice de los diagramas Mermaid |
| 1.1 | 20/11/2026 | Diseño | Se agregan los códigos de CU, los `.png`, los diagramas generales y los enlaces a `docs/DISEÑO_UMBook.md` |
