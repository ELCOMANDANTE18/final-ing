# 00 — ÍNDICE DEL PROYECTO (leer primero)

**Versión:** 2.2 · **Última modificación:** 26/11/2026 · **Etapa:** Gestión del proyecto

**Materia:** Ingeniería de Software · **Alumno:** Victor Gimenez (legajo 61.174) · **Proyecto:** UMBook

---

## 1. Regla de oro

El repositorio contiene **dos clases de documentos**:

| | Qué es | Dónde |
|---|---|---|
| **Entregables** | Los `.docx`, `.pdf`, `.xlsx` y `.png` de las carpetas de etapa | `1. Requerimientos/` … `5. Pruebas/` |
| **Fuentes en markdown** | Los textos de los que salen los entregables y la documentación técnica | `docs/` |

**Cuando un `.md` y su entregable difieren, manda el `.md`** en los documentos que tienen generador (fichas de caso de uso, listado de RNF y diagramas). En el resto, manda el entregable de la carpeta de etapa.

**Alcance:** la implementación (`4. Implementacion/`) es la del repositorio de una compañera del grupo, con correcciones de seguridad y frontend nuevo: **CU0001 Iniciar Sesión, CU0006 Registrar Usuario y CU0010 Invitación a la aplicación**. Todas las etapas están alineadas con ese código (revisión en [`OBSERVACIONES_POR_ETAPA_UMBook.md`](./OBSERVACIONES_POR_ETAPA_UMBook.md)). Lo que describía la implementación anterior (amistad, CU0011 a CU0013) y los originales reemplazados del grupo están en `_version_anterior/`.

---

## 2. Dónde buscar cada cosa

| Necesito… | Ir a |
|---|---|
| Correr el sistema o las pruebas | `4. Implementacion/codigo/README.md` |
| Qué se tomó del código de la compañera y qué se cambió | `4. Implementacion/README.md` |
| Saber qué código tiene cada caso de uso | [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md) |
| Las fichas de los casos de uso implementados | `1. Requerimientos/4_Casos de Uso/`: `CU0001_Iniciar_Sesión.docx`, `CU0006.docx` y `CU0006_Registrar_Usuario.docx`, `CU0010.docx` (fuente de las generadas: `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md`) |
| Los requisitos no funcionales | `1. Requerimientos/5_Requisitos No Funcionales/UMBook_RNF.docx` (fuente: `REQUISITOS_NO_FUNCIONALES_UMBook.md`) |
| Clases y paquetes de análisis, colaboración por caso de uso | `2. Análisis/` (fuente: `ANALISIS_UMBook.md`) |
| Arquitectura, clases de diseño, despliegue, subsistemas, secuencias y estados | `3. Diseño/` (fuente: `DISEÑO_UMBook.md` y `3. Diseño/README.md`) |
| Plan, casos y procedimientos de prueba | `5. Pruebas/` (fuente: `PRUEBAS_UMBook.md`) |
| Qué se observó en cada etapa y cómo se resolvió | [`OBSERVACIONES_POR_ETAPA_UMBook.md`](./OBSERVACIONES_POR_ETAPA_UMBook.md) |
| Qué falta antes de la defensa | [`tareas.md`](./tareas.md) |

---

## 3. Documentos de `docs/`

| Documento | Etapa | Versión | Qué contiene |
|---|---|---|---|
| `00_INDICE.md` | Gestión del proyecto | 2.0 | Este archivo |
| `CATALOGO_CASOS_DE_USO_UMBook.md` | Requisitos | 2.0 | Códigos de todos los casos de uso, las fichas del repositorio y los tres implementados |
| `ESPECIFICACIONES_CASOS_DE_USO_UMBook.md` | Requisitos | 2.0 | Fichas generadas de CU0001 y CU0006 con la plantilla de la cátedra |
| `REQUISITOS_NO_FUNCIONALES_UMBook.md` | Requisitos | 3.0 | RNF-01 a RNF-25, con su estado contra el código |
| `ANALISIS_UMBook.md` | Análisis | 2.1 | Clases de análisis, paquetes y colaboraciones de los tres casos |
| `DISEÑO_UMBook.md` | Diseño | 2.2 | Capas, estructura, mecanismos, patrones, despliegue, subsistemas, diferencias con la propuesta y hallazgos |
| `PRUEBAS_UMBook.md` | Prueba | 2.2 | Plan, casos y procedimientos de los tres casos y de seguridad, trazados a las 42 pruebas del backend y las 11 del frontend |
| `OBSERVACIONES_POR_ETAPA_UMBook.md` | Gestión del proyecto | 1.6 | Revisión de cada etapa contra el código y cómo se resolvió cada observación |
| `tareas.md` | Gestión del proyecto | 2.0 | Lo pendiente antes de la defensa, lo resuelto y los límites declarados |

