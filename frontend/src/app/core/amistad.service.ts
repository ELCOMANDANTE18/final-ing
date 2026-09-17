import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

const API_URL = 'http://localhost:5000/amistad';

export interface Solicitud {
  id: number;
  estado: 'pendiente' | 'aceptada' | 'rechazada';
  emisor: { id: number; name: string };
  receptor: { id: number; name: string };
  fecha_creacion: string;
}

@Injectable({ providedIn: 'root' })
export class AmistadService {
  constructor(private http: HttpClient) {}

  solicitar(emailReceptor: string): Observable<Solicitud> {
    return this.http.post<Solicitud>(`${API_URL}/solicitudes`, {
      email_receptor: emailReceptor,
    });
  }

  pendientes(): Observable<Solicitud[]> {
    return this.http.get<Solicitud[]>(`${API_URL}/solicitudes/pendientes`);
  }

  aceptar(id: number): Observable<Solicitud> {
    return this.http.post<Solicitud>(`${API_URL}/solicitudes/${id}/aceptar`, {});
  }

  rechazar(id: number): Observable<Solicitud> {
    return this.http.post<Solicitud>(`${API_URL}/solicitudes/${id}/rechazar`, {});
  }
}
