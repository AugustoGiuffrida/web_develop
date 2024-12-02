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
  user: any = {};
  editForm!: FormGroup;
  isModalOpen = false;

  constructor(
    private usuariosService: UsuariosService,
    private fb: FormBuilder,
    private authService: AuthService // Inyectar AuthService
  ) {}

  ngOnInit(): void {
    const userID = this.authService.UserId; // Obtener userID desde AuthService
    if (userID) {
      this.usuariosService.getUser(userID).subscribe({
        next: (data) => {
          this.user = data;
          this.initForm();
        },
        error: (err) => {
          console.error('Error al obtener el usuario:', err);
        }
      });
    } else {
      console.error('No se pudo obtener el ID del usuario loggeado.');
    }
  }

  initForm(): void {
    this.editForm = this.fb.group({
      usuario_nombre: [this.user.usuario_nombre, [Validators.required, Validators.minLength(3)]],
      usuario_apellido: [this.user.usuario_apellido, [Validators.required]],
      usuario_email: [this.user.usuario_email, [Validators.required, Validators.email]],
      usuario_telefono: [this.user.usuario_telefono, [Validators.required]]
    });
  }

  openEditModal(): void {
    this.isModalOpen = true;
  }

  closeModal(): void {
    this.isModalOpen = false;
  }

  submitEdit(): void {
    if (this.editForm.valid) {
      this.usuariosService.updateUser(this.user.usuarioID, this.editForm.value).subscribe(() => {
        Object.assign(this.user, this.editForm.value); // Actualiza los datos locales
        this.closeModal();
      });
    }
  }
}
