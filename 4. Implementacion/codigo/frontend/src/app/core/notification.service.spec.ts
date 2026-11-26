import { provideHttpClient } from '@angular/common/http';
import { HttpTestingController, provideHttpClientTesting } from '@angular/common/http/testing';
import { TestBed } from '@angular/core/testing';

import { environment } from '../../environments/environment';
import { API_URL } from './api-url';
import { NotificationService } from './notification.service';

describe('NotificationService', () => {
  it('la invitación usa la dirección configurada (H10)', () => {
    TestBed.configureTestingModule({
      providers: [
        provideHttpClient(),
        provideHttpClientTesting(),
        { provide: API_URL, useValue: 'http://api.prueba' },
      ],
    });
    const http = TestBed.inject(HttpTestingController);

    TestBed.inject(NotificationService).sendInvite('beto@test.com').subscribe();

    const pedido = http.expectOne('http://api.prueba/invite');
    expect(pedido.request.method).toBe('POST');
    expect(pedido.request.body).toEqual({ email: 'beto@test.com' });
    pedido.flush({ msg: 'Invitación enviada.' });
    http.verify();
  });

  it('por defecto la dirección es la de environment.ts (H10)', () => {
    TestBed.configureTestingModule({});
    expect(TestBed.inject(API_URL)).toBe(environment.apiUrl);
  });
});
