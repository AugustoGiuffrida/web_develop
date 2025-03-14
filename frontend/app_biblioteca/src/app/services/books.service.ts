import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class BooksService {
url = '/api'

  constructor(private httpClient:HttpClient) { }

  getBooks(page: Number, query?: string): Observable<any> {
    if (query == undefined) {
      return this.httpClient.get(`${this.url}/libros?page=${page}&sortby_rating=desc`);
    } else {
      return this.httpClient.get(`${this.url}/libros?page=${page}&sortby_rating=desc&titulo=${query}`);
    }
  }

  createBook(dataBook: any): Observable<any> {
    return this.httpClient.post('/api/libros', dataBook);
  }

}