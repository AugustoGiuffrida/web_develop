import { Component, Input } from '@angular/core';
import { Router } from '@angular/router';
import { BookService } from '../../services/book.service';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-book',
  templateUrl: './book.component.html',
  styleUrls: ['./book.component.css']
})
export class BookComponent {
  @Input() id!: number; 
  @Input() title!: string;
  @Input() author!: any;
  @Input() gender: string = '';
  @Input() quantity: number = 0;
  @Input() image!: string;
  @Input() rating: number = 0;

  // Propiedades para el formulario de edición
  isEditing: boolean = false;
  updatedTitle: string = '';
  updatedAuthor: string = '';
  updatedGender: string = '';
  updatedQuantity: number = 0;


  constructor(private router: Router, private bookService: BookService, private authService: AuthService) {}
  get isAdmin(): boolean {
    return this.authService.isAdmin();
  }

  get isLibrarian(): boolean {
    return this.authService.isLibrarian();
  }

  get isUser(): boolean {
    return this.authService.isUser();
  }

  get authors():string {
    let authors = '';
    try {
      authors = this.author.map((autor: any) => `${autor.autor_nombre} ${autor.autor_apellido}`).join(', ');
    } catch (error) {
      console.log(error);
    }
    return authors;
  }
  
  // Método para navegar a la página de detalles del libro
  navigateToBookDetails() {
    this.router.navigate([`/book`, this.id]); 
  }

  navigateToBookEdit() {
    this.router.navigate([`/book-edit`, this.id]); 
  }

  onDeleteBook() {
    this.bookService.deleteBook(this.id).subscribe(() => {
      window.location.reload();
    });
  }

  onEditBook() {
    this.isEditing = true;
    // Guardamos los valores actuales en el formulario
    this.updatedTitle = this.title;
    this.updatedAuthor = this.authors;
    this.updatedGender = this.gender;
    this.updatedQuantity = this.quantity;

  }

  updateBook() {
    const updatedBookData = {
      titulo: this.updatedTitle,
      autor: this.updatedAuthor,
      cantidad: this.updatedQuantity,
      genero: this.updatedGender
    };

    this.bookService.updateBook(this.id, updatedBookData).subscribe(() => {
      console.log('Libro actualizado');
      this.isEditing = false; // Oculta el formulario
    });
  }

  onRentBook() {
    // Lógica para rentar el libro
  }
}