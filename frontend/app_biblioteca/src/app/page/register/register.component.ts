import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormGroup, Validators, AbstractControl } from '@angular/forms';
import { AuthService } from '../../services/auth.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.css'],
})
export class RegisterComponent implements OnInit {
  registerForm!: FormGroup;
  isLoading = false;
  submitted = false;
  formInvalid = false;


  constructor(
    private formBuilder: FormBuilder,
    private authService: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.registerForm = this.formBuilder.group(
      {
        usuario_nombre: ['',[Validators.required, Validators.minLength(4), Validators.pattern('^[a-zA-Z ]*$')],],
        usuario_apellido: ['',[Validators.required, Validators.minLength(4), Validators.pattern('^[a-zA-Z ]*$')],],
        usuario_email: ['', [Validators.required, Validators.email]],
        usuario_contrasena: ['',[Validators.required, Validators.minLength(8), Validators.pattern(/(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]/),],],
        confirmPassword: ['', Validators.required],
        usuario_telefono: ['', [Validators.required, Validators.pattern(/^[0-9]*$/)]], 
      },
      { validators: this.passwordsMatchValidator }
    );
  }

  isFieldInvalid(fieldName: string): boolean {
    const field = this.registerForm.get(fieldName);
    return !!(field?.touched && field.invalid); 
  }

  getFieldError(fieldName: string): string | null {
    const field = this.registerForm.get(fieldName);
    if (field?.hasError('required')) return 'Este campo es obligatorio';
    if (field?.hasError('minlength')) return `Debe tener al menos ${field.errors?.['minlength'].requiredLength} caracteres`;
    if (field?.hasError('email')) return 'Ingrese un correo electrónico válido';
    if (field?.hasError('pattern')) return 'Formato inválido';
    return null;
  }

  passwordsMatchValidator(group: AbstractControl): { mismatch: boolean } | null {
    const password = group.get('usuario_contrasena')?.value;
    const confirmPassword = group.get('confirmPassword')?.value;
    return password === confirmPassword ? null : { mismatch: true };
  }

  submit(): void {
    this.submitted = true; // Marcar el formulario como enviado
    if (this.registerForm.invalid) {
      this.formInvalid = true; // Activar alerta general
      return;
    }
    this.formInvalid = false; // Apagar alerta general si es válido
    this.isLoading = true;
  
    const formData = this.registerForm.value;
    this.authService.register(formData).subscribe(
      () => {
        this.isLoading = false;
        this.router.navigate(['/login']);
      },
      (error) => {
        this.isLoading = false;
        console.error('Error al registrar:', error);
      }
    );
  }
  
  
}
