import { ChangeDetectorRef, Component } from '@angular/core';
import { Router } from '@angular/router';

import { AuthService } from '../core/auth.service';

@Component({ selector: 'app-register', standalone: false, templateUrl: './register.component.html' })
export class RegisterComponent {
  public name = '';
  public email = '';
  public password = '';
  public errorMessage = '';
  public successMessage = '';
  public loading = false;

  constructor(private auth: AuthService, private router: Router, private cdr: ChangeDetectorRef) {}

  public register(): void {
    this.errorMessage = '';
    this.successMessage = '';
    // CU0006, ca 5.1: faltan campos o la contraseña no cumple el mínimo.
    if (!this.name || !this.email || this.password.length < 8) {
      this.errorMessage = 'Por favor complete todos los campos correctamente.';
      return;
    }

    this.loading = true;
    this.auth.register(this.name, this.email, this.password).subscribe({
      // CU0006, paso 7: redirige al inicio de sesión.
      next: () => {
        this.successMessage = 'Cuenta creada con éxito. Ya podés iniciar sesión.';
        this.cdr.detectChanges();
        setTimeout(() => this.router.navigate(['/login']), 1200);
      },
      // Seguridad: antes se mostraba JSON.stringify(err), con todo el detalle
      // de la respuesta HTTP. Ahora solo el mensaje del servidor.
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.msg ?? 'No se pudo completar el registro.';
        this.cdr.detectChanges();
      },
    });
  }

  public goToLogin(): void {
    this.router.navigate(['/login']);
  }
}
