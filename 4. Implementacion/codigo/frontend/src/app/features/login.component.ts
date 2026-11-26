import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';

@Component({ selector: 'app-login', standalone: false, templateUrl: './login.component.html' })
export class LoginComponent {
  public email = '';
  public password = '';
  public errorMessage = '';
  public loading = false;

  constructor(private auth: AuthService, private router: Router, private cdr: ChangeDetectorRef) {}

  public login(): void {
    this.errorMessage = '';
    // CU0001, ca 4.1: campos vacíos (el formato del correo lo valida el servidor).
    if (!this.email || !this.password) {
      this.errorMessage = 'Por favor complete todos los campos correctamente.';
      return;
    }

    this.loading = true;
    this.auth.login(this.email, this.password).subscribe({
      // CU0001, paso 7: redirige a la pantalla principal (Welcome).
      next: () => this.router.navigate(['/welcome']),
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.msg ?? 'Credenciales incorrectas.';
        this.cdr.detectChanges();
      },
    });
  }

  public goToRegister(): void {
    this.router.navigate(['/register']);
  }
}
