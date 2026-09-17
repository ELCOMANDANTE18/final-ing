import { Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-register',
  standalone: false,
  templateUrl: './register.component.html',
})
export class RegisterComponent {
  name = '';
  email = '';
  password = '';
  errorMessage = '';
  successMessage = '';

  constructor(private auth: AuthService, private router: Router) {}

  submit(): void {
    this.errorMessage = '';
    this.successMessage = '';

    if (!this.name || !this.email || !this.password) {
      this.errorMessage = 'Por favor complete todos los campos correctamente.';
      return;
    }

    this.auth.register(this.name, this.email, this.password).subscribe({
      next: () => {
        this.successMessage = 'Cuenta creada con éxito. Ya podés iniciar sesión.';
        setTimeout(() => this.router.navigate(['/login']), 1200);
      },
      error: (err) => {
        this.errorMessage = err.error?.error ?? 'No se pudo completar el registro.';
      },
    });
  }
}
