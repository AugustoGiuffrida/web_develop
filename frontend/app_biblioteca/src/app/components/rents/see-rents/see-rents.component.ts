import { Component, Input } from '@angular/core';
import { RentsService } from '../../../services/rents.service';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-see-rents',
  templateUrl: './see-rents.component.html',
  styleUrls: ['./see-rents.component.css'],
})
export class SeeRentsComponent {
  @Input() id: number = 0;
  @Input() title: string = 'Default title';
  @Input() userEmail: string = 'Default Email';
  @Input() fecha_entrega: Date = new Date(2024, 0, 1);
  @Input() fecha_devolucion: Date = new Date(2024, 0, 1);
  @Input() image: string = 'media/default-book-cover.jpg';
  @Input() copyID: number = 0;
  @Input() status: string = '';
  @Input() daysLeft: number = 0;
  @Input() rent: any = {};

  isModalOpen: boolean = false;
  editedFechaEntrega: string = '';
  editedFechaDevolucion: string = '';

  constructor(private rentsService: RentsService, private authService: AuthService) {}

  
  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  get isLibrarian(): boolean {
    return this.authService.isLibrarian();
  }


  deleteLoan() {
    this.rentsService.deleteLoan(this.id).subscribe(() => {
      window.location.reload();
    });
  }  

  openModal(): void {
    // Convertir las fechas a instancias de Date si no lo son
    if (!(this.fecha_entrega instanceof Date)) {
      this.fecha_entrega = new Date(this.fecha_entrega);
    }
    if (!(this.fecha_devolucion instanceof Date)) {
      this.fecha_devolucion = new Date(this.fecha_devolucion);
    }
  
    this.isModalOpen = true;
  
    // Convertimos las fechas a formato ISO para los inputs
    this.editedFechaEntrega = this.fecha_entrega.toISOString().split('T')[0];
    this.editedFechaDevolucion = this.fecha_devolucion.toISOString().split('T')[0];
  }
  

  get statusColor(): string {
    if (this.rent.status === 'active') {
      return 'success';
    } if (this.rent.status === 'pending') {
      return 'warning';
    } else {
      return 'danger';
    }
  }


  closeModal(): void {
    this.isModalOpen = false;
    window.location.reload();
  }

  updateLoan(): void {
    const updatedData = {
      fecha_entrega: this.editedFechaEntrega,
      fecha_devolucion: this.editedFechaDevolucion,
    };

    this.rentsService.renewLoan(this.id, updatedData).subscribe(
      () => {
        this.fecha_entrega = new Date(this.editedFechaEntrega);
        this.fecha_devolucion = new Date(this.editedFechaDevolucion);
        this.closeModal();
      },
      (error) => {
        console.error('Error al actualizar el préstamo:', error);
      }
    );
  }
}
