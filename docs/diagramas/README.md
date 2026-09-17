# Diagramas

Diagramas UML de las 3 implementaciones, en Mermaid (se renderizan solos en
GitHub/GitLab; para pegarlos en un Word/PDF se pueden exportar como imagen con
el editor de Mermaid o el plugin de VS Code). El detalle narrativo de cada uno
—por qué está armado así— vive en [`../construccion.md`](../construccion.md).

## Login

- [`login-secuencia.md`](./login-secuencia.md) — curso normal + alternativos,
  con el punto exacto del fix del bug de bypass de contraseña.

## Solicitar Amistad / Aceptar-Rechazar Solicitud (patrón State)

- [`amistad-clases-state.md`](./amistad-clases-state.md) — `SolicitudAmistad`
  (contexto) + `EstadoSolicitud`/`Pendiente`/`Aceptada`/`Rechazada`.
- [`amistad-estados.md`](./amistad-estados.md) — transiciones válidas e
  inválidas entre los tres estados.
- [`amistad-secuencia-solicitar.md`](./amistad-secuencia-solicitar.md) —
  validaciones (auto-solicitud, duplicada, ya amigos) y creación de la
  solicitud.
- [`amistad-secuencia-aceptar-rechazar.md`](./amistad-secuencia-aceptar-rechazar.md)
  — autorización, delegación al State, y la transacción única (estado +
  vínculo `Amistad`).

## Notificar Solicitud de Amistad Recibida (patrón Observer + Singleton)

- [`notificar-clases-observer-singleton.md`](./notificar-clases-observer-singleton.md)
  — `Usuario` (Observable) + `Observador` + `NotificationService` (Singleton).
- [`notificar-secuencia.md`](./notificar-secuencia.md) — desde que
  `AmistadService` publica el evento hasta que el mail llega y la home lo
  refleja.

## Faltan / a agregar

Diagramas propios que no dependen del código (van acá cuando el alumno los
tenga): diagrama de casos de uso general, diagrama de paquetes, modelo de
dominio completo si la cátedra lo pide por fuera de lo ya cubierto arriba.
