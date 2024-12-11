import { Component, Input } from '@angular/core';
import { NotificationsService } from '../../../services/notifications.service';

@Component({
  selector: 'app-see-notifications',
  templateUrl: './see-notifications.component.html',
  styleUrl: './see-notifications.component.css'
})
export class SeeNotificationsComponent {
  @Input() id: number = 0;
  @Input() titulo: string = 'Título por defecto';
  @Input() descripcion: string = 'Mensaje por defecto';
  @Input() categoria: string = 'info'; // warning, info, danger
  @Input() notification_date: Date = new Date();
  
  constructor(private notificationsService: NotificationsService) {}

  getDateDifference(date: Date): string {
    const currentDate = new Date();
    const notificationDate = new Date(date);
    const differenceInTime = currentDate.getTime() - notificationDate.getTime();
    const differenceInDays = Math.floor(differenceInTime / (1000 * 3600 * 24));

    if (differenceInDays === 0) return 'Hoy';
    if (differenceInDays === 1) return 'Ayer';
    return `${differenceInDays} días atrás`;
  }


  getCategoryLabel(type: string): string {
    switch (type) {
      case 'info':
        return 'Información';
      case 'warning':
        return 'Advertencia';
      case 'danger':
        return 'Peligro';
      case 'success':
        return 'Éxito';
      default:
        return 'Otro';
    }
  }
}
