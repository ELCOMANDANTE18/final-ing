# CU0006 — Registrar Usuario — Diagrama de secuencia

**Versión:** 2.1 · **Última modificación:** 26/11/2026 · **Etapa:** Diseño

Curso normal y cursos alternativos de la ficha CU0006 (ca 5.1 y ca 6.1), con los nombres del código actual. Sigue la estética de los diagramas de la compañera (`4. Implementacion/2_Diagramas de Secuencia/caso6-registro.png`) y agrega lo que la observación I-02 marcaba como faltante: el camino de datos inválidos (400) y los mensajes reales de la pantalla.

<!-- png: 3. Diseño/4_Diagramas de Secuencia/CU0006 - Registrar Usuario.png -->
```mermaid
---
config:
  theme: redux-color
---
sequenceDiagram
    autonumber
    actor U as Usuario No Registrado
    participant R as RegisterComponent (Angular)
    participant A as AuthService (Angular)
    participant C as auth_controller (Flask)
    participant S as AuthService (Flask)
    participant D as UserDAO
    participant B as Base de Datos (SQLite)

    U->>R: Completa nombre, email y contraseña y presiona "Registrarse"
    alt ca 5.1 — Falta un campo o la contraseña tiene menos de 8 caracteres
        R-->>U: Muestra "Por favor complete todos los campos correctamente."
    else Formulario completo
        R->>A: register(name, email, password)
        A->>C: POST /auth/register {name, email, password}
        activate C
        Note right of C: RegisterSchema (marshmallow): nombre de 1 a 128,<br/>email válido (máx. 255), contraseña de 8 o más
        alt ca 5.1 — Datos inválidos
            C-->>A: 400 {msg: "Por favor complete todos los campos correctamente.", errors}
            A-->>R: error
            R-->>U: Muestra el mensaje
        else Datos válidos
            C->>S: register_user(name, email, password)
            activate S
            S->>D: get_by_email(email)
            D->>B: SELECT * FROM users WHERE email = ?
            B-->>D: fila o ninguna
            D-->>S: User | None
            alt ca 6.1 — El email ya está registrado
                S-->>C: None
                C-->>A: 409 {msg: "Este correo ya está registrado."}
                A-->>R: error
                R-->>U: Muestra "Este correo ya está registrado."
            else Email disponible
                S->>S: generate_password_hash(password)
                S->>D: create(name, email, password_hash)
                Note right of D: Guarda el email normalizado<br/>(minúsculas, sin espacios)
                D->>B: INSERT INTO users (name, email, password_hash, created_at)
                B-->>D: id asignado
                D-->>S: User
                S-->>C: User
                C-->>A: 201 {id, email}
                A-->>R: respuesta
                R-->>U: Muestra "Cuenta creada con éxito. Ya podés iniciar sesión."
                R->>R: Espera 1,2 s y navega a /login (CU0001)
            end
            deactivate S
        end
        deactivate C
    end
```

## Notas

- **Registro simultáneo con el mismo correo** (ca 6.1): si dos registros pasan a la vez la búsqueda del mensaje 9, la restricción única de la base rechaza el segundo en el `INSERT`; `UserDAO.create` deshace la transacción y devuelve `None`, y la respuesta es la misma rama de 409.
- **Email duplicado sin distinguir mayúsculas** (ca 6.1): `UserDAO` normaliza el email al buscar y al guardar, así `ana@x.com` y `ANA@X.COM` son la misma cuenta.
- **La contraseña se cifra en el servidor** con `generate_password_hash` (Werkzeug) dentro de `register_user`; la base nunca guarda la contraseña en texto plano (rnf 1.3).
- **No inicia sesión automáticamente:** después del registro el usuario va a la pantalla de inicio de sesión (paso 7 de la ficha).
- **Validación en dos lugares:** el navegador corta los campos vacíos y la contraseña corta; el servidor vuelve a validar todo con `RegisterSchema`. Los dos casos son el ca 5.1.
- `POST /auth/register` no lleva `@token_required`: por definición, el usuario todavía no tiene sesión.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Diseño | Versión inicial, con los nombres de la implementación anterior |
| 2.0 | 26/11/2026 | Diseño | Rehecho con los nombres del código actual, numerado y con la estética de los diagramas de la compañera. Cursos alternativos con el código de la ficha (ca 5.1, ca 6.1) |
| 2.1 | 26/11/2026 | Diseño | `register_user` devuelve `User` o `None` (H9); nota sobre el registro simultáneo (H8) |
