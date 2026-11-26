import { ChangeDetectorRef, Component } from '@angular/core';

import { NotificationService } from '../core/notification.service';

const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

@Component({ selector: 'app-invite', standalone: false, templateUrl: './invite.component.html' })
export class InviteComponent {
  public email = '';
  public errorMessage = '';
  public successMessage = '';
  public loading = false;

  constructor(private notif: NotificationService, private cdr: ChangeDetectorRef) {}

  public sendInvite(): void {
    this.errorMessage = '';
    this.successMessage = '';
    // CU0010, ca 4.1: formato de correo inválido (rnf 2.1: máximo 254 caracteres).
    if (!EMAIL_RE.test(this.email) || this.email.length > 254) {
      this.errorMessage = 'Ingresá un correo válido.';
      return;
    }

    this.loading = true;
    this.notif.sendInvite(this.email).subscribe({
      // CU0010, paso 6: mensaje de confirmación.
      next: (res) => {
        this.loading = false;
        this.successMessage = `${res.msg} Le llegará un correo a ${this.email}.`;
        this.email = '';
        this.cdr.detectChanges();
      },
      // CU0010, ca 5.1: aviso de fallo; el formulario queda listo para reintentar.
      error: (err) => {
        this.loading = false;
        this.errorMessage = err.error?.msg ?? 'No se pudo enviar la invitación. Intentá de nuevo.';
        this.cdr.detectChanges();
      },
    });
  }
}
