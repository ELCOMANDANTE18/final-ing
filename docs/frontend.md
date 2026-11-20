# Frontend — UMBook

**Versión:** 1.1 · **Última modificación:** 20/11/2026 · **Etapa:** Implementación

Angular, con módulos NgModule (sin componentes standalone, sin lazy loading —
convención deliberada, ver nota de versión más abajo). Todo declarado en
`app.module.ts`.

## Cómo correrlo

```bash
cd frontend
npm install
npx ng serve   # sirve en :4200
```

El backend debe estar corriendo en `:5000` (`CORS_ORIGIN` en `backend/.env` tiene
que incluir `http://localhost:4200`, ya viene así en `.env.example`).

> **Nota de versión**: se generó con Angular CLI 22 (`--standalone=false
> --routing=false`) en vez de Angular 15, porque el Node disponible al construir
> este proyecto (v24) no es compatible con Angular CLI 15. Se le pidió
> explícitamente NgModules en vez de standalone para no romper la convención
> descrita acá. Ver [`construccion.md` sección 0](./construccion.md#0-desviaciones-respecto-a-la-especificación-original).

## Estructura

```
frontend/src/app/
  app.module.ts          # Rutas + declaraciones + providers (interceptor JWT)
  app.component.ts/html    # shell, solo <router-outlet>
  core/                     # Servicios transversales
    auth.service.ts          # login/register, guarda token en localStorage,
                              # isAuthenticated()
    auth.guard.ts              # CanActivate, aplicado a /welcome
    token.interceptor.ts        # agrega header Authorization: Bearer <token>;
                                 # si esa request vuelve con 401/422 (JWT
                                 # vencido o corrupto), desloguea y redirige
                                 # a /login solo
    amistad.service.ts           # solicitar/pendientes/aceptar/rechazar/amigos
  features/                # Un componente por pantalla
    login.component.ts/html
    register.component.ts/html
    welcome.component.ts/html  # home: amigos + enviar solicitud + ver
                                # pendientes + aceptar/rechazar (las 3
                                # implementaciones convergen acá)
```

## Diseño visual

Los estilos globales viven en dos archivos, ambos declarados en
`angular.json` → `styles` (**si se edita esa lista hay que reiniciar
`ng serve`**, no alcanza con el watch): `src/styles/chamba.css` (paleta y
componentes base — `.card`, `.btn-primary`, `.btn-ghost`, `.status-pill`,
`.chip`, `.sidebar`, `.avatar-btn`, etc.) y `src/styles.css` (layout propio de
UMBook: `.auth-shell`/`.brand-panel` para login/register, `.request-row`/
`.request-list` para las listas de amigos y solicitudes).

## Rutas (`app.module.ts`)

```
''        → redirect a /login
/login    → LoginComponent
/register → RegisterComponent
/welcome  → WelcomeComponent   (canActivate: [AuthGuard])
```

Login redirige a `/welcome` después de un login exitoso (no a `/invite` — CU0010
no está implementado, ver [`proyecto.md`](./proyecto.md)).

## Convención para una pantalla nueva

1. Componente en `features/<nombre>.component.ts` + `.html` (template en archivo
   separado, lógica simple en el `.ts`, llamadas HTTP a través de un service).
2. Si necesita llamar al backend, service en `core/` usando `HttpClient`, siguiendo
   el estilo de `auth.service.ts`/`amistad.service.ts` (base URL hardcodeada a
   `http://localhost:5000/...`).
3. Declarar el componente y agregar la ruta en `app.module.ts`.
4. Si la pantalla requiere sesión, agregar `canActivate: [AuthGuard]` en la ruta.

---

## Control del documento

| Versión | Fecha | Etapa / Chat | Cambios |
|---|---|---|---|
| 1.1 | 20/11/2026 | Implementación | Se agrega el control de versiones |
