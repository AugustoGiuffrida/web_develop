import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BooksService {
url = '/api'

  constructor(private httpClient:HttpClient) { }

  getBooks(page: Number): Observable<any> {
    return this.httpClient.get(`${this.url}/libros?page=${page}&sortby_rating=desc`);
  }

  createBook(dataBook: any): Observable<any> {
    return this.httpClient.post('/api/libros', dataBook);
  }

}
