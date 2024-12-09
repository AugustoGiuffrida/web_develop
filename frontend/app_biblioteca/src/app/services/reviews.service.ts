import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class ReviewsService {
  url = '/api';

  constructor(
    private httpClient: HttpClient,
    private router: Router
  ) { }

  postReview(dataComment: any): Observable<any> {
    return this.httpClient.post(this.url+'/resenas', dataComment).pipe(take(1));
  }

  deleteReview(id: number): Observable<any> {
    return this.httpClient.delete(`${this.url}/resena/${id}`).pipe(take(1));
  }

}
