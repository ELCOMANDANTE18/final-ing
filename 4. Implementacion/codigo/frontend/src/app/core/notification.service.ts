import { HttpClient } from '@angular/common/http';
import { Inject, Injectable } from '@angular/core';
import { Observable } from 'rxjs';

import { API_URL } from './api-url';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private base: string;

  constructor(private http: HttpClient, @Inject(API_URL) apiUrl: string) {
    this.base = `${apiUrl}/invite`;
  }

  sendInvite(email: string): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, { email });
  }
}
