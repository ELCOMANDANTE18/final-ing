import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from './core/auth.service';

@Component({
  selector: 'app-root',
  standalone: false,
  templateUrl: './app.component.html',
})
export class AppComponent {
  constructor(public auth: AuthService, private router: Router) {}

  get userInitial(): string {
    return (this.auth.getUserName().charAt(0) || '?').toUpperCase();
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
