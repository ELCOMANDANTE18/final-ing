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
        // La petición llevaba token y el servidor lo rechazó (vencido o
        // inválido): se cierra la sesión local en vez de dejar un token muerto.
        if (err.status === 401) {
          this.auth.logout();
          this.router.navigate(['/login']);
        }
        return throwError(() => err);
      })
    );
  }
}
