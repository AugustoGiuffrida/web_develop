import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';



@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent {
[x: string]: any;
  registerForm!: FormGroup;
  isSubmitting = false; // Indicador de carga

  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {
    this.registerForm = this.formBuilder.group({
      usuario_nombre: ['', Validators.required],
      usuario_apellido: ['', Validators.required],
      usuario_email: ['', [Validators.required, Validators.email]], 
      usuario_contraseña: ['', [Validators.required, Validators.minLength(6), Validators.pattern(/(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/)]],
      confirmPassword: ['', Validators.required],
      usuario_telefono: ['', [Validators.required, Validators.pattern(/^[0-9]*$/)]], 
    }, { validator: this.passwordMatchValidator });
  }

  // Validador para verificar que las contraseñas coincidan
  passwordMatchValidator(form: FormGroup) {
    return form.get('usuario_contraseña')?.value === form.get('confirmPassword')?.value
      ? null : { mismatch: true };
  }

  submit() {
    if (this.registerForm.valid) {
      this.isSubmitting = true; // Activar el indicador de carga
      this.registerUser(this.registerForm.value);
    } else {
      alert('Todos los campos son obligatorios y deben ser válidos!');
    }
  }

  registerUser(registerData: any) {
    this.authService.register(registerData).subscribe({
      next: (response: any) => {
        this.isSubmitting = false; // Desactivar el indicador de carga
        alert('¡Registro exitoso!');
        this.router.navigateByUrl('/login'); // Redirigir a una página post-registro
      },
      error: (error: any) => {
        this.isSubmitting = false; // Desactivar el indicador de carga
        alert('Falló el registro');
        console.error('Error:', error);
      },
    });
  }
}
