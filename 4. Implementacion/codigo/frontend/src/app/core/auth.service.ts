import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

const TOKEN_KEY = 'access_token';
const NAME_KEY = 'umbook_user_name';

export interface LoginResponse {
  access_token: string;
  user: { id: number; name: string; email: string };
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  private base = 'http://localhost:5000/auth';

  constructor(private http: HttpClient) {}

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

  isAuthenticated(): boolean {
    return !!this.getToken();
  }
}
