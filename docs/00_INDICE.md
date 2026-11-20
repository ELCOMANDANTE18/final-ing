# 00 — ÍNDICE DEL PROYECTO (leer primero)

**Versión:** 1.0 · **Última modificación:** 20/11/2026 · **Etapa:** Gestión del proyecto

**Materia:** Ingeniería de Software · **Alumno:** Victor Gimenez (legajo 61.174) · **Proyecto:** UMBook

---

## 1. Regla de oro

El repositorio contiene **dos clases de documentos**:

| | Qué es | Dónde |
|---|---|---|
| **Entregables** | Los `.docx`, `.pdf`, `.xlsx` y `.png` de las carpetas de etapa | `1. Requerimientos/` … `5. Pruebas/` |
| **Fuentes en markdown** | Los textos de los que salen los entregables y la documentación técnica | `docs/` |

**Cuando un `.md` y su entregable difieren, manda el `.md`** en los documentos que tienen generador (fichas de caso de uso, listado de RNF y diagramas). En el resto, manda el entregable de la carpeta de etapa.

**Alcance:** este repositorio implementa **cinco casos de uso** de UMBook (los del alumno). Los demás casos de uso del grupo están en `1. Requerimientos/Casos de Uso/` con las fichas de sus autores y **no se implementaron**. Ver el catálogo.

---

## 2. Dónde buscar cada cosa

| Necesito… | Ir a |
|---|---|
| Correr el sistema, las pruebas o cargar datos de demostración | `4. Implementacion/codigo/README.md` |
| Saber qué código tiene cada caso de uso y **dónde choca** | [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) |
| Las fichas de los casos de uso implementados | `1. Requerimientos/Casos de Uso/CU0001_…`, `CU0006_…`, `CU0011_…`, `CU0012_…`, `CU0013_…` (fuente: `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md`) |
| Los requisitos no funcionales | `1. Requerimientos/UMBook_RNF.docx` (fuente: `REQUISITOS_NO_FUNCIONALES_UMBook.md`) |
| Clases y paquetes de análisis, colaboración por caso de uso | `2. Análisis/` (fuente: `ANALISIS_UMBook.md`) |
| Arquitectura, clases de diseño, despliegue, subsistemas, secuencias y estados | `3. Diseño/` (fuente: `DISEÑO_UMBook.md` y `3. Diseño/README.md`) |
| Casos y procedimientos de prueba | `PRUEBAS_UMBook.md` (fuente) y `5. Pruebas/` |
| Cómo y por qué se construyó cada implementación | [`construccion.md`](./construccion.md) |
| Qué falta antes de la defensa | [`tareas.md`](./tareas.md) |

---

## 3. Documentos de `docs/`

| Documento | Etapa | Versión | Qué contiene |
|---|---|---|---|
| `00_INDICE.md` | Gestión del proyecto | 1.0 | Este archivo |
| `CATALOGO_CASOS_DE_USO_UMBook.md` | Requisitos | 1.1 | Códigos de los CU implementados, todas las fichas del repositorio, los choques de códigos y el diagrama de CU de lo implementado |
| `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md` | Requisitos | 1.1 | Las cinco fichas de caso de uso con la plantilla de la cátedra |
| `PRUEBAS_UMBook.md` | Prueba | 1.0 | Casos y procedimientos de prueba alineados con el comportamiento real, trazados a las 32 pruebas automáticas |
| `REQUISITOS_NO_FUNCIONALES_UMBook.md` | Requisitos | 2.0 | RNF-01 a RNF-18, con su estado contra el código |
| `ANALISIS_UMBook.md` | Análisis | 1.0 | Clases de análisis, paquetes y cinco diagramas de colaboración |
| `DISEÑO_UMBook.md` | Diseño | 1.0 | Capas, mecanismos, clases integral, despliegue, subsistemas, diferencias con la propuesta original y hallazgos |
| `proyecto.md` | Gestión del proyecto | 1.1 | Casos de uso implementados, alcance y decisiones de diseño |
| `backend.md` | Implementación | 1.1 | Arquitectura, endpoints y convenciones del backend |
| `frontend.md` | Implementación | 1.1 | Arquitectura, rutas y convenciones del frontend |
| `construccion.md` | Implementación | 1.1 | Paso a paso de la construcción |
| `tareas.md` | Gestión del proyecto | 1.1 | Lo resuelto y lo pendiente |
| `prompt-construccion.md` | Gestión del proyecto | 1.1 | Especificación original usada para construir el proyecto (documento histórico) |

### Herramientas

| Archivo | Para qué sirve |
|---|---|
| `generar_diagramas.py` | Dibuja los `.png` de los diagramas a partir de los bloques Mermaid de los `.md`. Requiere `mmdc` (Mermaid CLI). |
| `generar_entregables.py` | Genera los `.docx` (fichas de CU, listado de RNF, plan y procedimientos de prueba) y el `.xlsx` de casos de prueba a partir de los `.md`. Requiere `python-docx` y `openpyxl`. |

---

## 4. Estado de los entregables

| Etapa | Entregable | Estado |
|---|---|---|
| Requisitos | Fichas de los 5 CU implementados | ✅ Hechas; códigos con choques marcados |
| Requisitos | Listado de RNF | ✅ Actualizado al código |
| Requisitos | Diagrama de CU único | ✅ `0-CU_General.pdf` (del grupo, un solo diagrama, sin códigos) y `Diagrama de Casos de Uso - Implementados.png` (con códigos) |
| Requisitos | Modelo de dominio, prototipo de interfaces | Del grupo: el modelo de dominio es una sola imagen sin texto y el prototipo es un enlace a Figma. No se tocaron |
| Análisis | Clases, paquetes y colaboración | ✅ Hechos para los 5 CU |
| Diseño | Capas, clases integral, despliegue, subsistemas, secuencias y estados | ✅ Hechos |
| Implementación | Código, pruebas (32), datos de demostración | ✅ |
| Prueba | Plan, casos (31) y procedimientos | ✅ Generados desde `PRUEBAS_UMBook.md`, alineados con el código. `Modelo_Plan_de_Pruebas.docx` es el modelo del grupo (cubre otros CU y nombra JUnit); se conserva sin tocar |

Los pendientes y su detalle están en [`tareas.md`](./tareas.md), sección "Pendientes de consistencia".

---

## 5. Control de versiones de los documentos

Aplica a todos los documentos de `docs/`.

**Encabezado**, debajo del título:

```
**Versión:** X.Y · **Última modificación:** DD/MM/AAAA · **Etapa:** <flujo del PU>
```

**Bloque de cierre**, al final:

```
## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | DD/MM/AAAA | <flujo del PU> | Versión inicial |
```

**Reglas:**

- Una fila **por cambio con contenido**. Una corrección de tipeo no genera fila ni sube la versión.
- Se conservan **como máximo las últimas cuatro filas**.
- **X.1, X.2…** para cambios menores; **X.0** para cambios de alcance o decisiones estructurales.
- En **Etapa / Chat** va el flujo del Proceso Unificado: Requisitos, Análisis, Diseño, Implementación, Prueba, o **Gestión del proyecto**.
- Si cambia un documento que tiene generador, hay que **volver a correr el generador** y revisar el entregable.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Gestión del proyecto | Versión inicial: índice, regla de control de versiones y estado de los entregables |
