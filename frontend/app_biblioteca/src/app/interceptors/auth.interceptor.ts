import { Injectable } from '@angular/core';
import { HttpEvent, HttpInterceptor, HttpHandler, HttpRequest } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { AuthService } from '../services/auth.service';
import { catchError } from 'rxjs/operators';

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(private authService: AuthService) {}

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
    // Verificar si el token está disponible en sessionStorage
    const authToken = sessionStorage.getItem('token');

    if (authToken) {
      // Si el token está presente, se agrega a la cabecera de la solicitud
      const authReq = req.clone({
        setHeaders: {
          Authorization: `Bearer ${authToken}`
        }
      });
      return next.handle(authReq).pipe(
        catchError(err => {
          if (err.status === 401) {
            this.authService.logout();
          }
          return throwError(err);
        })
      );
    }

    // Si no hay token, se continua con la solicitud sin modificarla
    return next.handle(req);
  }
}

