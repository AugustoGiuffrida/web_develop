import { Component } from '@angular/core';
import { NotificationsService } from '../../services/notifications.service';

@Component({
  selector: 'app-notifications',
  templateUrl: './notifications.component.html',
  styleUrl: './notifications.component.css'
})
export class NotificationsComponent {
  notifications: any[] = [];

  constructor(private notificationsService: NotificationsService) {}

  ngOnInit(): void {
    this.getNotifications();
  }

  trackById(index: number, item: any): any {
    return item.notificacionID;
  }
  

  getNotifications() {
    this.notificationsService.getNotifications().subscribe(
      (answer: any) => {
        if (answer && answer.notificaciones) {
          this.notifications = answer.notificaciones; // Cambié 'notifications' por 'notificaciones'
        } else {
          console.error('Formato de respuesta incorrecto:', answer);
        }
        console.log(this.notifications);
      },
      (error) => {
        console.error('Error al obtener notificaciones:', error);
      }
    );
  }
  
  


}
