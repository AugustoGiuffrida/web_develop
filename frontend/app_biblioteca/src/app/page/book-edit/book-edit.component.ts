import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';
import { AuthorsService } from '../../services/authors.service';
import { BookService } from '../../services/book.service';

@Component({
  selector: 'app-book-edit',
  templateUrl: './book-edit.component.html',
  styleUrls: ['./book-edit.component.css']
})
export class BookEditComponent implements OnInit {

  bookId: number = -1; 
  titulo: string = '';
  image: string = ''; 
  editorial: string = '';
  genero: string = '';
  autores: any[] = [];            // Ya están en el libro
  new_autores: any[] = [];        // id de nuevos autores
  lista_autores: any[] = [];      // Lista de autores dinámica (input)
  libros_autores: any[] = [];
  isLoading = false;
  errors: any = {};


  generos = ['Fiction', 'Non-fiction', 'Mystery', 'Science Fiction', 'Fantasy'];
  editBookForm = new FormGroup({
    title: new FormControl(''),
    author: new FormControl(''),
    editorial: new FormControl(''),
    genero: new FormControl(''),
  })

  constructor(
    private authorsService: AuthorsService,
    private bookService: BookService,
    private route: ActivatedRoute
  ) {}


  ngOnInit() {
    // Obtén el ID del libro desde la URL
    this.bookId = Number(this.route.snapshot.paramMap.get('id'));
    // Llama a la función para obtener los detalles del libro
    this.getBook(this.bookId);

  }

  get str_autores(): string {
    let str_authors: string = '';
    let comma: string = '';
    if (this.autores.length == 0) {
      return 'Desconocido';
    }
    for (let author of this.autores) {
      str_authors += comma + author.autor_nombre + ' ' + author.autor_apellido;
      comma = ', ';
    }
    return str_authors;
  }
 
  repeatedAuthor(test_id: number): boolean {
    for (let id of this.new_autores) {
      if (id == test_id) {
        return true;
      }
    }
    return false;
  }  

  addAuthor() {
    const fullname = this.editBookForm.controls['author'].value;
    if (!fullname) {
      return;
    } else {
      this.authorsService.getAuthor_by_fullname(fullname).subscribe((answer:any) => {
        const id = answer.autores[0].autorID;
        if (id && !(this.repeatedAuthor(id))) {
          this.new_autores.push(id);
          this.libros_autores.push(answer.autores[0]);
          this.editBookForm.controls['author'].setValue('');
        }
      })
    }
  }

  deleteAuthor(id: number): void {
    for (let i = 0; i < this.new_autores.length; i++) {
      if (this.new_autores[i] == id) {
        this.new_autores.splice(i, 1);
      }
    }
    for (let i = 0; i < this.libros_autores.length; i++) {
      if (this.libros_autores[i].autorID == id) {
        this.libros_autores.splice(i, 1);
      }
    }
  }
  
  getAuthors() {
    const query = this.editBookForm.controls['author'].value
    if (typeof query === 'string') {
      this.authorsService.getAuthors_by_name_or_lastname(query).subscribe((answer:any) => {
        this.lista_autores = answer.autores;
      })
    } else {
      this.authorsService.getAuthors_by_name_or_lastname('').subscribe((answer:any) => {
        this.lista_autores = answer.autores;
      })
    }
  }
  
  getBook(id: number) {
    this.bookService.getBook(id).subscribe((data: any) => {
      this.bookId = id;
      this.titulo = data.titulo;
      this.image = data.image;
      this.editorial = data.editorial;
      this.genero = data.genero;
      this.autores = data.autores;
      for (let author of this.autores) {
        this.new_autores.push(author.autorID);
        this.libros_autores.push(author);
      }
    });
  }
  
  uploadImage(event: any): void {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = () => {
        this.image = reader.result as string;
      };
      reader.readAsDataURL(file);
    }
  }
  
  submit() {
    let data: any = {};
    data.titulo = this.editBookForm.controls['title'].value;
    data.editorial = this.editBookForm.controls['editorial'].value;
    data.genero = this.editBookForm.controls['genero'].value;
    data.autores = this.new_autores;
    this.bookService.updateBook(this.bookId, data).subscribe(() => {})
    window.location.reload();
  }

}