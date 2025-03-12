import { Component, Input, OnInit } from '@angular/core';
import { UsuariosService } from '../../../services/usuarios.service';

@Component({
  selector: 'app-see-user',
  templateUrl: './see-user.component.html',
  styleUrls: ['./see-user.component.css'],
})
export class SeeUserComponent implements OnInit{
  @Input() id: number = 0;
  @Input() nombre: string = '';
  @Input() apellido: string = '';
  @Input() email: string = '';
  @Input() telefono: string = '0';
  @Input() rol: string = '';
  user: any = null;

  // Variables para el modal
  isModalOpen: boolean = false;
  editedRole: string = '';
  roles: string[] = ['admin', 'librarian', 'user', 'pending']; // Opciones válidas

  constructor(private usuariosService: UsuariosService) {}

  ngOnInit() { //se ejecuta al iniciar el componente.
    this.usuariosService.getUser(this.id).subscribe(user => {
    this.user = user;
  });
  }


  // Abrir modal
  openModal(): void {
    this.isModalOpen = true;
    this.editedRole = this.rol; // Prellenar con el rol actual
  }

  // Cerrar modal
  closeModal(): void {
    this.isModalOpen = false;
  }

  // Actualizar el rol del usuario
  updateUserRole(): void {
    if (!this.roles.includes(this.editedRole)) {
      alert('Por favor, selecciona un rol válido.');
      return;
    }

    const updatedData = { rol: this.editedRole }; //datos que se enviarán al backend 
    this.usuariosService.updateUser(this.id, updatedData).subscribe(
      () => {
        this.rol = this.editedRole; // Actualizar el rol en la vista
        this.closeModal(); // Cerrar modal
      },
      (error) => {
        console.error('Error al actualizar el rol:', error);
      }
    );
  }

  getUserImage(user: any) {
    if (!user?.image || user?.image === '') {
      return `https://via.placeholder.com/150?text=${user?.usuario_nombre[0]}${user?.usuario_apellido[0]}`;
    }
    return user?.image;
  }


  // Eliminar usuario
  deleteUser() {
    this.usuariosService.deleteUser(this.id).subscribe(() => {
      window.location.reload();
    });
  } 
}
