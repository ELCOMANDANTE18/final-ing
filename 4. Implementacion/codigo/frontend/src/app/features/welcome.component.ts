import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';

@Component({ selector: 'app-welcome', standalone: false, templateUrl: './welcome.component.html' })
export class WelcomeComponent {
  public userName: string;

  constructor(private auth: AuthService, private router: Router) {
    this.userName = this.auth.getUserName();
  }

  public goToInvite(): void {
    this.router.navigate(['/invite']);
  }

  public goToLogin(): void {
    // Seguridad: antes solo navegaba a /login y el token seguía guardado,
    // así que la sesión nunca se cerraba.
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
