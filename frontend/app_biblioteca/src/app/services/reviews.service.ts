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
    return this.httpClient.post(this.url+'/reseñas', dataComment).pipe(take(1));
  }

}
