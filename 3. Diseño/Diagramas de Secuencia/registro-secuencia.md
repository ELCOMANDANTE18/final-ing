# CU0006 — Registrar Usuario — Diagrama de secuencia

CU0006. Curso normal + los dos alternativos: email ya registrado (409, lo
decide `AuthService`) y formato inválido (400, lo corta `RegisterSchema` de
marshmallow antes de tocar la base). El frontend nunca inicia sesión
automáticamente después de registrarse: muestra un mensaje de éxito y
redirige a `/login` para que el usuario entre con sus credenciales.

<!-- png: 3. Diseño/Diagramas de Secuencia/CU0006 - Registrar Usuario.png -->
```mermaid
sequenceDiagram
    actor U as Usuario
    participant FE as RegisterComponent (Angular)
    participant API as POST /auth/register
    participant SVC as AuthService (backend)
    participant DAO as UserDao
    participant DB as SQLite

    U->>FE: completa name + email + password, submit

    alt algún campo vacío (validación del propio FE)
        FE-->>U: "Por favor complete todos los campos correctamente."
    else campos completos
        FE->>API: POST /auth/register {name, email, password}
        API->>API: RegisterSchema().load(body)

        alt formato inválido (email mal formado o password < 8 caracteres)
            API-->>FE: 400 {"error": "Por favor complete todos los campos correctamente."}
            FE-->>U: muestra error, se queda en el formulario
        else formato válido
            API->>SVC: registrar(name, email, password)
            SVC->>DAO: get_by_email(email)
            DAO->>DB: SELECT * FROM usuarios WHERE email = ?
            DB-->>DAO: fila o ninguna
            DAO-->>SVC: Usuario | None

            alt ya existe un usuario con ese email
                SVC-->>API: raise EmailYaRegistradoError
                API-->>FE: 409 {"error": "Este correo ya está registrado."}
                FE-->>U: muestra error, se queda en el formulario
            else email disponible
                SVC->>SVC: generate_password_hash(password)
                SVC->>DAO: create(name, email, password_hash)
                DAO->>DB: INSERT INTO usuarios (...)
                DB-->>DAO: usuario con id asignado
                DAO-->>SVC: Usuario
                SVC-->>API: Usuario creado
                API-->>FE: 201 {id, name, email}
                FE->>FE: successMessage = "Cuenta creada con éxito..."
                FE-->>U: espera ~1.2s y redirige a /login
            end
        end
    end
```

**Por qué no hashea el frontend ni valida la password ahí:** el hash
(`generate_password_hash`, Werkzeug/PBKDF2) se calcula en `AuthService.registrar`,
nunca antes — la contraseña en texto plano solo viaja una vez, por HTTPS, del
formulario al backend. La regla de "mínimo 8 caracteres" vive en
`RegisterSchema` (backend), no en el FE: `RegisterComponent.submit()` sólo
chequea que los campos no estén vacíos, así que un password corto sí llega a
pegarle a la API y vuelve como 400 — no hay duplicación de la regla de
negocio en dos capas.

**Nota de autorización:** `POST /auth/register` es el único endpoint de
`auth_controller` sin `@token_required` (junto con `/auth/login`), porque por
definición todavía no existe un usuario autenticado en este flujo.
