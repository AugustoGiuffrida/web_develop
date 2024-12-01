import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { HttpParams } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthorsService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}


  getAuthors_by_name_or_lastname(filter: string): Observable<any> {
    const params = new HttpParams().set('nombre_o_apellido', filter);
    return this.httpClient.get(`${this.url}/autores`, { params });
    
  }
  

  getAuthor_by_fullname(autor_nombre: string, autor_apellido: string): Observable<any> {
    return this.httpClient.get('/api/autores?nombre='+autor_nombre+'&apellido='+autor_apellido);
  }


}