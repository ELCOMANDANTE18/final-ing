# Diseño — diagramas

**Versión:** 2.0 · **Última modificación:** 26/11/2026 · **Etapa:** Diseño

Todos los artefactos de esta carpeta corresponden a la implementación actual: **CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación** (`4. Implementacion/codigo/`). Lo que describía la implementación anterior (amistad) y los originales reemplazados del grupo están en `_version_anterior/3. Diseño/`.

Índice de los artefactos de la etapa de Diseño, **numerados con el orden de la corrección de la cátedra** (`correccion_catedra_grupo3.pdf`). La tabla completa de todas las etapas está en [`docs/00_INDICE.md`](../docs/00_INDICE.md) §4.

Los diagramas son **generados**: los de clases y secuencia, desde el Mermaid de su `.md` con `python3 docs/generar_diagramas.py` (Mermaid CLI 12); despliegue y subsistemas con `docs/generar_despliegue_subsistemas.py`, y estados con `docs/generar_estados.py`. Si una imagen y su texto difieren, manda el texto y se regenera la imagen.

El documento de diseño completo (capas, mecanismos, hallazgos y diferencias con la propuesta original) es [`docs/DISEÑO_UMBook.md`](../docs/DISEÑO_UMBook.md). Los códigos de caso de uso están en [`docs/CATALOGO_CASOS_DE_USO_UMBook.md`](../docs/CATALOGO_CASOS_DE_USO_UMBook.md).

## Artefactos

| Nº | Artefacto que pide la cátedra | Archivo o carpeta | Origen |
|---|---|---|---|
| 1 | Diagrama de despliegue | `1_Diagrama de Despliegue.png` | Generado con la forma del original del grupo |
| 2 | Diagrama de subsistemas | `2_Diagrama de Subsistemas.png` | Generado con la forma del original del grupo |
| 3 | Diagrama de clases de diseño (con patrones) | `3_Diagramas de Clases/` | Generado, del código actual |
| 4 | Diagramas de secuencia | `4_Diagramas de Secuencia/` | Generados con la estética de la compañera (CU0001, CU0006, CU0010), más `Diagrama_Secuencia.pdf` del grupo |
| 5 | Diagramas de estados | `5_Diagramas de Estado/` | Generado con la forma del PDF del grupo |
| 6 | Propuesta de arquitectura basada en patrones | `6_Propuesta de Arquitectura/` | Del grupo (`.docx` y `.odt`), con la sección "Estado de la implementación" agregada |
| 7 | *(complementario)* Documento de implementación | `7_Implementacion.docx` | Del grupo, con el enlace corregido |

## 1 y 2 — Despliegue y subsistemas

Los genera [`docs/generar_despliegue_subsistemas.py`](../docs/generar_despliegue_subsistemas.py) (`.svg` y `.png`) con la forma de los diagramas del grupo (PlantUML: nodos en 3D, componentes, paquetes) y el contenido del código actual. La explicación de cada nodo y subsistema está en `docs/DISEÑO_UMBook.md` §5 y §6; los originales del grupo, en `_version_anterior/3. Diseño/`.

## 3 — Diagramas de clases (`3_Diagramas de Clases/`)

| Diagrama | Fuente (`.md`) | Imagen |
|---|---|---|
| Clases de diseño de CU0001, CU0006 y CU0010, con Singleton (`NotificationService`), DAO (`UserDAO`, `InvitationDAO`) y Decorator (`@token_required`) | [`diseno-clases.md`](./3_Diagramas%20de%20Clases/diseno-clases.md) | `Diagrama de clases de diseño.png` |

Es el ítem que la corrección marcó como **FALTA**. Está hecho a partir del código actual: frontend Angular, Blueprints, servicios y persistencia. Los diagramas de clases de la implementación anterior (integral de amistad, State, Observer y Singleton) están en `_version_anterior/3. Diseño/3_Diagramas de Clases/`.

## 4 — Diagramas de secuencia (`4_Diagramas de Secuencia/`)

