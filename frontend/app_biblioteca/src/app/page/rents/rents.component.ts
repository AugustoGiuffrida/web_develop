import { Component, OnInit } from '@angular/core';
import { RentsService } from '../../services/rents.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-rents',
  templateUrl: './rents.component.html',
  styleUrls: ['./rents.component.css']
})
export class RentsComponent implements OnInit {
  rents: any[] = []; 
  userId: number | null = null; // ID del usuario logueado
  days_left: number = 0;
  page: number = 1;
  pages: number = 0;

  constructor(private rentsService: RentsService, private authService: AuthService) {}

  ngOnInit(): void {
    this.userId = this.authService.UserId; // Obtener ID del usuario logueado
    if (this.userId) {
      this.getUserRents(this.page);
    }
  }

  // Obtener préstamos filtrados por usuario
  getUserRents(page: number): void {
    this.rentsService.getRents(page, { usuarioID: this.userId }).subscribe(
      (response) => {
        this.rents = response.prestamos;
        this.pages = response.pages;
      },
      (error) => {
        console.error('Error fetching user rents:', error);
      }
    );
  }


}
