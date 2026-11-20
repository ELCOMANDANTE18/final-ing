# UMBook — Red social de gestión de usuarios

Trabajo final de la materia **Ingeniería de Software**.

**Alumno:** Victor Gimenez · **Legajo:** 61.174

UMBook es una aplicación web de gestión de usuarios con tres funcionalidades centrales: **iniciar sesión**, **solicitar, aceptar y rechazar amistad** y **notificar por correo la solicitud de amistad recibida**. El backend es una API REST en Flask y el frontend es una aplicación Angular.

El proyecto se desarrolló siguiendo el **Proceso Unificado**, con sus flujos de trabajo: Requisitos, Análisis, Diseño, Implementación y Prueba.

---

## Alcance de esta entrega

Funcionalidades realizadas (diseñadas, implementadas y probadas):

| Funcionalidad | Patrón de diseño |
|---|---|
| Registrar usuario | — |
| Iniciar sesión | — |
| Solicitar amistad y aceptar / rechazar la solicitud | **State** |
| Notificar solicitud de amistad recibida | **Observer** sobre un `NotificationService` **Singleton** |

Los casos de uso restantes (invitación a la aplicación, búsqueda de usuarios, comentarios, cumpleaños, permisos, etc.) están especificados en `1. Requerimientos/Casos de Uso/` y quedan fuera del alcance de implementación de esta versión. El detalle de qué entra y qué no, y por qué, está en `docs/proyecto.md`.

---

## Dónde está cada cosa

| Carpeta | Qué contiene |
|---|---|
| `enunciado_umbook.pdf` | Enunciado del proyecto de la cátedra |
| `1. Requerimientos/` | Fichas de los casos de uso (`Casos de Uso/`, con las del grupo y las cinco implementadas) · listado de requisitos no funcionales · lista de actores · modelo de dominio · prototipo de interfaces |
| `2. Análisis/` | Diagrama de clases de análisis · diagrama de paquetes · diagramas de colaboración de los cinco casos de uso implementados |
| `3. Diseño/` | Arquitectura y mecanismos · diagramas de capas, de clases integral, de despliegue y de subsistemas · diagramas de secuencia y de estado. Su `README.md` es el índice |
| `4. Implementacion/codigo/` | El código fuente (`backend/` y `frontend/`), con su propio `README.md` |
| `5. Pruebas/` | Plan de pruebas, casos de prueba y procedimientos de prueba |
| `docs/` | Documentación en markdown, con `00_INDICE.md` como punto de entrada |

**Casos de uso y códigos.** Los códigos de los casos de uso implementados (CU0001, CU0006, CU0011, CU0012 y CU0013) y los choques con otras fichas del grupo están en [`docs/CATALOGO_CASOS_DE_USO_UMBook.md`](docs/CATALOGO_CASOS_DE_USO_UMBook.md).

---

## Sobre la carpeta `docs/`

Los entregables de la materia son los archivos **`.docx`, `.pdf`, `.xlsx` y `.png`** que están en las carpetas de etapa. La carpeta `docs/` contiene los textos en markdown de los que salen varios de ellos, y la documentación técnica que acompaña al código.

`docs/00_INDICE.md` es el punto de entrada: dice qué contiene cada documento, en qué versión está y dónde buscar cada cosa. Todos los documentos de `docs/` llevan encabezado de versión y bloque de control.

**Cuando un `.md` y su entregable difieren, manda el `.md`** en los documentos que tienen generador (las fichas de caso de uso, el listado de RNF y los diagramas, con `docs/generar_entregables.py` y `docs/generar_diagramas.py`). En el resto, manda el entregable de la carpeta de etapa.

Las rutas de código que aparecen en `docs/` (por ejemplo `backend/app/...`) son relativas a `4. Implementacion/codigo/`.

---

## Cómo ejecutar el sistema

Las instrucciones completas —dependencias, configuración, datos de demostración y ejecución de las pruebas— están en `4. Implementacion/codigo/README.md`.

En resumen: **Python 3 · Flask · SQLAlchemy · SQLite** en el backend (puerto 5000) y **Angular** en el frontend (puerto 4200).

```bash
cd "4. Implementacion/codigo/backend"
python3 -m venv venv && source venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env          # y completar JWT_SECRET_KEY
python run.py

# en otra terminal
cd "4. Implementacion/codigo/frontend"
npm install
npx ng serve
```

---

## Nota sobre secretos

La clave de firma de los tokens (`JWT_SECRET_KEY`) y las credenciales de correo se leen de un archivo `.env` que **no está en el repositorio**. La plantilla sin valores secretos es `backend/.env.example`. Tampoco se versiona la base de datos (`instance/`).
