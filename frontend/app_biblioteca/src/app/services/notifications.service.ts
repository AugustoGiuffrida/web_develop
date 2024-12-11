import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { take } from 'rxjs/operators';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root'
})
export class NotificationsService {

  constructor(private httpClient: HttpClient, private authService: AuthService) { }

  url = '/api'

  getNotifications(): Observable<any> {
    const userId = this.authService.UserId;  // Obtener el ID del usuario desde AuthService
    return this.httpClient.get(`${this.url}/notificaciones?usuarioID=${userId}`);
  }
  

  postNotification(dataNotification: any): Observable<any> {
    return this.httpClient.post(this.url + '/notificaciones', dataNotification).pipe(take(1));
  }

}
