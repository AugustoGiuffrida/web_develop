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
      quantity: Number(cantidad)
    }
    return this.httpClient.post(`${this.url}/libros_copias`, data).pipe(take(1))
  }

  deleteCopy(id: number): Observable<any> {
    return this.httpClient.delete(`${this.url}/libros_copia/${id}`).pipe(take(1))
  }

}
