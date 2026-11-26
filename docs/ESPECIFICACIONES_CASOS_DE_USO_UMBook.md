# ESPECIFICACIÓN DE CASOS DE USO — UMBook (casos implementados)

**Versión:** 2.0 · **Última modificación:** 25/11/2026 · **Etapa:** Requerimientos

Texto fuente de dos fichas de `1. Requerimientos/4_Casos de Uso/`: **`CU0001_Iniciar_Sesión.docx`** y **`CU0006_Registrar_Usuario.docx`**. Las genera `docs/generar_entregables.py`; **si el `.docx` y este texto difieren, manda este texto** y hay que volver a generar el `.docx`.

El tercer caso implementado, **CU0010 Invitación a la aplicación**, tiene la ficha del grupo (`CU0010.docx`, de Juan Pablo Samsó), corregida directamente sobre el `.docx`. Qué ficha corresponde a cada caso está en [`CATALOGO_CASOS_DE_USO_UMBook.md`](./CATALOGO_CASOS_DE_USO_UMBook.md).

## Convenciones

| Código | Significa |
|---|---|
| `ca n.m` | Curso alternativo `m` que nace en el paso `n` del curso normal |
| `rnf n.m` | Requisito no funcional de la ficha. La numeración es propia de cada ficha y sigue la de la ficha del grupo |
| `Ob n` | Observación de la ficha |
| `RNF-xx` | Requisito del listado general (`REQUISITOS_NO_FUNCIONALES_UMBook.md`) |

Los actores son los de `2_Lista de Actores y CU.docx`: **Usuario No Registrado**, **Usuario Registrado** (tiene cuenta pero no inició sesión) y **Usuario Autenticado** (inició sesión).

---

# PAQUETE: GESTIÓN DE USUARIOS

## CU0001 — Iniciar Sesión

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0001 |
| Paquete | Gestión de Usuarios |
| Nombre | Iniciar Sesión |
| Versión | 2.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez |
| Descripción | Permite a un usuario registrado acceder a la aplicación con su email y su contraseña. Al ingresar recibe un token de sesión (JWT). |
| Actores | Usuario Registrado: persona que ya posee una cuenta en el sistema. Al terminar el caso de uso pasa a ser Usuario Autenticado. |
| Frecuencia | Cada vez que el usuario accede a la aplicación. |
| Observaciones | Ver Ob 1 a Ob 4. |

### Curso normal

**Precondición:** el usuario ya está registrado (CU0006) y no tiene la sesión iniciada.

| Nº | Paso |
|---|---|
| 1 | El usuario ingresa a la pantalla de inicio de sesión. |
| 2 | El sistema muestra el formulario con los campos email y contraseña. |
| 3 | El usuario completa ambos campos y presiona "Ingresar". |
| 4 | El sistema valida que ambos campos estén completos y que el email tenga formato válido. {rnf 1.4} |
| 5 | El sistema busca al usuario por su email y verifica la contraseña contra el hash guardado. {rnf 1.1} {rnf 1.3} |
| 6 | El sistema genera un token de sesión (JWT) y lo devuelve junto con el nombre del usuario. {rnf 1.5} |
| 7 | El sistema guarda el token en el navegador y lleva al usuario a la pantalla principal. |
| 8 | FIN CASO DE USO |

### Cursos alternativos

**ca 4.1 — Error en el formulario**

| Nº | Paso |
|---|---|
| 4.1.1 | Falta el email o la contraseña, o el email no tiene formato válido. |
| 4.1.2 | El sistema muestra "Por favor complete todos los campos correctamente." y no consulta las credenciales. |
| 4.1.3 | Ir al paso 3. |

**ca 5.1 — Credenciales incorrectas**

| Nº | Paso |
|---|---|
| 5.1.1 | El email no corresponde a ningún usuario, o la contraseña no coincide. |
| 5.1.2 | El sistema muestra "Credenciales incorrectas.", el mismo mensaje en los dos casos, y no genera token. {rnf 1.2} |
| 5.1.3 | Ir al paso 3. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 1.1 | Clave con hash | La contraseña se compara contra un hash con salt; nunca se guarda ni se registra en texto plano. Deriva de RNF-09. |
| rnf 1.2 | Mensaje único | El error no distingue entre email inexistente y contraseña incorrecta, para no revelar qué emails están registrados. Deriva de RNF-18. |
| rnf 1.3 | Verificar antes de decidir | La contraseña se verifica antes de elegir entre éxito y error: no hay un camino de éxito que no pase por esa verificación. Deriva de RNF-09. |
| rnf 1.4 | Validación en el servidor | El formato de los datos se valida también en el servidor, no solo en la pantalla. Deriva de RNF-19. |
| rnf 1.5 | Tiempo de respuesta | La validación de credenciales no debe superar los 2 segundos. Deriva de RNF-02. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 1 | El token se guarda en el `localStorage` del navegador. Es una decisión aceptada para esta versión: `localStorage` es accesible desde JavaScript, así que no es un almacenamiento "seguro" en sentido estricto. |
| Ob 2 | Si una operación que lleva el token recibe 401 (token vencido o inválido), la interfaz cierra la sesión y vuelve a la pantalla de inicio de sesión (RNF-20). |
| Ob 3 | No hay bloqueo por intentos fallidos. |
| Ob 4 | "Cerrar sesión" no es un caso de uso aparte: el botón de la pantalla principal borra el token guardado. |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0001 - Iniciar Sesión | Diagrama de colaboración | `2. Análisis/3_Diagramas de Colaboración/` |
| CU0001 - Iniciar Sesión | Diagrama de secuencia | `3. Diseño/4_Diagramas de Secuencia/` |
| CU001-login | Ficha de la implementación | `4. Implementacion/1_Casos de Uso/` |

