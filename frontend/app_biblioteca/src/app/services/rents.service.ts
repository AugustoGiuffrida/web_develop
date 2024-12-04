import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class RentsService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}


  getRents(page: number, filters: any): Observable<any> {
    let params = `?page=${page}`;
    for (const key in filters) {
      if (filters[key]) {
        params += `&${key}=${filters[key]}`;
      }
    }

    return this.httpClient.get(`${this.url}/prestamos${params}`).pipe(
      map((response: any) => response), 
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
