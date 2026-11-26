# Solicitar Amistad / Aceptar-Rechazar — Diagrama de clases (patrón State)

`SolicitudAmistad` es el **contexto** del patrón: `aceptar()`/`rechazar()` son una
línea cada una, delegan siempre en `_estado_obj`. Nunca decide ella misma si la
transición es válida — eso lo sabe cada estado. Código real en
[`estado_solicitud.py`](../../docs/backend.md) y `persistence/models.py`.

<!-- implementación anterior, no se regenera: _version_anterior/3. Diseño/3_Diagramas de Clases/Diagrama de clases - Patrón State.png -->
```mermaid
classDiagram
    class SolicitudAmistad {
        +int id
        +int emisor_id
        +int receptor_id
        +string estado
        +datetime fecha_creacion
        -EstadoSolicitud _estado_obj
        +aceptar()
        +rechazar()
        +set_estado(estado_obj)
        +crear_vinculo_amistad()
    }

    class EstadoSolicitud {
        <<abstract>>
        +string nombre
        +aceptar(solicitud)*
        +rechazar(solicitud)*
    }

    class Pendiente {
        +nombre = "pendiente"
        +aceptar(solicitud) crea vínculo, pasa a Aceptada
        +rechazar(solicitud) pasa a Rechazada
    }

    class Aceptada {
        +nombre = "aceptada"
        +aceptar(solicitud) lanza EstadoInvalidoError
        +rechazar(solicitud) lanza EstadoInvalidoError
    }

    class Rechazada {
        +nombre = "rechazada"
        +aceptar(solicitud) lanza EstadoInvalidoError
        +rechazar(solicitud) lanza EstadoInvalidoError
    }

    class EstadoInvalidoError {
        <<exception>>
    }

    class Amistad {
        +int id
        +int usuario1_id
        +int usuario2_id
        +datetime fecha_creacion
    }

    SolicitudAmistad o-- "1" EstadoSolicitud : _estado_obj
    EstadoSolicitud <|-- Pendiente
    EstadoSolicitud <|-- Aceptada
    EstadoSolicitud <|-- Rechazada
    Aceptada ..> EstadoInvalidoError : lanza
    Rechazada ..> EstadoInvalidoError : lanza
    SolicitudAmistad ..> Amistad : crea (vía crear_vinculo_amistad)
```

`estado` (string persistido) y `_estado_obj` (objeto State, no persistido) se
mantienen sincronizados: `_estado_obj` se reconstruye con `@reconstructor` cada
vez que SQLAlchemy carga la fila desde la DB, a partir del string guardado
(`estado_desde_nombre()`).
