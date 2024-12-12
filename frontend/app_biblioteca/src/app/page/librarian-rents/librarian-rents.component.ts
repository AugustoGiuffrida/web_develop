import { Component, OnInit } from '@angular/core';
import { RentsService } from '../../services/rents.service';

@Component({
  selector: 'app-librarian-rents',
  templateUrl: './librarian-rents.component.html',
  styleUrls: ['./librarian-rents.component.css']
})
export class LibrarianRentsComponent implements OnInit {
  rents: any[] = [];
  searchQuery: string = '';
  page: number = 1;
  pages: number = 0;
  days_left: number = 0;
  filters: any = {
    fecha_entrega: '',
    fecha_devolucion: '',
    libroID: '',
    usuarioID: ''
  };

  constructor(private rentsService: RentsService) {}

  ngOnInit(): void {
    this.getRents(this.page);
  }

  getRents(page: number): void {
    this.rentsService.getRents(page, this.filters).subscribe(
      (data) => {
        this.rents = data.prestamos;
        this.pages = data.pages; 
        console.log(this.rents);
      },
      (error) => {
        console.error('Error fetching rents:', error);
      }
    );
  }

  // Método para filtrar
  filterRents(): void {
    this.page = 1; // Reiniciar a la primera página al filtrar
    this.getRents(this.page);
  }

  rentCreated() {
    this.showAlert('Prestamo creado con exito', 'success');
    document.documentElement.scrollTo({top:0, behavior: 'smooth'});
    this.getRents(this.page);
  }

  errorRentCreated(): void {
    this.showAlert('Error al crear el prestamo', 'danger');
    document.documentElement.scrollTo({top:0, behavior: 'smooth'});
  }


  showAlert(message: string, type: 'danger' | 'success') {
    const alertPlaceholder = document.getElementById('rentAlertPlaceholder')
    const wrapper = document.createElement('div')
    wrapper.innerHTML = [
      `<div class="alert alert-${type} alert-dismissible" role="alert">`,
      `   <div>${message}</div>`,
      '   <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>',
      '</div>'
    ].join('')
    alertPlaceholder?.append(wrapper)
  }

  }