---

## CU0006 — Registrar Usuario

### Resumen ejecutivo

| Campo | Valor |
|---|---|
| Código | CU0006 |
| Paquete | Gestión de Usuarios |
| Nombre | Registrar Usuario |
| Versión | 2.0 |
| Prioridad | Alta |
| Confeccionó | Victor Gimenez, a partir de la ficha `CU0006.docx` de Alexis Martin Yassuff |
| Descripción | Permite a un nuevo usuario registrarse completando un formulario con su nombre, su email y una contraseña. |
| Actores | Usuario No Registrado: persona que aún no posee cuenta en el sistema y desea registrarse. |
| Frecuencia | Varias veces al día. |
| Observaciones | Ver Ob 1 a Ob 3. |

### Curso normal

**Precondición:** no haber iniciado sesión.

| Nº | Paso |
|---|---|
| 1 | El usuario accede a la pantalla de registro desde la pantalla de inicio de sesión o desde el enlace del correo de invitación (CU0010). |
| 2 | El sistema muestra el formulario de registro. |
| 3 | El usuario completa los campos requeridos (nombre, email y contraseña). |
| 4 | El usuario envía el formulario presionando el botón "Registrarse". |
| 5 | El sistema valida los datos: nombre de 1 a 128 caracteres, email con formato válido y contraseña de al menos 8 caracteres. {rnf 1.1} |
| 6 | El sistema verifica que el email no esté registrado y guarda la nueva cuenta, con la contraseña cifrada. {rnf 1.3} {rnf 1.4} |
| 7 | El sistema informa "Cuenta creada con éxito. Ya podés iniciar sesión." y redirige al usuario a la pantalla de inicio de sesión (CU0001). {rnf 1.2} |
| 8 | FIN CASO DE USO |

### Cursos alternativos

**ca 5.1 — Error en el formulario**

| Nº | Paso |
|---|---|
| 5.1.1 | Falta algún campo, el email no tiene formato válido o la contraseña tiene menos de 8 caracteres. |
| 5.1.2 | El sistema muestra "Por favor complete todos los campos correctamente." y no guarda nada. |
| 5.1.3 | Ir al paso 3. |

**ca 6.1 — Email ya registrado**

| Nº | Paso |
|---|---|
| 6.1.1 | Ya existe una cuenta con ese email (sin distinguir mayúsculas). |
| 6.1.2 | El sistema muestra "Este correo ya está registrado." y no guarda nada. |
| 6.1.3 | Ir al paso 3. |

### Requerimientos no funcionales

| Cod | Nombre | Descripción |
|---|---|---|
| rnf 1.1 | Validación de datos | El sistema debe validar, también en el servidor, que el email tenga formato válido y que la contraseña tenga al menos 8 caracteres. Deriva de RNF-19. |
| rnf 1.2 | Confirmación visual | El sistema debe mostrar mensajes claros de éxito o de error durante el registro. Deriva de RNF-07. |
| rnf 1.3 | Clave con hash | La contraseña se guarda con hash y salt. Deriva de RNF-09. |
| rnf 1.4 | Email único | El email es único en el sistema; lo garantiza una restricción de la base de datos, además de la verificación del paso 6. Deriva de RNF-23. |

### Observaciones

| Cod | Descripción |
|---|---|
| Ob 1 | El registro no inicia la sesión automáticamente: al terminar lleva a la pantalla de inicio de sesión. |
| Ob 2 | El email se guarda en minúsculas: "ana@x.com" y "ANA@X.COM" son la misma cuenta. |
| Ob 3 | No hay confirmación del email ni reglas de complejidad de la contraseña más allá del largo mínimo. |

### Documentación anexa

| Nombre | Tipo | Lugar |
|---|---|---|
| CU0006 | Ficha del grupo (Alexis Martin Yassuff) | `1. Requerimientos/4_Casos de Uso/CU0006.docx` |
| CU0006 - Registrar Usuario | Diagrama de colaboración | `2. Análisis/3_Diagramas de Colaboración/` |
| CU0006 - Registrar Usuario | Diagrama de secuencia | `3. Diseño/4_Diagramas de Secuencia/` |
| CU0006-registro | Ficha de la implementación | `4. Implementacion/1_Casos de Uso/` |

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 – 1.2 | 20/11/2026 – 25/11/2026 | Requisitos | Fichas de CU0001, CU0006, CU0011, CU0012 y CU0013 de la implementación anterior. Archivado en `_version_anterior/docs/` |
| 2.0 | 25/11/2026 | Requerimientos | Solo CU0001 y CU0006, contra el código actual. CU0006 sigue el flujo de la ficha del grupo (ca 5.1 y ca 6.1, rnf 1.x). Actores de la lista del grupo. CU0001: 401 como única respuesta de sesión inválida, rnf 1.5 de tiempo de respuesta y Ob 1 sobre `localStorage`. Se retiran las fichas de amistad |
