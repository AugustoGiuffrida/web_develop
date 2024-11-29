import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { catchError } from 'rxjs/operators';
import { throwError, Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class RentService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}

  // Función para obtener un préstamo por su ID
  getRent(id: Number) {
  
    return this.httpClient.get(`${this.url}/prestamo/${id}`).pipe(
      catchError((error) => {
        console.error('Error fetching rents:', error);
        return throwError(error);
      })
    );
  }

  // Función para renovar un préstamo
  renewLoan(id: number): Observable<any> {

    return this.httpClient.put(`${this.url}/prestamo/${id}`, null).pipe(
      catchError((error) => {
        console.error('Error al renovar el préstamo:', error);
        return throwError(error);
      })
    );
  }

  // Función para eliminar un préstamo
  deleteLoan(id: number): Observable<any> {

    return this.httpClient.delete(`${this.url}/prestamo/${id}`).pipe(
      catchError((error) => {
        console.error('Error al eliminar el préstamo:', error);
        return throwError(error);
      })
    );
  }
}
