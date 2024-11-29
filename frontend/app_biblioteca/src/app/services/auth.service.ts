import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, take, tap } from 'rxjs';
import { Router } from '@angular/router';
import { jwtDecode } from 'jwt-decode';


@Injectable({
  providedIn: 'root'
})
export class AuthService {
  url = '/api';

  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  isLibrarian(): boolean {
    return this.rol === 'librarian';
  }

  isAdmin(): boolean {
    return this.rol === 'admin';
  }

  isUser(): any {
    return this.rol === 'user';
  }
  
  isLoggedIn(): boolean {
    return this.isAdmin() || this.isLibrarian() || this.isUser();
  }

  get token(): any {
    const token = sessionStorage.getItem('token');
    if (!token) {
      return '';
    } else {
      return token;
    }
  }


  get UserId(): any {
    const token = this.token;
    if (!token) {
      return '';
    }
    try {
      const decoded: any = jwtDecode(token);
      return decoded.id;
    } catch (e) {
      console.error('Invalid token format', e);
      return '';
    }
  }


  get rol(): string {
    const token = this.token;
    if (!token) {
      return '';
    }
    try {
      const decoded: any = jwtDecode(token);
      return decoded.rol;
    } catch (e) {
      console.error('Invalid token format', e);
      return '';
    }
  }


  login(dataLogin: any): Observable<any> {
    return this.httpClient.post(this.url + '/auth/login', dataLogin).pipe(
      take(1),
      tap((response: any) => {
        // Guardar el token en sessionStorage
        sessionStorage.setItem('token', response.token);
      })
    );
  }

  register(dataRegister: any): Observable<any> {
    return this.httpClient.post(this.url + '/auth/register', dataRegister).pipe(
      take(1),
      tap((response: any) => {
        // Guardar el token en sessionStorage
        sessionStorage.setItem('token', response.token);
      })
    );
  }

  logout() {
    // Eliminar el token de sessionStorage al hacer logout
    sessionStorage.removeItem('token');
    this.router.navigateByUrl("home");
  }

  isAuthenticated(): boolean {
    // Verificar si el token está presente en sessionStorage
    return !!sessionStorage.getItem('token');
  }
}