import { InjectionToken } from '@angular/core';

import { environment } from '../../environments/environment';

/** Dirección base del backend. Por defecto sale de `environment.apiUrl`; las
 *  pruebas la reemplazan para comprobar que ningún servicio la tiene fija. */
export const API_URL = new InjectionToken<string>('API_URL', {
  providedIn: 'root',
  factory: () => environment.apiUrl,
});
