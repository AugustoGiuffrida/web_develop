import { Component, EventEmitter, Output } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { AuthorsService } from '../../services/authors.service';
import { BooksService } from '../../services/books.service';

@Component({
  selector: 'app-add-book',
  templateUrl: './add-book.component.html',
  styleUrls: ['./add-book.component.css']
})
export class AddBookComponent {
  @Output() bookCreated = new EventEmitter<string>();
  @Output() errorBookCreated = new EventEmitter<string>();

  bookForm: FormGroup;
  books: any[] = [];
  authors: any[] = [];
  selectedAuthors: any[] = [];
  genders = ['Fiction', 'Non-fiction', 'Mystery', 'Science Fiction', 'Fantasy'];

  constructor(
    private fb: FormBuilder,
    private authorsService: AuthorsService,
    private booksService: BooksService
  ) {
    this.bookForm = this.fb.group({
      title: ['', [Validators.required, Validators.minLength(4)]],
      publisher: ['', [Validators.required, Validators.minLength(4)]],
      author: [''],
      gender: ['', Validators.required]
    });
  }

  getAuthors() {
    const query = this.bookForm.get('author')?.value || '';
    this.authorsService.getAuthors_by_name_or_lastname(query).subscribe((response: any) => {
      this.authors = response.autores;
    });
  }

  addAuthor(author: any) {
    if (!this.selectedAuthors.includes(author)) {
      this.selectedAuthors.push(author);
    }
    this.bookForm.get('author')?.reset();
  }

  removeAuthor(author: any) {
    this.selectedAuthors = this.selectedAuthors.filter(a => a !== author);
  }

  save() {
    if (this.bookForm.invalid || this.selectedAuthors.length === 0) {
      this.errorBookCreated.emit('Todos los campos son obligatorios y debe haber al menos un autor.');
      return;
    }

    const data = {
      titulo: this.bookForm.value.title.trim(),
      genero: this.bookForm.value.gender,
      editorial: this.bookForm.value.publisher.trim(),
      autores: this.selectedAuthors.map(author => author.id)
    };

    this.booksService.createBook(data).subscribe(
      (response) => {
        this.bookForm.reset();
        this.selectedAuthors = [];
        this.bookCreated.emit(`Libro creado con éxito: ID ${response.id}`);
      },
      () => this.errorBookCreated.emit('Error al crear el libro. Verifica los datos.')
    );
  }
}
