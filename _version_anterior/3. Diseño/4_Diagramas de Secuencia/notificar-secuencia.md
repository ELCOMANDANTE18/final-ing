# CU0013 — Notificar Solicitud de Amistad Recibida — Diagrama de secuencia

Continúa exactamente donde termina
[`amistad-secuencia-solicitar.md`](./amistad-secuencia-solicitar.md): el punto
que hace válido el patrón es que `AmistadService` publica el evento en el
`Usuario` receptor y nunca llama al `NotificationService` directo.

<!-- implementación anterior, no se regenera: _version_anterior/3. Diseño/4_Diagramas de Secuencia/CU0013 - Notificar Solicitud Recibida.png -->
```mermaid
sequenceDiagram
    participant SVC as AmistadService
    participant B as Usuario B (Observable)
    participant OBS as NotificationService (Observador, Singleton)
    participant TPL as Jinja templates/emails/
    participant MAIL as Flask-Mail → SMTP Gmail
    participant FE as WelcomeComponent (home de B)
    participant API as GET /amistad/solicitudes/pendientes

    SVC->>B: notificar_observadores({tipo: "solicitud_recibida",<br/>receptor_email, emisor_nombre})
    loop por cada observador registrado en B
        B->>OBS: actualizar(evento)
    end
    OBS->>OBS: evento["tipo"] == "solicitud_recibida"?
    OBS->>TPL: render_template(solicitud_recibida.html / .txt, emisor_nombre)
    TPL-->>OBS: HTML + texto plano
    OBS->>MAIL: Message(subject, body, html) → mail.send(msg)
    alt envío correcto
        MAIL-->>B: llega el mail (canal "push")
    else falla el servidor de correo
        MAIL-->>OBS: excepción
        OBS->>OBS: logger.exception(...) — se registra y NO se propaga
        Note over OBS: la solicitud ya está guardada:<br/>la petición responde 201 igual (RNF-11)
    end

    Note over FE,API: canal "pull": la próxima vez que B entra a /welcome
    FE->>API: GET /amistad/solicitudes/pendientes (JWT de B)
    API-->>FE: [ {solicitud pendiente de A} ]
    FE-->>FE: renderiza card "Solicitudes de amistad recibidas"
```

**No hay entidad `Notificacion` separada** (decisión documentada en
[`../proyecto.md`](../../docs/proyecto.md)): el mail es la notificación "push" en tiempo
real, y la lista de `solicitudes/pendientes` es la notificación "pull" que ve la
home — la misma consulta que ya usa el CU de Solicitar Amistad.

**Si el correo falla** (servidor SMTP caído, credenciales inválidas),
`NotificationService.actualizar()` registra el error en el log y no lo propaga:
la solicitud ya creada se conserva y el receptor la ve igual por el canal "pull"
(RNF-11, CU0013 ca 4.2).
