import { Injectable } from '@angular/core';
import { CanActivate, Router, UrlTree } from '@angular/router';

import { AuthService } from './auth.service';

/** Protege las pantallas que requieren sesión. En el código original existía
 *  pero ninguna ruta lo usaba: /welcome e /invite se abrían sin iniciar sesión. */
@Injectable({ providedIn: 'root' })
export class AuthGuard implements CanActivate {
  constructor(private auth: AuthService, private router: Router) {}

  canActivate(): boolean | UrlTree {
    if (this.auth.isAuthenticated()) return true;
    return this.router.parseUrl('/login');
  }
}
