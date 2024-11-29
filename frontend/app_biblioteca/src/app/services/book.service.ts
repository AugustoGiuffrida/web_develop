import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BookService {
  url = '/api/libro';

  constructor(private httpClient: HttpClient) { }

  getBook(id: Number): Observable<any> {
    return this.httpClient.get(`${this.url}/${id}`);
  }

  deleteBook(id: number): Observable<any> {
    return this.httpClient.delete(`${this.url}/${id}`);
  }

  updateBook(id: number, bookData: any): Observable<any> {
    return this.httpClient.put(`${this.url}/${id}`, bookData);
  }
}
