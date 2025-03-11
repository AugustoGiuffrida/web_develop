import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class CopiesService {
  url = '/api';

  constructor(private httpClient: HttpClient) { }

  addCopy(libroID: number, cantidad: number): Observable<any> {
    const data = {
      libroID: libroID,
      cantidad: Number(cantidad)
    };
    return this.httpClient.post(`${this.url}/libros_copias`, data).pipe(take(1));
  }

  deleteCopy(id: number): Observable<any> {
    return this.httpClient.delete(`${this.url}/libro_copia/${id}`).pipe(take(1));
  }

  // Nuevo método para obtener las copias de un libro
  getCopies(libroID: number): Observable<any> {
    return this.httpClient.get(`${this.url}/libros_copias?libroID=${libroID}`).pipe(take(1));
  }
}
