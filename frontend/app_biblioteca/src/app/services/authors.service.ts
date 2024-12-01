import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthorsService {
  url = '/api';

  constructor(private httpClient: HttpClient) {}


  getAuthors_by_name_or_lastname(filter: string): Observable<any> {
    return this.httpClient.get('/api/autores?nombre_o_apellido='+filter);
  }

  getAuthor_by_fullname(name: string, lastname: string): Observable<any> {
    return this.httpClient.get('/api/autores?nombre='+name+'&apellido='+lastname);
  }


}