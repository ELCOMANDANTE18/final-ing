import { TestBed } from '@angular/core/testing';
import { provideRouter, Router, UrlTree } from '@angular/router';

import { AuthGuard } from './auth.guard';

function jwt(exp: number): string {
  return `encabezado.${btoa(JSON.stringify({ sub: '1', exp })).replace(/=+$/, '')}.firma`;
}

describe('AuthGuard', () => {
  let guard: AuthGuard;
  let router: Router;

  beforeEach(() => {
    localStorage.clear();
    TestBed.configureTestingModule({ providers: [provideRouter([])] });
    guard = TestBed.inject(AuthGuard);
    router = TestBed.inject(Router);
  });

  it('deja pasar con un token vigente', () => {
    localStorage.setItem('access_token', jwt(Math.floor(Date.now() / 1000) + 600));
    expect(guard.canActivate()).toBe(true);
  });

  it('sin token redirige a /login', () => {
    const resultado = guard.canActivate() as UrlTree;
    expect(router.serializeUrl(resultado)).toBe('/login');
  });

  it('con el token vencido redirige a /login y cierra la sesión (H6)', () => {
    localStorage.setItem('access_token', jwt(Math.floor(Date.now() / 1000) - 10));

    const resultado = guard.canActivate() as UrlTree;

    expect(router.serializeUrl(resultado)).toBe('/login');
    expect(localStorage.getItem('access_token')).toBeNull();
  });
});
