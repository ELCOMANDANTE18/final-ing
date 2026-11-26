# CU0001 — Iniciar Sesión — Diagrama de secuencia

**Versión:** 2.0 · **Última modificación:** 26/11/2026 · **Etapa:** Diseño

Curso normal y cursos alternativos de la ficha CU0001 (ca 4.1 y ca 5.1), con los nombres del código actual. Sigue la estética de los diagramas de la compañera (`4. Implementacion/2_Diagramas de Secuencia/caso1-login.png`) y corrige lo anotado en la observación I-01: la contraseña se verifica **antes** de decidir la rama, dentro de `AuthService.authenticate`, y el token lo crea el controller.

<!-- png: 3. Diseño/4_Diagramas de Secuencia/CU0001 - Iniciar Sesión.png -->
```mermaid
---
config:
  theme: redux-color
---
sequenceDiagram
    autonumber
    actor U as Usuario Registrado
    participant L as LoginComponent (Angular)
    participant A as AuthService (Angular)
    participant C as auth_controller (Flask)
    participant S as AuthService (Flask)
    participant D as UserDAO
    participant B as Base de Datos (SQLite)

    U->>L: Ingresa email y contraseña y presiona "Ingresar"
    alt ca 4.1 — Falta el email o la contraseña
        L-->>U: Muestra "Por favor complete todos los campos correctamente."
    else Campos completos
        L->>A: login(email, password)
        A->>C: POST /auth/login {email, password}
        activate C
        Note right of C: LoginSchema (marshmallow)<br/>valida el formato del email
        alt ca 4.1 — Email con formato inválido
            C-->>A: 400 {msg: "Por favor complete todos los campos correctamente."}
            A-->>L: error
            L-->>U: Muestra el mensaje
        else Formato válido
            C->>S: authenticate(email, password)
            activate S
            S->>D: get_by_email(email)
            Note right of D: Normaliza el email<br/>(minúsculas, sin espacios)
            D->>B: SELECT * FROM users WHERE email = ?
            B-->>D: fila o ninguna
            D-->>S: User | None
            opt Existe el usuario
                S->>S: check_password_hash(user.password_hash, password)
            end
            S-->>C: User | None
            deactivate S
            alt ca 5.1 — El email no existe o la contraseña no coincide
                C-->>A: 401 {msg: "Credenciales incorrectas."}
                A-->>L: error
                L-->>U: Muestra "Credenciales incorrectas."
            else Credenciales correctas
                C->>C: create_access_token(identity=str(user.id))
                C-->>A: 200 {access_token, user: {id, name, email}}
                A->>A: Guarda access_token y nombre en localStorage
                A-->>L: LoginResponse
                L-->>U: Redirige a /welcome
            end
        end
        deactivate C
    end
```

## Notas

- **Un solo mensaje para los dos errores de credenciales** (ca 5.1, rnf 1.2): `authenticate` devuelve `None` tanto si el email no existe como si la contraseña no coincide, así la respuesta no revela qué correos están registrados.
- **La contraseña se verifica antes de decidir.** `check_password_hash` corre dentro de `authenticate`, que solo devuelve el usuario si la verificación da bien. En el diagrama de la compañera aparecía dentro de la rama "Credenciales válidas", es decir, después de haber decidido (I-01).
- **El token lo genera el controller**, no el servicio: `create_access_token` está en `auth_controller.login`. Dura 15 minutos (valor por defecto de Flask-JWT-Extended); ver el diagrama de estados de la sesión en `5_Diagramas de Estado/`.
- **Validación en dos lugares:** el navegador solo revisa que los campos no estén vacíos; el formato del email lo valida `LoginSchema` en el servidor. Los dos casos son el ca 4.1.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.0 | 20/11/2026 | Diseño | Versión inicial, con los nombres de la implementación anterior |
| 2.0 | 26/11/2026 | Diseño | Rehecho con los nombres del código actual, numerado y con la estética de los diagramas de la compañera. Cursos alternativos con el código de la ficha (ca 4.1, ca 5.1) |
