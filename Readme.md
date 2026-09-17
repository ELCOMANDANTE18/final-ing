# UMBook

## Alumno: Victor Gimenez
## Nro Legajo: 61.174

Aplicación de gestión de usuarios (materia Ingeniería de Software). Backend Flask +
frontend Angular, con tres funcionalidades centrales: **Login**, **Solicitar /
Aceptar / Rechazar Amistad** (patrón *State*) y **Notificar Solicitud de Amistad
Recibida** (patrón *Observer* sobre un `NotificationService` *Singleton*).

## Estructura del repo

```
backend/    Flask + SQLAlchemy + SQLite — API REST
frontend/   Angular — UI
docs/       documentación del proyecto (ver índice abajo)
```

## Quickstart

```bash
# Backend — :5000
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env      # completar JWT_SECRET_KEY y credenciales de Gmail (app password)
python run.py

# Frontend — :4200 (en otra terminal)
cd frontend
npm install
npx ng serve
```

`backend/.env` nunca se commitea (ver `backend/.gitignore`). Sin credenciales de
Gmail reales, poner `MAIL_SUPPRESS_SEND=true` en `.env` para probar el flujo sin
que falle el envío de mail.

## Documentación

- [`docs/proyecto.md`](docs/proyecto.md) — casos de uso implementados, alcance y
  decisiones de diseño.
- [`docs/backend.md`](docs/backend.md) — arquitectura, endpoints y convenciones del
  backend.
- [`docs/frontend.md`](docs/frontend.md) — arquitectura, rutas y convenciones del
  frontend.
- [`docs/construccion.md`](docs/construccion.md) — paso a paso de cómo se construyó
  cada implementación y por qué (los patrones de diseño, el bug de login evitado,
  autorización, transacciones).
- [`docs/tareas.md`](docs/tareas.md) — qué falta antes de la defensa.
- [`docs/diagramas/`](docs/diagramas) — diagramas UML del proyecto.
- [`docs/prompt-construccion.md`](docs/prompt-construccion.md) — spec original
  usada para construir el proyecto (documento histórico).
