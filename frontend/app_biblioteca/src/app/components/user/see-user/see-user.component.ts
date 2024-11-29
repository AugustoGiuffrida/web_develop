import { Component, Input } from '@angular/core';
import { UsuariosService } from '../../../services/usuarios.service';

@Component({
  selector: 'app-see-user',
  templateUrl: './see-user.component.html',
  styleUrls: ['./see-user.component.css']
})
export class SeeUserComponent {

  @Input() id: number = 0;
  @Input() nombre: string = '';
  @Input() apellido: string = '';
  @Input() email: string = '';
  @Input() telefono: string = '0';
  @Input() rol: string = '';

  // Variables para edición
  isEditing: boolean = false;
  updatedNombre: string = '';
  updatedApellido: string = '';
  updatedEmail: string = '';
  updatedTelefono: string = '';

  constructor(private usuariosService: UsuariosService) {}

  // Eliminar usuario
  deleteUser(usuarioID: number): void {
    this.usuariosService.deleteUser(usuarioID).subscribe(() => {
      console.log('Usuario eliminado');
    }, error => {
      console.error('Error al eliminar el usuario:', error);
    });
  }

  // Abrir la pestaña de edición
  onEditUser(): void {
    this.isEditing = true;
    this.updatedNombre = this.nombre;
    this.updatedApellido = this.apellido;
    this.updatedEmail = this.email;
    this.updatedTelefono = this.telefono;
  }

  // Cerrar la pestaña de edición
  closeEdit(): void {
    this.isEditing = false;
  }

  // Actualizar usuario
  updateUser(): void {
    const updatedUserData = {
      nombre: this.updatedNombre,
      apellido: this.updatedApellido,
      email: this.updatedEmail,
      telefono: this.updatedTelefono
    };
  
    console.log('Datos a actualizar:', updatedUserData);
  
    this.usuariosService.updateUser(this.id, updatedUserData).subscribe(
      () => {
        console.log('Usuario actualizado');
        this.isEditing = false; // Cierra la pestaña al actualizar
      },
      error => {
        console.error('Error al actualizar el usuario:', error);
      }
    );
  }
  
}
