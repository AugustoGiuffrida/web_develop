import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RentsService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}

  // Obtener préstamos y calcular días restantes
  getRents(page: number, filters: any): Observable<any> {
    // Crear los parámetros de filtrado y paginación para la URL
    let params = `?page=${page}`;
    for (const key in filters) {
      if (filters[key]) {
        params += `&${key}=${filters[key]}`;
      }
    }

    return this.httpClient.get(`${this.url}/prestamos${params}`).pipe(
      map((data: any) => {
        // Calcular días restantes para cada préstamo en la respuesta
        data.prestamos.forEach((prestamo: any) => {
          const fechaDevolucion = new Date(prestamo.fecha_devolucion);
          const hoy = new Date();
          const diff = fechaDevolucion.getTime() - hoy.getTime();
          prestamo.daysLeft = Math.ceil(diff / (1000 * 60 * 60 * 24));
        });
        return data;
      }),
      catchError((error) => {
        console.error('Error fetching rents:', error);
        return throwError(error);
      })
    );
  }

  // Renovar préstamo
  renewLoan(loanId: number): Observable<any> {

    return this.httpClient.put(`${this.url}/prestamos/${loanId}/renew`, {}).pipe(
      take(1),
      catchError((error) => {
        console.error('Error renewing loan:', error);
        return throwError(error);
      })
    );
  }

  // Eliminar préstamo
  deleteLoan(loanId: number): Observable<any> {

    return this.httpClient.delete(`${this.url}/prestamos/${loanId}`).pipe(
      take(1),
      catchError((error) => {
        console.error('Error deleting loan:', error);
        return throwError(error);
      })
    );
  }
}
