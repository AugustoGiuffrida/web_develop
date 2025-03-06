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

  repeatedAuthor(test_id: number): boolean {
    if (test_id === -1){
      return true
    }
    for (let author of this.selectedAuthors) {
      let id:number = author.autorID 
      if (id == test_id) {
        return true
      }
    }
    return false
  }

  addAuthor() {
    const author = this.bookForm.get('author')?.value
    const name: string = author?.split(' ')[0] || '';
    const lastname: string = author?.split(' ')[1] || '';
    if (!name || !lastname) {
      return; 
    } else {
      this.authorsService.getAuthor_by_fullname(name + " " + lastname).subscribe((answer:any) => {
        const new_author = answer.autores[0];
        const id: number = new_author?.autorID || -1
        if (new_author && !this.repeatedAuthor(id)) { //No permite añadir autores repetidos
          this.selectedAuthors.push(new_author);
          //this.book_authors.push(answer.authors[0]);
          this.bookForm.controls['author'].setValue('');
        }
      })      
    }
    this.bookForm.get('author')?.reset();
  }

  removeAuthor(author: any) {
    this.selectedAuthors = this.selectedAuthors.filter(a => a !== author);
  }

  save() {
    if (this.bookForm.invalid) {
      this.errorBookCreated.emit('Todos los campos son obligatorios y debe haber al menos un autor.');
      return;
    }

    const data = {
      image: "default-book-cover.jpg",
      titulo: this.bookForm.value.title.trim(),
      genero: this.bookForm.value.gender,
      editorial: this.bookForm.value.publisher.trim(),
      autores: this.selectedAuthors.map(author => author.autorID)
    };
    this.booksService.createBook(data).subscribe((answer)=>{
      this.bookForm.reset();
    })
  }
}