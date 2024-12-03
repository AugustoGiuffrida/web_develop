import { Component, Input, ChangeDetectorRef } from '@angular/core';
import { RentsService } from '../../../services/rents.service';
import { AuthService } from '../../../services/auth.service';

declare var window: any; // Para usar Bootstrap Modal con JavaScript

@Component({
  selector: 'app-see-rents',
  templateUrl: './see-rents.component.html',
  styleUrls: ['./see-rents.component.css']
})
export class SeeRentsComponent {
  @Input() id: number = 0;
  @Input() title: string = 'Default title';
  @Input() user: string = 'Default user';
  @Input() fecha_entrega: string = ''; // Cambiar a string para parsear fechas
  @Input() fecha_devolucion: string = '';
  @Input() image: string = 'media/default-book-cover.jpg';

  @Input() daysLeft: number = 0; // Mover esta propiedad fuera del Input
  selectedLoan: any; // Para almacenar el préstamo seleccionado en el modal
  renewLoanModal: any;

  constructor(private cdr: ChangeDetectorRef, private authService: AuthService, private rentsService: RentsService) {}

  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  get isLibrarian(): boolean {
    return this.authService.isLibrarian();
  }

  get isUser(): boolean {
    return this.authService.isUser();
  }

  ngOnInit() {
    this.renewLoanModal = new window.bootstrap.Modal(document.getElementById('renewLoanModal'));
  }

  // Función para calcular los días restantes
  calculateDaysLeft() {
    if (this.fecha_devolucion) {
      const fechaDevolucion = new Date(this.fecha_devolucion);
      const hoy = new Date();
      const diff = fechaDevolucion.getTime() - hoy.getTime();
      this.daysLeft = Math.ceil(diff / (1000 * 60 * 60 * 24));
    } else {
      this.daysLeft = 0;
    }
  }

  // Abre el modal de renovación y carga la información del préstamo seleccionado
  openRenewModal(loan: any) {
    this.selectedLoan = loan;
    this.renewLoanModal.show();
  }

  // Función para renovar el préstamo
  renewLoan() {
    if (this.selectedLoan) {
      this.rentsService.renewLoan(this.selectedLoan.id).subscribe(
        (response) => {
          console.log(`Préstamo renovado para: ${this.selectedLoan.title}`, response);
          this.renewLoanModal.hide();
        },
        (error) => {
          console.error('Error al renovar el préstamo:', error);
        }
      );
    }
  }

  get expirationReport() {
    return this.daysLeft <= 1;
  }
}
