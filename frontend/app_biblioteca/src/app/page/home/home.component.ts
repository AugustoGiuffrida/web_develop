import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { BooksService } from '../../services/books.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  books: any[] = [];
  searchQuery = '';
  filteredBooks = this.books;

  page = 1;
  pages = 1;

  constructor(private route: ActivatedRoute, private booksService: BooksService) {}

  ngOnInit(): void {
    this.getBooks(this.page);
  }

  bookCreated(message: string) {
    console.log(message); // Para verificar si el evento se recibe
    this.getBooks(this.page); // Refresca la lista de libros
  }
  
  errorBookCreated(message: string) {
    console.error(message); // Muestra el error en la consola
  }
  
  
  getBooks(page: number) {
    this.page = page; // Actualiza la página actual
    this.booksService.getBooks(page).subscribe((answer: any) => {
      this.books = answer.libros || [];
      this.filteredBooks = [...this.books];
      this.pages = answer.pages || 1; 
    });
  }
  
  filterBooks() {
    const query = this.searchQuery
    this.booksService.getBooks(1,query).subscribe((answer: any) => {
      this.books = answer.libros || [];
      this.filteredBooks = [...this.books];
      this.pages = answer.pages || 1; 
    });
  }
}

