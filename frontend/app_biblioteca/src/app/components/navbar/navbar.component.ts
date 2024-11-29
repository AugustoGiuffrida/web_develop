import { Component } from '@angular/core';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent {
  isDropdownOpen = false;

  constructor(private authService: AuthService) {}

  // Verificar si el token está presente usando el servicio AuthService
  get isToken() {
    return this.authService.isAuthenticated();  // Verifica si el token está en sessionStorage
  }

  cerrarSesion() {
    this.authService.logout();  // Eliminar el token de sessionStorage
  }

  toggleDropdown() {
    this.isDropdownOpen = !this.isDropdownOpen;
  }
}
