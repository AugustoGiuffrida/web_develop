import { Component, OnInit } from '@angular/core';
import { UsuariosService } from '../../services/usuarios.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.css']
})
export class UsersComponent implements OnInit {
  page: number = 1;         
  pages: number = 1;        
  usuarios: any[] = [];     
  selectedRole: string = 'Todos'; 
  selectedNombre: string = ''; 
  selectedApellido: string = '';
  selectedNrPrestamos: number | undefined = undefined; // Cambiar tipo a "number | undefined"
  
  constructor(private usuariosService: UsuariosService) {}

  ngOnInit() {
    this.loadUsers();
    console.log(`Total de páginas inicializado: ${this.pages}`);
  }

  // Método para cargar usuarios con filtros
  loadUsers(page: number = 1) {
    const nombre = this.selectedNombre.trim();
    const apellido = this.selectedApellido.trim();
    const nr_prestamos = this.selectedNrPrestamos ?? undefined;
    const rol = this.selectedRole === 'Todos' ? undefined : this.selectedRole;

    this.usuariosService.getUsers(page, 9, nombre, apellido, nr_prestamos, rol).subscribe(
      (data: any) => {
        if (data && typeof data.pages === 'number') {
          this.pages = data.pages;
        } else {
          console.error('Error: pages no encontrado en la respuesta');
        }
        this.usuarios = data.usuarios;
      },
      (error) => {
        console.error('Error al cargar usuarios:', error);
      }
    );
}


  // Método para manejar el cambio de página
  onPageChange(newPage: number) {
    this.page = newPage;
    this.loadUsers(this.page);  
  }

  // Método para aplicar el filtro de rol
  get filteredUsers() {
    if (this.selectedRole === 'Todos') {
      return this.usuarios; 
    }
    return this.usuarios.filter(usuario => usuario.rol === this.selectedRole); 
  }
}