Los documentos técnicos de la implementación anterior (`proyecto.md`, `backend.md`, `frontend.md`, `construccion.md` y `prompt-construccion.md`) están en `_version_anterior/docs/`. Lo vigente está en `4. Implementacion/README.md` y `4. Implementacion/codigo/README.md`.

### Herramientas

| Archivo | Para qué sirve |
|---|---|
| `generar_diagramas.py` | Dibuja los `.png` de los diagramas de clases y de secuencia a partir de los bloques Mermaid de los `.md`. Requiere Mermaid CLI 12 (`mmdc`). |
| `generar_diagrama_casos_de_uso.py` | Dibuja el diagrama de casos de uso único de Requerimientos. |
| `generar_colaboraciones.py` | Dibuja los diagramas de colaboración de Análisis, con los íconos del Proceso Unificado. |
| `generar_despliegue_subsistemas.py` | Dibuja los diagramas de despliegue y de subsistemas de Diseño, con la forma de los del grupo (PlantUML). Requiere ImageMagick para el `.png`. |
| `generar_estados.py` | Dibuja la lámina de diagramas de estados de Diseño. Requiere ImageMagick para el `.png`. |
| `generar_entregables.py` | Genera los `.docx` (fichas de CU, listado de RNF, plan y procedimientos de prueba) y el `.xlsx` de casos de prueba a partir de los `.md`. Requiere `python-docx` y `openpyxl`. |

---

## 4. Entregables en el orden de la corrección de la cátedra

Fuente: `correccion_catedra_grupo3.pdf` (corrección del 8/6/25). Dentro de cada carpeta de etapa, cada artefacto lleva un número (`1_`, `2_`, …) con el orden de la corrección. Lo que la corrección no pide va al final. Lo que se hizo en JIRA no tiene archivo en el repositorio.

### 1. Requerimientos

| Nº | Artefacto que pide la cátedra | Dónde | Corrección | Estado actual |
|---|---|---|---|---|
| — | Listado de requerimientos candidatos (backlog) | JIRA | Hecho en JIRA | Fuera del repositorio |
| 1 | Modelo del Dominio o del Negocio | `1_Modelo de Dominio/` | OK | Del grupo (`.docx` e imagen); con la invitación guardada, coincide con el código |
| 2 | Listado de actores y casos de uso | `2_Lista de Actores y CU.docx` | OK | Del grupo, con el código de cada caso de uso |
| — | Priorización de casos de uso | JIRA | Hecho en JIRA | Fuera del repositorio |
| 3 | Diagrama de casos de uso (uno solo para toda la aplicación) | `3_Diagrama de Casos de Uso/` | **FALTA** | ✅ `Diagrama de Casos de Uso - UMBook` (`.pdf`, `.png` y `.svg`): 24 casos con código, en los paquetes de Análisis, con los tres implementados resaltados |
| 4 | Detalle de cada caso de uso | `4_Casos de Uso/` | OK | ✅ Fichas del grupo, con las de CU0001, CU0006 y CU0010 corregidas para coincidir con el código |
| 5 | Listado de requerimientos no funcionales | `5_Requisitos No Funcionales/` | **FALTA** | ✅ `UMBook_RNF.docx` (generado, RNF-01 a RNF-25, con su estado) y el listado anterior del grupo |
| 6 | *(no lo pide la corrección)* Prototipo de interfaces | `6_Prototipo de Interfaces/` | — | Enlace a Figma |

### 2. Análisis

| Nº | Artefacto que pide la cátedra | Dónde | Corrección | Estado actual |
|---|---|---|---|---|
| 1 | Diagrama de clases de análisis | `1_Diagrama de Clases de Análisis…` | OK | ✅ `- Casos implementados.png` (generado, con estereotipos interfaz, control y entidad) y el del grupo, que cubre toda la aplicación |
| 2 | Diagrama de paquetes | `2_Diagrama de Paquetes.png` | OK | ✅ Rehecho con los paquetes del grupo, corregido |
| 3 | Diagramas de interacción (colaboración) | `3_Diagramas de Colaboración/` | OK | ✅ CU0001, CU0006 y CU0010 (generados, numerados, con íconos del Proceso Unificado) |
| 4 | *(complementario)* Documento de paquetes y colaboración | `4_Diagrama de paquetes y colaboracion.docx` | — | Del grupo, con una nota que remite a los diagramas vigentes |
| — | Completar el documento de requisitos no funcionales | `1. Requerimientos/5_Requisitos No Funcionales/` | OK | ✅ Ver Requerimientos, Nº 5 |

