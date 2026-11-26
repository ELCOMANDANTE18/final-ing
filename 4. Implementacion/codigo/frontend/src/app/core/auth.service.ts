import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

import { API_URL } from './api-url';

const TOKEN_KEY = 'access_token';
const NAME_KEY = 'umbook_user_name';

export interface LoginResponse {
  access_token: string;
  user: { id: number; name: string; email: string };
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private base: string;

  constructor(private http: HttpClient, @Inject(API_URL) apiUrl: string) {
    this.base = `${apiUrl}/auth`;
  }

  register(name: string, email: string, password: string): Observable<unknown> {
    return this.http.post(`${this.base}/register`, { name, email, password });
  }

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http.post<LoginResponse>(`${this.base}/login`, { email, password }).pipe(
      tap((res) => {
        if (res && res.access_token) {
          localStorage.setItem(TOKEN_KEY, res.access_token);
          localStorage.setItem(NAME_KEY, res.user.name);
        }
      })
    );
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(NAME_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  getUserName(): string {
    return localStorage.getItem(NAME_KEY) ?? '';
  }

  /** Hay sesión si hay un token guardado y todavía no venció. Antes solo se
   *  miraba si había token, así que con uno vencido se abrían las pantallas
   *  protegidas hasta la primera petición (hallazgo H6). Un token vencido o
   *  ilegible cierra la sesión local. */
  isAuthenticated(): boolean {
    const token = this.getToken();
    if (!token) return false;
    if (tokenVencido(token)) {
      this.logout();
      return false;
    }
    return true;
  }
}

/** Lee el vencimiento (`exp`, en segundos) del JWT sin verificar la firma: eso
 *  lo hace el backend. Un token sin `exp` o ilegible se trata como vencido. */
export function tokenVencido(token: string, ahora: number = Date.now()): boolean {
  try {
    const payload = token.split('.')[1].replace(/-/g, '+').replace(/_/g, '/');
    const { exp } = JSON.parse(atob(payload));
    return typeof exp !== 'number' || exp * 1000 <= ahora;
  } catch {
    return true;
  }
}
