import { Component, Input } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { CopiesService } from '../../services/copies.service';
import { ActivatedRoute } from '@angular/router';


@Component({
  selector: 'app-add-copies',
  templateUrl: './add-copies.component.html',
  styleUrls: ['./add-copies.component.css'],
})
export class AddCopiesComponent {
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
    this.libroID = Number(this.route.snapshot.paramMap.get('id'));
  }

  

  get addQuantityInvalid(): boolean {
    return this.addQuantity.invalid && (this.addQuantity.touched || this.addQuantity.dirty);
  }

  get copiesQuantity(): number {
    return this.copies.length;
  }

  addCopies(): void {
    if (this.addQuantity.valid && this.addQuantity.value) {
      const cantidad = this.addQuantity.value;
      console.log(this.libroID,cantidad);
      this.copiesService.addCopy(this.libroID, cantidad).subscribe(
        (response) => {
          this.showAlert('Copias agregadas exitosamente.', 'success');
          this.addQuantity.reset();
        },
        () => {
          this.showAlert('Error al agregar copias.', 'danger');
        }
      );
    }
  }

  deleteCopy(copyId: number): void {
    this.copiesService.deleteCopy(copyId).subscribe(
      () => {
        this.copies = this.copies.filter((copy) => copy.id !== copyId);
        this.showAlert('Copia eliminada exitosamente.', 'success');
      },
      () => {
        this.showAlert('Error al eliminar la copia. Puede estar asociada a un préstamo.', 'danger');
      }
    );
  }

  private showAlert(message: string, type: string): void {
    const alertPlaceholder = document.getElementById('alertPlaceholder');
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
      <div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
    alertPlaceholder?.append(wrapper);

    setTimeout(() => wrapper.remove(), 5000);
  }
}
