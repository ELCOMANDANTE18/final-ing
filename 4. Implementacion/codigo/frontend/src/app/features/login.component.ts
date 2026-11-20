import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-login',
  standalone: false,
  templateUrl: './login.component.html',
})
export class LoginComponent {
  email = '';
  password = '';
  errorMessage = '';

  constructor(private auth: AuthService, private router: Router, private cdr: ChangeDetectorRef) {}

  submit(): void {
    this.errorMessage = '';

    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor complete todos los campos correctamente.';
      return;
    }

    this.auth.login(this.email, this.password).subscribe({
      // CU0001 paso 6: redirige a la pantalla principal (Welcome), no a /invite.
      next: () => this.router.navigate(['/welcome']),
      error: (err) => {
        this.errorMessage = err.error?.error ?? 'Credenciales incorrectas.';
        this.cdr.detectChanges();
      },
    });
  }
}
