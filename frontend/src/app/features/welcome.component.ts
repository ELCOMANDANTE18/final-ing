import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';

import { Amigo, AmistadService, Solicitud } from '../core/amistad.service';
import { AuthService } from '../core/auth.service';

@Component({
  selector: 'app-welcome',
  standalone: false,
  templateUrl: './welcome.component.html',
})
export class WelcomeComponent implements OnInit {
  pendientes: Solicitud[] = [];
  amigos: Amigo[] = [];
  emailReceptor = '';
  mensaje = '';
  errorMessage = '';
  userName = '';

  constructor(
    private amistadService: AmistadService,
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.userName = this.auth.getUserName();
    this.cargarPendientes();
    this.cargarAmigos();
  }

  get userInitial(): string {
    return this.userName.charAt(0).toUpperCase();
  }

  cargarAmigos(): void {
    this.amistadService.amigos().subscribe((amigos) => (this.amigos = amigos));
  }

  cargarPendientes(): void {
    // Consulta derivada: no hay una entidad Notificacion separada, esta
    // lista ES la notificación de "solicitud de amistad recibida".
    this.amistadService.pendientes().subscribe((pendientes) => (this.pendientes = pendientes));
  }

  enviarSolicitud(): void {
    this.errorMessage = '';
    this.mensaje = '';

    if (!this.emailReceptor) {
      this.errorMessage = 'Por favor complete todos los campos correctamente.';
      return;
    }

    this.amistadService.solicitar(this.emailReceptor).subscribe({
      next: () => {
        this.mensaje = 'Solicitud enviada.';
        this.emailReceptor = '';
      },
      error: (err) => {
        this.errorMessage = err.error?.error ?? 'No se pudo enviar la solicitud.';
      },
    });
  }

  responder(solicitud: Solicitud, aceptar: boolean): void {
    const accion = aceptar
      ? this.amistadService.aceptar(solicitud.id)
      : this.amistadService.rechazar(solicitud.id);

    accion.subscribe({
      next: () => {
        this.cargarPendientes();
        if (aceptar) {
          this.cargarAmigos();
        }
      },
      error: (err) => {
        this.errorMessage = err.error?.error ?? 'No se pudo procesar la solicitud.';
      },
    });
  }

  logout(): void {
    this.auth.logout();
    this.router.navigate(['/login']);
  }
}
