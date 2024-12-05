import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, take } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  url = '/api';
  
  constructor(private httpClient: HttpClient) { }

  getUsers(page: number = 1, perPage: number = 9, nombre?: string, apellido?: string, nr_prestamos?: number, rol?: string): Observable<any> {

    let params: any = { page, per_page: perPage };
    if (nombre) params.nombre = nombre;
    if (apellido) params.apellido = apellido;
    if (nr_prestamos) params.nr_prestamos = nr_prestamos;
    if (rol && rol !== 'Todos') params.rol = rol;  

    return this.httpClient.get(`${this.url}/usuarios`, { params });
}
  
  getUser(usuarioID: number): Observable<any> {
    return this.httpClient.get(`${this.url}/usuario/${usuarioID}`);
  }

  updateUser(usuarioID: number, userData: any): Observable<any> {
    console.log('Datos enviados al backend:', userData);
    return this.httpClient.put(`${this.url}/usuario/${usuarioID}`, userData, {
      headers: { 'Content-Type': 'application/json' }
    });
  }
  

  // Método para eliminar un usuario
  deleteUser(usuarioID: number): Observable<any> {
    return this.httpClient.delete(`${this.url}/usuario/${usuarioID}`).pipe(
      take(1)
    );
  }


  getUserName(usuarioID: Number): Observable<any> {
    return this.httpClient.get(this.url+`/usuario/${usuarioID}`);
  }

}
