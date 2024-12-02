import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { UsuariosService } from '../../services/usuarios.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-profile',
  templateUrl: './profile.component.html',
  styleUrls: ['./profile.component.css']
})
export class ProfileComponent implements OnInit {
  usuarioID: number = 0;
  usuario_nombre: string = '';
  usuario_apellido: string = '';
  usuario_email: string = '';
  usuario_telefono: string = '0';
  rol: string = '';
  editForm!: FormGroup;
  isModalOpen = false;

  constructor(
    private usuariosService: UsuariosService,
    private fb: FormBuilder,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    this.usuarioID = this.authService.UserId; 
    if (this.usuarioID) {
      this.usuariosService.getUser(this.usuarioID).subscribe({
        next: (data) => {
          // Asigna los datos a las variables locales
          this.usuario_nombre = data.usuario_nombre;
          this.usuario_apellido = data.usuario_apellido;
          this.usuario_email = data.usuario_email;
          this.usuario_telefono = data.usuario_telefono;
          this.rol = data.rol;
  
          // Inicializa el formulario con los datos obtenidos
          this.initForm();
        },
      });
    }
  }
  
  
  initForm(): void {
    // Inicializa el formulario con los valores actuales
    this.editForm = this.fb.group({
      usuario_nombre: [this.usuario_nombre, [
        Validators.required, 
        Validators.minLength(4), 
        Validators.pattern('^[a-zA-Z ]*$')
      ]],
      usuario_apellido: [this.usuario_apellido, [
        Validators.required, 
        Validators.minLength(4), 
        Validators.pattern('^[a-zA-Z ]*$')
      ]],
      usuario_email: [this.usuario_email, [Validators.required, Validators.email]],
      usuario_telefono: [this.usuario_telefono, [
        Validators.required, 
        Validators.pattern(/^[0-9]*$/)
      ]],
    });
  }
  

  isFieldInvalid(fieldName: string): boolean {
    const field = this.editForm.get(fieldName);
    return !!(field?.touched && field.invalid); 
  }

  getFieldError(fieldName: string): string | null {
    const field = this.editForm.get(fieldName);
    if (field?.hasError('required')) return 'Este campo es obligatorio';
    if (field?.hasError('minlength')) return `Debe tener al menos ${field.errors?.['minlength'].requiredLength} caracteres`;
    if (field?.hasError('email')) return 'Ingrese un correo electrónico válido';
    if (field?.hasError('pattern')) return 'Formato inválido';
    return null;
  }


  openEditModal(): void {
    this.editForm.patchValue({
      usuario_nombre: this.usuario_nombre,
      usuario_apellido: this.usuario_apellido,
      usuario_email: this.usuario_email,
      usuario_telefono: this.usuario_telefono
    });
    this.isModalOpen = true;
  }
  

  closeModal(): void {
    this.isModalOpen = false;
    window.location.reload();
  }

  submitEdit(): void {
    if (this.editForm.valid) {
      const updatedData = {
        usuario_nombre: this.editForm.value.usuario_nombre,
        usuario_apellido: this.editForm.value.usuario_apellido,
        usuario_email: this.editForm.value.usuario_email,
        usuario_telefono: this.editForm.value.usuario_telefono
      };
  
      this.usuariosService.updateUser(this.usuarioID, updatedData).subscribe(() => {
        // Actualizar los datos locales con los nuevos valores
        this.usuario_nombre = updatedData.usuario_nombre;
        this.usuario_apellido = updatedData.usuario_apellido;
        this.usuario_email = updatedData.usuario_email;
        this.usuario_telefono = updatedData.usuario_telefono;
        
        this.closeModal(); // Cerrar el modal después de actualizar
      });
    }
  }
  
}
