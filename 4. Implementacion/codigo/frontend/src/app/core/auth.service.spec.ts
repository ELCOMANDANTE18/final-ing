import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { API_URL } from './api-url';
import { AuthService, tokenVencido } from './auth.service';

/** Arma un JWT con el `exp` indicado (en segundos). La firma no importa: el
 *  frontend solo lee el vencimiento; la firma la verifica el backend. */
function jwt(exp: number): string {
  const payload = btoa(JSON.stringify({ sub: '1', exp })).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
  return `encabezado.${payload}.firma`;
}

const enSegundos = (ms: number) => Math.floor(ms / 1000);

describe('AuthService', () => {
  let auth: AuthService;
  let http: HttpTestingController;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: API_URL, useValue: 'http://api.prueba' },
      ],
    });
    auth = TestBed.inject(AuthService);
    http = TestBed.inject(HttpTestingController);
  });

  afterEach(() => http.verify());

  // --- H6: el token vencido no cuenta como sesión ---

  it('sin token no hay sesión', () => {
    expect(auth.isAuthenticated()).toBe(false);
  });

  it('con un token vigente hay sesión', () => {
    localStorage.setItem('access_token', jwt(enSegundos(Date.now()) + 600));
    expect(auth.isAuthenticated()).toBe(true);
  });

  it('con un token vencido no hay sesión y se borra la sesión local (H6)', () => {
    localStorage.setItem('access_token', jwt(enSegundos(Date.now()) - 10));
    localStorage.setItem('umbook_user_name', 'Ana');

    expect(auth.isAuthenticated()).toBe(false);
    expect(localStorage.getItem('access_token')).toBeNull();
    expect(localStorage.getItem('umbook_user_name')).toBeNull();
  });

  it('un token ilegible o sin vencimiento se trata como vencido', () => {
    expect(tokenVencido('esto-no-es-un-jwt')).toBe(true);
    expect(tokenVencido(`a.${btoa(JSON.stringify({ sub: '1' }))}.c`)).toBe(true);
  });

  // --- H10: la dirección del backend sale de API_URL ---

  it('el login usa la dirección configurada y guarda el token (H10)', () => {
    let respuesta: unknown;
    auth.login('ana@test.com', 'password123').subscribe((r) => (respuesta = r));

    const pedido = http.expectOne('http://api.prueba/auth/login');
    expect(pedido.request.method).toBe('POST');
    expect(pedido.request.body).toEqual({ email: 'ana@test.com', password: 'password123' });
    pedido.flush({ access_token: 'tok', user: { id: 1, name: 'Ana', email: 'ana@test.com' } });

    expect(respuesta).toBeTruthy();
    expect(auth.getToken()).toBe('tok');
    expect(auth.getUserName()).toBe('Ana');
  });

  it('el registro usa la dirección configurada (H10)', () => {
    auth.register('Ana', 'ana@test.com', 'password123').subscribe();
    const pedido = http.expectOne('http://api.prueba/auth/register');
    expect(pedido.request.body).toEqual({ name: 'Ana', email: 'ana@test.com', password: 'password123' });
    pedido.flush({ id: 1, email: 'ana@test.com' });
  });
});
