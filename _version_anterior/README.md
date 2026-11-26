# Versión anterior — no forma parte de la entrega

Artefactos retirados de las carpetas de etapa durante la corrección del 25/11/2026. Se guardan por si hacen falta como referencia; **no describen la implementación actual** (CU0001, CU0006 y CU0010).

| Carpeta | Qué hay | Por qué se retiró |
|---|---|---|
| `1. Requerimientos/3_Diagrama de Casos de Uso/` | `0-CU_General.pdf` (diagrama general del grupo, sin códigos) y `CU-7-11-23.pdf` | Reemplazados por el diagrama único con códigos `Diagrama de Casos de Uso - UMBook.pdf`. `CU-7-11-23.pdf` usaba los códigos anteriores a la renumeración (hoy CU0014, CU0015 y CU0023) |
| `1. Requerimientos/4_Casos de Uso/` | Fichas CU0011 Solicitar Amistad, CU0012 Aceptar / Rechazar y CU0013 Notificar Solicitud Recibida | Eran de la implementación anterior (amistad), que ya no está en el código |
| `2. Análisis/` | Diagrama de paquetes original del grupo y colaboraciones de CU0011 a CU0013 | El de paquetes se reemplazó por una versión corregida (Invitación en Gestión de Usuarios, Iniciar Sesión, códigos); las colaboraciones eran de la implementación anterior |
| `3. Diseño/` | `1_Diagrama de Despliegue (grupo).png` y `2_Diagrama de Subsistemas (grupo).png` | Mostraban Spring Boot, JDBC, PostgreSQL/MySQL, HTTPS, Android/iOS, y subsistemas que no existen. Reemplazados por versiones con la misma forma y el contenido del código, generadas con `docs/generar_despliegue_subsistemas.py` |
| `3. Diseño/4_Diagramas de Secuencia/` | Secuencias de CU0011, CU0012 y CU0013 y sus fuentes `.md` | Eran de la implementación anterior (amistad) |
| `3. Diseño/5_Diagramas de Estado/` | `Diagrama_de_Estado (grupo).pdf` y `amistad-estados.md` | Modelaban Solicitud de Amistad, Usuario y Notificación, que no tienen estados en el código. Reemplazados por `Diagramas de Estado.png` (Invitación y Sesión) |
| `3. Diseño/6_Propuesta de Arquitectura/` | `Diseño de Arquitectura - UMBook (original del grupo).docx` | Versión sin la sección "Estado de la implementación" y con el título "Spring @RestController". La vigente es la misma con esos dos cambios. El `.odt` original no se guarda: tenía el mismo texto que este `.docx` y pesaba 21 MB por las fuentes incrustadas |
| `3. Diseño/` | `7_Implementacion (anterior).docx` | Enlazaba a `MaguiMaluff/implementacion_login_UMBook`, que es otro repositorio |
| `docs/` | `PRUEBAS_UMBook (amistad).md` | Plan, casos y procedimientos de CU0001, CU0006 y CU0011 a CU0013, trazados a las pruebas de la implementación anterior |
| `docs/` | `proyecto.md`, `backend.md`, `frontend.md`, `construccion.md`, `prompt-construccion.md` | Documentación técnica de la implementación anterior. Lo vigente está en `4. Implementacion/README.md` y `4. Implementacion/codigo/README.md` |
| `docs/` | `DISEÑO_UMBook (amistad).md` | Versión 1.3 del documento de diseño, con las secciones de la implementación de amistad (State, Observer, hallazgos H1 a H5) |
| `3. Diseño/3_Diagramas de Clases/` | Diagrama de clases de diseño integral de amistad, diagramas de los patrones State y Observer + Singleton, y sus fuentes `.md` | Describían `AmistadService`, `SolicitudAmistad` y el Observer, que ya no están en el código. Reemplazados por `3. Diseño/3_Diagramas de Clases/diseno-clases.md` |
| `docs/` | Versiones anteriores del catálogo, de las especificaciones y del listado de RNF | Describían la implementación anterior |

Detalle de cada cambio: `docs/OBSERVACIONES_POR_ETAPA_UMBook.md`, sección "Avance de las correcciones".