### 3. Diseño

| Nº | Artefacto que pide la cátedra | Dónde | Corrección | Estado actual |
|---|---|---|---|---|
| 1 | Diagrama de despliegue | `1_Diagrama de Despliegue.png` | OK | ✅ Rehecho con el código actual (Flask, SQLite, Angular, Gmail) y la forma del original del grupo |
| 2 | Diagrama de subsistemas | `2_Diagrama de Subsistemas.png` | OK | ✅ Rehecho con el código actual y la forma del original del grupo; la aplicación específica usa los paquetes de Análisis |
| 3 | Diagrama de clases de diseño (con patrones de diseño) | `3_Diagramas de Clases/` | **FALTA** | ✅ `Diagrama de clases de diseño.png` del código actual (CU0001, CU0006, CU0010), con Singleton, DAO y Decorator; fuente `diseno-clases.md` |
| 4 | Diagramas de secuencia | `4_Diagramas de Secuencia/` | OK | ✅ CU0001, CU0006 y CU0010 con los nombres del código y la estética de la compañera; `Diagrama_Secuencia.pdf` del grupo para los no implementados |
| 5 | Diagramas de estados | `5_Diagramas de Estado/` | OK | ✅ `Diagramas de Estado.png`: Invitación y Sesión del usuario, con la forma del PDF del grupo; fuente `estados.md` |
| 6 | Propuesta de arquitectura basada en patrones | `6_Propuesta de Arquitectura/` | OK | ✅ Del grupo, con la sección "Estado de la implementación" (qué se implementó y qué no); resumen en `DISEÑO_UMBook.md` §8 |
| 7 | *(complementario)* Documento de implementación | `7_Implementacion.docx` | — | ✅ Enlace corregido a `MaguiMaluff/final-software` (commit `fe825751`); remite a `4. Implementacion/` |

### 4. Implementación

| Artefacto que pide la cátedra | Dónde | Corrección | Estado actual |
|---|---|---|---|
| Implementar una parte (por ejemplo, el login) | `4. Implementacion/` | OK | ✅ CU0001, CU0006 y CU0010 (código de la compañera con 10 correcciones de seguridad, invitación guardada y frontend nuevo), 42 pruebas automáticas del backend y 11 del frontend. Sus fichas (`1_Casos de Uso/`) y secuencias (`2_Diagramas de Secuencia/`) se conservan tal cual; el README anota en qué difieren del código |

### 5. Prueba

| Nº | Artefacto que pide la cátedra | Dónde | Corrección | Estado actual |
|---|---|---|---|---|
| 1 | Plan de prueba | `1_Plan de Pruebas/` | OK | ✅ `UMBook_Plan_de_Pruebas.docx` (generado). `Modelo_Plan_de_Pruebas.docx` es el modelo del grupo y se conserva sin tocar |
| 2 | Procedimientos de prueba | `2_Procedimientos de Prueba.docx` | OK, falta completar | ✅ PR 0001, PR 0006, PR 0010 y PR SEG (generado) |
| 3 | Casos de prueba | `3_Casos de Prueba.xlsx` | OK, falta completar | ✅ 32 casos (CU0001, CU0006, CU0010 y seguridad) trazados a las 42 pruebas del backend y las 11 del frontend (generado) |

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
| 2.2 | 26/11/2026 | Gestión del proyecto | H6, H9, H10 y H11 resueltos: todos los hallazgos de diseño cerrados; pruebas del frontend; 32 casos de prueba |
| 2.1 | 26/11/2026 | Gestión del proyecto | H7 y H8 resueltos en el código; 37 pruebas y 29 casos de prueba |
| 2.0 | 26/11/2026 | Gestión del proyecto | Todas las etapas alineadas con la implementación actual (Etapas 4 y 5: pruebas rehechas para CU0001, CU0006, CU0010 y seguridad; documentos técnicos viejos archivados). Se reescriben §1 a §4 |
| 1.4 | 26/11/2026 | Gestión del proyecto | Diagrama de clases de diseño, despliegue, subsistemas, secuencias y estados rehechos a partir del código actual (D-01 a D-05); propuesta de arquitectura, `7_Implementacion.docx` y `DISEÑO_UMBook.md` realineados (D-06 a D-08): Etapa 3 corregida |
