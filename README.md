# UMBook — Red social de gestión de usuarios

Trabajo final de la materia **Ingeniería de Software**.

**Alumno:** Victor Gimenez · **Legajo:** 61.174

UMBook es una aplicación web de gestión de usuarios con tres funcionalidades implementadas: **registrarse**, **iniciar sesión** e **invitar a otra persona por correo**. El backend es una API REST en Flask y el frontend es una aplicación Angular.

El proyecto se desarrolló siguiendo el **Proceso Unificado**, con sus flujos de trabajo: Requisitos, Análisis, Diseño, Implementación y Prueba.

---

## Alcance de esta entrega

La implementación toma como base el proyecto de una compañera del grupo, con su acuerdo: **el mismo código, con los errores de seguridad corregidos y un frontend con diseño nuevo**. Sus fichas de caso de uso y sus diagramas de secuencia viven dentro de `4. Implementacion/`. El detalle de qué se tomó y qué se cambió está en [`4. Implementacion/README.md`](4.%20Implementacion/README.md).

| Caso de uso | Patrón de diseño |
|---|---|
| CU0001 Iniciar Sesión | — |
| CU0006 Registrar Usuario | — |
| CU0010 Invitación a la aplicación | **Singleton** (`NotificationService`) |

Los demás casos de uso del grupo están especificados en `1. Requerimientos/4_Casos de Uso/` y no se implementaron.

> ⚠️ **Pendiente:** varios documentos de las etapas (fichas generadas, análisis, diseño y pruebas en `docs/` y sus entregables) todavía describen la implementación anterior (amistad y notificaciones, CU0011 a CU0013). La lista está en `docs/tareas.md`.

---

## Dónde está cada cosa

| Carpeta | Qué contiene |
|---|---|
| `enunciado_umbook.pdf` | Enunciado del proyecto de la cátedra |
| `1. Requerimientos/` | `1_Modelo de Dominio/` · `2_Lista de Actores y CU.docx` · `3_Diagrama de Casos de Uso/` · `4_Casos de Uso/` (fichas del grupo y las cinco implementadas) · `5_Requisitos No Funcionales/` · `6_Prototipo de Interfaces/` |
| `2. Análisis/` | `1_Diagrama de Clases de Análisis.png` · `2_Diagrama de Paquetes.png` · `3_Diagramas de Colaboración/` (los cinco casos de uso implementados) · `4_Diagrama de paquetes y colaboracion.docx` |
| `3. Diseño/` | `1_Diagrama de Despliegue.png` · `2_Diagrama de Subsistemas.png` · `3_Diagramas de Clases/` (clases de diseño con patrones) · `4_Diagramas de Secuencia/` · `5_Diagramas de Estado/` · `6_Propuesta de Arquitectura/` · `7_Implementacion.docx`. Su `README.md` es el índice |
| `4. Implementacion/` | `1_Casos de Uso/` y `2_Diagramas de Secuencia/` (de la compañera, tal cual) · `codigo/` (backend y frontend, con su propio `README.md`). Su `README.md` explica el origen y los cambios |
| `5. Pruebas/` | `1_Plan de Pruebas/` · `2_Procedimientos de Prueba.docx` · `3_Casos de Prueba.xlsx` |

**Numeración.** Dentro de cada carpeta de etapa, los artefactos llevan un número (`1_`, `2_`, …) con **el orden de la corrección de la cátedra** (`correccion_catedra_grupo3.pdf`). Lo que la corrección no pide (prototipo de interfaces, documentos complementarios) va al final. La tabla completa, con lo que marcó la cátedra y el estado actual de cada artefacto, está en [`docs/00_INDICE.md`](docs/00_INDICE.md) §4.
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

Las instrucciones completas —dependencias, configuración y ejecución de las pruebas— están en `4. Implementacion/codigo/README.md`.

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
