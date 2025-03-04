import { Component, Output, EventEmitter } from '@angular/core';
import { inject } from '@angular/core'; //permite inyectar dependencias fuera del constructor
//garantiza que los controles no retornen valores nulos.
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { RentsService } from '../../services/rents.service';

@Component({
  selector: 'app-add-rent',
  templateUrl: './add-rent.component.html',
  styleUrl: './add-rent.component.css'
})
export class AddRentComponent {
  @Output() rentCreated = new EventEmitter()
  @Output() errorRentCreated = new EventEmitter()

  private fb = inject(NonNullableFormBuilder) //permite construir el formulario reactivo sin declararlo en el constructor

  rentForm = this.fb.group({
    usuarioID: ['', [Validators.required, Validators.pattern(/^[0-9]*$/)]],
    copiaID: ['', [Validators.required, Validators.pattern(/^[0-9]*$/)]],
    fecha_entrega: ['', [Validators.required]],
    fecha_devolucion: ['', [Validators.required]],
  })

  constructor (  private rentsService: RentsService) {}

  createRent() {
    console.log(this.rentForm.value)
    this.rentsService.createLoan(this.rentForm.value).subscribe({
      next: (res) => { //se ejecuta cada vez que el Observable emite un valor.
        console.log(res);
        this.rentCreated.emit() //se emite el evento rentCreated para notificar que la operación fue exitosa.
      },
      error: (err) => { //se ejecuta si hay algún error en la emisión de valores por el Observable
        console.log(err);
        this.errorRentCreated.emit()
      }
    })
  }

  displayError(controlName:string): string | null {
    const control = this.rentForm.get(controlName);
    if (control?.hasError('required')) return 'Este campo es obligatorio';
    if (control?.hasError('pattern')) return 'El identificador debe contener solo números';
    return null;
  }


  get usuarioIdInvalid(): boolean {
    return this.rentForm.controls.usuarioID.invalid && (this.rentForm.controls.usuarioID.touched || this.rentForm.controls.usuarioID.dirty)
  }

  get bookCopyIdInvalid(): boolean {
    return this.rentForm.controls.copiaID.invalid && (this.rentForm.controls.copiaID.touched || this.rentForm.controls.copiaID.dirty)
  }

  get initDateInvalid(): boolean {
    return this.rentForm.controls.fecha_entrega.invalid && (this.rentForm.controls.fecha_entrega.touched || this.rentForm.controls.fecha_entrega.dirty)
  }

  get endDateInvalid(): boolean {
    return this.rentForm.controls.fecha_devolucion.invalid && (this.rentForm.controls.fecha_devolucion.touched || this.rentForm.controls.fecha_devolucion.dirty)
  }

}
