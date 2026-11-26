import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { NgModule } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { BrowserModule } from '@angular/platform-browser';
import { RouterModule, Routes } from '@angular/router';

import { AppComponent } from './app.component';
import { AuthGuard } from './core/auth.guard';
import { TokenInterceptor } from './core/token.interceptor';
import { InviteComponent } from './features/invite.component';
import { LoginComponent } from './features/login.component';
import { RegisterComponent } from './features/register.component';
import { WelcomeComponent } from './features/welcome.component';

const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  // Seguridad: en el original estas dos rutas no tenían guard y se abrían sin sesión.
  { path: 'welcome', component: WelcomeComponent, canActivate: [AuthGuard] },
  { path: 'invite', component: InviteComponent, canActivate: [AuthGuard] },
  { path: '**', redirectTo: '/login' },
];

@NgModule({
  declarations: [AppComponent, LoginComponent, RegisterComponent, InviteComponent, WelcomeComponent],
  imports: [BrowserModule, FormsModule, HttpClientModule, RouterModule.forRoot(routes)],
  providers: [{ provide: HTTP_INTERCEPTORS, useClass: TokenInterceptor, multi: true }],
  bootstrap: [AppComponent],
})
export class AppModule {}