| Caso de uso | Fuente (`.md`) | Imagen |
|---|---|---|
| CU0001 Iniciar Sesión | [`login-secuencia.md`](./4_Diagramas%20de%20Secuencia/login-secuencia.md) — ca 4.1 (formulario, en el navegador y en el servidor) y ca 5.1 (credenciales); la contraseña se verifica antes de decidir | `CU0001 - Iniciar Sesión.png` |
| CU0006 Registrar Usuario | [`registro-secuencia.md`](./4_Diagramas%20de%20Secuencia/registro-secuencia.md) — ca 5.1 (datos inválidos, 400) y ca 6.1 (email ya registrado, 409) | `CU0006 - Registrar Usuario.png` |
| CU0010 Invitación a la aplicación | [`invitacion-secuencia.md`](./4_Diagramas%20de%20Secuencia/invitacion-secuencia.md) — ca 4.1 (email inválido), ca 5.1 (fallo del correo) y sesión vencida (401); estados de la invitación y Singleton | `CU0010 - Invitación a la aplicación.png` |

Siguen la estética de los diagramas de la compañera (`4. Implementacion/2_Diagramas de Secuencia/`: Mermaid con el tema `redux-color`, mensajes numerados, notas y marcos `alt`), con los nombres del código actual y los cursos alternativos de cada ficha. **Para CU0001, CU0006 y CU0010 mandan estos.** `Diagrama_Secuencia.pdf` es la versión del grupo y cubre casos de uso no implementados (álbum, comentarios, amistad); su "Registrar Usuario" es anterior al código (pide apellido y usuario) y queda reemplazado por el de esta carpeta. Las secuencias de amistad (CU0011 a CU0013) están en `_version_anterior/3. Diseño/4_Diagramas de Secuencia/`.

## 5 — Diagramas de estado (`5_Diagramas de Estado/`)

| Diagrama | Fuente | Imagen |
|---|---|---|
| Invitación (pendiente → enviada / fallida) y Sesión del usuario en el frontend (sin sesión, sesión iniciada, token vencido) | [`estados.md`](./5_Diagramas%20de%20Estado/estados.md) y [`docs/generar_estados.py`](../docs/generar_estados.py) | `Diagramas de Estado.png` (y `.svg`) |

Una lámina con la forma del `Diagrama_de_Estado.pdf` del grupo (título y un diagrama por entidad, estilo PlantUML), con dos diagramas de cosas que existen en el código. El PDF del grupo (Solicitud de Amistad, Usuario y Notificación, sin estados en el código) está en `_version_anterior/3. Diseño/5_Diagramas de Estado/`.

## Observaciones

- La **propuesta de arquitectura** (`6_Propuesta de Arquitectura/`) describe un sistema más grande que el implementado. Su última sección, "Estado de la implementación", compara cada elemento con el código (implementado, con otro nombre, agregado, parcial o no implementado); el resumen está en `docs/DISEÑO_UMBook.md` §8. El `.odt` se regenera desde el `.docx`, sin fuentes incrustadas: el `.docx` trae activada la opción `embedTrueTypeFonts` y, si se convierte tal cual, LibreOffice incrusta unos 20 MB de fuentes del sistema. Para regenerarlo, sacar `<w:embedTrueTypeFonts w:val="1"/>` de `word/settings.xml` en una copia del `.docx` y convertir esa copia con `soffice --headless --convert-to odt`.
- **`7_Implementacion.docx`** enlaza al repositorio de la compañera del que sale el código (`MaguiMaluff/final-software`, commit `fe825751`) y remite a `4. Implementacion/`. Antes enlazaba a otro repositorio.
- El **diagrama de capas** está en Mermaid dentro de `docs/DISEÑO_UMBook.md` §1, pero no se entrega como imagen: la corrección no lo pide.
- No hay diagrama de estados de `Usuario` ni de notificaciones: no tienen estados en el código (ver `estados.md`).

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 16/09/2026 | Diseño | Índice de los diagramas Mermaid |
| 1.1 | 20/11/2026 | Diseño | Se agregan los códigos de CU, los `.png`, los diagramas generales y los enlaces a `docs/DISEÑO_UMBook.md` |
| 1.2 | 25/11/2026 | Diseño | Artefactos numerados con el orden de la corrección de la cátedra; despliegue, subsistemas y estados pasan a la versión del grupo |
| 1.3 | 26/11/2026 | Diseño | Diagrama de clases de diseño del código actual (D-03); los de amistad pasan a `_version_anterior/`. Despliegue y subsistemas generados con el código actual (D-01, D-02). Secuencias de CU0001, CU0006 y CU0010 y lámina de estados (D-04, D-05) |
| 2.0 | 26/11/2026 | Diseño | Realineado con la implementación actual: se quita el aviso de desactualizado; propuesta de arquitectura con su estado de implementación (D-06), enlace de `7_Implementacion.docx` corregido (D-07) |
