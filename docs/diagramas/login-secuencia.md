# Login — Diagrama de secuencia

Curso normal + los dos alternativos de CU0001, unificados en un solo `alt` para
mostrar el punto exacto del fix: `check_password_hash` se evalúa **antes** de
decidir la rama (a diferencia del diagrama original de la compañera, donde
aparecía adentro de la rama "éxito" — ver
[`../construccion.md` sección 1](../construccion.md#1-login--corrección-de-un-bypass-de-autenticación)).

```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE as LoginComponent (Angular)
    participant API as POST /auth/login
    participant SVC as AuthService (backend)
    participant DAO as UserDao
    participant DB as SQLite

    U->>FE: completa email + password, submit
    FE->>API: POST /auth/login {email, password}
    API->>SVC: autenticar(email, password)
    SVC->>DAO: get_by_email(email)
    DAO->>DB: SELECT * FROM usuarios WHERE email = ?
    DB-->>DAO: fila o ninguna
    DAO-->>SVC: Usuario | None

    Note over SVC: check_password_hash se evalúa ACÁ,<br/>antes de decidir la rama de éxito/error.

    alt usuario no existe OR password incorrecta
        SVC-->>API: raise CredencialesInvalidasError
        API-->>FE: 401 {"error": "Credenciales incorrectas."}
        FE-->>U: muestra error genérico (no distingue cuál de las dos falló)
    else usuario existe Y password correcta
        SVC-->>API: Usuario autenticado
        API->>API: create_access_token(identity=usuario.id)
        API-->>FE: 200 {token, user: {id, name}}
        FE->>FE: localStorage.setItem(token, name)
        FE-->>U: redirige a /welcome
    end
```

**Curso alternativo de formato** (campos vacíos/inválidos) no llega a pegarle al
backend: `LoginSchema` de marshmallow lo valida en `POST /auth/login`, y el
frontend ya corta antes con el mismo mensaje si `email`/`password` vienen vacíos
(`LoginComponent.submit()`).
