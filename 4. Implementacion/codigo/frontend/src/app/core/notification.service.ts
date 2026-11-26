import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class NotificationService {
  private base = 'http://localhost:5000/invite';

  constructor(private http: HttpClient) {}

  sendInvite(email: string): Observable<{ msg: string }> {
    return this.http.post<{ msg: string }>(this.base, { email });
  }
}
