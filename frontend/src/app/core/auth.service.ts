import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, tap } from 'rxjs';

const API_URL = 'http://localhost:5000';
const TOKEN_KEY = 'umbook_token';

export interface LoginResponse {
  token: string;
  user: { id: number; name: string };
}

@Injectable({ providedIn: 'root' })
export class AuthService {
  constructor(private http: HttpClient) {}

  login(email: string, password: string): Observable<LoginResponse> {
    return this.http
      .post<LoginResponse>(`${API_URL}/auth/login`, { email, password })
      .pipe(tap((res) => localStorage.setItem(TOKEN_KEY, res.token)));
  }

  register(name: string, email: string, password: string): Observable<unknown> {
    return this.http.post(`${API_URL}/auth/register`, { name, email, password });
  }

  logout(): void {
    localStorage.removeItem(TOKEN_KEY);
  }

  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY);
  }

  isAuthenticated(): boolean {
    return this.getToken() !== null;
  }
}
