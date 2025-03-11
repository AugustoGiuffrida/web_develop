import { Component, Input, inject } from '@angular/core';
import { NonNullableFormBuilder, ReactiveFormsModule, Validators } from '@angular/forms';
import { AuthorsService } from '../../services/authors.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-new-author',
  templateUrl: './new-author.component.html',
  styleUrls: ['./new-author.component.css'], // Agrega estilos si los tienes
})
export class NewAuthorComponent {
  @Input() createBook = false;

  private fb = inject(NonNullableFormBuilder);
  private authorService = inject(AuthorsService);

  authorForm = this.fb.group({
    autor_nombre: ['', [
      Validators.required,
      Validators.minLength(4),
      Validators.maxLength(100)
    ]],
    autor_apellido: ['', [
      Validators.required,
      Validators.minLength(4),
      Validators.maxLength(100)
    ]]
  });

  get nameInvalid(): boolean {
    return this.authorForm.controls.autor_nombre.invalid && 
           (this.authorForm.controls.autor_nombre.touched || this.authorForm.controls.autor_nombre.dirty);
  }

  get lastnameInvalid(): boolean {
    return this.authorForm.controls.autor_apellido.invalid && 
           (this.authorForm.controls.autor_apellido.touched || this.authorForm.controls.autor_apellido.dirty);
  }

  async authorExists(): Promise<boolean> {
    const nombre = this.authorForm.controls.autor_nombre.value.trim();
    const apellido = this.authorForm.controls.autor_apellido.value.trim();
    
    if (!nombre || !apellido) return false;
  
    const fullname = `${nombre} ${apellido}`;
    const response = await this.authorService.getAuthor_by_fullname(fullname).toPromise();
    return response.autores.length > 0;
  }
  

  async onSubmit() {
    if (!(await this.authorExists())) {
      this.authorService.addAuthor(this.authorForm.value).subscribe(() => {
        alert('Autor agregado con éxito');
        this.authorForm.reset();
      });
    } else {
      alert('El autor ya existe');
    }
  }
}
