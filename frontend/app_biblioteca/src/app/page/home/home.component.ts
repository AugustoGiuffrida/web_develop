import { Component } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BooksService } from '../../services/books.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  books: any[] = [];
  searchQuery = '';
  filteredBooks = this.books;

  page = 1;
  pages = 1;

  constructor(private route: ActivatedRoute, private booksService: BooksService) {}

  ngOnInit(): void {
    this.getBooks(this.page);
  }

  getBooks(page: number) {
    this.page = page; // Actualiza la página actual
    this.booksService.getBooks(page).subscribe((answer: any) => {
      this.books = answer.libros || [];
      this.filteredBooks = [...this.books];
      this.pages = answer.pages || 1; // Cambia aquí para obtener el número de páginas
    });
  }
  
  
  

  filterBooks() {
    this.filteredBooks = this.books.filter(book =>
      book.titulo.toLowerCase().includes(this.searchQuery.toLowerCase()) ||
      book.autores?.some((autor: any) =>
        (autor.autor_nombre + ' ' + autor.autor_apellidos).toLowerCase().includes(this.searchQuery.toLowerCase())
      )
    );
  }
}

