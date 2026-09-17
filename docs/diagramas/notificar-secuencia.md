# Notificar Solicitud de Amistad Recibida — Diagrama de secuencia

Continúa exactamente donde termina
[`amistad-secuencia-solicitar.md`](./amistad-secuencia-solicitar.md): el punto
que hace válido el patrón es que `AmistadService` publica el evento en el
`Usuario` receptor y nunca llama al `NotificationService` directo.

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
    MAIL-->>B: llega el mail (canal "push")

    Note over FE,API: canal "pull": la próxima vez que B entra a /welcome
    FE->>API: GET /amistad/solicitudes/pendientes (JWT de B)
    API-->>FE: [ {solicitud pendiente de A} ]
    FE-->>FE: renderiza card "Solicitudes de amistad recibidas"
```

**No hay entidad `Notificacion` separada** (decisión documentada en
[`../proyecto.md`](../proyecto.md)): el mail es la notificación "push" en tiempo
real, y la lista de `solicitudes/pendientes` es la notificación "pull" que ve la
home — la misma consulta que ya usa el CU de Solicitar Amistad.
