# CU0012 — Aceptar / Rechazar Solicitud — Diagrama de secuencia

Muestra las tres cosas que `PROMPT_CONSTRUCCION.md` pedía explícitas: la
autorización (solo el receptor puede responder), la delegación al patrón State, y
la transacción única (estado + vínculo `Amistad` se confirman o se revierten
juntos).

<!-- implementación anterior, no se regenera: _version_anterior/3. Diseño/4_Diagramas de Secuencia/CU0012 - Aceptar - Rechazar Solicitud.png -->
```mermaid
sequenceDiagram
    actor B as Usuario B (receptor)
    participant FE as WelcomeComponent
    participant API as POST /amistad/solicitudes/{id}/aceptar
    participant SVC as AmistadService
    participant SDAO as SolicitudDao
    participant SOL as SolicitudAmistad (contexto State)
    participant EST as _estado_obj (Pendiente)
    participant DB as SQLAlchemy session

    B->>FE: click "Aceptar" en una solicitud
    FE->>API: POST .../{id}/aceptar (JWT de B)
    API->>SVC: responder_solicitud(id, usuario_id=B.id, aceptar=true)
    SVC->>SDAO: get_by_id(id)
    SDAO-->>SVC: SolicitudAmistad | None

    alt no existe
        SVC-->>API: raise SolicitudNoEncontradaError
        API-->>FE: 404
    else B no es el receptor de esta solicitud
        SVC-->>API: raise NoAutorizadoError
        API-->>FE: 403
    else B es el receptor
        SVC->>SOL: aceptar()
        SOL->>EST: aceptar(solicitud)
        alt estado actual = Pendiente
            EST->>SOL: crear_vinculo_amistad()
            SOL->>DB: session.add(Amistad(...))
            EST->>SOL: set_estado(Aceptada())
            SVC->>DB: session.commit()
            Note over SVC,DB: un solo commit para el estado="aceptada"<br/>y el nuevo vínculo Amistad
            SVC-->>API: solicitud actualizada
            API-->>FE: 200 {estado: "aceptada"}
        else estado ya terminal (Aceptada o Rechazada)
            EST-->>SOL: raise EstadoInvalidoError
            SOL-->>SVC: propaga excepción
            SVC->>DB: session.rollback()
            Note over SVC,DB: nada de lo anterior queda a mitad de camino
            SVC-->>API: propaga EstadoInvalidoError
            API-->>FE: 409
        end
    end
```

El flujo de **Rechazar** es el mismo diagrama reemplazando `aceptar()` por
`rechazar()`: no hay rama de `crear_vinculo_amistad()`, solo el cambio de estado a
`Rechazada` (o el mismo `EstadoInvalidoError` si ya estaba en un estado terminal).
