import {
  HttpErrorResponse,
  HttpEvent,
  HttpHandler,
  HttpInterceptor,
  HttpRequest,
} from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, catchError, throwError } from 'rxjs';

import { AuthService } from './auth.service';

@Injectable()
export class TokenInterceptor implements HttpInterceptor {
  constructor(private auth: AuthService, private router: Router) {}

  intercept(req: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const token = this.auth.getToken();
    if (!token) {
      return next.handle(req);
    }

    const cloned = req.clone({ setHeaders: { Authorization: `Bearer ${token}` } });

    return next.handle(cloned).pipe(
      catchError((err: HttpErrorResponse) => {
        // Solo acá: esta request SÍ llevaba token y el backend la rechazó
        // igual — el JWT venció (401, "Token has expired") o quedó corrupto/
        // manipulado (422, Flask-JWT-Extended lo distingue así). No confundir
        // con el 401 de /auth/login, que va sin token porque el usuario
        // todavía no inició sesión (ese nunca pasa por acá).
        if (err.status === 401 || err.status === 422) {
          this.auth.logout();
          this.router.navigate(['/login']);
        }
        return throwError(() => err);
      })
    );
  }
}
