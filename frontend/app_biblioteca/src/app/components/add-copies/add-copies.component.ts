import { Component, Input, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { CopiesService } from '../../services/copies.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-add-copies',
  templateUrl: './add-copies.component.html',
  styleUrls: ['./add-copies.component.css'],
})
export class AddCopiesComponent implements OnInit {
  @Input() libroID!: number; // ID del libro para asociar las copias
  @Input() copies: any[] = []; // Lista de copias actuales

  addQuantity = new FormControl(0, [
    Validators.required,
    Validators.pattern(/^[0-9]*$/),
    Validators.min(1),
    Validators.max(99),
  ]);

  constructor(private copiesService: CopiesService, private route: ActivatedRoute) {}

  ngOnInit() {
    // Extrae el parámetro id de la ruta (si no se pasa desde el padre)
    this.libroID = Number(this.route.snapshot.paramMap.get('id'));
    // Obtener las copias actuales del libro
    this.getCopies();
  }

  openModal(): void {
    this.getCopies(); // Actualiza las copias antes de abrir el modal
  }
  

  get addQuantityInvalid(): boolean {
    return this.addQuantity.invalid && (this.addQuantity.touched || this.addQuantity.dirty);
  }

  get copiesQuantity(): number {
    return this.copies.length;
  }

  getCopies(): void {
    this.copiesService.getCopies(this.libroID).subscribe(
      (response: any) => {
        this.copies = response.libros_copias || [];
      },
      (error) => {
        console.error('Error al obtener copias:', error);
      }
    );
  }

  addCopies(): void {
    if (this.addQuantity.valid && this.addQuantity.value) {
      const cantidad = this.addQuantity.value;
      console.log('Agregar copias:', this.libroID, cantidad);
      this.copiesService.addCopy(this.libroID, cantidad).subscribe(
        (response) => {
          // En vez de usar response.book_copies, refrescamos la lista
          this.getCopies();
          this.addQuantity.reset();
        },
        () => {
          alert('Error al agregar copias.');
        }
      );
    }
  }

  deleteCopy(copyId: number): void {
    this.copiesService.deleteCopy(copyId).subscribe(
      () => {
        this.copies = this.copies.filter((copy) => copy.copiaID !== copyId);
      },
      () => {
        alert('Error al eliminar la copia. Puede estar asociada a un préstamo.');
      }
    );
  } 

  trackByCopyId(index: number, copy: any): number {
    return copy.copiaID;
  }

}
